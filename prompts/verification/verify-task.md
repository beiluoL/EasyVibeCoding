---
name: verify-task
use_when: AI 说"完成了"时，逐条验证
goal: 按验收标准逐条核对，有证据才算完成
related_skill: skills/core/verification-before-completion
status: experimental
verified: false
---

# Prompt — 完工验证

> 链接到 Skill：[verification-before-completion](../../skills/core/verification-before-completion/SKILL.md)

## Use When

AI 说"完成了"时，逐条验证

## Goal

按验收标准逐条核对，有证据才算完成

## Input Variables

- `{{TASK}}` — AI 声称完成的任务名称
- `{{ACCEPTANCE_CRITERIA}}` — 验收标准清单

## Expected Behavior

- AI 逐条验证，不跳步
- 每条给出客观证据（命令输出/测试结果/截图）
- 不根据自己的回答判断完成——必须基于证据

## Validation

- 7 项验证全部有 ✅/❌ 标记
- 每项有客观证据
- 最终判定为 PASS / PARTIAL / FAIL

## Prompt

```
AI 说完成了{{TASK}}。

请逐条验证以下验收标准：
{{ACCEPTANCE_CRITERIA}}

每条验证步骤：
1. Requirement — 需求是否满足？
2. Changed Files — 改了哪些文件？是否在范围内？
3. Build — 能否编译/构建？
4. Tests — 测试是否通过？通过率？
5. Behavior — 手动触发功能是否正常？
6. Known Issues — 有无已知问题？
7. Remaining Risks — 有无剩余风险？

每条输出：✅ 通过 + 证据 / ❌ 未通过 + 原因

最终输出：PASS / PARTIAL / FAIL
不要根据自己的回答判断完成——必须基于证据。
```

## Expected Output

- 7 项验证结果表
- 每条的客观证据
- 最终判定：PASS / PARTIAL / FAIL

## Common Mistakes

- ❌ "看起来能跑"就算 PASS
- ❌ 只验正常路径不验错误场景
- ❌ AI 自己验证自己——应该用第二个视角
