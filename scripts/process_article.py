#!/usr/bin/env python3
"""
第二大脑 - 文章处理脚本（支持多链接）
从飞书接收 /sb 命令，处理多个相关链接

用法: python process_article.py "/sb https://xxx.com https://yyy.com 批注"
"""

import sys
import os
import re
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

def extract_urls_and_note(text):
    """从 /sb 命令中提取所有 URL 和批注"""
    text = text.strip()
    if not text.startswith('/sb'):
        return [], None
    
    content = text[3:].strip()  # 移除 /sb
    
    # 提取所有 URL
    urls = re.findall(r'https?://[^\s]+', content)
    
    if not urls:
        return [], None
    
    # 批注是最后一个 URL 之后的内容
    last_url_end = content.rfind(urls[-1]) + len(urls[-1])
    note = content[last_url_end:].strip()
    
    return urls, note

def generate_article(url, note="", related_urls=None):
    """生成文章 Markdown"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    
    # 相关链接部分
    related_section = ""
    if related_urls:
        related_section = "\n## 相关链接\n\n"
        for i, related_url in enumerate(related_urls, 1):
            related_section += f"{i}. [{related_url}]({related_url})\n"
    
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
{related_section}
## 信息增量

待对比分析

## 我的批注

{note if note else '（暂无批注）'}

---

*原文链接：[{url}]({url})*
"""
    return md_content

def generate_index_article(urls, note=""):
    """生成主索引文章（当有多链接时）"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    # 生成相关文章列表
    related_list = "\n".join([f"{i+1}. [{url}]({url})" for i, url in enumerate(urls)])
    
    md_content = f"""---
title: "主题收录 - {len(urls)} 个相关资源"
date: {date_str}
source: "多链接收录"
tags: [待分类, 主题收录]
---

## 核心摘要

> 一句话摘要：待补充

一段话摘要：
待补充

## 收录资源

{related_list}

## 信息增量

待对比分析各资源之间的关系

## 我的批注

{note if note else '（暂无批注）'}

---

*收录时间：{time_str}*
"""
    return md_content

def process_single_article(url, note, related_urls=None):
    """处理单篇文章"""
    filename = sanitize_filename(url)
    filepath = f"/root/.openclaw/workspace/second-brain/content/articles/{filename}"
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # 过滤掉当前 URL 自身的相关链接
    other_related = [u for u in (related_urls or []) if u != url]
    
    content = generate_article(url, note, other_related if other_related else None)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已创建: {filename}")
    
    # 应用技能处理
    processors = [
        ('paper', '/root/.openclaw/workspace/second-brain/scripts/paper_processor.py'),
        ('plain', '/root/.openclaw/workspace/second-brain/scripts/plain_processor.py'),
        ('writes', '/root/.openclaw/workspace/second-brain/scripts/writes_processor.py'),
        ('card', '/root/.openclaw/workspace/second-brain/scripts/card_processor.py'),
    ]
    
    for name, processor_path in processors:
        try:
            result = subprocess.run(
                ['python3', processor_path, filepath, url],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                print(f"  {result.stdout.strip()}")
        except Exception as e:
            pass  # 静默跳过错误
    
    return filename

def save_and_push(urls, note=""):
    """保存文章并推送到 GitHub"""
    
    created_files = []
    
    if len(urls) == 1:
        # 单链接：直接处理
        filename = process_single_article(urls[0], note)
        created_files.append(filename)
    else:
        # 多链接：创建主索引 + 各子文章
        print(f"📝 检测到 {len(urls)} 个相关链接")
        print()
        
        # 先创建各子文章
        for i, url in enumerate(urls, 1):
            print(f"[{i}/{len(urls)}] 处理: {url[:60]}...")
            filename = process_single_article(url, note, urls)
            created_files.append(filename)
            print()
        
        # 创建主索引文章
        index_filename = f"{datetime.now().strftime('%Y%m%d')}-theme-index.md"
        index_filepath = f"/root/.openclaw/workspace/second-brain/content/articles/{index_filename}"
        
        index_content = generate_index_article(urls, note)
        with open(index_filepath, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        created_files.append(index_filename)
        print(f"✅ 已创建主题索引: {index_filename}")
    
    # 更新首页 index.md
    print("\n📝 更新首页文章列表...")
    for filename in created_files[:5]:  # 最多更新前5篇文章（避免过多）
        filepath = f"/root/.openclaw/workspace/second-brain/content/articles/{filename}"
        try:
            subprocess.run(
                ['python3', '/root/.openclaw/workspace/second-brain/scripts/index_updater.py', '--article', filepath],
                check=True,
                capture_output=True
            )
        except subprocess.CalledProcessError:
            pass  # 静默跳过错误
    print("✅ 首页已更新")
    
    # Git 提交
    repo_path = "/root/.openclaw/workspace/second-brain"
    try:
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True, capture_output=True)
        
        if len(urls) == 1:
            commit_msg = f'Add article: {urls[0][:50]}...'
        else:
            commit_msg = f'Add theme with {len(urls)} links'
        
        subprocess.run(['git', 'commit', '-m', commit_msg], 
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
        print("用法: python process_article.py '\u003c/sb URL [URL2 URL3...] 批注\u003e'")
        print("示例:")
        print("  单链接: /sb https://example.com/article 讲AI的")
        print("  多链接: /sb https://podcast.com/ep1 https://blog.com/transcript 播客+文字稿")
        sys.exit(1)
    
    full_text = sys.argv[1]
    
    if not full_text.strip().startswith('/sb'):
        print("❌ 未检测到 /sb 命令，跳过第二大脑收录")
        sys.exit(0)
    
    urls, note = extract_urls_and_note(full_text)
    
    if not urls:
        print("❌ 未能提取到 URL，请检查格式")
        print("正确格式：/sb https://example.com/article 批注")
        sys.exit(1)
    
    print(f"📝 检测到 /sb 命令")
    print(f"🔗 链接数: {len(urls)}")
    for i, url in enumerate(urls, 1):
        print(f"   [{i}] {url}")
    print(f"💬 批注: {note or '(无)'}")
    print()
    
    save_and_push(urls, note)
