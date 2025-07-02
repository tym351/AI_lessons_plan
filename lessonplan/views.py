from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import LessonPlan
from django.views.decorators.csrf import csrf_exempt
import json
from .tongyi_api import tongyi_generate_lesson, tongyi_generate_objectives, tongyi_generate_key_difficult, tongyi_generate_content, tongyi_generate_ideological
from django.conf import settings
import requests
import re
from django.utils.safestring import mark_safe
import markdown
from django.contrib.auth.decorators import login_required

# 首页
def home(request):
    return render(request, 'lessonplan/home.html')

# 教案列表
def list_lessonplans(request):
    plans = LessonPlan.objects.all().order_by('-updated_at')
    return render(request, 'lessonplan/list.html', {'plans': plans})

# 生成教案页面（表单）
@login_required(login_url='/admin/login/')
@csrf_exempt
def generate_lessonplan(request):
    if request.method == 'POST':
        theme = request.POST.get('theme', '')
        duration = request.POST.get('duration', '')
        # 修正duration类型，确保为int
        try:
            duration_int = int(duration)
        except Exception:
            duration_int = 45
        ai_only = request.POST.get('ai_only')
        step = request.POST.get('step')
        # 分步AI生成，ai_only参数或step参数时只返回JsonResponse，不保存教案
        if ai_only or step:
            try:
                if not step or step == 'objectives':
                    ai_content = tongyi_generate_objectives(theme, duration_int)
                    # 只要AI有内容就视为成功，不再因包含“【”判定失败
                    if not ai_content or len(ai_content.strip()) == 0:
                        return JsonResponse({
                            'success': False, 
                            'msg': '教学目标生成失败，请检查API密钥或主题内容',
                            'error': ai_content or '未知错误',
                            'objectives': ''
                        })
                    
                    # 清理响应内容，移除多余的说明文字
                    cleaned_content = ai_content.strip()
                    if "教学目标" in cleaned_content:
                        cleaned_content = cleaned_content.split("教学目标")[-1].strip()
                    if "示例" in cleaned_content:
                        cleaned_content = cleaned_content.split("示例")[0].strip()
                    
                    return JsonResponse({
                        'success': True, 
                        'objectives': cleaned_content,
                        'raw': ai_content.strip()
                    })
                elif step == 'key_difficult':
                    objectives = request.POST.get('objectives', '')
                    ai_content = tongyi_generate_key_difficult(theme, duration_int, objectives)
                    key_points = difficult_points = ''
                    key_match = re.search(r'(教学重点|重点)[:：]?([\s\S]*?)(教学难点|难点|$)', ai_content)
                    if key_match:
                        key_points = key_match.group(2).strip()
                    diff_match = re.search(r'(教学难点|难点)[:：]?([\s\S]*)', ai_content)
                    if diff_match:
                        difficult_points = diff_match.group(2).strip()
                    if not key_points and not difficult_points:
                        return JsonResponse({'success': False, 'msg': ai_content or 'AI生成失败', 'key_points': '', 'difficult_points': ''})
                    return JsonResponse({'success': True, 'key_points': key_points, 'difficult_points': difficult_points, 'raw': ai_content.strip()})
                elif step == 'content':
                    objectives = request.POST.get('objectives', '')
                    key_points = request.POST.get('key_points', '')
                    difficult_points = request.POST.get('difficult_points', '')
                    ai_content = tongyi_generate_content(theme, duration_int, objectives, key_points, difficult_points)
                    # 只要AI有内容就视为成功，不再因包含“【”判定失败
                    if not ai_content or len(ai_content.strip()) == 0:
                        return JsonResponse({'success': False, 'msg': ai_content or 'AI生成失败', 'content': ''})
                    return JsonResponse({'success': True, 'content': ai_content.strip()})
                elif step == 'ideological':
                    objectives = request.POST.get('objectives', '')
                    key_points = request.POST.get('key_points', '')
                    difficult_points = request.POST.get('difficult_points', '')
                    content = request.POST.get('content', '')
                    ai_content = tongyi_generate_ideological(theme, duration_int, objectives, key_points, difficult_points, content)
                    # 只要有内容就返回success true
                    if ai_content and len(ai_content.strip()) > 0:
                        return JsonResponse({'success': True, 'ideological_points': ai_content.strip()})
                    return JsonResponse({'success': False, 'msg': ai_content or 'AI生成失败', 'ideological_points': ''})
                else:
                    return JsonResponse({'success': False, 'msg': '未指定生成步骤'})
            except Exception as e:
                return JsonResponse({'success': False, 'msg': f'AI生成异常: {e}'})
        # 正常表单提交，保存教案
        objectives = request.POST.get('objectives', '')
        key_points = request.POST.get('key_points', '')
        difficult_points = request.POST.get('difficult_points', '')
        content = request.POST.get('content', '')
        ideological_points = request.POST.get('ideological', '').strip()
        if not ideological_points:
            ideological_points = auto_add_ideological_points(content)
        plan = LessonPlan.objects.create(
            title=theme,
            duration=duration_int,
            objectives=objectives,
            key_points=key_points,
            difficult_points=difficult_points,
            content=content,
            ideological_points=ideological_points
        )
        return JsonResponse({'success': True, 'msg': '教案已保存', 'id': plan.id})
    return render(request, 'lessonplan/generate.html')

