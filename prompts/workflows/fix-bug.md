---
name: fix-bug
use_when: 遇到 Bug 需要修复
goal: 用证据找根因，最小修复，跑回归
related_skill: skills/core/systematic-debugging
related_workflow: workflows/bug-fix
status: experimental
verified: false
---

# Prompt — Bug 修复

> 链接到 Workflow：[Bug Fix](../../workflows/bug-fix/README.md)

## Use When

遇到 Bug 需要修复

## Goal

用证据找根因，最小修复，跑回归

## Input Variables

- `{{BUG_DESCRIPTION}}` — Bug 描述

## Expected Behavior

- 先复现再修复，不猜测
- 没有证据不声称 Root Cause
- 修完跑回归测试

## Expected Output

- 复现步骤（Step 1）
- 证据清单（Step 2）
- 根因假设 + 验证方法（Step 3）
- 修改内容 + 理由（Step 4）
- 回归测试结果（Step 5）
- Review 结果（Step 6）
- PASS / FAIL（Step 7）

## Validation

- Bug 已修复且有证据
- 回归测试通过
- 最终判定为 PASS / FAIL

## Prompt

```
我遇到了一个 Bug：{{BUG_DESCRIPTION}}

请按以下流程修复：

Step 1 — Reproduce
找到稳定复现的步骤。
→ 输出复现步骤

Step 2 — Collect Evidence
看日志、报错、网络请求、数据库状态。
→ 输出证据清单

Step 3 — Root Cause
基于证据定位根因。
→ 输出根因假设 + 验证方法

【GATE】没有充分证据之前，不允许声称 Root Cause。

Step 4 — Minimal Fix
只改导致根因的那一处代码。
→ 输出修改内容 + 理由

Step 5 — Regression Test
跑全部相关测试（不只是修的那个场景）。
→ 输出测试结果

Step 6 — Review
检查修改是否引入新问题。
→ 输出 Review 结果

Step 7 — Verify
验证 Bug 已修复 + 无回归。
→ 输出 PASS / FAIL
```

## Hard Gate

| Gate | 条件 | 不满足时 |
| --- | --- | --- |
| 1 | 有证据支撑根因 | 不允许声称 Root Cause |
| 2 | 回归测试通过 | 不允许标记完成 |

## Common Mistakes

- ❌ "可能是这里的问题" → 直接改
- ❌ 只测修的场景不跑回归
- ❌ 一次改多个文件
