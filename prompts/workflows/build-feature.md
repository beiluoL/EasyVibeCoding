---
name: build-feature
use_when: 要增加一个新功能
goal: 按 7 步流程完成功能开发，不跳步
related_skill: skills/core/implementation
related_workflow: workflows/feature-development
status: experimental
verified: false
---

# Prompt — 功能开发

> 链接到 Workflow：[Feature Development](../../workflows/feature-development/README.md)

## Use When

要增加一个新功能

## Goal

按 7 步流程完成功能开发，不跳步

## Input Variables

- `{{FEATURE}}` — 用户想增加的功能描述

## Expected Behavior

- AI 按 7 步顺序执行，不跳步
- 每个 Gate 不满足时停下来
- 不一次性修改大量文件

## Expected Output

- 需求清单（Step 1）
- 项目理解摘要（Step 2）
- 任务列表（Step 3）
- 代码变更 + 变更说明（Step 4）
- 测试结果（Step 5）
- Review 结果（Step 6）
- PASS / PARTIAL / FAIL（Step 7）

## Validation

- 7 步全部执行，无跳步
- 每个 Gate 条件满足
- 最终判定为 PASS / PARTIAL / FAIL

## Prompt

```
我想增加：{{FEATURE}}

请按以下流程执行：

Step 1 — Requirement
分析需求：做什么？为谁做？验收标准是什么？
→ 输出需求清单

Step 2 — Inspect
理解现有项目：相关文件、调用链、规范
→ 输出项目理解摘要

Step 3 — Plan
拆成小任务：每个任务范围明确、可独立验证
→ 输出任务列表

【GATE 1】需求没有理解清楚，不得编码。
【GATE 2】没有开发计划，不得大规模修改。

Step 4 — Implement
逐个任务实现，一次只做一个
→ 输出代码变更 + 变更说明

Step 5 — Test
写测试并运行
→ 输出测试结果

【GATE 3】测试没有执行，不得声称完成。

Step 6 — Review
检查：安全、质量、一致性
→ 输出 Review 结果

Step 7 — Verify
逐条验证验收标准
→ 输出 PASS / PARTIAL / FAIL

【GATE 4】验证没有通过，不得标记 Done。
```

## Hard Gates

| Gate | 条件 | 不满足时 |
| --- | --- | --- |
| 1 | 需求已理解 | 不编码 |
| 2 | 已有计划 | 不大规模修改 |
| 3 | 测试已执行 | 不声称完成 |
| 4 | 验证已通过 | 不标记 Done |

## Common Mistakes

- ❌ 用户一句话 → 直接修改大量文件
- ❌ 跳过 Inspect 直接编码
- ❌ 不跑测试就说完成
