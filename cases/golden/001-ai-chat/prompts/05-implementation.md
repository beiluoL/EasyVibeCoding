---
name: 05-implementation
use_when: 按任务清单逐个实现
goal: 一次只做一个任务，做完验证再做下一个
related_skill: skills/core/implementation
status: experimental
verified: false
---

# Prompt 05 — 小步实现

> 链接到 Skill：[implementation](../../../../skills/core/implementation/SKILL.md)

## Prompt

```
请帮我实现 Task {{TASK_NUMBER}}：{{TASK_DESCRIPTION}}

要求：
1. 只做这一个任务，不要做其他任务的内容
2. 只修改任务指定的文件
3. 完成后告诉我：改了什么、为什么这样改、怎么验证
4. 如果遇到不确定的地方，先问我，不要自己猜
```

## Expected Output

- 修改了哪些文件
- 每处改动的理由
- 如何验证这个任务完成

## Common Mistakes

- ❌ 一次做多个任务
- ❌ 改了任务范围外的文件
- ❌ 不确定的地方自己猜
