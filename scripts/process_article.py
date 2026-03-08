#!/usr/bin/env python3
"""
第二大脑 - 文章处理脚本
从飞书接收链接，处理后推送到 GitHub
"""

import sys
import os
import re
import json
import subprocess
from datetime import datetime
from urllib.parse import urlparse
import hashlib

sys.path.insert(0, '/usr/lib/node_modules/openclaw')

def sanitize_filename(url):
    """生成安全的文件名"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    path = parsed.path.strip('/').replace('/', '-')
    
    # 取路径的最后一部分
    if path:
        name = path.split('-')[-1][:30]
    else:
        name = domain[:30]
    
    # 清理非法字符
    name = re.sub(r'[^\w\s-]', '', name).strip()
    name = re.sub(r'[-\s]+', '-', name)
    
    date_str = datetime.now().strftime('%Y%m%d')
    return f"{date_str}-{name or 'article'}.md"

def generate_article(url, note=""):
    """生成文章 Markdown"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 从 URL 提取域名作为标题
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    
    md_content = f"""---
title: "来自 {domain}"
date: {date_str}
source: "{url}"
tags: [待分类]
---

## 核心摘要

> 待分析

## 关键信息抽取

| 项目 | 内容 |
|------|------|
| 来源 | [{domain}]({url}) |
| 收录时间 | {time_str} |
| 状态 | 🔄 处理中 |

## 信息增量

待对比分析

## 我的批注

{note if note else '（暂无批注）'}

---

*原文链接：[{url}]({url})*
"""
    return md_content

def save_and_push(url, note=""):
    """保存文章并推送到 GitHub"""
    
    # 生成文件名
    filename = sanitize_filename(url)
    filepath = f"/root/.openclaw/workspace/second-brain/content/articles/{filename}"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # 写入文件
    content = generate_article(url, note)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已创建: {filename}")
    
    # Git 操作
    repo_path = "/root/.openclaw/workspace/second-brain"
    try:
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'Add article: {url[:50]}...'], 
                      cwd=repo_path, check=True, capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'], 
                      cwd=repo_path, check=True, capture_output=True)
        print("🚀 已推送到 GitHub，网站将在 2-3 分钟后更新")
        print(f"📖 查看地址: https://andy03withai.github.io/second-brain/")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git 操作失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python process_article.py <URL> [批注]")
        sys.exit(1)
    
    url = sys.argv[1]
    note = sys.argv[2] if len(sys.argv) > 2 else ""
    
    save_and_push(url, note)
