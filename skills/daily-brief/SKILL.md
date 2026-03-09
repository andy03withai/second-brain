---
name: daily-brief
description: "每日简报生成器。自动采集 arXiv、Hugging Face Daily Papers 等信息源，基于多信号评分系统筛选出高质量论文，生成结构化日报。支持AI、Agent、自动驾驶、多模态、具身智能等主题。每天定时运行或手动触发。"
version: "2.0.0"
---

# daily-brief: 每日简报

自动化的信息筛选与简报生成系统。从海量论文中筛选出值得你关注的10篇。

## 核心能力

### 多源采集
- **arXiv**: 实时抓取 cs.AI/LG/CL/CV/RO/MM 分类
- **Hugging Face Daily Papers**: 社区投票精选
- **Semantic Scholar**: 引用数查询

### 智能筛选（6维评分）

| 维度 | 权重 | 说明 |
|------|------|------|
| 关键词匹配 | +5/词 | 主题相关度，最多30分 |
| 顶级机构 | +15 | Google/DeepMind/OpenAI/Stanford等 |
| 顶级会议 | +20 | CVPR/ICML/NeurIPS/ICLR等 |
| 引用数量 | +0~15 | 100+/500+/1000+ |
| HF社区热度 | +0~10 | Hugging Face upvotes 20+/50+ |
| 代码开源 | +8 | 提供GitHub/Code |

### 输出格式

```markdown
## 📊 今日概览
- 扫描论文: 156 篇 (arXiv + HF Daily)
- 入选推荐: 10 篇
- 平均分: 78

## 🌟 TOP 推荐
### 1. 论文标题
- 评分: 92/100 (🏛️ DeepMind | 📜 ICLR | 📈 引用:523)
- 摘要: ...
- 链接: [arXiv]

## 📋 其他值得关注的
...
```

## 触发方式

### 定时自动（推荐）
每天早上 **6:00**（上海时间）自动运行，生成5个主题的简报。

### 手动触发
```bash
python3 scripts/daily_brief.py --date 20260309
```

### 指定主题
```bash
python3 scripts/daily_brief.py --topic autonomous-driving
```

## 配置

### 主题配置 (config/topics.json)

```json
{
  "ai": {
    "name": "AI 前沿",
    "arxiv_cats": ["cs.AI", "cs.LG", "cs.CL"],
    "keywords": ["大语言模型", "LLM", "Transformer", "GPT"]
  },
  "autonomous-driving": {
    "name": "自动驾驶",
    "arxiv_cats": ["cs.CV", "cs.RO"],
    "keywords": ["端到端", "VLA", "BEV", "Occupancy"]
  }
}
```

### 评分权重调整 (config/scoring.json)

```json
{
  "base_score": 40,
  "keyword_weight": 5,
  "institution_bonus": 15,
  "conference_bonus": 20,
  "citation_tiers": [100, 500, 1000],
  "citation_bonus": [5, 10, 15],
  "hf_upvote_tiers": [20, 50],
  "hf_bonus": [5, 10],
  "code_bonus": 8
}
```

## 输出目录

```
content/input/
├── {YYYYMMDD}-index.md          # 每日总索引
├── ai/{YYYYMMDD}.md              # AI前沿简报
├── agent/{YYYYMMDD}.md           # Agent简报
├── autonomous-driving/           # 自动驾驶简报
├── multimodal/                   # 多模态简报
└── embodied-intelligence/        # 具身智能简报
```

## 与第二大脑集成

```
daily-brief 生成简报
      ↓
用户浏览 /sb 收录有价值的
      ↓
second-brain 处理 → 白话化 → 写作消化 → 发布
```

## 依赖

```bash
pip install requests urllib3
```

## API 限制说明

- **arXiv**: 无限制，但建议间隔1秒请求
- **Semantic Scholar**: 免费版 100次/5分钟
- **HF Daily**: 无限制

建议每日运行1次，避免触发限制。

## 版本历史

- **v2.0.0** (P1): 新增 HF Daily Papers + Semantic Scholar引用数
- **v2.1.0** (P2, 计划中): 新增会议等级检测 + Twitter/GitHub热度
- **v2.2.0** (计划中): 个性化推荐，基于历史收录调整权重

---

*设计参考: 李自然 AI论文简报、Karpathy RSS聚合、李继刚信息筛选方法论*
