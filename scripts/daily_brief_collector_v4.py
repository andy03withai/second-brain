#!/usr/bin/env python3
"""
每日简报 v4.0 - 信息源采集模块
基于 AI 资讯速览方法论升级
- 20+ 国际化信息源
- 多源交叉验证
- 社区热度追踪
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
import xml.etree.ElementTree as ET
import time

# 信息源配置 v4.0
SOURCES = {
    'rss': [
        {'name': 'OpenAI Blog', 'url': 'https://openai.com/blog/rss.xml', 'type': 'company_official'},
        {'name': 'Anthropic Blog', 'url': 'https://www.anthropic.com/rss.xml', 'type': 'company_official'},
        {'name': 'DeepMind Blog', 'url': 'https://deepmind.google/blog/rss.xml', 'type': 'company_official'},
        {'name': 'Google AI Blog', 'url': 'https://blog.google/technology/ai/rss/', 'type': 'company_official'},
        {'name': 'Meta AI Blog', 'url': 'https://ai.meta.com/blog/rss/', 'type': 'company_official'},
        {'name': 'NVIDIA Blog', 'url': 'https://blogs.nvidia.com/blog/category/artificial-intelligence/feed/', 'type': 'company_official'},
        {'name': 'MIT Technology Review', 'url': 'https://www.technologyreview.com/feed/', 'type': 'tier1_media'},
        {'name': 'The Verge AI', 'url': 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml', 'type': 'tier1_media'},
        {'name': 'TechCrunch AI', 'url': 'https://techcrunch.com/category/artificial-intelligence/feed/', 'type': 'tier1_media'},
        {'name': 'Wired AI', 'url': 'https://www.wired.com/tag/artificial-intelligence/feed/', 'type': 'tier1_media'},
        {'name': 'Ars Technica', 'url': 'https://feeds.arstechnica.com/arstechnica/index', 'type': 'tier1_media'},
        {'name': '404 Media', 'url': 'https://www.404media.co/rss/', 'type': 'tier1_media'},
        {'name': 'Simon Willison', 'url': 'https://simonwillison.net/atom.xml', 'type': 'independent_blog'},
    ],
    'newsletter': [
        {'name': 'Import AI', 'url': 'https://importai.substack.com/feed', 'type': 'newsletter'},
        {'name': 'Ben\'s Bites', 'url': 'https://bensbites.beehiiv.com/feed', 'type': 'newsletter'},
        {'name': 'Latent Space', 'url': 'https://www.latent.space/feed', 'type': 'newsletter'},
        {'name': 'One Useful Thing', 'url': 'https://www.oneusefulthing.org/feed', 'type': 'newsletter'},
    ],
    'api': [
        {'name': 'Hacker News', 'fetcher': 'fetch_hn_ai_stories'},
        {'name': 'HuggingFace Papers', 'fetcher': 'fetch_hf_daily_papers'},
        {'name': 'HuggingFace Trending', 'fetcher': 'fetch_hf_trending'},
        {'name': 'arXiv', 'fetcher': 'fetch_arxiv_recent'},
    ]
}

# 顶级机构和会议
TOP_INSTITUTIONS = ['openai', 'anthropic', 'deepmind', 'google', 'meta', 'nvidia', 'microsoft', 'amazon', 'stanford', 'mit', 'cmu', 'berkeley', 'tsinghua', 'bytedance', 'alibaba', 'deepseek']
TOP_CONFERENCES = ['cvpr', 'iccv', 'eccv', 'neurips', 'icml', 'iclr', 'acl', 'emnlp', 'naacl', 'aaai', 'ijcai']

def fetch_url(url, timeout=30, retries=2):
    """通用URL获取，带重试"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read().decode('utf-8')
        except urllib.error.HTTPError as e:
            if e.code == 429:  # Too many requests
                time.sleep(2 ** attempt)  # 指数退避
                continue
            print(f"  HTTP Error {e.code} for {url}")
            return None
        except Exception as e:
            if attempt < retries - 1:
                time.sleep(1)
                continue
            print(f"  Failed to fetch {url}: {e}")
            return None
    return None

def parse_rss_feed(feed_content, source_name, source_type):
    """解析RSS feed"""
    items = []
    try:
        root = ET.fromstring(feed_content)
        
        # 处理 RSS 2.0
        if root.tag == 'rss':
            channel = root.find('channel')
            if channel is not None:
                for item in channel.findall('item')[:10]:  # 只取前10条
                    title = item.find('title')
                    link = item.find('link')
                    description = item.find('description')
                    pub_date = item.find('pubDate')
                    
                    if title is not None and link is not None:
                        items.append({
                            'title': title.text or '',
                            'url': link.text or '',
                            'summary': (description.text[:300] + '...') if description and len(description.text) > 300 else (description.text or ''),
                            'published': pub_date.text if pub_date is not None else '',
                            'source': source_name,
                            'source_type': source_type,
                            'fetched_at': datetime.now().isoformat()
                        })
        
        # 处理 Atom
        elif 'feed' in root.tag:
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            for entry in root.findall('atom:entry', ns)[:10]:
                title = entry.find('atom:title', ns)
                link = entry.find('atom:link', ns)
                summary = entry.find('atom:summary', ns)
                content = entry.find('atom:content', ns)
                published = entry.find('atom:published', ns) or entry.find('atom:updated', ns)
                
                if title is not None:
                    link_url = ''
                    if link is not None:
                        link_url = link.get('href', '')
                    
                    text_content = ''
                    if summary is not None:
                        text_content = summary.text or ''
                    elif content is not None:
                        text_content = content.text or ''
                    
                    items.append({
                        'title': title.text or '',
                        'url': link_url,
                        'summary': text_content[:300] + '...' if len(text_content) > 300 else text_content,
                        'published': published.text if published is not None else '',
                        'source': source_name,
                        'source_type': source_type,
                        'fetched_at': datetime.now().isoformat()
                    })
    except Exception as e:
        print(f"  Error parsing RSS from {source_name}: {e}")
    
    return items

