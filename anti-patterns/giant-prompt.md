# Giant Prompt（巨型提示词）

> 反模式：把整个项目需求塞进一个巨型 Prompt，让 AI 一次写完——看似高效，实则最容易翻车。
>
> 术语小贴士：**Prompt**（提示词）= 你给 AI 的那句指令。**Giant Prompt** = 一句话塞太多，AI 顾此失彼。

## Bad Approach

写一条超长 Prompt，把"做登录、做列表、做权限、做部署"全塞进去，让 AI 一次生成整个项目。常见表现：

- 一条 Prompt 几百字，含 5 个以上不相关功能
- 不给验收标准，只说"做一个 XX 系统"
- 不拆步骤，期望 AI 一口气交付可运行项目

## Why It Looks Reasonable

- "一句话说完所有需求，AI 一次生全，省得来回对话"——感觉省时省力。
- 以为 AI 足够强，一次能处理所有功能并保持一致性。
- 小项目（3 个功能以内）时确实有时能碰巧跑通，让人误以为规模大了也行。

## Why It Fails

- **上下文超载**：AI 的注意力（attention，模型生成时分配给各部分的权重）被稀释，常漏掉约束。
- **抓不住重点**：需求越多越难判断优先级，AI 平均用力，关键功能反而做得糙。
- **出错难定位**：一锅出后报错，分不清是哪段逻辑的锅，回退只能整锅倒掉。
- **违反原则 02** Small tasks over giant prompts——拆小任务，别一句话塞太多。

一句话：AI 一次干太多事，必然出错且难调试。

## Better Approach

先拆任务，再逐个实现：

1. 用 task-planning 把需求拆成"单次可完成 + 可独立验证"的小任务。
2. 每个任务配一个验收点（做到什么算完成）。
3. 一次只让 AI 做一个任务，做完验一步，再做下一个。
4. 任务之间标依赖顺序，按拓扑排序推进。

## Example

需求：给笔记应用加"登录 + 笔记列表 + 新建笔记"。

❌ 巨型 Prompt：

```
帮我做一个笔记系统，要登录、列表、新建、编辑、删除、搜索、
标签分类、导出 PDF、部署上线，用 React + Node + Postgres，
风格好看点，做完直接能跑。
```

AI 一次吐出几千行，跑起来一堆报错，不知道从哪修。

✅ 拆小后逐个做：

| 序号 | 任务 | 验收点 | 依赖 |
| --- | --- | --- | --- |
| 1 | 登录接口 + 校验 | 输错密码返回 401 | - |
| 2 | 笔记列表查询 | 返回当前用户的笔记 | 1 |
| 3 | 新建笔记接口 | 保存后列表能查到 | 2 |

每个任务一个 Prompt，做完跑一次验收，错了只回退这一步。

## Prevention

- 每个 Prompt 限制 1–2 个功能，超过 3 个就先走 [task-planning](../skills/core/task-planning/SKILL.md)。
- 写 Prompt 前先列验收点：每个功能"做到什么算完成"。
- 如果 AI 产出超过 200 行，大概率是塞太多了——停下来拆。

## Related Skill

- [task-planning](../skills/core/task-planning/SKILL.md) —— 把需求拆成有序小任务
- [context-engineering](../skills/ai/context-engineering/SKILL.md) —— 控制给 AI 的上下文量
- 原则 02 Small tasks over giant prompts：项目根 `README.md`
