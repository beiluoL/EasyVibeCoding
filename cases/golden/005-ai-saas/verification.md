# Verification — 多租户 AI SaaS 平台 MVP

> ⚠️ **Verification Pending**
>
> 本案例尚未实际运行。以下为 **Expected Verification Steps**（要验证该案例需做的事），**不是**已通过的证据。在真实执行并观察到通过前，绝不标记为 Verified / ✅ Tested / 已部署。

## 当前状态

- `status: experimental`
- `verified: false`
- `last_verified: null`

## Expected Verification Steps

按序执行，每步留下可复现证据（命令输出 / 截图 / 测试结果）：

### 1. 环境准备与起服务

```bash
# Node 版或 Python 版二选一
npm install && npm start
# 或
pip install -r requirements.txt && python app.py
export LLM_API_KEY=...        # key 从环境变量读，不入库
export EMBEDDING_API_KEY=...
export JWT_SECRET=...
```

**期望**：服务在 `localhost` 起来，无报错；登录页可访问。

> ⚠️ 未实际执行——上述命令仅为预期步骤，未跑过。依赖版本需自验。

### 2. 两租户互相看不到对方文档

- 注册租户 A、租户 B，各自登录拿 Token
- A 上传文档 DocA 入知识库；B 上传 DocB
- A 提问 DocA 内容 → **期望**：答对且引用 DocA
- B 提问 DocA 内容 → **期望**：检索不到、答"未覆盖"，而非泄露 DocA
- B 列文档 → **期望**：列表只含 DocB，无 DocA

### 3. 查无硬编码 key

```bash
grep -rn "sk-" --include="*.js" --include="*.ts" --include="*.py" --include="*.html" .
grep -rni "api_key\|secret\|password" --include="*.js" --include="*.ts" --include="*.py" --include="*.html" .
git check-ignore .env   # 期望 .env 被忽略
```

**期望**：除环境变量读取占位符（如 `process.env.LLM_API_KEY`）外，搜不到真实 key；`.env` 不在版本控制中；用户密码字段无明文。

### 4. 计费 stub 是否按用量累加

- A 问答 3 次（均成功）→ 查 A 用量 = 3
- B 问答 2 次（均成功）→ 查 B 用量 = 2
- A 再问 1 次但断网/超时失败 → **期望**：A 用量仍为 3（失败不计）
- 查 `GET /usage/a` 与 `/usage/b` 互不串账

> ⚠️ 计费为 stub，无真实支付请求；上述为预期行为，未实测。

### 5. 断网/超限看兜底

- 断网后 A 问答 → **期望**：显示"请求失败/超时"，不串租户、不卡死
- 伪造/缺失租户 ID 请求 → **期望**：被网关拒（401/403）
- A 用自己的 Token 访问 B 的 doc ID → **期望**：返回 403/404，不返回 B 的内容

### 6.（可选）隔离回归测试

用 [`../../../skills/core/testing/SKILL.md`](../../../skills/core/testing/SKILL.md) 给每个数据访问接口写隔离用例：
- A 的 Token 访问 B 的资源 → 应被拒
- 缺失 Token → 应被拒
- 每个查询接口默认带 `tenant_id` 过滤

## 诚实声明

- 以上均为"要验证该案例需做的事"，**尚未执行**。
- 不存在任何运行截图、测试通过输出、部署 URL、隔离审计报告。
- 计费 stub 仅演示用量统计链路，不构成真实计费/支付能力。
- 隔离强度为应用层 collection 分离，未做安全渗透测试。
- 在拿到真实证据前，本案例保持 `⚠️ Verification Pending`。
