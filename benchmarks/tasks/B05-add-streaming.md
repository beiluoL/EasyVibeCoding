# B05 — 给 LLM 接口加 SSE 流式输出

> ⚠️ Not Yet Verified — 此任务尚未在真实模型上跑过分。以下所有"Expected / Acceptance / Evaluation"都是对目标行为的**期望定义**，不代表任何模型已经实现或得分。

## Task

在一个「调用 LLM → 等待完整响应 → 一次性 JSON 返回」的现有接口基础上，改造为 **SSE（Server-Sent Events）流式输出**：浏览器能**逐字显示** LLM 生成过程，最后收到 `end` 事件；并在**断网 / LLM 超时**等异常情况下给出正确的错误事件而不是直接挂。

- SSE（大白话解释）：**服务器不停地给浏览器"推一小段一小段文本"**，浏览器每收到一段就往页面上追加一个字，这样用户不用等 AI 全说完才看到内容。
- Server-Sent Events（正式名）= SSE：基于普通 HTTP，响应头 `Content-Type: text/event-stream`，数据格式 `data: xxx\n\n`。

## Difficulty

**intermediate**

## Goal

- 将 `POST /chat` 从"全量 JSON 返回"改造为 `text/event-stream` 返回：
  - 首字节（首字）延迟 ≤ 2s（本地连 Mock LLM，网络良好环境测）；
  - 正确发送 `event: token` / `data: 字` 事件；
  - 结束时发送 `event: end\n\n`；
- 浏览器端 Demo HTML `public/index.html` 提供最小可运行示例：打开后点"发送"，页面 `<div id="output">` 会**逐字追加**，最后一行显示 `[DONE]`；
- LLM 抛错 / 超时（>30s）/ TCP 断连时，SSE 流能通过 `event: error` + `data: { message, code }` 明确错误，不静默断开。

## Input

### 1）项目骨架

```
easyvibe-b05/
├── package.json      ← 已声明 axios、dotenv；测试用：node:test
├── .env.example      ← LLM_API_KEY / LLM_CHAT_MODEL / LLM_BASE_URL（同 B04 风格）
├── src/
│   ├── index.js      ← 现有版本（见下方"现有 POST /chat 关键代码"）
│   └── llm.js        ← 封装了 chatComplete({ messages, stream:false }) → 非流式返回全文
├── public/
│   └── index.html    ← 空壳页面，只有 <textarea id="input"/> + <button/> + <div id="output"/>
└── tests/
    └── mock-llm.js   ← 提供一个本地 Mock LLM：按字符间隔 10ms 吐出给定回复（供验收脚本用）
```

### 2）现有 POST /chat 关键片段（原样注入）

```js
// src/index.js — 现在的实现（非流式）
app.post('/chat', async (req, res) => {
  const { question } = await parseJSON(req);
  try {
    const answer = await llm.chatComplete({
      messages: [{ role: 'user', content: question }],
      stream: false,
    });
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({ answer }));
  } catch (e) {
    res.statusCode = 500;
    res.end(JSON.stringify({ error: e.message }));
  }
});
```

### 3）测试辅助：Mock LLM（由验收端通过 `TEST_MODE=1` 注入）

- 当 `process.env.TEST_MODE=1` 时，`llm.js` 改为直接使用 `tests/mock-llm.js`：
  - `chatComplete({ messages, stream: true })` 返回一个 Node Readable，每 10ms emit 一个字符；
  - 支持 `forceErrorAfter = N` 参数：发 N 个字符后抛异常（用于 AC-8）。

### 4）约束

- 必须**真 SSE**：响应头 `Content-Type: text/event-stream` + `Cache-Control: no-cache` + `Connection: keep-alive`，**不能**用 `WebSocket` 或 `Transfer-Encoding: chunked` 的非标准自定义协议；
- 每段字符以 `event: token\ndata: {字}\n\n` 发出（`event: end` 不发 `data`）；
- 兼容：同时保留 `?stream=false` 查询参数能走回旧 JSON 返回（不破坏原调用方）；
- 代码改动集中在 `src/index.js` + `src/llm.js`（新增 `stream:true` 分支）+ `public/index.html` 前端逻辑，不要改其他文件。

## Expected Behavior

1. 启动服务 `node src/index.js`，用 `curl -N -X POST http://localhost:3000/chat?stream=true -d '{"question":"你好"}'`
   - 首行立刻看到 HTTP 200 + `Content-Type: text/event-stream`；
   - 然后陆续出现若干行：
     ```
     event: token
     data: 你

     event: token
     data: 好
     ...
     event: end

     ```
