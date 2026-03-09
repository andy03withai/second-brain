#!/usr/bin/env python3
"""
第二大脑 - 知识卡片生成器
基于李继刚 ljg-card 适配

简化版：生成 HTML 模板，截图功能待实现
"""

import sys
import os
import re
from datetime import datetime

def extract_card_content(article_content):
    """从文章提取卡片内容"""
    
    # 提取标题
    title_match = re.search(r'title:\s*"([^"]+)"', article_content)
    title = title_match.group(1) if title_match else "知识卡片"
    
    # 提取一句话摘要
    one_liner_match = re.search(r'一句话摘要：(.+)', article_content)
    one_liner = one_liner_match.group(1).strip() if one_liner_match else title
    
    # 提取核心论点
    points = []
    # 查找列表项
    for match in re.finditer(r'^[*-]\s*(.+)$', article_content, re.MULTILINE):
        point = match.group(1).strip()
        if len(point) > 10 and len(point) < 100:
            points.append(point)
        if len(points) >= 4:
            break
    
    # 提取来源
    source_match = re.search(r'source:\s*"([^"]+)"', article_content)
    source = source_match.group(1) if source_match else ""
    
    return {
        'title': title,
        'summary': one_liner,
        'points': points[:4],
        'source': source
    }

def generate_card_html(content, date_str):
    """生成卡片 HTML"""
    
    points_html = '\n'.join([f'      <li>{p}</li>' for p in content['points']]) if content['points'] else ''
    
    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');
    
    * {{
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }}
    
    body {{
      font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
      background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
      padding: 40px;
    }}
    
    .card {{
      width: 1080px;
      background: white;
      border-radius: 24px;
      padding: 80px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.1);
    }}
    
    .header {{
      margin-bottom: 48px;
    }}
    
    .date {{
      font-size: 18px;
      color: #999;
      margin-bottom: 16px;
      text-transform: uppercase;
      letter-spacing: 2px;
    }}
    
    .title {{
      font-size: 56px;
      font-weight: 700;
      color: #1a1a1a;
      line-height: 1.3;
      margin-bottom: 24px;
    }}
    
    .summary {{
      font-size: 28px;
      color: #666;
      line-height: 1.6;
      padding-left: 24px;
      border-left: 4px solid #4a90d9;
    }}
    
    .points {{
      margin-top: 48px;
    }}
    
    .points h3 {{
      font-size: 24px;
      color: #999;
      margin-bottom: 24px;
      text-transform: uppercase;
      letter-spacing: 1px;
    }}
    
    .points ul {{
      list-style: none;
    }}
    
    .points li {{
      font-size: 26px;
      color: #333;
      line-height: 1.8;
      margin-bottom: 16px;
      padding-left: 40px;
      position: relative;
    }}
    
    .points li::before {{
      content: "→";
      position: absolute;
      left: 0;
      color: #4a90d9;
      font-weight: bold;
    }}
    
    .footer {{
      margin-top: 60px;
      padding-top: 30px;
      border-top: 1px solid #eee;
      font-size: 18px;
      color: #999;
    }}
    
    .footer a {{
      color: #4a90d9;
      text-decoration: none;
    }}
  </style>
</head>
<body>
  <div class="card">
    <div class="header">
      <div class="date">{date_str}</div>
      <h1 class="title">{content['title']}</h1>
      <p class="summary">{content['summary']}</p>
    </div>
    
    <div class="points">
      <h3>核心要点</h3>
      <ul>
{points_html}
      </ul>
    </div>
    
    <div class="footer">
      收藏于 第二大脑 · {content['source'][:50]}{'...' if len(content['source']) > 50 else ''}
    </div>
  </div>
</body>
</html>"""
    
    return html

def generate_card(filepath):
    """生成知识卡片"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        article_content = f.read()
    
    # 提取内容
    content = extract_card_content(article_content)
    
    if not content['points']:
        print("⚠️ 未提取到足够的核心要点")
        return False
    
    # 生成文件名
    date_str = datetime.now().strftime('%Y%m%d')
    title_slug = re.sub(r'[^\w]', '-', content['title'])[:30]
    
    # 确保目录存在
    cards_dir = '/root/.openclaw/workspace/second-brain/assets/cards'
    os.makedirs(cards_dir, exist_ok=True)
    
    # 生成 HTML
    html = generate_card_html(content, date_str)
    html_path = f"{cards_dir}/{date_str}-{title_slug}.html"
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 已生成卡片 HTML: {html_path}")
    print(f"   标题: {content['title']}")
    print(f"   要点: {len(content['points'])} 个")
    
    # TODO: 使用 Playwright 截图生成 PNG
    print(f"   ⚠️ PNG 截图功能待实现（需要安装 Playwright）")
    
    return html_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python card_processor.py <文章路径>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    generate_card(filepath)
