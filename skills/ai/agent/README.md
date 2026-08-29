# Agent（智能体）— 概览

> ⚠️ Not Yet Verified — 本概念尚未在生产中实际验证。

Agent（智能体）= 让 AI 自主"规划 + 调用工具 + 多步执行"完成一个任务，而不是一问一答。

## 一句话价值

把"给一句答一句"升级为"给个目标、自己干完"，让 AI 处理多步、需中间决策的复杂任务。

## 关键点

- 核心循环：目标 → 拆解 → 选工具 → 执行 → 观察结果 → 再规划 → 完成。
- 必须有终止条件、步数 / token 上限、危险操作二次确认。
- 常见坑：死循环、权限过大、不记中间状态、一次给太多目标。

## 去哪里看

- 完整说明：[SKILL.md](SKILL.md)
- 配套提示词：[`prompts/ai-app/build-agent.md`](../../../prompts/ai-app/build-agent.md)
- 相关技能：[工具调用](../tool-calling/SKILL.md) · [记忆](../memory/SKILL.md)

## 验证状态

`status: experimental` / `verified: false` / `last_verified: null` — 暂未在生产中实际验证，按概念介绍使用。