def fetch_hn_ai_stories():
    """获取 Hacker News 上 AI 相关的热门故事"""
    items = []
    try:
        # 获取 Top Stories
        url = "https://hacker-news.firebaseio.com/v0/topstories.json"
        data = fetch_url(url, timeout=15)
        if not data:
            return items
        
        story_ids = json.loads(data)[:30]  # 取前30个
        
        # AI 相关关键词
        ai_keywords = ['ai', 'artificial intelligence', 'llm', 'machine learning', 'openai', 'anthropic', 'deepmind', 'gpt', 'claude', 'neural', 'model']
        
        for story_id in story_ids:
            try:
                story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                story_data = fetch_url(story_url, timeout=10)
                if not story_data:
                    continue
                
                story = json.loads(story_data)
                if not story:
                    continue
                
                title = story.get('title', '').lower()
                
                # 检查是否AI相关
                is_ai_related = any(kw in title for kw in ai_keywords)
                if not is_ai_related:
                    continue
                
                items.append({
                    'title': story.get('title', ''),
                    'url': story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    'summary': f"Score: {story.get('score', 0)}, Comments: {story.get('descendants', 0)}",
                    'hn_score': story.get('score', 0),
                    'hn_comments': story.get('descendants', 0),
                    'published': datetime.fromtimestamp(story.get('time', 0)).isoformat(),
                    'source': 'Hacker News',
                    'source_type': 'community',
                    'fetched_at': datetime.now().isoformat()
                })
                
                if len(items) >= 15:  # 最多15条AI相关
                    break
                    
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"  Error fetching HN: {e}")
    
    return items

def fetch_hf_daily_papers():
    """获取 HuggingFace Daily Papers"""
    items = []
    try:
        url = "https://huggingface.co/api/daily-papers"
        data = fetch_url(url, timeout=20)
        if not data:
            return items
        
        papers = json.loads(data)
        for paper in papers.get('papers', [])[:10]:
            paper_data = paper.get('paper', {})
            items.append({
                'title': paper.get('title', ''),
                'url': paper_data.get('url', ''),
                'summary': paper.get('summary', '')[:300] + '...' if paper.get('summary') else '',
                'hf_upvotes': paper_data.get('upvotes', 0),
                'arxiv_id': paper_data.get('id', ''),
                'published': datetime.now().isoformat(),
                'source': 'HF Daily Papers',
                'source_type': 'academic_community',
                'fetched_at': datetime.now().isoformat()
            })
    except Exception as e:
        print(f"  Error fetching HF papers: {e}")
    
    return items

def fetch_hf_trending():
    """获取 HuggingFace Trending Models/Datasets"""
    items = []
    try:
        # 获取 trending models
        url = "https://huggingface.co/api/models?sort=trending&limit=10"
        data = fetch_url(url, timeout=15)
        if data:
            models = json.loads(data)
            for model in models:
                items.append({
                    'title': f"[Model] {model.get('id', '')}",
                    'url': f"https://huggingface.co/{model.get('id', '')}",
                    'summary': f"Downloads: {model.get('downloads', 0)}, Likes: {model.get('likes', 0)}",
                    'downloads': model.get('downloads', 0),
                    'likes': model.get('likes', 0),
                    'source': 'HF Trending',
                    'source_type': 'community',
                    'fetched_at': datetime.now().isoformat()
                })
    except Exception as e:
        print(f"  Error fetching HF trending: {e}")
    
    return items

