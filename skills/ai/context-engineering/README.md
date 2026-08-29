# Context Engineering（上下文工程）— 概览

> ⚠️ Not Yet Verified — 本概念尚未在生产中实际验证。

Context Engineering（上下文工程）= 决定 AI 当前这一步该看到哪些信息（选 / 压 / 排 / 丢），把有限上下文窗口用在刀刃上。

## 一句话价值

替 AI 做"该留哪几条、该丢哪几条"的取舍，让有限窗口聚焦关键信息，提升输出质量、控制成本。

## 关键点

- 四个动作：筛选（选）→ 压缩（压）→ 排序（排）→ 丢弃（丢）。
- 先定 token 预算，再倒推能塞多少输入。
- 常见坑：整个代码库都塞、不区分新旧、忽略预算、只塞不排。

## 去哪里看

- 完整说明：[SKILL.md](SKILL.md)
- 配套提示词：[`prompts/ai-app/build-context.md`](../../../prompts/ai-app/build-context.md)
- 相关技能：[RAG](../rag/SKILL.md) · [记忆](../memory/SKILL.md)

## 验证状态

`status: experimental` / `verified: false` / `last_verified: null` — 暂未在生产中实际验证，按概念介绍使用。
