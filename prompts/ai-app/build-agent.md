# 构建 Agent（build-agent）

## Use When（何时使用）

> 想搭一个能"自己拆任务、调工具、看结果再决定下一步"的 AI Agent，而不是单轮问答。

## Goal（目标）

> 设计一个最小可运行的 Agent 循环：目标 → 拆解 → 工具调用 → 观察 → 再规划，并重点设定终止条件与工具权限边界。

## Input Variables（输入变量）

- `{{agent_goal}}`：Agent 要完成的目标（如：查询订单状态并通知用户）。
- `{{available_tools}}`：可用工具清单及各自能力（如：查订单、发消息）。
- `{{safety_constraints}}`：安全约束（哪些操作需人工确认、最大步数、最大花费）。

## Prompt（提示词正文）

```
Role: 你是一名务实负责的 Agent 设计者，清楚"Agent 失控"比"Agent 不动"更危险。
Context: 目标：{{agent_goal}}
可用工具：{{available_tools}}
安全约束：{{safety_constraints}}
Goal: 给出最小可运行的 Agent 循环设计，重点处理终止条件与工具权限控制。
Constraints:
- 必须画出循环：目标 → 拆解步骤 → 选工具调用 → 观察返回 → 再规划 → 直到完成或终止。
- 终止条件必须明确，至少包含：达成目标、达到最大步数、连续失败 N 次、超出花费上限、命中需人工确认的操作。
- 工具权限控制必须明确：哪些工具可自动调用、哪些必须人工确认、哪些禁止调用；写操作默认需确认。
- 每轮必须保留"为什么选这个工具"的依据，便于事后审计。
- 给出最小伪代码或流程，可落地。
- 未在生产验证，标注 ⚠️ Not Yet Verified，并列出上线前需验证项（失控场景、成本上限、并发安全）。
- 不编造成功率等数字。
Workflow:
1. 把 {{agent_goal}} 拆成可执行子步骤。
2. 定义每个工具的入参 schema 与权限等级（auto / confirm / deny）。
3. 设定终止条件清单。
4. 给出主循环伪代码（含观察 → 再规划 → 终止判断）。
5. 列出失控场景与兜底。
Output format:
## 工具与权限表
| 工具 | 能力 | 权限等级 |
## 终止条件
## 主循环伪代码
## 失控兜底
## ⚠️ 未在生产验证的事项
Verification: 回顾是否每工具有权限等级、终止条件是否含最大步数与失败兜底、写操作是否默认需确认、是否诚实标注未验证。
```

## Expected Behavior（期望行为）

> 模型给出带终止条件与权限分级的 Agent 循环，写操作默认需确认，并诚实标注未验证事项。

## Expected Output（期望输出）

```
## 工具与权限表
| 查订单 | 读订单状态 | auto |
| 发消息 | 通知用户 | confirm |
| 删除订单 | 删数据 | deny |
## 终止条件
达成目标 / 步数>10 / 连续失败3次 / 花费>阈值 / 命中confirm未确认
## 主循环伪代码
for step in 1..MAX: 拆解→选工具→(若confirm则等人工)→调用→观察→再规划→判断终止
## ⚠️ 未在生产验证
循环死锁、并发竞态、成本失控均未实测
```

## Validation（验证）

- 每个工具有明确权限等级（auto/confirm/deny）。
- 终止条件包含最大步数与失败兜底。
- 写操作默认需人工确认。

## Common Mistakes（常见错误）

- 只设计"happy path"不给终止条件，Agent 陷入死循环或无限花钱。
- 所有工具都设成 auto 自动调用，写操作（删除/发消息）失控。
- 不留"为什么调这个工具"的依据，出错无法审计。
- 编造"99% 成功率"等未测数字。

## Related Skills（相关技能）

- [`../../skills/ai/agent/SKILL.md`](../../skills/ai/agent/SKILL.md)
- [`../../skills/ai/tool-calling/SKILL.md`](../../skills/ai/tool-calling/SKILL.md)
- [`../../skills/ai/memory/SKILL.md`](../../skills/ai/memory/SKILL.md)

## Related Workflows（相关流程）

- 暂无直接对应流程（可参考 `workflows/feature-development/` 的迭代环节）
