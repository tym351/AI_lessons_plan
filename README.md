# Django 教案系统

本项目是一个基于 Django 的智能教案管理系统，支持教案的 AI 分步生成、编辑、评价（目标达成校验、重难点区分、自动添加课程思政点）、美观的前后端交互与展示。

## 主要功能
- 教案分步 AI 生成（目标、重难点、内容、思政点，支持 Markdown 格式）
- 教案增删改查，支持异步删除与编辑
- 教案评价（目标达成、重难点区分、自动推断思政点）
- 列表、详情、编辑、删除等页面美化与交互优化
- 详情页支持 HTML/Markdown 双视图，Markdown 可一键复制
- 通义千问 API Key 配置与调试

## 快速开始
1. 安装依赖：`pip install -r requirements.txt`
2. 迁移数据库：`python manage.py migrate`
3. 启动服务：`python manage.py runserver`
4. 配置通义千问 API Key（在 settings.py 中设置 `TONGYI_API_KEY`，或通过前端页面调试）

## 依赖环境
- Python 3.8+
- Django >= 4.0
- requests
- markdown

## 目录结构
- teachsys/         # Django 主项目
- lessonplan/       # 教案管理 app
- requirements.txt  # 依赖列表

## 亮点说明
- 分步 AI 生成：每个教案环节可单独 AI 生成，支持 Markdown 格式，提示词精细优化
- 详情页双视图：HTML 渲染与 Markdown 源码一键切换，Markdown 支持一键复制
- 页面美观：卡片式分组、渐变配色、响应式布局，交互友好
- API Key 调试：前端可直接测试和配置通义千问 API Key
- 代码结构清晰，易于二次开发

## 后续开发建议
- 增加用户权限与多角色支持
- 教案导出 PDF/Word
- AI 生成内容的多模型支持
- 教案内容智能推荐与分析

---
如有问题或建议，欢迎 issue 或 PR！