2. `curl http://localhost:3000/chat?stream=false -d '{"question":"你好"}'` 仍然返回一次性 JSON：
   ```json
   { "answer": "你好……（全文）" }
   ```
   （即 stream=false 为 backward compatible）
3. 浏览器打开 `http://localhost:3000/` → 填入问题 → 点发送 → `<div id="output">` 逐字追加；完成后末尾追加 `[DONE]`；
4. 首字延迟（从 curl 发请求到首段 `event: token\ndata: ...` 抵达），在 Mock LLM 场景下**≤ 2000ms**；
5. 断网测试：客户端在流中途关闭 socket（验收脚本关闭 curl 进程），服务端**10 秒内检测到并释放资源**，没有内存泄漏（压测 100 次前后 process RSS 差 ≤ 50MB）；
6. LLM 异常测试：`forceErrorAfter=5` → 流输出 5 个 token 后，下一条是 `event: error\ndata: {"code":"LLM_ERR","message":"..."}\n\n`，之后服务端正常结束响应。

## Acceptance Criteria

| # | 验收项 | 对应维度 |
|:---:|:---|:---|
| AC-1 | `?stream=true` 响应头含 `Content-Type: text/event-stream` 且返回 HTTP 200 | Correctness |
| AC-2 | `curl -N` 能看到 ≥ 5 行 `event: token`，且最后一行有效事件为 `event: end`（不含额外 data） | Correctness |
| AC-3 | `?stream=false` 仍然返回 JSON 结构 `{answer:"..."}` 与改造前一致（逐字段深比较） | Correctness / Maintainability（兼容性） |
| AC-4 | 浏览器 Demo：发问题后 `<div id="output">` 的文本最后等于 Mock LLM 预期完整回答（用 Playwright/ puppeteer 断言） | Correctness |
| AC-5 | 首字延迟 ≤ 2000ms（Mock LLM 下跑 5 次取均值 ≤ 1500ms，允许尖峰到 2000ms） | Latency 子项 / Correctness |
| AC-6 | 流数据量校验：Mock LLM 设定回答长度 = 100 字 → 实际 `event: token` 行数正好 = 100 | Correctness |
| AC-7 | 断网 100 次压测前后 RSS 差 ≤ 50MB（无明显泄漏），同时活跃句柄数 `process._getActiveHandles().length` 差值 ≤ 5 | Maintainability |
| AC-8 | `forceErrorAfter=5` 后，出现且仅出现一次 `event: error` + JSON data 含 `code` 与 `message`；且 error 事件后不再出现 `event: token`；随后响应正常关闭 | Correctness / Code Quality |
| AC-9 | 服务端不得把 `LLM_API_KEY` 或其他 `.env` 中的 secret 作为任何 event 的 data 输出（简单扫描所有事件 data 串中不含 `sk-` 前缀） | Security |

## Evaluation

满分 100 分：

| AC | 小分 | 归属维度 |
|:---:|:---:|:---|
| AC-1 | 5  | Correctness |
| AC-2 | 15 | Correctness |
| AC-3 | 15 | Correctness / Maintainability（向后兼容） |
| AC-4 | 15 | Correctness |
| AC-5 | 10 | Latency / Correctness |
| AC-6 | 10 | Correctness（流保真） |
| AC-7 | 10 | Maintainability（泄漏） |
| AC-8 | 15 | Correctness / Code Quality（错误处理） |
| AC-9 | 5  | Security |

## Scoring Tie-in

| scoring 维度 | 本任务怎么评 |
|:---|:---|
| Correctness        | AC-1/2/3/4/6/8：流式格式 + 事件序列 + 兼容性 + 浏览器端逐字 + 异常错误事件 |
| Test Pass Rate     | 9 条 AC 通过 + AI 若自写 EventSource 客户端测试也计入 |
| Code Quality       | 流式分支与非流式分支是否复用；是否把 SSE 格式封装成 helper；错误链路是否清晰 |
| Security           | AC-9（key 不泄露）+ 问题/回答是否经过 XSS 基础转义（浏览器 Demo 里 innerHTML 时小心） |
| Maintainability    | AC-3 向后兼容 + AC-7 内存泄漏；超时/重试的可配置性 |
| Token Usage        | 同样跑 100 字回答，Prompt+Completion Token 与非流式的差值（流式应该略少或持平） |
| Latency            | AC-5 首字延迟；另外记录流完成耗时（非流式 vs 流式的"全字到齐"时间差） |
| Human Intervention | 纠偏次数（流 + SSE 细节较多，默认 2 次纠偏为 5-6 分线） |
