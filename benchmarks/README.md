# EasyVibeCoding Benchmarks V0.1

> ⚠️ Not Yet Verified — V0.1 仅提供任务定义与评分标准，尚未进行任何真实模型对比执行。

## 什么是 Benchmark？（给小白的一句话解释）

**Benchmark（基准测试）** 就像一张"统一考卷"：我们把同样的 10 道编程题，发给不同的 AI 模型（或人类程序员）去做，然后用同一套打分规则给他们评分，最后对比谁做得更好。

## 为什么要做 Benchmark？

EasyVibeCoding 是"面向小白的 AI 工程化知识库"，我们最终想回答一个朴素的问题：

> **当一个小白把需求交给 AI 去做时，它到底能不能把事情做对？**

要回答这个问题，不能靠"感觉"，要靠"考卷"。V0.1 先把卷子（任务定义）和打分规则（评分标准）写出来；V0.2 再让模型们真的来考一次，把结果填到 [results/](./results/) 里。

## 目录结构

```
benchmarks/
├── README.md          ← 你现在看的这个文件（总览 + 10 张任务卡）
├── scoring.md         ← 8 维度评分标准 + 总分加权公式
├── tasks/             ← 10 个 Benchmark 任务（B01 ~ B10）
│   ├── B01-create-crud.md
│   ├── B02-fix-runtime-bug.md
│   ├── B03-add-redis-cache.md
│   ├── B04-build-rag.md
│   ├── B05-add-streaming.md
│   ├── B06-add-authentication.md
│   ├── B07-add-mcp-tool.md
│   ├── B08-refactor-service.md
│   ├── B09-write-tests.md
│   └── B10-security-review.md
└── results/           ← 真实跑分结果（V0.2 填充）
    └── README.md      ← 结果说明 + 空白对比表模板
```

## 10 张任务卡片

| 编号 | 任务名 | 难度 | 一句话说明 | 链接 |
|:---:|:---|:---:|:---|:---|
| B01 | **实现 CRUD 接口** | beginner | 空 Node+SQLite 项目里，给 `notes` 表写 4 个 REST 接口（增删改查） | [B01-create-crud.md](./tasks/B01-create-crud.md) |
| B02 | **修复运行时 Bug** | intermediate | 定位并最小修复"保存笔记后列表不刷新"的 Bug，并写回归测试 | [B02-fix-runtime-bug.md](./tasks/B02-fix-runtime-bug.md) |
| B03 | **加 Redis 缓存层** | intermediate | 给已有 CRUD 加 Redis 缓存（热点查询缓存 + 写入自动失效） | [B03-add-redis-cache.md](./tasks/B03-add-redis-cache.md) |
| B04 | **搭建最小 RAG** | advanced | MD 文档集 + LLM Key → 文档切块/向量化/检索/拼 Prompt/带引用回答 | [B04-build-rag.md](./tasks/B04-build-rag.md) |
| B05 | **加 SSE 流式输出** | intermediate | 给一个 LLM 调用接口从"等全量返回"改造为"逐字流式"（SSE） | [B05-add-streaming.md](./tasks/B05-add-streaming.md) |
| B06 | **加邮箱/密码登录鉴权** | intermediate | 邮箱+密码注册登录 + JWT 鉴权，密码哈希存储，未登录 401 | [B06-add-authentication.md](./tasks/B06-add-authentication.md) |
| B07 | **编写 MCP Todo 工具** | advanced | 给 MCP client 写一个 todo CRUD 工具，含 schema/安全边界/最小权限 | [B07-add-mcp-tool.md](./tasks/B07-add-mcp-tool.md) |
| B08 | **重构单块大函数** | intermediate | 把一个 150 行"读 DB → 处理 → 返回"的大函数拆成三个职责清晰的小函数 | [B08-refactor-service.md](./tasks/B08-refactor-service.md) |
| B09 | **写 3 个接口测试** | beginner | 给已实现的 `note create` 接口写：正常/空标题/超长内容 三条测试 | [B09-write-tests.md](./tasks/B09-write-tests.md) |
| B10 | **AI 代码安全审计** | intermediate | 审查一段含 SQL 拼接/Key 泄露/无校验等问题的代码，分级+给修复建议 | [B10-security-review.md](./tasks/B10-security-review.md) |

## 难度图例

- **beginner** — AI 写提示词+几行代码就能完成，小白也能看懂验收结果
- **intermediate** — 需要理解业务上下文并做合理设计，有一定工程要求
- **advanced** — 需要多文件协作 + 非平凡架构决策，结果质量差距会比较大

## 如何使用

1. **出题方（我们）**：维护 `tasks/*.md` 和 `scoring.md` 的定义。
2. **执行方（V0.2）**：用同一套 Prompt 骨架，把每个任务发给不同模型，产出代码。
3. **验收方（V0.2）**：按照每个任务的「Acceptance Criteria」逐条跑自动化/半自动化验收，按 `scoring.md` 给 8 个维度打分。
4. **产出物**：把结果填入 `results/README.md` 的空白对比表，并为每个模型生成详细结果页。

> ⚠️ V0.1 仅完成第 1 步（定义卷子和打分规则）。第 2~4 步留待 V0.2 执行。
