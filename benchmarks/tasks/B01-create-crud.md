# B01 — 为 notes 表实现 CRUD 接口

> ⚠️ Not Yet Verified — 此任务尚未在真实模型上跑过分。以下所有"Expected / Acceptance / Evaluation"都是对目标行为的**期望定义**，不代表任何模型已经实现或得分。

## Task

在一个空的 Node.js + SQLite 项目里，给 `notes`（笔记）表实现 **4 个 REST CRUD 接口**：Create（新建）、Read（查一条 + 查列表）、Update（改一条）、Delete（删一条）。

- CRUD（大白话解释）：**增(Create) 查(Read) 改(Update) 删(Delete)** 的首字母缩写，是后端最基本的 4 个操作。
- REST（大白话解释）：**一种大家约定俗成的写 HTTP 接口的风格**，比如创建用 `POST /notes`、查询用 `GET /notes`。

## Difficulty

**beginner**

## Goal

启动项目后：

- 有一个监听在 `3000` 端口的 HTTP 服务；
- 4 条路由全部可用，返回正确 HTTP 状态码与 JSON；
- 所有对 SQLite 的写入操作都**使用参数化查询**（防 SQL 注入）；
- 对明显错误输入（空标题、超长内容、非数字 id）返回 4xx 错误而不是 5xx 崩溃。

## Input

### 1）项目骨架（V0.1 作为 Prompt 原样注入）

```
easyvibe-b01/
├── package.json          ← 已存在，含 { "name": "b01", "dependencies": { "better-sqlite3": "^11" } }
├── schema.sql            ← 已存在（见下方）
├── src/
│   └── index.js          ← 已存在，只有一句：console.log('TODO');
└── README.md             ← 已存在，写着"运行命令：node src/index.js"
```

### 2）schema.sql（原样注入内容）

```sql
CREATE TABLE IF NOT EXISTS notes (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  title      TEXT    NOT NULL,
  content    TEXT    NOT NULL DEFAULT '',
  created_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
  updated_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);
```

### 3）约束

- 只能用 Node 20 LTS 内置的 `http` 模块 + `better-sqlite3`；
- 不允许安装 Express / Koa / Fastify 等任何额外框架；
- 数据库文件固定写到 `./data/app.db`（若目录不存在请创建）；
- 数据交换统一用 JSON；
- 代码放 `src/index.js`，可拆分 `src/db.js`，但不要超过 3 个 JS 文件。

## Expected Behavior

1. **启动即建表**：`node src/index.js` 后，如果 DB 不存在就自动执行 `schema.sql`，然后监听 3000 端口并打印 `Listening on 3000`。
2. **POST /notes**：请求体 `{ title, content }` → 写入一条新记录，返回 `201 Created` + 新记录完整 JSON（含自增 id）。
3. **GET /notes**：返回 `200` + 数组（按 id 倒序，最多 100 条）。
4. **GET /notes/:id**：返回 `200` + 单条对象；若 id 不存在 → 返回 `404` + `{ "error": "Not Found" }`。
5. **PATCH /notes/:id**：请求体 `{ title?, content? }`（只传要改的字段），更新记录并把 `updated_at` 改成当前时间戳，返回 `200` + 更新后的记录；id 不存在 → `404`。
6. **DELETE /notes/:id**：删除记录，返回 `204 No Content`（无响应体）；id 不存在 → `404`。
7. **错误输入处理**：
   - `POST /notes` 时 `title` 为空 / 缺失 → `400` + 错误信息；
   - `title` 超过 200 字符 / `content` 超过 10000 字符 → `400` + 错误信息；
   - `:id` 不是正整数（比如 `/notes/abc`）→ `400` 直接拒绝，不进入 SQL 查询。

## Acceptance Criteria

验收脚本对每条 AC 输出 pass / fail：

