#!/usr/bin/env python3
"""
第二大脑索引更新脚本 - 首页文章列表
扫描 articles/ 目录，自动更新首页最新收录列表
"""

import os
import re
import yaml
from datetime import datetime
from pathlib import Path

def extract_frontmatter(content):
    """提取 YAML frontmatter"""
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1])
            except:
                return {}
    return {}

def parse_date_from_filename(filename):
    """从文件名解析日期"""
    # 匹配 20260309-xxx 或 2026-03-09-xxx 格式
    patterns = [
        r'^(\d{4})-(\d{2})-(\d{2})-',
        r'^(\d{4})(\d{2})(\d{2})-'
    ]
    for pattern in patterns:
        match = re.match(pattern, filename)
        if match:
            try:
                return datetime(int(match.group(1)), int(match.group(2)), int(match.group(3)))
            except:
                pass
    return None

def scan_articles(content_dir, limit=10):
    """扫描文章目录"""
    articles_dir = Path(content_dir) / "articles"
    articles = []
    
    if not articles_dir.exists():
        return articles
    
    for item in articles_dir.iterdir():
        if item.suffix != '.md':
            continue
        
        with open(item, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fm = extract_frontmatter(content)
        
        # 优先使用 frontmatter 中的日期
        date = None
        if 'date' in fm:
            try:
                date = datetime.fromisoformat(fm['date'].replace('Z', '+00:00').replace('+08:00', ''))
            except:
                pass
        
        # 从文件名解析
        if date is None:
            date = parse_date_from_filename(item.stem)
        
        # 使用文件修改时间
        if date is None:
            date = datetime.fromtimestamp(item.stat().st_mtime)
        
        articles.append({
            'date': date,
            'date_str': date.strftime("%Y-%m-%d") if date else "",
            'title': fm.get('title', item.stem.replace('-', ' ').title()),
            'slug': item.stem
        })
    
    # 按日期倒序排列
    articles.sort(key=lambda x: x['date'], reverse=True)
    return articles[:limit]

def update_homepage_index(content_dir, articles):
    """更新首页 index.md 的文章列表"""
    index_path = Path(content_dir) / "index.md"
    
    if not index_path.exists():
        print(f"⚠️ 首页文件不存在: {index_path}")
        return
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 生成新的最新收录列表
    new_list = ["### 最新收录"]
    for article in articles:
        new_list.append(f"- [[articles/{article['slug']}|{article['title']}]] - {article['date_str']}")
    
    new_section = "\n".join(new_list)
    
    # 使用正则替换 ### 最新收录 部分
    pattern = r'(### 最新收录\n)(.*?)(?=\n### |\n## |\n\*最后更新|$)'
    
    def replace_section(match):
        return new_section + "\n"
    
    updated_content = re.sub(pattern, replace_section, content, flags=re.DOTALL)
    
    # 更新最后更新时间
    today = datetime.now().strftime("%Y-%m-%d")
    updated_content = re.sub(
        r'\*最后更新：.*\*',
        f'*最后更新：{today}*',
        updated_content
    )
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ 已更新首页文章列表: {index_path}")
    print(f"📊 共 {len(articles)} 篇文章")

def main():
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.parent
    content_dir = script_dir.parent.parent  # 指向 content/ 目录
    
    # 扫描文章
    articles = scan_articles(content_dir, limit=10)
    
    if not articles:
        print("未找到文章")
        return
    
    # 更新首页
    update_homepage_index(content_dir, articles)

if __name__ == "__main__":
    main()