# 修改教案
@login_required(login_url='/admin/login/')
@csrf_exempt
def edit_lessonplan(request, pk):
    plan = get_object_or_404(LessonPlan, pk=pk)
    if request.method == 'POST':
        # 兼容表单提交和json
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        plan.title = data.get('theme', plan.title)
        plan.duration = data.get('duration', plan.duration)
        plan.objectives = data.get('objectives', plan.objectives)
        plan.key_points = data.get('key_points', plan.key_points)
        plan.difficult_points = data.get('difficult_points', plan.difficult_points)
        plan.content = data.get('content', plan.content)
        plan.ideological_points = data.get('ideological', plan.ideological_points)
        if not plan.ideological_points:
            plan.ideological_points = auto_add_ideological_points(plan.content)
        plan.save()
        return JsonResponse({'success': True, 'msg': '教案修改成功', 'id': plan.id})
    # GET请求渲染与generate共用模板
    return render(request, 'lessonplan/generate.html', {
        'plan': plan
    })

# 删除教案
@login_required(login_url='/admin/login/')
@csrf_exempt
def delete_lessonplan(request, pk):
    if request.method == 'POST':
        try:
            plan = LessonPlan.objects.get(pk=pk)
            plan.delete()
            return JsonResponse({'success': True})
        except LessonPlan.DoesNotExist:
            return JsonResponse({'success': False, 'msg': '教案不存在'})
        except Exception as e:
            return JsonResponse({'success': False, 'msg': str(e)})
    return JsonResponse({'success': False, 'msg': '仅支持POST'}, status=405)

# 教案评价
@csrf_exempt
def evaluate_lessonplan(request, pk):
    plan = get_object_or_404(LessonPlan, pk=pk)
    result = {
        'objectives_achieved': check_objectives(plan.objectives, plan.content),
        'key_difficult_distinct': check_key_difficult(plan.key_points, plan.difficult_points),
        'ideological_points': plan.ideological_points or auto_add_ideological_points(plan.content)
    }
    return JsonResponse(result)

# 目标达成校验（简单规则）
def check_objectives(objectives, content):
    return all(obj.strip() in content for obj in objectives.split('\n') if obj.strip())

# 重难点区分校验（简单规则）
def check_key_difficult(key_points, difficult_points):
    return key_points.strip() != difficult_points.strip()

# 自动添加思政点（示例规则）
def auto_add_ideological_points(content):
    if '创新' in content:
        return '创新精神'
    if '团队' in content:
        return '团队协作'
    return '社会主义核心价值观'

# 验证通义千问API Key
def test_tongyi_key(request):
    result = None
    if request.method == 'POST':
        api_key = request.POST.get('api_key') or getattr(settings, 'TONGYI_API_KEY', '')
        url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "qwen-turbo",
            "input": {"prompt": "你好，请返回一句简短的自我介绍。"},
            "parameters": {"result_format": "message"}
        }
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=15)
            resp.raise_for_status()
            result = resp.json().get('output', {}).get('text', 'Key有效，但未返回内容')
        except Exception as e:
            result = f"Key无效或网络异常：{e}"
    return render(request, 'lessonplan/test_tongyi_key.html', {'result': result})

# 教案详情
def lessonplan_to_markdown(plan):
    md = f"""# {plan.title}\n\n**授课时长：** {plan.duration} 分钟\n\n## 教学目标\n{plan.objectives or '-'}\n\n## 教学重点\n{plan.key_points or '-'}\n\n## 教学难点\n{plan.difficult_points or '-'}\n\n## 课程内容\n{plan.content or '-'}\n\n## 思政点\n{plan.ideological_points or '-'}\n"""
    return md

@csrf_exempt
def detail_lessonplan(request, pk):
    plan = get_object_or_404(LessonPlan, pk=pk)
    if request.GET.get('view') == 'markdown':
        md = lessonplan_to_markdown(plan)
        return render(request, 'lessonplan/detail_markdown.html', {'plan': plan, 'markdown_content': md})
    # 渲染HTML视图时将各字段markdown转为html，并去除多余空行
    def md2html(text):
        if not text:
            return ''
        # 去除首尾空行和多余连续空行
        lines = [line.rstrip() for line in text.strip().splitlines()]
        compact_lines = []
        prev_blank = False
        for line in lines:
            if line.strip() == '':
                if not prev_blank:
                    compact_lines.append('')
                prev_blank = True
            else:
                compact_lines.append(line)
                prev_blank = False
        # 自动为无序列表前后补空行，避免被解析为有序列表
        fixed_lines = []
        for i, line in enumerate(compact_lines):
            if (line.strip().startswith('- ') or line.strip().startswith('* ')):
                if i == 0 or compact_lines[i-1].strip() != '':
                    fixed_lines.append('')  # 列表前补空行
            fixed_lines.append(line)
            # 列表后补空行（如果下一个不是列表且不是空行）
            if (line.strip().startswith('- ') or line.strip().startswith('* ')):
                if i+1 == len(compact_lines) or (compact_lines[i+1].strip() != '' and not compact_lines[i+1].strip().startswith(('-', '*'))):
                    fixed_lines.append('')
        compact_text = '\n'.join(fixed_lines)
        html = markdown.markdown(compact_text, extensions=['extra', 'sane_lists'])
        return mark_safe(html)
    context = {
        'plan': plan,
        'objectives_html': md2html(plan.objectives),
        'key_points_html': md2html(plan.key_points),
        'difficult_points_html': md2html(plan.difficult_points),
        'content_html': md2html(plan.content),
        'ideological_points_html': md2html(plan.ideological_points),
    }
    return render(request, 'lessonplan/detail.html', context)

@csrf_exempt
def reflect_lessonplan(request, pk):
    plan = get_object_or_404(LessonPlan, pk=pk)
    from .tongyi_api import tongyi_generate_reflection
    if request.method == 'POST':
        reflection = tongyi_generate_reflection(
            plan.title,
            plan.duration,
            plan.objectives,
            plan.key_points,
            plan.difficult_points,
            plan.content,
            plan.ideological_points
        )
        return JsonResponse({'success': True, 'reflection': reflection})
    return JsonResponse({'success': False, 'msg': '仅支持POST'})
