# Tool Calling（工具调用）— 概览

> ⚠️ Not Yet Verified — 本概念尚未在生产中实际验证。

Tool Calling（工具调用）= 让 AI 按约定格式输出"我要调用某工具 + 参数"，由外部真正执行（查数据库 / 调 API / 读写文件）再把结果回给 AI。

## 一句话价值

给 AI 配"手"：它填调用单、外部执行器干活、结果回传，让模型能触达实时数据与真实副作用，且全程可校验可限权。

## 关键点

- 一次往返：LLM 输出 tool_call → 执行器校验运行 → 结果回传 → LLM 继续。
- 工具三件套：名称 + 一句话描述 + 参数 schema。
- 常见坑：描述不清、不校验参数、危险操作无确认、结果不结构化、粒度不当。

## 去哪里看

- 完整说明：[SKILL.md](SKILL.md)
- 配套提示词：[`prompts/ai-app/build-mcp-tool.md`](../../../prompts/ai-app/build-mcp-tool.md)
- 相关技能：[Agent](../agent/SKILL.md)

## 验证状态

`status: experimental` / `verified: false` / `last_verified: null` — 暂未在生产中实际验证，按概念介绍使用。
