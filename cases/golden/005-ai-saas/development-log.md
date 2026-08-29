# Development Log — 多租户 AI SaaS 平台 MVP

> ⚠️ Verification Pending — 以下步骤为**计划中的构建顺序**，尚未实际执行。每步标注了拟用的 prompt/skill，但代码未真正生成与运行。

## 构建原则

一次只做一件事、每步可验证，隔离与密钥红线贯穿全程。参考 [`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)（小步实现）。

## 步骤 1 — 租户模型

**做什么**：建数据模型——租户表、用户表（密码哈希）、文档元数据表，每行带 `tenant_id`；初始化向量库按租户分 collection。

**拟用 prompt**：[`../../../prompts/architecture/analyze-requirement.md`](../../../prompts/architecture/analyze-requirement.md)

**拟用 skill**：[`../../../skills/core/requirement-analysis/SKILL.md`](../../../skills/core/requirement-analysis/SKILL.md) · [`../../../skills/core/architecture-design/SKILL.md`](../../../skills/core/architecture-design/SKILL.md)

**验收点**：表结构带 `tenant_id`；向量库能创建 `tenant_a` / `tenant_b` 两个 collection。

> ⚠️ 未实际执行。

## 步骤 2 — 鉴权登录

**做什么**：实现注册（建租户+管理员）、登录（校验哈希、签发带 `tenant_id` 的 JWT）、网关验 Token。

**拟用 prompt**：[`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**拟用 skill**：[`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)

**验收点**：登录拿到 Token；解 Token 能取到 `tenant_id`；无 Token / 错 Token 请求被拒。

> ⚠️ 未实际执行。

## 步骤 3 — 隔离边界

**做什么**：租户路由——所有数据查询默认带 `WHERE tenant_id = ?`（取自 Token，不接受前端传参）；对象级授权校验（访问 `/docs/{id}` 时校验归属）。

**拟用 prompt**：[`../../../prompts/architecture/design-architecture.md`](../../../prompts/architecture/design-architecture.md)

**拟用 skill**：[`../../../skills/core/architecture-design/SKILL.md`](../../../skills/core/architecture-design/SKILL.md)

**验收点**：用 A 的 Token 访问 B 的 doc ID 返回 403/404；伪造 `tenant_id` 请求体无效。

> ⚠️ 未实际执行。

## 步骤 4 — 上传文档

**做什么**：租户内成员上传文档，落盘 + 写元数据（带 `tenant_id`），进入本租户处理队列。

**拟用 prompt**：[`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**拟用 skill**：[`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)

**验收点**：A 上传后元数据归属 A；B 查不到 A 的文档列表。

> ⚠️ 未实际执行。

## 步骤 5 — RAG 入库

**做什么**：切块 + Embedding + 入本租户 collection（带 `tenant_id` 元数据）。

**拟用 prompt**：[`../../../prompts/ai-app/build-rag.md`](../../../prompts/ai-app/build-rag.md)

**拟用 skill**：[`../../../skills/ai/rag/SKILL.md`](../../../skills/ai/rag/SKILL.md)

**验收点**：A 的文档向量进 `tenant_a` collection；查 `tenant_b` collection 为空。

> ⚠️ 未实际执行。

## 步骤 6 — 问答

**做什么**：问题向量化 → 仅在本租户 collection 检索 Top-K → 拼 prompt → 调 LLM → 回答 + 引用。

**拟用 prompt**：[`../../../prompts/ai-app/build-context.md`](../../../prompts/ai-app/build-context.md)

**拟用 skill**：[`../../../skills/ai/context-engineering/SKILL.md`](../../../skills/ai/context-engineering/SKILL.md) · [`../../../skills/ai/rag/SKILL.md`](../../../skills/ai/rag/SKILL.md)

**验收点**：A 问 A 的文档答对且引用 A；B 问 A 的文档应"未覆盖"而非泄露。

> ⚠️ 未实际执行。

## 步骤 7 — 用量统计

**做什么**：每次问答成功后，给该租户用量计数 +1（或 +Token 数），可按租户查累计。

**拟用 prompt**：[`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**拟用 skill**：[`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)

**验收点**：A、B 各自计数随问答累加且互不影响；失败/超时不计。

> ⚠️ 未实际执行。

## 步骤 8 — 计费 stub

**做什么**：暴露一个 `GET /usage/{tenant}` 占位接口返回累计用量；明确不接支付，注释标 stub。

**拟用 prompt**：[`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**拟用 skill**：[`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)

**验收点**：接口返回用量数字；代码无任何对外支付请求；注释/README 标 stub。

> ⚠️ 未实际执行。

## 步骤 9 — 发布检查（隔离与密钥自查）

**做什么**：跨租户隔离回归测试；断网/超限/key 失效兜底；全仓库 grep 无硬编码 key；`.env` 不在版本控制。

**拟用 prompt**：[`../../../prompts/review/security-review.md`](../../../prompts/review/security-review.md)

**拟用 skill**：[`../../../skills/core/code-review/SKILL.md`](../../../skills/core/code-review/SKILL.md) · [`../../../skills/core/verification-before-completion/SKILL.md`](../../../skills/core/verification-before-completion/SKILL.md)

**验收点**：两租户互相看不到对方文档；grep 无真实 key；断网显示错误不串租户。

> ⚠️ 未实际执行。

## 状态总览

| 步骤 | 状态 |
| --- | --- |
| 1 租户模型 | ⚠️ 未执行 |
| 2 鉴权登录 | ⚠️ 未执行 |
| 3 隔离边界 | ⚠️ 未执行 |
| 4 上传文档 | ⚠️ 未执行 |
| 5 RAG 入库 | ⚠️ 未执行 |
| 6 问答 | ⚠️ 未执行 |
| 7 用量统计 | ⚠️ 未执行 |
| 8 计费 stub | ⚠️ 未执行 |
| 9 发布检查 | ⚠️ 未执行 |
