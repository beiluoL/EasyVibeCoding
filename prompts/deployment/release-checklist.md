# 发布检查清单（release-checklist）

## Use When（何时使用）

> 功能开发完成、即将上线，需要过一遍发布前必查清单，确认可发布且可回滚。

## Goal（目标）

> 逐项核对发布前清单，每项给 ✅/❌+证据，全过才发布，并确保有回滚方案。

## Input Variables（输入变量）

- `{{release_scope}}`：本次发布包含的功能/变更范围。
- `{{acceptance_criteria}}`：对应的验收标准。
- `{{rollback_plan}}`：已有回滚方案（如无则需现场制定）。

## Prompt（提示词正文）

```
Role: 你是发布负责人，对"上线后出事能不能兜住"负责，而不是对"按时上线"负责。
Context: 发布范围：{{release_scope}}
验收标准：{{acceptance_criteria}}
回滚方案：{{rollback_plan}}
Goal: 逐项过发布前清单，给 ✅/❌+证据，全过才放行，并确认回滚方案可执行。
Constraints:
- 必须逐项核对，无相关也标注"不适用"，不跳过：
  1. 测试通过（自动化测试全绿，含正常/边界/错误路径）。
  2. 验收完成（每条验收标准有客观证据，参见 verify-feature）。
  3. 代码已评审（无 blocker，参见 code-review）。
  4. 密钥已清（无硬编码密钥/Token 入代码或配置）。
  5. 文档已更新（接口/部署/用户说明同步）。
  6. 回滚方案可执行（怎么回滚、谁执行、回滚后数据怎么办）。
  7. 监控告警就位（关键指标有告警，出事能被发现）。
- 任一 ❌ 即不可发布，指出卡在哪。
- 回滚方案不能是"出事再说"，要有具体步骤与触发条件。
- 未实际验证的项标注 ⚠️ Not Yet Verified，不得记 ✅。
Workflow:
1. 逐项核对 7 项清单，记录证据。
2. 确认回滚方案具体可执行。
3. 给出发布判定。
Output format:
| # | 检查项 | 判定 | 证据/说明 |
最终判定：可发布 / 不可发布 + 阻塞项
Verification: 回顾是否 7 项都留痕、每个 ✅ 有证据、回滚方案是否具体可执行、判定与清单是否一致。
```

## Expected Behavior（期望行为）

> 模型逐项核对清单，给客观证据，确保回滚方案具体可执行，任一不过就不放行。

## Expected Output（期望输出）

```
| 1 | 测试通过 | ✅ | 25用例全绿 |
| 2 | 验收完成 | ✅ | 3条标准逐条有证据 |
| 3 | 代码评审 | ❌ | 有1个 blocker 未修 |
| 4 | 密钥已清 | ✅ | 扫描无硬编码 |
| 5 | 文档已更新 | ⚠️ | 接口文档未更新 |
| 6 | 回滚方案 | ✅ | 回滚到上一版本，数据需修复脚本 |
| 7 | 监控告警 | ✅ | 关键接口已配告警 |
最终判定：不可发布。阻塞项：代码评审 blocker。
```

## Validation（验证）

- 7 项清单全部留痕（含"不适用"）。
- 每个 ✅ 有客观证据，无"看起来"式措辞。
- 回滚方案有具体步骤与触发条件，不是"出事再说"。

## Common Mistakes（常见错误）

- 只看测试绿就发布，漏掉密钥清理、文档更新、回滚方案。
- 回滚方案写"出事再回滚"，没有具体步骤和触发条件，真出事手忙脚乱。
- 把未验证的项偷偷记成 ✅，发布后才发现没监控。
- 因为"赶上线"放过 blocker，上线后出事且无法回滚。

## Related Skills（相关技能）

- [`../../skills/core/verification-before-completion/SKILL.md`](../../skills/core/verification-before-completion/SKILL.md)
- [`../../skills/core/code-review/SKILL.md`](../../skills/core/code-review/SKILL.md)

## Related Workflows（相关流程）

- [`../../workflows/release/README.md`](../../workflows/release/README.md)
