#!/usr/bin/env python3
"""
第二大脑 - 白话化处理器
基于李继刚 ljg-plain 适配
"""

import sys
import re

def plain_summary(content):
    """
    将复杂内容转换为白话摘要
    遵循：好问题 + 类比 + 裂缝 结构
    """
    
    # 提取核心论点（简化版）
    lines = content.strip().split('\n')
    key_points = []
    
    for line in lines:
        line = line.strip()
        # 提取标题、列表项
        if line.startswith('# ') or line.startswith('## '):
            key_points.append(line.lstrip('# ').strip())
        elif line.startswith('- ') or line.startswith('* '):
            key_points.append(line[2:].strip())
    
    if not key_points:
        return "内容暂无法解析", "需要进一步分析"
    
    # 生成一句话摘要（取第一个关键点做类比）
    main_point = key_points[0][:50]
    one_liner = f"就像{main_point}..." if len(main_point) < 40 else main_point[:47] + "..."
    
    # 生成一段话摘要
    # 简化版：好问题 + 核心内容 + 反思
    if len(key_points) >= 2:
        paragraph = f"为什么{key_points[0]}？{key_points[1]}。"
        if len(key_points) > 2:
            paragraph += f"这意味着{key_points[2]}。"
    else:
        paragraph = key_points[0]
    
    # 限制长度
    one_liner = one_liner[:50]
    paragraph = paragraph[:150] + "..." if len(paragraph) > 150 else paragraph
    
    return one_liner, paragraph

def update_article_summary(filepath):
    """更新文章的白话化摘要"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取正文（移除 frontmatter）
    body_match = re.search(r'---\n.*?---\n(.*)', content, re.DOTALL)
    if not body_match:
        print("未找到文章正文")
        return False
    
    body = body_match.group(1)
    
    # 生成摘要
    one_liner, paragraph = plain_summary(body)
    
    # 替换核心摘要部分
    new_summary = f"""## 核心摘要

> 一句话摘要：{one_liner}

一段话摘要：
{paragraph}
"""
    
    # 替换旧的核心摘要
    updated_content = re.sub(
        r'## 核心摘要\n\n> 待分析',
        new_summary.strip(),
        content
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ 已生成白话摘要")
    print(f"   一句话：{one_liner}")
    print(f"   一段话：{paragraph[:80]}...")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python plain_processor.py <文章路径>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    update_article_summary(filepath)
