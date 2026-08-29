# RAG（检索增强生成）— 概览

> ⚠️ Not Yet Verified — 本概念尚未在生产中实际验证。

RAG（Retrieval-Augmented Generation，检索增强生成）= 先从你的文档里检索相关片段，再把它塞进 AI 的提问里，让 AI 基于你的资料回答，而不是凭空编。

## 一句话价值

让 AI 的回答"有据可依、可更新、可引用"，减少幻觉、覆盖私有 / 最新知识。

## 关键点

- 先检索后生成：文档 → 切块 → 向量化 → 向量库 → 检索 Top-K → 拼 Prompt → LLM 回答。
- 切块大小、是否重排、是否引用来源是成败关键。
- 常见坑：块太大太小、不重排、塞太多超上下文、不引用来源。

## 去哪里看

- 完整说明：[SKILL.md](SKILL.md)
- 配套提示词：[`prompts/ai-app/build-rag.md`](../../../prompts/ai-app/build-rag.md)
- 相关技能：[上下文工程](../context-engineering/SKILL.md)

## 验证状态

`status: experimental` / `verified: false` / `last_verified: null` — 暂未在生产中实际验证，按概念介绍使用。
