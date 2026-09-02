---
name: build-feature
use_when: 给已有项目加一个新功能
goal: 让 AI 按 Understand→Inspect→Plan→Implement→Test→Review→Verify 7 步安全地完成一个功能
compatible: [unspecified]
status: experimental
verified: false
last_verified: null
---

# build-feature · 万能开发 Prompt

> ⚠️ Not Yet Verified — Prompt 模板已定义，尚未在真实项目中验证效果。

## Use When

- 用户说"我想增加：{{FEATURE}}"
- 给已有项目加新功能
- 需要一个端到端的开发流程

## Goal

用户只需要说"我想增加 XX"，AI 就按 7 步流程执行：理解需求 → 检查项目 → 拆任务 → 实现 → 测试 → 评审 → 验证。每步有 Hard Gate——不通过就不继续。

## Input Variables

| 变量 | 说明 | 示例 |
| --- | --- | --- |
| `{{FEATURE}}` | 用户想加的功能 | "用户注册登录" |

## Prompt

```
我要给现有项目增加一个功能：{{FEATURE}}

请按以下 7 步执行，每步有 Hard Gate——不通过不得继续：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Understand（理解需求）
- 用一句话说清这个功能要做什么
- 列出验收标准（做完怎么判定对了）
- 列出边界（做什么、不做什么）

GATE 1: 需求没有理解清楚 → 不得编码。
  判定：验收标准已列 + 用户已确认 → 通过

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 2: Inspect（检查项目）
- 这个功能涉及哪些现有模块？
- 改一个地方会影响哪里？
- 有没有可复用的已有代码？

GATE 2: 没有项目上下文分析 → 不得大规模修改。
  判定：已列出涉及模块 + 已标注影响范围 → 通过

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 3: Plan（拆任务）
- 把功能拆成 Task 级小任务（每个 < 半天）
- 每个任务标依赖顺序和验收点
- 标注哪些文件会被修改

GATE 2 → 通过后继续

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 4: Implement（实现）
- 按任务清单逐个实现
- 每完成一个任务跑一次相关测试
- 一次只改一个任务的范围

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 5: Test（测试）
- 跑全量测试
- 手动验证核心路径
- 验证错误场景（异常输入、边界条件）

GATE 3: 测试没有执行 → 不得声称完成。
  判定：测试全绿 + 核心路径通过 → 通过

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 6: Review（评审）
- 检查代码风格一致性
- 检查是否引入了安全风险
- 检查是否有不必要的复杂度

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 7: Verify（验证）
- 逐条核对验收标准
- 每条给出客观证据（测试名 / 请求结果）
- 有 ❌ 回 Step 4 修复

GATE 4: 验证没有通过 → 不得标记 Done。
  判定：所有验收标准 ✅ → 完成

━━━━━━━━━━━━━━━━━━━━━━━━━━━━

现在开始 Step 1。
```

## Expected Behavior

- AI 按顺序执行 7 步，不跳步
- 每步完成后暂停，展示 Hard Gate 判定结果
- Gate 不通过时不继续下一步
- 全部通过后输出验收报告

## Expected Output

```
Step 1: Understand ✅
  目标：<>
  验收标准：1. <> 2. <> 3. <>
  GATE 1: ✅ 通过

Step 2: Inspect ✅
  涉及模块：<>
  影响范围：<>
  GATE 2: ✅ 通过

...

Step 7: Verify ✅
  1. <> → ✅（证据：<>）
  2. <> → ✅（证据：<>）
  GATE 4: ✅ 全部通过
  完成判定：完成
```

## Validation

验证此 Prompt 是否有效：
1. 用 3 个不同功能（如"用户注册""搜索筛选""导出 PDF"）各跑一次完整 7 步。
2. 检查是否：AI 按顺序执行不跳步、每步 Hard Gate 有判定结果、Gate 不通过时停止。
3. 检查最终输出是否有逐条验收证据（不是"我觉得做完了"）。
4. 故意让 AI 在 Step 5 跳过错误场景，确认 Gate 3 能拦住。
5. 收集至少 2 个真实使用案例后，更新 verified 与 last_verified 字段。

## Common Mistakes

- ❌ 跳过 Step 2 直接写代码——不理解项目就改，会碰坏别的模块
- ❌ 一个 Prompt 塞多个功能——每个功能独立走一次 7 步
- ❌ Gate 不通过就继续——Gate 存在就是为了拦住"自以为做完了"
- ❌ 验证只做正常路径——错误场景不验等于没验

## Related Skills

- [project-discovery](../../skills/core/project-discovery/SKILL.md) — Step 2 用到
- [task-planning](../../skills/core/task-planning/SKILL.md) — Step 3 用到
- [implementation](../../skills/core/implementation/SKILL.md) — Step 4 用到
- [testing](../../skills/core/testing/SKILL.md) — Step 5 用到
- [code-review](../../skills/core/code-review/SKILL.md) — Step 6 用到
- [verification-before-completion](../../skills/core/verification-before-completion/SKILL.md) — Step 7 用到

## Related Workflows

- [feature-development](../../workflows/feature-development/README.md) — 完整的功能开发工作流
