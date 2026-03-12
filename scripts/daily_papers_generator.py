#!/usr/bin/env python3
"""
每日论文推荐生成器 v1.0
生成结构化简报
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

FOCUS_AREAS = {
    'autonomous-driving': {'name': '自动驾驶', 'emoji': '🚗'},
    'physical-ai': {'name': 'Physical AI', 'emoji': '🏗️'},
    'ai-agent': {'name': 'AI Agent', 'emoji': '🤖'}
}

def load_papers(date_str):
    """加载采集的论文"""
    data_file = Path(f"/root/.openclaw/workspace/second-brain/data/daily_papers/papers_{date_str}.json")
    
    if not data_file.exists():
        print(f"❌ 找不到数据文件: {data_file}")
        return []
    
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data.get('papers', [])

def select_top_papers(papers, area_key, max_count=3):
    """为每个领域选择TOP论文"""
    area_papers = []
    
    for paper in papers:
        classifications = paper.get('classifications', [])
        for c in classifications:
            if c['area'] == area_key:
                area_papers.append(paper)
                break
    
    # 按评分排序，取前N篇
    area_papers.sort(key=lambda x: x.get('score', 0), reverse=True)
    return area_papers[:max_count]

def generate_paper_summary(paper, index):
    """生成单篇论文的解读"""
    title = paper.get('title', '')
    summary = paper.get('summary', '')
    url = paper.get('url', '')
    arxiv_id = paper.get('arxiv_id', '')
    
    # 提取关键信息
    badges = []
    if paper.get('top_institution'):
        badges.append(f"🏛️ {paper['top_institution']}")
    if paper.get('conference'):
        badges.append(f"📜 {paper['conference']}")
    if paper.get('has_code'):
        badges.append("💻 开源代码")
    if paper.get('hf_upvotes', 0) > 20:
        badges.append(f"👍 HF {paper['hf_upvotes']}")
    if paper.get('citation_count', 0) > 10:
        badges.append(f"📈 引用 {paper['citation_count']}")
    
    badge_str = " | ".join(badges) if badges else ""
    
    # 生成解读
    content = f"""### {index}. {title}

**一句话总结**: {summary[:120]}...

**为什么重要**:
{generate_importance(paper)}

**技术要点**:
- {extract_key_point(summary)}

**{badge_str}**

**链接**: [{url}]({url})

---
"""
    
    return content

def generate_importance(paper):
    """生成'为什么重要'段落"""
    classifications = paper.get('classifications', [])
    inst = paper.get('top_institution', '')
    
    points = []
    
    # 基于领域的重要性
    for c in classifications:
        area = c['area']
        if area == 'autonomous-driving':
            points.append("自动驾驶技术栈的关键进展")
        elif area == 'physical-ai':
            points.append("物理世界建模的重要突破，直接影响机器人与仿真能力")
        elif area == 'ai-agent':
            points.append("AI Agent能力的实质性提升，有明确的应用落地路径")
    
    # 基于来源的重要性
    if inst:
        points.append(f"来自{inst}的权威研究，方法论经过严格验证")
    
    if paper.get('conference'):
        points.append("已被顶级会议接收，学术质量有保障")
    
    if paper.get('has_code'):
        points.append("开源代码 available，可快速验证和复用")
    
    if not points:
        points.append("在相关领域提出了新的思路或方法")
    
    return "\n".join([f"- {p}" for p in points[:3]])

def extract_key_point(summary):
    """从摘要提取关键技术点"""
    # 简化处理：取摘要的前150个字符
    text = summary[:150]
    sentences = text.split('. ')
    if sentences:
        return sentences[0] + "."
    return text

def generate_daily_recommendation(date_str, papers):
    """生成每日推荐简报"""
    date_display = datetime.strptime(date_str, '%Y%m%d').strftime('%Y年%m月%d日')
    weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][datetime.strptime(date_str, '%Y%m%d').weekday()]
    
    # 为每个领域选择TOP论文
    selections = {}
    for area_key in FOCUS_AREAS.keys():
        selections[area_key] = select_top_papers(papers, area_key, max_count=3)
    
    # 构建简报
    brief = f"""---
title: "每日论文推荐 - {date_display}"
date: {date_str[:4]}-{date_str[4:6]}-{date_str[6:]}
tags: [daily-papers, autonomous-driving, physical-ai, ai-agent]
---

# 📚 每日论文推荐 - {date_display} {weekday}

> **专注领域**: 🚗 自动驾驶 | 🏗️ Physical AI | 🤖 AI Agent
> 
> **筛选方法**: 8类信号评分 → 从业者视角解读 | **数据来源**: arXiv + HuggingFace Daily Papers

---

"""
    
    # 添加每个领域的内容
    all_selected = []
    for area_key, area_config in FOCUS_AREAS.items():
        area_papers = selections[area_key]
        if not area_papers:
            continue
        
        brief += f"""## {area_config['emoji']} {area_config['name']}

**本期推荐 {len(area_papers)} 篇**

"""
        
        for i, paper in enumerate(area_papers, 1):
            brief += generate_paper_summary(paper, i)
            all_selected.append(paper)
        
        brief += "\n"
    
    # 数据看板
    total_papers = len(papers)
    selected_count = len(all_selected)
    high_score_papers = len([p for p in papers if p.get('score', 0) >= 50])
    
    brief += f"""## 📊 今日数据

