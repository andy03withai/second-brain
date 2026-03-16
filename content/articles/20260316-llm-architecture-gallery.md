---
title: "LLM Architecture Gallery：主流大模型架构一图对比"
date: 2026-03-16
tags: [llm, architecture, deep-learning, visualization]
source: "https://sebastianraschka.com/llm-architecture-gallery/"
annotation: "模型架构大赏"
---

# LLM Architecture Gallery

> Sebastian Raschka 整理的 LLM 架构图谱，以可视化卡片形式对比主流大模型的关键架构决策。

## 核心内容

这个页面收集了 Sebastian Raschka 两篇深度文章中的架构图和参数表：
- [The Big LLM Architecture Comparison](https://magazine.sebastianraschka.com/p/the-big-llm-architecture-comparison)
- [A Dream of Spring for Open-Weight LLMs](https://magazine.sebastianraschka.com/p/a-dream-of-spring-for-open-weight)

### 涵盖模型

| 模型 | 参数量 | 架构类型 | 注意力机制 | 关键特点 |
|------|--------|----------|-----------|----------|
| **Llama 3** | 8B | Dense Decoder | GQA + RoPE | Pre-norm 基线，比同规模 OLMo 2 更宽 |
| **OLMo 2** | 7B | Dense Decoder | MHA + QK-Norm | 残差内 Post-norm，非常规 Pre-norm 布局 |
| **DeepSeek V3** | 671B (37B active) | Sparse MoE | MLA | Dense prefix + 共享专家，保持大模型推理效率 |
| **DeepSeek R1** | 671B (37B active) | Sparse MoE | MLA | 基于 V3 架构，主要改变是推理导向的训练配方 |
| **Gemma 3** | 27B | Dense Decoder | GQA + QK-Norm + 5:1 滑动窗口/全局注意力 | 27B 甜点规模，大型多语言词表 |
| **Mistral Small 3.1** | 24B | Dense Decoder | Standard GQA | 延迟优化设计，KV Cache 更小，层数更少 |
| **Llama 4** | 400B (17B active) | Sparse MoE | GQA | 交替 Dense/MoE 块，比 DeepSeek V3 更少更大的专家 |
| **Qwen3 235B** | 235B (22B active) | Sparse MoE | GQA + QK-Norm | 无共享专家的高容量 MoE，优化服务效率 |
| **Qwen3 32B** | 32B | Dense Decoder | GQA + QK-Norm | OLMo 3 32B 的对照基准 |
| **Qwen3 4B** | 4B | Dense Decoder | GQA + QK-Norm | 紧凑型，151k 词表 |

### 架构趋势观察

1. **MoE 成为大模型标配** - DeepSeek V3/R1、Llama 4、Qwen3 大版本均采用 Sparse MoE
2. **QK-Norm 逐渐普及** - 从 OLMo 2 开始，Gemma 3、Qwen3 系列均引入 QK-Norm 稳定训练
3. **注意力机制分化** - MLA (DeepSeek) vs GQA (Meta/Qwen) 两条路线
4. **滑动窗口注意力** - Gemma 3 的 5:1 局部/全局注意力比例是一个有趣的工程权衡

## 用户批注

模型架构大赏

---

*收录时间: 2026-03-16*  
*来源: Sebastian Raschka's LLM Architecture Gallery*
