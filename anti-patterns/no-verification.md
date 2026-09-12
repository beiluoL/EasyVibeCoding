---
name: no-verification
description: AI 说"完成了"就信了——不做验证。
category: verification
---

# No Verification 不验证

## Bad Approach

AI 说"登录功能已经完成"，用户直接相信，不做任何验证。

## Why It Looks Reasonable

> AI 看起来很自信，代码也确实写了，测试也写了——看起来不需要再验证了。

## Why It Actually Fails

- 代码写了 ≠ 能跑
- 测试写了 ≠ 测试通过
- 功能做了 ≠ 满足需求
- AI 的自我评价不等于客观证据

## Better Approach

1. 走 [verification-before-completion](../skills/core/verification-before-completion/SKILL.md)
2. 逐条核对验收标准
3. 每条有客观证据（命令输出/截图/测试结果）
4. 使用 [verify-task Prompt](../prompts/verification/verify-task.md)

## Example

```text
Bad:
AI："登录功能已完成" → 用户信了

Good:
AI："登录功能已完成"
人："逐条验证"
→ 代码存在？✅
→ Build 通过？✅
→ 测试通过？❌ 2/5 失败
→ 接口能调？✅
→ 错误场景正常？❌ 空密码崩溃
→ 结论：未完成，回去修
```

## Prevention

- 禁止用 "Done"——用 Validated 或 Failed
- 设 Verification Gate：不验证不算完成
- AI 说完成时自动触发 [verify-task](../prompts/verification/verify-task.md)

## Related Skill

- [verification-before-completion](../skills/core/verification-before-completion/SKILL.md)
