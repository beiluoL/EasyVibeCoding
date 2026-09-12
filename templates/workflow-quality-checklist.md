# Workflow Quality Checklist 工作流质量检查清单

> 用于检查一个 Workflow 是否达到 EasyVibeCoding 质量标准。创建/升级 Workflow 前逐项勾选。

## 基本结构

- [ ] README.md 存在
- [ ] 在 registry/workflows.yaml 中注册

## 内容质量

- [ ] Trigger clear — 什么时候触发
- [ ] Preconditions clear — 前置条件
- [ ] Steps clear — 步骤清晰
- [ ] Skills linked — 链接到相关 Skill
- [ ] Prompts linked — 链接到相关 Prompt
- [ ] Human checkpoints defined — 人工检查点
- [ ] Stop conditions defined — 停止条件
- [ ] Verification defined — 验证方法
- [ ] Failure modes documented — 常见失败模式
- [ ] Beginner explanation included — 小白说明

## 一致性

- [ ] 与其他 Workflow 的结构一致（15 节）
- [ ] 状态使用统一状态模型
- [ ] 与 Skill 的职责不重叠（Workflow 编排，Skill 方法）
- [ ] 与 Prompt 的职责不重叠（Workflow 编排，Prompt 执行）

## 诚实标注

- [ ] 未验证内容标 `⚠️ Not Yet Verified`
- [ ] 示例性内容标 `Illustrative Example`
- [ ] 无虚假 `Verified` / `Production Ready`
