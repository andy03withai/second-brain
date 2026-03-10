#!/usr/bin/env python3
"""
第二大脑 - 首页自动更新器
自动更新 index.md 中的各种链接和列表

用法:
  python index_updater.py --daily 20260311          # 更新每日简报日期
  python index_updater.py --article <filepath>      # 添加新文章到列表
  python index_updater.py --research <filepath>     # 添加调研报告到列表
"""

import os
import re
import sys
from datetime import datetime
from pathlib import Path

INDEX_PATH = "/root/.openclaw/workspace/second-brain/content/index.md"

def read_index():
    """读取 index.md 内容"""
    try:
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def write_index(content):
    """写入 index.md"""
    os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

def update_daily_brief_date(date_str):
    """更新每日简报的最新日期链接"""
    content = read_index()
    
    # 格式: YYYYMMDD → YYYY-MM-DD
    date_display = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    
    # 更新各主题的今日链接
    topics = ['ai', 'agent', 'autonomous-driving', 'multimodal', 'embodied-intelligence']
    for topic in topics:
        # 旧格式: [[input/20260310/ai|今日]]
        old_pattern = rf'\[\[input/\d{{8}}/{topic}\|今日\]\]'
        new_link = f'[[input/{date_str}/{topic}|今日]]'
        content = re.sub(old_pattern, new_link, content)
        
        # 处理 topic 名称变化的情况
        topic_map = {
            'autonomous-driving': 'autonomous_driving',
            'embodied-intelligence': 'embodied_intelligence'
        }
        if topic in topic_map:
            old_topic = topic_map[topic]
            old_pattern = rf'\[\[input/\d{{8}}/{old_topic}\|今日\]\]'
            content = re.sub(old_pattern, new_link, content)
    
    # 更新每日简报总览链接
    old_index_pattern = r'\[\[input/\d{8}/index\|\d{4}-\d{2}-\d{2} 每日简报总览\]\]'
    new_index_link = f'[[input/{date_str}/index|{date_display} 每日简报总览]]'
    content = re.sub(old_index_pattern, new_index_link, content)
    
    # 更新最后更新时间
    content = re.sub(
        r'\*最后更新：\d{4}-\d{2}-\d{2}\*',
        f'*最后更新：{date_display}*',
        content
    )
    
    write_index(content)
    print(f"✅ 已更新每日简报日期: {date_display}")
    return True

def update_article_list(filepath):
    """添加新文章到最新收录列表"""
    content = read_index()
    
    # 提取文件名和标题
    filename = os.path.basename(filepath)
    
    # 从文件读取标题
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
            title_match = re.search(r'title:\s*"([^"]+)"', file_content)
            title = title_match.group(1) if title_match else filename.replace('.md', '')
            date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', file_content)
            date_str = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
    except:
        title = filename.replace('.md', '')
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    # 创建新的文章条目
    article_name = filename.replace('.md', '')
    new_entry = f"- [[articles/{article_name}|{title}]] - {date_str}"
    
    # 检查是否已存在
    if f"[[articles/{article_name}|" in content:
        print(f"⚠️ 文章已存在于列表中: {title}")
        return False
    
    # 插入到"最新收录"部分
    # 查找 "### 最新收录" 部分
    pattern = r'(### 最新收录\n\n)'
    if re.search(pattern, content):
        content = re.sub(pattern, rf'\1{new_entry}\n', content)
        
        # 只保留最近10篇文章
        latest_section = re.search(r'### 最新收录\n\n(.*?)(?=\n###|\n## 主题收录|$)', content, re.DOTALL)
        if latest_section:
            lines = [line for line in latest_section.group(1).split('\n') if line.strip().startswith('-')]
            if len(lines) > 10:
                # 保留前10条
                lines_to_keep = lines[:10]
                new_section = '\n'.join(lines_to_keep) + '\n'
                content = re.sub(
                    r'(### 最新收录\n\n).*?(?=\n###|\n## 主题收录|$)',
                    rf'\1{new_section}',
                    content,
                    flags=re.DOTALL
                )
        
        write_index(content)
        print(f"✅ 已添加文章到列表: {title}")
        return True
    else:
        print("⚠️ 未找到 '最新收录' 部分")
        return False

def update_research_list(filepath):
    """添加调研报告到列表"""
    content = read_index()
    
    # 提取文件名和标题
    filename = os.path.basename(filepath)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
            title_match = re.search(r'title:\s*"([^"]+)"', file_content)
            title = title_match.group(1) if title_match else filename.replace('.md', '')
            date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', file_content)
            date_str = date_match.group(1) if date_match else datetime.now().strftime('%Y-%m-%d')
    except:
        title = filename.replace('.md', '')
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    # 创建新条目
    research_name = filename.replace('.md', '')
    new_entry = f"- [[deep-research/{research_name}|{title}]] - {date_str}"
    
    # 检查是否已存在
    if f"[[deep-research/{research_name}|" in content:
        print(f"⚠️ 调研报告已存在于列表中: {title}")
        return False
    
    # 插入到"调研报告列表"链接附近
    # 在 "[[deep-research/index|📊 调研报告列表]]" 后添加最新条目
    pattern = r'(## 🔬 深度调研.*?\n\n)'
    match = re.search(pattern, content, re.DOTALL)
    if match:
        # 在调研部分开头添加最新报告
        section_start = match.end()
        content = content[:section_start] + f"**最新报告**: {new_entry}\n\n" + content[section_start:]
        
        write_index(content)
        print(f"✅ 已添加调研报告到列表: {title}")
        return True
    else:
        print("⚠️ 未找到 '深度调研' 部分")
        return False

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == '--daily' and len(sys.argv) >= 3:
        date_str = sys.argv[2]
        update_daily_brief_date(date_str)
    elif command == '--article' and len(sys.argv) >= 3:
        filepath = sys.argv[2]
        update_article_list(filepath)
    elif command == '--research' and len(sys.argv) >= 3:
        filepath = sys.argv[2]
        update_research_list(filepath)
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
