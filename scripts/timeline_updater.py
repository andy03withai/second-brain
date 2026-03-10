#!/usr/bin/env python3
"""
第二大脑 - 时间线自动更新器
自动更新 timeline.md，添加新条目

用法:
  python timeline_updater.py --daily "20260311"          # 添加每日简报条目
  python timeline_updater.py --article "filepath" "title" # 添加文章条目
  python timeline_updater.py --research "filepath" "title" # 添加调研报告条目
  python timeline_updater.py --book "title" "批注"        # 添加书籍条目
"""

import os
import re
import sys
from datetime import datetime

TIMELINE_PATH = "/root/.openclaw/workspace/second-brain/content/timeline.md"

def read_timeline():
    """读取 timeline.md 内容"""
    try:
        with open(TIMELINE_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

def write_timeline(content):
    """写入 timeline.md"""
    os.makedirs(os.path.dirname(TIMELINE_PATH), exist_ok=True)
    with open(TIMELINE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

def get_today_entry():
    """获取今天的日期条目，如果不存在则创建"""
    today = datetime.now()
    year_month = f"{today.year}年{today.month}月"
    day_str = f"{today.day}日"
    weekday = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][today.weekday()]
    
    return {
        'year_month': year_month,
        'day_str': day_str,
        'weekday': weekday,
        'full_date': f"{today.month}月{day_str} {weekday}"
    }

def update_daily_brief(date_str):
    """添加每日简报条目到时间线"""
    content = read_timeline()
    
    date_info = get_today_entry()
    year_month = date_info['year_month']
    full_date = date_info['full_date']
    
    # 创建新的条目HTML
    new_entry = f'''
<div class="card">
<div class="card-icon">📰</div>
<div class="card-content">
<div class="card-title">每日简报 - {full_date}</div>
<div class="card-desc">AI、Agent、自动驾驶、多模态、具身智能 5个主题简报</div>
<div class="card-link"><a href="input/{date_str}/index">查看简报 →</a></div>
</div>
</div>
'''
    
    # 检查今天是否已有条目
    if f"每日简报 - {full_date}" in content:
        print(f"⚠️ 今日简报已存在于时间线中")
        return False
    
    # 检查是否需要创建新的月份标题
    if f"## {year_month}" not in content:
        # 在 "## 2026年" 或其他月份之前插入新月份
        month_header = f"\n## {year_month}\n\n### 📅 {full_date}\n\n<div class=\"timeline-cards\">\n{new_entry}\n</div>"
        
        # 在第一个 ## 202X年 之后插入
        content = re.sub(
            r'(## 2026年3月\n)',
            rf'## 2026年3月\n{month_header}\n',
            content
        )
    else:
        # 月份已存在，检查日期是否存在
        date_pattern = rf'(### 📅 {full_date}\s*\n\s*<div class="timeline-cards">)'
        if re.search(date_pattern, content):
            # 日期存在，插入到现有div中
            content = re.sub(
                date_pattern,
                rf'\1\n{new_entry}',
                content
            )
        else:
            # 日期不存在，创建新的日期块
            new_date_block = f"\n### 📅 {full_date}\n\n<div class=\"timeline-cards\">\n{new_entry}\n</div>"
            
            # 在月份标题后的第一个 ### 之前插入
            content = re.sub(
                rf'(## {year_month}.*?)(\n### 📅 )',
                rf'\1{new_date_block}\n\2',
                content,
                flags=re.DOTALL,
                count=1
            )
    
    # 更新最后更新时间
    content = re.sub(
        r'\*时间线最后更新: \d{4}-\d{2}-\d{2}\*',
        f'*时间线最后更新: {datetime.now().strftime("%Y-%m-%d")}*',
        content
    )
    
    write_timeline(content)
    print(f"✅ 已添加每日简报到时间线: {full_date}")
    return True

def update_article(filepath, title):
    """添加文章条目到时间线"""
    content = read_timeline()
    
    date_info = get_today_entry()
    full_date = date_info['full_date']
    
    # 从filepath提取文章名
    article_name = os.path.basename(filepath).replace('.md', '')
    
    new_entry = f'''
<div class="card">
<div class="card-icon">📄</div>
<div class="card-content">
<div class="card-title">文章收录: {title}</div>
<div class="card-desc">新文章已收录到第二大脑</div>
<div class="card-link"><a href="articles/{article_name}">阅读文章 →</a></div>
</div>
</div>
'''
    
    # 类似上面的逻辑...
    date_pattern = rf'(### 📅 {full_date}\s*\n\s*<div class="timeline-cards">)'
    if re.search(date_pattern, content):
        content = re.sub(date_pattern, rf'\1\n{new_entry}', content)
    else:
        # 创建新的日期块
        new_date_block = f"\n### 📅 {full_date}\n\n<div class=\"timeline-cards\">\n{new_entry}\n</div>"
        year_month = date_info['year_month']
        content = re.sub(
            rf'(## {year_month}.*?)(\n### 📅 )',
            rf'\1{new_date_block}\n\2',
            content,
            flags=re.DOTALL,
            count=1
        )
    
    # 更新统计数字
    # 简单增加文章计数
    content = re.sub(
        r'(<div class="stat-card">\s*<div class="stat-number">)(\d+)(</div>\s*<div class="stat-label">文章收录)',
        lambda m: f'{m.group(1)}{int(m.group(2))+1}{m.group(3)}',
        content
    )
    
    content = re.sub(
        r'\*时间线最后更新: \d{4}-\d{2}-\d{2}\*',
        f'*时间线最后更新: {datetime.now().strftime("%Y-%m-%d")}*',
        content
    )
    
    write_timeline(content)
    print(f"✅ 已添加文章到时间线: {title}")
    return True

def update_research(filepath, title):
    """添加调研报告条目到时间线"""
    content = read_timeline()
    
    date_info = get_today_entry()
    full_date = date_info['full_date']
    
    report_name = os.path.basename(filepath).replace('.md', '')
    
    new_entry = f'''
<div class="card">
<div class="card-icon">🔬</div>
<div class="card-content">
<div class="card-title">深度调研: {title}</div>
<div class="card-desc">基于 OpenAI Deep Research 方法论的系统调研报告</div>
<div class="card-link"><a href="deep-research/{report_name}">阅读报告 →</a></div>
</div>
</div>
'''
    
    date_pattern = rf'(### 📅 {full_date}\s*\n\s*<div class="timeline-cards">)'
    if re.search(date_pattern, content):
        content = re.sub(date_pattern, rf'\1\n{new_entry}', content)
    else:
        new_date_block = f"\n### 📅 {full_date}\n\n<div class=\"timeline-cards\">\n{new_entry}\n</div>"
        year_month = date_info['year_month']
        content = re.sub(
            rf'(## {year_month}.*?)(\n### 📅 )',
            rf'\1{new_date_block}\n\2',
            content,
            flags=re.DOTALL,
            count=1
        )
    
    # 更新统计数字
    content = re.sub(
        r'(<div class="stat-card">\s*<div class="stat-number">)(\d+)(</div>\s*<div class="stat-label">深度调研)',
        lambda m: f'{m.group(1)}{int(m.group(2))+1}{m.group(3)}',
        content
    )
    
    content = re.sub(
        r'\*时间线最后更新: \d{4}-\d{2}-\d{2}\*',
        f'*时间线最后更新: {datetime.now().strftime("%Y-%m-%d")}*',
        content
    )
    
    write_timeline(content)
    print(f"✅ 已添加调研报告到时间线: {title}")
    return True

def update_book(title, note=""):
    """添加书籍条目到时间线"""
    content = read_timeline()
    
    date_info = get_today_entry()
    full_date = date_info['full_date']
    
    new_entry = f'''
<div class="card">
<div class="card-icon">📚</div>
<div class="card-content">
<div class="card-title">书单新增: {title}</div>
<div class="card-desc">{note if note else "新书籍已添加到书单"}</div>
<div class="card-link"><a href="books/index">查看书单 →</a></div>
</div>
</div>
'''
    
    date_pattern = rf'(### 📅 {full_date}\s*\n\s*<div class="timeline-cards">)'
    if re.search(date_pattern, content):
        content = re.sub(date_pattern, rf'\1\n{new_entry}', content)
    else:
        new_date_block = f"\n### 📅 {full_date}\n\n<div class=\"timeline-cards\">\n{new_entry}\n</div>"
        year_month = date_info['year_month']
        content = re.sub(
            rf'(## {year_month}.*?)(\n### 📅 )',
            rf'\1{new_date_block}\n\2',
            content,
            flags=re.DOTALL,
            count=1
        )
    
    # 更新统计数字
    content = re.sub(
        r'(<div class="stat-card">\s*<div class="stat-number">)(\d+)(</div>\s*<div class="stat-label">书籍记录)',
        lambda m: f'{m.group(1)}{int(m.group(2))+1}{m.group(3)}',
        content
    )
    
    content = re.sub(
        r'\*时间线最后更新: \d{4}-\d{2}-\d{2}\*',
        f'*时间线最后更新: {datetime.now().strftime("%Y-%m-%d")}*',
        content
    )
    
    write_timeline(content)
    print(f"✅ 已添加书籍到时间线: {title}")
    return True

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == '--daily' and len(sys.argv) >= 3:
        date_str = sys.argv[2]
        update_daily_brief(date_str)
    elif command == '--article' and len(sys.argv) >= 4:
        filepath = sys.argv[2]
        title = sys.argv[3]
        update_article(filepath, title)
    elif command == '--research' and len(sys.argv) >= 4:
        filepath = sys.argv[2]
        title = sys.argv[3]
        update_research(filepath, title)
    elif command == '--book' and len(sys.argv) >= 3:
        title = sys.argv[2]
        note = sys.argv[3] if len(sys.argv) > 3 else ""
        update_book(title, note)
    else:
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
