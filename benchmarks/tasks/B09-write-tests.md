# B09 — 给 note create 接口写 3 条测试用例

> ⚠️ Not Yet Verified — 此任务尚未在真实模型上跑过分。以下所有"Expected / Acceptance / Evaluation"都是对目标行为的**期望定义**，不代表任何模型已经实现或得分。

## Task

给一个已实现且可启动的 `POST /notes`（note create）接口，写 **3 条**自动化测试：**(1) 正常创建成功、(2) 空标题应报错、(3) 超长内容应被截断（按接口约定 10000 字上限）**。要求按「先红后绿」流程写——即先让测试跑失败，再确认接口实现能把它跑绿。

- 先红后绿（大白话解释）：**先写失败的测试（红），再跑实现让测试通过（绿）**——这是保证"测试真的在测东西"的老派技巧，避免你写了一条永远通过的"假测试"。

## Difficulty

**beginner**

## Goal

- 新建文件 `tests/note-create.test.js`；
- 使用 Node.js 20 内置 `node:test` + `node:assert`（不允许装 jest / vitest / mocha 任何新库）；
- 测试启动前会自动跑起真实服务 `node src/index.js`（端口 3001 避免冲突），并在全部测试结束后关闭；
- 3 条测试分别对应：
  1. **T1 正常创建**：`{ title:"A", content:"B" }` → HTTP 201 + 返回体中 id / title / content 正确；
  2. **T2 空标题报错**：`{ title:"", content:"B" }` 以及 `{ content:"B" }`（无 title）→ HTTP 400 + 响应体有 `error` 字段；
  3. **T3 超长内容截断**：`{ title:"L", content:"x".repeat(15000) }` → 实际写入 DB 的 content 长度 = 10000（即接口必须截断，不是直接报错）。
- 断言必须**清晰无硬编码依赖**：比如「返回的 id > 0」就好，不要断言 `id === 1`（这样换个干净 DB 就不用改测试）。

## Input

### 1）项目骨架

```
easyvibe-b09/
├── package.json       ← 已含 better-sqlite3；不装其他测试库
├── schema.sql         ← 同 B01
├── src/
│   └── index.js       ← B01 的通过版本：POST /notes 实现了：
│                      │   • title 非空校验；
│                      │   • content 超过 10000 字符时**截断**再写入（关键！此实现 V0.1 会随任务一起注入）；
│                      │   • 返回体 { id, title, content, created_at, updated_at }。
└── tests/             ← 空目录（你要新建 note-create.test.js）
```

### 2）测试运行约定（Prompt 中注入）

```
> node --test tests/note-create.test.js
- 每条测试内，使用 fetch('http://127.0.0.1:3001/notes', {...}) 发起真实 HTTP 请求；
- 验收端在测试前启动服务：TEST_PORT=3001 TEST_DB=./data/test.db node src/index.js &
- 验收端在每条测试前会清空 notes 表（DELETE FROM notes; DELETE FROM sqlite_sequence WHERE name='notes';），所以测试之间互不影响；
- 测试文件需要：
  - 1) 只 import node:test / node:assert / node:process 三类；
  - 2) 不 import src/index.js（进程隔离地 HTTP 黑盒测）；
  - 3) 不直接连 SQLite；一切断言都通过 HTTP 响应。
```

### 3）约束

- **必须**有 3 条且**恰好 3 条**顶级 `test(...)`：名字必须包含 "正常创建"、"空标题报错"、"超长内容截断" 三串中文子串（否则自动化无法匹配）。
- 每条测试必须有 ≥ 2 个 `assert` 断言；
- 不得出现 `assert.equal(actual_id, 1)` 这种依赖 DB 自增起点的硬编码；
- 不得用 `.skip` / `.todo` 跳过任何一条；
- 测试跑完后 `node --test` 的退出码 = 0。

## Expected Behavior

1. **先红验证（AI 交付前自检用）**：
   - 如果把 `src/index.js` 里的「content 截断」注释掉 → T3 应**失败**（assert 报错：写入的 content 长度是 15000 而不是 10000）；
   - 如果把 title 校验整段删掉 → T2 应**失败**（返回 201 而不是 400）。
   （这证明测试是真的在测事，而不是永远通过。）
