# 🧠 Second Brain

基于 Quartz 的个人知识管理系统。

## 功能

- 收集：通过飞书发送链接自动收录
- 整理：自动分类和标签
- 学习：提取关键信息，建立知识结构
- 消化：信息增量分析
- 发布：自动生成静态网站

## 访问

🌐 **在线访问**: https://andy03withai.github.io

## 本地开发

```bash
npm install
npx quartz build --serve
```

## 目录结构

```
content/
├── index.md          # 主页
├── templates/        # 模板
│   └── article.md    # 文章收录模板
└── ...               # 收录的文章
```
