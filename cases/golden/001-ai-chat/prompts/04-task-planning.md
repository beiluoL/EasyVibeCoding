---
name: 04-task-planning
use_when: 把需求拆成可执行的小任务
goal: 从 Feature 拆到 Task 级，每个任务可独立验收
related_skill: skills/core/task-planning
status: experimental
verified: false
---

# Prompt 04 — 任务拆解

> 链接到 Skill：[task-planning](../../../../skills/core/task-planning/SKILL.md)

## Prompt

```
我的需求是：做一个 AI 聊天应用。

请帮我把需求拆成 Task 级小任务：
1. 每个任务目标明确（一句话说清做什么）
2. 每个任务标依赖顺序
3. 每个任务列出验收标准（做完怎么判定过了）
4. 每个任务列出会修改哪些文件

一个任务不要出现"和"字——出现就拆。
```

## Expected Output

- 任务列表（编号 + 目标 + 依赖 + 验收 + 文件范围）
- 任务关系图（Mermaid）

## Common Mistakes

- ❌ 任务太大（"做前端"而不是"做聊天 UI 页面"）
- ❌ 一个任务塞多个功能
