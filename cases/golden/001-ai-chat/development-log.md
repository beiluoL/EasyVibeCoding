# Development Log — AI 聊天应用

> ⚠️ Verification Pending — 以下步骤为**计划中的构建顺序**，尚未实际执行。每步标注了拟用的 prompt/skill，但代码未真正生成与运行。

## 构建原则

一次只做一件事、每步可验证。参考 [`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)（小步实现）。

## 步骤 1 — 项目骨架

**Goal**: 建目录、初始化 `index.html` + 一个空 `server.js`/`app.py`、配 `.env` 与 `.gitignore`。

**Prompt**: [`../../../prompts/start-here/start-project.md`](../../../prompts/start-here/start-project.md)

**Skill**: [`../../../skills/core/project-discovery/SKILL.md`](../../../skills/core/project-discovery/SKILL.md)

**AI Result (Illustrative)**:
AI 生成 `index.html` 空白页骨架、`server.js` 空文件、`.gitignore` 包含 `.env`、`.env.example` 模板。

**Human Decision**: 确认目录结构合理，`.gitignore` 确实包含 `.env`。

**Problem (Illustrative)**: AI 忘了在 `.gitignore` 里加 `.env`，导致 key 可能被提交。

**Fix (Illustrative)**: 手动在 `.gitignore` 加 `.env`，跑 `git status` 确认 `.env` 不在跟踪列表。

**Verification**: `git status` 确认 `.env` 不在跟踪列表；浏览器打开 `index.html` 能显示空白页。

**Acceptance**: 目录就位，`.gitignore` 含 `.env`，`index.html` 能打开。

> ⚠️ 未实际执行——以上为计划性记录。

## 步骤 2 — 聊天 UI

**Goal**: 在 `index.html` 画输入框 + 发送按钮 + 消息列表容器；`app.js` 能把用户输入追加到列表。

**Prompt**: [`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**Skill**: [`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)

**AI Result (Illustrative)**:
AI 生成 `app.js`，绑定发送按钮点击事件，把输入框内容追加到消息列表 DOM。

**Human Decision**: 确认 UI 布局合理——输入框在底部、消息列表占主体。

**Problem (Illustrative)**: AI 把发送按钮写成了 `<a>` 标签而不是 `<button>`，点击会跳转页面。

**Fix (Illustrative)**: 改成 `<button type="button">`，阻止默认行为。

**Verification**: 浏览器打开页面，打字点发送，消息出现在列表。此时不接 LLM。

**Acceptance**: 打字点发送，消息出现；发送后输入框清空。

> ⚠️ 未实际执行——以上为计划性记录。

## 步骤 3 — 后端接口

**Goal**: 后端开 `POST /api/chat`，从环境变量读 key，调 LLM 的 Chat Completions，把回复返回前端。

**Prompt**: [`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**Skill**: [`../../../skills/core/architecture-design/SKILL.md`](../../../skills/core/architecture-design/SKILL.md)

**AI Result (Illustrative)**:
AI 生成 Express 路由 `POST /api/chat`，从 `process.env.API_KEY` 读 key，调 LLM Chat Completions，返回 JSON。

**Human Decision**: 确认 key 从环境变量读，不硬编码。确认超时时间设为 30s。

**Problem (Illustrative)**: AI 把 key 写成了硬编码 `const API_KEY = "sk-xxx"` # safe: example 而不是从环境变量读。

**Fix (Illustrative)**: 改成 `const API_KEY = process.env.API_KEY`，并在 `.env` 中设置。grep 确认无硬编码 key。

**Verification**: curl 发请求，能拿到 LLM 回复。`grep -rn "sk-" .` 无真实 key。

**Acceptance**: curl 发请求拿到回复；key 从环境变量读。

> ⚠️ 未实际执行——以上为计划性记录。

## 步骤 4 — 前端接后端、渲染回复

**Goal**: `app.js` 用 `fetch` 调 `/api/chat`，把回复渲染进消息列表，区分用户/AI 气泡。回复做 HTML 转义。

**Prompt**: [`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**Skill**: [`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)

**AI Result (Illustrative)**:
AI 生成 fetch 逻辑，用户消息右对齐、AI 消息左对齐。回复用 `textContent` 插入防 XSS。

**Human Decision**: 确认回复做了转义（防 XSS）。确认发送期间按钮禁用。

**Problem (Illustrative)**: AI 用 `innerHTML` 插入回复，若 LLM 回复含 `<script>` 会被执行。

**Fix (Illustrative)**: 改成 `textContent` 或先转义 `<` `>` 再插入。

**Verification**: 浏览器发消息→看到 AI 回复；连续追问→历史保留。回复含 `<script>` 时作为文本显示。

**Acceptance**: 发消息看到回复；用户/AI 可区分；历史保留。

> ⚠️ 未实际执行——以上为计划性记录。

## 步骤 5 — 清空历史

**Goal**: 加"清空历史"按钮，点击清空列表（如用 localStorage 一并清）。

**Prompt**: [`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**AI Result (Illustrative)**:
AI 加了清空按钮，点击清空 DOM 消息列表和 `localStorage`。页面加载时从 `localStorage` 恢复历史。

**Human Decision**: 确认清空前不需要确认弹窗（小白项目，简单优先）。

**Problem (Illustrative)**: AI 忘了清空 `localStorage`，导致刷新后旧消息又回来了。

**Fix (Illustrative)**: 清空时同时清 `localStorage.removeItem('messages')`。

**Verification**: 发消息→刷新→历史在；点清空→列表空；再刷新→不恢复。

**Acceptance**: 点清空列表清空；再发消息从空白开始。

> ⚠️ 未实际执行——以上为计划性记录。

## 步骤 6 — 错误兜底与安全自查

**Goal**: 前端加请求超时（30s）与 try/catch；断网/key 失效显示可读错误；提交前全仓库 grep 确认无硬编码 key。

**Prompt**: [`../../../prompts/debugging/debug-error.md`](../../../prompts/debugging/debug-error.md) · [`../../../prompts/review/security-review.md`](../../../prompts/review/security-review.md)

**Skill**: [`../../../skills/core/systematic-debugging/SKILL.md`](../../../skills/core/systematic-debugging/SKILL.md) · [`../../../skills/core/verification-before-completion/SKILL.md`](../../../skills/core/verification-before-completion/SKILL.md)

**AI Result (Illustrative)**:
AI 加了 `AbortController` 30s 超时，`try/catch` 包住 fetch，失败时显示"⚠️ 请求失败：<原因>"。

**Human Decision**: 确认错误提示可读（不是 JS 报错信息）。确认 grep 无真实 key。

**Problem (Illustrative)**: AI 的错误提示显示 `TypeError: Failed to fetch`——用户看不懂。

**Fix (Illustrative)**: 改成"网络连接失败，请检查网络"等可读提示。

**Verification**: 断网发消息→看到提示不白屏；停后端发消息→看到提示不卡死；grep 无真实 key。

**Acceptance**: 断网→提示不白屏；超时→提示不卡死；grep 无 key。

> ⚠️ 未实际执行——以上为计划性记录。

## 状态总览

| 步骤 | 状态 |
| --- | --- |
| 1 骨架 | ⚠️ 未执行 |
| 2 UI | ⚠️ 未执行 |
| 3 接口 | ⚠️ 未执行 |
| 4 渲染 | ⚠️ 未执行 |
| 5 清空 | ⚠️ 未执行 |
| 6 错误兜底 | ⚠️ 未执行 |
