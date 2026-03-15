#!/usr/bin/env python3
"""
第二大脑 - 每日简报生成器
每天早上6点自动采集各领域最新信息，生成简报
"""

import os
import sys
import json
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, '/usr/lib/node_modules/openclaw')

# 配置
TOPICS = {
    'ai': {
        'name': 'AI 前沿',
        'sources': [
            'arxiv-cs.AI',
            'arxiv-cs.LG',
            'arxiv-cs.CL',
            'huggingface-daily',
        ],
        'keywords': ['大语言模型', 'LLM', 'Transformer', 'GPT', '推理', '训练优化']
    },
    'agent': {
        'name': 'Agent 智能体',
        'sources': [
            'arxiv-cs.AI',
            'github-trending',
        ],
        'keywords': ['Agent', '智能体', 'Multi-Agent', '工具调用', 'AutoGPT', 'Claude']
    },
    'autonomous-driving': {
        'name': '自动驾驶大模型',
        'sources': [
            'arxiv-cs.CV',
            'waymo-blog',
            'autonomous-heart',
        ],
        'keywords': ['端到端', 'end-to-end', 'VLA', 'VLM', 'BEV', 'Occupancy', 'nuScenes', 'Waymo']
    },
    'multimodal': {
        'name': '多模态数据',
        'sources': [
            'arxiv-cs.CV',
            'arxiv-cs.MM',
        ],
        'keywords': ['多模态', 'Multimodal', 'CLIP', 'Vision-Language', 'VLM', '图文']
    },
    'embodied-intelligence': {
        'name': '具身智能',
        'sources': [
            'arxiv-robotics',
            'stanford-iliad',
        ],
        'keywords': ['具身智能', 'Embodied', '机器人', 'Robot', 'RT-2', 'VLA', 'Manipulation']
    }
}

