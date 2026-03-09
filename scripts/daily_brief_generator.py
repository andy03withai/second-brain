#!/usr/bin/env python3
"""
第二大脑 - 每日简报生成器 v2.0 (P1优化版)
增加: HF Daily Papers + Semantic Scholar引用数
"""

import os
import sys
import json
import re
import subprocess
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, '/usr/lib/node_modules/openclaw')

# 配置
TOPICS = {
    'ai': {
        'name': 'AI 前沿',
        'sources': ['arxiv-cs.AI', 'arxiv-cs.LG', 'arxiv-cs.CL', 'huggingface-daily'],
        'keywords': ['大语言模型', 'LLM', 'Transformer', 'GPT', '推理', '训练优化'],
        'arxiv_cats': ['cs.AI', 'cs.LG', 'cs.CL']
    },
    'agent': {
        'name': 'Agent 智能体',
        'sources': ['arxiv-cs.AI', 'huggingface-daily'],
        'keywords': ['Agent', '智能体', 'Multi-Agent', '工具调用', 'AutoGPT'],
        'arxiv_cats': ['cs.AI']
    },
    'autonomous-driving': {
        'name': '自动驾驶大模型',
        'sources': ['arxiv-cs.CV', 'huggingface-daily'],
        'keywords': ['端到端', 'end-to-end', 'VLA', 'VLM', 'BEV', 'Occupancy'],
        'arxiv_cats': ['cs.CV', 'cs.RO']
    },
    'multimodal': {
        'name': '多模态数据',
        'sources': ['arxiv-cs.CV', 'arxiv-cs.MM', 'huggingface-daily'],
        'keywords': ['多模态', 'Multimodal', 'CLIP', 'Vision-Language', 'VLM'],
        'arxiv_cats': ['cs.CV', 'cs.MM']
    },
    'embodied-intelligence': {
        'name': '具身智能',
        'sources': ['arxiv-robotics', 'huggingface-daily'],
        'keywords': ['具身智能', 'Embodied', '机器人', 'Robot', 'RT-2', 'Manipulation'],
        'arxiv_cats': ['cs.RO']
    }
}

# 顶级会议列表
TOP_CONFERENCES = ['cvpr', 'iccv', 'eccv', 'neurips', 'icml', 'iclr', 'acl', 'emnlp', 'naacl']

# 顶级机构列表
TOP_INSTITUTIONS = ['google', 'deepmind', 'openai', 'meta', 'anthropic', 'stanford', 'mit', 'cmu', 'berkeley', 'tsinghua', 'waymo', 'tesla']

def fetch_hf_daily_papers():
    """获取 Hugging Face Daily Papers"""
    try:
        url = "https://huggingface.co/api/daily-papers"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            papers = []
            for item in data.get('papers', [])[:10]:  # 取前10篇
                papers.append({
                    'title': item.get('title', ''),
                    'summary': item.get('summary', '')[:200] + '...' if item.get('summary') else '',
                    'url': item.get('paper', {}).get('url', ''),
                    'arxiv_id': item.get('paper', {}).get('id', ''),
                    'source': 'HF Daily',
                    'upvotes': item.get('paper', {}).get('upvotes', 0),
                    'thumbnail': item.get('paper', {}).get('thumbnail', '')
                })
            return papers
    except Exception as e:
        print(f"HF Daily Papers获取失败: {e}")
    return []

def fetch_arxiv_papers(categories, max_results=30):
    """获取arXiv论文（支持多分类）"""
    try:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        today = datetime.now().strftime('%Y%m%d')
        
        # 构建多分类查询
        cat_query = ' OR '.join([f'cat:{cat}' for cat in categories])
        query = f'({cat_query}) AND submittedDate:[{yesterday}0000 TO {today}0000]'
        
        url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}'
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            content = response.read().decode('utf-8')
            
        # 解析XML
        entries = re.findall(r'<entry[^>]*>(.*?)</entry>', content, re.DOTALL)
        papers = []
        
        for entry in entries:
            title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
            summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
            url_match = re.search(r'<id>(.*?)</id>', entry)
            authors_match = re.findall(r'<name>(.*?)</name>', entry)
            published_match = re.search(r'<published>(.*?)</published>', entry)
            
            if title_match and summary_match:
                title = title_match.group(1).strip().replace('\n', ' ')
                # 跳过arXiv默认标题
                if title == 'Error 503 Service Unavailable':
                    continue
                    
                arxiv_id = url_match.group(1).strip().split('/abs/')[-1] if url_match else ''
                
                papers.append({
                    'title': title,
                    'summary': summary_match.group(1).strip()[:300] + '...',
                    'url': url_match.group(1).strip() if url_match else '',
                    'arxiv_id': arxiv_id,
                    'authors': authors_match[:5],  # 只取前5个作者
                    'published': published_match.group(1)[:10] if published_match else '',
                    'source': 'arXiv'
                })
        
        return papers
    except Exception as e:
        print(f"arXiv获取失败: {e}")
    return []

