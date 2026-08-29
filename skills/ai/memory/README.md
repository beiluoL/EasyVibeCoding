# Memory（记忆）— 概览

> ⚠️ Not Yet Verified — 本概念尚未在生产中实际验证。

Memory（记忆）= 让 AI 跨会话 / 跨步骤记住关键信息（用户偏好 / 项目决策 / 已做过的），避免每次重复说明。

## 一句话价值

给 AI 配一本"会自动翻的项目笔记本"，让它在跨会话与多步任务中保持上下文、越用越懂你。

## 关键点

- 三层：短期（当前对话）+ 长期（向量 / 结构化）+ 检索注入。
- 配套机制：写入判定、检索、更新 / 清理。
- 常见坑：什么都记、不更新过期、记敏感信息、只存不索引。

## 去哪里看

- 完整说明：[SKILL.md](SKILL.md)
- 配套提示词：[`prompts/ai-app/build-memory.md`](../../../prompts/ai-app/build-memory.md)
- 相关技能：[上下文工程](../context-engineering/SKILL.md)

## 验证状态

`status: experimental` / `verified: false` / `last_verified: null` — 暂未在生产中实际验证，按概念介绍使用。