def fetch_arxiv_papers(category, date_str, max_results=20):
    """获取arXiv论文"""
    try:
        # 使用 arxiv API 获取最近论文
        from datetime import datetime, timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        query = f'cat:{category} AND submittedDate:[{yesterday} TO {datetime.now().strftime("%Y-%m-%d")}]'
        
        result = subprocess.run([
            'curl', '-s', 
            f'http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            # 简单解析XML提取标题和摘要
            import re
            entries = re.findall(r'<entry>(.*?)</entry>', result.stdout, re.DOTALL)
            papers = []
            for entry in entries[:5]:  # 只取前5篇
                title = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
                summary = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
                url = re.search(r'<id>(.*?)</id>', entry)
                if title and summary:
                    papers.append({
                        'title': title.group(1).strip().replace('\n', ' '),
                        'summary': summary.group(1).strip()[:200] + '...',
                        'url': url.group(1).strip() if url else ''
                    })
            return papers
    except Exception as e:
        print(f"arXiv获取失败: {e}")
    return []

def score_paper(paper, topic_config):
    """给论文打分"""
    score = 50  # 基础分
    title_summary = (paper.get('title', '') + ' ' + paper.get('summary', '')).lower()
    
    # 关键词匹配
    for keyword in topic_config['keywords']:
        if keyword.lower() in title_summary:
            score += 10
    
    # 机构背景加分
    top_institutions = ['google', 'openai', 'meta', 'stanford', 'mit', 'tsinghua', 'deepmind', 'waymo', 'tesla']
    for inst in top_institutions:
        if inst in title_summary:
            score += 15
            break
    
    # 代码开源加分
    if 'github' in title_summary or 'code' in title_summary:
        score += 10
    
    return min(score, 100)

def generate_topic_brief(topic_key, topic_config, date_str):
    """生成单个主题的简报"""
    
    print(f"\n📚 正在生成: {topic_config['name']}")
    
    # 获取论文
    all_papers = []
    
    # 根据主题获取对应arXiv分类
    category_map = {
        'ai': 'cs.AI',
        'agent': 'cs.AI',
        'autonomous-driving': 'cs.CV',
        'multimodal': 'cs.CV',
        'embodied-intelligence': 'cs.RO'
    }
    
    if topic_key in category_map:
        papers = fetch_arxiv_papers(category_map[topic_key], date_str)
        for paper in papers:
            paper['score'] = score_paper(paper, topic_config)
            paper['source'] = 'arXiv'
        all_papers.extend(papers)
    
    # 排序并取前10
    all_papers.sort(key=lambda x: x.get('score', 0), reverse=True)
    top_papers = all_papers[:10]
    
    # 生成Markdown
    date_display = datetime.strptime(date_str, '%Y%m%d').strftime('%Y年%m月%d日')
    
    md_content = f"""---
title: "{topic_config['name']} - 每日简报"
date: {datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')}
topic: {topic_key}
tags: [daily-brief, {topic_key}]
---

# {topic_config['name']} - {date_display} 简报

## 📊 今日概览

- **扫描论文**: {len(all_papers)} 篇
- **入选推荐**: {len(top_papers)} 篇
- **更新时间**: {datetime.now().strftime('%H:%M')}

## 🌟 TOP 推荐

"""
    
    for i, paper in enumerate(top_papers[:3], 1):
        md_content += f"""### {i}. {paper['title']}
- **来源**: {paper.get('source', 'arXiv')}
- **评分**: {paper.get('score', 0)}/100
- **摘要**: {paper['summary'][:150]}...
- **链接**: [{paper['url']}]({paper['url']})

"""
    
    if len(top_papers) > 3:
        md_content += "## 📋 其他值得关注的\n\n"
        for i, paper in enumerate(top_papers[3:], 4):
            md_content += f"{i}. **{paper['title']}** - 评分:{paper.get('score', 0)} - [链接]({paper['url']})\n"
    
    md_content += f"""
## 🏷️ 关键词

{', '.join(topic_config['keywords'])}

---

*简报由 Ace 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*
*如需深度分析某篇论文，请使用 `/sb 链接` 命令收录*
"""
    
    # 写入文件
    filepath = f"/root/.openclaw/workspace/second-brain/content/input/{topic_key}/{date_str}.md"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"✅ 已生成: {filepath}")
    return filepath

def generate_daily_index(date_str, topics_generated):
    """生成每日总索引"""
    date_display = datetime.strptime(date_str, '%Y%m%d').strftime('%Y年%m月%d日')
    
    md_content = f"""---
title: "每日简报总览 - {date_display}"
date: {datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')}
tags: [daily-brief, index]
---

# 📰 每日简报总览 - {date_display}

## 各主题简报

| 主题 | 状态 | 链接 |
|------|------|------|
"""
    
    for topic_key, topic_config in TOPICS.items():
        status = "✅ 已生成" if topic_key in topics_generated else "⏭️ 跳过"
        link = f"[[input/{topic_key}/{date_str}|{topic_config['name']}]]"
        md_content += f"| {topic_config['name']} | {status} | {link} |\n"
    
    md_content += f"""
## 使用指南

1. 浏览各主题简报，寻找感兴趣的内容
2. 对有价值的文章使用 `/sb 链接` 命令收录
3. 收录后会自动进入第二大脑处理流程

---

*总索引生成于 {datetime.now().strftime('%H:%M')}*
"""
    
    filepath = f"/root/.openclaw/workspace/second-brain/content/input/{date_str}-index.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return filepath

def main():
    """主函数"""
    date_str = datetime.now().strftime('%Y%m%d')
    
    print(f"🤖 Ace 开始生成每日简报 - {date_str}")
    print("=" * 50)
    
    topics_generated = []
    
    # 为每个主题生成简报
    for topic_key, topic_config in TOPICS.items():
        try:
            generate_topic_brief(topic_key, topic_config, date_str)
            topics_generated.append(topic_key)
        except Exception as e:
            print(f"❌ {topic_config['name']} 生成失败: {e}")
    
    # 生成总索引
    index_path = generate_daily_index(date_str, topics_generated)
    print(f"\n✅ 总索引: {index_path}")
    
    # 推送到GitHub
    print("\n🚀 推送到 GitHub...")
    repo_path = "/root/.openclaw/workspace/second-brain"
    try:
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'Add daily briefs for {date_str}'], 
                      cwd=repo_path, check=True, capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'], 
                      cwd=repo_path, check=True, capture_output=True)
        print("✅ 推送成功")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git推送失败: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎉 每日简报生成完成！")
    print(f"📖 查看地址: https://andy03withai.github.io/second-brain/input/{date_str}/")

if __name__ == "__main__":
    main()
