---
name: 07-testing
use_when: 给功能配可验证测试
goal: 写自动化测试覆盖正常路径和错误路径
related_skill: skills/core/testing
status: experimental
verified: false
---

# Prompt 07 — 测试

> 链接到 Skill：[testing](../../../../skills/core/testing/SKILL.md)

## Prompt

```
请帮我给 {{FEATURE}} 写测试：

1. 正常路径：{{NORMAL_CASE}}
2. 错误路径：{{ERROR_CASE}}
3. 边界情况：{{EDGE_CASE}}

要求：
- 每个测试能独立运行
- 测试名说清"测了什么"
- 失败时输出有用的错误信息
```

## Expected Output

- 测试文件
- 测试用例列表
- 运行测试的命令

## Common Mistakes

- ❌ 只测正常路径不测错误路径
- ❌ 测试之间有依赖（A 必须先跑才能跑 B）
