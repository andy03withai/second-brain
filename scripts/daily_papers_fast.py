#!/usr/bin/env python3
"""
每日论文推荐 v1.1 - 快速版
使用 HF Daily Papers 作为主要数据源
"""

import json
import urllib.request
from datetime import datetime
from pathlib import Path

FOCUS_AREAS = {
    'autonomous-driving': {
        'name': '自动驾驶',
        'keywords': ['autonomous driving', 'self-driving', 'vehicle', 'traffic', 'perception', 'planning', 'trajectory', 'bev', 'bird eye view', 'occupancy', 'vla']
    },
    'physical-ai': {
        'name': 'Physical AI',
        'keywords': ['physical', 'physics', 'world model', 'simulation', 'rigid body', 'deformable', 'fluid', 'multiphysics', 'material', 'mechanics', 'dynamics', 'manipulation', 'locomotion', 'sim-to-real', 'robot']
    },
    'ai-agent': {
        'name': 'AI Agent',
        'keywords': ['agent', 'multi-agent', 'autonomous agent', 'llm agent', 'tool use', 'planning', 'reasoning', 'chain-of-thought', 'react', 'computer use', 'gui automation', 'web agent', 'code agent']
    }
}

def fetch_hf_papers():
    """快速获取 HF Daily Papers"""
    try:
        url = "https://huggingface.co/api/daily-papers"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
            
        papers = []
        for item in data.get('papers', []):
            paper_data = item.get('paper', {})
            papers.append({
                'title': item.get('title', ''),
                'summary': item.get('summary', ''),
                'url': paper_data.get('url', ''),
                'arxiv_id': paper_data.get('id', ''),
                'hf_upvotes': paper_data.get('upvotes', 0),
                'authors': paper_data.get('authors', []),
                'source': 'HF Daily'
            })
        return papers
    except Exception as e:
        print(f"获取失败: {e}")
        return []

def classify_paper(paper):
    """分类论文"""
    text = (paper.get('title', '') + ' ' + paper.get('summary', '')).lower()
    classifications = []
    
    for area_key, area_config in FOCUS_AREAS.items():
        score = sum(1 for kw in area_config['keywords'] if kw.lower() in text)
        if score > 0:
            classifications.append({
                'area': area_key,
                'name': area_config['name'],
                'score': score
            })
    
    classifications.sort(key=lambda x: x['score'], reverse=True)
    return classifications

def score_paper(paper):
    """简单评分"""
    score = 0
    upvotes = paper.get('hf_upvotes', 0)
    
    if upvotes > 50:
        score += 25
    elif upvotes > 30:
        score += 20
    elif upvotes > 15:
        score += 15
    elif upvotes > 5:
        score += 10
    else:
        score += 5
    
    # 机构加分
    text = paper.get('title', '').lower()
    top_institutions = ['openai', 'anthropic', 'deepmind', 'google', 'meta', 'nvidia', 'stanford', 'mit']
    for inst in top_institutions:
        if inst in text:
            score += 10
            paper['top_institution'] = inst.title()
            break
    
    return min(score, 100)

def main():
    date_str = datetime.now().strftime('%Y%m%d')
    print(f"📚 每日论文推荐 (快速版) - {date_str}")
    print("=" * 60)
    
    # 获取论文
    print("🔍 获取 HuggingFace Daily Papers...")
    papers = fetch_hf_papers()
    print(f"✅ 获取 {len(papers)} 篇")
    
    if not papers:
        print("❌ 未能获取论文")
        return
    
    # 分类和评分
    print("🏷️ 分类和评分...")
    for paper in papers:
        paper['classifications'] = classify_paper(paper)
        paper['score'] = score_paper(paper)
    
    # 只保留相关论文
    relevant = [p for p in papers if p.get('classifications')]
    print(f"📊 相关论文: {len(relevant)} 篇")
    
    # 排序
    relevant.sort(key=lambda x: x['score'], reverse=True)
    
    # 保存
    output_dir = Path("/root/.openclaw/workspace/second-brain/data/daily_papers")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / f"papers_{date_str}.json", 'w', encoding='utf-8') as f:
        json.dump({'papers': relevant, 'count': len(relevant), 'date': date_str}, 
                  f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 已保存: {len(relevant)} 篇论文")
    
    # 显示TOP 10
    print("\n🌟 TOP 10 预览:")
    for i, p in enumerate(relevant[:10], 1):
        areas = ', '.join([c['name'] for c in p['classifications'][:2]])
        inst = p.get('top_institution', '')
        print(f"{i}. [{p['score']}分] {p['title'][:50]}... ({areas}){f' [{inst}]' if inst else ''}")
    
    print("\n✅ 采集完成！")

if __name__ == "__main__":
    main()
