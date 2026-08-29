# 易错点与教训 - AI Agent

## 易错点
1. 无终止条件 → 死循环
   对应：[anti-patterns/uncontrolled-agent.md](../../../anti-patterns/uncontrolled-agent.md)
2. 工具描述不清 → LLM 选错工具
   对应：[skills/ai/tool-calling.md](../../../skills/ai/tool-calling.md)
3. 权限过大 → 危险工具被自动执行
   对应：[skills/ai/agent.md](../../../skills/ai/agent.md)
4. 不记中间态 → 循环中上下文丢失
   对应：[skills/ai/agent.md](../../../skills/ai/agent.md)

## Anti-patterns
见 [anti-patterns/uncontrolled-agent.md](../../../anti-patterns/uncontrolled-agent.md)。

## 教训
- 工具描述要写给 LLM 看，越具体越好
- 每个工具默认 deny，按需放开
- 循环上限宁可低不可无
