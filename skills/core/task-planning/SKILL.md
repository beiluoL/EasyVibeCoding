---
name: task-planning
description: 把需求拆成小步、可独立验证的任务清单，每步范围受控，避免一个巨大 prompt 让 AI 一次写完整个项目。
version: 0.1.0
category: core
difficulty: beginner
status: experimental
verified: false
compatible: [unspecified]
prerequisites:
  - 已有需求清单或架构设计
inputs:
  - 需求清单 / 架构设计
outputs:
  - 有序任务清单（含依赖、验收点）
triggers:
  - 需求已定准备进入编码
  - 项目被一次性塞给 AI
  - 任务粒度过大无法独立验证
validation:
  - 单任务 < 半天可完成
  - 每任务有验收标准
  - 依赖关系已标注
last_verified: null
---

# Task Planning（任务拆解）

## Purpose（目的）

把一个需求拆成"小步、可独立验证"的任务清单。每步范围受控，避免一个巨大 prompt 让 AI 一次写完一整个项目（那样必然出错、难调试）。

> 对应原则：**Small tasks over giant prompts（小任务胜过巨型提示）**。AI 一次只做一小步，做一步验一步。

## When to Use（何时使用）

- 需求/架构已定，准备开始编码
- 用户想把整个项目一次性丢给 AI
- 任务太大无法独立验证

## Trigger Conditions（触发条件）

- 用户说"帮我做完整个项目""一次性生成"
- 需求清单存在但还没有任务拆解
- 单个 prompt 输出过长/出错率高

## Preconditions（前置条件）

- 有需求清单或架构设计
- 已决定逐步推进（而非一把梭）

## Workflow（工作流）

1. **需求 → 拆子任务**：按模块/功能切。
2. **每任务 < 半天可完成**：粒度控制。
3. **标依赖顺序**：A 依赖 B 就排在 B 后。
4. **每任务配验收点**：做完怎么验。
5. **排成有序清单输出**：按依赖拓扑排序。

```mermaid
flowchart LR
    A[需求/架构] --> B[拆子任务]
    B --> C[控制粒度 <半天]
    C --> D[标依赖顺序]
    D --> E[每任务配验收点]
    E --> F[有序清单交付]
```

## Rules（规则）

- 单任务粒度要小（原则：Small tasks over giant prompts）。
- 每任务必须有验收标准。
- 有依赖要标（任务 B 依赖任务 A）。
- 清单按依赖拓扑排序，先做的排前面。
- 不在一个任务里塞多个不相关功能。

## Anti-Patterns（反模式）

- ❌ 一个任务"做完整个前端"
- ❌ 没有验收点，做完不知道对不对
- ❌ 不标依赖，导致顺序错乱
- ❌ 任务粒度过大（>半天）

## Validation（验证）

验证状态：⚠️ Not Yet Verified — 待按 Expected Validation Steps 实际运行后更新。

**Expected Validation Steps：**
1. 拿真实需求清单产出任务清单。
2. 检查每任务粒度 < 半天、有验收点、依赖已标。
3. 按清单顺序逐步执行，验证每步可独立通过验收。

## Output Format（输出格式）

| 序号 | 任务 | 依赖 | 验收点 |
|------|------|------|--------|
| 1 | … | - | … |
| 2 | … | 1 | … |

## Example（示例）

见 `examples/README.md`：笔记网站拆成 8 个有序任务清单。