| # | 验收项（可自动化） | 对应维度（见 scoring.md） |
|:---:|:---|:---|
| AC-1 | `node src/index.js` 启动成功，10s 内 `Listening on 3000` 出现在 stdout，且端口可连接 | Correctness |
| AC-2 | `POST /notes { "title":"t","content":"c" }` 返回 201 + 含 `id`/`title`/`content`/`created_at`/`updated_at` 的 JSON | Correctness |
| AC-3 | 连续创建 2 条，`GET /notes` 返回 200 + 长度 2 数组，按 id 倒序排列 | Correctness |
| AC-4 | `GET /notes/1` 返回 200 + id=1 的记录；`GET /notes/9999` 返回 404 + error 字段 | Correctness |
| AC-5 | `PATCH /notes/1 { "title":"new" }` 返回 200，`title` 已变且 `updated_at` ≥ 原 `updated_at`；id=9999 patch 返回 404 | Correctness |
| AC-6 | `DELETE /notes/1` 返回 204；再次 GET /notes/1 返回 404 | Correctness |
| AC-7 | 所有 SQL 读写（含 WHERE id = ?）**全部为参数化查询**：AST 扫描 `better-sqlite3` 的 `.prepare().run/get/all(...)` 调用，参数全部通过数组/对象占位符传入，0 次字符串拼接。 | Security |
| AC-8 | SQL 注入 payload：`POST /notes { "title":"x','y'); DROP TABLE notes; --" }` 执行后 `notes` 表仍存在、记录仅新增一条（title 就是整段字符串） | Security |
| AC-9 | `POST /notes { "title":"" }` → 400；`POST /notes {}` → 400；`POST /notes { "title":"x".repeat(201) }` → 400（实际使用等价 JSON 字符串） | Correctness / Code Quality |
| AC-10 | `GET /notes/abc`、`PATCH /notes/-1 {}`、`DELETE /notes/0` → 全部 400、不触发 SQL、不抛 500 | Correctness / Security |
| AC-11 | 整个验收过程 stdout/stderr 没有出现 uncaught exception 或未处理的 promise rejection | Code Quality / Maintainability |

## Evaluation（每项 AC 对应分值 → 维度）

满分 100 分（再按维度映射到 0-10 分）：

| AC | 小分 | 归属维度 |
|:---:|:---:|:---|
| AC-1 | 5 | Correctness |
| AC-2 | 10 | Correctness |
| AC-3 | 10 | Correctness |
| AC-4 | 10 | Correctness |
| AC-5 | 10 | Correctness |
| AC-6 | 10 | Correctness |
| AC-7 | 15 | Security |
| AC-8 | 10 | Security |
| AC-9 | 10 | Correctness |
| AC-10 | 5 | Correctness + Security |
| AC-11 | 5 | Code Quality |

维度折合方式：

- Correctness = (AC-1~6 + AC-9 + AC-10 半 + AC-11 半) / 65 × 10
- Security    = (AC-7 + AC-8 + AC-10 半) / 30 × 10
- Code Quality / Maintainability / Test Pass Rate / Token / Latency / Human = 按 scoring.md 通用定义打分。

## Scoring Tie-in（引用 scoring.md 的维度）

本任务打分与 [../scoring.md](../scoring.md) 的对应关系：

| scoring 维度 | 本任务里怎么评 |
|:---|:---|
| Correctness        | AC-1~6 + AC-9~10 的功能正确性（占本任务主要分） |
| Test Pass Rate     | 验收脚本 AC-1~11 的通过率 |
| Code Quality       | AC-11（无崩溃）+ 人工读代码看命名/路由结构/重复代码 |
| Security           | AC-7（参数化查询）+ AC-8（SQLi 实打）+ AC-10（非数字 id 不入 SQL） |
| Maintainability    | 是否把 DB 初始化/路由/校验分函数；是否 100+ 行的大函数堆在一处 |
| Token Usage        | 实际完成任务消耗 Prompt+Completion Token / 基准线 |
| Latency            | 从发 Prompt 到全部 AC 通过的墙钟时间 |
| Human Intervention | 过程中人类纠偏次数 |
