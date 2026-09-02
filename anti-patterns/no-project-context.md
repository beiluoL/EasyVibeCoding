# No Project Context（不给项目上下文）

> 反模式：不告诉 AI 项目结构、技术栈、约定，直接让它写代码——它只能靠猜，产出必然不一致。

## Bad Approach

新开一个对话，不交代项目背景，直接说"帮我写一个用户注册接口"。常见表现：

- 不告诉 AI 用什么框架、什么版本
- 不说项目目录结构、已有工具函数
- 不交代命名约定、错误处理约定
- 每次对话都从零让 AI 猜

## Why It Looks Reasonable

- "需求很简单，就一个接口，不需要交代整个项目背景"——感觉过度准备。
- 以为 AI 能从代码片段推断出项目约定（框架、版本、风格）。
- 短对话里碰巧 AI 猜对了，让人误以为每次都能猜对。

## Why It Fails

- **AI 靠猜**：不知道项目用 Express 还是 Koa、用 CommonJS 还是 ESM、用不用 ORM，只能按最常见的写法生成，跟你项目对不上。
- **产出不一致**：同一个功能，不同对话里 AI 写法都不一样——这次用 fetch，下次用 axios，项目里冒出 N 种风格。
- **重复造轮子**：项目里已有 `formatError()` 工具函数，AI 不知道，又写一个，违反原则 03 Reuse before reinvent。
- **难合并**：AI 生成的代码风格、依赖跟项目对不上，硬塞进去到处冲突。

## Better Approach

动手前先做 project-discovery，把上下文给 AI：

1. 让 AI 先读项目结构：目录、依赖（package.json）、技术栈、版本。
2. 指出可复用的东西：已有的工具函数、配置、约定。
3. 说明命名/错误处理/分层约定。
4. 把这些上下文固定下来（写到 AGENTS.md 或项目说明），每次对话复用。

## Example

❌ 不给上下文：

```
帮我写一个用户注册接口。
```

AI 用 Express + mongoose 写，你项目其实是 Koa + Prisma，命名风格也对不上，改起来比重写还累。

✅ 先给上下文：

```
先读懂这个项目：看 package.json 和 src/ 目录结构，
告诉我技术栈、目录约定、已有的工具函数。
然后再实现"用户注册接口"，复用项目已有的校验和错误处理。
```

AI 先汇报"你用 Koa + Prisma，有 utils/validate.ts 和 utils/error.ts"，再按约定写，产出直接能并进项目。

## Prevention

- 每次新对话先贴项目上下文（技术栈、目录结构、约定），或用 [understand-project](../prompts/start-here/understand-project.md) 让 AI 先读。
- 把项目约定写进 `AGENTS.md`，AI 每次自动读取，不用手动重复。
- 检查 AI 产出是否符合项目已有风格（命名、依赖、分层），不符合就退回重做。

## Related Skill

- [project-discovery](../skills/core/project-discovery/SKILL.md) —— 先搞懂项目再动手
- [requirement-analysis](../skills/core/requirement-analysis/SKILL.md) —— 把需求拆给 AI
- [understand-project](../prompts/start-here/understand-project.md) —— 让 AI 先读懂项目
- 原则 01 Understand before coding：项目根 `README.md`
