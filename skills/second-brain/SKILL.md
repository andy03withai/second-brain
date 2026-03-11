---
name: second-brain
description: "第二大脑文章收录工作流。处理 /sb 命令，自动提取内容、生成白话摘要、写作消化提示、知识卡片，推送到 GitHub Pages。自动更新首页和时间线。用于构建个人知识管理系统。"
version: "1.1.0"
---

# second-brain: 第二大脑收录 v1.1

完整的文章收录工作流。输入链接，输出结构化知识笔记。

## 触发方式

### 文章收录

用户消息以 `/sb` 开头：

**单链接**
```
/sb https://example.com/article 你的批注（可选）
```

**多链接（主题收录）**
```
/sb https://podcast.com/ep1 https://blog.com/transcript 播客+文字稿
```

## 工作流步骤

### 1. 解析命令
提取 URL 和批注。

### 2. 创建文章
生成基础 Markdown 文件到 `content/articles/`。

### 3. 应用处理器
根据内容类型选择处理器：

| 类型 | 处理器 | 功能 |
|------|--------|------|
| 学术论文 | paper | 检测 arXiv，生成论文速读模板 |
| 普通文章 | plain | 白话化：一句话 + 一段话摘要 |
| 所有文章 | writes | 写作消化：提取论点 + 生成问题 |
| 所有文章 | card | 知识卡片：生成 HTML 视觉卡片 |

### 4. 自动更新
- 更新 `index.md` 最新收录列表
- 更新 `timeline.md` 时间线
- 推送到 GitHub

### 5. 返回链接
返回具体文章页面地址（包含文章标题，而非纯数字ID）。

## 用户偏好

### URL 格式偏好
- **必须包含文章标题**：如 `articles/20260311-skillcraft-llm-agent-skills`
- **避免纯数字ID**：如 `articles/20260311-260300718` ❌
- **目的**：方便一眼识别内容

### 返回格式偏好
- **必须返回具体页面网址**：如 `https://andy03withai.github.io/second-brain/articles/20260311-article-name`
- **不能返回根地址**：如 `https://andy03withai.github.io/second-brain/` ❌
- **说明**：GitHub Pages 部署需要 2-3 分钟

## 配置要求

### 文件结构
```
second-brain/
├── content/articles/     # 文章输出目录
├── scripts/
│   ├── process_article.py    # 主处理器
│   ├── paper_processor.py    # 论文检测
│   ├── plain_processor.py    # 白话化
│   ├── writes_processor.py   # 写作消化
│   ├── card_processor.py     # 知识卡片
│   ├── index_updater.py      # 首页自动更新
│   └── timeline_updater.py   # 时间线自动更新
└── .github/workflows/    # 自动部署
```

## 输出格式

生成的文章包含：

```markdown
---
title: "文章标题"
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

## 我的批注
用户原始批注
```

## 使用示例

### 论文链接
```
/sb https://arxiv.org/abs/2501.12345
```
自动启用论文速读模式，URL 将包含论文标题。

### 普通文章
```
/sb https://36kr.com/p/3702322702922116
```
自动提取文章标题，生成友好 URL。

### 带批注
```
/sb https://example.com/article 这篇文章关于...
```

## 注意事项

- 只有 `/sb` 开头的消息才会触发
- 网站更新需 2-3 分钟
- 部分网站内容无法自动抓取，需手动补充
