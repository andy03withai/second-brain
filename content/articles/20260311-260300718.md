---
title: "SkillCraft: Can LLM Agents Learn to Use Tools Skillfully?"
date: 2026-03-11
source: "https://arxiv.org/abs/2603.00718"
tags: [待分类, arxiv, agent, skill]
---

## 核心摘要

> 一句话摘要：SkillCraft 提出了一个评估 LLM Agent 学习并复用工具组合能力（Skills）的基准测试，通过技能复用可降低 80% token 使用量。

一段话摘要：
这篇论文提出了 SkillCraft 基准测试，专门评估 LLM Agent 形成和复用高级工具组合（称为 Skills）的能力。现有基准主要测量实例级成功率，而 SkillCraft 测试 agent 在真实、高度组合化的工具使用场景中抽象和跨任务复用技能的能力。研究发现，通过技能保存和复用，token 使用量可降低 80%，且成功率与测试时的工具组合能力强相关。

## 论文速读

### 基本信息
- **标题**: SkillCraft: Can LLM Agents Learn to Use Tools Skillfully?
- **作者**: Shiqi Chen, Jingze Gai, Ruochen Zhou, Jinghan Zhang, Tongyao Zhu, Junlong Li, Kangrui Wang, Zihan Wang, Zhengyu Chen, Klara Kaleb, Ning Miao, Siyang Gao, Cong Lu, Manling Li, Junxian He, Yee Whye Teh
- **来源**: [arXiv:2603.00718](https://arxiv.org/abs/2603.00718)
- **发布时间**: 2026-02-28
- **收录时间**: 2026-03-11

### 研究问题
现有 benchmarks 主要测量 instance-level 成功率，无法评估 agents 获取可复用技能的能力。如何测试 agent 形成和复用高级工具组合（Skills）的能力？

### 方法
- 提出 SkillCraft 基准测试，包含真实、高度组合化的工具使用场景
- 难度在定量和结构维度上递进
- 轻量级评估协议：支持 agent 自动将原子工具组合成可执行 Skills

### 核心结论
1. 通过技能保存和复用，token 使用量可降低 **80%**
2. 成功率与测试时的工具组合能力强相关
3. 组合技能获取是 agent 的核心能力

### 局限与未来工作
- 场景复杂度仍可扩展
- 跨领域技能迁移能力待验证

### 可复现性
- [x] 论文公开
- [ ] 代码公开（待确认）
- [ ] 数据公开（待确认）

### 质量评估
- **创新性**: ★★★★☆（新基准测试）
- **严谨性**: ★★★★☆（多维度评估）
- **影响力**: ★★★★☆（对 Agent 技能学习有重要启发）

## 信息增量

## 通过写作消化

原文核心论点：
1. 现有 benchmarks 无法评估 agents 获取可复用技能的能力
2. SkillCraft 提供真实、高度组合化的工具使用场景
3. 技能保存和复用可显著降低 token 使用量（80%）
4. 成功率与工具组合能力正相关
5. 组合技能获取是 agent 的核心能力

写作问题：
- [ ] 这篇论文提出的 SkillCraft 基准与你已知的其他 agent 评测方法（如 SWE-bench、WebArena）有什么本质区别？
- [ ] "技能复用降低 80% token"这一发现，对实际应用中的 agent 系统设计有什么启发？
- [ ] 如果质疑这个基准的有效性，你会从哪些角度切入？
- [ ] 这篇论文的结论边界在哪里？在什么类型的任务上可能不适用？
- [ ] 顺着"技能抽象和复用"的思路，还能推出什么新的研究方向？

建议的写作方向：
- **对比**：与现有的 agent 评测基准比较优劣势
- **应用**：如何将技能复用机制应用到你的 agent 系统中？  
- **质疑**：这个基准是否真正捕捉到了"技能"的本质？
- **延伸**：如何设计一个持续学习、不断积累技能的 agent 架构？


## 我的批注

SkillCraft论文：评估LLM Agent学习和复用工具技能的能力

---

*原文链接：[https://arxiv.org/abs/2603.00718](https://arxiv.org/abs/2603.00718)*
