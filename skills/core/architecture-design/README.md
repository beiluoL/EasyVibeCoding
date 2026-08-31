# Architecture Design（架构设计）

> 写代码前先搭好架子，模块/数据流/选型一次说清。

## What（是什么）

在编码前确定技术架构：模块划分（模块 = 把大程序拆成各管一摊的小块）、数据流（数据从输入到输出经过哪些模块）、技术选型与外部边界。

## When（何时用）

- 需求清单已确认
- 进入编码前
- 多任务需统一架构依据

## How（怎么用）

1. 画模块图（Mermaid）
2. 定数据模型
3. 定技术栈 + 理由
4. 标注复用（Reuse before reinvent）
5. 标风险点

## 相关资源

- 详细规范：[SKILL.md](./SKILL.md)
- 完整示例：[examples/](./examples/README.md)
- 上游技能：[../requirement-analysis/SKILL.md](../requirement-analysis/SKILL.md)、[../brainstorming/SKILL.md](../brainstorming/SKILL.md)
- 下游技能：[../task-planning/SKILL.md](../task-planning/SKILL.md)
- 配套 Prompt 模板：[../../../prompts/architecture/design-architecture.md](../../../prompts/architecture/design-architecture.md)
