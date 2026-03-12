# 每日简报 v4.0 升级设计文档

## 参考：AI 资讯速览方法论

## 核心升级

### 1. 信息来源全面国际化

全部信息源来自英文互联网，不使用中文信息源。

**公司官方博客**:
- OpenAI Blog
- Anthropic Blog
- Google AI Blog
- DeepMind Blog
- Meta AI Blog
- NVIDIA Blog

**科技媒体**:
- MIT Technology Review
- The Verge
- TechCrunch
- Ars Technica
- Wired
- 404 Media

**社区与论文**:
- Hacker News (AI相关讨论)
- HuggingFace Daily Papers
- HuggingFace Trending
- arXiv (cs.AI, cs.LG, cs.CL, cs.CV, cs.RO)

**行业 Newsletter**:
- Import AI (Jack Clark)
- Ben's Bites
- Latent Space
- Interconnects (Nathan Lambert)
- AI Snake Oil (Arvind Narayanan)
- One Useful Thing (Ethan Mollick)
- The Batch (Andrew Ng)
- TLDR AI

**独立博客**:
- Simon Willison's Weblog

### 2. 筛选机制 v4.0

#### 2.1 算法评分维度

| 维度 | 权重 | 说明 |
|------|------|------|
| **多源交叉验证** | 最高 | 同一事件被多个独立信息源报道 |
| **社区热度** | 高 | Hacker News 点赞/评论、HF upvotes |
| **来源权威度** | 高 | 官方博客 > 一线媒体 > 聚合Newsletter |
| **时效性** | 中 | 24小时内的新闻获得加分 |
| **机构背景** | 中 | Google/DeepMind/OpenAI 等发布 |

#### 2.2 分层候选池

- **重点关注池**: 评分超过阈值，多源验证的重要新闻
- **值得关注池**: 其他值得关注的条目
- **快讯池**: 简短的资讯片段

#### 2.3 AI 选题原则

- 每天选出 **3 个值得深入报道的故事**
- 故事覆盖不同领域，避免同质化
- 每个故事综合多条相关信息源
- 参考近几天已发布的内容，避免重复选题
- 叙事方式刻意错开，避免阅读疲劳

### 3. 产品形态 v4.0

#### 内容结构

```
📰 AI 每日简报 - YYYY年MM月DD日

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 今日三大焦点
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

01 [标题] - [来源]
   [一句话核心要点]
   
02 [标题] - [来源]
   [一句话核心要点]
   
03 [标题] - [来源]
   [一句话核心要点]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 深度报道
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### 01 [故事标题]

[正文 - AI撰写，遵循新闻写作规范]

**关键信息**:
- [要点1]
- [要点2]
- [要点3]

**来源**: [链接1] | [链接2] | [链接3]

---

### 02 [故事标题]
...

### 03 [故事标题]
...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ 快讯
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- [快讯1] - [来源]
- [快讯2] - [来源]
- [快讯3] - [来源]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 数据看板
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- 监控信息源: XX 个
- 今日筛选条目: XXX 条
- 入选主题报道: 3 篇
- 入选快讯: X 条

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

> 人只调算法，不碰内容。
> 所有内容均可点击来源链接验证。
> 收录使用 `/sb 链接 批注`
```

### 4. 技术实现

#### 4.1 信息源采集模块

需要实现以下采集器：

```python
SOURCES = {
    # RSS 源
    'rss': [
        {'name': 'OpenAI Blog', 'url': 'https://openai.com/blog/rss.xml'},
        {'name': 'Anthropic Blog', 'url': 'https://www.anthropic.com/rss.xml'},
        {'name': 'DeepMind Blog', 'url': 'https://deepmind.google/blog/rss.xml'},
        {'name': 'Google AI Blog', 'https': '//ai.googleblog.com/feeds/posts/default'},
        {'name': 'MIT Tech Review', 'url': 'https://www.technologyreview.com/feed/'},
        {'name': 'The Verge AI', 'url': 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml'},
        {'name': 'TechCrunch', 'url': 'https://techcrunch.com/category/artificial-intelligence/feed/'},
        {'name': 'Wired AI', 'url': 'https://www.wired.com/tag/artificial-intelligence/feed/'},
        {'name': 'Simon Willison', 'url': 'https://simonwillison.net/atom.xml'},
    ],
    # API 源
    'api': [
        {'name': 'Hacker News', 'fetcher': 'fetch_hn_ai_stories'},
        {'name': 'HuggingFace Papers', 'fetcher': 'fetch_hf_daily_papers'},
        {'name': 'arXiv', 'fetcher': 'fetch_arxiv_recent'},
        {'name': 'Import AI', 'fetcher': 'fetch_import_ai_archive'},
        {'name': 'Ben\'s Bites', 'fetcher': 'fetch_bens_bites'},
    ]
}
```

#### 4.2 评分算法 v4.0

