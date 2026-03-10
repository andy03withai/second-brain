---
title: "Agent Skills 完全指南 - 我的核心见解"
date: 2026-03-10
source: "个人思考"
tags: [agent, skills, 我的见解]
---

# Agent Skills 完全指南 - 我的核心见解

**关联报告**: [[deep-research/2026-03-10-agent-skills-guide|Agent Skills 完全指南]]

---

## 核心见解 1: Skills 是 AI 时代的"函数库"

就像编程有标准库和自定义函数，AI Agent 也需要：
- **标准 Skills** - 官方或社区提供的通用能力
- **业务 Skills** - 团队根据业务流抽象的能力
- **个人 Skills** - 个人工作习惯的固化

**启示**: 我的 `/sb` 和 `/r` 命令本质上也是 Skills，只是目前硬编码在系统里。未来可以：
- 把这些能力抽象为可配置的 Skills
- 让用户自定义工作流

---

## 核心见解 2: 渐进式披露是关键设计

报告中提到的 "Progressive Disclosure" 机制非常关键：
- 启动时只加载元数据（100 tokens）
- 匹配时才加载完整内容
- 避免上下文爆炸

**启示**: 我的第二大脑设计也遵循了这个原则：
- 每日简报是「元数据」- 快速浏览
- 感兴趣的文章才深入「阅读全文」
- 有价值的才「收录消化」

可以优化：添加一个「快速预览」模式，类似 Twitter 的线程预览。

---

## 核心见解 3: 自进化是终极方向

Capability Evolver 和 Self-Improving Agent 排名靠前说明：
- 用户不满足于静态 AI
- 希望 AI 能从交互中学习
- 越用越懂我

**启示**: Ace 也可以有自进化能力：
- 记录用户的修改反馈
- 学习用户的偏好（如输出格式、深度级别）
- 自动优化 Prompt

**具体想法**:
```
用户: "/r Agent Skills"
Ace 生成报告
用户: "太深了，下次简短点"
Ace 记录: 用户偏好 shorter format
下次: 自动使用 standard 深度
```

---

## 行动计划

- [ ] 研究 Capability Evolver 的实现机制
- [ ] 设计 Ace 的偏好学习系统
- [ ] 尝试让 Ace 根据历史交互优化输出

---

*记录于 2026-03-10*
