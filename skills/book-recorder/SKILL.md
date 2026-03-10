---
name: book-recorder
description: "书籍记录和读书笔记管理。使用 /book 命令记录想读的书、添加读书笔记。支持亚马逊、豆瓣等链接提取信息。"
version: "1.0.0"
---

# book-recorder: 书籍记录管理

记录想读的书籍，管理读书笔记。

## 触发方式

### 添加新书
```
/book https://amazon.com/... 想读这本书，关于分布式系统的
```

### 添加读书笔记
```
/book 《设计数据密集型应用》 今天读到第三章，关于一致性算法的部分很有启发
```

## 工作流程

### 1. 解析命令
- 提取 URL（如有）
- 提取书名（从 URL 或用户输入）
- 提取批注/笔记内容

### 2. 信息提取（如果是链接）
- 从亚马逊页面提取：书名、作者、简介、评分
- 从豆瓣页面提取：书名、作者、简介、豆瓣评分
- 生成结构化书籍信息

### 3. 分类识别
根据内容自动识别分类：
- **计算机系统**: 操作系统、网络、系统架构
- **分布式计算**: 分布式系统、一致性、共识
- **数据工程**: 数据库、大数据、数据管道
- **自动驾驶**: 自动驾驶、机器人、VLA
- **AI 与 Agents**: AI、大模型、智能体
- **人文社科**: 历史、哲学、社会学、心理学

### 4. 创建书籍页面
生成 Markdown 文件到对应分类目录：
```
content/books/{category}/{book-slug}.md
```

### 5. 更新分类索引
在分类索引中添加书籍条目

### 6. 提交部署
```bash
git add .
git commit -m "Add book: {书名}"
git push origin main
```

## 书名匹配规则

支持多种方式引用书籍：

| 方式 | 示例 | 说明 |
|------|------|------|
| **完整书名** | `/book 《设计数据密集型应用》 ...` | 最精确 |
| **简称/别名** | `/book DDIA ...` | 常用缩写 |
| **部分书名** | `/book 数据密集型 ...` | 模糊匹配 |

**别名管理**: 在书籍页面的 frontmatter 中记录常见简称
```yaml
aliases: ["DDIA", "数据密集型应用", "Designing Data-Intensive Applications"]
```

## 语音笔记处理

对于语音转文字的笔记，进行轻度处理：

**处理内容**:
- 去除重复词汇（"这个这个" → "这个"）
- 去除填充词（"嗯"、"啊"、"那个"）
- 修正明显的语音识别错误（根据上下文）
- 保持段落和停顿结构

**保留内容**:
- 口语化的表达方式
- 个人的语气和情感
- 不完整的句子（思维流动感）
- 自问自答的形式

**示例**:
```
原始语音: "嗯...今天读到第三章，那个...关于一致性算法的部分，嗯，挺有意思的，就是...CAP定理那个部分"

处理后: "今天读到第三章，关于一致性算法的部分挺有意思的，就是 CAP 定理那个部分。"
```

## 输出格式

### 书籍页面模板
```markdown
---
title: "{书名}"
author: "{作者}"
category: "{分类}"
status: "想读|在读|已读"
source_url: "{原始链接}"
publication_date: "YYYY"  # 出版年份
douban_rating: "{豆瓣评分}"
douban_rating_count: "{豆瓣评分人数}"  # 如：12,345人
amazon_rating: "{亚马逊评分}"
amazon_rating_count: "{亚马逊评分人数}"
goodreads_rating: "{Goodreads评分}"
goodreads_rating_count: "{Goodreads评分人数}"
date_added: "YYYY-MM-DD"
tags: [标签]
aliases: [别名1, 别名2]
---

# {书名}

**作者**: {作者}  
**出版年份**: YYYY  
**分类**: {分类}  
**状态**: {状态}

## 简介

{书籍简介}

## 评分

| 平台 | 评分 | 评分人数 | 链接 |
|------|------|----------|------|
| 豆瓣 | {评分} | {人数} | [链接] |
| 亚马逊 | {评分} | {人数} | [链接] |
| Goodreads | {评分} | {人数} | [链接] |

## 我的批注

{用户添加书籍时的批注}

## 读书笔记

### 2026-03-10
{笔记内容}

### 2026-03-15
{笔记内容}

---

*添加于 YYYY-MM-DD*
*最后更新: YYYY-MM-DD*
```

## 使用示例

### 示例 1: 亚马逊链接
```
/book https://www.amazon.com/Designing-Data-Intensive-Applications-Reliable-Maintainable/dp/1449373321 分布式系统经典，必读
```

**输出**:
- 创建 `content/books/distributed-computing/designing-data-intensive-applications.md`
- 提取书名: Designing Data-Intensive Applications
- 提取作者: Martin Kleppmann
- 分类: 分布式计算
- 状态: 想读

### 示例 2: 豆瓣链接
```
/book https://book.douban.com/subject/26176885/ 朋友推荐
```

**输出**:
- 创建对应分类下的书籍页面
- 提取豆瓣评分
- 记录批注: "朋友推荐"

### 示例 3: 添加读书笔记
```
/book 《设计数据密集型应用》 今天读到第三章，关于一致性算法的部分很有启发，特别是 CAP 定理的实践指导
```

**输出**:
- 找到已存在的书籍页面
- 追加读书笔记（带日期）
- 更新最后更新时间

## 分类规则

| 关键词 | 分类 |
|--------|------|
| 操作系统、网络、体系结构 | 计算机系统 |
| 分布式、一致性、共识、CAP | 分布式计算 |
| 数据库、大数据、数据管道 | 数据工程 |
| 自动驾驶、机器人、VLA | 自动驾驶 |
| AI、机器学习、Agent、大模型 | AI 与 Agents |
| 历史、哲学、社会学、心理学 | 人文社科 |

## 注意事项

1. **链接提取失败**: 如果无法提取信息，使用用户提供的标题创建基础页面
2. **重复检测**: 检查是否已有相同书籍（书名+作者）
3. **状态管理**: 支持 想读/在读/已读 三种状态切换
4. **读书笔记**: 每段笔记自动添加日期，原始保留用户输入

## 文件结构

```
content/books/
├── index.md                          # 书单总览
├── computer-systems/
│   ├── index.md                      # 分类索引
│   └── book-slug.md                  # 单本书籍
├── distributed-computing/
│   ├── index.md
│   └── ...
├── data-engineering/
│   ├── index.md
│   └── ...
├── autonomous-driving/
│   ├── index.md
│   └── ...
├── ai-agents/
│   ├── index.md
│   └── ...
└── humanities-social-sciences/
    ├── index.md
    └── ...
```
