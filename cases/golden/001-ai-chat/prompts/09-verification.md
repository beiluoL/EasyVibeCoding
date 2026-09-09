---
name: 09-verification
use_when: AI 说"做完了"时，逐条验证
goal: 按验收标准逐条核对，有证据才算完成
related_skill: skills/core/verification-before-completion
status: experimental
verified: false
---

# Prompt 09 — 完工前验证

> 链接到 Skill：[verification-before-completion](../../../../skills/core/verification-before-completion/SKILL.md)

## Prompt

```
AI 说完成了{{FEATURE}}。

请帮我逐条验证验收标准：
{{ACCEPTANCE_CRITERIA}}

每条验证：
1. 执行验证（跑命令/发请求/看文件）
2. 记录结果：✅ 通过 + 证据 / ❌ 未通过 + 原因
3. 有 ❌ 的回到实现阶段修复

全部 ✅ 才算完成。
```

## Expected Output

- 验收标准逐条验证表
- 每条的客观证据
- 最终判定：完成 / 未完成

## Common Mistakes

- ❌ "AI 说做完了就信了"——这不是验证
- ❌ 只验证正常路径不验错误场景
- ❌ "看着能跑"就算过了——要有客观证据
