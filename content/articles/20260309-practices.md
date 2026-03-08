---
title: "Agent Skills 最佳实践"
date: 2026-03-09
source: "https://github.com/mgechev/skills-best-practices"
tags: [skills, ai-agent, best-practices, codex]
---

## 核心摘要

Mgechev 编写的 Agent Skills 创建指南，涵盖如何编写专业级技能、使用 LLM 验证、保持上下文窗口精简。与 Claude 的 Agents & Tools 文档互补。

## 关键信息抽取

### 技能结构
```
skill-name/
├── SKILL.md      # 必需：元数据 + 核心指令 (<500行)
├── scripts/      # 可执行代码 (Python/Bash)
├── references/   # 补充上下文
└── assets/       # 模板或静态文件
```

### Frontmatter 优化
- **name**: 1-64字符，小写+数字+连字符，与目录名一致
- **description**: 最多1024字符，第三人称，包含"负面触发"
  - ❌ 差: "React skills." (太模糊)
  - ✅ 好: "Creates React components using Tailwind. Don't use for Vue/Svelte."

### 渐进式披露原则
- SKILL.md 保持精简 (<500行)
- 细节放到 references/，通过相对路径引用
- 不使用: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md

### 写作风格
- 使用步骤编号，严格时序
- 提供具体模板，利用 LLM 的模式匹配
- 第三人称祈使句: "Extract the text..." 而非 "You should..."

### 脚本化重复操作
- 复杂解析逻辑用 Python/Bash 脚本
- 脚本返回描述性错误信息，便于 Agent 自纠正

## 信息增量

| 概念 | 本资料 | 之前的认知 |
|------|--------|-----------|
| 技能验证 | 提供完整的 LLM 验证流程（发现/逻辑/边界/架构） | 未系统化处理 |
| 描述优化 | 明确需要"负面触发" | 只关注正面描述 |
| 文件组织 | 明确禁止 README/CHANGELOG | 无明确限制 |

## 待探索问题

- [ ] 如何为 OpenClaw 的 skills 编写 eval 测试？
- [ ] skill-eval 框架是否适用？

## 我的批注

如何使用 skills — 这篇文章正好回答了我搭建第二大脑时技能设计的问题。特别是渐进式披露和验证流程部分，可以应用到后续的技能优化。

---

*原文链接：[github.com/mgechev/skills-best-practices](https://github.com/mgechev/skills-best-practices)*
