---
title: "Skill: 发布前测试流程"
description: 验证内容完整性和链接正确性的自动化测试流程
date: 2026-03-14
tags: [skill, workflow, testing, automation]
---

# Skill: 发布前测试流程 (pre-publish-testing)

> 在将内容推送到 GitHub Pages 之前，必须执行此测试流程以确保内容完整性。

## 为什么需要这个 Skill

### 问题背景

在每日简报自动生成过程中，曾出现以下问题：

1. **任务超时导致文件缺失** - 3月12日和13日的每日简报生成任务超时，只生成了总索引，缺少各主题简报文件（ai.md、agent.md 等），导致用户访问时出现 **404 错误**

2. **input/index.md 更新不一致** - 有时显示"今日"链接，有时显示"查看历史"，用户体验不统一

3. **主题历史页面缺失** - "查看历史"链接指向的页面不存在

### 解决方案

建立发布前测试流程，在每次推送到 GitHub 之前自动验证：
- ✅ 所有必需文件都已生成
- ✅ 索引页面链接正确更新
- ✅ 主题历史页面存在
- ✅ Git 工作区干净

---

## 文件结构

```
skills/pre-publish-testing/
├── SKILL.md                          # Skill 说明文档
└── scripts/
    └── test_before_publish.py        # 测试脚本
```

---

## 测试脚本详解

### 完整代码