def fetch_semantic_scholar_citations(arxiv_id):
    """获取Semantic Scholar引用数"""
    try:
        if not arxiv_id:
            return 0
        
        url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=citationCount"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            return data.get('citationCount', 0)
    except Exception as e:
        # 静默失败，返回0
        pass
    return 0

def detect_conference(title_summary):
    """检测是否来自顶级会议"""
    title_lower = title_summary.lower()
    for conf in TOP_CONFERENCES:
        if conf in title_lower:
            return conf.upper()
    return None

def score_paper_v2(paper, topic_config):
    """改进版论文打分（P1优化）"""
    score = 40  # 降低基础分，让差异更明显
    title_summary = (paper.get('title', '') + ' ' + paper.get('summary', '')).lower()
    title_summary_lower = title_summary.lower()
    
    # 1. 关键词匹配 (+5~30分)
    keyword_hits = 0
    for keyword in topic_config['keywords']:
        if keyword.lower() in title_summary_lower:
            keyword_hits += 1
            score += 5
    score += min(keyword_hits * 2, 10)  # 额外奖励多关键词命中
    
    # 2. 顶级机构背景 (+15分)
    for inst in TOP_INSTITUTIONS:
        if inst in title_summary_lower:
            score += 15
            paper['top_institution'] = inst.title()
            break
    
    # 3. 会议等级 (+10~20分)
    conference = detect_conference(title_summary)
    if conference:
        score += 20
        paper['conference'] = conference
    
    # 4. 引用数 (+0~15分)
    citations = paper.get('citation_count', 0)
    if citations > 1000:
        score += 15
    elif citations > 500:
        score += 10
    elif citations > 100:
        score += 5
    
    # 5. HF社区热度 (+5~10分)
    upvotes = paper.get('upvotes', 0)
    if upvotes > 50:
        score += 10
    elif upvotes > 20:
        score += 5
    
    # 6. 代码开源 (+8分)
    if 'github' in title_summary_lower or 'code' in title_summary_lower or '开源' in title_summary_lower:
        score += 8
        paper['has_code'] = True
    
    return min(score, 100)

def deduplicate_papers(papers):
    """去重：相同arxiv_id或相似标题只保留一篇"""
    seen_ids = set()
    seen_titles = set()
    unique_papers = []
    
    for paper in papers:
        arxiv_id = paper.get('arxiv_id', '')
        title = paper.get('title', '').lower()
        
        # 跳过重复arxiv_id
        if arxiv_id and arxiv_id in seen_ids:
            continue
        
        # 跳过相似标题（简单判断：前30个字符相同）
        title_key = title[:30]
        if title_key in seen_titles:
            continue
        
        if arxiv_id:
            seen_ids.add(arxiv_id)
        seen_titles.add(title_key)
        unique_papers.append(paper)
    
    return unique_papers

def generate_topic_brief(topic_key, topic_config, date_str):
    """生成单个主题的简报"""
    
    print(f"\n📚 正在生成: {topic_config['name']}")
    
    all_papers = []
    
    # 1. 从arXiv获取
    if 'arxiv_cats' in topic_config:
        print(f"  🔍 从 arXiv 获取...")
        arxiv_papers = fetch_arxiv_papers(topic_config['arxiv_cats'], max_results=30)
        print(f"  ✅ arXiv: {len(arxiv_papers)} 篇")
        all_papers.extend(arxiv_papers)
    
    # 2. 从HF Daily Papers获取
    print(f"  🔍 从 HF Daily Papers 获取...")
    hf_papers = fetch_hf_daily_papers()
    print(f"  ✅ HF Daily: {len(hf_papers)} 篇")
    all_papers.extend(hf_papers)
    
    # 3. 去重
    all_papers = deduplicate_papers(all_papers)
    print(f"  📊 去重后: {len(all_papers)} 篇")
    
    # 4. 获取引用数并打分
    print(f"  ⏳ 正在获取引用数和评分...")
    for paper in all_papers:
        # 获取引用数
        if paper.get('arxiv_id'):
            paper['citation_count'] = fetch_semantic_scholar_citations(paper['arxiv_id'])
        
        # 打分
        paper['score'] = score_paper_v2(paper, topic_config)
    
    # 5. 排序并取前10
    all_papers.sort(key=lambda x: x.get('score', 0), reverse=True)
    top_papers = all_papers[:10]
    
    print(f"  🎯 TOP10 最低分: {top_papers[-1]['score'] if top_papers else 0}")
    
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

