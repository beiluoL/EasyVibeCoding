---
name: 02-project-discovery
use_when: 进入一个已有项目时，先理解项目
goal: 系统理解项目结构、技术栈、入口、调用链
related_skill: skills/core/project-discovery
status: experimental
verified: false
---

# Prompt 02 — 项目发现

> 链接到 Skill：[project-discovery](../../../../skills/core/project-discovery/SKILL.md)

## Prompt

```
我要在这个项目里加一个新功能。

请先帮我理解项目：
1. 这个项目用什么技术栈？
2. 入口文件是哪个？
3. 目录怎么组织的？
4. 有哪些核心模块？
5. 测试在哪？怎么跑？

先不要改任何代码。只输出项目理解摘要。
```

## Expected Output

- 技术栈列表
- 入口文件路径
- 目录结构概览
- 核心模块列表
- 测试位置和运行方式

## Common Mistakes

- ❌ 不理解项目就直接改代码
- ❌ 只看用户指定的文件，不看调用链
