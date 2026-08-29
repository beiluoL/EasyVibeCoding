# 03 — 启动你的第一个项目

> 用 start-project prompt，把一个模糊想法变成清晰的项目定义。

> 术语小贴士：**Project Brief（项目简介）**= 一份说清"做什么、给谁、怎么做"的文档，是项目的起点。

---

## 为什么要先"启动项目"

很多人上来就让 AI "写代码"，结果 AI 问一堆问题、你答不上来、代码跑不通。

正确顺序是：**先定义清楚，再动手写**（Principle 01 — Understand before coding）。

[start-project](../../prompts/start-here/start-project.md) prompt 就是帮你做这件事的——它会让 AI 引导你把想法说清楚，产出一份 Project Brief。

> ⚠️ Not Yet Verified：start-project prompt 在 V0.1 为规划内容，可能尚未填充完整。以下演示其预期用法。

---

## 分步演示

### Step 1：复制 start-project prompt

打开 [prompts/start-here/start-project.md](../../prompts/start-here/start-project.md)，复制里面的 Prompt 内容。

### Step 2：粘贴给你用的 AI

把 Prompt 粘贴到 AI 对话框（ChatGPT / Claude / Cursor 等），然后把你的想法填进去。

### Step 3：回答 AI 的引导问题

AI 会问你一系列问题，比如：
- 你想做什么？
- 给谁用？
- 核心功能有哪些？
- 技术上有偏好吗？

**老实回答**，别编。不知道就说"不确定，请给建议"。

### Step 4：拿到 Project Brief

AI 会输出一份结构化的项目简介，像下面这样。

---

## 最小示例输出（Project Brief）

假设你的想法是"做一个待办清单"，产出的 Project Brief 大致长这样：

```markdown
# Project Brief：极简待办清单

## 一句话目标
一个能记录、勾选、删除待办事项的网页应用，帮自己管理每日任务。

## 目标用户
- 个人用户，想轻量管理待办
- 不需要团队协作、不需要复杂分类

## 核心功能
1. 添加待办（输入文字 + 回车）
2. 标记完成（点击勾选）
3. 删除待办（点击删除按钮）
4. 列表展示（按添加时间倒序）

## 技术栈建议
- 前端：Next.js（React）
- 状态：React useState（MVP 不用数据库）
- 样式：Tailwind CSS
- 部署：Vercel

## MVP 范围（最小可用版本）
- 单页应用，数据存浏览器 localStorage
- 不做登录、不做云端同步
- 完成上述 4 个核心功能即可

## 验收标准
- [ ] 能添加一条待办并看到
- [ ] 能勾选完成，完成后有视觉变化
- [ ] 能删除一条待办
- [ ] 刷新页面数据不丢（localStorage）
```

> 注意：这是一个**示例输出**，展示 Project Brief 的样子。你自己的项目要按你的想法来。

---

## 拿到 Project Brief 之后

1. **检查**：逐条看，是不是你要的？不对就让 AI 改。
2. **拆需求**：进入 [Level 2](../learning-path/level-2.md)，把 Brief 拆成需求清单。
3. **拆任务**：进入 [Level 3](../learning-path/level-3.md)，把需求拆成小任务，开始让 AI 写代码。

---

## 下一步

- 学会拆需求 → [Level 2 — 学会理解项目](../learning-path/level-2.md)
- 避开新手坑 → [04-common-mistakes.md](04-common-mistakes.md)

> ⚠️ Not Yet Verified：以上 Project Brief 为示例，不代表该待办应用已被实现或验证。
