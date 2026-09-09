# Skill Quality Checklist 技能质量检查清单

> 用于检查一个 Skill 是否达到 EasyVibeCoding 质量标准。创建/升级 Skill 前逐项勾选。

## 基本结构

- [ ] SKILL.md 存在，YAML 元数据完整（14 个字段）
- [ ] README.md 存在，面向用户说明
- [ ] examples/ 目录存在，至少 1 个示例

## 内容质量

- [ ] Clear Purpose — 一句话说清做什么
- [ ] Clear Trigger — 什么时候用
- [ ] Clear Inputs — 输入是什么
- [ ] Clear Outputs — 输出是什么
- [ ] Repeatable Workflow — 可重复的流程
- [ ] Rules — 明确的规则
- [ ] Human Checkpoints — 什么时候需要人确认
- [ ] Anti-Patterns — 至少 2 个典型错误
- [ ] Validation — 如何验证这个 Skill 有效
- [ ] Example — 至少 1 个示例
- [ ] Related Resources — 链接到相关 Prompt / Workflow / Case

## 诚实标注

- [ ] 未验证内容标 `⚠️ Not Yet Verified` / `status: experimental`
- [ ] `verified: false` 时 `status` 为 `experimental`
- [ ] 无虚假 `Verified` / `✅ Tested` / `Production Ready`
- [ ] 示例性内容标 `Illustrative Example`

## 结构一致性

- [ ] 与其他 Core Skill 的章节结构一致
- [ ] 命名使用 kebab-case
- [ ] 版本号语义化
- [ ] 在 registry/skills.yaml 中注册
