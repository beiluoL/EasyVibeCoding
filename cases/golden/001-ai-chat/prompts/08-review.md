---
name: 08-review
use_when: 代码写完后做安全和质量检查
goal: 检查安全风险、代码质量、一致性
related_skill: skills/core/code-review
status: experimental
verified: false
---

# Prompt 08 — 代码评审

> 链接到 Skill：[code-review](../../../../skills/core/code-review/SKILL.md)

## Prompt

```
请帮我 review 以下代码：

{{CODE}}

检查项：
1. 安全：有没有 API Key 泄露？有没有 XSS 风险？
2. 质量：有没有不必要的复杂度？有没有重复代码？
3. 一致性：命名风格、代码风格是否一致？
4. 错误处理：所有失败路径是否覆盖？

逐项输出：✅ 通过 / ❌ 问题 + 修复建议
```

## Expected Output

- 4 项检查结果
- 问题列表 + 修复建议

## Common Mistakes

- ❌ 只看功能不查安全
- ❌ "看起来还行"——没逐项检查
