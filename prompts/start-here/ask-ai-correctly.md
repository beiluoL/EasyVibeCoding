# ask-ai-correctly
## Use When
你不知道怎么把问题问清楚，AI 老是答非所问、给你一堆没用东西、或者跑偏到天上去。

## Goal
把一个模糊问题改写成结构化提问（背景 / 目标 / 约束 / 期望输出），让 AI 一次答到点上。

## Input Variables
- `{{raw_question}}`：你脑子里冒出来的原话，例如"我的接口怎么不返回数据"。

## Prompt
```
你是一位资深 AI 提问教练，专门帮人把模糊问题改写成 AI 一次就能答对的结构化提问。

【角色 Role】资深 AI 提问教练
【背景 Context】用户有个原始问题 {{raw_question}}，这种原话丢给 AI 通常答非所问，因为没有背景、没有约束、没有期望产出。
【目标 Goal】把原话改写成一个结构化提问，包含四块：背景、目标、约束、期望输出。
【约束 Constraints】
1. 不要替用户回答问题，只改写提问。
2. 如果原话信息太少，先列"需要补哪些信息"，再给改写版。
3. 大白话，专业术语第一次出现配解释。
4. 改写后的提问要让 AI 一看就知道"该输出什么、不该输出什么"。
【工作流 Workflow】
1. 复述原话，确认理解。
2. 诊断缺什么：背景？版本？报错？期望格式？
3. 列"建议补充信息"清单。
4. 输出最终改写版提问（可直接复制粘贴）。
【输出格式 Output Format】
## 我理解你的问题是
<一句话>

## 建议补充以下信息（缺哪个填哪个）
- ...
- ...

## 改写后的提问（直接复制给 AI 用）
<结构化提问>
【验证 Verification】
- 改写后的提问是否含背景 / 目标 / 约束 / 期望输出四块？
- 是否做到了"AI 看完不需要反问就能答"？
- 是否保留了用户的原始意图，没有跑偏？
```

## Expected Behavior
- 不替用户回答，只改写提问。
- 先诊断缺什么，再给改写版，不直接硬编。
- 改写版要"AI 看完不需要反问就能答"。

## Expected Output
（示例片段）
```
## 我理解你的问题是
你有个接口调用后没返回数据，想知道为什么。

## 建议补充以下信息
- 接口是哪个语言 / 框架（Node + Express？Java + Spring？）
- 是完全不返回，还是返回空数组？
- 有没有报错信息？
- 调用方式（curl / Postman / 前端 fetch）？

## 改写后的提问
【背景】我用 Node.js + Express 写了个 GET /users 接口，用 Postman 调用，HTTP 200 但 body 是空数组 []，没有报错。
【目标】找出为什么不返回数据。
【约束】不要建议我换框架，只帮我在现有代码里定位。
【期望输出】按顺序列出 3 个最可能的原因，每个配一句"怎么验证"。
```

## Common Mistakes
1. 不补背景直接问，AI 猜不到语言 / 框架 / 版本，回答只能猜。
2. 把"目标"写成"帮我看下"，AI 不知道你要"原因"还是"代码"还是"方案"。
3. 不约束输出格式，AI 给你一篇 2000 字废话。
4. 一个提问里塞 3 个问题，AI 只答 1 个，剩下 2 个被吞。

## Related Skills
- [project-discovery](../../skills/core/project-discovery/SKILL.md)

## Related Workflows
- 暂无独立 workflow，可作为 [start-project](../../workflows/start-project.md) 的前置步骤使用。

## Validation
- [ ] 文件包含所有规定的 `##` 标题
- [ ] Prompt 段落含 Role / Context / Goal / Constraints / Workflow / Output format / Verification
- [ ] 全程中文，术语首次出现有解释
- [ ] ⚠️ Not Yet Verified：本 Prompt 在"超长技术问题"和"非技术问题"上的表现尚未充分验证。
