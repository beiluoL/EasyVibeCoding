---
name: code-review
description: 用结构化清单评审 AI 生成的代码：正确性/安全/可维护/可读，而不是"看起来没问题"。
version: 0.1.0
category: core
difficulty: intermediate
status: experimental
verified: false
compatible: [unspecified]
prerequisites:
  - 待评审的代码已实现完成
  - 验收标准已知
inputs:
  - 待评审代码
  - 验收标准
outputs:
  - 结构化评审报告（问题分级 + 位置 + 理由 + 建议）
triggers:
  - AI 生成代码后需要评审
  - 功能实现完成准备合并前
  - 需要确认代码安全性和正确性
validation:
  - 每条问题有位置、理由、建议
  - blocker 级问题必须修复才能通过
  - 安全项零遗漏
last_verified: null
---

# Code Review（结构化代码评审）

> ⚠️ Not Yet Verified

## Purpose

用**结构化清单**评审 AI 生成的代码，逐项检查正确性、安全、可维护、可读，而不是看一眼觉得"好像没问题"就放行。

AI 写的代码看起来通顺，但常藏隐患：拼 SQL、硬编码密钥、没处理错误。不逐项过就会漏。

## When to Use

- AI 生成了一段代码，准备用它之前。
- 功能实现完成，准备合并到主分支前。
- 对代码安全性不确定，需要系统检查。

## Trigger Conditions

- AI 产出了新代码 / 改动，需要评审。
- 用户问"这段代码有没有问题 / 能不能用"。
- implementation 流程结束后、verification 之前。

## Preconditions

1. 待评审代码已完成（至少能跑）。
2. 验收标准已知（否则无法判断"是否满足需求"）。
3. 评审者能看懂代码所在语言。

## Workflow

1. **对清单逐项过**：按下方清单，一项一项检查，不跳过。
2. **标问题等级**：
   - **blocker**：必须改，不改不能用（安全漏洞、逻辑错误、会导致崩溃）。
   - **warn**：建议改，不改能跑但有隐患（可维护性、重复代码）。
   - **nit**：可选改，锦上添花（命名、格式）。
3. **每条给位置 + 理由 + 建议**：光说"有问题"没用，要说清在哪一行、为什么是问题、怎么改。
4. **区分"必须改"与"可选"**：blocker 全改完才能放行；warn 和 nit 记录但不阻塞。

## 评审清单

每项都要过一遍：

**正确性**
- [ ] 是否满足验收标准（功能对不对）
- [ ] 是否有未处理的错误（空值、异常、失败分支）

**安全**
- [ ] 是否有硬编码密钥 / 密码 / 路径
- [ ] 是否有 SQL 注入风险（拼接 SQL 而非参数化）
- [ ] 是否有 XSS 风险（未转义的用户输入直接输出）

**可维护**
- [ ] 是否有重复代码（可提取复用）
- [ ] 是否过度设计（简单功能写了复杂抽象）

**可读**
- [ ] 命名是否清楚（变量名能看懂意图）
- [ ] 逻辑是否直观（不需要猜才能懂）

**测试**
- [ ] 是否需要补测试（关键路径有没有覆盖）

## Rules

- 清单逐项过，不跳过安全项。
- 每条问题必须给位置 + 理由 + 建议，三件套缺一不可。
- blocker 不修不放行。
- 评审关注逻辑和安全隐患，不只是格式。

## Anti-Patterns

- ❌ "代码没问题"式评审——等于没评审。
- ❌ 只看格式不看逻辑——格式整齐不代表逻辑对。
- ❌ 忘记查安全——SQL 注入、硬编码密钥最容易漏。
- ❌ 问题只说"有问题"不说怎么改——没建议的评审没用。

## Validation

> 本技能 V0.1 新写，尚未经实际运行验证。

**Expected Validation Steps**：
1. 用本清单评审 3 段 AI 生成代码（含已知问题）。
2. 检查是否能找出预设的安全漏洞和逻辑错误。
3. 检查每条问题是否含位置+理由+建议。
4. 收集至少 2 个真实使用案例后，更新 verified 与 last_verified 字段。

验证状态：⚠️ Not Yet Verified — 待按 Expected Validation Steps 实际运行后更新。

## Output Format

```
评审对象：<文件/功能>
清单结果：逐项 ✅/❌
问题列表：
  [blocker] <位置> — <理由> → <建议>
  [warn]    <位置> — <理由> → <建议>
  [nit]     <位置> — <理由> → <建议>
结论：<blocker 全清可放行 / 仍有 blocker 待修>
```

## Example

评审一段有 SQL 拼接漏洞的 AI 生成代码。

待评审代码：

```js
router.post('/api/notes', async (req, res) => {
  const { title, content } = req.body;
  const sql = "INSERT INTO notes (title, content) VALUES ('" + title + "','" + content + "')";
  await db.query(sql);
  res.status(201).json({ ok: true });
});
```

清单结果与问题：

```
评审对象：src/routes/notes.js POST /api/notes
清单结果：
  满足验收标准：❌（未返回新笔记数据）
  未处理错误：❌（无 try/catch，db 失败会崩）
  硬编码密钥/路径：✅
  SQL注入风险：❌（拼接 SQL）
  XSS风险：✅
  重复代码：✅
  命名清楚：✅
  需要测试：❌（关键路径无测试）

问题列表：
  [blocker] db.query 拼接 title/content — 直接拼接用户输入到 SQL，
            有 SQL 注入风险（用户输入 ' OR 1=1 -- 即可攻击）
            → 改用参数化查询：db.query('INSERT INTO notes (title, content) VALUES (?, ?)', [title, content])
  [blocker] 无错误处理 — db.query 失败时整个请求挂掉，无错误响应
            → 包 try/catch，失败返回 500
  [warn]    未返回新笔记数据 — 验收标准要求返回 201 + 笔记
            → 返回插入后的笔记数据
  [warn]    未校验空 title — 验收标准要求空 title 返回 400
            → 加空值校验
  [nit]     用 INSERT 后可取插入 id —
            → 返回 insertId 以便前端使用

结论：2 个 blocker 待修，不放行。修完 SQL 注入和错误处理后再评审。
```
