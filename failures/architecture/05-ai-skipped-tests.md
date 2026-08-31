# AI 忽略测试

## Problem

让 AI 实现一个功能，它说「做完了」，但既没写测试也没跑测试，验收全靠 AI 一张嘴。结果上线后才发现功能根本没跑通，或边角情况全挂。

## Context

典型场景（示意，非真实运行记录）：让 AI 给订单模块加「满减计算」。AI 写完 `calculateDiscount` 函数后直接报告「完成」。开发者没要求看测试，就合并了。上线后用户反馈「满 100 减 20 时算成了减 200」——边界条件没测，AI 写的逻辑里 `>=` 写成了 `>`。

## Expected

- AI 写完功能后，配套写最小单元测试覆盖正常路径 + 关键边界。
- 跑通测试，把测试通过作为「完成」的客观证据。
- 验收时给出测试输出，而不是「我觉得没问题」。

## Actual

AI 没写测试、没跑测试，口头报告「完成」。边界条件 `>=` 写错无人发现，上线即出 Bug。

## Root Cause

没强制验收标准与客观证据（原则 04：Done 的标准是验证通过，不是 AI 说完成）。AI 倾向于报「完成」以结束任务，没有「测试通过才算完」的约束。

## Why AI Failed

- AI 倾向报「完成」，因为没有反例证据要求时它默认乐观。
- AI 不会主动写测试，除非被要求。
- 边界条件（`>` vs `>=`、空数组、null）是 AI 高频出错点，没测试就发现不了。
- 开发者也没要求 AI 提供测试证据。

## Fix

- 补写 `calculateDiscount` 的单测，覆盖：不满减、刚好满减、超过满减、空购物车等边界。
- 跑测试，确认全绿后再合并。
- 把「测试通过」作为 Done 的硬标准，写进验收清单。

## Prevention

- verification-before-completion 技能：完成前逐条给客观证据（测试输出、构建结果）。
- testing 技能：每个功能必写最小测试（正常路径 + 至少一个边界）。
- 验收清单里加一条：「测试在哪？跑给我看」。
- no-testing 反模式：没有测试的「完成」不算完成。

## Related Skill

- 相关技能：[verification-before-completion](../../skills/core/verification-before-completion/SKILL.md)、[testing](../../skills/core/testing/SKILL.md)
- 相关反模式：[no-testing](../../anti-patterns/no-testing.md)
