---
title: "Agent 的 Harness 工程：从上下文调优到工业级治理架构"
date: 2026-04-13T10:00:00+08:00
draft: false
---

# Agent 的 Harness 工程

> 模型不是产品，围绕它的基础设施才是。

2026 年初，AI 圈出现一个明显的新风向：**Harness Engineering**。Anthropic 和 OpenAI 几乎在同一时期发布了各自的方法论总结，LangChain、Stripe、Braintrust 等公司也相继跟进。这个词正在快速取代过时的 "Prompt Engineering"，成为衡量一个团队 Agent 工程能力的核心指标。

## 一、什么是 Harness

**Harness（挽具/支架）** 指的是包裹在 LLM 调用之外的所有基础设施层。它把单次、无状态的文本预测，转化为能够执行长周期、多步骤复杂任务的 Agent 系统。

用 Anthropic 的话说：

> "一个 agent 在复杂任务进行到第 20 分钟时失控，这不是模型问题，而是基础设施问题。模型正在准确执行它被要求做的事——只是它没有被放在正确的环境里。"

Harness 包含但不限于：

- **上下文管理**：如何分配、重置、传递长对话中的状态
- **工具编排**：Agent 能调用什么、以什么格式调用、失败时如何重试
- **反馈回路**：测试、编译、运行结果如何返回给 Agent 作为学习信号
- **评估与验证**：谁来评判 Agent 的输出，评判标准是什么
- **交接机制**：跨会话、跨 Agent 实例的状态外部化（Artifacts）

简言之，**Harness 是模型与真实世界之间的翻译层和缓冲带**。

## 二、为什么 Harness 成为新的竞争壁垒

### 1. 模型能力在趋同，Harness 成为差异化来源

随着 Claude 4.5、GPT-5-2、Gemini 3 等模型的能力差距逐渐缩小，"换模型就能显著提升"的边际效应在递减。真正拉开差距的是：同样的模型，在不同 Harness 下表现天差地别。

LangChain 的一个经典实验可以说明这一点：在 TerminalBench 2.0 上，他们**只改了基础设施，没有换模型**，排名从 30 名开外直接冲到第 5。Harness 本身就是性能杠杆。

### 2. Harness 与模型已经深度耦合

OpenAI 的 Codex 和 Anthropic 的 Claude Code 都已经证明：模型是在特定 Harness 的 scaffolding 中训练出来的。粗暴地剥离或替换 Harness，性能反而会断崖式下跌。这催生了一个新的工程共识——**Harness 应该被设计成"可逐步拆除的脚手架"**，但拆除的时机和节奏必须与模型进化同步。

### 3. 长任务中的两大"死亡模式"

Anthropic 在长期任务研究中识别出两种典型的 Agent 失效模式：

**上下文焦虑（Context Anxiety）**：当模型感知到上下文窗口即将耗尽时，行为会退化——走捷径、提前收尾、用"以下留给用户完成"来搪塞。这并非 bug，而是训练数据中"结尾处收敛"模式的过度泛化。

**自我评估偏差（Self-evaluation Bias）**：让模型评审自己的工作，它几乎总是给出正面反馈。这不是"谦虚"问题，而是确认偏见的训练痕迹。在 UI 设计等主观任务中，这种偏差尤为致命。

这两种模式都无法通过"更好的 prompt"解决，必须通过 Harness 架构层面的干预才能缓解。

## 三、大厂 Harness 方法论对比

### Anthropic：薄 Harness + 三 Agent 分离

Anthropic 的核心理念是**"dumb loop"**——让 Harness 尽量薄，把推理负担交给模型本身。但他们的关键创新在于**角色分离**：

- **Planner（规划者）**：把简短需求扩展为完整规格
- **Generator（生成者）**：迭代实现功能
- **Evaluator（评估者）**：使用 Playwright MCP 进行交互式验证，对照规格逐项检查

这种设计的灵感来自 GAN（生成对抗网络）。**Evaluator 被专门调优为怀疑论者**，其核心洞察是："让独立的评估者保持批判性，比让生成者自我批判要容易得多。"

Anthropic 的内部对比实验极具说服力：

