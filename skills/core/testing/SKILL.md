---
name: testing
description: 为功能写"最小可验证的测试"，让"做完"有客观标准，而不是靠人感觉。
version: 0.1.0
category: core
difficulty: intermediate
status: experimental
verified: false
compatible: [unspecified]
prerequisites:
  - 功能的验收标准已定义
  - 项目已配置测试框架
inputs:
  - 验收标准
  - 待测功能代码
outputs:
  - 可运行的测试用例
  - 测试通过/失败结果
triggers:
  - 实现完一个功能，需要补测试
  - 需要为"做完"提供客观证据
  - 修复 Bug 后需要回归测试
validation:
  - 测试能独立运行
  - 测试结果可重复
  - 覆盖正常、边界、错误三类路径
last_verified: null
---

# Testing（最小可验证测试）

> ⚠️ Not Yet Verified

## Purpose

给功能写**最小可验证的测试**，让"做完"这件事有客观标准。

没有测试时，"做完"全靠人感觉——感觉对就是做完了。有测试后，测试跑过才算完，跑不过就是没完。

## When to Use

- 实现完一个功能，需要确认它真的能用。
- 修复一个 Bug 后，需要回归测试防止再犯。
- 需要给 verification-before-completion 提供客观证据。

## Trigger Conditions

- 一个功能实现完成，进入验收阶段。
- 用户问"这个功能做完了没 / 对不对"。
- systematic-debugging 修完 Bug 后补回归测试。

## Preconditions

1. 功能的验收标准已定义（至少知道正常情况该返回什么）。
2. 项目已配置测试框架（如 Jest、Pytest、JUnit 等）。
3. 被测代码能独立运行。

## Workflow

1. **从验收标准挑可测点**：把"功能应该怎样"翻译成"输入 X 应该得到 Y"。可测点 = 能用输入输出表达的验收标准。
2. **写最小测试（先红后绿）**：先写测试，跑一遍确认它失败（红），再写或改代码让它通过（绿）。先红是为了证明测试真的在测东西。
3. **覆盖正常 + 边界 + 错误路径**：
   - 正常：典型输入，应该成功。
   - 边界：极端输入（空值、超长、特殊字符），应该合理处理。
   - 错误：非法输入，应该拒绝并给明确错误。
4. **跑通 = 完成的客观证据**：测试全绿，这个功能才算"做完"。

### 术语解释

- **先红后绿**：先写一个会失败的测试（红），再写代码让它通过（绿）。如果一开始就绿，说明测试可能根本没在测这个功能。
- **边界**：极端输入，比如空字符串、超长字符串、特殊字符、0、负数。这些地方最容易出 Bug。
- **回归测试**：修完 Bug 后跑的测试，确认没把原来好的功能改坏。

## Rules

- **不追求 100% 覆盖率**，追求关键路径有测试。覆盖率是手段不是目的。
- **测试要快**：单测应该秒级跑完，否则没人愿意跑。
- **测试要独立**：测试之间不能有依赖，先跑 A 再跑 B 才过——这是坏味道。
- **测试要可重复**：同样输入每次结果一样，不能"有时过有时不过"。
- 一个测试只测一件事。混在一起出错了不知道是哪条挂的。

## Anti-Patterns

- ❌ 不写测试只靠手动点——慢、不可重复、容易漏。
- ❌ 测试依赖顺序——A 必须先跑 B 才过。
- ❌ 写一堆慢测试——跑一次要几分钟，最后没人跑。
- ❌ 只测正常路径——边界和错误才是 Bug 高发区。
- ❌ 测试里塞复杂逻辑——测试本身应该是"输入→断言"，简单直白。

## Validation

> 本技能 V0.1 新写，尚未经实际运行验证。

**Expected Validation Steps**：
1. 在真实项目里为 3 个功能各写正常/边界/错误三类测试。
2. 检查测试是否：能独立跑、可重复、秒级完成。
3. 故意引入一个 Bug，确认测试能抓到。
4. 收集至少 2 个真实使用案例后，更新 verified 与 last_verified 字段。

验证状态：⚠️ Not Yet Verified — 待按 Expected Validation Steps 实际运行后更新。

## Output Format

```
功能：<名称>
可测点：<从验收标准挑出的>
测试用例：
  - 正常：<输入 → 期望>
  - 边界：<输入 → 期望>
  - 错误：<输入 → 期望>
结果：✅/❌
```

## Example

给"创建笔记"接口写 3 个测试。

验收标准：
1. 正常请求返回 201。
2. title 为空返回 400。

挑可测点 → 写 3 个测试：

```js
// 正常路径
test('正常创建笔记返回 201', async () => {
  const res = await request(app)
    .post('/api/notes')
    .send({ title: '标题', content: '内容' });
  expect(res.status).toBe(201);
  expect(res.body.title).toBe('标题');
});

// 边界：空标题
test('空标题返回 400', async () => {
  const res = await request(app)
    .post('/api/notes')
    .send({ title: '', content: '内容' });
  expect(res.status).toBe(400);
});

// 边界：超长标题（超过 10000 字符）
test('超长标题返回 400', async () => {
  const longTitle = 'a'.repeat(10001);
  const res = await request(app)
    .post('/api/notes')
    .send({ title: longTitle, content: '内容' });
  expect(res.status).toBe(400);
});
```

先红后绿：先跑确认前两条能过（已有代码满足），第三条超长标题当前没限制 → 红。加一行长度校验后 → 绿。

```
功能：创建笔记
可测点：正常返回201 / 空标题400 / 超长标题400
测试用例：
  - 正常：title+content → 201 ✅
  - 边界：空title → 400 ✅
  - 边界：10001字符title → 400 ✅
结果：3/3 ✅
```

三条测试全绿，"创建笔记"这个功能才算有了客观的"做完"证据。
