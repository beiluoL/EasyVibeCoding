# Code Review 示例 — 评审有 SQL 拼接漏洞的 AI 代码

## 输入

待评审代码（AI 生成的创建笔记接口）：

```js
router.post('/api/notes', async (req, res) => {
  const { title, content } = req.body;
  const sql = "INSERT INTO notes (title, content) VALUES ('" + title + "','" + content + "')";
  await db.query(sql);
  res.status(201).json({ ok: true });
});
```

验收标准：正常返回 201 + 笔记；空 title 返回 400。

## 1. 对清单逐项过

| 清单项 | 结果 | 说明 |
|--------|------|------|
| 满足验收标准 | ❌ | 未返回笔记数据，未校验空 title |
| 未处理错误 | ❌ | 无 try/catch，db 失败即崩 |
| 硬编码密钥/路径 | ✅ | 无 |
| SQL 注入风险 | ❌ | 拼接用户输入到 SQL |
| XSS 风险 | ✅ | 不涉及输出渲染 |
| 重复代码 | ✅ | 无 |
| 命名清楚 | ✅ | — |
| 需要测试 | ❌ | 关键路径无测试 |

## 2-3. 问题列表（等级 + 位置 + 理由 + 建议）

```
[blocker] db.query 拼接 title/content
  理由：直接拼接用户输入到 SQL 字符串，存在 SQL 注入。
        用户输入 title = '; DROP TABLE notes; -- 即可攻击。
  建议：改用参数化查询
        db.query('INSERT INTO notes (title, content) VALUES (?, ?)', [title, content])

[blocker] 无错误处理
  理由：db.query 失败时无 try/catch，请求直接挂掉，前端收不到响应。
  建议：包 try/catch，失败返回 500

[warn] 未返回新笔记数据
  理由：验收标准要求返回 201 + 笔记，当前只返回 { ok: true }。
  建议：返回插入后的笔记数据（含 id）

[warn] 未校验空 title
  理由：验收标准要求空 title 返回 400，当前直接入库。
  建议：开头加 if (!title) return res.status(400)...

[nit] 可返回 insertId
  理由：前端创建后可能需要 id 做后续操作。
  建议：返回 insertId 以便前端使用
```

## 4. 区分必须改与可选

| 等级 | 数量 | 处理 |
|------|------|------|
| blocker | 2 | 必须修，修完才能放行 |
| warn | 2 | 建议修，不影响本次放行但应跟进 |
| nit | 1 | 可选 |

## 产出

```
评审对象：src/routes/notes.js POST /api/notes
清单结果：8 项过，3 项不过（验收、错误处理、SQL注入、测试）
问题列表：
  [blocker] 拼接 SQL → 参数化查询
  [blocker] 无错误处理 → try/catch + 500
  [warn] 未返回笔记 → 返回插入数据
  [warn] 未校验空 title → 加 400 校验
  [nit] 可返回 insertId
结论：2 个 blocker 待修，不放行。
```

修复后的代码：

```js
router.post('/api/notes', async (req, res) => {
  const { title, content } = req.body;
  if (!title) return res.status(400).json({ error: 'title 不能为空' });
  try {
    const result = await db.query(
      'INSERT INTO notes (title, content) VALUES (?, ?)',
      [title, content]
    );
    res.status(201).json({ id: result.insertId, title, content });
  } catch (err) {
    res.status(500).json({ error: '保存失败' });
  }
});
```

blocker 清零 → 可放行进入验证阶段。