| 配置 | 时间 | 成本 | 结果 |
|------|------|------|------|
| Solo Agent | 20 分钟 | $9 | UI 能显示，但游戏模式损坏，无错误提示 |
| 完整 Harness | 6 小时 | $200 | 可运行的完整应用，含精灵编辑器、关卡编辑器、可玩游戏 |

### OpenAI：厚文档 + 确定性约束门控

OpenAI 的路径更工程化。他们的标志性实验是：3 个工程师、几个月内交付 100 万行代码，其中几乎没有手写的代码，全部来自 Agent 生成。

核心洞察：**"Agent 只能处理它能读取的东西"**。任何存在于 Slack 线程、Google Doc 或某人脑中的信息，对 Agent 来说都是不可见的。

OpenAI 的解决方案是：

- **AGENTS.md 作为目录**：一个 100 行左右的简短文件，充当整个代码库的"目录页"，指向更详细的文档
- **架构 Linter**：不请求 Agent 遵守规则，而是通过工程手段强制执行。例如禁止 UI 层直接调用数据库
- **Pre-commit Hooks**：Agent 生成的任何内容都必须先通过静态类型检查、死代码检测和 Shell 脚本校验
- **CI + LLM Audit Agent 双层验证**：CI 负责确定性检查，LLM Audit Agent 负责捕捉 linter 无法检测的设计违规

### LangChain： thick harness 与可审计性

LangChain 代表的则是**厚 Harness** 路线，通过 LangGraph 等工具把大量逻辑和状态管理固化在基础设施层。这种模式更适合复杂、确定性的工作流，以及需要强审计追踪的企业场景。

其代价是灵活性降低、与模型的耦合更深。LangChain 也承认，未来的理想状态是**"Build to Remove"**——像建筑脚手架一样，随着模型能力提升逐步拆除 Harness 的复杂度。

## 四、Harness 的核心组件

综合 Anthropic、OpenAI、Stripe 和 LangChain 的实践，可以提炼出工业级 Harness 的六大核心组件：

### 1. 确定性约束门控（Deterministic Guardrails）

这是 Harness Engineering 与传统 AI 应用的根本区别。不是"请 Agent 遵守规则"，而是"让规则不可违背"。

- **架构 Linter**：检测代码变更是否违反预定义的依赖规则
- **重试上限（Retry Caps）**：Stripe 的经验表明，两次重试是编译错误修复的成本-收益临界点
- **前置提交钩子**：死代码检测、类型检查、脚本校验

### 2. 反馈循环与自我验证

Agent 的进化依赖于"执行错误"作为学习信号。

- **Write-Test-Fix Cycle**：在沙盒中自动运行测试，失败时将堆栈跟踪信息喂回 Agent
- **Pre-completion Checklist**：独立的审计 Agent 在任务完成前逐项核对需求。LangChain 的实验表明，这一机制能提升 13.7% 的基准测试分数

### 3. 上下文治理与 Gardening

大规模代码库中，上下文污染是 Agent 失效的主因。

- **上下文重置（Context Reset）优于压缩**：与其让模型总结历史，不如清空窗口，把关键状态以外部化 Artifact 的形式传递给新的 Agent 实例
- **结构化交接**：progress 文件、docs 目录、TODO.md 等外部化状态成为"记忆替代"

### 4. 生成与评估分离

核心原则：**写代码的 Agent 不应该评判自己的代码**。

- Anthropic：GAN 式三 Agent 分离
- OpenAI：CI/Lint 独立验证 + LLM Audit Agent 语义评估
- 共同结论：评估必须是外部的、自动的、快速的

### 5. 工具接口标准化

随着 MCP（Model Context Protocol）和 A2A（Agent-to-Agent）等协议的出现，Harness 正在从"每个团队各自为政"走向标准化。

统一协议的好处是：任何符合标准的 Agent 都可以接入任何评估 Harness，无需为每个 benchmark 写定制适配器。

### 6. 评估 Harness 的可观测性

完整的 Agent 评估需要记录：

- **Transcript/Trace**：完整的执行轨迹，包括所有 tool calls、参数、返回结果
- **Outcome**：环境最终状态（而不是 Agent 说了什么）
- **Grader**：多维度评分逻辑，支持 deterministic checks 和 LLM-as-judge 的混合

