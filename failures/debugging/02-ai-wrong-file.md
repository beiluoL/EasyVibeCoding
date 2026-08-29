# AI 修改错误文件

## Problem

让 AI 改后端登录逻辑，它跑去改了前端的登录页样式；或者说要改订单计算，它把无关的用户模块也一起重写了。改的不是该改的地方，还把能跑的代码弄坏。

## Context

典型场景（示意，非真实运行记录）：项目结构是 `src/server/`（后端）和 `src/client/`（前端）混合在一个仓库。开发者对 AI 说「登录接口返回 401，帮我修一下」，没指明文件。AI 搜到 `client/login.vue` 里有 `401` 字样，直接在前端改了错误处理；真正的后端 JWT（JSON Web Token，一种用于认证的令牌）校验逻辑在 `server/auth/middleware.ts` 里纹丝未动。结果 401 依旧，前端还被改坏了。

## Expected

AI 只修改 `server/auth/middleware.ts` 中 JWT 校验的相关逻辑，前端不动，后端修复后 401 消失。

## Actual

AI 改了前端 `login.vue`，后端问题原封不动；前端原本正常的错误提示被改宽，用户反而看不到 401 了，更难排查。

## Root Cause

上下文没给清项目结构与目标文件。开发者只描述了「症状」（401），没给「位置」（哪个文件、哪个函数）。AI 只能靠文件名和关键词猜，猜错就改错地方。

## Why AI Failed

- AI 靠文件名/关键词猜测目标，没有「先确认范围再动手」的约束。
- 前后端同仓时，关键词（如 login、auth）会同时命中多个文件，AI 倾向选第一个。
- 开发者没限定「只能改这几个文件」，AI 就自由发挥。
- AI 不会主动反问「你指的是前端还是后端」，默认开干。

## Fix

- 给 AI 明确的文件路径：`修改 server/auth/middleware.ts 中的 verifyToken 函数`。
- 在指令里限定范围：`只允许改这一个文件，其他不要动`。
- 改之前让 AI 先复述「我准备改 X 文件的 Y 函数，对吗」，确认后再改。

## Prevention

- implementation 技能强调「一次只改一个任务、明确文件范围」。
- 改之前先让 AI 列出「将修改的文件清单」，人工确认后再执行。
- 前后端同仓的项目，在 prompt 里附上项目结构说明，避免 AI 靠猜。
- 任何「顺手改了别的地方」都视为越权，回滚。

## Related Skill

- 相关技能：[implementation](../../skills/implementation.md)
- 相关反模式：[blind-rewrite](../../anti-patterns/blind-rewrite.md)
