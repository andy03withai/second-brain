#!/usr/bin/env python3
"""
每日论文推荐 v1.0
基于 AI-Brief 方法论
聚焦领域: 自动驾驶、Physical AI、AI Agent
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from pathlib import Path
import time

# 专注领域配置
FOCUS_AREAS = {
    'autonomous-driving': {
        'name': '自动驾驶',
        'arxiv_cats': ['cs.CV', 'cs.RO', 'cs.SY'],
        'keywords': [
            'autonomous driving', 'self-driving', 'end-to-end', 'perception', 'planning', 
            'prediction', 'trajectory', 'motion planning', 'vehicle', 'traffic', 'sensor fusion',
            'lidar', 'camera', 'bev', 'bird eye view', 'occupancy', 'vla', 'vision language action'
        ],
        'weight': 1.0
    },
    'physical-ai': {
        'name': 'Physical AI',
        'arxiv_cats': ['cs.RO', 'cs.AI', 'physics.comp-ph'],
        'keywords': [
            'physical ai', 'physics-informed', 'world model', 'simulation', 'rigid body', 
            'deformable', 'fluid', 'multiphysics', 'material', 'mechanics', 'dynamics',
            'contact', 'friction', 'manipulation', 'locomotion', 'sim-to-real', 'digital twin'
        ],
        'weight': 1.0
    },
    'ai-agent': {
        'name': 'AI Agent',
        'arxiv_cats': ['cs.AI', 'cs.MA', 'cs.SE', 'cs.CL'],
        'keywords': [
            'agent', 'multi-agent', 'autonomous agent', 'llm agent', 'tool use', 'function calling',
            'planning', 'reasoning', 'chain-of-thought', 'react', 'reflexion', 'autogpt',
            'computer use', 'gui automation', 'web agent', 'code agent', 'devin', 'swe'
        ],
        'weight': 1.0
    }
}

# 顶级机构
TOP_INSTITUTIONS = [
    'openai', 'anthropic', 'deepmind', 'google', 'meta', 'nvidia', 'microsoft', 'amazon',
    'stanford', 'mit', 'cmu', 'berkeley', 'tsinghua', 'peking', 'shanghai jiao tong',
    'waymo', 'tesla', 'cruise', 'zoox', 'aurora', 'comma.ai',
    'bytedance', 'alibaba', 'baidu', 'tencent', 'huawei',
    'deepseek', '01.ai', 'moonshot', 'zhipu', 'minimax',
    'eth zurich', 'oxford', 'cambridge', 'toronto', 'montreal'
]

# 顶级会议
TOP_CONFERENCES = ['cvpr', 'iccv', 'eccv', 'neurips', 'nips', 'icml', 'iclr', 'acl', 'emnlp', 'naacl', 'aaai', 'ijcai', 'rss', 'corl', 'iros', 'icra']

def fetch_url(url, timeout=30, retries=2):
    """通用URL获取"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            print(f"  获取失败: {url[:50]}... - {e}")
    return None

def fetch_arxiv_papers(categories, max_results=50):
    """获取arXiv论文"""
    papers = []
    try:
        # 获取最近3天的论文
        three_days_ago = (datetime.now() - timedelta(days=3)).strftime('%Y%m%d')
        today = datetime.now().strftime('%Y%m%d')
        
        cat_query = ' OR '.join([f'cat:{cat}' for cat in categories])
        query = f'({cat_query}) AND submittedDate:[{three_days_ago}0000 TO {today}0000]'
        
        url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}'
        
        data = fetch_url(url, timeout=30)
        if not data:
            return papers
        
        entries = re.findall(r'<entry[^>]*>(.*?)</entry>', data, re.DOTALL)
        
        for entry in entries:
            title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
            summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
            url_match = re.search(r'<id>(.*?)</id>', entry)
            authors_match = re.findall(r'<name>(.*?)</name>', entry)
            published_match = re.search(r'<published>(.*?)</published>', entry)
            
            if title_match and summary_match:
                title = title_match.group(1).strip().replace('\n', ' ')
                if title == 'Error 503 Service Unavailable':
                    continue
                
                arxiv_id = url_match.group(1).strip().split('/abs/')[-1] if url_match else ''
                
                papers.append({
                    'title': title,
                    'summary': summary_match.group(1).strip(),
                    'url': url_match.group(1).strip() if url_match else '',
                    'arxiv_id': arxiv_id,
                    'authors': authors_match,
                    'published': published_match.group(1)[:10] if published_match else '',
                    'source': 'arXiv'
                })
    except Exception as e:
        print(f"  arXiv获取错误: {e}")
    
    return papers