## 五、评估生态：Benchmark 与 Harness 的共生

评估 Agent 时，我们实际上在评估 **"模型 + Harness" 的联合表现**。这催生了一个庞大的 evaluation harness 生态。

### 主流 Benchmark

| Benchmark | 领域 | 特点 |
|-----------|------|------|
| **SWE-bench** | 软件工程 | 真实 GitHub issue 修复，执行级验证 |
| **WebArena** | 网页自动化 | 812 个长周期网页任务，自托管环境 |
| **AgentBench** | 通用能力 | 跨 8 种环境（OS、数据库、游戏等） |
| **GAIA** | 真实助理任务 | 466 个人工设计问题，测试推理和工具使用 |
| **Terminal-Bench** | 终端长任务 | 验证密集型的终端原生任务 |
| **IDE-Bench** | IDE Agent | 模拟 Cursor/Windsurf 的结构化工具生态 |

### 开源 Evaluation Harness 工具

- **lm-evaluation-harness**：EleutherAI 的 LLM 统一评估框架
- **Harbor**：Tessl 推出的容器化 Agent 评估标准
- **kbench**：支持 SWE-bench、Terminal-Bench、SAE 的统一 CLI
- **OpenHands Benchmarks**：为 OpenHands 系统定义的评估 harness

### Harness 对 Benchmark 分数的影响

在 SWE-bench 上，使用相同模型但不同 Harness 的实现， solve rate 可以相差 20% 以上。这说明：**benchmark 排名的提升，可能来自 Harness 优化而非模型进步**。这是当前评估领域最受关注的议题之一。

## 六、工程实践建议

如果你正在构建或优化一个 Agent 系统，以下建议来自一线的共识：

### 不要让 Agent 评估自己的输出

```
# 不好
"你刚才写的这段代码有没有问题？"

# 好
"你是一位严苛的 code reviewer。请从以下维度评估：
1. 竞态条件
2. 错误处理完整性
3. N+1 查询问题
4. 安全漏洞（SQL 注入、XSS）
每个维度给出 1-5 分，并列出具体行号。"
```

### 用工具验证，不用模型"感觉"验证

能运行的测试 > 模型的文字确认。在 Claude Code / Cursor 中，明确要求：

```
"实现完成后，请：
1. 运行 `npm test`
2. 如果有失败用例，先修复再汇报
3. 最后给我测试通过的输出截图
不要只告诉我'已完成'。"
```

### 控制每次任务的范围

- 每次只做一件事（feature-by-feature）
- 使用 depth-first 而非 breadth-first 的执行策略
- 通过 TODO.md 等 Artifact 维护状态

### 构建渐进式移除的脚手架

假设你当前的 Harness 复杂度为 N。每当你升级模型时，问自己："新模型是否已经内化了这部分逻辑？"如果是，就尝试将其从 Harness 中移除。

## 七、未来展望

Harness Engineering 的演进方向已经比较清晰：

1. **协议标准化**：MCP、A2A 等协议将降低 Harness 的碎片化程度
2. **评估即训练**：RLVR（Reinforcement Learning from Verifiable Rewards）让 benchmark 本身成为训练信号
3. **Self-Evolving Harness**：像 VeRO 这样的框架正在探索让 Agent 自动优化其他 Agent 的 Harness
4. **安全与治理**：Stub Model、Red Team Eval 等测试方法正在成为企业部署的标配

最终，Harness Engineering 的目标不是让 Agent 依赖更多的脚手架，而是**在模型能力提升的同时，不断简化基础设施，让智能本身成为系统的主干**。

---

## 参考来源

- Anthropic: *Demystifying Evals for AI Agents* / *Harness Design* 系列
- OpenAI: Codex 工程实践博客
- LangChain: *The Anatomy of an Agent Harness*
- Tessl: *How to Evaluate AI Agents: An Introduction to Harbor*
- Braintrust: *AI Agent Evaluation: A Practical Framework*
- Berkeley RDI: *How We Broke Top AI Agent Benchmarks*
- arXiv: VeRO, IDE-Bench, AIRTBench, ProdCodeBench 等论文
