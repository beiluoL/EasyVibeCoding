# refactor-code
## Use When
代码能跑，但写得乱（函数太长、命名糟、重复多、嵌套深），想改善结构又怕改坏。

## Goal
在不改变外部行为（输入输出不变）的前提下改善代码结构，标出 before / after，让人能 review。

## Input Variables
- `{{code_snippet}}`：要重构的代码。
- `{{refactor_goal}}`（可选）：重构目标，如"函数太长拆开""命名改清楚""去掉重复"。

## Prompt
```
你是一位资深重构工程师，信奉"小步重构、行为不变"，每次只改一类问题。

【角色 Role】资深重构工程师
【背景 Context】用户有一段能跑但写得乱的代码：{{code_snippet}}。重构目标：{{refactor_goal}}。要求行为不变，只改结构。
【目标 Goal】输出 before / after 对比 + 改动说明，让人能 review 每一处。
【约束 Constraints】
1. 行为不变：对外接口 / 输入输出必须一致，重构后跑同样用例结果相同。
2. 一次只改一类问题（要么拆函数，要么改命名，要么去重复），不混改。
3. 每处改动必须能说清"为什么这么改"，不能"我觉得更好看"。
4. 不要顺手加新功能、新参数、新分支。
5. 大白话，术语第一次出现配解释。
6. 给"怎么验证行为没变"的步骤（跑什么、看什么）。
【工作流 Workflow】
1. 先读代码，找出主要问题（命名 / 长函数 / 重复 / 嵌套）。
2. 选一类最痛的问题先改（不混改）。
3. 输出 before / after 对比 + 每处改动的理由。
4. 给"行为不变"的验证步骤。
5. 如果还有其他问题没改，列在"后续建议"里，不在本次顺手改。
【输出格式 Output Format】
## 主要问题
1. ...
2. ...

## 本次改哪类
<只改一类，比如"拆长函数">

## Before / After
### Before
```<语言>
<原代码>
```
### After
```<语言>
<新代码>
```

## 改动说明
- 第 X 行 → 第 Y 行：<为什么这么改>

## 行为不变验证
1. 跑 `xxx`
2. 输入 `a` 应输出 `b`（跟 before 一样）

## 后续建议（不在本次改）
- ...
【验证 Verification】
- 行为是否真不变？（接口 / 输入输出一致）
- 是否只改了一类问题，没混改？
- 每处改动是否有"为什么"？
- 是否给了验证步骤？
```

## Expected Behavior
- 行为严格不变，接口 / 输入输出一致。
- 一次只改一类问题，不顺手混改。
- 每处改动都有"为什么"，不是"我觉得好看"。
- 给"行为不变"的验证步骤。

## Expected Output
（示例片段）
```
## 主要问题
1. calculateTotal 函数 80 行，干 3 件事。
2. 变量 a / b / c 命名无意义。

## 本次改哪类
只改"拆长函数"。

## Before / After
### Before
```js
function calculateTotal(items, tax, discount) {
  // 80 行混在一起
}
```
### After
```js
function calculateSubtotal(items) { /* 只算小计 */ }
function applyDiscount(subtotal, discount) { /* 只算折扣 */ }
function calculateTotal(items, tax, discount) {
  return applyDiscount(calculateSubtotal(items), discount) * (1 + tax);
}
```

## 改动说明
- 拆成 3 个函数：单一职责（一个函数只干一件事），便于单独测试。

## 行为不变验证
1. 跑 `node test/calc.test.js`
2. 6 组输入输出应跟 before 完全一致。
```

## Common Mistakes
1. 重构顺手加新功能 / 新参数，行为变了还以为没改坏。
2. 一次改 5 类问题（命名 + 拆函数 + 换库 + 去重复），review 不动，回滚也回不动。
3. 不给验证步骤，重构完没法证明行为没变。
4. 理由写"这样更优雅"，没说解决了什么实际问题。

## Related Skills
- [implementation](../../skills/core/implementation/SKILL.md)
- [code-review](../../skills/core/code-review/SKILL.md)

## Related Workflows
- 暂无独立 workflow，可作为 [feature-development](../../workflows/feature-development.md) 的"质量回填"环节。

## Validation
- [ ] 文件包含所有规定的 `##` 标题
- [ ] Prompt 段落含 Role / Context / Goal / Constraints / Workflow / Output format / Verification
- [ ] 全程中文，术语首次出现有解释
- [ ] ⚠️ Not Yet Verified：本 Prompt 在"无测试覆盖"老代码上的行为不变性保障未充分验证，强烈建议先补测试再重构。
