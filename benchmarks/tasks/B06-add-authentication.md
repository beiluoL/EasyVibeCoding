# B06 — 加邮箱 + 密码注册登录与 JWT 鉴权

> ⚠️ Not Yet Verified — 此任务尚未在真实模型上跑过分。以下所有"Expected / Acceptance / Evaluation"都是对目标行为的**期望定义**，不代表任何模型已经实现或得分。

## Task

在一个「没有任何用户概念」的 REST 笔记项目基础上，增加：**邮箱+密码注册、登录、JWT 鉴权**三部分。要求：密码只存哈希；未登录访问受保护接口返回 401；每条笔记归属于创建者，A 不能看/改/删 B 的笔记（越权防御）。

- JWT（大白话解释）：**登录成功后服务器发给你的一串"加密小票"**，之后你每次请求把小票带在 Header 里，服务器验一下小票签名和过期时间就知道"你是你"，不用再查数据库里的 session。
- 哈希（大白话解释）：**单向加密**——把密码"打碎"成一串乱码存起来，打碎后谁也还原不出原密码；即使数据库被盗，攻击者也拿不到真实密码。

## Difficulty

**intermediate**

## Goal

- 注册 `POST /auth/register`：邮箱+密码 → 写入 `users` 表，**密码 bcrypt/md5+盐**（推荐 bcrypt ≥ 10 轮）→ 返回 201 + `{ token }`；
- 登录 `POST /auth/login`：邮箱+密码 → 比对哈希 → 返回 200 + `{ token }`；错误邮箱或密码 → 401 + 含糊错误信息（不暴露"邮箱不存在还是密码错"）；
- 鉴权中间件：请求任何 `/notes*` 接口时，必须带 `Authorization: Bearer <token>`；缺 Header / 格式错 / token 过期 / 签名错 → 401；
- 数据隔离：`notes` 表新增 `user_id` 字段；所有 CRUD 只操作当前登录者自己的笔记（A 创建的，B 去 GET/PATCH/DELETE 一律 404）；
- 注册时如果邮箱已存在 → 409 Conflict；
- JWT 默认过期时间 = **2 小时**，通过 `exp` claim 生效。

## Input

### 1）项目骨架

```
easyvibe-b06/
├── package.json          ← 已含 better-sqlite3、bcrypt、jsonwebtoken、dotenv
├── schema.sql            ← 仅含 notes 表（见下方"需扩展的点"）
├── src/
│   ├── index.js          ← B01 通过版本（无鉴权，有 notes CRUD）
│   ├── db.js             ← 同 B01
│   └── auth.js           ← 空文件（推荐写鉴权中间件 + 用户函数）
└── .env.example          ← JWT_SECRET=change-me
```

### 2）schema.sql（初始只有 notes 表，AI 需要在代码或扩展 schema 里加 users 表 + notes.user_id）

```sql
-- 初始版本（AI 需自行补 users 表并迁移 notes）
CREATE TABLE IF NOT EXISTS notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  content TEXT NOT NULL DEFAULT '',
  created_at INTEGER NOT NULL DEFAULT (strftime('%s','now')),
  updated_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);
```

### 3）约束

- 只允许使用指定三个库：`bcrypt` 做哈希、`jsonwebtoken` 做签名、`better-sqlite3` 做 DB；
- 密码哈希工作因子（salt rounds）≥ 10；
- JWT 使用 `HS256` 算法 + 来自 `process.env.JWT_SECRET` 的密钥（**禁止**写死密钥在源码里）；
- `POST /auth/login` 的错误返回必须统一：`401 { "error": "邮箱或密码错误" }`，不要区分「邮箱不存在 vs 密码不对」（防用户名枚举）；
- 任何 `/notes*` 路由**永远不要**把 `user_id` 放进请求体让前端传（必须从 JWT 取）；
- 注册邮箱校验：基本正则 `/.+@.+\..+/` + 长度 ≤ 255。

## Expected Behavior

1. `POST /auth/register {"email":"a@b.c","password":"abcd1234"}`
   - 返回 201；
   - body = `{ "token": "eyJhbGciOi..." }`；
   - `SELECT email, password FROM users` 能看到邮箱，`password` 字段前缀是 `$2b$10$`（bcrypt）且长度 ~60 字，**不是**明文。
