# B08 — 把 150 行大函数拆成三个职责清晰的小函数

> ⚠️ Not Yet Verified — 此任务尚未在真实模型上跑过分。以下所有"Expected / Acceptance / Evaluation"都是对目标行为的**期望定义**，不代表任何模型已经实现或得分。

## Task

拿到一段「单块大函数」代码（一个函数做了三件事：读 DB → 业务处理 → 返回 JSON），要求**重构**为三个职责清晰的小函数，保持行为 100% 一致（同输入 → 同输出），**不引入任何新依赖**，并让圈复杂度下降。

- 圈复杂度（大白话解释）：**函数里有多少条"如果/那么/否则/循环"岔路口**，数字越多表示函数越难读、越容易出 Bug。一个函数圈复杂度最好 ≤ 10。
- 重构（大白话解释）：**改代码的内部结构，但对外行为完全不变**——就像把一本书重新排版、分章节，但内容一字不差。

## Difficulty

**intermediate**

## Goal

- 原大函数 `getNotesReport(userId)`（150 行）拆为：
  1. `loadUserNotes(userId)` — 只负责读 DB + 返回行数组；
  2. `buildReport(rows)` — 纯函数：从行数组算出统计 { total, done, doing, todo, byDay, topTags }；
  3. `formatResponse(report, userId)` — 纯函数：把统计包装成前端要的 JSON 结构（含 code/msg/data/ts 4 个固定键）；
  4. 顶层 `getNotesReport(userId)` 只做一件事：依次调用 1 → 2 → 3，并做错误包装；
- 重构前后，**对 100 组固定 userId 输入**，响应 JSON **深相等**（字节级允许 `ts` 字段相同秒内一致，其他字段完全一致）；
- 圈复杂度：
  - 原函数 `getNotesReport` 复杂度（目标 ≥ 18 的基线）；
  - 重构后**每个子函数 ≤ 8**，且**整体总和**仍 ≤ 原函数（不许把复杂度"藏进新的 if 嵌套"）；
- 不引入新 npm 包、不新增文件（只改 `src/report.js` 单文件）。

## Input

### 1）项目骨架

```
easyvibe-b08/
├── package.json      ← 仅含 better-sqlite3；devDependency: complexity-report（验收脚本测圈复杂度）
├── schema.sql        ← notes + note_tags 两张表（B01 基础上多了 note_tags）
├── src/
│   └── report.js     ← 只有一个文件，里面有 150 行大函数 getNotesReport(userId)
├── tests/
│   ├── fixtures.sql  ← 注入 100 个 userId 各 10~50 条 notes（总量约 3000 行）
│   └── before.json   ← 重构前用原版 report.js 跑 100 个 userId 得到的快照（验收端提供基线）
```

### 2）大函数关键结构（注入）

```js
// src/report.js —— 150 行单体（示意结构，不是全部代码）
export function getNotesReport(userId) {
  // ---------- 第 1 部分：读 DB（约 30 行，含 if/else 参数拼装 SQL）----------
  if (!userId || typeof userId !== 'string') {
    throw new Error('bad user id');
  }
  const rows1 = db.prepare(`SELECT ... FROM notes WHERE user_id = ? ... AND status IN (...)`).all(userId);
  const rows2 = db.prepare(`SELECT tag FROM note_tags WHERE note_id IN (SELECT id FROM notes WHERE user_id = ?)`).all(userId);
  // ... 中间有 3 处 if 分支拼接不同 WHERE（status 过滤、due_date 范围、是否含归档）

  // ---------- 第 2 部分：业务处理（约 80 行，大量 for/if）----------
  const result = { total:0, done:0, doing:0, todo:0, byDay:{}, topTags:[] };
  for (const r of rows1) {
    result.total++;
    if (r.status === 'done') { result.done++; if (r.due_date) { ... } }
    else if (r.status === 'doing') { result.doing++; ... }
    else { ... }
    const day = r.created_at_day();
    if (!result.byDay[day]) result.byDay[day] = 0;
    result.byDay[day]++;
    // ... topTags 处理：二重循环 20 行
  }
  // ... 末尾还有一个 10 行的 "byDay 取最近 7 天补 0" 循环

  // ---------- 第 3 部分：返回 JSON 包装（约 40 行）----------
  const data = {};
  if (result.total === 0) { data.message = '空'; data.empty = true; ... }
  data.summary = { total, done, doing, todo };
  data.chart = Object.entries(result.byDay).sort(...);
  data.topTags = result.topTags.slice(0, 5).map(...);
  return {
    code: 0,
    msg: 'ok',
    data,
    ts: Date.now(),
  };
}
```

