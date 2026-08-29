# 04 — 新手最常犯的 8 个错

> 用 AI 写代码，90% 的坑都在这 8 个里。先看一遍，能少走很多弯路。

> 术语小贴士：**Anti-Pattern（反模式）**= 看似合理、实则埋雷的做法。知道什么不该做，和知道该做什么一样重要。

---

## 8 个反模式速览

| # | 错误 | 一句话 | 详细 |
| --- | --- | --- | --- |
| 1 | Giant Prompt 巨型提示词 | 一句话塞太多，AI 记不住 | [anti-patterns/giant-prompt.md](../../anti-patterns/giant-prompt.md) |
| 2 | No Testing 不写测试 | AI 说对了就信，不验证 | [anti-patterns/no-testing.md](../../anti-patterns/no-testing.md) |
| 3 | Blind Rewrite 盲目重写 | 出错就整个重生成 | [anti-patterns/blind-rewrite.md](../../anti-patterns/blind-rewrite.md) |
| 4 | Endless Debug Loop 无限调试 | 改了跑、跑不通再改，没头 | [anti-patterns/endless-debug-loop.md](../../anti-patterns/endless-debug-loop.md) |
| 5 | Secret Leak 密钥泄露 | 把 API Key 贴进代码 | [anti-patterns/secret-leak.md](../../anti-patterns/secret-leak.md) |
| 6 | Uncontrolled Agent 失控的 Agent | 给 AI 太大权限，不设防 | [anti-patterns/uncontrolled-agent.md](../../anti-patterns/uncontrolled-agent.md) |
| 7 | No Project Context 不给项目上下文 | AI 瞎猜你的项目结构 | [anti-patterns/no-project-context.md](../../anti-patterns/no-project-context.md) |
| 8 | Architecture by Guessing 猜式架构 | 让 AI 猜技术方案 | [anti-patterns/architecture-by-guessing.md](../../anti-patterns/architecture-by-guessing.md) |

> ⚠️ Not Yet Verified：以上 anti-patterns 链接在 V0.1 为规划内容，可能尚未填充。

---

## 1. Giant Prompt（巨型提示词）

**错误表现**：一句话甩给 AI"帮我写个完整的电商系统，要有商品、购物车、支付、订单、后台管理……"

**为什么错**：
- AI 上下文窗口有限，需求太多它记不住开头（见 [02-how-ai-coding-works.md](02-how-ai-coding-works.md)）。
- 一旦出错，你不知道是哪条需求导致的。
- 违反 Principle 02（拆小任务）。

**正确做法**：拆成小任务，一次做一块。用 [write-development-plan](../../prompts/architecture/write-development-plan.md) 先拆任务，再逐个实现。

---

## 2. No Testing（不写测试）

**错误表现**：AI 说"写好了"，你看一眼能跑，就当完成。改别的地方时，这里悄悄坏了你不知道。

**为什么错**：
- AI 生成代码不保证正确，"看着对"不等于"逻辑对"。
- 违反 Principle 04（要证据）。
- 没有测试，改动 = 赌博。

**正确做法**：关键路径至少写最小测试。见 [Level 4 — Debug + Test](../learning-path/level-4.md) 和 [testing Skill](../../skills/core/testing/SKILL.md)。

---

## 3. Blind Rewrite（盲目重写）

**错误表现**：代码报错，不排查原因，直接让 AI"重新写一遍"。重写完又有新 bug，再重写……循环。

**为什么错**：
- 重写不解决根因，只是换一批 bug。
- 违反 Principle 06（每次犯错变成知识）——你不留记录，下次还犯。

**正确做法**：先系统化调试（复现→定位→假设→验证→修复），再改。见 [systematic-debugging Skill](../../skills/core/systematic-debugging/SKILL.md)。

---

## 4. Endless Debug Loop（无限调试循环）

**错误表现**：改一行 → 跑 → 报错 → 改一行 → 跑 → 又报错……改了几十轮还没好，时间全耗进去。

