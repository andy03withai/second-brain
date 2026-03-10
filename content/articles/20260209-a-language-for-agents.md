---
title: "A Language for Agents"
author: "Armin Ronacher"
date: 2026-02-09
source: "https://lucumr.pocoo.org/2026/2/9/a-language-for-agents/"
tags: [AI, agents, programming-language, code-review]
status: 想读
---

# A Language for Agents

**作者**: Armin Ronacher  
**日期**: 2026-02-09  
**来源**: [lucumr.pocoo.org](https://lucumr.pocoo.org/2026/2/9/a-language-for-agents/)

## 核心观点

> "为什么我们需要为 AI Agent 设计新的编程语言？"

作者认为，随着 Agentic Engineering 的兴起，我们将看到更多新编程语言的出现，因为：

1. **代码成本下降** - AI 让编写代码的成本大幅降低，生态系统的广度变得不那么重要
2. **新语言可以成功** - 如果价值主张足够强，人们会采用新语言，即使它们在模型权重中代表性不足
3. **理解代码变得更重要** - 因为产生更多代码，理解代码做什么变得比节省打字更重要

## Agent 想要什么

### ✅ 有利于 Agent 的语言特性

- **无需 LSP 的上下文** - 统一的有/无 LSP 的工作方式
- **显式括号** - 而非基于缩进的语法（Python 的空白缩进对 LLM 不友好）
- **流式上下文但显式** - 效果标记通过代码格式化步骤自动传播
- **结果而非异常** - Agent 对异常处理有困难
- **最小差异** - 减少重构时的行变化
- **可 grep** - 代码易于搜索（如 Go 的包前缀）
- **本地推理** - Agent 喜欢局部推理，常只加载少数文件

### ❌ Agent 讨厌的特性

- **宏** - Agent 经常 struggle with 宏
- **重导出和 barrel 文件** - 难以追踪符号来源
- **别名** - 导入别名让 Agent 困惑
- **不稳定测试** - Agent 特别擅长创建不稳定测试
- **多种失败条件** - TypeScript 可以运行但类型检查失败，会误导 Agent

## 新语言的设计原则

```
fn issue(sub: UserId, scopes: []Scope) -> Token
    needs { time, rng }
{
    return Token{
        sub,
        exp: time.now().add(24h),
        scopes,
    }
}
```

**关键设计**:
- `needs` 声明效果依赖
- 测试时可以精确 mock
- 格式化工具自动传播注解

## 我的批注

（用户提问：为什么要给 agent 发明一门语言？）

这篇文章系统性地回答了这个问题。核心逻辑是：AI 改变了编程的成本结构，使得我们重新思考语言设计的权衡。

---

*收录于 2026-03-10*
