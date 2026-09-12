# Definition of Done 完成标准

> 一个任务什么算"完成"？不是 AI 说"做完了"就算。

## 完成条件

一个任务只有在以下条件全部满足时才算完成：

```text
1. Requirements satisfied — 需求满足
2. Code implemented — 代码实现
3. Build passes — 构建通过
4. Tests pass — 测试通过
5. Review completed — Review 完成
6. Verification completed — 验证完成
7. Documentation updated if necessary — 文档更新（如有必要）
8. No known blocking issue remains — 无已知阻塞问题
```

## 不要要求所有任务都执行所有级别

> 根据 [风险等级](./risk-based-verification.md) 选择合理验证级别。

| 风险 | 最低验证级别 | 示例 |
| --- | --- | --- |
| Low | Level 1-2 | 改 README、改注释 |
| Medium | Level 3 | 改业务逻辑、加功能 |
| High | Level 4-5 | 改数据库、改 API |
| Critical | Level 6-7 | 生产发布、支付、用户数据 |

## Done ≠ 代码已生成

| ❌ Done | ✅ Done |
| --- | --- |
| 代码已生成 | 需求满足 + 测试通过 + Review 通过 + 验证通过 |
| AI 说"完成了" | 有证据证明完成了 |
| 文件有改动 | 构建通过 + 测试通过 + 无已知问题 |

## 延伸阅读

- [Verification System](./verification-system.md)
- [Risk-Based Verification](./risk-based-verification.md)
- [Human Approval Matrix](./human-approval-matrix.md)
