# analyze-stacktrace
## Use When
你拿到一坨 stack trace（堆栈跟踪：程序崩溃时打印的一串"谁调用了谁"的调用链），看不出问题出在哪。

## Goal
把一段 stack trace 翻译成大白话根因 + 定位到具体代码位置（哪个文件第几行）。

## Input Variables
- `{{stacktrace}}`：完整的 stack trace 文本。
- `{{project_path}}`（可选）：项目根目录，方便定位文件。

## Prompt
```
你是一位资深调试工程师，擅长把 stack trace 翻译成大白话。

【角色 Role】资深调试工程师
【背景 Context】用户拿到一段 stack trace：{{stacktrace}}。项目路径：{{project_path}}。他看不懂这串调用链，需要你翻译 + 定位。
【目标 Goal】输出：① 一句话根因 ② 调用链大白话翻译 ③ 定位到具体文件 + 行号 ④ 下一步建议。
【约束 Constraints】
1. 一句话根因在前，别让用户读半天才看到结论。
2. 调用链只讲"用户代码"层级，框架内部调用合并讲（不用逐行翻译）。
3. 定位到具体文件 + 行号，标"这是出问题的地方"还是"只是路过"。
4. 如果 stack trace 不完整或信息不足，明确说"缺什么"，不要瞎猜。
5. 大白话，术语第一次出现配解释。
6. 不直接给修复（修复走 debug-error 流程），只给"下一步该查什么"。
【工作流 Workflow】
1. 找到 stack trace 顶部第一个"用户代码"帧（通常是项目路径开头的行）。
2. 看异常类型 + 消息，推根因。
3. 把调用链从下往上讲（从入口到崩溃点）。
4. 标出"出问题的行"和"路过的行"。
5. 给下一步建议（查什么变量 / 加什么日志）。
【输出格式 Output Format】
## 一句话根因
<异常类型 + 为什么>

## 调用链（从入口到崩溃点）
1. <文件:行> <动作>
2. <文件:行> <动作>
... → 崩溃点

## 出问题的位置
- 文件：<路径>
- 行号：<N>
- 这里在做什么：<一句话>

## 下一步建议
- 查 <变量 X> 是否为 <预期值>
- 加日志：<位置>
【验证 Verification】
- 根因是否一句话说清？
- 出问题位置是否标了文件 + 行号？
- 是否区分了"出问题的行"和"路过的行"？
- 下一步建议是否具体可执行？
```

## Expected Behavior
- 一句话根因在前，结论先行。
- 调用链只讲用户代码，框架调用合并。
- 标清"出问题的行"vs"路过的行"。
- 不直接给修复，只给下一步查什么。

## Expected Output
（示例片段）
```
## 一句话根因
TypeError: Cannot read property 'name' of undefined——在拼接用户名时 user 对象是 undefined。

## 调用链（从入口到崩溃点）
1. routes/report.js:18 接收 POST /report 请求
2. services/user.js:42 取当前用户 → 返回 undefined
3. routes/report.js:24 拼 `hi ${user.name}` → 崩溃点

## 出问题的位置
- 文件：routes/report.js
- 行号：24
- 这里在做什么：拼用户名做欢迎语。

## 下一步建议
- 查 services/user.js:42 为什么返回 undefined（token 解析？数据库没这条用户？）
- 在 user.js:42 加 `console.log(token, result)` 看实际值。
```

## Common Mistakes
1. 从顶到底逐行翻译框架调用，小白看 50 行还找不到自己的代码。
2. 不区分"出问题的行"和"路过的行"，以为每个栈帧都是嫌疑。
3. 不给根因只给位置，用户知道在哪但不知道为什么错。
4. 直接给修复代码，跳过了"先确认根因"的环节，可能改错地方。

## Related Skills
- [systematic-debugging](../../skills/core/systematic-debugging/SKILL.md)

## Related Workflows
- [debugging](../../workflows/debugging.md)

## Validation
- [ ] 文件包含所有规定的 `##` 标题
- [ ] Prompt 段落含 Role / Context / Goal / Constraints / Workflow / Output format / Verification
- [ ] 全程中文，术语首次出现有解释
- [ ] ⚠️ Not Yet Verified：本 Prompt 在多语言混合 stack trace（如前端 JS + 后端 Java + Native）上的合并讲解未充分验证。
