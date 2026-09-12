---
name: uncontrolled-production-change
description: AI 直接改生产环境——不可逆灾难。
category: deployment
---

# Uncontrolled Production Change 不可控生产变更

## Bad Approach

AI 直接在生产数据库执行 `DROP TABLE`，或直接修改生产配置文件，无人确认。

## Why It Looks Reasonable

> AI 被要求"清理旧数据"，它找到了 DELETE 语句并执行。看起来就是执行了用户指令。

## Why It Actually Fails

- 生产操作不可逆
- AI 不理解"生产"的含义
- 没有备份就改 = 灾难
- 一旦出错无法回滚

## Better Approach

1. 生产操作必须经过 [Release Workflow](../workflows/release/README.md)
2. 任何破坏性操作必须人工确认
3. 使用 [Human Approval Matrix](../docs/concepts/human-approval-matrix.md)
4. 先在 staging 验证

## Example

```text
Bad:
AI："清理旧数据" → 执行 DELETE FROM users WHERE last_login < '2024'

Good:
AI："我准备执行 DELETE FROM users WHERE..."
人："等等，这是生产库吗？" → 确认是
人："先在 staging 跑一遍" → staging 验证通过
人："备份了吗？" → 备份完成
人："执行" → AI 执行
```

## Prevention

- 生产环境操作必须 Human Gate
- 破坏性 SQL 必须人工确认
- 使用 [Human Approval Matrix](../docs/concepts/human-approval-matrix.md)
- 在 [Release Workflow](../workflows/release/README.md) 中设强制 Gate

## Related Skill

- [verification-before-completion](../skills/core/verification-before-completion/SKILL.md)
