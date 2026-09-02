# Current Sprint

> 冲刺时间：2026-09-02
> 冲刺目标：补齐 3 份最高价值缺失文档

---

## Task 1

**Goal**: 创建 `docs/concepts/core-methodology.md`——核心方法论文档

**Why**: EasyVibeCoding 缺少一份系统论述"为什么不推荐一条超级 Prompt 直接生成整个项目"以及"工程化方法论的 9 步流程"的文档。这是所有 Skills / Workflows / Cases 的概念基础，没有它，用户只能看到零散的技能和流程，无法理解整体框架。影响范围：全部用户。缺口严重度：完全缺失。

**Files**:
- `docs/concepts/core-methodology.md`（新建）

**Acceptance Criteria**:
- [ ] 讲清楚 Idea → Understand → Design → Plan → Build → Test → Review → Verify → Ship 的 9 步流程
- [ ] 解释"为什么不推荐一条超级 Prompt 直接生成整个项目"
- [ ] 每步配一句大白话 + 对应的 Skill / Workflow
- [ ] 包含 Mermaid 流程图
- [ ] 交叉链接到相关 Skill / Workflow / Anti-Pattern
- [ ] 标注 `⚠️ Not Yet Verified`

---

## Task 2

**Goal**: 创建 `docs/getting-started/how-to-use-easyvibecoding.md`——小白入口指南

**Why**: EasyVibeCoding 的使命是"让不会编程的人也能用 AI 做软件"，但当前仓库没有一份面向小白的集中入口指南。README 的"首次用户旅程"列了 8 步但过于精简，初学者需要更明确的"我应该先看什么→复制哪个 Prompt→学哪个 Skill→做哪个 Case"的路径。影响范围：所有初学者。缺口严重度：完全缺失。

**Files**:
- `docs/getting-started/how-to-use-easyvibecoding.md`（新建）

**Acceptance Criteria**:
- [ ] 回答"我是小白，我应该先看什么？"
- [ ] 回答"我应该复制哪个 Prompt？"
- [ ] 回答"我应该学哪个 Skill？"
- [ ] 回答"我应该做哪个 Case？"
- [ ] 给出明确路径：Start Here → First Project → Debugging → Testing → Workflow → Advanced
- [ ] 每步有链接指向具体文件
- [ ] 标注 `⚠️ Not Yet Verified`

---

## Task 3

**Goal**: 创建 `docs/getting-started/decision-tree.md`——场景决策树

**Why**: 用户来到仓库后，面对 5 个 Workflow、16 个 Skill、23 个 Prompt，无法快速判断"我的场景该走哪条路"。缺少决策树导致用户要么随机翻文件，要么放弃。影响范围：所有用户。缺口严重度：完全缺失。

**Files**:
- `docs/getting-started/decision-tree.md`（新建）

**Acceptance Criteria**:
- [ ] 覆盖场景：新项目 / 加功能 / 程序报错 / 重构 / 测试 / 验证 AI 是否完成
- [ ] 每个场景指向对应的 Workflow
- [ ] 包含 Mermaid 决策树图
- [ ] 每个场景配"你需要哪个 Skill / Prompt"的快速链接
- [ ] 标注 `⚠️ Not Yet Verified`
