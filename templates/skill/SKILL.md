---
name:             # skill id, kebab-case
description:      # one-line what it does
version: 0.1.0
category:         # core | ai
difficulty:       # beginner | intermediate | advanced
status:           # experimental | stable | deprecated
verified: false   # MUST be false unless truly runtime-verified
compatible: [unspecified]   # list; use [unspecified] until tested
prerequisites: []
inputs: []
outputs: []
triggers: []
validation:       # how to validate this skill works
last_verified: null   # MUST stay null when verified:false
---

# {{Skill Name（技能名称）}}

## Purpose（目的）

> 一段话：这个技能解决什么问题、为什么存在。

## When to Use（何时使用）

> 一段话：什么场景下应该使用这个技能。

## Trigger Conditions（触发条件）

> 一段话：哪些信号 / 关键词表明应该激活这个技能。

## Preconditions（前置条件）

> 一段话：运行这个技能前必须已成立的前提。

## Workflow（工作流）

> 该技能执行的有序步骤。

## Rules（规则）

> 该技能必须遵守的硬性约束。

## Anti-Patterns（反模式）

> 不该做什么；常见错误。

## Validation（验证）

> 如何确认该技能有效；在真正运行验证前，`verified` 保持 `false`、`last_verified` 保持 `null`。

## Output Format（输出格式）

> 该技能输出的确切形态。

## Example（示例）

> 一个具体的、可复现的示例。
