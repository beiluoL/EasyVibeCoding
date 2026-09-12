# Workflow Matrix 工作流矩阵

> 6 个 Workflow 各用了哪些 Skill、哪些 Human Gate、什么级别的验证。

| Workflow | Skills | Human Gates | Verification Level |
| --- | --- | --- | --- |
| New Project | requirement-analysis, brainstorming, architecture-design, task-planning, implementation, testing, code-review, verification | Gate1 需求确认, Gate2 架构确认, Gate3 范围确认, Gate4 发布确认 | Level 4+ |
| Feature Development | requirement-analysis, project-discovery, task-planning, implementation, testing, code-review, verification | Gate1 需求确认, Gate2 实现范围确认, Gate3 Review 确认 | Level 3+ |
| Bug Fix | systematic-debugging, testing, code-review, verification | Gate1 根因确认, Gate2 修复方案确认 | Level 3+ |
| Refactoring | project-discovery, testing, code-review, verification | Gate1 重构计划确认, Gate2 回归确认 | Level 4+ |
| Testing | testing, verification | Gate1 测试策略确认 | Level 3+ |
| Release | testing, verification, code-review | Gate1 发布确认（必须） | Level 5+ |

> 验证级别参考 [Verification Ladder](./verification-ladder.md)。

## Skill → Workflow 映射

| Skill | 被哪些 Workflow 使用 |
| --- | --- |
| project-discovery | New Project, Feature Development, Refactoring |
| requirement-analysis | New Project, Feature Development |
| brainstorming | New Project |
| architecture-design | New Project |
| task-planning | New Project, Feature Development |
| implementation | New Project, Feature Development |
| systematic-debugging | Bug Fix |
| testing | 所有 |
| code-review | 所有（除 Testing） |
| verification-before-completion | 所有 |

> testing 和 verification 被 6 个 Workflow 全部使用——它们是最通用的 Skill。

## 延伸阅读

- [Workflow State Machine](./workflow-state-machine.md)
- [Core Skills Matrix](./core-skills-matrix.md)
- [Human Approval Matrix](./human-approval-matrix.md)
