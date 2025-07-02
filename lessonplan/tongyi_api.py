import requests
import time
from django.conf import settings

def tongyi_generate_objectives(theme, duration):
    api_key = getattr(settings, 'TONGYI_API_KEY', None)
    if not api_key:
        return "【未配置通义千问API密钥】"
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""请作为教学专家，为{duration}分钟的课程“{theme}”制定教学目标, 使用markdown语法，要求如下：\n1. 紧密围绕教学主题，并且能在教学时长内合理完成；\n2. 明确分为三类：知识目标、技能目标、素质目标，每类至少1条；\n3. 每条目标必须可观察、可测量；\n4. 使用数字序号列出3-5条。\n\n示例：\n ###知识目标\n1. 了解XX概念\n2. 熟悉XX并举例说明\n###技能目标\n1. 独立完成XX操作\n2. 熟练XX技能\n###素质目标\n体会XX的价值\n\n请直接返回教学目标，不要包含其他说明。"""
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }
    max_retries = 3
    timeout = 60  # 增加超时时间到60秒
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=timeout)
            resp.raise_for_status()
            result = resp.json()
            print(f"API完整响应: {result}")  # 详细调试日志
            # 统一优化的响应解析逻辑
            try:
                if 'output' in result:
                    output = result['output']
                    if isinstance(output, str):
                        return output
                    elif 'text' in output:
                        return output['text']
                    elif 'choices' in output and len(output['choices']) > 0:
                        return output['choices'][0]['message']['content']
                    elif 'message' in output:
                        return output['message']
                    else:
                        return str(output)
                elif 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                elif 'message' in result:
                    return result['message']
                return f"【无法解析响应结构，完整响应：{result}】"
            except Exception as e:
                return f"【响应解析错误：{str(e)}，完整响应：{result}】"
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return f"【API调用失败：{e}】"
            time.sleep(1)  # 重试前等待1秒

def tongyi_generate_key_difficult(theme, duration, objectives):
    api_key = getattr(settings, 'TONGYI_API_KEY', None)
    if not api_key:
        return "【未配置通义千问API密钥】"
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""请基于以下教学信息，简明生成本课的重点和难点：\n课程主题：{theme}\n课时：{duration}分钟\n教学目标：\n{objectives}\n\n要求：\n1. 直接返回“重点：”和“难点：”两部分内容，内容要精炼，每部分内容可以是一段话，也可以分点列出，但每项不要多于2点；\n2. 语言简洁明了，便于教师理解和把握。\n\n示例：\n重点：\n1. XX概念的理解与应用\n2. XX技能的掌握\n难点：\n1. XX原理的深入理解\n2. XX能力的迁移运用\n\n请直接用markdown语法返回重点和难点内容，不要包含其他说明。"""
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }
    max_retries = 3
    timeout = 60  # 增加超时时间到60秒
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=timeout)
            resp.raise_for_status()
            result = resp.json()
            print(f"API完整响应: {result}")  # 详细调试日志
            # 统一优化的响应解析逻辑
            try:
                if 'output' in result:
                    output = result['output']
                    if isinstance(output, str):
                        return output
                    elif 'text' in output:
                        return output['text']
                    elif 'choices' in output and len(output['choices']) > 0:
                        return output['choices'][0]['message']['content']
                    elif 'message' in output:
                        return output['message']
                    else:
                        return str(output)
                elif 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                elif 'message' in result:
                    return result['message']
                return f"【无法解析响应结构，完整响应：{result}】"
            except Exception as e:
                return f"【响应解析错误：{str(e)}，完整响应：{result}】"
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return f"【API调用失败：{e}】"
            time.sleep(1)  # 重试前等待1秒

def tongyi_generate_content(theme, duration, objectives, key_points, difficult_points):
    api_key = getattr(settings, 'TONGYI_API_KEY', None)
    if not api_key:
        return "【未配置通义千问API密钥】"
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""请设计{duration}分钟的课程教学流程：\n\n【设计要求】\n1. 导入要激发兴趣、联系已有知识，时长为1-3分钟\n2. 讲解要分解难点、突出重点\n3. 活动要互动性强、巩固知识\n4. 总结要提炼要点、布置作业，时长大概3分钟\n\n【参考信息】\n教学目标：\n{objectives}\n\n教学重点：\n{key_points}\n\n教学难点：  \n{difficult_points}\n\n请按时间顺序详细描述每个环节的教学活动，流程内容无需出现“课程名称"、"教学流程设计"或“课程结束”等字样。"""
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }
    max_retries = 3
    timeout = 60  # 增加超时时间到60秒
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=timeout)
            resp.raise_for_status()
            result = resp.json()
            print(f"API完整响应: {result}")  # 详细调试日志
            # 统一优化的响应解析逻辑
            try:
                if 'output' in result:
                    output = result['output']
                    if isinstance(output, str):
                        return output
                    elif 'text' in output:
                        return output['text']
                    elif 'choices' in output and len(output['choices']) > 0:
                        return output['choices'][0]['message']['content']
                    elif 'message' in output:
                        return output['message']
                    else:
                        return str(output)
                elif 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                elif 'message' in result:
                    return result['message']
                return f"【无法解析响应结构，完整响应：{result}】"
            except Exception as e:
                return f"【响应解析错误：{str(e)}，完整响应：{result}】"
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return f"【API调用失败：{e}】"
            time.sleep(1)  # 重试前等待1秒

def tongyi_generate_ideological(theme, duration, objectives, key_points, difficult_points, content):
    api_key = getattr(settings, 'TONGYI_API_KEY', None)
    if not api_key:
        return "【未配置通义千问API密钥】"
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""结合以下教学信息：
主题：{theme}
教学目标：
{objectives}

