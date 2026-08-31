# B03 — 给 CRUD 加 Redis 缓存层

> ⚠️ Not Yet Verified — 此任务尚未在真实模型上跑过分。以下所有"Expected / Acceptance / Evaluation"都是对目标行为的**期望定义**，不代表任何模型已经实现或得分。

## Task

在一个**已经通过 B01** 的 Node+SQLite CRUD 项目基础上，给读接口加 **Redis 缓存层**：热点查询（`GET /notes/:id`）命中缓存时不查 SQLite；写入（POST/PATCH/DELETE）时主动让相关缓存失效（Cache Invalidation）。

- Redis（大白话解释）：**一个存在内存里的超高速键值对数据库**，常用作"缓存"——把热点数据放这里，免得每次都去查慢很多的硬盘数据库 SQLite。
- 缓存失效（大白话解释）：**数据被改了之后，把旧缓存删掉**，下次读就会去查最新的 SQLite 数据再放回缓存，避免"读到旧数据"。

## Difficulty

**intermediate**

## Goal

- `GET /notes/:id` 在命中缓存时 **0 次 SQLite 查询**；
- 对同一条 id 连续 2 次 `GET`，SQLite "SELECT ... WHERE id=?" 只执行 **1 次**（第 2 次命中缓存）；
- `POST` / `PATCH /notes/:id` / `DELETE /notes/:id` 后，对应缓存键**立即失效**：下一次 GET 必须重新查 SQLite；
- 缓存统一设置 **TTL = 60 秒**（防止孤儿缓存长期占用内存）；
- Redis 挂掉时服务**不崩溃**，自动降级为直连 SQLite（优雅降级）。

## Input

### 1）项目骨架

```
easyvibe-b03/
├── package.json      ← 已含 better-sqlite3@11、ioredis@5（只许用 ioredis，不要装别的 redis client）
├── schema.sql        ← 同 B01
├── src/
│   ├── index.js      ← B01 正确版本（所有 CRUD 接口已通过，可直接用）
│   ├── db.js         ← 导出 db 对象 + 一个事件发射器，每次 SQL 执行会 emit('sql', sql, params)
│   └── cache.js      ← 空文件（推荐把 Redis 封装写这里，也可以不建）
└── tests/
    └── crud.test.js  ← B01 的 4 条基础测试（要求仍通过）
```

### 2）db.js 能力（原样注入，关键）

```js
// 验收脚本会通过 db.on('sql', ...) 监听每次 SQL 执行次数
import { EventEmitter } from 'node:events';
import Database from 'better-sqlite3';
export const ee = new EventEmitter();
export const db = new Database('./data/app.db');
// 已通过 monkey-patch 让每次 prepare(...).run/get/all 调用前 ee.emit('sql', sql, params);
```

### 3）运行环境假设（验收端准备）

- 机器上 **Docker 里起一个 Redis 7**，`redis://localhost:6379/0` 可连；
- 同时提供一个**可切换的假 Redis 端口**（连不上）用来测"优雅降级"；
- 通过环境变量 `REDIS_URL` 传给服务。

### 4）约束

- 缓存粒度：**单条 id**（键 = `note:${id}`，值 = 记录 JSON）；不要缓存 `GET /notes` 列表（防止一致性复杂）。
- TTL 固定 60 秒。
- 不允许把写入先写 Redis 再异步刷 DB（write-back 太复杂，只做 cache-aside pattern = 读时补缓存、写时删缓存）。
- 代码改动不得破坏 B01 既有的输入校验与 SQL 注入防护。

## Expected Behavior

1. 启动服务 → `POST /notes {title:"A"}` 得到 `id=1`。
2. 第 1 次 `GET /notes/1`：
   - 命中 SQLite **1 次** `SELECT * FROM notes WHERE id = 1`；
   - 返回 200 + 记录 A；
   - Redis 里出现键 `note:1`，TTL 介于 59~60s。
3. 第 2 次 `GET /notes/1`：
   - SQLite `SELECT WHERE id=1` 次数**不再增加**（仍是 1）；
   - 返回 200 + 同样的记录 A。
4. `PATCH /notes/1 {title:"A2"}`：
   - 返回 200 + 新 title；
   - Redis 键 `note:1` 立刻消失。
5. 第 3 次 `GET /notes/1`：
   - SQLite SELECT 次数**再 +1**（从 1 → 2）；
   - 返回 title="A2" 的最新记录。
6. 设 `REDIS_URL=redis://localhost:1`（故意错）：服务仍能启动，POST/GET/PATCH/DELETE 全可用（降级直查 DB），不抛未捕获异常。
7. B01 原有 `crud.test.js` 4/4 仍通过。

## Acceptance Criteria

| # | 验收项 | 对应维度 |
|:---:|:---|:---|
| AC-1 | Expected Behavior 步骤 1~3：2 次 GET /notes/1 间，SQLite SELECT WHERE id=1 计数 = 1 | Correctness |
| AC-2 | 第 2 次 GET /notes/1 的响应 body 与第 1 次 JSON 深相等 | Correctness |
| AC-3 | PATCH/DELETE 对应 id 后，再 GET 该 id 时 SELECT 计数正确 +1（缓存失效生效） | Correctness |
| AC-4 | PATCH id=1 后，GET id=2 的缓存不受影响（不会把整个缓存全清掉） | Correctness / Code Quality |
| AC-5 | Redis 键 TTL 在写入后 ≤ 60s 且 ≥ 58s（有 2s 容忍） | Correctness |
| AC-6 | `REDIS_URL` 错端口 → 服务启动不崩溃、POST/GET 正常、无 Uncaught Exception | Maintainability / Code Quality |
| AC-7 | B01 crud.test.js 4/4 通过（无回归） | Test Pass Rate |
| AC-8 | B01 所有 Security AC（参数化查询 / SQLi payload）仍通过 | Security |
| AC-9 | `POST /notes {title:"x'+(sleep 5)+'"}` 类 payload 时，不会因为缓存键拼法出漏洞（比如拼接成 `note:1 OR 1=1`）——实际上 id 是整数路径参数，这里用 AC-10 保证 | Security |
| AC-10 | 对路径 `/notes/abc OR 1=1`，仍先返回 400（校验在前），不会拼入 Redis 键 / SQL | Security / Correctness |

## Evaluation

满分 100 分：

| AC | 小分 | 归属维度 |
|:---:|:---:|:---|
| AC-1 | 20 | Correctness |
| AC-2 | 5  | Correctness |
| AC-3 | 20 | Correctness |
| AC-4 | 5  | Correctness / Code Quality |
| AC-5 | 10 | Correctness |
| AC-6 | 10 | Maintainability / Code Quality |
| AC-7 | 10 | Test Pass Rate |
| AC-8 | 10 | Security |
| AC-9 / AC-10 | 10 | Security / Correctness |

## Scoring Tie-in

| scoring 维度 | 本任务怎么评 |
|:---|:---|
| Correctness        | AC-1~5：是否真的"2 次读只有 1 次 DB、写入后第 3 次读重新到 DB" |
| Test Pass Rate     | AC-7：旧测试仍通过；如果 AI 自写 Redis 命中/失效测试也一并纳入 |
| Code Quality       | AC-4 / AC-6：是否优雅、边界处理是否统一；cache.js 封装是否清晰 |
| Security           | AC-8 / AC-10：别为了加缓存把参数化查询/输入校验给弄丢了 |
| Maintainability    | 降级机制/错误日志是否到位；TTL/键前缀是否集中配置 |
| Token / Latency / Human | scoring.md 通用定义 |
