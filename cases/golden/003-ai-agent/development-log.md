# 开发日志 - AI Agent

⚠️ 本日志为开发步骤说明，未实际执行。所有"完成"字样指代码结构完成，不代表跑通。

## Step 1 定义工具 schema
为天气 / 算数 / 读文件各写一个 JSON schema：name、description、parameters。
链：[skills/ai/tool-calling.md](../../../skills/ai/tool-calling.md)

## Step 2 权限白名单
给每个工具加 permission 字段（auto / confirm / deny）。
链：[anti-patterns/uncontrolled-agent.md](../../../anti-patterns/uncontrolled-agent.md)

## Step 3 Planner
prompt 让 LLM 看任务 + 历史 + 工具列表，输出"下一步动作"。
链：[prompts/agent-planner.md](../../../prompts/agent-planner.md)

## Step 4 Tool Caller
解析 Planner 输出的 JSON，按 schema 校验后执行。
链：[skills/ai/agent.md](../../../skills/ai/agent.md)

## Step 5 Observer 循环
看工具返回，塞回 Planner 上下文，决定继续或停。
链：[skills/ai/agent.md](../../../skills/ai/agent.md)

## Step 6 终止判定
检查终止条件：完成 / 上限 / 失败阈值。
链：[anti-patterns/uncontrolled-agent.md](../../../anti-patterns/uncontrolled-agent.md)

## Step 7 汇总
任务完成后让 LLM 把中间结果汇总成最终答复。
链：[prompts/agent-summary.md](../../../prompts/agent-summary.md)

⚠️ 未实际执行验证。
