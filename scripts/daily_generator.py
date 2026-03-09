#!/usr/bin/env python3
"""
第二大脑 - Daily 日记生成器
每天晚上 22:00 自动生成日记，总结一天的对话
"""

import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, '/usr/lib/node_modules/openclaw')

def generate_daily_note(date_str):
    """生成日记内容"""
    
    date_obj = datetime.strptime(date_str, '%Y%m%d')
    weekday = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][date_obj.weekday()]
    
    content = f"""---
title: "{date_str} 日记"
date: {date_obj.strftime('%Y-%m-%d')}
tags: [daily, 日记]
---

# {date_str} {weekday} 日记

## 📊 今日概览

- **日期**: {date_obj.strftime('%Y年%m月%d日')} {weekday}
- **天气**: （待补充）
- **心情**: （待补充）

## 💬 今日对话

### 上午

（待自动总结）

### 下午

（待自动总结）

### 晚上

（待自动总结）

## 📚 今日收录

- [[index|查看今日收录的文章]]

## 🤔 今日思考

（待记录）

## 📌 明日待办

- [ ] （待补充）

---

*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    return content

def create_daily_note():
    """创建今天的日记"""
    
    # 获取今天日期（上海时间）
    date_str = datetime.now().strftime('%Y%m%d')
    
    # 文件路径
    daily_dir = '/root/.openclaw/workspace/second-brain/content/daily'
    filepath = f"{daily_dir}/{date_str}.md"
    
    # 如果文件已存在，不覆盖
    if os.path.exists(filepath):
        print(f"日记已存在: {filepath}")
        return filepath
    
    # 确保目录存在
    os.makedirs(daily_dir, exist_ok=True)
    
    # 生成内容
    content = generate_daily_note(date_str)
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已创建日记: {filepath}")
    return filepath

def push_to_github():
    """推送到 GitHub"""
    import subprocess
    
    repo_path = "/root/.openclaw/workspace/second-brain"
    date_str = datetime.now().strftime('%Y%m%d')
    
    try:
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'Add daily note: {date_str}'], 
                      cwd=repo_path, check=True, capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'], 
                      cwd=repo_path, check=True, capture_output=True)
        print("🚀 已推送到 GitHub")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git 操作失败: {e}")

if __name__ == "__main__":
    filepath = create_daily_note()
    push_to_github()
    print(f"📖 查看地址: https://andy03withai.github.io/second-brain/daily/{os.path.basename(filepath).replace('.md', '')}")