def fetch_hf_daily_papers():
    """获取HuggingFace Daily Papers"""
    papers = []
    try:
        url = "https://huggingface.co/api/daily-papers"
        data = fetch_url(url, timeout=20)
        if not data:
            return papers
        
        papers_data = json.loads(data)
        for paper in papers_data.get('papers', []):
            paper_data = paper.get('paper', {})
            papers.append({
                'title': paper.get('title', ''),
                'url': paper_data.get('url', ''),
                'summary': paper.get('summary', ''),
                'arxiv_id': paper_data.get('id', ''),
                'hf_upvotes': paper_data.get('upvotes', 0),
                'source': 'HF Daily'
            })
    except Exception as e:
        print(f"  HF获取错误: {e}")
    return papers

def fetch_semantic_scholar_citations(arxiv_id):
    """获取Semantic Scholar引用数"""
    try:
        if not arxiv_id:
            return 0
        url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}?fields=citationCount"
        data = fetch_url(url, timeout=10)
        if data:
            result = json.loads(data)
            return result.get('citationCount', 0)
    except:
        pass
    return 0

def detect_institution(text):
    """检测顶级机构"""
    text_lower = text.lower()
    for inst in TOP_INSTITUTIONS:
        if inst.lower() in text_lower:
            return inst.title()
    return None

def detect_conference(text):
    """检测顶级会议"""
    text_lower = text.lower()
    for conf in TOP_CONFERENCES:
        if conf.lower() in text_lower:
            return conf.upper()
    return None

def classify_paper(paper):
    """分类论文到专注领域"""
    text = (paper.get('title', '') + ' ' + paper.get('summary', '')).lower()
    classifications = []
    
    for area_key, area_config in FOCUS_AREAS.items():
        score = 0
        for keyword in area_config['keywords']:
            if keyword.lower() in text:
                score += 1
        
        if score > 0:
            classifications.append({
                'area': area_key,
                'name': area_config['name'],
                'relevance': min(score * 0.3, 1.0)  # 归一化相关性
            })
    
    # 按相关性排序
    classifications.sort(key=lambda x: x['relevance'], reverse=True)
    return classifications

def score_paper(paper):
    """8类信号评分"""
    score = 0
    text = (paper.get('title', '') + ' ' + paper.get('summary', '')).lower()
    
    # 1. 机构背景 (+0-20分)
    inst = detect_institution(text)
    if inst:
        score += 20
        paper['top_institution'] = inst
    
    # 2. 社区推荐 (+10分) - 来自HF Daily
    if paper.get('source') == 'HF Daily':
        score += 10
        paper['community_recommended'] = True
    
    # 3. 社区热度 (+0-15分)
    upvotes = paper.get('hf_upvotes', 0)
    if upvotes > 50:
        score += 15
    elif upvotes > 20:
        score += 10
    elif upvotes > 10:
        score += 5
    
    # 4. 顶会收录 (+15分)
    conf = detect_conference(text)
    if conf:
        score += 15
        paper['conference'] = conf
    
    # 5. 代码可用 (+8分)
    if 'github' in text or 'code' in text or 'implementation' in text:
        score += 8
        paper['has_code'] = True
    
    # 6. 从业者相关性 (+0-10分) - 已在分类时考虑
    classifications = paper.get('classifications', [])
    if classifications:
        max_relevance = max(c['relevance'] for c in classifications)
        score += int(max_relevance * 10)
    
    # 7. 学术影响力 (+0-12分)
    citations = paper.get('citation_count', 0)
    if citations > 100:
        score += 12
    elif citations > 50:
        score += 8
    elif citations > 10:
        score += 4
    
    # 8. 开源热度 (GitHub stars) - 这里简化处理
    
    return min(score, 100)

