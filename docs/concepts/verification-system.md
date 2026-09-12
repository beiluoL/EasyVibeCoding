# Verification System 验证体系

> EasyVibeCoding 的核心原则：**AI 的输出不是证据。** 验证必须基于客观证据。

## 验证分层

| Level | 名称 | 验证什么 | 谁执行 | 成本 | 什么时候需要 |
| --- | --- | --- | --- | --- | --- |
| 0 | AI Claim | AI 说"做完了" | AI | 极低 | 永远不够——这只是起点 |
| 1 | Static Validation | 文件存在、代码结构、语法检查 | AI | 低 | 每次都做 |
| 2 | Build Validation | 能否编译/构建 | AI | 低 | 每次都做 |
| 3 | Automated Tests | 单元/集成测试是否通过 | AI | 中 | 有测试时 |
| 4 | Behavior Validation | 手动触发功能是否正常 | 人或AI | 中 | 功能完成后 |
| 5 | Integration Validation | 多模块协作是否正常 | 人或AI | 高 | 涉及多模块时 |
| 6 | Real Environment | 真实环境（staging/prod） | 人 | 高 | 发布前 |
| 7 | Human Acceptance | 用户确认"这就是我要的" | 人 | 最高 | 发布前 |

## 核心规则

> Level 0 不是验证。它只是 AI 的声明。

> Level 1-3 是 AI 可以自动执行的。Level 4-7 需要人参与。

> 不是所有任务都需要 Level 7。根据 [风险等级](./risk-based-verification.md) 选择合理级别。

## 与 Verification Ladder 的关系

[Verification Ladder](./verification-ladder.md) 是早期版本（7 级），本文件是升级版（8 级，加了 Level 0 AI Claim 和 Level 7 Human Acceptance）。两者兼容，Ladder 的 Level 0-6 对应本体系的 Level 1-7。

## 延伸阅读

- [Verification Ladder](./verification-ladder.md)
- [Risk-Based Verification](./risk-based-verification.md)
- [Definition of Done](./definition-of-done.md)
- [Human Approval Matrix](./human-approval-matrix.md)
