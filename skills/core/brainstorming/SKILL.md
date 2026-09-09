---
name: brainstorming
description: 方案未定时结构化发散→收敛，列出至少 3 个候选方案并对比优缺点风险，避免锁死第一个想到的方案。
version: 1.0.0
category: core
difficulty: beginner
status: experimental
verified: false
compatible:
  - codex
  - claude-code
  - cursor
prerequisites:
  - 存在一个待决策的技术/方案问题
inputs:
  - 待决策问题（如"笔记数据怎么存"）
outputs:
  - 方案对比表 + 选定方案 + 否决方案记录
triggers:
  - 用户面临多个技术选型
  - 出现"用 A 还是 B"的开放决策
  - 方案空间未充分探索
validation:
  - 至少 3 个候选方案
  - 每方案列优缺点 + 风险
  - 选定方案有理由，否决方案有原因
last_verified: null
---

# Brainstorming（方案发散与收敛）

## Purpose（目的）

方案还没定、有多种可能时，结构化地"发散→收敛"：先列至少 3 个候选，再对比优缺点与风险，最后选一个并说明理由。避免一上来就锁死第一个想到的方案。

> 小白常见误区：想到"用 localStorage"就立刻动手，结果后期发现存不下/不能同步。先发散再收敛，能少走弯路。

## What Problem Does It Solve?（解决什么问题）

在设计之前探索多个可能方案，避免一开始就锁死技术选择。直接用第一个想到的方案，后期往往发现它不满足约束（容量、成本、同步、性能），但已成定局难以回头。先发散列对比再收敛，能少走弯路。

## When to Use（何时使用）

- 面临技术选型（存哪、用什么框架、同步还是本地）
- 有多个可行路径，不确定哪个好
- 在 architecture-design（架构设计）定技术栈之前

## When Not to Use（何时不要用）

- 方案已经确定且有明确 spec 时
- 纯 CRUD 功能不需要头脑风暴
- 时间极其紧、约束已限定唯一路径

## Beginner Explanation（小白解释）

头脑风暴就是"先别急着选，把可能的方案都列出来比一比"——就像买手机前先看几款对比参数。

## Trigger Conditions（触发条件）

- 用户问"A 还是 B"或"用什么好"
- 出现开放性技术决策
- 想到的第一个方案没人质疑时

## Preconditions（前置条件）

- 有一个明确的待决策问题
- 决策维度已清楚（如成本、复杂度、性能）

## Inputs（输入）

- 项目目标（要解决什么、给谁用）
- 约束条件（预算 / 时间 / 技术能力）
- 已知限制（如必须用某语言、必须离线运行）

## Outputs（输出）

- 方案对比表，包含：
  - Options（候选方案，≥3 个）
  - Trade-offs（优缺点对比）
  - Risks（每方案风险）
  - Recommendation（选定方案 + 理由 + 否决方案记录）

## Workflow（工作流）

1. **列至少 3 个候选方案**：穷举可能选项，哪怕看起来不靠谱。
2. **每方案列优缺点 + 风险**：客观列。
3. **用一张对比表**：横向对比。
4. **选一个并说明理由**：基于项目实际（MVP、用户、约束）。
5. **记录被否决方案（why）**：避免以后重复讨论。

```mermaid
flowchart LR
    A[待决策问题] --> B[列 ≥3 候选]
    B --> C[每方案:优缺点+风险]
    C --> D[对比表]
    D --> E[选 1 个+理由]
    E --> F[记录否决方案]
```

## Rules（规则）

- 至少 3 个方案，不允许只列 1 个。
- 不允许"我觉得这个好"无理由——必须给依据。
- 选定理由要绑定项目约束（MVP 规模、谁用、预算）。
- 否决方案要写原因，不是删掉。

## Human Checkpoints（人工确认点）

- **最终方案选择由人确认**：AI 给出对比表和推荐理由，但选定哪个方案、放弃哪个方案，由人根据实际偏好与隐性约束拍板。

## Anti-Patterns（反模式）

- ❌ 只列 1 个方案就开干
- ❌ 理由是"感觉""大家都用"
- ❌ 否决方案直接删掉不留记录
- ❌ 对比表没有风险列

## Validation（验证）

验证状态：⚠️ Not Yet Verified — 待按 Expected Validation Steps 实际运行后更新。

**Expected Validation Steps：**
1. 取真实选型题（如"笔记存储方案"），产出对比表。
2. 检查方案数 ≥ 3，每方案优缺点/风险齐全。
3. 让另一人仅看对比表能否复现选定结论。

## Output Format（输出格式）

| 方案 | 优点 | 缺点 | 风险 |
|------|------|------|------|
| A | … | … | … |
| B | … | … | … |
| C | … | … | … |

**选定**：X — 理由：…
**否决**：Y（因为…）、Z（因为…）

## Example（示例）

见 `examples/README.md`：笔记存储方案对比（localStorage vs SQLite vs 云数据库）。

## Related Prompts（相关提示词）

- [analyze-requirement](../../../prompts/architecture/analyze-requirement.md)

## Related Workflows（相关工作流）

- [Start Project](../../../workflows/start-project/README.md)

## Related Cases（相关案例）

- [AI Chat](../../../cases/golden/001-ai-chat/README.md)
