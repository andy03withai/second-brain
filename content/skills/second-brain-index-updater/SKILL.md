---
name: second-brain-index-updater
description: 自动更新第二大脑首页和深度调研索引页面。在新增文章、深度调研报告或每日简报后使用，确保所有索引页面保持最新。扫描 content/ 目录结构，自动生成和更新 index.md 文件中的链接列表。
---

# 第二大脑索引更新器

自动扫描第二大脑目录结构，更新各类索引页面。

## 使用场景

- 新增深度调研报告后更新 deep-research/index.md
- 新增文章后更新首页最新文章列表
- 每日简报生成后更新首页简报链接

## 工作流程

1. **扫描目录结构**
   - deep-research/ - 深度调研报告
   - articles/ - 知识库文章
   - input/daily/ - 每日简报

2. **提取元数据**
   - 从文件 frontmatter 读取标题、日期、标签
   - 提取字数估算

3. **更新索引文件**
   - 按日期倒序排列
   - 更新表格/列表格式
   - 保持原有格式风格

## 脚本使用

```bash
# 更新深度调研索引
python3 scripts/update_deep_research_index.py

# 更新首页文章列表
python3 scripts/update_homepage_articles.py

# 更新所有索引
python3 scripts/update_all_indices.py
```

## 手动更新格式

### 深度调研索引格式

```markdown
| 日期 | 主题 | 深度 | 字数 | 链接 |
|------|------|------|------|------|
| 2026-03-18 | Coding Agent 深度调研 | deep | ~10000 | [[deep-research/2026-03-18-coding-agent-deep-research\|查看报告]] |
```

### 首页最新文章格式

```markdown
### 最新收录
- [[articles/20260318-xxx|文章标题]] - YYYY-MM-DD
```

## 注意事项

- 保持日期格式统一：YYYY-MM-DD
- 链接使用 Obsidian 格式：[[path\|显示文本]]
- 更新后检查页面渲染是否正常
