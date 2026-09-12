# Failure Analysis — AI 聊天应用

> ⚠️ 以下为 Illustrative Example——基于常见 AI Coding 失败模式构建的示例，非真实开发记录。

---

## Failure 01 — AI 修改了错误的文件

### Problem

用户说"登录有问题"，AI 直接搜 "login" 关键词，命中前端 `login.vue` 并修改。实际问题是后端 JWT 校验逻辑。

### Context

- 项目有前端 `app.js` 和后端 `server.js`
- 用户报告"发消息后看不到回复"
- AI 搜索 "chat" 关键词，命中 `app.js` 的渲染函数

### Symptom

- 用户看到：发消息后页面没变化
- AI 判断：可能是 `app.js` 的渲染逻辑有问题
- AI 改了：`app.js` 的 `renderMessage()` 函数

### Root Cause

实际问题在后端 `server.js`——LLM 调用超时没有返回，前端 `fetch` 一直在等。AI 只看了前端，没查后端接口是否正常返回。

### Why AI Failed

- 只用了关键词搜索，没有走 Project Discovery 理解调用链
- 没有 Collect Evidence（没看 Network 面板确认请求响应）
- 直接跳到 Fix 步骤，跳过了 Locate 和 Hypothesis

### Fix

1. 走 [project-discovery](../../../skills/core/project-discovery/SKILL.md) 理解项目：前端 `app.js` → `fetch /api/chat` → 后端 `server.js` → LLM
2. 在浏览器 Network 面板看请求：发现 `/api/chat` 返回 500
3. 看后端日志：LLM 调用超时
4. 根因在后端超时处理，不在前端渲染
5. 修 `server.js` 的超时逻辑，`app.js` 回滚

### Prevention

- 改代码前先走 Project Discovery，理解调用链
- 改之前让 AI 复述"我准备改 X 文件的 Y 函数，对吗"
- 任何"顺手改了别的地方"都视为越权

### Related Skill

- [project-discovery](../../../skills/core/project-discovery/SKILL.md)
- [systematic-debugging](../../../skills/core/systematic-debugging/SKILL.md)

### Related Prompt

- [02-project-discovery](prompts/02-project-discovery.md)
- [06-debugging](prompts/06-debugging.md)

### Related Anti-Pattern

- [wrong-file-editing](../../../anti-patterns/wrong-file-editing.md)

---

## Failure 02 — AI Debug 进入循环

### Problem

AI 修 Bug 时不断猜测式修改，每轮改一个地方，引入新问题，形成无限循环。

### Context

- 报错：`TypeError: Cannot read 'id' of undefined`
- AI 第 1 轮：加了个 `if (user)` 判断 → 报错消失但功能不对
- AI 第 2 轮：改了判断逻辑 → 新报错出现
- AI 第 3 轮：又改了一处 → 旧报错回来了
- 循环 10+ 轮，代码面目全非

### Symptom

- 每轮都有改动，看起来在推进
- 但 Bug 没有真正修好
- 代码越改越乱
- 最终原始 Bug 还在 + 引入了 3 个新 Bug

### Root Cause

AI 没有走 systematic-debugging 的 9 步流程：
- 没有稳定复现
- 没有 Collect Evidence
- 没有 Locate 定位
- 没有 Hypothesis 假设
- 直接跳到 Fix，而且是猜测式 Fix

### Why AI Failed

- "改了试试"不是 Debug 是赌博
- 每轮改完没有回归验证
- 没有"3 轮无进展就停"的规则
- 一直在症状层面打补丁，没找根因

### Fix

1. 停止猜测式修改
2. 回到 systematic-debugging Step 1：Observe
3. 复现：什么操作触发？→ 登录后跳转首页时
4. Collect Evidence：看接口返回，发现 `/api/user` 返回 `{}`
5. Locate：后端 `userController.getUser` 查询条件错了
6. Hypothesis：userId 从 session 取值是 null
7. Verify：打印 session，确认 null
8. Fix：修 session 设置逻辑，一处
9. Regression：原用例 ✅ + 相关测试 ✅

### Prevention

- 禁止"先改了再说"——改之前必须有根因假设
- 设修改轮数上限（3 轮无进展就停）
- 每轮改完必须跑回归测试
- 使用 [debugging workflow](../../../workflows/bug-fix/README.md)

### Related Skill

- [systematic-debugging](../../../skills/core/systematic-debugging/SKILL.md)

### Related Prompt

- [06-debugging](prompts/06-debugging.md)

### Related Anti-Pattern

- [blind-debugging](../../../anti-patterns/blind-debugging.md)
- [endless-debug-loop](../../../anti-patterns/endless-debug-loop.md)
