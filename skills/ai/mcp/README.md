# MCP（模型上下文协议）— 概览

> ⚠️ Not Yet Verified — 本概念尚未在生产中实际验证。

MCP（Model Context Protocol，模型上下文协议）= 给 AI 接工具 / 数据 / 资源的标准协议，像"AI 的 USB"，让不同工具能被不同模型通用接入。

## 一句话价值

把"工具 / 资源 / Prompt"标准化暴露，让一份实现服务多端，告别 M×N 适配地狱、实现工具与模型解耦。

## 关键点

- 两端：MCP Host（客户端）↔ MCP Server（暴露 tools / resources / prompts）。
- 标准约定：发现、描述、调用、回传。
- 常见坑：不安全操作直接暴露、粒度过细或过粗、不版本化、权限不收敛、暴露敏感资源。

## 去哪里看

- 完整说明：[SKILL.md](SKILL.md)
- 配套提示词：[`prompts/ai-app/build-mcp-tool.md`](../../../prompts/ai-app/build-mcp-tool.md)
- 相关技能：[工具调用](../tool-calling/SKILL.md) · [Agent](../agent/SKILL.md)

## 验证状态

`status: experimental` / `verified: false` / `last_verified: null` — 暂未在生产中实际验证，按概念介绍使用。
