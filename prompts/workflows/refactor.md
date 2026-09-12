---
name: refactor
use_when: 需要重构代码
goal: 有测试保护地小步重构
related_skill: skills/core/implementation
related_workflow: workflows/refactoring
status: experimental
verified: false
---

# Prompt — 重构

> 链接到 Workflow：[Refactoring](../../workflows/refactoring/README.md)

## Use When

需要重构代码

## Goal

有测试保护地小步重构

## Input Variables

- `{{REFACTOR_TARGET}}` — 要重构的代码/模块描述

## Expected Behavior

- 没有测试保护时不允许大规模重构
- 每步只做一个小改动
- 每步改完跑测试

## Expected Output

- 行为摘要（Step 1）
- 测试确认/补充结果（Step 2）
- 重构计划（Step 3）
- 修改内容（Step 4）
- 测试结果（Step 5）
- Review 结果（Step 6）
- PASS / FAIL（Step 7）

## Validation

- 重构完成且测试通过
- 无回归
- 最终判定为 PASS / FAIL

## Prompt

```
我需要重构：{{REFACTOR_TARGET}}

请按以下流程执行：

Step 1 — Understand
理解现有行为：这段代码做什么？谁调用它？
→ 输出行为摘要

Step 2 — Characterize Behavior
确认/补充测试：现有行为有没有测试保护？
→ 如果没有，先写测试

【GATE】没有足够测试保护的情况下，不允许大规模重构。

Step 3 — Plan
制定重构计划：分几步？每步改什么？
→ 输出重构计划

Step 4 — Small Refactor
每步只做一个小改动。
→ 输出修改内容

Step 5 — Test
每步改完跑测试。
→ 输出测试结果

Step 6 — Review Diff
检查改动是否安全。
→ 输出 Review 结果

Step 7 — Regression
跑全部相关测试确认无回归。
→ 输出 PASS / FAIL
```

## Hard Gate

| Gate | 条件 | 不满足时 |
| --- | --- | --- |
| 1 | 有测试保护 | 不允许大规模重构 |
| 2 | 每步测试通过 | 不允许进入下一步 |

## Common Mistakes

- ❌ 没测试就重构——改完不知道有没有破坏
- ❌ 一次改太多——无法定位问题
- ❌ 重构和功能修改混在一起
