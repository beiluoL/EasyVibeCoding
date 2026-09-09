---
name: 03-architecture
use_when: 设计项目的技术架构
goal: 确定模块划分、数据流、关键技术决策
related_skill: skills/core/architecture-design
status: experimental
verified: false
---

# Prompt 03 — 架构设计

> 链接到 Skill：[architecture-design](../../../../skills/core/architecture-design/SKILL.md)

## Prompt

```
我要做一个 AI 聊天应用。

请帮我设计架构：
1. 画一个简单的模块关系图
2. 说明数据怎么流转（用户发消息到看到回复的完整路径）
3. 解释每个关键技术决策的理由（为什么前后端分离？为什么后端调 LLM？）
4. 列出风险和应对

不要过度设计。只要最小可行架构。
```

## Expected Output

- 模块关系图
- 数据流说明
- 关键决策表（决策 + 理由）
- 风险与应对表

## Common Mistakes

- ❌ 过度设计（新手项目加微服务、消息队列）
- ❌ 只画图不解释为什么