def fetch_arxiv_recent():
    """获取 arXiv 最近24小时论文"""
    items = []
    try:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
        today = datetime.now().strftime('%Y%m%d')
        
        # AI 相关分类
        categories = ['cs.AI', 'cs.LG', 'cs.CL', 'cs.CV', 'cs.RO']
        cat_query = ' OR '.join([f'cat:{cat}' for cat in categories])
        query = f'({cat_query}) AND submittedDate:[{yesterday}0000 TO {today}0000]'
        
        url = f'http://export.arxiv.org/api/query?search_query={urllib.parse.quote(query)}&sortBy=submittedDate&sortOrder=descending&max_results=30'
        
        data = fetch_url(url, timeout=30)
        if not data:
            return items
        
        # 解析XML
        entries = re.findall(r'<entry[^>]*>(.*?)</entry>', data, re.DOTALL)
        
        for entry in entries:
            title_match = re.search(r'<title>(.*?)</title>', entry, re.DOTALL)
            summary_match = re.search(r'<summary>(.*?)</summary>', entry, re.DOTALL)
            url_match = re.search(r'<id>(.*?)</id>', entry)
            authors_match = re.findall(r'<name>(.*?)</name>', entry)
            
            if title_match:
                title = title_match.group(1).strip().replace('\n', ' ')
                if title == 'Error 503 Service Unavailable':
                    continue
                
                arxiv_id = url_match.group(1).strip().split('/abs/')[-1] if url_match else ''
                
                items.append({
                    'title': title,
                    'url': url_match.group(1).strip() if url_match else '',
                    'summary': summary_match.group(1).strip()[:300] + '...' if summary_match else '',
                    'authors': authors_match[:3],
                    'arxiv_id': arxiv_id,
                    'published': datetime.now().isoformat(),
                    'source': 'arXiv',
                    'source_type': 'academic',
                    'fetched_at': datetime.now().isoformat()
                })
    except Exception as e:
        print(f"  Error fetching arXiv: {e}")
    
    return items

def collect_all_sources():
    """采集所有信息源"""
    all_items = []
    stats = {'rss': 0, 'api': 0, 'newsletter': 0, 'failed': []}
    
    print("\n📡 开始采集信息源 v4.0...")
    print("=" * 60)
    
    # 1. 采集 RSS 源
    print("\n📰 RSS 源:")
    for source in SOURCES['rss']:
        print(f"  🔍 {source['name']}...", end=' ')
        try:
            content = fetch_url(source['url'], timeout=20)
            if content:
                items = parse_rss_feed(content, source['name'], source['type'])
                all_items.extend(items)
                print(f"✅ {len(items)} 条")
                stats['rss'] += len(items)
            else:
                print("❌ 获取失败")
                stats['failed'].append(source['name'])
        except Exception as e:
            print(f"❌ 错误: {e}")
            stats['failed'].append(source['name'])
        time.sleep(0.5)  # 避免请求过快
    
    # 2. 采集 Newsletter
    print("\n📧 Newsletters:")
    for source in SOURCES['newsletter']:
        print(f"  🔍 {source['name']}...", end=' ')
        try:
            content = fetch_url(source['url'], timeout=20)
            if content:
                items = parse_rss_feed(content, source['name'], source['type'])
                all_items.extend(items)
                print(f"✅ {len(items)} 条")
                stats['newsletter'] += len(items)
            else:
                print("❌ 获取失败")
                stats['failed'].append(source['name'])
        except Exception as e:
            print(f"❌ 错误: {e}")
            stats['failed'].append(source['name'])
        time.sleep(0.5)
    
    # 3. 采集 API 源
    print("\n🔌 API 源:")
    
    print(f"  🔍 Hacker News...", end=' ')
    try:
        items = fetch_hn_ai_stories()
        all_items.extend(items)
        print(f"✅ {len(items)} 条")
        stats['api'] += len(items)
    except Exception as e:
        print(f"❌ 错误: {e}")
        stats['failed'].append('Hacker News')
    
    print(f"  🔍 HuggingFace Daily Papers...", end=' ')
    try:
        items = fetch_hf_daily_papers()
        all_items.extend(items)
        print(f"✅ {len(items)} 条")
        stats['api'] += len(items)
    except Exception as e:
        print(f"❌ 错误: {e}")
        stats['failed'].append('HF Daily Papers')
    
    print(f"  🔍 HuggingFace Trending...", end=' ')
    try:
        items = fetch_hf_trending()
        all_items.extend(items)
        print(f"✅ {len(items)} 条")
        stats['api'] += len(items)
    except Exception as e:
        print(f"❌ 错误: {e}")
        stats['failed'].append('HF Trending')
    
    print(f"  🔍 arXiv...", end=' ')
    try:
        items = fetch_arxiv_recent()
        all_items.extend(items)
        print(f"✅ {len(items)} 条")
        stats['api'] += len(items)
    except Exception as e:
        print(f"❌ 错误: {e}")
        stats['failed'].append('arXiv')
    
    print("\n" + "=" * 60)
    print(f"📊 采集统计:")
    print(f"  RSS 源: {stats['rss']} 条")
    print(f"  Newsletters: {stats['newsletter']} 条")
    print(f"  API 源: {stats['api']} 条")
    print(f"  总计: {len(all_items)} 条")
    if stats['failed']:
        print(f"  ⚠️ 失败: {', '.join(stats['failed'])}")
    
    return all_items, stats

if __name__ == "__main__":
    items, stats = collect_all_sources()
    
    # 保存到文件供下游使用
    output_dir = Path("/root/.openclaw/workspace/second-brain/data/daily_brief")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    date_str = datetime.now().strftime('%Y%m%d')
    output_file = output_dir / f"raw_items_{date_str}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'items': items,
            'stats': stats,
            'collected_at': datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 已保存到: {output_file}")
