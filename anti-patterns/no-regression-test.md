---
name: no-regression-test
description: 修了 Bug 不跑回归测试——修好一个引入三个。
category: testing
---

# No Regression Test 无回归测试

## Bad Approach

AI 修了 Bug，只验证修的那个场景，不跑其他测试就宣布完成。

## Why It Looks Reasonable

> Bug 修了，那个场景能跑了——看起来确实修好了。

## Why It Actually Fails

- 修 Bug 可能引入新 Bug
- 改动可能影响其他功能
- 没有回归测试就不知道有没有破坏其他东西
- "修好一个引入三个"是常见后果

## Better Approach

1. 修完 Bug 后必须跑全部相关测试
2. 如果没有测试，先写测试再修
3. 使用 [Bug Fix Workflow](../workflows/bug-fix/README.md)

## Example

```text
Bad:
修了登录 Bug → 只测登录 → 提交
结果：注册功能被破坏了（共用 auth service）

Good:
修了登录 Bug → 跑全部测试 → 发现注册测试失败
→ 先修回归 → 全部通过 → 提交
```

## Prevention

- 修 Bug 后必须跑全部测试（不是只测修的那个）
- 使用 [fix-bug Prompt](../prompts/workflows/fix-bug.md) 强制跑回归
- 没有 auto test 的项目，至少手动测 3 个相关场景

## Related Skill

- [systematic-debugging](../skills/core/systematic-debugging/SKILL.md)
- [testing](../skills/core/testing/SKILL.md)
