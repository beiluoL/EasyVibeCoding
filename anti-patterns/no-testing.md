# No Testing（不写测试）

> 反模式：不写测试，靠手动点一遍"看着对"就算完——没有客观标准，回归来了也察觉不到。

## Bad Approach

功能写完，AI 说"做完了"，你手动在界面上点几下，看着没报错就算交付。常见表现：

- 没有任何自动化测试
- 验收靠"我试了一下能用"
- 改了别处之后，不回头验旧功能有没有坏

## Why It Fails

- **没客观标准**：手动点一遍覆盖不了边界（空数据、超长输入、并发），"看着对"不等于"真的对"。
- **回归无感知**：改 A 功能把 B 功能改坏了，没人手动去点 B，问题就溜到线上才暴雷。
- **违反原则 04** Evidence over claims——要证据，别听 AI 自吹。AI 说"完成"只是声明，得看客观证据。

手动验证不可重复、不可批量，项目一大就完全失效。

## Better Approach

给每个功能配最小可验证测试：

1. 开工前先写验收标准（做到什么算完成）。
2. 实现后立刻配最小测试：一个能自动判定通过/失败的用例。
3. 优先覆盖"主流程 + 容易出错的边界"（空值、越界、权限）。
4. 每次改动后跑一遍测试套件，回归立刻暴露。

> 术语小贴士：**回归**（regression）= 改了 A，把本来没问题的 B 改坏了。

## Example

需求：笔记保存后返回 id。

❌ 不写测试：

```
AI 写完 saveNote，我在页面上新建了一条笔记，看到列表里有了，
就说"做完了"。
```

后来有人改了返回结构，id 变成 `note.id` 而不是 `id`，手动点页面看不出问题，接口调用方却崩了。

✅ 最小可验证测试：

```js
test('保存笔记返回 id', async () => {
  const res = await saveNote({ title: 't', content: 'c' });
  assert(res.id !== undefined, '应返回 id');
});
```

改返回结构后这条测试立刻红，回归当场被发现。

## Related Skill

- [testing](../skills/core/testing/SKILL.md) —— 给功能配可验证测试
- [verification-before-completion](../skills/core/verification-before-completion/SKILL.md) —— 任务收尾要有客观证据
- 原则 04 Evidence over claims：项目根 `README.md`
