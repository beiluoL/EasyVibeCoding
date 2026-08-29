# Lessons — 多租户 AI SaaS 平台 MVP

> ⚠️ 以下为基于多租户常见坑总结的预判性教训，尚未经本案例实际运行验证。

## 易错点 → Anti-Pattern 对应

| # | 易错点 | 后果 | 对应 Anti-Pattern |
| --- | --- | --- | --- |
| 1 | 跨租户数据泄露 | A 看到 B 的文档/对话，合规与信任崩塌 | [`../../../anti-patterns/secret-leak.md`](../../../anti-patterns/secret-leak.md)（数据越权版） |
| 2 | 密钥上前端/入库 | key 被偷，全平台被白嫖 | [`../../../anti-patterns/secret-leak.md`](../../../anti-patterns/secret-leak.md) + [`../../../prompts/review/security-review.md`](../../../prompts/review/security-review.md) |
| 3 | 计费误计 | 失败也算钱 / 超额不算 / 算到别家账上 | [`../../../anti-patterns/secret-leak.md`](../../../anti-patterns/secret-leak.md)（计费口径版） |
| 4 | 隔离不彻底（某接口漏过滤） | 单个越权点击穿整套隔离 | [`../../../anti-patterns/secret-leak.md`](../../../anti-patterns/secret-leak.md) + [`../../../skills/core/code-review/SKILL.md`](../../../skills/core/code-review/SKILL.md) |

> 术语解释：**越权（Broken Access Control）**= 用户干了超出自己权限的事，比如 A 用自己的登录态看到了 B 的数据。多租户里这是头号大坑。

## 教训详解

### 1. 跨租户数据泄露

**现象**：A 上传文档后，B 提问居然检索到了 A 的内容；或 A 用自己的 Token 访问到 B 的对话记录。

**根因**：① 检索没带 `tenant_id` 过滤，全局查了；② 对象级授权没做，`/docs/{id}` 不校验归属；③ 租户 ID 从前端传参而非 Token 解析，可伪造。

**正确做法**：两层隔离——数据层按租户分 collection / 每行带 `tenant_id`；应用层所有查询默认 `WHERE tenant_id = ?`，租户 ID 取自 Token，对象级访问必校验归属。见 [architecture.md](architecture.md) "隔离边界"。

### 2. 密钥上前端/入库

**现象**：为省事把 LLM/Embedding key 写进前端或提交到仓库，被 F12 或爬仓库的人偷走，全平台 API 调用被白嫖。

**正确做法**：key 只在后端环境变量，`.env` 加 `.gitignore`；提交前 `grep -rni "sk-\|api_key\|secret"` 自查；用户密码只存哈希。

### 3. 计费误计

**现象**：① LLM 失败/超时也算一次问答，账面虚高；② 超额不拦，租户刷爆；③ 用量记到错租户头上，A 的调用算到 B 账上。

**正确做法**：仅问答成功后 +1，失败/超时不计；超额设阈值告警（V0.1 暂可不拦，但计数要准）；用量记录与问答同租户绑定，取自 Token。

### 4. 隔离不彻底

**现象**：90% 接口都过滤了 `tenant_id`，但某一个忘写了，于是这一个接口成为越权后门，整套隔离功亏一篑。

**根因**：隔离是"全有或全无"——漏一个等于没隔离。

**正确做法**：关键路径日志带租户 ID 便于审计；写隔离回归测试覆盖每个数据访问接口；Code Review 专项查"每个查询是否带租户过滤"。见 [`../../../skills/core/code-review/SKILL.md`](../../../skills/core/code-review/SKILL.md)。

## 可复用的知识

- "隔离是全有或全无"——多租户通用铁律
- "租户 ID 来自 Token，不来自前端"——防伪造的通用规则
- "对象级授权"不能省——即使登录态合法，访问具体资源也要校验归属
- "key 不入库 + 密码只存哈希"是所有带鉴权系统的通用底线
- "计费只算成功的"是计量类系统的通用心法
