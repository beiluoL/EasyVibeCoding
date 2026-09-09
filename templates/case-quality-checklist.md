# Case Quality Checklist

> 用于检查一个 Case 是否达到 EasyVibeCoding 质量标准。开 PR 前逐项勾选。

---

## 基本结构

- [ ] README.md 存在，第一屏说清"项目是什么"
- [ ] requirements.md 存在，含 MVP + 验收标准
- [ ] architecture.md 存在，含模块图 + 关键决策理由
- [ ] development-plan.md 存在，任务拆到 Task 级
- [ ] development-log.md 存在，每步有 Prompt + 结果 + 验证

## 内容质量

- [ ] Goal clear — 项目目标一句话说清
- [ ] User clear — 目标用户明确
- [ ] MVP defined — 最小可行版本定义清楚
- [ ] Architecture explained — 架构有"为什么"的解释
- [ ] Tasks small enough — 每个任务可独立验收（不出现"和"字）
- [ ] Prompts included — 每个 Prompt 链接到 Skill
- [ ] Skills included — 使用的 Skill 有映射表
- [ ] Failure included — 至少 1 个失败案例（含根因 + 修复）
- [ ] Verification defined — 有验证步骤和验收标准
- [ ] Limitations documented — 局限性明确列出

## 诚实标注

- [ ] 未验证内容标 `⚠️ Verification Pending` 或 `Status: experimental`
- [ ] 示例性内容标 `Illustrative Example`
- [ ] 无虚假测试结果 / 运行截图 / 性能数据
- [ ] 无 `✅ Tested` / `Verified` / `Production Ready`（除非有真实证据）

## 交叉引用

- [ ] Case → Skill 链接存在
- [ ] Case → Prompt 链接存在
- [ ] Case → Workflow 链接存在
- [ ] Failure → Anti-Pattern 链接存在
- [ ] Failure → Skill 链接存在

## 小白体验

- [ ] 专业术语首次出现有解释
- [ ] 有"一句话理解"
- [ ] 有实际例子
- [ ] 有推荐学习路径
