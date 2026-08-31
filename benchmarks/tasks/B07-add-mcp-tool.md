# B07 — 给 MCP client 写一个 Todo CRUD 工具

> ⚠️ Not Yet Verified — 此任务尚未在真实模型上跑过分。以下所有"Expected / Acceptance / Evaluation"都是对目标行为的**期望定义**，不代表任何模型已经实现或得分。

## Task

给一个 **MCP（Model Context Protocol）客户端**，写一个独立的 **Todo CRUD 工具**（工具 = MCP Tool），包含：
1. 正确的 JSON Schema（输入参数校验）；
2. 本地 SQLite 存储（每个 user_id 一份 todo，做到多用户数据隔离）；
3. **安全边界与最小权限**：
   - 只允许操作当前 user 的 todo（越权防御）；
   - 对「清空所有 todo」这类高危动作要求调用方显式 confirm（**AI 不能自作主张自动执行**）。

- MCP（大白话解释）：**一套让 AI 模型"调用外部工具"的统一协议**——就像给 AI 一个工具箱，每个工具告诉 AI"我能干什么 / 传什么参数 / 返回什么结果"。本任务要写的是工具箱里的一件具体工具：Todo CRUD。
- 最小权限原则（大白话解释）：**能少给的权限绝不乱给**——调用方说自己是 user A，就只让他碰 A 的 todo，别人的一条也看不到、改不动。

## Difficulty

**advanced**

## Goal

产出一个可被 MCP client 动态 `registerTool(...)` 的模块 `tools/todo.js`，包含 4 个 MCP Tool：

| Tool 名 | 作用 | 危险等级 |
|:---|:---|:---:|
| `todo_create`   | 新建一条 todo（user_id, title, due_date?） | 低 |
| `todo_list`     | 列出当前 user 的 todo（status? 过滤） | 无 |
| `todo_update`   | 更新一条 todo（status, title, due_date） | 中 |
| `todo_clear_all` | 清空当前 user 所有 todo | **高（需 confirm）** |

并满足：

- 每个 Tool 的 `inputSchema` 都是合法 JSON Schema（Draft 7），MCP SDK 能加载不报错；
- `todo_update` / `todo_clear_all` 在执行前会先检查该 todo 归属（或 clear_all 检查 user），**越权直接返回 MCP error**，不做任何写操作；
- `todo_clear_all` 在首次调用时返回一个 `confirmation_required` 对象（MCP 约定），包含 `confirmation_token=xxx`；只有再次调用且传了 `confirm_token=xxx` 才真的执行清空；
- 所有 DB 操作用参数化查询；
- 代码里**没有暴露全局管理员模式**（例如 `?admin=1` 能看所有用户 todo 的后门）。

## Input

### 1）项目骨架

```
easyvibe-b07/
├── package.json        ← 已声明：@modelcontextprotocol/sdk（MCP SDK）、better-sqlite3、ajv（JSON Schema 校验器）
├── schema.sql          ← 只有 todo 表（见下）
├── data/               ← SQLite 输出目录
├── tools/
│   └── todo.js         ← 空文件：AI 要在这里 export 4 个 MCP Tool
├── tests/
│   ├── mcp-client.js   ← 验收端提供：一个最小 MCP client，能 registerTool + 调用
│   └── fixtures.sql    ← 预置 2 个 user、各 3 条 todo 的 SQL
└── README-mcp.md       ← MCP SDK 的 Tool 接口示例（见下方片段注入）
```

### 2）schema.sql（Todo 表）

```sql
CREATE TABLE IF NOT EXISTS todos (
  id        INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id   TEXT NOT NULL,       -- 来自调用上下文，不是用户请求参数
  title     TEXT NOT NULL,
  status    TEXT NOT NULL DEFAULT 'todo' CHECK (status IN ('todo','doing','done')),
  due_date  TEXT,                -- ISO 8601 日期或 NULL
  created_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);
CREATE INDEX IF NOT EXISTS idx_todos_user ON todos(user_id);
```

### 3）MCP Tool 接口约定（README-mcp.md 片段注入）

```js
// 一个 MCP Tool 的对象结构示例
export const todo_create = {
  name: 'todo_create',
  description: '给当前用户创建一条 todo。',
  inputSchema: {
    type: 'object',
    required: ['title'],
    properties: {
      title:    { type: 'string', minLength: 1, maxLength: 200 },
      due_date: { type: 'string', format: 'date' }
    },
    additionalProperties: false,   // 禁止额外字段（最小权限）
  },
  // MCP SDK 会把上下文 ctx = { user_id, confirmToken? } 注入进来
  async execute(args, ctx) {
    // ... 真正的逻辑写这里
  }
};
```

### 4）约束

- 每个 Tool 必须提供 `name` / `description` / `inputSchema` / `execute(args, ctx)` 四项，缺一不可；
- `user_id` 必须从 `ctx.user_id` 取，**绝对不能**从 `args` 取（防越权）；
- `todo_clear_all` 的 confirm token 采用 HMAC：`HMAC_SHA256(APP_SECRET, "clear_all:" + user_id + ":" + 最近 5 分钟的时间桶)`，token **一次性有效**；
- 代码中不得出现形如 `if (args.admin) return all todos` 的后门；
- 不使用 `DELETE FROM todos`（不带 WHERE）这种无差别 SQL（静态扫描拦截）。

