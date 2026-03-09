# Daily Brief Skill

## 快速开始

```bash
# 安装依赖
pip install requests urllib3

# 运行每日简报生成
python3 scripts/daily_brief.py

# 指定日期
python3 scripts/daily_brief.py --date 20260309

# 指定主题
python3 scripts/daily_brief.py --topic autonomous-driving
```

## 目录结构

```
daily-brief/
├── SKILL.md              # 技能说明
├── README.md             # 本文件
├── config/
│   ├── topics.json       # 主题配置
│   └── scoring.json      # 评分权重配置
└── scripts/
    └── daily_brief.py    # 主脚本
```

## 配置说明

### 添加新主题

编辑 `config/topics.json`：

```json
"new-topic": {
  "name": "新主题名称",
  "arxiv_cats": ["cs.XX"],
  "keywords": ["关键词1", "关键词2"],
  "hf_filter": ["hf-tag"]
}
```

### 调整评分权重

编辑 `config/scoring.json`：

```json
{
  "base_score": 40,
  "dimensions": {
    "keyword": {"weight_per_hit": 5, "max_bonus": 30},
    "institution": {"bonus": 15}
  }
}
```

## 输出示例

见 `../../content/input/ai/20260309.md`

## 集成方式

### 作为独立脚本

```bash
python3 scripts/daily_brief.py --output /path/to/output
```

### 作为OpenClaw Skill

将本目录复制到 OpenClaw skills 目录：

```bash
cp -r daily-brief ~/.openclaw/skills/
```

### 作为Cron任务

```bash
# 每天早上6点运行
0 6 * * * cd /path/to/daily-brief && python3 scripts/daily_brief.py
```

## 数据来源

- **arXiv**: https://arxiv.org/help/api
- **HF Daily Papers**: https://huggingface.co/api/daily-papers
- **Semantic Scholar**: https://api.semanticscholar.org/

## 许可证

MIT
