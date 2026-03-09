---
name: second-brain
description: "第二大脑文章收录工作流。处理 /sb 命令，自动提取内容、生成白话摘要、写作消化提示、知识卡片，推送到 GitHub Pages。用于构建个人知识管理系统。"
version: "1.0.0"
---

# second-brain: 第二大脑收录

完整的文章收录工作流。输入链接，输出结构化知识笔记。

## 触发方式

用户消息以 `/sb` 开头：
```
/sb https://example.com/article 你的批注（可选）
```

## 工作流步骤

### 1. 解析命令
提取 URL 和批注。

### 2. 创建文章
生成基础 Markdown 文件到 `content/articles/`。

### 3. 应用技能处理
依次调用 4 个子处理器：

| 顺序 | 处理器 | 功能 |
|------|--------|------|
| 1 | paper | 检测 arXiv，生成论文速读模板 |
| 2 | plain | 白话化：一句话 + 一段话摘要 |
| 3 | writes | 写作消化：提取论点 + 生成问题 |
| 4 | card | 知识卡片：生成 HTML 视觉卡片 |

### 4. 提交部署
```bash
git add .
git commit -m "Add article: ..."
git push origin main
```

GitHub Actions 自动构建部署到 Pages。

## 配置要求

### 环境变量
```bash
export SB_REPO="/path/to/second-brain"
export SB_CONTENT="$SB_REPO/content/articles"
```

### 依赖
- Python 3.8+
- Git
- Quartz 站点结构

### 文件结构
```
second-brain/
├── content/articles/     # 文章输出目录
├── scripts/
│   ├── process_article.py    # 主处理器
│   ├── paper_processor.py    # 论文检测
│   ├── plain_processor.py    # 白话化
│   ├── writes_processor.py   # 写作消化
│   └── card_processor.py     # 知识卡片
└── .github/workflows/    # 自动部署
```

## 输出格式

生成的文章包含：

```markdown
---
title: "来源域名"
date: YYYY-MM-DD
source: "URL"
tags: [待分类]
---

## 核心摘要
> 一句话摘要

一段话摘要...

## 关键信息抽取
| 项目 | 内容 |
...

## 通过写作消化
- 核心论点
- 写作问题
- 思考方向

## 信息增量
| 概念 | 本资料 | 当前认知 |
...

## 我的批注
用户原始批注
```

## 使用示例

### 基本用法
```
/sb https://github.com/mgechev/skills-best-practices
```

### 带批注
```
/sb https://xiaoyuzhoufm.com/episode/xxx 李继刚专访，值得学习
```

### 论文链接
```
/sb https://arxiv.org/abs/2501.12345
```
自动启用论文速读模式。

## 注意事项

- 只有 `/sb` 开头的消息才会触发
- 网站更新需 2-3 分钟
- 部分网站内容无法自动抓取，需手动补充
