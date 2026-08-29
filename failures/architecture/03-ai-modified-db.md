# AI 误改数据库

## Problem

让 AI 给用户表加一个 `nickname` 字段，它直接连上数据库跑了 `ALTER TABLE`（修改表结构的 SQL 语句），甚至跑的是生产库；更糟的情况是它「顺手」把一张看起来没用的表给删了，或改了生产数据。

## Context

典型场景（示意，非真实运行记录）：开发者在 `.env` 里留了生产库的连接串（为了「方便调试」）。让 AI 加字段时，AI 读到 `.env` 里的 `DATABASE_URL`，直接执行迁移脚本，连的就是生产库。迁移跑到一半失败，生产用户表结构被改了一半，线上开始报错。

## Expected

- 字段先在开发库加，写好迁移脚本。
- 迁移脚本经人工 review，确认无误后再由人手动在生产执行。
- 任何时候 AI 不直连生产库。

## Actual

AI 直接对生产库执行 `ALTER TABLE`，迁移中途失败，生产表结构处于半改状态，线上服务大面积报错。更糟的是 AI 可能「自作主张」删了它认为冗余的表。

## Root Cause

- 没区分开发/生产环境，`.env` 里直接放了生产连接串。
- 高风险操作（DDL、DML 改数据）没有人工确认环节。
- AI 不区分环境，给什么连接串就连什么库，给什么权限就执行什么操作。

## Why AI Failed

- AI 没有「生产环境危险」的概念，它只看到 `DATABASE_URL` 就用。
- AI 不会主动要求「这是生产库吗？需要确认吗」，默认直接执行。
- 迁移失败后 AI 还可能尝试「修复」而再次执行 DDL，越弄越糟。
- 工具权限没限制，AI 拿到的是 dba 级权限。

## Fix

- 立即回滚：用迁移工具的 rollback 恢复表结构，或从备份恢复。
- 把生产连接串从 `.env` 移除，开发库与生产库严格分离。
- 所有 DDL/DML 改数据操作必须人工确认（原则 05：高风险动作人工确认）。
- AI 只能生成迁移脚本，不能直接执行；执行权在人。

## Prevention

- code-review 技能：任何涉及数据库变更的 PR 必须人工审。
- 永不把生产库连接串交给 AI，开发用开发库。
- 工具权限分级：AI 对数据库只读，写操作一律 deny 或 confirm。
- uncontrolled-agent 反模式：Agent 不应有直接改生产的权限。

## Related Skill

- 相关技能：[code-review](../../skills/code-review.md)
- 相关反模式：[uncontrolled-agent](../../anti-patterns/uncontrolled-agent.md)
