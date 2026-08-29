# Level 4 — Debug + Test

> Level 3 你能让 AI 写功能了，但写完就一定对吗？这一级你要学会**系统化调试**和**最小测试**——让"能跑"变成"可信"。

> 术语小贴士：**Debug（调试）**= 找出代码为什么不对并修好；**回归测试**= 修完 bug 后写个测试，确保这个 bug 以后不再出现。

---

## 目标

- 学会**系统化调试**：不靠瞎猜，靠证据定位 bug。
- 学会**最小测试**：用最少的测试覆盖关键路径，不是为了 100% 覆盖率。
- 能**修一个 Bug 并写出对应回归测试**。

---

## 知识

### 1. 系统化调试（别瞎猜）

| ❌ 瞎猜式调试 | ✅ 系统化调试 |
| --- | --- |
| "是不是这里错了？改改试试" | 1. 复现 → 2. 看报错 → 3. 定位 → 4. 假设 → 5. 验证 → 6. 修复 → 7. 测试 |
| 改了跑、跑不通再改 | 每一步都留下"我改了什么、为什么改、结果如何"的记录 |

> 详见 [systematic-debugging](../../skills/core/systematic-debugging/SKILL.md)。核心：**先复现，再定位，最后才改**。

### 2. 最小测试（别过度）

新手容易陷入两个极端：要么不写测试，要么想测到 100% 覆盖率。正确的做法：

**先测关键路径**——最容易出问题、最重要的那几条。比如一个登录功能：
- ✅ 正确账号密码能登录
- ✅ 错误密码登录失败
- ✅ 不存在的账号登录失败

这三条覆盖了核心逻辑。边角情况（比如"密码里有 emoji"）可以后补。

### 3. 验证先行（Principle 04）

> AI 说"我修好了"——**不算修好**。能跑通测试、能复现修复、bug 不再出现——**才算修好**。

---

## Skills

- 🧠 [systematic-debugging](../../skills/core/systematic-debugging/SKILL.md) — 系统化排查 bug
- 🧠 [testing](../../skills/core/testing/SKILL.md) — 写最小可用测试
- 🧠 [code-review](../../skills/core/code-review/SKILL.md) — 让 AI 帮你审代码
- 🧠 [verification-before-completion](../../skills/core/verification-before-completion/SKILL.md) — 完成前必须验证

> ⚠️ Not Yet Verified：以上 Skill 链接在 V0.1 为规划内容，可能尚未填充。

---

## Prompts

- 💬 [debug-error](../../prompts/debugging/debug-error.md) — 让 AI 系统化帮你排查报错
- 💬 [write-tests](../../prompts/testing/write-tests.md) — 让 AI 帮你写测试
- 💬 [verify-feature](../../prompts/testing/verify-feature.md) — 验证一个功能是否真的完成
- 💬 [code-review](../../prompts/review/code-review.md) — 让 AI 审查代码

> ⚠️ Not Yet Verified：以上 Prompt 链接在 V0.1 为规划内容，可能尚未填充。

---

## 练习

1. **故意制造一个 bug**：在 Level 3 的 CRUD 项目里，故意改坏一段代码，然后用 [systematic-debugging](../../skills/core/systematic-debugging/SKILL.md) 的流程排查并修复。
2. **写回归测试**：修完后，用 [write-tests](../../prompts/testing/write-tests.md) 让 AI 帮你写一个测试，覆盖刚修的 bug。
3. **代码审查**：用 [code-review](../../prompts/review/code-review.md) 让 AI 审一遍你的项目代码，看它能不能找出问题。

---

## 项目（小项目建议）

> 在 Level 3 的 CRUD 项目基础上，做一轮完整的"Debug + Test"。

产出：
- 一个被修复的 bug（附复现步骤）
- 对应的回归测试（能跑通）
- 一份代码审查记录（AI 找出的问题 + 你怎么处理的）

---

## 毕业标准（可客观判断）

- [ ] 能说出系统化调试的**至少 5 个步骤**（复现→定位→假设→验证→修复）。
- [ ] 能说清**"AI 说修好了"和"真的修好了"的区别**（验证先行）。
- [ ] **修了一个真实的 bug**，且能复现修复前的错误。
- [ ] **写了对应的回归测试**，且测试**真能跑通**（不是 AI 说"测试通过"就算）。
- [ ] 完成 at least 一次代码审查，有记录。

> 毕业检验：把你的回归测试跑一遍——修复前会失败、修复后会通过。这就是"证据"（Principle 04）。
>
> ⚠️ 注意：本级"测试能跑通"是**学习产出**，需你本地实际运行验证，本仓库未代为验证。