- **扫描论文**: {len(all_papers)} 篇 (arXiv + HF Daily)
- **入选推荐**: {len(top_papers)} 篇
- **平均分**: {sum(p['score'] for p in top_papers) // len(top_papers) if top_papers else 0}
- **更新时间**: {datetime.now().strftime('%H:%M')}

## 🌟 TOP 推荐

"""
    
    for i, paper in enumerate(top_papers[:3], 1):
        extra_info = []
        if paper.get('top_institution'):
            extra_info.append(f"🏛️ {paper['top_institution']}")
        if paper.get('conference'):
            extra_info.append(f"📜 {paper['conference']}")
        if paper.get('citation_count', 0) > 0:
            extra_info.append(f"📈 引用:{paper['citation_count']}")
        if paper.get('upvotes', 0) > 0:
            extra_info.append(f"👍 HF:{paper['upvotes']}")
        if paper.get('has_code'):
            extra_info.append("💻 开源")
        
        extra_str = " | ".join(extra_info) if extra_info else ""
        
        md_content += f"""### {i}. {paper['title']}
- **来源**: {paper.get('source', 'arXiv')}
- **评分**: {paper.get('score', 0)}/100 {f'({extra_str})' if extra_str else ''}
- **摘要**: {paper['summary'][:150]}...
- **链接**: [{paper['url']}]({paper['url']})

"""
    
    if len(top_papers) > 3:
        md_content += "## 📋 其他值得关注的\n\n"
        for i, paper in enumerate(top_papers[3:], 4):
            badges = []
            if paper.get('top_institution'):
                badges.append(paper['top_institution'])
            if paper.get('conference'):
                badges.append(paper['conference'])
            if paper.get('citation_count', 0) > 100:
                badges.append(f"引用{paper['citation_count']}")
            
            badge_str = f" [{', '.join(badges)}]" if badges else ""
            md_content += f"{i}. **{paper['title']}**{badge_str} - 评分:{paper.get('score', 0)} - [链接]({paper['url']})\n"
    
    md_content += f"""
## 🏷️ 关键词

{', '.join(topic_config['keywords'])}

## 📈 评分维度说明

- **关键词匹配**: +5/词 (最多30分)
- **顶级机构**: +15分 (Google/DeepMind/OpenAI等)
- **顶级会议**: +20分 (CVPR/ICML/NeurIPS等)
- **引用数量**: +0~15分 (100+/500+/1000+)
- **HF社区热度**: +0~10分 (20+/50+ upvotes)
- **代码开源**: +8分

---

*简报由 Ace 自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*
*数据来源: arXiv + Hugging Face Daily Papers + Semantic Scholar*
*如需深度分析某篇论文，请使用 `/sb 链接` 命令收录*
"""
    
    # 写入文件
    filepath = f"/root/.openclaw/workspace/second-brain/content/input/{topic_key}/{date_str}.md"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"  ✅ 已生成: {filepath}")
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
## 📊 今日数据来源

- **arXiv**: 实时抓取 (cs.AI/LG/CL/CV/RO/MM)
- **Hugging Face Daily Papers**: 社区投票Top10
- **Semantic Scholar**: 引用数查询

## 🎯 评分维度 (P1优化版)

| 维度 | 权重 | 说明 |
|------|------|------|
| 关键词匹配 | +5/词 | 主题相关度 |
| 顶级机构 | +15 | Google/DeepMind/OpenAI等 |
| 会议等级 | +20 | CVPR/ICML/NeurIPS等 |
| 引用数量 | +0~15 | 100+/500+/1000+ |
| HF热度 | +0~10 | 社区upvotes |
| 代码开源 | +8 | GitHub/Code |

## 使用指南

1. 浏览各主题简报，寻找感兴趣的内容
2. 关注 🏛️顶级机构 📜顶级会议 📈高引用 的论文
3. 对有价值的文章使用 `/sb 链接` 命令收录
4. 收录后自动进入第二大脑处理流程

---

*总索引生成于 {datetime.now().strftime('%H:%M')}*
*P1优化: 新增HF Daily Papers + Semantic Scholar引用数*
"""
    
    filepath = f"/root/.openclaw/workspace/second-brain/content/input/{date_str}-index.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    return filepath

def main():
    """主函数"""
    import urllib.parse  # 需要在main中用到
    
    date_str = datetime.now().strftime('%Y%m%d')
    
    print(f"🤖 Ace 开始生成每日简报 v2.0 (P1优化) - {date_str}")
    print("=" * 60)
    print("📊 新增数据源: HF Daily Papers + Semantic Scholar引用数")
    print("=" * 60)
    
    topics_generated = []
    
    # 为每个主题生成简报
    for topic_key, topic_config in TOPICS.items():
        try:
            generate_topic_brief(topic_key, topic_config, date_str)
            topics_generated.append(topic_key)
        except Exception as e:
            print(f"❌ {topic_config['name']} 生成失败: {e}")
            import traceback
            traceback.print_exc()
    
    # 生成总索引
    index_path = generate_daily_index(date_str, topics_generated)
    print(f"\n✅ 总索引: {index_path}")
    
    # 推送到GitHub
    print("\n🚀 推送到 GitHub...")
    repo_path = "/root/.openclaw/workspace/second-brain"
    try:
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'Add daily briefs v2.0 for {date_str} (P1: HF+SS)'], 
                      cwd=repo_path, check=True, capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'], 
                      cwd=repo_path, check=True, capture_output=True)
        print("✅ 推送成功")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git推送失败: {e}")
    
    print("\n" + "=" * 60)
    print(f"🎉 每日简报 v2.0 生成完成！")
    print(f"📖 查看地址: https://andy03withai.github.io/second-brain/input/")
    print("📊 新增: HF社区投票 + Semantic Scholar引用数")

if __name__ == "__main__":
    main()
