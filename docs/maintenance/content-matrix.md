# Content Matrix

> 内容矩阵：跟踪每类资产的数量、状态、质量和优先级。
> 更新时间：2026-09-02

---

## 状态定义

| 状态 | 含义 |
| --- | --- |
| planned | 已规划，尚未创建 |
| draft | 已创建草稿，结构不完整 |
| experimental | 结构完整，未真实验证 |
| community | 社区使用过，有反馈 |
| verified | 真实验证（有可复现证据） |
| stable | 验证通过 + 多项目使用 + 稳定 |
| deprecated | 已废弃，不再推荐 |

---

## 资产总览

| Asset | Target | Actual | Status | Quality | Priority |
| --- | --- | --- | --- | --- | --- |
| Skill (core) | 10 | 10 | experimental | 结构完整，有示例但未验证 | P0 |
| Skill (ai) | 6 | 6 | experimental | 结构完整，有示例但未验证 | P2 |
| Prompt | 20 | 23 | experimental | 结构完整，未实战验证 | P1 |
| Workflow | 5 | 5 | experimental | 结构完整，已补齐暂停/确认 | P1 |
| Case (golden) | 5 | 5 | experimental | 结构完整，未跑通 | P1 |
| Case (beginner) | 1+ | 0 | planned | — | P2 |
| Failure | 10 | 10 | experimental | 结构完整，内容充实 | P1 |
| Anti-Pattern | 8 | 8 | experimental | 7 节结构完整 | P1 |
| Benchmark | 10 | 10 | experimental | 任务定义完成，无真实结果 | P3 |
| Learning Roadmap | 1 | 1 | experimental | 11 级详细路线 | P1 |
| Coding Constitution | 1 | 1 | experimental | 10 条宪法 | P1 |
| Verification Standard | 1 | 1 | draft | 56 行，缺 5 级等级 | P1 |
| Core Methodology | 1 | 0 | planned | — | P0 |
| Beginner Guide | 1 | 0 | planned | — | P0 |
| Decision Tree | 1 | 0 | planned | — | P1 |

---

## Core Skills 明细

| Skill | Status | Verified | Examples | 交叉引用 | 缺口 |
| --- | --- | --- | --- | --- | --- |
| project-discovery | experimental | false | 1 个 | → prompts, skills | 缺项目入口检测清单 |
| requirement-analysis | experimental | false | 1 个 | → prompts, skills | — |
| brainstorming | experimental | false | 1 个 | → prompts, skills | — |
| architecture-design | experimental | false | 1 个 | → prompts, skills | — |
| task-planning | experimental | false | 1 个 | → prompts, skills | — |
| implementation | experimental | false | 1 个 | → prompts, skills | — |
| systematic-debugging | experimental | false | 1 个 | → prompts, skills | 缺 9 步显式拆分 |
| testing | experimental | false | 1 个 | → prompts, skills | — |
| code-review | experimental | false | 1 个 | → prompts, skills | — |
| verification-before-completion | experimental | false | 1 个 | → prompts, skills | — |

## AI Skills 明细

| Skill | Status | Verified | Examples | 缺口 |
| --- | --- | --- | --- | --- |
| agent | experimental | false | 1 个 | — |
| context-engineering | experimental | false | 1 个 | — |
| mcp | experimental | false | 1 个 | — |
| memory | experimental | false | 1 个 | — |
| rag | experimental | false | 1 个 | — |
| tool-calling | experimental | false | 1 个 | — |

## Workflows 明细

| Workflow | Status | Trigger | When to Pause | Validation | 关联 Skills |
| --- | --- | --- | --- | --- | --- |
| start-project | experimental | ✅ | ✅ | ✅ | project-discovery → requirement → brainstorming → architecture → planning → implementation → testing → review → verification |
| feature-development | experimental | ✅ | ✅ | ✅ | requirement → planning → implementation → testing → review → verification |
| debugging | experimental | ✅ | ✅ | ✅ | systematic-debugging → testing → verification |
| refactoring | experimental | ✅ | ✅ | ✅ | implementation → testing → review → verification |
| release | experimental | ✅ | ✅ | ✅ | testing → review → verification |

## Anti-Patterns 明细

| Anti-Pattern | 7 节结构 | → failures 链接 | → skills 链接 |
| --- | --- | --- | --- |
| giant-prompt | ✅ 7/7 | ❌ 缺 | ✅ |
| blind-rewrite | ✅ 7/7 | ❌ 缺 | ✅ |
| endless-debug-loop | ✅ 7/7 | ❌ 缺 | ✅ |
| no-project-context | ✅ 7/7 | ❌ 缺 | ✅ |
| no-testing | ✅ 7/7 | ❌ 缺 | ✅ |
| architecture-by-guessing | ✅ 7/7 | ❌ 缺 | ✅ |
| uncontrolled-agent | ✅ 7/7 | ✅ | ✅ |
| secret-leak | ✅ 7/7 | ✅ | ✅ |

> 缺口：6/8 个 anti-patterns 未链接到相关 failures。

## Failures 明细

| Failure | 类别 | 9 节结构 | → skills 链接 |
| --- | --- | --- | --- |
| 01-ai-infinite-bug-fix | debugging | ✅ | ✅ |
| 02-ai-wrong-file | debugging | ✅ | ✅ |
| 03-ai-modified-db | architecture | ✅ | ✅ |
| 04-ai-duplicate-code | architecture | ✅ | ✅ |
| 05-ai-skipped-tests | architecture | ✅ | ✅ |
| 06-token-explosion | ai | ✅ | ✅ |
| 07-rag-retrieval-failed | ai | ✅ | ✅ |
| 08-agent-infinite-loop | ai | ✅ | ✅ |
| 09-tool-overscope | ai | ✅ | ✅ |
| 10-api-key-leak | deployment | ✅ | ✅ |

---

## 优先级定义

| 优先级 | 含义 | 当前范围 |
| --- | --- | --- |
| P0 | 核心基础设施 | 内容标准、Skill 标准、维护文档、核心方法论、小白入口 |
| P1 | 核心内容 | Core Skills 完善、Core Prompts、Core Workflows、Beginner Cases、Failure Cases |
| P2 | 扩展内容 | AI Skills、RAG、Agent、MCP、Context、Memory |
| P3 | 长期研究 | Benchmark 扩展、Evaluation、高级 Agent Engineering |
