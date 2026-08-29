---
name: implementation
description: 按"小步、可验证、复用既有模式"的方式，让 AI 写出能真正运行的代码。
version: 0.1.0
category: core
difficulty: beginner
status: experimental
verified: false
compatible: [unspecified]
prerequisites:
  - task-planning 技能产出的任务清单（拆好的单步任务）
  - 项目结构已知，相关文件路径明确
inputs:
  - 单个任务描述（一次只取一个）
  - 项目结构概览
  - 相关文件内容
outputs:
  - 最小代码改动（仅针对当前任务）
  - 跑通的证据（测试或手动复现）
triggers:
  - 需要实现某个具体功能点
  - 从任务清单中取出一个任务准备编码
  - AI 被要求"写一段功能代码"
validation:
  - 代码能跑起来，无运行时报错
  - 通过本任务定义的验收点
  - 未改动与本次任务无关的文件
last_verified: null
---

# Implementation（小步实现）

> ⚠️ Not Yet Verified

## Purpose

让 AI 写出**能真正运行的代码**，而不是一堆看起来对、一跑就崩的代码。

核心思想：小步走、每步可验证、优先复用项目里已经有的东西，不要让 AI 一次铺太大。

## When to Use

- 已经用 task-planning 把功能拆成了单步任务，现在要动手写某一步。
- AI 要写一段新功能代码时。
- 拿到一个需求，需要把它落地成可运行代码时。

## Trigger Conditions

- 任务清单里有一个状态为"待实现"的任务。
- 用户说"实现这个功能 / 写这个接口 / 加这个逻辑"。

## Preconditions

1. 任务清单已存在（来自 task-planning）。
2. 当前任务范围清晰，验收点已定义。
3. 知道项目用了什么框架、什么语言、相关文件在哪。

## Workflow

1. **取单个任务**：从 task-planning 产出的清单里只取一个任务，不要一次拿多个。
2. **给 AI 明确上下文**：把项目结构、相关文件内容、项目已有的模式（比如已有的接口怎么写的）一起给 AI。上下文越具体，AI 输出越靠谱。
3. **要求只改这一步**：明确告诉 AI"只实现这个任务，不要动其他东西"。
4. **跑起来看结果**：把 AI 写的代码放进项目跑一次，看是否报错、是否达到验收点。
5. **过验收点再进下一步**：本步验收通过了，才取下一个任务。没过就停下来修。

## Rules

- **一次只做一个任务**（原则 02 小步可验证）。不要一个 prompt 让 AI 同时做三件事。
- **优先复用现有库**（原则 03 Reuse before reinvent）。项目里已经有工具函数、已有 ORM、已有鉴权中间件，就直接用，别让 AI 重新造一个。
- **不允许 AI 大范围重写无关代码**。AI 倾向于"顺手优化"，这会引入不可控风险。
- 上下文要给够：相关文件全文、项目约定、已有同类实现，都给 AI 看。
- 每一步必须有可验证的产出（能跑 / 能测），不允许"我觉得写完了"。

## Anti-Patterns

- ❌ 一个 prompt 让 AI 把整个项目写完——必然失控。
- ❌ AI 自行修改无关文件——跑题且难排查。
- ❌ 不验证就堆功能——Bug 会指数级累积。
- ❌ 让 AI 重新造一个项目里已有的轮子。

## Validation

> 本技能 V0.1 新写，尚未经实际运行验证。

**Expected Validation Steps**：
1. 在一个真实小型项目里，用本技能流程实现 3 个不同任务。
2. 检查每次产出的代码是否：能跑、过验收点、未动无关文件。
3. 对比"一次全写"与"小步走"的返工率差异。
4. 收集至少 2 个真实使用案例后，更新 verified 与 last_verified 字段。

验证状态：⚠️ Not Yet Verified — 待按 Expected Validation Steps 实际运行后更新。

## Output Format

每次完成一个任务，产出：

```
任务：<任务标题>
改动文件：<文件路径列表>
改动说明：<一两句话>
验证方式：<跑了什么 / 测试结果>
验收点：<✅/❌ 逐条>
```

## Example

需求：实现"创建笔记"接口。

给 AI 的完整 prompt（已含上下文）：

```
项目结构：
  src/
    routes/notes.js   （已有其他路由文件可参考）
    models/Note.js    （已有数据模型）
    db.js             （已封装数据库连接）

已有路由示例（src/routes/notes.js 已有的 GET /api/notes）：
  router.get('/', async (req, res) => {
    const notes = await Note.find();
    res.json(notes);
  });

任务：只实现 POST /api/notes 接口，接收 title 和 content，保存到数据库。
约束：
  - 只改 src/routes/notes.js，加一个 POST 路由
  - 复用已有的 Note 模型，不要新建文件
  - 不要改其他文件
验收点：
  1. 发 POST 请求能保存成功并返回 201
  2. title 为空时返回 400
```

AI 产出（最小代码）：

```js
router.post('/', async (req, res) => {
  const { title, content } = req.body;
  if (!title) return res.status(400).json({ error: 'title 不能为空' });
  const note = await Note.create({ title, content });
  res.status(201).json(note);
});
```

跑起来验证：发一个 POST 请求，确认返回 201；再发一个空 title，确认返回 400。两条验收点都 ✅，进入下一步。