2. **后绿验证（正式交付）**：
   - 把接口实现恢复为原版 → 3/3 全通过。
3. **断言风格无硬编码依赖**：
   - 正确断言示例：`assert.ok(result.id > 0 && Number.isInteger(result.id))`
   - 错误断言示例：`assert.strictEqual(result.id, 1)`
4. **测试隔离**：
   - 连续跑 3 次 `node --test tests/note-create.test.js`，每次 T1 都能通过（不会因为"id 不再是 1"而失败）。

## Acceptance Criteria

| # | 验收项 | 对应维度 |
|:---:|:---|:---|
| AC-1 | 文件 `tests/note-create.test.js` 存在，只 import node:test / node:assert / node:process，不直接连 DB | Code Quality + Test Pass Rate |
| AC-2 | 测试名 grep：文件内同时出现「正常创建」「空标题报错」「超长内容截断」3 个中文串，各只出现一次在顶级 `test(...)` 名里 | Correctness（要求 3 条且仅 3 条） |
| AC-3 | T1 正常创建：HTTP 201 + body 有 id/title/content 正确 + id > 0；且「title === "A" && content === "B"」。跑原版接口时通过 | Test Pass Rate |
| AC-4 | T2 空标题：同时测 `{"title":"",...}` 与 `{无title}` 两个子用例（`test('空标题报错', async t => { await t.test(...); await t.test(...);})`），两者都返回 400 + 含 error 字段 | Test Pass Rate |
| AC-5 | T3 超长内容：发送 content 长度 15000，接口返回 201；再 `GET /notes/:id` 验证 content.length === 10000（**截断**，不是报错） | Test Pass Rate |
| AC-6 | 每条测试内 `assert.*` 调用次数 ≥ 2（避免一条测试只有一个 assert 显得太浅）| Code Quality |
| AC-7 | 先红验证（验收端注入坏版本 1：无 title 校验）→ T2 必须 FAIL；坏版本 2：无 content 截断 → T3 必须 FAIL | Correctness（测试保真）|
| AC-8 | 无硬编码：grep 测试文件，`strictEqual.*result\.id,\s*(\d+)`（把 id 断言为具体数字）命中 0 次 | Code Quality（可移植性）|
| AC-9 | 连跑 3 次全部通过，flakiness（偶尔失败）= 0 | Maintainability / Test Pass Rate |

## Evaluation

满分 100 分：

| AC | 小分 | 归属维度 |
|:---:|:---:|:---|
| AC-1 | 5  | Code Quality / 结构 |
| AC-2 | 5  | Correctness（必须恰好 3 条） |
| AC-3 | 20 | Test Pass Rate（T1） |
| AC-4 | 25 | Test Pass Rate（T2 双子用例） |
| AC-5 | 20 | Test Pass Rate（T3） |
| AC-6 | 5  | Code Quality（断言密度） |
| AC-7 | 10 | Correctness（测试保真） |
| AC-8 | 5  | Code Quality（无硬编码） |
| AC-9 | 5  | Maintainability / 稳定性 |

## Scoring Tie-in

| scoring 维度 | 本任务怎么评 |
|:---|:---|
| Correctness        | 3 条测试本身"测到了东西"：先红后绿、名字对、覆盖三条路径（AC-2/7） |
| Test Pass Rate     | 在正确接口实现下 3 条全绿；在 2 个坏版本下对应条红（通过率 = 真测到） |
| Code Quality       | AC-1/6/8：结构清晰、断言够多、无硬编码；测试命名是否能直接当文档看 |
| Security           | 此任务不重点考，若测试泄漏 secret 会扣分 |
| Maintainability    | AC-9（flaky=0）+ 子用例结构是否清楚（失败了能不能一眼知道是缺 title 还是空 title） |
| Token Usage / Latency / Human Intervention | scoring.md 通用定义；本任务为 beginner，Human 1 次纠偏为 7-8 分线 |
