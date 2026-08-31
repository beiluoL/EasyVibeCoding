# B10 — AI 代码安全审计（找 4 类以上问题 + 分级 + 修复建议）

> ⚠️ Not Yet Verified — 此任务尚未在真实模型上跑过分。以下所有"Expected / Acceptance / Evaluation"都是对目标行为的**期望定义**，不代表任何模型已经实现或得分。

## Task

拿到一段**故意含多个严重问题的 AI 生成代码**（覆盖 SQL 拼接、API Key 前端硬编码、无输入校验、无错误处理、越权 五大类），要求：**逐项找出问题 → 给每个问题打严重等级（blocker / warn / nit）→ 并给出具体修复建议**。至少命中 **SQLi / Key Leak / Input Validation / Access Control 4 大类**，否则本任务判不通过。

- 安全审计（大白话解释）：**像查体检报告一样，把代码逐行看过去，把"会被黑客利用的坑 / 会让程序崩的坑 / 看起来不规范的坑"一条条列出来**。
- 严重等级（大白话）：
  - **blocker** = 今天不修复，明天可能被拖库/盗号（必须立刻修）；
  - **warn** = 短期没炸，但迟早出事（建议下版本修）；
  - **nit** = 风格/合规类小问题，不影响安全性但不专业（有时间就修）。

## Difficulty

**intermediate**

## Goal

- 输出文件 `audit-report.md`，结构固定为：
  ```
  # B10 安全审计报告
  ## 概览
  发现问题总数：N
  - blocker: X
  - warn:    Y
  - nit:     Z

  ## 问题清单

  ### P1 — 标题（严重等级：blocker）
  - 位置：`src/app.js:L12-L18`（给出代码行数，精确到 3 行以内）
  - 类别：SQL 注入（SQLi）/ API Key 泄露 / 输入校验缺失 / 错误处理缺失 / 越权访问
  - 代码片段：``` ... ``` 贴出原代码 ≤ 10 行
  - 风险说明：中文解释（给小白也能看懂的话）+ 一句专业描述
  - 修复建议：给出修改方向/伪代码，代码改动量 ≤ 10 行

  ### P2 ...
  ```
- 真实问题 ≥ 5 条，其中 blocker ≥ 3，且至少覆盖 **4 大类**（SQLi、Key Leak、Input Validation、Access Control）；
- 所有"位置"引用的代码行**不能不存在**（不编造行号）；
- 不得把"没问题的代码"硬说成有问题（误报 ≤ 1 条）。

## Input

### 1）项目骨架 + 待审计代码

```
easyvibe-b10/
├── src/
│   └── app.js    ← 120 行左右（5 类问题全都埋伏在里面）
└── tests/
    └── README-issues.md  ← 【验收端保密】参考答案（只在评分时内部看，不给 AI）
```

### 2）待审计的 `src/app.js`（原样完整注入，V0.1 作为 Prompt 片段）

```js
// src/app.js — 一段"AI 生成的笔记+用户后端代码"
// 审计时假设这段代码会被直接部署到公网生产环境
import http from 'node:http';
import sqlite from 'better-sqlite3';

const db = sqlite('./data/app.db');

// 🔴 问题 1（API Key 硬编码到前端可触达文件）：生产用 AK 直接写死在 JS 里
API_KEY = 'sk-live-example-not-a-real-key-redacted'  # safe: example (B10 task demo key, NOT real)

// 🔴 问题 2（SQL 拼接）：用字符串拼 SQL，最经典的 SQLi
function searchNotes(userId, keyword) {
  // 直接拼 keyword 进 SQL
  const sql = `SELECT * FROM notes WHERE user_id = '${userId}' AND title LIKE '%${keyword}%'`;
  return db.prepare(sql).all();
}

// 🔴 问题 3（越权 Access Control）：拿路径里的 userId 查 DB，没有和 token 里的当前用户比对
async function handleGetNotes(req, res) {
  const u = new URL(req.url, 'http://x').searchParams.get('userId');
  const rows = db.prepare(`SELECT * FROM notes WHERE user_id = ?`).all(u);
  res.end(JSON.stringify(rows));   // 任何登录用户只要改 URL 参数就能看别人的笔记
}

// 🔴 问题 4（完全没有输入校验）：title/content 完全不查，超长/空/XSS 都能进
async function handleCreateNote(req, res) {
  const body = await parseJSON(req);              // 没 try/catch
  const info = db.prepare('INSERT INTO notes (user_id, title, content) VALUES (?, ?, ?)')
    .run(body.userId, body.title, body.content);  // body 里什么字段都直接入库
  res.end(JSON.stringify({ id: info.lastInsertRowid }));
}

// 🟡 问题 5（错误处理缺失）：parseJSON 抛错或 DB 抛错直接让进程崩
function parseJSON(req) {
  return new Promise((resolve) => {
    let data = '';
    req.on('data', c => data += c);
    req.on('end', () => resolve(JSON.parse(data))); // JSON.parse 抛错会变成 uncaught rejection，进程挂
  });
}

// 🔵 问题 6（nit：console 直接打日志）：生产代码把敏感用户数据直接打 stdout
const server = http.createServer((req, res) => {
  console.log('REQ', req.url, req.headers.authorization);  // 直接打 JWT 到日志
  if (req.url.startsWith('/notes') && req.method === 'GET') handleGetNotes(req, res);
  if (req.url.startsWith('/notes') && req.method === 'POST') handleCreateNote(req, res);
});

server.listen(3000);
```

> 上面代码中，实际隐藏了 ≥ 6 个问题，问题 1~5 中覆盖 5 大类，6 是一个 nit 小问题。AI 需要从这段原始代码里自己挖掘并整理成报告。

