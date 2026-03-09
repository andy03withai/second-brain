#!/usr/bin/env python3
"""
第二大脑 - 文章处理脚本
从飞书接收 /sb 命令，处理后推送到 GitHub

用法: python process_article.py "/sb https://xxx.com 批注"
"""

import sys
import os
import re
import json
import subprocess
from datetime import datetime
from urllib.parse import urlparse

sys.path.insert(0, '/usr/lib/node_modules/openclaw')

def sanitize_filename(url):
    """生成安全的文件名"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    path = parsed.path.strip('/').replace('/', '-')
    
    if path:
        name = path.split('-')[-1][:30]
    else:
        name = domain[:30]
    
    name = re.sub(r'[^\w\s-]', '', name).strip()
    name = re.sub(r'[-\s]+', '-', name)
    
    date_str = datetime.now().strftime('%Y%m%d')
    return f"{date_str}-{name or 'article'}.md"

def extract_url_and_note(text):
    """从 /sb 命令中提取 URL 和批注"""
    # 移除 /sb 前缀
    text = text.strip()
    if not text.startswith('/sb'):
        return None, None
    
    content = text[3:].strip()  # 移除 /sb
    
    # 提取 URL
    url_match = re.search(r'https?://[^\s]+', content)
    if not url_match:
        return None, None
    
    url = url_match.group(0)
    # 批注是 URL 之后的内容
    note = content[url_match.end():].strip()
    
    return url, note

def generate_article(url, note=""):
    """生成文章 Markdown"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
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
    
    filename = sanitize_filename(url)
    filepath = f"/root/.openclaw/workspace/second-brain/content/articles/{filename}"
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    content = generate_article(url, note)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已创建: {filename}")
    
    # 应用 sb-paper：论文检测（最先执行，可能改变文章结构）
    try:
        result = sp.run(
            ['python3', '/root/.openclaw/workspace/second-brain/scripts/paper_processor.py', filepath, url],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(result.stdout)
    except Exception as e:
        print(f"⚠️ 论文处理跳过: {e}")
    
    # 应用 sb-plain：白话化处理
    try:
        result = sp.run(
            ['python3', '/root/.openclaw/workspace/second-brain/scripts/plain_processor.py', filepath],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(result.stdout)
    except Exception as e:
        print(f"⚠️ 白话化处理跳过: {e}")
    
    # 应用 sb-writes：写作消化
    try:
        result = sp.run(
            ['python3', '/root/.openclaw/workspace/second-brain/scripts/writes_processor.py', filepath, note],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(result.stdout)
    except Exception as e:
        print(f"⚠️ 写作消化跳过: {e}")
    
    # 应用 sb-card：生成知识卡片
    try:
        result = sp.run(
            ['python3', '/root/.openclaw/workspace/second-brain/scripts/card_processor.py', filepath],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(result.stdout)
    except Exception as e:
        print(f"⚠️ 卡片生成跳过: {e}")
    
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
        print("用法: python process_article.py '\u003c/sb https://xxx.com 批注\u003e'")
        print("示例: python process_article.py '/sb https://example.com/article 讲AI的'")
        sys.exit(1)
    
    full_text = sys.argv[1]
    
    # 检查是否以 /sb 开头
    if not full_text.strip().startswith('/sb'):
        print("❌ 未检测到 /sb 命令，跳过第二大脑收录")
        print("提示：使用 /sb 开头触发收录，例如：/sb https://xxx.com 批注")
        sys.exit(0)
    
    url, note = extract_url_and_note(full_text)
    
    if not url:
        print("❌ 未能提取到 URL，请检查格式")
        print("正确格式：/sb https://example.com/article 批注")
        sys.exit(1)
    
    print(f"📝 检测到 /sb 命令")
    print(f"🔗 URL: {url}")
    print(f"💬 批注: {note or '(无)'}")
    print()
    
    save_and_push(url, note)
