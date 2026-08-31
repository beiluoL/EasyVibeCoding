# start-project
## Use When
你有一个模糊想法但还没定义清楚要做什么。比如脑海里只有"我想做一个记账 App"这种一句话念头，不知道下一步该问什么、该写什么。

## Goal
把一个模糊想法变成一份清晰的 Project Brief（项目简介）：一句话目标 + 给谁用 + 核心痛点 + MVP（Minimum Viable Product，最小可用版本：只做最核心、能跑起来的那一版）。

## Input Variables
- `{{user_idea}}`：用户用大白话描述的想法，例如"我想做一个能提醒我交房租的 App"。

## Prompt
```
你现在是一位资深产品经理 + 架构师的合体，擅长把模糊想法拆成可执行方案。

【角色 Role】资深产品经理 + 架构师
【背景 Context】用户带来一个还不太成形的想法，需要你帮他从"一句话"走到"一份能交给开发的项目简介"。信息越早定义清楚，后面返工越少。
【目标 Goal】产出一份 Project Brief，包含：一句话目标、目标用户、核心痛点、MVP 范围（3-5 条）、明确不做什么（边界）、风险提示。
【约束 Constraints】
1. 不要一上来就写代码或选技术栈，这一步只定义"做什么"。
2. 全程用大白话，专业术语第一次出现要配一句解释。
3. 信息不够时先问关键问题，不要瞎猜、不要替用户做决定。
4. MVP 必须能在 1-2 周内做完，超出 5 条主动砍，砍掉的进"明确不做"。
5. 每条 MVP 需求要能对应到一个痛点。
【工作流 Workflow】
1. 先用一句话复述用户想法，确认理解无误（如果理解偏差，整个方向会跑偏）。
2. 问 3 个关键问题：① 用户是谁、什么场景下用？② 现在是怎么解决这个问题的？③ 最不能忍的痛点是什么？
3. 基于回答输出 Project Brief。
4. 最后给一句话风险提示（最可能让项目失败的因素）。
【输出格式 Output Format】
# Project Brief: <项目名>

## 一句话目标
<动词开头，一句话>

## 目标用户
<谁、什么场景>

## 核心痛点
<现在有多痛、为什么痛>

## MVP 范围（1-2 周可完成）
1. ...
2. ...
3. ...

## 明确不做
- ...

## 风险提示
<一句话>
【验证 Verification】
- 目标是否能一句话说清，别人听完能复述？
- MVP 每条是否都对应一个痛点？
- 砍掉的"明确不做"是否真的不影响核心？
- 用户是否确认了这个 Brief？
```
（把上面整段连同你的想法一起发给 AI）

## Expected Behavior
- 先复述确认理解，不直接开干。
- 问的问题聚焦"用户 / 痛点 / 现状"，不问技术细节。
- MVP 条数控制在 3-5 条，超出会主动砍进"明确不做"。
- 给出风险提示，让用户对最可能翻车的点有预期。

## Expected Output
（示例片段）
```
我先确认一下：你想做一个"到点提醒交房租"的 App，对吗？

在我给方案前，3 个问题：
1. 你是给自己用，还是给一群租客用？
2. 现在你是怎么记着交房租的（日历 / 备忘 / 经常忘）？
3. 最不能忍的是"忘了被房东催"还是"算不清金额"？

# Project Brief: 房租提醒小助手
## 一句话目标
让用户在房租到期前 3 天自动收到提醒，不再被房东催。
## 目标用户
合租 / 整租的年轻人，房租按月固定交。
## 核心痛点
现在靠脑子记，经常忘，被房东催很尴尬。
## MVP 范围（1-2 周可完成）
1. 手动录入一条房租（金额、到期日）。
2. 到期前 3 天自动弹通知。
3. 标记"已交"。
## 明确不做
- 多人分摊
- 历史报表
- 多房间管理
## 风险提示
最大风险是"通知打不到"——需要提前确认系统通知权限。
```

## Common Mistakes
1. 不复述直接开方案，理解偏差后整个方向跑偏，返工一周。
2. MVP 列了 10 条，2 周根本做不完，最后全废。
3. 一上来就聊"用 React 还是 Vue"，偏离了定义阶段。
4. "目标用户"写成"所有人"，等于没定义，等于没法做决策。

## Related Skills
- [project-discovery](../../skills/core/project-discovery/SKILL.md)
- [requirement-analysis](../../skills/core/requirement-analysis/SKILL.md)

## Related Workflows
- [start-project](../../workflows/start-project/README.md)

## Validation
- [ ] 文件包含所有规定的 `##` 标题（Use When / Goal / Input Variables / Prompt / Expected Behavior / Expected Output / Common Mistakes / Related Skills / Related Workflows / Validation）
- [ ] Prompt 段落含 Role / Context / Goal / Constraints / Workflow / Output format / Verification 七要素
- [ ] 全程中文，术语首次出现有解释
- [ ] ⚠️ Not Yet Verified：本 Prompt 尚未在实际项目中跑通验证，建议先在 1-2 个真实想法上试跑再大规模复用。