### 3）约束

- 报告只写 `audit-report.md` 一个文件；
- 每条问题必须**贴原代码片段**（不能只口嗨"有 SQL 注入"不说哪一行）；
- 分类严格限制在：`SQL 注入 / API Key 泄露 / 输入校验缺失 / 错误处理缺失 / 越权访问 / 日志敏感信息 / 其他`；
- 修复建议必须**具体可操作**，不能写"请使用安全最佳实践"这种空话；SQLi 那条要明确写出「参数化查询」的伪代码。

## Expected Behavior

1. 概览里的 `N ≥ 5`、`blocker X ≥ 3`；
2. 4 大类问题中，每个大类都**至少一条**：
   - ✅ SQL 注入（对应 searchNotes 的字符串拼接）；
   - ✅ API Key 泄露（对应 `sk-live-...` 写死在源码）；
   - ✅ 输入校验缺失（对应 handleCreateNote 里完全不校验 title/content）；
   - ✅ 越权访问（对应 handleGetNotes 没有取 token 用户，直接拿 URL 的 userId）；
3. 严重等级合理：
   - SQLi、Key Leak、越权 → 必须标 **blocker**（标成 warn 或 nit 判错）；
   - 错误处理缺失、输入校验缺失 → **warn 或 blocker 均可**；
   - 打印 JWT 到日志 → 至少 **warn**，严格可标 blocker；
4. 位置精度：行号误差 ≤ 3（例如 searchNotes 写 `app.js:L9-L12` 都算对，写成 `:L1-L4` 就错）；
5. 修复建议质量：
   - SQLi 修复必须包含「用 ? 占位 + 数组传参」意思；
   - Key Leak 修复必须包含「改成 process.env.LLM_API_KEY」意思；
   - 越权修复必须包含「从 JWT 的 sub/uid 取当前 userId，与参数 userId 比较，不一致返回 403/404」意思；
   - 输入校验修复必须包含「min/max 长度 + 类型校验」；
   - 错误处理修复必须包含「try/catch 或 Promise.catch + 给客户端 500/400」。

## Acceptance Criteria

| # | 验收项 | 对应维度 |
|:---:|:---|:---|
| AC-1 | 报告中明确列出 ≥ 5 条问题（按 `### Pn -` 格式数）；blocker 数量 ≥ 3 | Correctness（覆盖度）|
| AC-2 | 确实命中 **SQL 注入** 类 ≥ 1 条，且代码片段行号指向 searchNotes 或其附近（±3） | Security 核心命中 |
| AC-3 | 确实命中 **API Key 泄露** 类 ≥ 1 条，且片段包含 `sk-live-...` 的那行（±3） | Security 核心命中 |
| AC-4 | 确实命中 **输入校验缺失** 类 ≥ 1 条，片段指向 handleCreateNote（±3）| Security 核心命中 |
| AC-5 | 确实命中 **越权访问** 类 ≥ 1 条，片段指向 handleGetNotes（±3） | Security 核心命中 |
| AC-6 | 严重等级：SQLi / Key Leak / 越权 三条中 **≥ 2 条**被标为 blocker（满分点） | Code Quality（分级合理性） |
| AC-7 | 5 条问题的行号精度：每条误差 ≤ 3 行的比例 = 100% | Correctness（定位准确性） |
| AC-8 | 修复建议可操作度：分别对 4 大类做"关键词匹配"：SQLi 提到"参数化 / ?"、Key 提到 "process.env"、越权提到 "JWT / 比对 / 403"、校验提到 "长度 / 类型" → 4/4 全有 | Maintainability / Code Quality |
| AC-9 | 误报率 ≤ 1 条：报告列出的所有问题中，"实际没问题被硬说成问题"的条数 ≤ 1 | Correctness（专业度） |
| AC-10 | 风险说明含"大白话 + 专业话"双重解释的问题条数 ≥ 4（符合 EasyVibeCoding"面向小白"定位）| Code Quality（可理解性）|

## Evaluation

满分 100 分：

| AC | 小分 | 归属维度 |
|:---:|:---:|:---|
| AC-1 | 10 | Correctness（量够） |
| AC-2 | 15 | Security（SQLi 必中） |
| AC-3 | 15 | Security（Key 必中） |
| AC-4 | 10 | Security（校验必中） |
| AC-5 | 15 | Security（越权必中） |
| AC-6 | 10 | Code Quality（分级合理） |
| AC-7 | 5  | Correctness（行号准） |
| AC-8 | 10 | Maintainability / Code Quality（修得动） |
| AC-9 | 5  | Correctness（少误报） |
| AC-10 | 5  | Code Quality（小白能懂） |

## Scoring Tie-in

| scoring 维度 | 本任务怎么评 |
|:---|:---|
| Correctness        | 找得全（AC-1）、找得对（AC-9）、找得准（AC-7） |
| Test Pass Rate     | 10 条 AC 通过率；无真实"跑代码"测试，但每条 AC 是结构化的可自动核验项 |
| Code Quality       | 报告格式、分级合理（AC-6）、小白能懂（AC-10） |
| Security           | 核心维度：AC-2/3/4/5（4 大类必须全命中，否则 Security 维度直接 0 分线） |
| Maintainability    | AC-8：修复建议是否真的能让工程团队拿去改、没有空话 |
| Token Usage / Latency | scoring.md 通用定义；本任务以"输出报告质量"为主，Token 不是关键指标 |
| Human Intervention | 典型纠偏：等级标错、修复建议太空、行号不对；2 次纠偏 = 5-6 分线 |
