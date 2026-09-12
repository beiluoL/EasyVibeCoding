---
name: requirement-analysis
description: 把 Project Brief 拆成可验证的需求清单，分功能性需求(FR)与非功能性需求(NFR)，每条配验收标准，让"做完"可被检验。
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
  - 已有 Project Brief（建议先用 project-discovery）
inputs:
  - Project Brief
outputs:
  - 需求清单（FR + NFR，含优先级 P0/P1/P2 与验收标准）
triggers:
  - 项目目标已明确，需要拆解成具体功能
  - 用户问"这个项目要做哪些功能"
  - 需求不清或不可验证时
validation:
  - 每条 FR 用"用户能做 X"句式
  - 每条需求有验收标准
  - FR 与 NFR 分开
last_verified: null
---

# Requirement Analysis（需求分析）

## Purpose（目的）

把 Project Brief 拆成一份"可验证的需求清单"。分功能性需求（FR）与非功能性需求（NFR），每条都要能被检验——"怎么算完成"写得清清楚楚。

> 术语解释：
> - **FR（功能性需求，Functional Requirement）**：产品"能做什么"。比如"用户能创建笔记"。
> - **NFR（非功能性需求，Non-Functional Requirement）**：做得"好不好"。比如速度、安全、兼容性。"单页打开 < 1 秒"。

## What Problem Does It Solve?（解决什么问题）

把"帮我做一个 AI 聊天网站"这种一句话需求变成可执行需求文档。一句话想法无法直接进入开发，必须先拆成"做什么/不做什么/每条怎么算完成"，否则开发会跑偏、范围失控、验收无据。

## When to Use（何时使用）

- Project Brief 已确认，要往下拆功能
- 需要把"目标"翻译成"可执行的清单"
- 在 brainstorming（方案发散）或 architecture-design（架构设计）之前

## When Not to Use（何时不要用）

- 需求已经非常明确且有详细 spec 文档时
- 已有成熟 PRD / 验收清单，无需重新拆解
- 纯探索阶段，连 Project Brief 都还没成型

## Beginner Explanation（小白解释）

需求分析就是在动手之前先搞清楚"到底要做什么"——就像装修前先量房出图，不能直接砸墙。

## Trigger Conditions（触发条件）

- 用户说"列出功能""需求有哪些""要做哪些事"
- 存在 Project Brief 但还没有需求清单
- 需求描述含糊（如"要好""要快"）无法验证

## Preconditions（前置条件）

- 已有 Project Brief
- 用户愿意逐条确认验收标准

## Inputs（输入）

- 用户的一句话想法
- 项目背景（要给谁用、解决什么问题）
- 目标用户描述（谁、在哪、为什么用）

## Outputs（输出）

- 需求文档，包含：
  - Goal（项目目标）
  - Users（目标用户）
  - User Stories（用户故事）
  - FR（功能性需求，含优先级与验收标准）
  - NFR（非功能性需求）
  - MVP 范围（必须做的最小集合）
  - Acceptance Criteria（验收标准）

## Workflow（工作流）

1. **从 Brief 提取功能点**：把 MVP 里的每件事拆成独立功能点。
2. **每点写成"用户能做 X"句式**：主语是用户，动词是动作。
3. **标优先级**：P0（必须有）/ P1（应该有）/ P2（可以有）。
4. **补 NFR**：性能、安全、兼容、可维护等"质量"要求。
5. **每条写验收标准**：怎么算这条做完了（可观察、可检验）。

```mermaid
flowchart LR
    A[Project Brief] --> B[提取功能点]
    B --> C[写成 用户能做X]
    C --> D[标 P0/P1/P2]
    D --> E[补 NFR]
    E --> F[每条写验收标准]
    F --> G[需求清单交付]
```

## Rules（规则）

- 每条 FR 必须是"用户能做 X"，不能写成"系统支持 X"。
- 每条需求必须有验收标准（写不出验收标准 = 需求不清）。
- FR 与 NFR 分开列。
- 优先级只能选一个，不能全是 P0。
- 不在此阶段定技术实现。

## Human Checkpoints（人工确认点）

- **MVP 范围确认**：哪些功能进 MVP、哪些延后，需人工拍板，不能由 AI 单方决定。
- **Out of Scope 确认**：明确写出"不做的事项"，由人确认无遗漏后再进入下一阶段。

## Anti-Patterns（反模式）

- ❌ 需求写成"系统要强大""体验要好"——无法验证
- ❌ 没有验收标准
- ❌ FR/NFR 混在一起
- ❌ 所有需求都是 P0

## Validation（验证）

验证状态：⚠️ Not Yet Verified — 待按 Expected Validation Steps 实际运行后更新。

**Expected Validation Steps：**
1. 拿一份真实 Project Brief，产出需求清单。
2. 逐条检查：能否用"用户能做 X"复述？验收标准能否用一句话检验？
3. 让另一位协作者仅凭验收标准判断"是否完成"，能判断即合格。

## Output Format（输出格式）

| 编号 | 类型 | 需求描述 | 优先级 | 验收标准 |
|------|------|----------|--------|----------|
| FR-01 | 功能 | 用户能… | P0 | … |
| NFR-01 | 非功能 | … | P1 | … |

## Example（示例）

见 `examples/README.md`：笔记网站 → FR-01 用户能创建/编辑/删除笔记；NFR-01 单页打开 < 1s。

## Related Prompts（相关提示词）

- [start-project](../../../prompts/start-here/start-project.md)
- [analyze-requirement](../../../prompts/architecture/analyze-requirement.md)

## Related Workflows（相关工作流）

- [Start Project](../../../workflows/new-project/README.md)
- [Feature Development](../../../workflows/feature-development/README.md)

## Related Cases（相关案例）

- [AI Chat](../../../cases/golden/001-ai-chat/README.md)
