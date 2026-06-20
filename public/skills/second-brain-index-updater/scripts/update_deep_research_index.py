#!/usr/bin/env python3
"""
第二大脑索引更新脚本 - 深度调研索引
扫描 deep-research/ 目录，自动生成索引表格
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

def estimate_word_count(file_path):
    """估算文件字数"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # 移除 frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                content = parts[2]
        # 估算中文字符和英文单词
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_words = len(re.findall(r'[a-zA-Z]+', content))
        return chinese_chars + english_words
    except:
        return 0

def get_depth_from_tags(tags):
    """从标签获取深度级别"""
    if not tags:
        return "standard"
    if 'comprehensive' in tags:
        return "comprehensive"
    elif 'deep' in tags:
        return "deep"
    return "standard"

def scan_deep_research(content_dir):
    """扫描深度调研目录"""
    dr_dir = Path(content_dir) / "deep-research"
    reports = []
    
    if not dr_dir.exists():
        return reports
    
    for item in dr_dir.iterdir():
        if item.is_dir():
            # 子目录模式：2026-03-18-coding-agent-deep-research/index.md
            index_file = item / "index.md"
            if index_file.exists():
                with open(index_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                fm = extract_frontmatter(content)
                
                date_str = item.name[:10]  # 2026-03-18
                try:
                    date = datetime.strptime(date_str, "%Y-%m-%d")
                except:
                    date = datetime.fromtimestamp(item.stat().st_mtime)
                
                word_count = estimate_word_count(index_file)
                word_str = f"~{word_count//1000*1000}" if word_count > 1000 else f"~{word_count}"
                
                reports.append({
                    'date': date,
                    'date_str': date.strftime("%Y-%m-%d"),
                    'title': fm.get('title', item.name[11:].replace('-', ' ').title()),
                    'depth': get_depth_from_tags(fm.get('tags', [])),
                    'words': word_str,
                    'link': f"[[deep-research/{item.name}|查看报告]]"
                })
        elif item.suffix == '.md' and item.name != 'index.md':
            # 旧格式：2026-03-10-agent-skills-guide.md
            with open(item, 'r', encoding='utf-8') as f:
                content = f.read()
            fm = extract_frontmatter(content)
            
            date_str = item.stem[:10]
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
            except:
                date = datetime.fromtimestamp(item.stat().st_mtime)
            
            word_count = estimate_word_count(item)
            word_str = f"~{word_count//1000*1000}" if word_count > 1000 else f"~{word_count}"
            
            reports.append({
                'date': date,
                'date_str': date.strftime("%Y-%m-%d"),
                'title': fm.get('title', item.stem[11:].replace('-', ' ').title()),
                'depth': get_depth_from_tags(fm.get('tags', [])),
                'words': word_str,
                'link': f"[[deep-research/{item.stem}|查看报告]]"
            })
    
    # 按日期倒序排列
    reports.sort(key=lambda x: x['date'], reverse=True)
    return reports

def generate_index_content(reports):
    """生成索引文件内容"""
    lines = [
        "---",
        "title: Deep Research - 深度调研",
        "description: 系统性深度调研报告，涵盖技术、商业、学术等多维度分析",
        "---",
        "",
        "# 🔬 Deep Research - 深度调研",
        "",
        "这里存放系统性深度调研报告。",
        "",
        "## 调研方法论",
        "",
        "每次调研包含：",
        "1. **多轮信息收集** - 基础概念 → 最新进展 → 深度分析 → 延伸探索",
        "2. **信息整合** - 去重、验证、分类、对比",
        "3. **结构化输出** - 执行摘要、背景、分析、案例、趋势、结论",
        "",
        "## 报告列表",
        "",
        "| 日期 | 主题 | 深度 | 字数 | 链接 |",
        "|------|------|------|------|------|"
    ]
    
    for report in reports:
        lines.append(f"| {report['date_str']} | {report['title']} | {report['depth']} | {report['words']} | {report['link']} |")
    
    lines.extend([
        "",
        "---",
        "",
        "*使用 `/r <主题>` 命令发起新的深度调研*"
    ])
    
    return "\n".join(lines)

def main():
    # 获取脚本所在目录
    script_dir = Path(__file__).parent.parent
    content_dir = script_dir.parent.parent  # 指向 content/ 目录
    
    # 扫描报告
    reports = scan_deep_research(content_dir)
    
    if not reports:
        print("未找到深度调研报告")
        return
    
    # 生成索引内容
    index_content = generate_index_content(reports)
    
    # 写入文件
    index_path = content_dir / "deep-research" / "index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"✅ 已更新深度调研索引: {index_path}")
    print(f"📊 共 {len(reports)} 份报告")
    for r in reports[:5]:
        print(f"  - {r['date_str']}: {r['title']}")

if __name__ == "__main__":
    main()
