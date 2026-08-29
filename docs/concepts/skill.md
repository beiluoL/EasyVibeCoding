# Skill 技能

## 是什么

Skill（技能）是一个可复用的工程化能力包。大白话：把一段经常重复的 Prompt + 它需要的步骤 + 验收标准，打包成一个有名字、能反复调用的"工具"。

它不是一句话指令，而是一套"怎么干这件事"的说明书：包含目的、前置条件、执行步骤、输出格式、怎么验证做对了。

## Skill 和 Prompt 的区别

| 维度 | Prompt 提示词 | Skill 技能 |
| --- | --- | --- |
| 本质 | 单次指令，一次性 | 能力包，可反复调用 |
| 寿命 | 用完即弃 | 沉淀下来，团队/自己都能复用 |
| 内容 | 一段文字 | 目的 + 步骤 + 约束 + 输出 + 验证 |
| 适用场景 | 临时、一次性的需求 | 反复出现的同类任务（写测试、做评审、发版检查） |
| 类比 | 临时口令 | 写在手册里的标准操作流程 |

一句话：Prompt 是"这次帮我干一下"，Skill 是"以后这类活都这么干"。

## 为什么重要

原则 03 Reuse before reinvent——先复用，再造轮子。把重复劳动固化成 Skill，下次不用重新想 Prompt，AI 也不用重新猜你的偏好，质量更稳。

## 什么时候用

- 同一类任务你做了第三次，就该考虑抽成 Skill
- 想让团队成员都用同一套标准做事
- 一个任务步骤多、容易漏步骤，需要清单化

## 怎么用

1. 在 [`skills/`](../../skills/) 目录下按类别建子目录（如 `skills/core/`、`skills/ai/`）
2. 每个技能对应一个说明文件，参考模板：[`templates/skill/SKILL.md`](../../templates/skill/SKILL.md)
3. 文件里写清：这个技能解决什么问题、前置条件、执行步骤、输出格式、怎么验证
4. 在 Prompt 里通过链接引用对应 Skill，让 AI 按这套流程走

## 常见误用

- **把 Skill 当 Prompt 用**：Skill 不是让你直接粘贴执行的指令，而是一份"该这么干"的规范，需要 AI 结合当前任务去执行。
- **Skill 写得太大**：一个 Skill 只解决一类问题。太大会变成"万能指令"，反而模糊。该拆就拆（见 [task-decomposition](../best-practices/task-decomposition.md)）。
- **只写了步骤没写验收标准**：没有验证的 Skill 等于让 AI 自己判分，违反原则 04。每个 Skill 都该有"怎么算做对了"。
- **建了一堆 Skill 却不维护**：项目变了 Skill 不更新，反而误导 AI。Skill 是活文档。

## 相关资源

- Skill 模板：[`templates/skill/SKILL.md`](../../templates/skill/SKILL.md)
- Skill 目录：[`skills/`](../../skills/)
- 多个 Skill 串成流程：[workflow](./workflow.md)
- 让 AI 自主调用多个 Skill：[agent](./agent.md)
