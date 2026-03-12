#!/usr/bin/env python3
"""
每日简报 v4.0 - 评分和筛选模块
- 多源交叉验证
- 社区热度评分
- 来源权威度评分
- 分层候选池
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
import hashlib

# 评分权重配置
SCORING_WEIGHTS = {
    'cross_sources': 30,      # 多源交叉验证 (0-30)
    'community_heat': 25,     # 社区热度 (0-25)
    'source_authority': 20,   # 来源权威度 (0-20)
    'timeliness': 15,         # 时效性 (0-15)
    'institution': 10,        # 机构背景 (0-10)
}

# 来源权威度等级
SOURCE_AUTHORITY = {
    'company_official': 20,
    'tier1_media': 15,
    'academic': 12,
    'newsletter': 10,
    'community': 8,
    'independent_blog': 8,
    'academic_community': 10,
}

# 顶级机构关键词
TOP_INSTITUTIONS = [
    'openai', 'anthropic', 'deepmind', 'google', 'meta', 'nvidia', 
    'microsoft', 'amazon', 'stanford', 'mit', 'cmu', 'berkeley', 
    'tsinghua', 'bytedance', 'alibaba', 'deepseek', 'mistral', 'cohere'
]

# AI 相关关键词（用于分类）
AI_CATEGORIES = {
    'models': ['llm', 'gpt', 'claude', 'model', 'training', 'inference', 'fine-tune', 'parameter', 'transformer'],
    'agents': ['agent', 'autonomous', 'tool use', 'function calling', 'multi-agent', 'workflow'],
    'multimodal': ['vision', 'image', 'video', 'audio', 'speech', 'multimodal', 'vlm'],
    'robotics': ['robot', 'robotics', 'embodied', 'manipulation', 'locomotion'],
    'safety': ['safety', 'alignment', 'rlhf', 'constitutional ai', 'jailbreak', 'adversarial'],
    'product': ['product', 'launch', 'release', 'api', 'pricing', 'partnership'],
    'research': ['paper', 'arxiv', 'research', 'neurips', 'icml', 'cvpr', 'iclr'],
}

def generate_item_id(item):
    """生成条目唯一ID (基于标题和URL)"""
    title = item.get('title', '').lower().strip()
    url = item.get('url', '')
    # 清理标题，取前50个字符
    title_key = re.sub(r'[^\w\s]', '', title[:50])
    # 使用域名作为辅助
    domain = re.search(r'https?://(?:www\.)?([^/]+)', url)
    domain_str = domain.group(1) if domain else ''
    
    key = f"{title_key}|{domain_str}"
    return hashlib.md5(key.encode()).hexdigest()[:16]

def parse_publish_time(item):
    """解析发布时间，返回datetime对象"""
    pub_str = item.get('published', '')
    if not pub_str:
        return datetime.now()
    
    # 尝试多种格式
    formats = [
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%d %H:%M:%S',
        '%a, %d %b %Y %H:%M:%S %z',
        '%a, %d %b %Y %H:%M:%S GMT',
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(pub_str[:26], fmt)
        except:
            continue
    
    # 如果都失败，返回当前时间
    return datetime.now()

def detect_top_institution(item):
    """检测是否来自顶级机构"""
    text = (item.get('title', '') + ' ' + item.get('summary', '')).lower()
    for inst in TOP_INSTITUTIONS:
        if inst in text:
            return inst
    return None

def categorize_item(item):
    """对条目进行分类"""
    text = (item.get('title', '') + ' ' + item.get('summary', '')).lower()
    categories = []
    
    for cat, keywords in AI_CATEGORIES.items():
        if any(kw in text for kw in keywords):
            categories.append(cat)
    
    return categories if categories else ['general']

def score_item_v4(item, all_items_map):
    """v4.0 评分算法"""
    score = 0
    
    # 1. 多源交叉验证 (0-30分)
    item_id = generate_item_id(item)
    cross_sources = 0
    
    # 查找相似标题的条目
    item_title_key = item.get('title', '').lower()[:40]
    for other_id, other_item in all_items_map.items():
        if other_id != item_id:
            other_title_key = other_item.get('title', '').lower()[:40]
            # 简单相似度判断
            similarity = len(set(item_title_key.split()) & set(other_title_key.split()))
            if similarity >= 3:  # 有3个以上共同词
                cross_sources += 1
    
    if cross_sources >= 3:
        score += 30
    elif cross_sources == 2:
        score += 20
    elif cross_sources == 1:
        score += 10
    
    item['cross_sources'] = cross_sources
    
    # 2. 社区热度 (0-25分)
    hn_score = item.get('hn_score', 0)
    if hn_score > 200:
        score += 25
    elif hn_score > 100:
        score += 20
    elif hn_score > 50:
        score += 15
    elif hn_score > 20:
        score += 10
    elif hn_score > 0:
        score += 5
    
    # HF 热度
    hf_upvotes = item.get('hf_upvotes', 0)
    if hf_upvotes > 50:
        score += 15
    elif hf_upvotes > 20:
        score += 10
    elif hf_upvotes > 10:
        score += 5
    
    # HF downloads (for models)
    hf_downloads = item.get('downloads', 0)
    if hf_downloads > 10000:
        score += 10
    elif hf_downloads > 1000:
        score += 5
    
    # 3. 来源权威度 (0-20分)
    source_type = item.get('source_type', '')
    authority_score = SOURCE_AUTHORITY.get(source_type, 5)
    score += authority_score
    
    # 4. 时效性 (0-15分)
    try:
        pub_time = parse_publish_time(item)
        age = datetime.now() - pub_time
        age_hours = age.total_seconds() / 3600
        
        if age_hours < 6:
            score += 15
        elif age_hours < 12:
            score += 12
        elif age_hours < 24:
            score += 10
        elif age_hours < 48:
            score += 5
        
        item['age_hours'] = int(age_hours)
    except:
        item['age_hours'] = 48
        score += 3
    
    # 5. 机构背景 (0-10分)
    institution = detect_top_institution(item)
    if institution:
        score += 10
        item['top_institution'] = institution
    
    # 6. 学术会议加分
    text = (item.get('title', '') + ' ' + item.get('summary', '')).lower()
    if any(conf in text for conf in ['cvpr', 'iccv', 'eccv', 'neurips', 'icml', 'iclr', 'acl']):
        score += 8
        item['is_top_conference'] = True
    
    return min(score, 100)

def deduplicate_and_cluster(items):
    """去重并聚类相似条目"""
    # 生成ID并去重
    unique_items = {}
    for item in items:
        item_id = generate_item_id(item)
        if item_id not in unique_items:
            unique_items[item_id] = item
            item['id'] = item_id
    
    # 聚类：找出相似的事件/话题
    clusters = defaultdict(list)
    processed = set()
    
    for item_id, item in unique_items.items():
        if item_id in processed:
            continue
        
        # 为当前条目创建一个聚类
        cluster_key = item_id
        clusters[cluster_key].append(item)
        processed.add(item_id)
        
        # 查找相似的条目
        item_title_words = set(item.get('title', '').lower().split())
        
        for other_id, other_item in unique_items.items():
            if other_id in processed:
                continue
            
            other_title_words = set(other_item.get('title', '').lower().split())
            
            # 计算相似度
            common_words = item_title_words & other_title_words
            if len(common_words) >= 3:  # 有3个以上共同词，认为是同一事件
                clusters[cluster_key].append(other_item)
                processed.add(other_id)
    
    # 为每个条目添加聚类信息
    for cluster_key, cluster_items in clusters.items():
        for item in cluster_items:
            item['cluster_id'] = cluster_key
            item['cluster_size'] = len(cluster_items)
    
    return list(unique_items.values())

def create_candidate_pools(items):
    """创建分层候选池"""
    # 评分
    items_map = {item['id']: item for item in items}
    
    print("\n📊 正在评分...")
    for item in items:
        item['score'] = score_item_v4(item, items_map)
        item['categories'] = categorize_item(item)
    
    # 排序
    items.sort(key=lambda x: x['score'], reverse=True)
    
    # 分层
    threshold_high = 60
    threshold_medium = 40
    
    high_pool = [item for item in items if item['score'] >= threshold_high]
    medium_pool = [item for item in items if threshold_medium <= item['score'] < threshold_high]
    low_pool = [item for item in items if item['score'] < threshold_medium]
    
    print(f"  🔴 重点关注池 (>{threshold_high}分): {len(high_pool)} 条")
    print(f"  🟡 值得关注池 ({threshold_medium}-{threshold_high}分): {len(medium_pool)} 条")
    print(f"  🔵 快讯池 (<{threshold_medium}分): {len(low_pool)} 条")
    
    return {
        'high': high_pool,
        'medium': medium_pool,
        'low': low_pool,
        'all': items
    }

def save_pools(pools, date_str):
    """保存候选池到文件"""
    output_dir = Path("/root/.openclaw/workspace/second-brain/data/daily_brief")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"candidate_pools_{date_str}.json"
    
    # 序列化时处理datetime
    def serialize(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'high': pools['high'][:20],  # 只保存前20
            'medium': pools['medium'][:20],
            'low': pools['low'][:30],
            'stats': {
                'high_count': len(pools['high']),
                'medium_count': len(pools['medium']),
                'low_count': len(pools['low']),
                'total': len(pools['all'])
            },
            'created_at': datetime.now().isoformat()
        }, f, indent=2, ensure_ascii=False, default=serialize)
    
    print(f"\n💾 候选池已保存: {output_file}")
    return output_file

def main():
    """主函数"""
    date_str = datetime.now().strftime('%Y%m%d')
    
    # 读取原始数据
    input_file = Path(f"/root/.openclaw/workspace/second-brain/data/daily_brief/raw_items_{date_str}.json")
    
    if not input_file.exists():
        print(f"❌ 找不到原始数据文件: {input_file}")
        print("请先运行 daily_brief_collector_v4.py")
        return
    
    print(f"🤖 Ace 正在评分筛选 v4.0 - {date_str}")
    print("=" * 60)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        items = data.get('items', [])
    
    print(f"📥 原始条目: {len(items)} 条")
    
    # 去重并聚类
    print("\n🔄 去重聚类...")
    items = deduplicate_and_cluster(items)
    print(f"  去重后: {len(items)} 条")
    
    # 创建候选池
    pools = create_candidate_pools(items)
    
    # 保存
    output_file = save_pools(pools, date_str)
    
    # 打印高分条目预览
    print("\n🌟 TOP 10 高分条目预览:")
    print("-" * 60)
    for i, item in enumerate(pools['high'][:10], 1):
        categories = ','.join(item.get('categories', ['general'])[:2])
        cross = item.get('cross_sources', 0)
        inst = item.get('top_institution', '')
        inst_str = f" [{inst}]" if inst else ""
        print(f"{i}. [{item['score']}分] {item['title'][:60]}...")
        print(f"   来源: {item['source']} | 交叉验证: {cross} | 分类: {categories}{inst_str}")
    
    print("\n✅ 评分筛选完成！")
    print(f"   重点关注: {len(pools['high'])} 条")
    print(f"   值得关注: {len(pools['medium'])} 条")
    print(f"   快讯: {len(pools['low'])} 条")

if __name__ == "__main__":
    main()
