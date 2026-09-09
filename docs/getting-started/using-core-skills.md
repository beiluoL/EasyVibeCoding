# Using Core Skills 核心技能使用指南

> 小白版：10 个 Core Skills 怎么用？什么时候用？

## 一句话理解

> Skills 不是要你每次全调用一遍。而是根据当前任务，选对的那一个。

## 完整流程示例

假设你要做一个网站：

```text
我要做一个网站
↓
01 Project Discovery（先理解项目，如果是已有项目）
↓
02 Requirement Analysis（搞清楚做什么）
↓
03 Brainstorming（方案不确定时，探索选项）
↓
04 Architecture Design（设计模块怎么连）
↓
05 Task Planning（拆成小任务）
↓
06 Implementation（逐个任务实现）
↓
08 Testing（证明代码能跑）
↓
09 Code Review（换视角检查质量）
↓
10 Verification（逐条验收，证明真的完成）
```

遇到 Bug？随时切到 07 Systematic Debugging。

## 不需要每次全调用

| 场景 | 需要的 Skills |
| --- | --- |
| 新项目 | 01→02→03→04→05→06→08→09→10 |
| 新功能 | 02→05→06→08→09→10 |
| 修 Bug | 07→06→08 |
| 重构 | 04→05→06→08→09→10 |
| 加测试 | 08→10 |

> 根据 [Skill Selector](./skill-selector.md) 选择需要的 Skill。

## 延伸阅读

- [Core Skills Map](../concepts/core-skills-map.md) — 技能依赖图
- [Core Skills Matrix](../concepts/core-skills-matrix.md) — 一览表
- [Decision Tree](./decision-tree.md) — 按场景做决策
- [AI Chat Reference Case](../../cases/golden/001-ai-chat/README.md) — 完整示例