| 指标 | 数值 |
|------|------|
| 扫描论文 | {total_papers} 篇 |
| 入选推荐 | {selected_count} 篇 |
| 高分论文 (>50分) | {high_score_papers} 篇 |
| 覆盖领域 | 3 个 |

---

## 📖 也值得关注

以下论文评分良好但未进入深度解读：

"""
    
    # 添加其他值得关注的论文
    other_papers = [p for p in papers if p not in all_selected and p.get('score', 0) >= 40][:10]
    
    for paper in other_papers:
        areas = ', '.join([c['name'] for c in paper.get('classifications', [])[:2]])
        inst = paper.get('top_institution', '')
        inst_str = f" [{inst}]" if inst else ""
        score = paper.get('score', 0)
        
        brief += f"- **[{paper['title'][:60]}...]({paper['url']})** - {areas}{inst_str} (评分: {score})\n"
    
    brief += f"""
---

## 📌 关于本推荐

**筛选机制** (8类信号评分):
| 信号 | 权重 |
|------|------|
| 机构背景 | +0-20分 |
| 社区推荐 | +10分 |
| 社区热度 | +0-15分 |
| 顶会收录 | +15分 |
| 代码可用 | +8分 |
| 从业者相关性 | +0-10分 |
| 学术影响力 | +0-12分 |
| 开源热度 | +0-10分 |

**局限**:
- 解读基于标题和摘要，非全文精读，关键结论以原论文为准
- 评分偏重工程导向，可能低估纯理论贡献
- 小众但高价值的工作可能因社区信号不足被遗漏

**收录使用**: `/sb 论文链接 批注` | **历史推荐**: [[../daily-papers/|查看全部]]

---

*推荐由 Ace 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*
*基于 AI-Brief 方法论*
"""
    
    return brief, selections

def update_daily_papers_index(date_str):
    """更新每日论文推荐索引"""
    index_path = Path("/root/.openclaw/workspace/second-brain/content/daily-papers/index.md")
    
    # 如果不存在，创建基础结构
    if not index_path.exists():
        index_content = f"""---
title: 每日论文推荐
description: 聚焦自动驾驶、Physical AI、AI Agent的每日论文精选
---

# 📚 每日论文推荐

专注领域: 🚗 自动驾驶 | 🏗️ Physical AI | 🤖 AI Agent

基于 AI-Brief 方法论，从 arXiv 每日数百篇论文中筛选最值得关注的论文，用从业者视角解读。

## 📅 历史推荐

- [[daily-papers/{date_str}/index|{date_str[:4]}年{date_str[4:6]}月{date_str[6:]}]] ⭐ 最新

## 🔬 覆盖领域

### 🚗 自动驾驶
端到端感知、规划、VLA模型、世界模型、仿真到现实迁移

### 🏗️ Physical AI
物理世界建模、机器人学习、世界模型、仿真、sim-to-real

### 🤖 AI Agent
Multi-Agent、工具调用、规划推理、代码智能、GUI自动化

---

*筛选方法: 8类信号评分 | 数据来源: arXiv + HF Daily Papers*
"""
        index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        print("✅ 已创建 daily-papers/index.md")
        return
    
    # 更新现有索引
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 添加新日期链接
    new_link = f"- [[daily-papers/{date_str}/index|{date_str[:4]}年{date_str[4:6]}月{date_str[6:]}]] ⭐ 最新"
    
    if f"daily-papers/{date_str}/index" in content:
        print("📄 今日链接已存在")
        return
    
    # 在历史推荐部分插入
    if "## 📅 历史推荐" in content:
        parts = content.split("## 📅 历史推荐")
        header = parts[0] + "## 📅 历史推荐\n\n"
        body = parts[1]
        
        # 移除旧的"最新"标记
        body = body.replace(" ⭐ 最新", "")
        
        # 插入新链接
        new_content = header + new_link + "\n" + body
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ 已更新 daily-papers/index.md")

def main():
    """主函数"""
    date_str = datetime.now().strftime('%Y%m%d')
    
    print(f"📚 生成每日论文推荐 - {date_str}")
    print("=" * 60)
    
    # 加载论文
    papers = load_papers(date_str)
    if not papers:
        print("❌ 没有论文数据，请先运行 daily_papers_collector.py")
        return 1
    
    print(f"📥 加载了 {len(papers)} 篇论文")
    
    # 生成简报
    brief_content, selections = generate_daily_recommendation(date_str, papers)
    
    # 保存文件
    output_dir = Path(f"/root/.openclaw/workspace/second-brain/content/daily-papers/{date_str}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / "index.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(brief_content)
    
    print(f"\n✅ 已生成: {output_file}")
    
    # 打印统计
    total_selected = sum(len(papers) for papers in selections.values())
    print(f"\n📊 本期推荐:")
    for area_key, area_papers in selections.items():
        if area_papers:
            print(f"  {FOCUS_AREAS[area_key]['emoji']} {FOCUS_AREAS[area_key]['name']}: {len(area_papers)} 篇")
    
    # 更新索引
    update_daily_papers_index(date_str)
    
    print("\n🎉 每日论文推荐生成完成！")
    print(f"📖 查看地址: https://andy03withai.github.io/second-brain/daily-papers/{date_str}/")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