**为什么错**：
- 没有系统流程，纯靠试错。
- 改了不记录，重复踩同样的坑。

**正确做法**：每次改动记录"改了什么、为什么、结果如何"。如果连续 3 次没进展，停下来重新分析，别硬改。见 [endless-debug-loop 反模式](../../anti-patterns/endless-debug-loop.md)。

---

## 5. Secret Leak（密钥泄露）

**错误表现**：把 API Key、数据库密码直接贴进代码，甚至贴给 AI 对话框。

**为什么错**：
- 密钥一旦进代码仓库，可能被公开泄露。
- 违反安全规则（[SECURITY.md](../../SECURITY.md)）。
- AI 对话记录也可能被留存。

**正确做法**：
- 密钥放环境变量（`.env`），`.env` 加入 `.gitignore`。
- 永远不把真实密钥贴给 AI，用占位符代替。
- 见 [secret-leak 反模式](../../anti-patterns/secret-leak.md)。

---

## 6. Uncontrolled Agent（失控的 Agent）

**错误表现**：给 AI Agent 太大权限（能删文件、能调数据库、能发请求），不设限制，让它"自由发挥"。

**为什么错**：
- Agent 可能误删重要文件、误改数据库。
- 违反 Principle 05（关键决策人来拍板）。
- 高风险操作必须有人确认。

**正确做法**：
- Agent 执行高风险操作前要人确认。
- 限制 Agent 能调用的工具范围。
- 见 [uncontrolled-agent 反模式](../../anti-patterns/uncontrolled-agent.md)。

---

## 7. No Project Context（不给项目上下文）

**错误表现**：直接让 AI"帮我加个登录功能"，但不告诉它你用什么技术栈、项目结构长啥样、有没有现成的认证代码。

**为什么错**：
- AI 看不到你的项目，只能猜，猜错就给你一段跑不通的代码。
- 上下文给得越少，AI 越容易"幻觉"。

**正确做法**：每次让 AI 写代码前，给全上下文（技术栈、项目结构、相关已有代码、验收标准）。见 [Level 1 — 学会和 AI 沟通](../learning-path/level-1.md) 和 [no-project-context 反模式](../../anti-patterns/no-project-context.md)。

---

## 8. Architecture by Guessing（猜式架构）

**错误表现**：项目还没想清楚，就让 AI "随便选个技术方案"。AI 选了，你就用，结果做到一半发现不合适。

**为什么错**：
- 架构决策影响全局，选错了后面全要返工。
- 违反 Principle 05（关键决策人来拍板）——架构是关键决策。
- AI 不了解你的真实约束（预算、团队、时间）。

**正确做法**：
- 架构由你定，参考 AI 建议但你来拍板。
- 用 [design-architecture](../../prompts/architecture/design-architecture.md) 让 AI 给方案，但你来选。
- 见 [architecture-by-guessing 反模式](../../anti-patterns/architecture-by-guessing.md)。

---

## 一句话总结

| 错误 | 对应原则 | 正确做法 |
| --- | --- | --- |
| 巨型提示词 | 02 拆小任务 | 一次一块 |
| 不写测试 | 04 要证据 | 关键路径写测试 |
| 盲目重写 | 06 错误变知识 | 先调试再改 |
| 无限调试 | 04 要证据 | 记录 + 3 次没进展就停 |
| 密钥泄露 | 安全规则 | 放 .env，别贴 AI |
| 失控 Agent | 05 人定决策 | 高危操作要确认 |
| 不给上下文 | 01 先搞懂 | 给全信息 |
| 猜式架构 | 05 人定决策 | 你定架构，AI 给建议 |

---

## 下一步

- 系统学习 → [学习路线总览](../learning-path/roadmap.md)
- 自我评估在哪一级 → [成熟度模型](../learning-path/maturity-model.md)

> ⚠️ Not Yet Verified：本文引用的 anti-patterns / skills / prompts 链接在 V0.1 为规划内容，可能尚未填充。原则与正确做法本身是方法论指导，非已验证的统计数据。
