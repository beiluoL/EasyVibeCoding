---
name: 06-debugging
use_when: 代码跑不起来或报错时
goal: 系统排查 Bug 根因，不靠猜
related_skill: skills/core/systematic-debugging
status: experimental
verified: false
---

# Prompt 06 — 系统化排障

> 链接到 Skill：[systematic-debugging](../../../../skills/core/systematic-debugging/SKILL.md)

## Prompt

```
我遇到一个问题：{{BUG_DESCRIPTION}}

请按系统化排障流程帮我排查：
1. Observe：先看清报什么错、什么时候错
2. Reproduce：帮我找到稳定复现的步骤
3. Collect Evidence：看日志、报错信息、网络请求
4. Locate：在嫌疑代码范围内二分定位
5. Hypothesis：提出根因假设
6. Verify Hypothesis：用最小手段验证假设
7. Fix：只改导致根因的那一处
8. Regression Test：跑回归验证

禁止猜测式修改。每步输出你的发现。
```

## Expected Output

- 8 步排障记录
- 根因说明
- 最小修复
- 回归验证结果

## Common Mistakes

- ❌ "可能是这里的问题，改了试试"——这不是 Debug 是赌博
- ❌ 一次改多个文件——改得越多越不知道是哪处修好的
