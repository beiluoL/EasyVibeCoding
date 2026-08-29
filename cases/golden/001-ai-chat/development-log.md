# Development Log — AI 聊天应用

> ⚠️ Verification Pending — 以下步骤为**计划中的构建顺序**，尚未实际执行。每步标注了拟用的 prompt/skill，但代码未真正生成与运行。

## 构建原则

一次只做一件事、每步可验证。参考 [`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)（小步实现）。

## 步骤 1 — 项目骨架

**做什么**：建目录、初始化 `index.html` + 一个空 `server.js`/`app.py`、配 `.env` 与 `.gitignore`。

**拟用 prompt**：[`../../../prompts/start-here/start-project.md`](../../../prompts/start-here/start-project.md)

**拟用 skill**：[`../../../skills/core/project-discovery/SKILL.md`](../../../skills/core/project-discovery/SKILL.md)

**验收点**：目录就位，`.gitignore` 含 `.env`，`index.html` 能在浏览器打开（空白页也算）。

> ⚠️ 未实际执行。

## 步骤 2 — 聊天 UI

**做什么**：在 `index.html` 画输入框 + 发送按钮 + 消息列表容器；`app.js` 能把用户输入追加到列表。

**拟用 prompt**：[`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**拟用 skill**：[`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)

**验收点**：打字点发送，消息出现在列表；此时还不接 LLM。

> ⚠️ 未实际执行。

## 步骤 3 — 后端接口

**做什么**：后端开 `POST /api/chat`，从环境变量读 key，调 LLM 的 Chat Completions，把回复返回前端。

**拟用 prompt**：[`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**拟用 skill**：[`../../../skills/core/architecture-design/SKILL.md`](../../../skills/core/architecture-design/SKILL.md)

**验收点**：用 curl/Postman 发一个请求，能拿到 LLM 回复（key 从 `.env` 读，不写死）。

> ⚠️ 未实际执行。

## 步骤 4 — 前端接后端、渲染回复

**做什么**：`app.js` 用 `fetch` 调 `/api/chat`，把回复渲染进消息列表，区分用户/AI 气泡。回复做 HTML 转义。

**拟用 prompt**：[`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**拟用 skill**：[`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)

**验收点**：浏览器发消息 → 看到 AI 回复；连续追问，历史保留。

> ⚠️ 未实际执行。

## 步骤 5 — 清空历史

**做什么**：加"清空历史"按钮，点击清空列表（如用 localStorage 一并清）。

**拟用 prompt**：[`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**验收点**：点清空，列表清空；再发消息从空白开始。

> ⚠️ 未实际执行。

## 步骤 6 — 错误兜底与安全自查

**做什么**：前端加请求超时（30s）与 try/catch；断网/key 失效显示可读错误；提交前全仓库 grep 确认无硬编码 key。

**拟用 prompt**：[`../../../prompts/debugging/debug-error.md`](../../../prompts/debugging/debug-error.md) · [`../../../prompts/review/security-review.md`](../../../prompts/review/security-review.md)

**拟用 skill**：[`../../../skills/core/systematic-debugging/SKILL.md`](../../../skills/core/systematic-debugging/SKILL.md) · [`../../../skills/core/verification-before-completion/SKILL.md`](../../../skills/core/verification-before-completion/SKILL.md)

**验收点**：断网发消息 → 看到错误提示不白屏；grep 无真实 key。

> ⚠️ 未实际执行。

## 状态总览

| 步骤 | 状态 |
| --- | --- |
| 1 骨架 | ⚠️ 未执行 |
| 2 UI | ⚠️ 未执行 |
| 3 接口 | ⚠️ 未执行 |
| 4 渲染 | ⚠️ 未执行 |
| 5 清空 | ⚠️ 未执行 |
| 6 错误兜底 | ⚠️ 未执行 |
