# Anti-Pattern：Blind Debugging（盲目调试）

> ⚠️ Not Yet Verified

## Bad Approach

AI 收到报错后直接"猜改"——看到报错指向某个文件就动手改，不复现、不定位根因、不跑回归测试。

```
报错 → "可能是这里的问题" → 改 → "好像好了" → 下一个报错 → 继续猜改
```

## Why It Looks Reasonable

- AI 改 Bug 很快，看起来在推进——每轮都有改动。
- 如果碰巧改对了，会强化"直接试"的习惯。
- 系统化排查看起来"慢"——复现、收集证据要花时间。

## Why It Actually Fails

- 没复现就无法验证是否真的修好——"好像好了"不是验证。
- 改了根因还是改了表象？不知道——因为没有根因假设。
- 改一处碰坏另一处——没有回归测试。
- 十几轮后代码面目全非，原始 Bug 还在。

## Better Approach

走 [systematic-debugging](../skills/core/systematic-debugging/SKILL.md) 的 9 步流程：

```
Observe → Reproduce → Collect Evidence → Locate → Hypothesis → Verify → Fix → Regression Test → Document
```

每轮要求 AI 输出"根因假设 + 验证证据"，而不是"我又改了一处"。

## Example

**❌ Blind Debugging**：
```
报错：TypeError: Cannot read 'id' of undefined
AI：可能是 user 为空，加个 if 判断
→ 改完，报错没了
→ 但 user 拿不到 id 的原因（接口没返回）没人查
→ 下次另一个地方又报同样的错
```

**✅ Systematic Debugging**：
```
报错：TypeError: Cannot read 'id' of undefined
AI：先复现——什么操作会触发？
→ 复现：登录后跳转首页时触发
→ 收集证据：看接口返回，发现 /api/user 返回 {}
→ 定位：后端 userController.getUser 查询条件错了
→ 假设：userId 从 session 取值是 null
→ 验证：打印 session，确实是 null
→ 根因：session 设置时少存了 userId
→ 修复：修 session 设置逻辑，一处
→ 回归：原用例 ✅ + 相关测试 ✅
```

## Prevention

- 禁止"先改了再说"——改之前必须有根因假设。
- 设修改轮数上限（3 轮无进展就停，重新复现）。
- 每轮改完必须跑回归测试，不只看原报错消失。
- 使用 [debugging workflow](../workflows/debugging/README.md) 约束流程。

## Related Skill

- [systematic-debugging](../skills/core/systematic-debugging/SKILL.md)
- [verification-before-completion](../skills/core/verification-before-completion/SKILL.md)

## Related Failure

- [AI 无限 Debug 循环](../failures/debugging/01-ai-infinite-bug-fix.md)