```python
def score_item_v4(item):
    """v4.0 评分算法"""
    score = 0
    
    # 1. 多源交叉验证 (0-30分)
    source_count = item.get('cross_sources', 0)
    if source_count >= 3:
        score += 30
    elif source_count == 2:
        score += 20
    elif source_count == 1:
        score += 10
    
    # 2. 社区热度 (0-25分)
    hn_score = item.get('hacker_news_score', 0)
    if hn_score > 200:
        score += 25
    elif hn_score > 100:
        score += 20
    elif hn_score > 50:
        score += 15
    elif hn_score > 20:
        score += 10
    
    hf_upvotes = item.get('hf_upvotes', 0)
    if hf_upvotes > 50:
        score += 15
    elif hf_upvotes > 20:
        score += 10
    
    # 3. 来源权威度 (0-20分)
    source_type = item.get('source_type', '')
    if source_type == 'company_official':
        score += 20
    elif source_type == 'tier1_media':
        score += 15
    elif source_type == 'newsletter':
        score += 10
    elif source_type == 'blog':
        score += 8
    
    # 4. 时效性 (0-15分)
    age_hours = item.get('age_hours', 48)
    if age_hours < 6:
        score += 15
    elif age_hours < 12:
        score += 12
    elif age_hours < 24:
        score += 10
    elif age_hours < 48:
        score += 5
    
    # 5. 机构背景 (0-10分)
    if item.get('from_top_institution'):
        score += 10
    
    return min(score, 100)
```

#### 4.3 AI 选题和内容生成

```python
def ai_select_stories(candidate_items, date_str, recent_topics):
    """AI 选出3个值得深入报道的故事"""
    
    # 准备候选条目信息
    candidates_info = []
    for item in candidate_items[:20]:  # 取前20个高分条目
        candidates_info.append({
            'title': item['title'],
            'source': item['source'],
            'summary': item['summary'][:200],
            'score': item['score'],
            'category': item.get('category', 'general')
        })
    
    # 构建 prompt
    prompt = f"""
作为AI新闻编辑，从以下候选条目中选出3个最值得今日深入报道的故事。

今日日期: {date_str}
近3天已报道主题: {recent_topics}

选题原则:
1. 故事覆盖不同领域，避免同质化
2. 每个故事有明确的新闻价值和影响
3. 叙事方式错开，避免阅读疲劳
4. 不与近3天已报道主题重复
5. 优先选择多源验证的重要事件

候选条目:
{json.dumps(candidates_info, indent=2, ensure_ascii=False)}

请返回3个选中故事的索引(0-19)，并简要说明选题理由。
格式: [index1, index2, index3]
"""
    
    # 调用 AI 进行选择
    # ...
    
    return selected_indices, reasons

def generate_story_content(selected_items):
    """生成深度报道内容"""
    
    for item in selected_items:
        prompt = f"""
基于以下信息源撰写一篇新闻风格的深度报道。

主题: {item['title']}
来源: {item['source']}
相关信息: {item['summary']}
相关链接: {item['urls']}

写作要求:
1. 用客观中立的语气
2. 开头一句话总结核心要点
3. 正文300-500字
4. 包含3-5个关键信息点
5. 末尾列出所有信息来源链接
6. 不添加主观评论或情绪化表达

请直接输出正文，不要添加任何元评论。
"""
        # 调用 AI 生成内容
        # ...
```

### 5. 中立性原则

**人只调算法，不碰内容**：
- ✅ 信息源权重、筛选规则、编辑规则 —— 由人制定
- ✅ 监控产出质量，发现问题后调整规则和算法
- ❌ 不直接修改某篇文章的内容或选题

**修复方式**：
- 如果内容有问题 → 改规则
- 如果选题有偏差 → 调评分权重
- 绝不手动改单篇文章

### 6. 已知局限声明

在简报末尾加入以下说明：

```markdown
---

## 📌 关于本简报

**信息源**: 全部来自英文互联网 (OpenAI/Anthropic/Google/DeepMind 官方博客, TechCrunch, MIT Tech Review, Hacker News, Import AI 等)

**筛选机制**: 算法评分 (多源交叉验证 + 社区热度 + 来源权威度 + 时效性) + AI选题

**中立性**: 人只调算法，不碰内容。所有文章由AI基于规则自动生成，未经人工编辑。

**局限**:
- 信息全部来自英文互联网，国内AI动态覆盖有限
- 文章由AI撰写，可能存在对原始信息的理解偏差
- 评分偏重社区热度和机构权威度，小团队突破性工作可能被低估
- 无追踪更新，除非后续本身成为新的新闻事件

**反馈**: 如发现事实错误或选题偏差，会调整对应规则，而非修改单篇文章。
```

### 7. 实施计划

#### Phase 1: 信息源采集器 (1-2天)
- [ ] 实现 RSS 采集器 (OpenAI, Anthropic, DeepMind, Google AI, MIT Tech Review, The Verge, TechCrunch, Wired, Simon Willison)
- [ ] 实现 API 采集器 (Hacker News, HF Daily Papers, arXiv)
- [ ] 实现 Newsletter 采集器 (Import AI, Ben's Bites)

#### Phase 2: 评分和筛选 (1天)
- [ ] 实现 v4.0 评分算法
- [ ] 实现分层候选池
- [ ] 实现去重和关联分析 (识别同一事件的多源报道)

#### Phase 3: AI 选题和内容生成 (1-2天)
- [ ] 实现 AI 选题模块
- [ ] 实现深度报道生成
- [ ] 实现快讯生成

#### Phase 4: 整合和测试 (1天)
- [ ] 整合所有模块
- [ ] 测试完整流程
- [ ] 部署并观察效果

#### Phase 5: 迭代优化 (持续)
- [ ] 根据产出质量调整评分规则
- [ ] 优化选题策略
- [ ] 添加/移除信息源
