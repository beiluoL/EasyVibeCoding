# Testing 示例 — 给"创建笔记"写 3 个测试

## 输入

功能：POST /api/notes 创建笔记接口。

验收标准：
1. 正常请求返回 201 并含新笔记
2. title 为空返回 400

## 1. 从验收标准挑可测点

| 可测点 | 输入 | 期望 |
|--------|------|------|
| 正常创建 | title + content | 201 + 笔记数据 |
| 空标题 | title 为空 | 400 |
| 超长标题 | title 10001 字符 | 400（应有长度限制） |

## 2. 写测试（先红后绿）

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

// 边界：超长标题
test('超长标题返回 400', async () => {
  const longTitle = 'a'.repeat(10001);
  const res = await request(app)
    .post('/api/notes')
    .send({ title: longTitle, content: '内容' });
  expect(res.status).toBe(400);
});
```

## 3. 先红后绿过程

```
第一轮跑：
  正常路径   ✅（代码已满足）
  空标题     ✅（代码已满足）
  超长标题   ❌ 红（代码没有长度限制，返回 201）

→ 在接口里加长度校验：
  if (title.length > 10000) return res.status(400)...

第二轮跑：
  正常路径   ✅
  空标题     ✅
  超长标题   ✅ 绿
```

先红证明了"超长标题"这个测试真的在测东西——如果一开始就绿，说明要么代码已经有限制，要么测试没写对。

## 4. 产出

```
功能：创建笔记
可测点：正常201 / 空标题400 / 超长标题400
测试用例：
  - 正常：title+content → 201 ✅
  - 边界：空title → 400 ✅
  - 边界：10001字符title → 400 ✅
结果：3/3 ✅
```

三条测试全绿且可独立重复运行。现在"创建笔记做完了"不再是感觉，而是测试通过的客观事实。
