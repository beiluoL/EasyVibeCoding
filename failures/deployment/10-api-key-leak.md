# API Key 泄露

## Problem

**API Key（应用程序密钥：服务商给你的一串"密码"，调用接口时用它证明你是你，别人拿到就能花你钱/冒充你）** 被泄露了：写在前端代码里被 F12 看到、写死在代码里提交到了 GitHub、或者打印进了日志被人扒出来。轻则几百块损失，重则 key 被盗刷几万、或者被用你的身份发垃圾消息/邮件。

## Context

典型场景 1（示意）：小白用 Vite 写了个小页面，想在前端直接调 OpenAI 接口，就把 key 直接写在 `api.js` 里：

```js
// 错误示例：key 直接写在前端代码里
API_KEY = "sk-example-not-a-real-key-redacted"  # safe: example (BAD pattern to avoid - do NOT copy)
fetch("https://api.openai.com/v1/chat/completions", {
  headers: { Authorization: `Bearer ${API_KEY}` },
  ...
});
```

部署上线后，任何人 F12 打开 Sources 面板就能看到 key。半天后被爬虫扫到，第二天醒来账单 8000 刀。

典型场景 2（示意）：后端项目的 `.env` 被误提交进 Git（`.gitignore` 漏写了 `.env`），仓库还设成了 public。1 小时后 GitHub 上的 secret scanner（密钥扫描机器人）直接邮件通知你 key 已泄露，你上控制台一看已经被刷了 300 多块。

典型场景 3（示意）：线上报错时，开发者为了方便调试把 `Authorization` 请求头整个打进日志。日志被运维的同事误导出分享，key 跟着就出去了。

## Expected

- Key 只出现在后端/服务端的**环境变量**里（OS 级或云平台 Secret Manager）。
- 前端**绝不**直接持有 key。前端要调用第三方 API，走你自己的后端转发（后端代你加 key、代你做限流和鉴权）。
- 代码库（git 历史）里**永远不出现**真实 key，哪怕一次。
- 日志里**绝不打印**任何 key、token、password。

## Actual

- Key 硬编码进前端 → F12 直接看。
- Key 写在 `.env`、`config.json`、`constants.js` 等被 git 追踪的文件 → 提交后公网可见，git 历史里也永远留痕。
- Key 打印进日志 / 错误消息 / Sentry 上报 → 日志泄漏 = key 泄漏。
- Key 直接分享给同事（微信 / 钉钉）→ 聊天记录泄漏 / 截屏外流。

## Root Cause

没把密钥当"一等公民"来管。潜意识里把 key 当成了"一个配置字符串"，放在"方便写代码的地方"就行；其实 key 的价值和你银行卡密码一样，放错地方就是事故。

常见心态：

- "先跑起来再说，key 之后再换个地方存" → 然后就没然后了。
- "我的项目这么小，没人会扫我" → 实际上 GitHub / 公网页面上的 key 有大量自动化爬虫 24 小时扫，公开仓库的 key 几分钟内就会被尝试盗刷。
- "前端直接调省事，省得写后端" → 省事的代价是 key 一定被拿。

## Why AI Failed

AI 默认倾向"把东西放在用户最方便直接用的位置"。你让 AI 写一个"前端调 GPT 的 demo"，它默认就会把 key 写在前端代码里——**AI 不会主动提醒你"这是 key，你不能放这"**，除非你在 prompt 里明确加安全要求。

同样，你让 AI 写一个"快速本地调试的配置"，它会很自然地把 key 写死在 `config.py` 里，而不是提醒你用环境变量。**AI 没把 key 的安全等级默认为"最高"**，这个责任要由开发者（人）来兜。

## Fix

1. **Key 只放后端环境变量**：
   - 后端用 `.env` 文件（但 `.env` 必须写进 `.gitignore`！），或部署平台（Vercel / Railway / 阿里云）的环境变量面板。
   - 生产环境优先用云厂商的 Secret Manager / Parameter Store，而不是 `.env`。
2. **前端永不持有 key**：
   - 前端 → 你自己的后端（比如 `/api/chat`）→ 后端从环境变量取 key → 后端调 OpenAI → 后端把结果返回前端。
   - 后端同时做**限流 + 鉴权 + 计费配额**，避免前端被盗用流量。
3. **立刻处理已泄漏的 key**：
   - 服务商控制台里 **Revoke（吊销）旧 key**，生成新 key。不要只"改代码里那一行"。
   - 查看账单和调用日志，排查盗刷记录。
   - 如果 key 进了 git 历史，**光改文件没用**，要用 `git filter-branch` 或 BFG Repo-Cleaner 把历史记录里的 key 清干净，或者干脆重建仓库历史。
4. **日志里 scrub（清洗）敏感字段**：
   - 全局加日志中间件：字段名只要包含 `key` / `token` / `secret` / `password` / `authorization`，一律打印成 `***`。
5. **统一配置中心**：团队里 key 走 1Password / Infisical / Vault 之类的工具共享，绝不走微信/钉钉/邮件。

## Prevention

- **仓库根目录放一份 [SECURITY.md](../../SECURITY.md)**，第一条写密钥管理规范，新成员上手必读。
- 对照 [secret-leak 反模式](../../anti-patterns/secret-leak.md) 自查：有没有把 key 写死、有没有把 `.env` 加 `.gitignore`、前端有没有 key、日志有没有 key。
- **git 提交前跑 secret-scan（密钥扫描）**：用 `gitleaks`、`trufflehog` 之类的工具做 pre-commit 钩子，检出 key 就直接阻止提交。GitHub 也自带 Secret scanning 免费功能，一定要开。
API_KEY = "$PROD_ENV_API_KEY"  # safe: placeholder (FIXED approach: use env var)
- 定期（比如每季度）**轮换一次所有 key**。轮换机制建好了，真泄露了心里也不慌。

## Related Skill

- 相关技能：[code-review](../../skills/core/code-review/SKILL.md)
- 相关反模式：[secret-leak](../../anti-patterns/secret-leak.md)