def deduplicate_papers(papers):
    """去重"""
    seen_ids = set()
    unique_papers = []
    
    for paper in papers:
        arxiv_id = paper.get('arxiv_id', '')
        title_key = paper.get('title', '').lower()[:40]
        
        key = arxiv_id if arxiv_id else title_key
        
        if key and key not in seen_ids:
            seen_ids.add(key)
            unique_papers.append(paper)
    
    return unique_papers

def collect_and_score():
    """采集并评分"""
    print("📚 每日论文推荐 v1.0")
    print("=" * 60)
    print("专注领域: 自动驾驶 | Physical AI | AI Agent")
    print("=" * 60)
    
    all_papers = []
    
    # 1. 从arXiv获取
    all_categories = set()
    for area in FOCUS_AREAS.values():
        all_categories.update(area['arxiv_cats'])
    
    print(f"\n🔍 从 arXiv 采集 ({len(all_categories)} 个分类)...")
    arxiv_papers = fetch_arxiv_papers(list(all_categories), max_results=100)
    print(f"  ✅ arXiv: {len(arxiv_papers)} 篇")
    all_papers.extend(arxiv_papers)
    
    # 2. 从HF Daily获取
    print(f"\n🔍 从 HuggingFace Daily Papers 采集...")
    hf_papers = fetch_hf_daily_papers()
    print(f"  ✅ HF Daily: {len(hf_papers)} 篇")
    all_papers.extend(hf_papers)
    
    # 3. 去重
    print(f"\n🔄 去重...")
    all_papers = deduplicate_papers(all_papers)
    print(f"  去重后: {len(all_papers)} 篇")
    
    # 4. 分类
    print(f"\n🏷️ 分类到专注领域...")
    for paper in all_papers:
        paper['classifications'] = classify_paper(paper)
    
    # 只保留有分类的论文
    relevant_papers = [p for p in all_papers if p.get('classifications')]
    print(f"  相关论文: {len(relevant_papers)} 篇")
    
    # 5. 获取引用数
    print(f"\n📊 获取引用数...")
    for paper in relevant_papers:
        if paper.get('arxiv_id'):
            paper['citation_count'] = fetch_semantic_scholar_citations(paper['arxiv_id'])
    
    # 6. 评分
    print(f"\n⭐ 评分...")
    for paper in relevant_papers:
        paper['score'] = score_paper(paper)
    
    # 7. 排序
    relevant_papers.sort(key=lambda x: x['score'], reverse=True)
    
    return relevant_papers

def save_results(papers, date_str):
    """保存结果"""
    output_dir = Path("/root/.openclaw/workspace/second-brain/data/daily_papers")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 保存原始数据
    raw_file = output_dir / f"papers_{date_str}.json"
    with open(raw_file, 'w', encoding='utf-8') as f:
        json.dump({
            'papers': papers[:50],
            'count': len(papers),
            'date': date_str
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 数据已保存: {raw_file}")
    return raw_file

def main():
    """主函数"""
    date_str = datetime.now().strftime('%Y%m%d')
    
    # 采集和评分
    papers = collect_and_score()
    
    # 保存
    save_results(papers, date_str)
    
    # 打印TOP 10预览
    print("\n🌟 TOP 10 高分论文预览:")
    print("-" * 60)
    for i, paper in enumerate(papers[:10], 1):
        areas = ', '.join([c['name'] for c in paper.get('classifications', [])[:2]])
        inst = paper.get('top_institution', '')
        inst_str = f" [{inst}]" if inst else ""
        print(f"{i}. [{paper['score']}分] {paper['title'][:60]}...")
        print(f"   领域: {areas}{inst_str} | 来源: {paper['source']}")
    
    print("\n✅ 采集完成！")
    print(f"   候选论文: {len(papers)} 篇")
    print(f"   下一步: 生成推荐简报")

if __name__ == "__main__":
    main()
