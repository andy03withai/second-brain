#!/usr/bin/env python3
"""
第二大脑 - 深度调研报告生成器
处理 /r 命令，生成深度调研报告

用法: python deep_research.py "主题" [--depth standard|deep|comprehensive]
"""

import os
import sys
import re
import subprocess
from datetime import datetime

sys.path.insert(0, '/usr/lib/node_modules/openclaw')

def sanitize_filename(topic):
    """生成安全的文件名"""
    # 移除特殊字符，保留中文、英文、数字
    name = re.sub(r'[^\w\u4e00-\u9fff\s-]', '', topic).strip()
    name = re.sub(r'[-\s]+', '-', name)
    
    date_str = datetime.now().strftime('%Y-%m-%d')
    return f"{date_str}-{name or 'research'}.md"

def generate_research_report(topic, depth="standard"):
    """生成调研报告 Markdown 模板"""
    date_str = datetime.now().strftime('%Y-%m-%d')
    time_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    depth_display = {
        "standard": "标准深度 (3-4k字)",
        "deep": "深度 (5-7k字)",
        "comprehensive": "全面 (8k+字)"
    }.get(depth, "标准深度")
    
    md_content = f"""---
title: "{topic} 深度调研报告"
date: {date_str}
research_method: "OpenAI Deep Research 4-Pillar Framework"
depth: {depth}
topics: [{topic}]
sources_count: 待统计
verification_status: 待验证
word_count: 待统计
---

# {topic} 深度调研报告

## 🎯 执行摘要 (Executive Summary)

### 核心发现
> 待补充：3-5条核心发现

### 关键结论
- 待补充

### 建议行动
- [ ] 待补充

---

## 1. 研究方法论

本次调研采用 **OpenAI Deep Research** 方法论，遵循四大支柱：
- **Expansion**: 从核心主题扩展至相关领域
- **Recursive Browsing**: 递归钻取关键信息
- **Cross-verification**: 多源交叉验证
- **Synthesis**: 综合形成洞察

研究深度: {depth_display}  
信息截止日期: {date_str}

---

## 2. 背景与定义

### 2.1 什么是{topic}
[定义说明]

### 2.2 发展历程
| 时间 | 里程碑 | 意义 |
|------|--------|------|
| YYYY | 事件 | 影响 |

### 2.3 核心概念解析
| 术语 | 定义 | 说明 |
|------|------|------|
| 术语1 | ... | ... |

---

## 3. 现状分析

### 3.1 技术现状
[技术分析]

### 3.2 市场格局
[市场分析]

### 3.3 主要玩家
| 公司/机构 | 角色 | 关键产品/贡献 | 来源 |
|-----------|------|---------------|------|
| 玩家1 | ... | ... | [链接] |

---

## 4. 深度分析

### 4.1 技术方案对比
| 方案 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| 方案A | ... | ... | ... |
| 方案B | ... | ... | ... |

### 4.2 商业模式分析
[商业分析]

### 4.3 竞争态势
[竞争分析]

---

## 5. 观点与争议

### 5.1 主流观点
- **观点一**: ... (来源: [链接])

### 5.2 反对声音
- **反驳一**: ... (来源: [链接])

### 5.3 未决问题
[争议点]

---

## 6. 案例研究

### 6.1 案例一: [名称]
**背景**: ...  
**做法**: ...  
**结果**: ...  
**启示**: ...

---

## 7. 趋势与预测

### 7.1 技术趋势
- 趋势一...

### 7.2 市场预测
[预测分析]

### 7.3 潜在风险
| 风险 | 可能性 | 影响 | 应对 |
|------|--------|------|------|
| 风险1 | 高/中/低 | 大/中/小 | ... |

---

## 8. 结论与建议

### 8.1 核心结论
1. ...

### 8.2 行动建议
- **短期**: ...
- **中期**: ...
- **长期**: ...

### 8.3 进一步研究
- 待研究问题一

---

## 📚 参考资料

### 主要来源
1. [标题](链接) - 来源类型 - 关键信息

### 延伸阅读
1. [标题](链接)

---

*本报告由 AI 深度调研系统生成*  
*方法论: OpenAI Deep Research 4-Pillar Framework*  
*生成时间: {time_str}*
"""
    return md_content

def save_and_push(topic, depth="standard"):
    """保存调研报告并推送到 GitHub"""
    
    filename = sanitize_filename(topic)
    filepath = f"/root/.openclaw/workspace/second-brain/content/deep-research/{filename}"
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    content = generate_research_report(topic, depth)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 已创建调研报告: {filename}")
    
    # 更新首页 index.md
    print("📝 更新首页调研报告列表...")
    try:
        subprocess.run(
            ['python3', '/root/.openclaw/workspace/second-brain/scripts/index_updater.py', '--research', filepath],
            check=True,
            capture_output=True
        )
        print("✅ 首页已更新")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ 首页更新失败: {e}")
    
    # Git 提交
    repo_path = "/root/.openclaw/workspace/second-brain"
    try:
        subprocess.run(['git', 'add', '.'], cwd=repo_path, check=True, capture_output=True)
        commit_msg = f'Add research report: {topic[:50]}... ({depth})'
        subprocess.run(['git', 'commit', '-m', commit_msg], 
                      cwd=repo_path, check=True, capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'], 
                      cwd=repo_path, check=True, capture_output=True)
        
        # 生成具体页面网址
        report_name = filename.replace('.md', '')
        page_url = f"https://andy03withai.github.io/second-brain/deep-research/{report_name}"
        
        print(f"🚀 已推送到 GitHub，网站将在 2-3 分钟后更新")
        print(f"📖 页面地址: {page_url}")
        
        return page_url
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Git 操作失败: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("用法: python deep_research.py '\u003c主题>' [--depth standard|deep|comprehensive]")
        print("示例:")
        print('  python deep_research.py "AI Agent 在电商领域的应用"')
        print('  python deep_research.py "具身智能最新进展" --depth deep')
        sys.exit(1)
    
    # 解析参数
    topic = sys.argv[1]
    depth = "standard"
    
    if '--depth' in sys.argv:
        depth_index = sys.argv.index('--depth') + 1
        if depth_index < len(sys.argv):
            depth = sys.argv[depth_index]
    
    print(f"🔬 开始深度调研: {topic}")
    print(f"📊 深度级别: {depth}")
    print()
    
    save_and_push(topic, depth)

if __name__ == "__main__":
    main()
