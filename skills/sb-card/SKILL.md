---
name: sb-card
description: "第二大脑 - 内容可视化技能。将文章核心内容转化为 PNG 视觉卡片，便于分享和记忆。支持长图、信息图、多卡片三种格式。基于李继刚 ljg-card 适配。"
version: "1.0.0"
---

# sb-card: 知识卡片

将内容铸成可见的形态。核心论点进去，PNG 卡片出来。

## 模具类型

| 类型 | 尺寸 | 用途 | 文件名 |
|------|------|------|--------|
| **长图** | 1080 x auto | 单张阅读卡，适合完整文章 | `{date}-{title}-card.png` |
| **信息图** | 1080 x auto | 视觉化呈现，适合数据/流程 | `{date}-{title}-info.png` |
| **多卡** | 1080 x 1440 x N | 系列卡片，适合要点罗列 | `{date}-{title}-{n}.png` |

## 内容来源

从第二大脑文章中提取：
- 标题
- 一句话摘要
- 核心论点（3-5 条）
- 信息增量
- 原文链接

## 设计准则

### 反 AI 痕迹

- ❌ 禁用 Inter 字体
- ❌ 禁用纯黑背景
- ❌ 禁用三等分布局
- ❌ 禁用居中 Hero
- ❌ 禁用 AI 文案腔
- ❌ 禁用假数据

### 品味底线

- 字体：思源黑体/宋体
- 配色：低饱和，暖色调
- 留白：充足，不拥挤
- 层级：清晰，不混乱

## 生成流程

### 1. 提取内容
从文章 Markdown 中提取关键信息。

### 2. 选择模具
根据内容类型自动选择：
- 流程/步骤 → 信息图
- 完整文章 → 长图
- 要点罗列 → 多卡

### 3. 生成 HTML
使用模板填充内容：

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    /* 基础样式 */
    body { font-family: 'Noto Sans SC', sans-serif; }
    .card { width: 1080px; padding: 60px; }
    .title { font-size: 48px; font-weight: bold; }
    .summary { font-size: 28px; color: #666; }
    .points { font-size: 24px; }
  </style>
</head>
<body>
  <div class="card">
    <h1 class="title">{标题}</h1>
    <p class="summary">{一句话摘要}</p>
    <ul class="points">
      <li>{论点1}</li>
      <li>{论点2}</li>
      <li>{论点3}</li>
    </ul>
    <p class="source">来源: {原文链接}</p>
  </div>
</body>
</html>
```

### 4. 截图生成
使用 Playwright/Puppeteer 渲染 HTML 并截图。

```bash
node scripts/capture.js input.html output.png 1080 auto
```

### 5. 存储
- PNG 文件存入 `assets/cards/`
- 在文章中嵌入卡片链接

## 融入第二大脑

每篇文章收录后，自动生成：
1. 长图卡片（完整版）
2. 信息图（核心要点版）

用户可选择下载分享。

## 输出示例

```markdown
## 知识卡片

<img src="./assets/cards/20260309-skills-card.png" width="400">

[下载长图](./assets/cards/20260309-skills-card.png) | [下载信息图](./assets/cards/20260309-skills-info.png)
```

## 依赖

```bash
npm install playwright
npx playwright install chromium
```
