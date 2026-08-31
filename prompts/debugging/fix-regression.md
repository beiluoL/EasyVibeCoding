# fix-regression
## Use When
一个原本好的功能突然坏了（昨天还能跑今天报错、上线后某功能失效），怀疑是某次改动引入的。

## Goal
定位是哪次改动引入了回归（Regression，回归：原本好的功能变坏了），然后给最小回滚 / 修复方案。

## Input Variables
- `{{broken_feature}}`：坏了的功能描述 + 现在的现象。
- `{{last_known_good}}`（可选）：最后一次确认还好的时间点 / commit。
- `{{recent_changes}}`（可选）：最近改了哪些东西（commit 列表 / 文件列表）。

## Prompt
```
你是一位资深调试工程师，擅长用"二分回滚"定位回归引入点。

【角色 Role】资深调试工程师
【背景 Context】用户有个功能原本好好的，现在坏了：{{broken_feature}}。最后一次确认还好的时间 / commit：{{last_known_good}}。最近改动：{{recent_changes}}。
【目标 Goal】定位是哪次改动引入的回归，给最小回滚 / 修复方案。
【约束 Constraints】
1. 先确认"真的坏了"——跑一遍当前版本，确认能稳定复现。
2. 用二分回滚定位：在"最后一次好的"和"现在"之间二分，找到第一个坏的版本 / commit。
3. 找到引入点后，先讲清楚"那次改动里哪一行导致"，不只说"是这次 commit"。
4. 优先最小回滚（撤销那一行 / 那个改动），回滚不了再就地修复。
5. 修复后必须跑回归（坏的功能恢复 + 没引入新问题）。
6. 大白话，术语第一次出现配解释。
7. 不顺手重构 / 加功能，只修回归。
【工作流 Workflow】
1. 复现：跑当前版本，确认坏现象稳定出现。
2. 二分回滚：在 last_known_good 和 HEAD 之间二分 commit / 改动，找第一个坏版本。
3. 定位：在那个坏版本里找"哪一行改动导致"。
4. 根因：讲清"那次改动因为 X，所以 Y 坏了"。
5. 最小回滚 / 修复：优先撤销那一行；不能撤销就就地补最小修复。
6. 回归验证：坏功能恢复 + 相关功能没坏。
【输出格式 Output Format】
## 1. 复现确认
- 现象：<>
- 能稳定复现：是 / 否

## 2. 二分回滚
- last_known_good：<commit / 时间>
- HEAD：<commit / 时间>
- 二分过程：<试 commit A 坏 → 试 commit A-1 好 → 引入点在 A>
- 引入点：<commit hash + 改动文件>

## 3. 根因
<那次改动因为 X，所以 Y 坏了>

## 4. 最小回滚 / 修复
- 方案：回滚 / 就地修复（二选一）
```<语言> <文件>
<改动>
```
- 为什么这么改能修：<一句>

## 5. 回归验证
1. 坏功能：<跑什么> → 恢复正常
2. 相关功能：<跑什么> → 不受影响
【验证 Verification】
- 是否确认了"真的坏了"？
- 二分是否找到了第一个坏版本？
- 根因是否讲了"那次改动为什么导致坏"？
- 修复是否最小？回归是否跑了两组？
```

## Expected Behavior
- 先确认真的坏，避免"环境问题"误判为回归。
- 二分找引入点，不一个个 commit 试。
- 优先回滚，回滚不了再就地修。
- 回归跑两组：坏功能恢复 + 相关不受影响。

## Expected Output
（示例片段）
```
## 1. 复现确认
- 现象：提交周报返回 500
- 能稳定复现：是

## 2. 二分回滚
- last_known_good：commit abc1234（周二早上的版本）
- HEAD：commit def5678（今早）
- 二分过程：试 commit mid(abc, def) 坏 → 试 abc+1 好 → 引入点在 abc+2 到 mid 之间 → 试 abc+2 好 → abc+3 坏
- 引入点：commit xyz9999，改了 services/user.js

## 3. 根因
那次改动把 user 对象从"一定有值"改成了"可能返回 null"，但调用方 routes/report.js:24 没加判空，所以 null 时 500。

## 4. 最小回滚 / 修复
- 方案：就地修复（回滚整个 commit 会丢掉其他有用改动）
```js routes/report.js
const name = user?.name || '匿名';
```
- 为什么这么改能修：user 为 null 时兜底，不再 500。

## 5. 回归验证
1. 提交周报 → 不再 500，返回"hi 匿名"
2. 老用户提交 → 仍"hi 张三"，那次 commit 的其他改动也还在用。
```

## Common Mistakes
1. 不确认"真的坏了"就开查，最后发现是本地环境 / 缓存问题。
2. 不用二分，一个个 commit 试，10 个 commit 试半天。
3. 直接回滚整个 commit，把里面其他有用改动也丢了。
4. 只跑坏功能不跑相关用例，回滚 / 修复后又引入新回归。
5. 不讲根因只说"这次 commit 引入的"，下次同类问题还是不会查。

## Related Skills
- [systematic-debugging](../../skills/core/systematic-debugging/SKILL.md)
- [testing](../../skills/core/testing/SKILL.md)

## Related Workflows
- [debugging](../../workflows/debugging/README.md)

## Validation
- [ ] 文件包含所有规定的 `##` 标题
- [ ] Prompt 段落含 Role / Context / Goal / Constraints / Workflow / Output format / Verification
- [ ] 全程中文，术语首次出现有解释
- [ ] ⚠️ Not Yet Verified：本 Prompt 在"无 git 历史"或"超大改动单 commit"场景下的二分策略未充分验证，可能需要补日志埋点。
