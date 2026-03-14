---
title: "Skills - Agent 技能库"
description: 我设计的 Agent Skills，解决实际工作中的问题
---

# 🛠️ Skills - Agent 技能库

这里是我为了解决特定问题而设计的 Agent Skills，每个 skill 都包含完整的文档和可运行的脚本。

---

## 已发布的 Skills

### [[pre-publish-testing|发布前测试流程]]

**问题**: 每日简报生成任务超时，导致部分主题文件缺失，用户访问 404

**解决**: 在推送到 GitHub Pages 之前自动验证：
- 每日简报 6 个文件完整性
- input/index.md 链接更新状态
- 5 个主题历史页面存在性
- Git 工作区干净

**技术**: Python 脚本，集成到 daily_brief_generator.py

**状态**: ✅ 已集成到每日工作流

---

## Skill 设计原则

1. **解决实际问题** - 每个 skill 都源于真实的工作痛点
2. **可自动化** - 尽量减少人工干预
3. **可验证** - 有明确的通过/失败标准
4. **可复用** - 设计时考虑多种使用场景

---

## 如何使用这些 Skills

### 方式一：直接运行

```bash
python3 /root/.openclaw/workspace/skills/{skill-name}/scripts/{script}.py
```

### 方式二：集成到工作流

参考各 skill 文档中的"集成到工作流"章节

### 方式三：学习借鉴

阅读 SKILL.md 和脚本源码，了解设计思路

---

*Skills 目录持续更新中...*
