# Core Skills Matrix 核心技能矩阵

> 每个核心技能的一览表：解决什么问题、输入输出、什么时候用。

| Skill | 解决的问题 | 输入 | 输出 | 触发时机 | 人工确认 |
| --- | --- | --- | --- | --- | --- |
| 01 Project Discovery | 理解陌生项目 | 项目目录 | 项目地图、架构摘要、运行方式 | 新项目、陌生仓库 | 架构理解确认 |
| 02 Requirement Analysis | 把一句话需求变成可执行需求 | 用户想法、项目背景 | 需求文档（Goal/FR/NFR/MVP/Acceptance） | 新项目、新功能 | MVP 范围确认 |
| 03 Brainstorming | 探索多方案再选择 | 项目目标、约束条件 | 方案对比表（Options/Trade-offs/Risks） | 方案不确定时 | 最终方案选择 |
| 04 Architecture Design | 把需求变成简单设计 | 需求文档、技术约束 | 架构图（模块/数据流/API/数据库/安全） | 需求明确后 | 关键架构决策 |
| 05 Task Planning | 拆大需求为小任务 | 需求文档、架构图 | 任务列表（Goal/Input/Files/Acceptance） | 架构确定后 | 任务拆解确认 |
| 06 Implementation | 小步可控的代码修改 | Task 描述、现有代码 | 代码变更（diff）、验证结果 | 每个 Task | 新依赖/公共接口改动 |
| 07 Systematic Debugging | 用证据 Debug 不靠猜 | 报错信息、复现步骤 | 根因、最小修复、回归验证 | 代码跑不起来 | 3 轮无进展时停 |
| 08 Testing | 证明代码能工作 | 代码、验收标准 | 测试文件、测试结果、覆盖率 | 功能完成后 | 测试策略选择 |
| 09 Code Review | 第二视角检查质量 | 代码 diff、项目规范 | Review 报告（PASS / CHANGES_REQUIRED） | 实现完成后 | CHANGES_REQUIRED 修复方案 |
| 10 Verification | 防止"假完成" | 验收标准、代码 | 逐条验证结果（✅/❌ + 证据） | AI 说"完成"时 | 最终完成判定 |

## 职责边界

| 容易混淆 | 区别 |
| --- | --- |
| Requirement Analysis vs Brainstorming | 需求分析 = 搞清"做什么"；头脑风暴 = 探索"怎么做" |
| Architecture Design vs Task Planning | 架构 = 设计"模块怎么连"；任务拆解 = 安排"先做哪个后做哪个" |
| Implementation vs Testing | 实现 = 写代码；测试 = 证明代码能跑 |
| Code Review vs Verification | Code Review = 检查"代码质量好不好"；Verification = 证明"需求真的完成了" |

## 延伸阅读

- [Core Skills Map](./core-skills-map.md) — 技能依赖关系图
- [Skill Selector](../getting-started/skill-selector.md) — 按场景选技能
- [Using Core Skills](../getting-started/using-core-skills.md) — 使用指南
