# Lessons — AI 聊天应用

> ⚠️ 以下为基于常见坑总结的预判性教训，尚未经本案例实际运行验证。

## 易错点 → Anti-Pattern 对应

| # | 易错点 | 后果 | 对应 Anti-Pattern |
| --- | --- | --- | --- |
| 1 | API Key 写在前端 JS | 任何人 F12 偷走 key | [`../../../anti-patterns/hardcoded-api-key.md`](../../../anti-patterns/hardcoded-api-key.md) |
| 2 | 一个 prompt 让 AI 把全站写完 | 失控、难排查、改一处崩多处 | [`../../../anti-patterns/ai-writes-too-much-at-once.md`](../../../anti-patterns/ai-writes-too-much-at-once.md) |
| 3 | 不设请求超时 | LLM 卡住时页面无限转圈 | [`../../../anti-patterns/missing-timeout.md`](../../../anti-patterns/missing-timeout.md) |
| 4 | 无错误兜底 | 断网/key 失效时白屏或卡死 | [`../../../anti-patterns/no-error-fallback.md`](../../../anti-patterns/no-error-fallback.md) |
| 5 | 直接把回复 innerHTML | XSS：回复含 `<script>` 被执行 | [`../../../anti-patterns/unsafe-innerhtml.md`](../../../anti-patterns/unsafe-innerhtml.md) |

## 教训详解

### 1. Key 暴露在前端

**现象**：为了省事，把 key 直接写进 `app.js`，前端直连 LLM。

**根因**：前端代码对用户完全可见，"藏"在前端等于没藏。

**正确做法**：key 放后端环境变量，前端只调自己的 `/api/chat`。提交前 grep `sk-` / `api_key` 自查。

### 2. AI 一次写太多

**现象**：一句话让 AI"把整个聊天应用写完"，结果一堆文件互相牵连，改一处崩三处。

**根因**：违反"小步可验证"。AI 没有全局一致性保证，铺得越大越乱。

**正确做法**：参考 [`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)，一次只给一个任务，跑通了再下一个。

### 3. 不处理超时

**现象**：LLM 偶尔响应慢，页面一直转圈，用户以为坏了。

**正确做法**：`fetch` 或后端请求设 30s 超时，超时显示"请求超时，请重试"。

### 4. 无错误兜底

**现象**：断网或 key 失效，`fetch` 抛错没人接，页面白屏。

**正确做法**：前端 `try/catch` 包住请求，失败时在消息列表显示一条"出错了：<原因>"。

### 5. 不转义回复

**现象**：把 LLM 回复直接 `innerHTML`，若回复含 `<img onerror=...>` 触发 XSS。

**正确做法**：用 `textContent` 或先转义 `<` `>` 再插入。

## 可复用的知识

- "key 永远不上前端"是所有调第三方 API 的通用规则
- "小步走 + 每步验收"是给 AI 编码的通用心法
- "错误兜底"不是可选项——网络请求一定会失败，只是什么时候
