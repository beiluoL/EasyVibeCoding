# 构建 MCP 工具（build-mcp-tool）

## Use When（何时使用）

> 想用 MCP 协议（让模型调用外部工具的标准协议）给 AI 暴露一个工具，让它能执行真实操作（查数据、发请求）。

## Goal（目标）

> 基于 MCP 协议封装一个可被模型调用的工具：给出工具定义、参数 schema、安全边界。

## Input Variables（输入变量）

- `{{tool_purpose}}`：工具要做什么（如：查询订单状态）。
- `{{tool_inputs}}`：工具需要的输入参数及含义。
- `{{tool_side_effects}}`：是否写操作、影响范围、可逆性。

## Prompt（提示词正文）

```
Role: 你是一名负责的 MCP 工具封装者，清楚"工具就是给 AI 的手"，手伸错地方就出事。
Context: 工具用途：{{tool_purpose}}
输入参数：{{tool_inputs}}
副作用：{{tool_side_effects}}
Goal: 给出符合 MCP 协议的工具定义：工具描述、参数 schema、安全边界。
Constraints:
- 给出 MCP 工具定义（name、description、inputSchema），描述要让模型能判断"何时该用这个工具"。
- 参数 schema 要严格：必填项、类型、枚举、范围；模糊输入要约束。
- 安全边界必须明确：读操作可放开、写操作需确认、破坏性操作需二次确认或拒绝。
- 工具描述要写清"不能做什么"，避免模型误用（如：本工具只读，不可修改）。
- 给出错误返回规范：失败时返回结构化错误而非崩溃，让模型能据此重试或放弃。
- 未在生产验证，标注 ⚠️ Not Yet Verified，列出需验证项（权限、并发、超时）。
- 不编造工具调用成功率数字。
Workflow:
1. 写工具 name 与 description（含能力边界）。
2. 写 inputSchema（必填/类型/约束）。
3. 写安全边界（auto/confirm/deny）。
4. 写错误返回规范。
5. 给最小实现骨架。
Output format:
## 工具定义（name/description）
## inputSchema
## 安全边界
## 错误返回规范
## 最小实现骨架
## ⚠️ 未在生产验证的事项
Verification: 回顾描述是否含能力边界、schema 是否严格、写操作是否需确认、错误是否结构化返回、是否诚实标注未验证。
```

## Expected Behavior（期望行为）

> 模型给出严格 schema 与安全边界的 MCP 工具定义，写操作需确认，错误结构化返回，诚实标注未验证。

## Expected Output（期望输出）

```
## 工具定义
name: get_order_status
description: 查询订单状态（只读，不可修改）
## inputSchema
{ order_id: string, required }
## 安全边界
读操作 auto；本工具不支持写
## 错误返回
{ error: "order_not_found", message: "..." }
## ⚠️ 未在生产验证
权限校验、并发、超时均未实测
```

## Validation（验证）

- 工具描述含能力边界（能做什么/不能做什么）。
- 参数 schema 有必填与类型约束。
- 写操作需确认，错误结构化返回。

## Common Mistakes（常见错误）

- 工具描述只写"能做什么"不写"不能做什么"，模型误拿只读工具去做写操作。
- 参数 schema 不严格，模型传模糊或越界值导致工具出错。
- 写操作不设确认，AI 一句调用就把数据删了。
- 失败时直接抛异常不返回结构化错误，模型无法据此重试。

## Related Skills（相关技能）

- [`../../skills/ai/mcp/SKILL.md`](../../skills/ai/mcp/SKILL.md)
- [`../../skills/ai/tool-calling/SKILL.md`](../../skills/ai/tool-calling/SKILL.md)

## Related Workflows（相关流程）

- 暂无直接对应流程