## Expected Behavior

1. **create 正常**：
   ```
   call(todo_create, {title:"写周报"}, {user_id:"A"})
   → 返回 { ok:true, id: N }
   DB 中存在一条 todos.user_id = A、title = 写周报。
   ```
2. **create 参数校验**：
   - title 缺失 → `error = { code: "VALIDATION", details: [...] }`（ajv 校验失败，不执行 SQL）。
   - title > 200 字符 → 同上。
3. **list 隔离**：
   ```
   call(todo_list, {}, {user_id:"A"}) → 只含 A 的；
   call(todo_list, {}, {user_id:"B"}) → 只含 B 的（fixtures 里各 3 条）。
   ```
4. **update 越权**：
   - 先用 fixtures 拿到 `todo_id_B = A 已知不存在的 id`（属于 B 的 todo id）；
   - `call(todo_update, {id: todo_id_B, status:"done"}, {user_id:"A"})` → 返回 `{ error: {code: "FORBIDDEN"} }`，DB 中该 todo 状态完全没变化。
5. **clear_all 需要 confirm**：
   - 首次调用 `call(todo_clear_all, {}, {user_id:"A"})` → 返回：
     ```
     { confirmation_required: {
         reason: "即将清空你全部 todo（不可恢复）",
         confirm_token: "hmac-sha256:..."
     } }
     ```
     - DB 里 A 的 todo 数**仍是 3**（没真删）。
   - 再次调用 `call(todo_clear_all, {confirm_token: 刚才拿到的 token}, {user_id:"A"})` →
     返回 `{ ok: true, deleted: 3 }`，DB 里 A 归零，B 仍 3 条。
   - 第三次使用**同一个** confirm_token → `{ error: {code: "TOKEN_REUSED"} }`。
6. **禁止全表删除**：
   - 静态扫描：`tools/todo.js` 里正则匹配 `DELETE FROM\s+todos\s*;?\s*$`（不带 WHERE） → 命中 0 次。

## Acceptance Criteria

| # | 验收项 | 对应维度 |
|:---:|:---|:---|
| AC-1 | 4 个 Tool 都能成功 `mcpClient.registerTool(...)`：无 schema 错误、无缺字段 | Correctness |
| AC-2 | `todo_create` 合法参数 → DB 实际写入 1 条，user_id 正确 | Correctness |
| AC-3 | `todo_create` 3 种非法参数（无 title / 空 title / 超长 title）→ ajv VALIDATION 错误 + SQL 写入次数未增 | Code Quality / Security（参数校验） |
| AC-4 | `todo_list` 隔离：A 只看到 A，B 只看到 B；fixtures 各 3 条返回长度全 =3 | Security（越权读取）|
| AC-5 | `todo_update` 越权（A 改 B）→ FORBIDDEN + DB 未变 | Security（越权写入） |
| AC-6 | `todo_clear_all` 首调无 confirm → 仅返回 `confirmation_required`，DB 条数不变 | Security（高危阻断） |
| AC-7 | 二次调用带正确 token → 真清空，B 的数据完好 | Security + Correctness |
| AC-8 | 三次调用复用相同 token → TOKEN_REUSED | Security（一次性） |
| AC-9 | 用错误 token（篡改 1 位）调用 → 直接 error，不清空 | Security |
| AC-10 | 静态扫描：`DELETE FROM todos`（无 WHERE）0 次；`if.*admin` 后门关键词 0 次（含大小写不敏感）| Security |
| AC-11 | SQLi：`todo_create` 注入 title="x', 'A'); DROP TABLE todos; --" → todos 表仍存在 | Security |

## Evaluation

满分 100 分：

| AC | 小分 | 归属维度 |
|:---:|:---:|:---|
| AC-1 | 5  | Correctness（注册 4 工具） |
| AC-2 | 5  | Correctness |
| AC-3 | 10 | Code Quality / Security |
| AC-4 | 15 | Security（读越权）|
| AC-5 | 15 | Security（写越权）|
| AC-6 | 15 | Security（高危首调不执行）|
| AC-7 | 10 | Security + Correctness |
| AC-8 | 10 | Security（一次性 token） |
| AC-9 | 5  | Security |
| AC-10 | 5  | Security（静态） |
| AC-11 | 5  | Security（SQLi 实打） |

## Scoring Tie-in

| scoring 维度 | 本任务怎么评 |
|:---|:---|
| Correctness        | AC-1/2/7（4 个工具能注册 + 基本功能 + 清空正常流程） |
| Test Pass Rate     | 11 条 AC 通过率 + AI 自写的工具级单测 |
| Code Quality       | schema 是否严谨（additionalProperties:false、长度、枚举、date format）；execute 是否分函数；错误码是否一致 |
| Security           | AC-4/5/6/8/9/10/11 全部命中（越权 / 高危 confirm / 一次性 token / 无后门 / SQLi）— 本任务最重维度 |
| Maintainability    | DB 访问是否封装；confirm 机制是否可复用为通用 `requireConfirm()` helper |
| Token Usage / Latency / Human Intervention | scoring.md 通用定义；本任务较复杂，Human 4 次为 3-4 分线 |
