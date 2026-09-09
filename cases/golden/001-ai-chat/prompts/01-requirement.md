---
name: 01-requirement
use_when: 开始一个新项目或功能时，先分析需求
goal: 把模糊想法变成清晰的验收标准
related_skill: skills/core/requirement-analysis
status: experimental
verified: false
---

# Prompt 01 — 需求分析

> 链接到 Skill：[requirement-analysis](../../../../skills/core/requirement-analysis/SKILL.md)

## Prompt

```
我要做一个{{PROJECT}}。

请帮我分析需求：
1. 用一句话说清这个项目做什么
2. 列出必须有的功能（MVP）
3. 列出暂时不做的功能
4. 为每个功能写验收标准（做完怎么判定对了）

先不要写代码。只输出需求清单。
```

## Expected Output

- 一句话项目定义
- MVP 功能列表 + 验收标准
- Out of Scope 列表

## Common Mistakes

- ❌ 跳过需求分析直接写代码
- ❌ 需求写得太笼统（"做一个聊天系统" vs "用户能输入消息并收到 AI 回复"）
