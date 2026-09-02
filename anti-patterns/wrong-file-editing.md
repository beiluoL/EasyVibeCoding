# Anti-Pattern：Wrong File Editing（改错文件）

> ⚠️ Not Yet Verified

## Bad Approach

用户说"修一下登录问题"，AI 靠关键词搜索命中第一个包含"login"的文件就动手改——不管它是前端页面还是后端逻辑，不管实际问题在哪个模块。

## Why It Looks Reasonable

- AI 搜索"login"确实能找到相关文件——看起来找对了。
- 前后端同仓时，login.vue 和 auth/middleware.ts 都包含"login"。
- 如果碰巧改的文件里有类似问题，改了可能确实有效果。

## Why It Actually Fails

- 关键词命中 ≠ 问题所在。401 报错的原因可能在后端 JWT 校验，但 AI 改了前端的错误处理。
- 改错文件不仅没修好原问题，还把能跑的代码改坏了。
- 前端改完后错误提示被"改宽"，用户反而看不到 401 了，更难排查。

## Better Approach

先走 [Project Discovery](../skills/core/project-discovery/SKILL.md) 理解项目结构和调用链：

1. **Scan**：扫描目录，发现 src/client/ 和 src/server/ 分离
2. **Map**：画调用链 → 前端 login.vue → POST /api/login → server/auth/middleware.ts
3. **Identify**：入口是 middleware.ts 的 verifyToken()
4. **Trace**：跟一个 401 请求的完整路径
5. **确认根因在哪个文件** → 再动手改

改之前让 AI 列出"将修改的文件清单"，人工确认后再执行。

## Example

**❌ Wrong File Editing**：
```
用户：登录返回 401，帮我修
AI：搜索 "login" → 命中 client/login.vue → 改前端错误处理
→ 401 依旧（后端问题没动）
→ 前端被改坏（错误提示消失，更难排查）
```

**✅ Correct Approach**：
```
用户：登录返回 401，帮我修
AI：我先理解项目结构。
→ Scan: src/client/ (前端) + src/server/ (后端)
→ Map: login.vue → /api/login → auth/middleware.ts
→ Trace: 401 从 middleware.ts 的 verifyToken() 抛出
→ 根因在 middleware.ts，不在前端
→ 只改 middleware.ts 一个文件，前端不动
```

## Prevention

- 改之前先走 Project Discovery，理解调用链。
- 在指令里限定范围："只改 server/auth/middleware.ts"。
- 改之前让 AI 复述"我准备改 X 文件的 Y 函数，对吗"。
- 任何"顺手改了别的地方"都视为越权，回滚。

## Related Skill

- [project-discovery](../skills/core/project-discovery/SKILL.md)
- [implementation](../skills/core/implementation/SKILL.md)

## Related Failure

- [AI 修改了错误文件](../failures/debugging/02-ai-wrong-file.md)