教学内容：
{content}

请根据教学目标和教学内容设计课程思政融入点，要求：
1. 包含：
   - 思政元素（如工匠精神、创新意识等）
   - 具体融入方式（如案例、讨论等）
   - 预期育人效果
2. 自然衔接专业内容

示例：
1. **名称**：以科学分类为基，育生态责任之思  
2. **课程思政目标**：培养学生的科学精神与生态保护意识，增强对植物多样性的尊重与保护责任感。  
3. **课程思政内容简述**：通过椰子分类的学习，引导学生认识到自然界的多样性不仅是科学研究的对象，更是人类可持续发展的基础资源。结合我国在植物资源保护和利用方面的成就，激发学生关注生态环境、尊重自然规律的意识。 
### 4. 融入设计：
- **教学时间**: 第2周  
- **教学单元**: 椰子分类与特征识别  
- **融入方式**: 
    (1) 案例融入：讲述中国在热带作物研究中的成就，如海南椰子产业的发展与生态保护实践，说明科学分类对于资源合理利用的重要性。  
    (2) 讨论融入：组织学生围绕“为什么我们需要了解椰子的不同种类？”展开讨论，引导他们思考植物多样性对生态、经济、文化等方面的意义。  
    (3) 情境融入：在讲解椰子分类依据时，结合当前全球气候变化背景，引导学生思考如何通过科学分类更好地保护和利用自然资源。  
- **教学方法**:
    (1) 讲授法：在讲解椰子分类知识的同时，穿插我国在植物资源保护方面的政策与成果，增强学生的民族自豪感和责任感。  
    (2) 讨论法：设置开放性问题，如“如果你是科学家，你会如何保护椰子这一重要资源？”，鼓励学生从多角度思考生态保护问题。  
    (3) 实践法：布置作业时，要求学生结合所学知识，撰写一份关于椰子分类与生态保护的小报告，提升其综合应用能力与社会责任感。  
- **教学实施过程**
    (1) 在讲解高种、矮种和杂交种椰子的特征时，适时引入我国在椰子品种选育和生态保护方面的案例，强调科学分类对农业发展和生态保护的价值。  
    (2) 在小组活动后，引导学生反思：“如果我们不了解椰子的分类，会对农业生产或生态保护带来什么影响？”从而深化学生对科学分类意义的理解。  
    (3) 在总结环节中，教师强调植物多样性是大自然赋予人类的宝贵财富，呼吁学生从自身做起，关注生态环境，践行绿色发展理念。  
- **教学效果预期**:  
学生能够理解科学分类不仅是知识学习的一部分，更是实现人与自然和谐共生的重要基础。通过本节课的学习，增强学生的生态责任意识，激发他们对自然科学的兴趣与热爱，培养其尊重自然、保护环境的自觉行动力。

请直接返回思政点内容。"""
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }
    max_retries = 3
    timeout = 60  # 增加超时时间到60秒
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=timeout)
            resp.raise_for_status()
            result = resp.json()
            print(f"API完整响应: {result}")  # 详细调试日志
            
            # 统一优化的响应解析逻辑
            try:
                if 'output' in result:
                    output = result['output']
                    if isinstance(output, str):
                        return output
                    elif 'text' in output:
                        return output['text']
                    elif 'choices' in output and len(output['choices']) > 0:
                        return output['choices'][0]['message']['content']
                    elif 'message' in output:
                        return output['message']
                    else:
                        return str(output)
                elif 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                elif 'message' in result:
                    return result['message']
                return f"【无法解析响应结构，完整响应：{result}】"
            except Exception as e:
                return f"【响应解析错误：{str(e)}，完整响应：{result}】"
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return f"【API调用失败：{e}】"
            time.sleep(1)  # 重试前等待1秒

def tongyi_generate_reflection(theme, duration, objectives, key_points, difficult_points, content, ideological_points):
    api_key = getattr(settings, 'TONGYI_API_KEY', None)
    if not api_key:
        return "【未配置通义千问API密钥】"
    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    prompt = f"""请作为教学教研专家，分析如下教案内容，判断其中可能存在的问题、不足或改进空间，并给出具体的教学反思建议，要求：\n1. 先简要指出教案中存在的主要问题或不足（如目标不清、重难点不突出、内容不连贯、思政点不自然等）；\n2. 针对每个问题给出详细的反思和改进建议；\n3. 语言简明、条理清晰，适合教师自我提升。\n\n【教案信息】\n课程主题：{theme}\n课时：{duration}分钟\n教学目标：\n{objectives}\n教学重点：\n{key_points}\n教学难点：\n{difficult_points}\n课程内容：\n{content}\n思政点：\n{ideological_points}\n\n请直接返回反思内容，不要包含其他说明。"""
    data = {
        "model": "qwen-turbo",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        },
        "parameters": {
            "result_format": "message"
        }
    }
    max_retries = 3
    timeout = 60
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=data, timeout=timeout)
            resp.raise_for_status()
            result = resp.json()
            try:
                if 'output' in result:
                    output = result['output']
                    if isinstance(output, str):
                        return output
                    elif 'text' in output:
                        return output['text']
                    elif 'choices' in output and len(output['choices']) > 0:
                        return output['choices'][0]['message']['content']
                    elif 'message' in output:
                        return output['message']
                    else:
                        return str(output)
                elif 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
                elif 'message' in result:
                    return result['message']
                return f"【无法解析响应结构，完整响应：{result}】"
            except Exception as e:
                return f"【响应解析错误：{str(e)}，完整响应：{result}】"
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                return f"【API调用失败：{e}】"
            time.sleep(1)
