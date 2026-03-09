#!/usr/bin/env python3
"""
第二大脑 - 论文处理器
基于李继刚 ljg-paper 适配
检测论文链接，生成结构化速读
"""

import sys
import re

def detect_paper(url, content=""):
    """检测是否为论文链接"""
    
    # 检测 arxiv
    if 'arxiv.org' in url:
        arxiv_match = re.search(r'arxiv\.org/abs/(\d+\.\d+)', url)
        if arxiv_match:
            return 'arxiv', arxiv_match.group(1)
    
    # 检测其他论文特征
    if 'paper' in content.lower() or '论文' in content:
        return 'paper', None
    
    return None, None

def generate_paper_template(url, paper_type, paper_id):
    """生成论文速读模板"""
    
    arxiv_link = f"https://arxiv.org/abs/{paper_id}" if paper_id else url
    
    template = f"""
## 论文速读

### 基本信息
- **来源**: [{paper_type.upper()}]({arxiv_link})
- **arxiv ID**: {paper_id or 'N/A'}
- **收录时间**: （自动生成）

### 研究问题
（待提取：论文试图解决什么问题？）

### 方法
（待提取：使用了什么方法/技术路线？）

### 核心结论
1. （待提取：结论1）
2. （待提取：结论2）
3. （待提取：结论3）

### 局限与未来工作
- （待提取：局限1）
- （待提取：局限2）

### 可复现性
- [ ] 代码公开
- [ ] 数据公开
- [ ] 实验可复现

### 质量评估
- **创新性**: （待评估）
- **严谨性**: （待评估）
- **影响力**: （待评估）
"""
    return template.strip()

def process_paper(filepath, url):
    """处理论文文章"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检测论文类型
    paper_type, paper_id = detect_paper(url, content)
    
    if not paper_type:
        print("ℹ️ 未检测到论文链接，跳过论文处理")
        return False
    
    print(f"📄 检测到 {paper_type.upper()} 论文")
    if paper_id:
        print(f"   ID: {paper_id}")
    
    # 生成论文模板
    paper_section = generate_paper_template(url, paper_type, paper_id)
    
    # 替换关键信息抽取部分
    updated_content = re.sub(
        r'## 关键信息抽取\n\n\| 项目 \| 内容 \|\n\|------\|------\|\n\| 来源 \| .*? \|\n\| 收录时间 \| .*? \|\n\| 状态 \| .*? \|',
        paper_section,
        content,
        flags=re.DOTALL
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ 已生成论文速读模板")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python paper_processor.py <文章路径> <URL>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    url = sys.argv[2]
    process_paper(filepath, url)
