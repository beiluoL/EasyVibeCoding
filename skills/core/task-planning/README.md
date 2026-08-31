# Task Planning（任务拆解）

> 别让 AI 一把梭，拆成小步做一步验一步。

## What（是什么）

把需求拆成小步、可独立验证的任务清单，每步范围受控（<半天），标依赖与验收点。对应原则：Small tasks over giant prompts。

## When（何时用）

- 需求/架构已定，准备编码
- 用户想一次性丢整个项目给 AI
- 任务太大无法独立验证

## How（怎么用）

1. 需求 → 拆子任务
2. 每任务 < 半天
3. 标依赖顺序
4. 每任务配验收点
5. 排成有序清单

## 相关资源

- 详细规范：[SKILL.md](./SKILL.md)
- 完整示例：[examples/](./examples/README.md)
- 上游技能：[../architecture-design/SKILL.md](../architecture-design/SKILL.md)、[../requirement-analysis/SKILL.md](../requirement-analysis/SKILL.md)
- 配套 Prompt 模板：[../../../prompts/architecture/write-development-plan.md](../../../prompts/architecture/write-development-plan.md)
