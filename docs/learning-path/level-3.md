# Level 3 — 学会让 AI 写功能

> Level 2 你会拆需求了，这一级你要让 AI 真正写出能跑的代码——关键是**小步、复用、给上下文**。

> 术语小贴士：**CRUD**= 增删改查（Create / Read / Update / Delete），绝大多数应用的核心就是 CRUD；**复用（Reuse）**= 别重造轮子，已有组件直接拿来用。

---

## 目标

- 学会**小步实现**：一次让 AI 写一小块，别一次要一整个系统。
- 学会**复用**：用现成的 Skill / Prompt / 库，不每次从零开始。
- 学会**给上下文**：让 AI 知道项目结构、技术栈、已有代码。
- 能让 AI 完成**一个 CRUD 小功能并通过验收**。

---

## 知识

### 1. 小步实现（Principle 02）

| ❌ 一步到位 | ✅ 小步走 |
| --- | --- |
| 帮我写完整的博客系统 | 第 1 步：先建项目骨架；第 2 步：写数据模型；第 3 步：写列表接口；第 4 步：写详情接口…… |

小步的好处：
- 每步都能**验证**（Principle 04），错了早发现。
- AI 上下文有限，一次塞太多它容易忘掉前面的要求。

### 2. 复用（Principle 03）

| 场景 | 别重造 | 该复用 |
| --- | --- | --- |
| 要做登录 | 自己写加密逻辑 | 用成熟的认证库（如 next-auth） |
| 要做 CRUD 接口 | 自己拼 SQL | 用 ORM（如 Prisma）或脚手架 |
| 要拆任务 | 每次想怎么问 | 用 [task-planning](../../skills/core/task-planning/SKILL.md) Skill |

### 3. 给上下文：让 AI 不瞎猜

每次让 AI 写功能前，给它这几样：
- **项目结构**：分了哪些模块、技术栈是什么
- **相关已有代码**：它要在哪个文件里加、要和哪些代码配合
- **验收标准**：写完怎么算"对"

---

## Skills

- 🧠 [architecture-design](../../skills/core/architecture-design/SKILL.md) — 定技术方案和模块划分
- 🧠 [task-planning](../../skills/core/task-planning/SKILL.md) — 把功能拆成可执行的小任务
- 🧠 [implementation](../../skills/core/implementation/SKILL.md) — 让 AI 按小步写代码

> ⚠️ Not Yet Verified：以上 Skill 链接在 V0.1 为规划内容，可能尚未填充。

---

## Prompts

- 💬 [design-architecture](../../prompts/architecture/design-architecture.md) — 设计技术架构
- 💬 [write-development-plan](../../prompts/architecture/write-development-plan.md) — 写开发计划（⭐ 拆任务利器）
- 💬 [implement-feature](../../prompts/coding/implement-feature.md) — 让 AI 实现单个功能

> ⚠️ Not Yet Verified：以上 Prompt 链接在 V0.1 为规划内容，可能尚未填充。

---

## 练习

1. **拆任务**：拿 Level 2 的需求清单，用 [write-development-plan](../../prompts/architecture/write-development-plan.md) 把它拆成 5–8 个小任务，每个任务能在 1 次对话内完成。
2. **小步实现**：挑其中一个小任务（比如"写用户列表接口"），用 [implement-feature](../../prompts/coding/implement-feature.md) 让 AI 实现，每次只做一个。
3. **复用检查**：实现前先问 AI / 搜一下，有没有现成的库或脚手架能省事。

---

## 项目（小项目建议）

> 做一个 CRUD 小功能（比如"待办清单 API"），完整跑通。

要求：
- 能创建、查询、修改、删除一条待办
- 每一步都**小步实现**，每步都验证能跑
- 至少复用一个现成库（数据库 ORM / Web 框架）

---

## 毕业标准（可客观判断）

- [ ] 能说清**为什么不能一次让 AI 写整个系统**（小步 vs 一步到位的区别）。
- [ ] 能用 [write-development-plan](../../prompts/architecture/write-development-plan.md) 把一个功能拆成**多个 1 次对话可完成的小任务**。
- [ ] 实现过程中至少**复用了一个现成库 / Skill**，而不是全手写。
- [ ] 完成一个 **CRUD 小功能**，且能**跑通验收标准**（增删改查每条都真的能执行，不是 AI 说"完成了"就算）。

> 毕业检验：让别人（或让 AI）按你的验收标准逐条测，每条都真能跑通——这叫"证据，不是声明"（Principle 04）。
>
> ⚠️ 注意：本级的"完成 CRUD"是**学习产出**，不代表已由第三方验证。
