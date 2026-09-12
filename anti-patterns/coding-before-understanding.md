---
name: coding-before-understanding
description: 不理解项目就动手写代码——AI 最常见的错误。
category: workflow
---

# Coding Before Understanding 不理解就编码

## Bad Approach

用户说"改一下登录功能"，AI 直接搜 "login" 关键词，找到第一个匹配的文件就开始改。

## Why It Looks Reasonable

> 用户指定了功能，AI 找到了文件，直接改看起来很高效。

## Why It Actually Fails

- 关键词匹配 ≠ 问题所在（登录可能涉及 auth service / middleware / database）
- 不理解调用链可能改错文件
- 不理解项目规范可能引入不一致的代码风格
- 不理解测试结构可能破坏已有测试

## Better Approach

1. 走 [project-discovery](../skills/core/project-discovery/SKILL.md) 理解项目
2. 找到相关调用链
3. 确认要改的文件和函数
4. 再动手

## Example

```text
Bad:
用户："登录有问题"
AI：搜索 "login" → 改了 login.vue

Good:
用户："登录有问题"
AI：先走 project-discovery → 发现调用链：
  login.vue → authMiddleware → userService → db
→ 检查每层 → 发现 authMiddleware 的 JWT 校验有问题
→ 改 authMiddleware，不改 login.vue
```

## Prevention

- 改代码前先让 AI 复述调用链
- 设 Gate：不完成 project-discovery 不允许编码
- 使用 [New Project Workflow](../workflows/new-project/README.md) 或 [Feature Development Workflow](../workflows/feature-development/README.md)

## Related Skill

- [project-discovery](../skills/core/project-discovery/SKILL.md)
- [requirement-analysis](../skills/core/requirement-analysis/SKILL.md)