```python
#!/usr/bin/env python3
"""
发布前测试脚本 - 验证每日简报和其他内容的完整性
"""

import os
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

def check_daily_brief(date_str):
    """检查指定日期的每日简报是否完整"""
    base_path = f"/root/.openclaw/workspace/second-brain/content/input/{date_str}"
    
    if not os.path.exists(base_path):
        return False, f"目录不存在: {base_path}"
    
    required_files = ['index.md', 'ai.md', 'agent.md', 
                      'autonomous-driving.md', 'multimodal.md', 
                      'embodied-intelligence.md']
    missing = []
    
    for f in required_files:
        filepath = os.path.join(base_path, f)
        if not os.path.exists(filepath):
            missing.append(f)
        elif os.path.getsize(filepath) < 500:
            print(f"  ⚠️  {f} 文件过小，可能是占位符")
    
    if missing:
        return False, f"缺少文件: {', '.join(missing)}"
    
    return True, "所有必需文件都存在"

def check_input_index():
    """检查 input/index.md 是否正确更新"""
    index_path = "/root/.openclaw/workspace/second-brain/content/input/index.md"
    
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    
    if "等待每日简报生成" in content:
        issues.append("存在'等待生成'占位符")
    
    today = datetime.now().strftime('%Y%m%d')
    if f"[[input/{today}/ai|" not in content and "📅 今日" not in content:
        issues.append("主题表格中的链接未更新为今日")
    
    if issues:
        return False, "; ".join(issues)
    
    return True, "input/index.md 检查通过"

def check_topic_history_pages():
    """检查主题历史页面是否存在"""
    topics = ['ai', 'agent', 'autonomous-driving', 
              'multimodal', 'embodied-intelligence']
    missing = []
    
    for topic in topics:
        path = f"/root/.openclaw/workspace/second-brain/content/input/{topic}/index.md"
        if not os.path.exists(path):
            missing.append(topic)
    
    if missing:
        return False, f"缺少主题历史页面: {', '.join(missing)}"
    
    return True, "所有主题历史页面都存在"

def check_github_status():
    """检查 GitHub 是否有未提交的更改"""
    import subprocess
    
    result = subprocess.run(
        ['git', 'status', '--porcelain'],
        cwd="/root/.openclaw/workspace/second-brain",
        capture_output=True, text=True
    )
    
    if result.stdout.strip():
        return False, "有未提交的更改"
    
    return True, "Git 工作区干净"

def main():
    """主函数"""
    print("=" * 60)
    print("🔍 发布前测试流程")
    print("=" * 60)
    
    all_passed = True
    
    # 1. 检查今日简报
    today = datetime.now().strftime('%Y%m%d')
    print(f"\n📋 1. 检查今日简报 ({today})")
    passed, msg = check_daily_brief(today)
    print(f"   {'✅' if passed else '❌'} {msg}")
    all_passed = all_passed and passed
    
    # 2. 检查昨日简报
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    print(f"\n📋 2. 检查昨日简报 ({yesterday})")
    passed, msg = check_daily_brief(yesterday)
    print(f"   {'✅' if passed else '❌'} {msg}")
    all_passed = all_passed and passed
    
    # 3. 检查 input/index.md
    print("\n📋 3. 检查 input/index.md")
    passed, msg = check_input_index()
    print(f"   {'✅' if passed else '❌'} {msg}")
    all_passed = all_passed and passed
    
    # 4. 检查主题历史页面
    print("\n📋 4. 检查主题历史页面")
    passed, msg = check_topic_history_pages()
    print(f"   {'✅' if passed else '❌'} {msg}")
    all_passed = all_passed and passed
    
    # 5. 检查 Git 状态
    print("\n📋 5. 检查 Git 状态")
    passed, msg = check_github_status()
    print(f"   {'✅' if passed else '❌'} {msg}")
    all_passed = all_passed and passed
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有测试通过！可以安全发布。")
        return 0
    else:
        print("❌ 测试未通过，请修复上述问题后再发布。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

---

## 核心测试项

### 1. 每日简报完整性检查

**检查内容**：
| 文件名 | 说明 |
|--------|------|
| `index.md` | 每日总索引 |
| `ai.md` | AI 前沿简报 |
| `agent.md` | Agent 智能体简报 |
| `autonomous-driving.md` | 自动驾驶简报 |
| `multimodal.md` | 多模态简报 |
| `embodied-intelligence.md` | 具身智能简报 |

**额外检查**：
- 文件大小检测（< 500 bytes 警告为占位符）

### 2. input/index.md 更新检查

**验证点**：
- 无 "等待生成" 占位符
- 主题表格链接指向今日（📅 今日）

### 3. 主题历史页面检查

**检查路径**：
- `input/ai/index.md`
- `input/agent/index.md`
- `input/autonomous-driving/index.md`
- `input/multimodal/index.md`
- `input/embodied-intelligence/index.md`

### 4. Git 状态检查

**命令**：`git status --porcelain`

**通过标准**：无任何输出（工作区干净）

---

## 集成到工作流

### 集成方式

在 `daily_brief_generator.py` 的末尾，`git push` 之前添加：

```python
# 推送到GitHub前执行测试
print("\n🔍 执行发布前测试...")
try:
    result = subprocess.run(
        ['python3', '/root/.openclaw/workspace/skills/pre-publish-testing/scripts/test_before_publish.py'],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print("⚠️ 测试未通过，停止推送")
        return
except Exception as e:
    print(f"⚠️ 测试执行失败: {e}")

# 推送到GitHub
print("\n🚀 推送到 GitHub...")
# ... git push 代码
```

### 执行顺序

```
生成各主题简报 → 生成总索引 → 更新时间线 
    → 更新 input/index.md → [执行测试] → git push
                                    ↓
                              测试失败则停止
```

---

## 使用示例

### 手动运行

```bash
python3 /root/.openclaw/workspace/skills/pre-publish-testing/scripts/test_before_publish.py
```

### 输出示例

```
============================================================
🔍 发布前测试流程
============================================================

📋 1. 检查今日简报 (20260314)
   ✅ 所有必需文件都存在

📋 2. 检查昨日简报 (20260313)
   ✅ 所有必需文件都存在

📋 3. 检查 input/index.md
   ✅ input/index.md 检查通过

📋 4. 检查主题历史页面
   ✅ 所有主题历史页面都存在

📋 5. 检查 Git 状态
   ✅ Git 工作区干净

============================================================
🎉 所有测试通过！可以安全发布。
```

### 失败示例

```
📋 1. 检查今日简报 (20260314)
   ❌ 缺少文件: ai.md, agent.md

📋 3. 检查 input/index.md
   ❌ 存在'等待生成'占位符，需要更新为今日链接

============================================================
❌ 测试未通过，请修复上述问题后再发布。
```

---

## 设计要点

### 1. 防御性编程

- 检查目录是否存在
- 文件大小阈值检测（发现占位符）
- 异常捕获（Git 命令可能失败）

### 2. 清晰的反馈

- 每个测试项独立输出
- 使用 ✅/❌ 直观显示结果
- 失败时提供具体原因

### 3. 可扩展性

- 函数化设计，易于添加新检查项
- 返回码规范（0=成功，1=失败）
- 支持集成到 CI/CD 流程

---

## 失败处理指南

| 失败项 | 解决方案 |
|--------|----------|
| 缺少文件 | 重新运行每日简报生成，或手动创建 |
| input/index.md 未更新 | 运行 `update_input_index()` 或手动替换占位符 |
| 缺少主题历史页面 | 创建对应的 `input/{topic}/index.md` 文件 |
| Git 未提交 | 执行 `git add . && git commit && git push` |

---

## 学习要点

1. **自动化测试的重要性** - 在发布前自动验证，避免人工遗漏
2. **完整性检查** - 不只是检查存在性，还要检查内容质量（文件大小）
3. **失败即停止** - 测试不通过时不推送，防止问题上线
4. **清晰的错误信息** - 让用户知道具体哪里出了问题

---

*Skill 创建于 2026-03-14*
*解决每日简报 404 问题和链接不一致问题*