2. 再 `POST /auth/register {"email":"a@b.c","password":"xxxx"}` → 409 `{ "error": "邮箱已被注册" }`。
3. `POST /auth/login {"email":"a@b.c","password":"abcd1234"}` → 200 + token。
4. `POST /auth/login {"email":"a@b.c","password":"WRONG"}` → 401，错误文案固定（不区分哪错）。
5. 不带 Header 调 `GET /notes` → 401 `{ "error": "未登录" }`。
6. 带第 3 步的 token 调 `POST /notes {"title":"A"}` → 201，背后 SQL 写入时 `user_id` 等于当前 JWT 的 `sub`。
7. 新注册用户 B：登录后 `GET /notes` 返回空数组（看不到 A 的笔记，数据隔离生效）。
8. B 尝试 `PATCH /notes/{id_A}` → 返回 404（不是 403！——防止让攻击者枚举真实 id）。
9. 等 JWT 过期 2 小时（测试时可临时发一个 1s 过期的 token 模拟）→ 带过期 token 调接口返回 401 + `{"error":"登录已过期"}`。

## Acceptance Criteria

| # | 验收项 | 对应维度 |
|:---:|:---|:---|
| AC-1 | 注册新邮箱 → 201 + 返回 JWT；DB 的 `users.password` 不以明文出现，且 `bcrypt.compare(plain, hash)` 返回 true | Correctness + Security |
| AC-2 | 同邮箱二次注册 → 409 | Correctness |
| AC-3 | 登录（正确邮箱密码）→ 200 + 可被 `jwt.verify(secret)` 通过的 token，含 `exp - iat = 7200s` (± 5s 容差) | Correctness |
| AC-4 | 登录（错误密码 / 不存在邮箱）→ 401；错误文案与 status 都相同（字节级比较），无法枚举用户名 | Security + Correctness |
| AC-5 | 无 Header / 格式错 / 空字符串 / "Bearer "（没 token）四种情况 → 全返回 401 且 body 都为 `{error:"未登录"}`（含糊） | Correctness + Security |
| AC-6 | 带合法 token 的 POST/GET/PATCH/DELETE notes，行为与 B01 一致 + 数据正确归属该 user_id | Correctness |
| AC-7 | 数据隔离：A 创建 note，B 的 token 去 GET/PATCH/DELETE → **全部 404**，绝不把 A 的内容返回给 B，也绝不允许修改 | Security（越权）+ Correctness |
| AC-8 | JWT 过期：构造 1s 过期 token → 1s 后请求 → 401 + `error="登录已过期"` | Correctness（有效期） |
| AC-9 | SQL 注入：`POST /auth/register {"email":"x','x'); DROP TABLE users; --","password":"abcd1234"}` → 执行后 users 表仍存在（参数化查询） | Security |
| AC-10 | JWT_SECRET 扫描：`grep -E "JWT_SECRET\s*=\s*['\"]" src/` 无结果；只从 `process.env` 读 | Security（Key 管理） |
| AC-11 | 密码哈希工作因子：从 bcrypt hash 前缀取 rounds，≥ 10 | Security |

## Evaluation

满分 100 分：

| AC | 小分 | 归属维度 |
|:---:|:---:|:---|
| AC-1 | 15 | Correctness + Security |
| AC-2 | 5  | Correctness |
| AC-3 | 10 | Correctness |
| AC-4 | 10 | Security + Correctness |
| AC-5 | 10 | Correctness + Security |
| AC-6 | 15 | Correctness（回归 B01） |
| AC-7 | 15 | Security（越权）+ Correctness |
| AC-8 | 5  | Correctness |
| AC-9 | 5  | Security |
| AC-10 | 5  | Security |
| AC-11 | 5  | Security |

## Scoring Tie-in

| scoring 维度 | 本任务怎么评 |
|:---|:---|
| Correctness        | 注册/登录/鉴权/数据隔离/过期 5 大核心功能是否按 Expected 表现 |
| Test Pass Rate     | 11 条 AC 自动化通过率；AI 自写的单测（bcrypt / JWT / 中间件）也纳入 |
| Code Quality       | 中间件是否抽象成 `auth.js`，路由中是否干净；是否把 JWT claim 定义集中 |
| Security           | 占比最高：AC-1 哈希、AC-4 防枚举、AC-7 越权、AC-9 SQLi、AC-10 secret、AC-11 rounds |
| Maintainability    | 错误码/错误 body 是否统一；`notes.user_id` 迁移是否幂等（多次启动不报错） |
| Token Usage / Latency / Human Intervention | scoring.md 通用定义 |
