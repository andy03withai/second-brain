#!/usr/bin/env python3
"""
第二大脑 - 写作消化处理器
基于李继刚 ljg-writes 适配
"""

import sys
import re

def generate_writing_prompts(article_content, user_note=""):
    """
    从文章内容生成写作提示
    遵循：对话 + 断裂 + 填补 结构
    """
    
    # 提取核心论点
    key_points = []
    lines = article_content.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        # 提取标题、列表项
        if line.startswith('## ') and '摘要' not in line and '信息' not in line:
            key_points.append(line.lstrip('## ').strip())
        elif line.startswith('- ') and len(line) > 5:
            key_points.append(line[2:].strip())
    
    key_points = key_points[:5]  # 最多 5 个
    
    if not key_points:
        key_points = ["文章核心观点", "作者的主要论据"]
    
    # 生成写作问题
    questions = [
        f"'{key_points[0]}' 让你联想到什么个人经验或已知知识？",
        f"如果质疑 '{key_points[0] if key_points else '作者观点'}'，你会从哪里切入？",
        "这篇文章的结论边界在哪里？在什么情况下不适用？",
        "如果把文章的核心观点推到极致，会得出什么结论？",
    ]
    
    # 如果用户有批注，加入
    if user_note:
        questions.insert(0, f"你提到 '{user_note}'——顺着这个思路还能想到什么？")
    
    return key_points, questions

def update_article_writes(filepath, user_note=""):
    """在文章中添加写作消化部分"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取正文
    body_match = re.search(r'---\n.*?---\n(.*)', content, re.DOTALL)
    if not body_match:
        print("未找到文章正文")
        return False
    
    body = body_match.group(1)
    key_points, questions = generate_writing_prompts(body, user_note)
    
    # 生成写作部分
    points_text = '\n'.join([f"{i+1}. {p}" for i, p in enumerate(key_points)])
    questions_text = '\n'.join([f"- [ ] {q}" for q in questions[:4]])
    
    writes_section = f"""## 通过写作消化

原文核心论点：
{points_text}

写作问题：
{questions_text}

建议的写作方向：
- **对比**：这个观点与你已知的概念有什么异同？
- **应用**：这个观点可以在什么场景下使用？  
- **质疑**：这个结论的边界在哪里？
- **延伸**：顺着这个思路还能推出什么？

> 💡 提示：选择 1-2 个问题，用 10 分钟写一段思考。不需要完整，只需要开始。
"""
    
    # 替换信息增量部分或插入到批注前
    if '## 信息增量' in content and '待对比分析' in content:
        content = content.replace(
            '## 信息增量\n\n待对比分析',
            f'## 信息增量\n\n{writes_section}'
        )
    else:
        # 插入到我的批注之前
        content = content.replace(
            '## 我的批注',
            f'{writes_section}\n\n## 我的批注'
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已添加写作消化提示")
    print(f"   核心论点: {len(key_points)} 个")
    print(f"   写作问题: {len(questions)} 个")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python writes_processor.py <文章路径> [用户批注]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    user_note = sys.argv[2] if len(sys.argv) > 2 else ""
    update_article_writes(filepath, user_note)
