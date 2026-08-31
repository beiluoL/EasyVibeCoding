# B02 — 修复「保存笔记后列表不刷新」的运行时 Bug

> ⚠️ Not Yet Verified — 此任务尚未在真实模型上跑过分。以下所有"Expected / Acceptance / Evaluation"都是对目标行为的**期望定义**，不代表任何模型已经实现或得分。

## Task

拿到一段可启动的 Node 后端代码（含一个已知 Bug），要求：**定位根因、做最小修复、并补一条回归测试**，确保"保存笔记后列表不刷新"的问题消失，同时原有 4 条 CRUD 测试全部继续通过。

- 运行时 Bug（大白话解释）：**代码能跑起来，但做某个操作时结果不符合预期**——它不会一启动就炸，而是在你点"保存"之后才坏。

## Difficulty

**intermediate**

## Goal

- 在 1 小时内（参考时间）定位 Bug 的根本原因；
- 修复的代码改动 ≤ 3 行（"最小修复"定义）；
- 验收时：Bug 复现脚本从 fail → pass；原有 CRUD 回归测试 4/4 全绿；
- 在 `REASON.md` 里用 ≤ 100 字说明根因（比如"保存后 DB 已更新但读的是内存缓存数组且未同步"）。

## Input

### 1）项目骨架（Prompt 原样注入）

```
easyvibe-b02/
├── package.json        ← 含 better-sqlite3、node:test（Node 20 内置）
├── schema.sql          ← 同 B01
├── src/
│   ├── index.js        ← HTTP 服务入口（含 Bug）
│   └── db.js           ← DB 封装
├── tests/
│   └── crud.test.js    ← 原有 4 条 CRUD 测试（启动前全部通过）
└── REASON.md           ← 空文件，要求填根因
```

### 2）Bug 代码关键片段（原样注入）

```js
// src/index.js — 已存在且启动无报错
import { db } from './db.js';

// ❗启动时一次性读进内存数组，之后再也没更新过
let notesCache = db.prepare('SELECT * FROM notes ORDER BY id DESC').all();

const app = async (req, res) => {
  if (req.method === 'GET' && req.url === '/notes') {
    res.json(notesCache);     // ← 直接返回启动时的快照
    return;
  }
  if (req.method === 'POST' && req.url === '/notes') {
    const body = await parseJSON(req);
    const info = db.prepare('INSERT INTO notes (title, content) VALUES (?, ?)')
      .run(body.title, body.content);
    res.statusCode = 201;
    res.json({ id: info.lastInsertRowid, ...body });
    // ❌ Bug：写入 DB 后没有更新 notesCache
    return;
  }
  // ... PATCH / DELETE 也只写 DB，没更新 notesCache（略）
};
```

### 3）复现步骤（原样注入，验收脚本会按此跑）

```
1. node src/index.js &
2. curl -X POST /notes -d '{"title":"A","content":"a"}' → 201
3. curl -X GET  /notes                                 → 期望看到 A；Bug 版本返回 []（空）
4. curl -X POST /notes -d '{"title":"B","content":"b"}' → 201
5. curl -X GET  /notes                                 → 期望看到 B,A；Bug 版本仍返回 []
```

### 4）约束

- 不允许更换 `better-sqlite3`、不允许引入 Redis 等新依赖；
- "最小修复" = 删掉/新增/修改 ≤ 3 行代码；
- 新增的回归测试写到 `tests/regression-B02.test.js`，使用 Node 内置 `node:test` + `assert`；
- `REASON.md` 只用中文，≤ 100 字，一句话说根因 + 一句话说怎么修。

## Expected Behavior

1. 修复后按"复现步骤"重跑：Step 3 返回 `[A]`、Step 5 返回 `[B,A]`；
2. 原有 `tests/crud.test.js` 4 条断言仍全部通过；
3. 新写的回归测试：先创建 → 立刻 list → 断言 list 长度正确；先 patch → 立刻 list → 断言 title 已变；先 delete → 立刻 list → 断言该 id 不存在；
4. `REASON.md` 内容与修复代码**相互对应**（不会出现说的是 A 修的却是 B）。

## Acceptance Criteria

| # | 验收项 | 对应维度 |
|:---:|:---|:---|
| AC-1 | 复现脚本 Step 3、Step 5 从 fail → pass（列表真的刷新了） | Correctness |
| AC-2 | `node --test tests/crud.test.js` 4/4 通过（无回归） | Test Pass Rate |
| AC-3 | `node --test tests/regression-B02.test.js` 中"create+list / patch+list / delete+list"3 条子用例全过 | Test Pass Rate |
| AC-4 | `git diff`（模拟：对比 Input 版本 src/*.js 与修复版本 src/*.js）的增删改行数 ≤ 3 行 | Code Quality / Maintainability |
| AC-5 | `REASON.md` 字数 ≤ 100 字，且同时包含"缓存"或 `notesCache` 字样 + 描述"写入后未同步"的语义 | Correctness（分析） |
| AC-6 | 修复后再执行 10 次"POST → GET"循环，10 次都看到新笔记（无偶发性） | Correctness |
| AC-7 | 测试前先 `POST { title:"" }` → GET 不会把空标题这条"非法记录"混进 list（沿用 B01 输入校验要求，原已实现则保持） | Correctness / Security |

## Evaluation

满分 100 分：

| AC | 小分 | 归属维度 |
|:---:|:---:|:---|
| AC-1 | 30 | Correctness |
| AC-2 | 15 | Test Pass Rate |
| AC-3 | 25 | Test Pass Rate |
| AC-4 | 10 | Code Quality / Maintainability |
| AC-5 | 10 | Correctness（根因分析质量） |
| AC-6 | 5  | Correctness |
| AC-7 | 5  | Correctness / Security |

维度折合：按 scoring.md 的 0-10 映射：
- Correctness = (AC-1 + AC-5 + AC-6 + AC-7·半) / 50 × 10
- Test Pass Rate = (AC-2 + AC-3) / 40 × 10
- 其余维度按 scoring.md 通用规则。

## Scoring Tie-in

| scoring 维度 | 本任务怎么评 |
|:---|:---|
| Correctness        | Bug 真的修好 + 根因写对 + 10 次循环不出错（AC-1/5/6/7） |
| Test Pass Rate     | 老 4 条过（回归）+ 新 3 条过（针对性） |
| Code Quality       | AC-4 的「≤ 3 行最小修复」——大动干戈扣分 |
| Security           | AC-7 沿用输入校验（别修 Bug 顺便把校验删了） |
| Maintainability    | 修复方式是否可读；是否留下 TODO/注释说明 notesCache 的使用边界 |
| Token Usage / Latency / Human Intervention | 按 scoring.md 通用定义 |
