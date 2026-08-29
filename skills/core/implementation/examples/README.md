# Implementation 示例 — 实现"创建笔记"接口

## 输入

需求：给笔记应用加一个"创建笔记"接口（POST /api/notes）。

已拆好的任务（来自 task-planning）：

```
任务 1：实现 POST /api/notes，保存 title + content
  验收点：
    1. 正常请求返回 201 并含新笔记
    2. title 为空返回 400
```

项目已有结构：

```
src/
  routes/notes.js   （已有 GET /api/notes 路由）
  models/Note.js    （已有 Note 模型）
  db.js             （已封装数据库连接）
```

## 给 AI 的完整 prompt

```
项目结构：见上
已有路由示例（src/routes/notes.js）：
  router.get('/', async (req, res) => {
    const notes = await Note.find();
    res.json(notes);
  });

任务：只实现 POST /api/notes，接收 title 和 content，保存到数据库。
约束：
  - 只改 src/routes/notes.js
  - 复用已有的 Note 模型
  - 不要改其他文件
验收点：
  1. 正常请求返回 201
  2. title 为空返回 400
```

## AI 产出（最小改动）

只往 `src/routes/notes.js` 加了一个 POST 路由：

```js
router.post('/', async (req, res) => {
  const { title, content } = req.body;
  if (!title) return res.status(400).json({ error: 'title 不能为空' });
  const note = await Note.create({ title, content });
  res.status(201).json(note);
});
```

没动其他文件，没新建文件，复用了已有的 `Note` 模型。

## 跑起来验证

用 curl 发两个请求：

```bash
# 验收点 1：正常请求
curl -X POST http://localhost:3000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"第一篇","content":"内容"}'
# 返回 201 + 新笔记 ✅

# 验收点 2：空 title
curl -X POST http://localhost:3000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"","content":"内容"}'
# 返回 400 ✅
```

## 产出记录

```
任务：实现 POST /api/notes
改动文件：src/routes/notes.js
改动说明：新增 POST 路由，复用 Note 模型
验证方式：2 个 curl 请求
验收点：1 ✅ / 2 ✅
```

两条验收点都通过 → 进入下一个任务。整个流程只改了一个文件、加了一个路由，小而可控。