关键：**Input 里给的是完整 150 行真实代码**（上面只是结构说明，真跑时给全量）。

### 3）约束

- 不能新增任何 `import` / `require`（`new` 包算作弊）；
- 不能改动 `package.json`、`schema.sql`、`tests/`；
- 函数拆分必须按名字拆分（验收脚本会直接按名字 `import` 那 4 个函数做单测）；
- `buildReport` 与 `formatResponse` 必须是 **纯函数**（内部不允许访问 `db` / `Date.now()` / `Math.random()` 等带副作用 API）。

## Expected Behavior

1. **行为等价**：运行验收脚本 `node tests/equivalence.js`，对 100 个 userId 的输出：
   - `code`、`msg`、`data` 字段 与 `tests/before.json` **深相等**；
   - `ts` 字段在同一秒内（误差 < 1000ms）视为一致；
   - 失败 0 个即通过。
2. **职责单一**（静态 + 动态验证）：
   - `loadUserNotes(userId)` 函数体内出现 `db.prepare` 次数 ≥ 1；
   - `loadUserNotes` 体内**不允许**出现 `byDay` / `topTags` / `code:0` 等处理/包装关键词；
   - `buildReport(rows)` 体内不允许 `db.prepare` / `process.env` / `Date.now()`；
   - `formatResponse(report, userId)` 体内不允许 `db.prepare` / `Date.now()`（ts 从外部传或让顶层加）。
3. **圈复杂度下降**：
   - 重构后 4 个函数各自 complexity ≤ 8；
   - 4 个函数复杂度之和 ≤ 原函数复杂度（防止"把 if 搬到新函数里凑拆分"）。
4. **无新依赖**：`package.json` 指纹与原指纹一致（字节级相同）。

## Acceptance Criteria

| # | 验收项 | 对应维度 |
|:---:|:---|:---|
| AC-1 | 行为等价 100/100 通过（`data` 字段完全相同） | Correctness |
| AC-2 | 4 个函数名字都存在并可 `import` 分别调用；参数个数符合 Input（load:1 / build:1 / format:2 / top:1）| Maintainability |
| AC-3 | 职责隔离静态扫描：`loadUserNotes` 不含 `topTags/code:`；`buildReport` 不含 `db/process.env/Date.now`；`formatResponse` 不含 `db` | Code Quality + Maintainability |
| AC-4 | 圈复杂度：4 个子函数 max ≤ 8，sum ≤ 原版 complexity（原版基线固定 22）| Maintainability |
| AC-5 | 纯函数验证：给 `buildReport` 喂假 rows（不连 DB）能算出正确统计；10 次同输入输出完全一致（无随机性）| Code Quality（纯函数）|
| AC-6 | 纯函数验证：给 `formatResponse` 喂假 report，输出 JSON 结构严格 `{code,msg,data}`，不含多余字段 | Code Quality |
| AC-7 | 无新依赖：`package.json` diff 空；`report.js` 新 import 0 个 | Maintainability |
| AC-8 | 错误输入等价：`getNotesReport('')`、`getNotesReport(null)`、`getNotesReport(42)` 抛错 message 与原版完全一致 | Correctness（边界回归）|

## Evaluation

满分 100 分：

| AC | 小分 | 归属维度 |
|:---:|:---:|:---|
| AC-1 | 30 | Correctness（最核心：同输入→同输出） |
| AC-2 | 10 | Maintainability |
| AC-3 | 15 | Code Quality + Maintainability |
| AC-4 | 15 | Maintainability |
| AC-5 | 10 | Code Quality（纯函数 buildReport） |
| AC-6 | 5  | Code Quality（纯函数 formatResponse） |
| AC-7 | 5  | Maintainability（无新依赖） |
| AC-8 | 10 | Correctness（边界回归） |

## Scoring Tie-in

| scoring 维度 | 本任务怎么评 |
|:---|:---|
| Correctness        | AC-1 + AC-8：重构绝对不能"看似对了实则改了行为" |
| Test Pass Rate     | 8 条 AC；AI 自写纯函数单测（buildReport 的各分支）也纳入 |
| Code Quality       | AC-3/5/6：职责是否真的单一、是否真纯函数；命名/注释是否到位 |
| Security           | 不引入新包 → 无新供应链风险；其他不重点考察本任务 |
| Maintainability    | AC-2/4/7：拆分后复杂度 + 函数边界 + 不引入依赖 |
| Token / Latency    | 本任务 Token 主要省在"理解并改更少的代码"；Latency 看运行 100 个用例耗时（应与原版相当或更快） |
| Human Intervention | 典型误区：改功能、多拆或少拆函数、buildReport 不纯，纠偏 2 次为 5-6 分线 |
