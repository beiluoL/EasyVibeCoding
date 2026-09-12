---
name: giant-task
description: 把整个项目塞进一个任务——AI 会失控。
category: workflow
---

# Giant Task 超级任务

## Bad Approach

用户说"帮我做一个 AI 聊天网站"，AI 直接开始生成 index.html + app.js + server.js + package.json，一次改十几个文件。

## Why It Looks Reasonable

> 一句话需求 → 一次性生成 → 看起来很高效。AI 似乎能处理大任务。

## Why It Actually Fails

- 任务太大时 AI 无法保持一致性
- 改一处可能在另一处引入问题
- 出错时无法定位是哪步的锅
- 无法逐个验证——测试不通过时不知道先改哪个
- 代码质量和结构通常很差

## Better Approach

1. 走 [task-planning](../skills/core/task-planning/SKILL.md) 拆成小任务
2. 每个任务目标明确、范围可控
3. 做完一个验证一个
4. 使用 [Feature Development Workflow](../workflows/feature-development/README.md)

## Example

```text
Bad:
"做一个 AI 聊天网站" → AI 一次生成 10+ 文件

Good:
"做一个 AI 聊天网站"
→ Task 01: 初始化项目
→ Task 02: 创建基础页面
→ Task 03: 创建 Chat API
→ ...（每个独立验证）
```

## Prevention

- 一个任务如果出现"和"字就拆
- 设 Gate：任务范围超过 3 个文件就拆
- 使用 [build-feature Prompt](../prompts/workflows/build-feature.md) 强制走 7 步

## Related Skill

- [task-planning](../skills/core/task-planning/SKILL.md)
- [implementation](../skills/core/implementation/SKILL.md)
