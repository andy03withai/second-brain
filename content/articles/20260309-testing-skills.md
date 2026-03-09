---
title: "Testing Agent Skills: 实战指南"
date: 2026-03-09
source: "https://www.philschmid.de/testing-skills"
tags: [skills, testing, evals, agent, philip-schmid]
---

## 核心摘要

> 一句话摘要：就像给代码写单元测试一样，给 Agent Skills 写评估——从 66.7% 到 100% 通过率的实战方法。

一段话摘要：
为什么大多数 Skills 没有经过测试？Philip Schmid 分享了评估 Agent Skills 的完整流程：定义成功标准、构建轻量级评估框架、迭代优化。他用 Gemini Interactions API skill 作为案例，通过重写描述（匹配用户意图而非 API 术语）、添加明确指令（而非被动警告），将通过率从 66.7% 提升到 100%。关键洞察：描述的质量决定了 skill 的触发可靠性，而清晰的指令比信息更重要。

## 关键信息抽取

| 项目 | 内容 |
|------|------|
| **来源** | [philschmid.de](https://www.philschmid.de/testing-skills) |
| **作者** | Philip Schmid (Hugging Face) |
| **主题** | Agent Skills 测试与评估 |
| **核心案例** | Gemini Interactions API skill |
| **收录时间** | 2026-03-09 22:35 |

### Skill 的两种类型

| 类型 | 说明 | 测试重点 |
|------|------|---------|
| **Capability skills** | 帮助 agent 做基础模型做不了的事 | 随模型进步可能过时，evals 告诉你何时退休 |
| **Preference skills** | 记录特定工作流程 | 验证与实际工作流的保真度 |

### 成功的三个维度

1. **Outcome**: 产出是否可用？（代码编译、图片渲染、文档创建）
2. **Style & Instructions**: 是否遵循约定？（正确 SDK、模型 ID、命名规范）
3. **Efficiency**: 时间/ token/ 努力是否合理？（无冗余重试、合理 token 数）

### 评估框架四步法

1. **Create prompt set**: 10-20 个测试用例，覆盖核心能力、边界情况、负例
2. **Run agent & capture output**: 通过 CLI 运行，捕获输出
3. **Write deterministic checks**: 用 regex 检查代码（正确 SDK、当前模型等）
4. **Add LLM-as-judge**: 对质量类检查（设计风格、命名规范）使用 LLM 评分

### 关键优化

| 优化 | 效果 |
|------|------|
| 重写 skill 描述（匹配用户意图） | 修复 5/7 失败 |
| 替换被动警告为明确指令 | 剩余失败修复 |
| **总计** | 66.7% → 100% |

## 通过写作消化

原文核心论点：
1. Skills 需要像代码一样被测试，但目前几乎没人做
2. 评估应该关注结果而非路径（agent 可能找到意想不到的解决方案）
3. Skill 描述是最关键的触发机制，模糊的描述会导致不可靠的触发
4. 指令优于信息——明确指令比被动推荐更有效

写作问题：
- [ ] 我们的 skills（second-brain, daily-brief, self-evolution）目前有多少测试覆盖？
- [ ] 如果要给 daily-brief 写 evals，成功标准应该是什么？
- [ ] "描述决定触发可靠性"——我们的 skill 描述是否需要重写？
- [ ] 什么情况下我们应该"退休"一个 skill？

建议的写作方向：
- **应用**：为现有 skills 设计评估框架
- **质疑**：轻量级 evals 是否足够？什么时候需要更重的测试？
- **延伸**：技能版本管理——如何处理 skill 的迭代和回滚？

## 信息增量

| 概念 | 本资料 | 当前认知 |
|------|--------|----------|
| Skill testing | 系统化方法（prompt set + checks + LLM judge） | 零散了解 |
| 成功维度 | Outcome + Style + Efficiency 三维 | 只关注功能 |
| Skill 退休 | 定期用无 skill 模式测试，看模型是否已吸收 | 未考虑 |
| 描述优化 | 匹配用户意图而非 API 术语 | 技术导向 |

## 待办事项

- [ ] 阅读相关资源（SkillsBench、Claude 的 agent evals 文章）
- [ ] 为现有 skills 设计 minimal evals
- [ ] 优化 skill 描述（特别是触发可靠性）

## 我的批注

学习 skills —— 这篇文章来得正好，我们刚沉淀了 self-evolution skill。Philip Schmid 的方法论可以直接应用到我们的技能测试中。特别是"描述决定触发"这个点，值得重新审视我们的 SKILL.md。

---

*原文链接：[philschmid.de/testing-skills](https://www.philschmid.de/testing-skills)*
