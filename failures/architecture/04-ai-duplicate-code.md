# AI 生成重复代码

## Problem

项目里已经有现成的 `formatDate` 工具函数，让 AI 写个新功能时，它又写了一个几乎一模一样的 `formatTime`，甚至逻辑还比原来的差。代码库越堆越多重复实现。

## Context

典型场景（示意，非真实运行记录）：项目 `utils/date.ts` 里已有 `formatDate(date, pattern)`。开发者让 AI 在 `order/components/OrderList.vue` 里加个「订单时间显示」，没告诉它有现成工具。AI 直接在组件里手写了一段 `new Date().getFullYear() + '-' + ...` 的拼接，还处理错了时区。

## Expected

AI 检索到 `utils/date.ts` 中的 `formatDate`，直接复用，零重复代码，时区也正确。

## Actual

AI 在组件内新写了一段日期格式化逻辑，与现有 `formatDate` 功能重叠、实现更差、还带时区 Bug。后续要改格式化规则得改两处。

## Root Cause

没给 AI 已有代码上下文，AI 不知道有现成的（违反原则 03：Reuse before reinvent，先复用再重造）。AI 默认「从零生成」而不是「先找现成的」。

## Why AI Failed

- AI 默认从零生成，不会主动检索项目内是否已有实现。
- 没有约束 AI「先复用再新建」，它就顺手写新的。
- 开发者也没在 prompt 里提示「先看 utils 目录有没有现成的」。
- 项目缺乏工具函数索引，AI 难以发现复用点。

## Fix

- 删除 AI 新写的重复实现，改为 `import { formatDate } from '@/utils/date'`。
- 让 AI 先检索项目内同类工具，再决定是否新建。
- 在 architecture-design / implementation 技能里强调「Reuse before reinvent」。

## Prevention

- implementation 技能：新建函数前先 Grep 同名/同类工具。
- architecture-design 技能：维护一份「常用工具函数清单」，让 AI 能快速复用。
- code-review 时把「重复实现」列为必查项。
- prompt 模板加一句：「先检索项目内是否已有类似实现，有则复用」。

## Related Skill

- 相关技能：[implementation](../../skills/core/implementation/SKILL.md)
- 相关反模式：[architecture-by-guessing](../../anti-patterns/architecture-by-guessing.md)
