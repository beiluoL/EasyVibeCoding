# 003 - 能自主调用工具完成任务的 AI Agent

## Project Goal
做一个"会自己拆任务、会调工具、会停下来"的 AI Agent。用户给一句话，Agent 自己规划步骤、调用工具、观察结果、继续或终止，最后给出答案。

## Difficulty
advanced（进阶）

## Prerequisites
- 会 Python 基本语法（函数 / 字典 / 异常处理）
- 调用过至少一次 LLM API
- 理解 JSON 结构
- 看过 case 001 / 002 更佳

## Tech Stack
- Python 3.10+
- LLM API（任选一家，需支持 tool-calling）
- 工具调用用 JSON 描述 schema
- 示例工具 2-3 个：查天气、算数、读本地文件
- ⚠️ 工具与 SDK 版本需自验，本案例未实际跑通

## User Scenario
用户用自然语言提一个多步任务，例如：
> "查北京明天天气并算出和今天的温差"

Agent 自主拆成"查今天温度 → 查明天温度 → 算温差 → 给答案"。中间不让人插手，但遇到需要权限的工具会停下来确认。

## MVP
- 一个循环 Agent：规划 → 工具调用 → 观察 → 继续或终止
- 终止条件：任务完成 / 达到循环上限 / 触发不可恢复错误
- 工具权限白名单：auto（自动调）/ confirm（要人批）/ deny（禁用）

## Architecture
见 [architecture.md](./architecture.md)。
一句话：Agent = 一个"会自己想下一步干嘛、能动手调工具、知道什么时候该停"的循环程序。

## Workflow
1. 用户输入任务
2. Planner 拆步骤
3. Tool Caller 按 schema 调工具
4. Observer 看结果
5. 回到 Planner 或终止
6. 汇总输出

## Prompts
- Planner：[prompts/agent-planner.md](../../../prompts/agent-planner.md)
- Summary：[prompts/agent-summary.md](../../../prompts/agent-summary.md)

## Skills
- [skills/ai/agent.md](../../../skills/ai/agent.md)
- [skills/ai/tool-calling.md](../../../skills/ai/tool-calling.md)

## Testing
- 给一个需 2 步 + 调工具的任务，看是否串起来
- 给一个工具做不了的任务，看是否承认而非乱编
- 故意制造死循环，看是否被上限拦住

## Verification
⚠️ Verification Pending。详见 [verification.md](./verification.md)。

## Known Limitations
- 工具有限，复杂任务做不了
- LLM 可能选错工具
- 没有真正的多轮记忆持久化
- 未实际执行验证

## Lessons Learned
见 [lessons.md](./lessons.md)。
