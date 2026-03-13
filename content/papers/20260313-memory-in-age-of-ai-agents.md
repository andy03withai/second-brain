---
title: "Memory in the Age of AI Agents"
authors: ["Yuyang Hu", "Shichun Liu", "Yanwei Yue", "Guibin Zhang", "Boyang Liu", "Fangyi Zhu", "Jiahang Lin", "Honglin Guo", "Shihan Dou", "Zhiheng Xi", "Senjie Jin", "Jiejun Tan", "Yanbin Yin", "Jiongnan Liu", "Zeyu Zhang", "Zhongxiang Sun", "Yutao Zhu", "Hao Sun", "Boci Peng", "Zhenrong Cheng", "Xuanbo Fan", "Jiaxin Guo", "Xinlei Yu", "Zhenhong Zhou", "Zewen Hu", "Jiahao Huo", "Junhao Wang", "Yuwei Niu", "Yu Wang", "Zhenfei Yin", "Xiaobin Hu", "Yue Liao", "Qiankun Li", "Kun Wang", "Wangchunshu Zhou", "Yixin Liu", "Dawei Cheng", "Qi Zhang", "Tao Gui", "Shirui Pan", "Yan Zhang", "Philip Torr", "Zhicheng Dou", "Ji-Rong Wen", "Xuanjing Huang", "Yu-Gang Jiang", "Shuicheng Yan"]
date: 2025-12-15
arxiv: "2512.13564"
category: "AI与Agents"
tags: [paper, survey, agent-memory, AI-agents]
---

# Memory in the Age of AI Agents

**Authors**: Yuyang Hu et al. (47 authors)
**arXiv**: [2512.13564](https://arxiv.org/abs/2512.13564)
**Submitted**: Dec 15, 2025 | Revised: Jan 13, 2026

---

## 摘要

记忆已成为、并将继续成为基于基础模型的智能体的核心能力。随着智能体记忆研究的迅速扩展和空前关注，该领域也变得越来越碎片化。现有的智能体记忆相关研究在动机、实现和评估协议上往往存在显著差异，而大量 loosely defined 的记忆术语进一步模糊了概念清晰度。传统的长期/短期记忆分类已不足以捕捉当代智能体记忆系统的多样性。

本文旨在提供当前智能体记忆研究的最新全景图。我们首先明确界定智能体记忆的范围，并将其与相关概念（如LLM记忆、检索增强生成RAG和上下文工程）区分开来。然后，我们从**形式**、**功能**和**动态**三个统一视角审视智能体记忆：

- **形式视角**：识别三种主导实现——token级记忆、参数记忆和隐式记忆
- **功能视角**：提出细粒度分类，区分事实记忆、经验记忆和工作记忆
- **动态视角**：分析记忆如何随时间形成、演化和检索

本文还编制了记忆基准测试和开源框架的综合总结，并对新兴研究前沿（包括记忆自动化、强化学习集成、多模态记忆、多智能体记忆和可信度问题）提出前瞻性观点。

---

## 核心贡献

1. **概念澄清**：明确区分 agent memory vs LLM memory vs RAG vs 上下文工程
2. **三维分析框架**：形式（Forms）、功能（Functions）、动态（Dynamics）
3. **实践资源汇总**：记忆基准测试和开源框架
4. **前瞻性展望**：记忆自动化、RL集成、多模态/多智能体记忆、可信度

---

## 与我的工作关联

- 第二大脑系统本身就是一种**外部记忆系统**
- 可借鉴本文的分类法来组织笔记/记忆结构
- 多智能体记忆与 Agent Network 项目相关

---

**收录时间**: 2026-03-13
**收录命令**: `/paper https://arxiv.org/abs/2512.13564 Memory in the Age of AI Agents`
