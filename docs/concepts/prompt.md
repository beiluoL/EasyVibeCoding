# Prompt 提示词

## 是什么

Prompt（提示词）就是你跟 AI 说话时输入的那段文字指令。大白话：你给 AI 写的"需求单"。一段好 Prompt 能让 AI 知道你是谁、要它干什么、有什么限制、最后交什么。

## 为什么重要

AI 不会读心。同样一个目标，Prompt 写得清楚和写得模糊，结果可能差出几条街。在 Vibe Coding 里，Prompt 是你和 AI 协作的最小单元，几乎所有质量问题都能往前追溯到 Prompt。

## 什么时候用

- 每次让 AI 写代码、改代码、解释代码
- 让 AI 按固定格式产出（接口文档、提交信息、测试用例）
- 把一个反复出现的指令固化成模板

## 怎么用：好 Prompt 的 7 个构建块

| 构建块 | 大白话 | 示例 |
| --- | --- | --- |
| Role 角色 | 让 AI 扮演谁 | 你是一名资深后端工程师，熟悉 Java/Spring Boot |
| Context 上下文 | 现在是什么情况 | 这是电商订单服务，用 MyBatis-Plus，已上线 |
| Goal 目标 | 到底要它干什么 | 给 OrderService 加一个按状态分页查询方法 |
| Constraints 约束 | 不能踩什么线 | 不引入新依赖；不改动公共接口签名；遵循阿里规范 |
| Workflow 流程 | 按什么顺序做 | 先读现有代码 → 找相似实现 → 照着写 → 自测 |
| Output format 输出格式 | 交什么样子 | 只给改动后的方法代码 + 一句说明，不要全文重贴 |
| Verification 验证 | 怎么算完成 | 给出能跑通的测试输入和期望输出 |

把这 7 块按顺序填进去，就得到了一个结构化 Prompt。模板和现成例子见 [`prompts/`](../../prompts/)。

## 好坏 Prompt 对比

**坏 Prompt（太模糊）**

> 帮我写个登录功能

问题：没说语言、没说框架、没说约束、没说验收标准，AI 只能猜，产出的代码十有八九用不了。

**好 Prompt（7 块齐全）**

> 角色：你是熟悉 Spring Boot 的后端工程师。
> 上下文：项目用 Spring Security + JWT，已有 `UserService` 和 `JwtUtil`。
> 目标：实现 `/api/login` 接口，校验账号密码后签发 token。
> 约束：不引入新依赖；密码用项目已有的 BCrypt；遵循阿里命名规范。
> 流程：先读 `UserController` 和 `UserService` → 复用现有方法 → 再写新接口。
> 输出格式：只贴新增的 Controller 方法和依赖的 import，不要重贴整个文件。
> 验证：给出 curl 请求示例和成功/失败两种期望响应。

## 常见误用

- **把所有要求塞进一句话**：AI 容易漏掉中间的约束。拆成结构化块更稳。
- **只说"做到最好"不给验收标准**：AI 没有客观依据，最后靠你"感觉"对不对，违反原则 04 Evidence over claims。
- **让 AI 一次性写整个大功能**：违反原则 02 Small tasks over giant prompts，应该拆成小任务分步走（见 [task-decomposition](../best-practices/task-decomposition.md)）。
- **不提供上下文就要求"按项目风格"**：AI 看不到你的项目，无从模仿。先让它读懂项目（见 [project-understanding](../best-practices/project-understanding.md)）。

## 相关资源

- Prompt 模板库：[`prompts/`](../../prompts/)
- 拆任务：[task-decomposition](../best-practices/task-decomposition.md)
- 把单次指令升级成可复用能力包：[skill](./skill.md)
- 七大原则全文：项目根 `README.md`
