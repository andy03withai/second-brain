#!/bin/bash
# 处理飞书发来的文章链接

URL="$1"
NOTE="$2"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date +%s)
SLUG=$(echo "$URL" | sed 's/[^a-zA-Z0-9]/-/g' | tr -s '-' | cut -c1-50)
FILENAME="${DATE}-${SLUG}.md"
CONTENT_DIR="/root/.openclaw/workspace/second-brain/content"

echo "正在处理: $URL"
echo "批注: $NOTE"

# 提取文章内容
echo "正在提取文章内容..."
ARTICLE_CONTENT=$(npx quartz fetch "$URL" 2>/dev/null || curl -sL "$URL" | head -c 10000)

# 生成 Markdown 文件
cat > "$CONTENT_DIR/articles/$FILENAME" << EOF
---
title: "${URL##*/}"
date: $DATE
source: "$URL"
tags: [待分类]
---

## 核心摘要

> 待生成

## 关键信息抽取

- 来源: $URL
- 收藏日期: $DATE

## 信息增量

待分析

## 我的批注

$NOTE

---

*原文链接: [$URL]($URL)*
EOF

echo "✅ 已创建: $FILENAME"

# 提交到 GitHub
cd /root/.openclaw/workspace/second-brain
git add .
git commit -m "Add article: $URL"
git push origin main

echo "🚀 已推送，网站将在几分钟后更新"
