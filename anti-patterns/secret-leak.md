# Secret Leak（密钥泄露）

> 反模式：把 API Key、密码、token 写进前端代码、提交进 git、打到日志里——泄露即事故。

## Bad Approach

为了"先跑通"，把密钥硬编码在代码里，顺手提交进仓库，或用 `console.log` 打出来调试。常见表现：

API_KEY = 'sk-example-not-a-real-key-redacted'  # safe: example (BAD anti-pattern, do NOT copy)
- `.env` 被提交进 git
- 把请求头（含 token）整个 `console.log` 出来
- 把密钥写进前端，靠"前端不展示"当安全

## Why It Fails

- **前端即公开**：前端代码任何人都能在浏览器里看，密钥写前端 = 直接公开。
- **git 是永久账本**：一旦提交，即使后面删掉，历史里还在，扒出来就能用。
- **日志会流转**：日志会被收集、转发、留存，密钥打日志 = 在多个系统里留副本。
- **泄露即事故**：密钥泄露意味着别人能冒用你的身份、刷你的额度、读你的数据，且常常不可逆。

## Better Approach

密钥只属于后端 + 环境变量：

1. **后端持有**：密钥只放在服务端代码里，前端通过后端代理访问，永远拿不到原始密钥。
2. **环境变量注入**：用 `.env` + `process.env` 读取，`.env` 加入 `.gitignore` 永不入库。
3. **不入日志**：打印前脱敏（只显示前 4 位），不要整段打请求头。
4. **合入前过 security-review**：检查有没有硬编码密钥、`.env` 有没有误提交。

## Example

❌ 泄露写法：

```js
// 前端代码里
API_KEY = 'sk-live-example-not-a-real-key-redacted'    # safe: example (BAD anti-pattern, do NOT copy)
fetch('https://api.x.com/data', { headers: { Authorization: API_KEY } });
console.log('请求头', headers); // token 被打到日志
```

任何人 F12 就能看到你的 live key，直接被盗刷。

✅ 安全写法：

```js
// 后端（.env 不入库，gitignore 掉）
const API_KEY = process.env.API_KEY; // 从环境变量读
// .gitignore: .env

// 前端只调自己的后端，永远拿不到第三方 key
fetch('/api/proxy/data'); // 后端用 key 去请求第三方
```

```js
// 打日志前脱敏
console.log('key:', API_KEY?.slice(0, 4) + '****');
```

## Related Skill

- [code-review](../skills/core/code-review/SKILL.md) —— 合入前结构化评审（含安全项零遗漏）
- [security-review](../prompts/review/security-review.md) —— 专门的安全评审清单
- 失败案例：[api-key-leak](../failures/deployment/10-api-key-leak.md)
