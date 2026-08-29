# EasyVibeCoding FAQ 常见问答

面向小白的高频问题，每条简短直接。先看这里，再深入对应概念文档。

## Vibe Coding 是什么

Vibe Coding 指用自然语言跟 AI 协作写代码的方式：你描述要什么，AI 写代码，你验证和决策。大白话：不用从零敲代码，而是"指挥" AI 干活。

相关：[prompt](../concepts/prompt.md)、[agent](../concepts/agent.md)

## Vibe Coding 和让 AI 直接写项目有啥区别

让 AI 直接写整个项目是"一把梭"，常常跑不起来、风格混乱、改不动。Vibe Coding 强调工程化：先理解、拆小任务、复用、验证、人决策。区别不在"用不用 AI"，而在"有没有工程纪律"。

相关：[coding-constitution](../concepts/coding-constitution.md)、[task-decomposition](../best-practices/task-decomposition.md)

## 我完全不会编程能用吗

能开始，但不能只会"指挥"。你需要学会读代码大意、看懂报错、判断 AI 说的对不对。完全不懂就全盘接受 AI 输出，风险很大（它会说错甚至编造）。建议边用边补基础。

相关：[verification](../concepts/verification.md)、[review](../best-practices/review.md)

## 用哪个 AI 工具好

没有唯一答案，按场景选：写小段代码可用通用对话类工具；改本地项目建议用能读写文件、能跑命令的编程类工具（如带 Agent 能力的 IDE）。关键是工具能否给 AI 提供读代码和执行的能力。

相关：[agent](../concepts/agent.md)、[context-engineering](../concepts/context-engineering.md)

## AI 说做完了但我跑不起来怎么办

别信"做完了"，去看证据（原则 04）。先看报错信息、构建能不能过、实际跑一下关键路径。AI 说完成 ≠ 真完成。

相关：[verification](../concepts/verification.md)、[debugging](../best-practices/debugging.md)

## Token 是什么为什么要钱

Token 是 AI 计算你输入输出的最小单位，大致一个汉字算一两个 token。用得多就花钱，像流量套餐。上下文塞太满、反复贴大段代码都会烧 token。学会挑该给的上下文能省钱又提质量。

相关：[context-engineering](../concepts/context-engineering.md)

## 怎么避免 AI 改坏代码

三招：小步改（一次一小块）、每次改完跑测试、用版本控制能随时退。别让 AI 一次性大改，也别在没测试和没备份的情况下乱动。

相关：[task-decomposition](../best-practices/task-decomposition.md)、[testing](../best-practices/testing.md)

## API Key 要给 AI 吗安全吗

不要把密钥写进代码或交给 AI 的对话。密钥放环境变量或密钥管理服务，代码里只读变量名。给 AI 看的代码里绝不能含真实密钥。Agent 需要执行命令时，用最小权限，高风险动作必须人审批。

相关：[deployment](../best-practices/deployment.md)、coding-constitution 第 9 条

## RAG / Agent / MCP 是啥先学哪个

- **RAG**（检索增强生成）：让 AI 先去查资料再回答，大白话"开卷考试"。
- **Agent**：能自主多步、用工具完成目标的 AI。
- **MCP**（模型上下文协议）：一种让 AI 接外部工具/数据的接口标准，大白话"AI 的插件口"。

建议先学 Prompt 和 Verification，再学 Agent，RAG 和 MCP 等遇到具体场景再深入。

相关：[prompt](../concepts/prompt.md)、[agent](../concepts/agent.md)、[verification](../concepts/verification.md)

## AI 写的代码要不要测试

要。测试是判断"对不对"最省力的客观证据。AI 写的代码"看起来对"很多，只有测试能给明确过/不过。

相关：[testing](../best-practices/testing.md)

## AI 会编造不存在的函数吗

会，这叫"幻觉"。它可能调用根本不存在的库函数或编造 API。所以产出必须验证：能跑、行为对、关键函数真实存在。别看代码"像那么回事"就信。

相关：[verification](../concepts/verification.md)、[review](../best-practices/review.md)

## 一段 Prompt 让 AI 写整个功能行不行

不推荐。大 Prompt 让 AI 一次干太多，容易漏约束、产出超长难验证。拆成小任务分步走更稳，每步还能独立验收。

相关：[task-decomposition](../best-practices/task-decomposition.md)、原则 02

## 怎么让 AI 知道我项目的风格

先让它读懂项目（入口、目录、一个样板功能、规范文档），把关键事实记进 Memory，每次给任务时带上相关上下文。别指望它"自己猜对"。

相关：[project-understanding](../best-practices/project-understanding.md)、[memory](../concepts/memory.md)

## AI 修 Bug 改了又坏怎么办

大概率是没找根因，只压了表象。按系统化调试：先稳定复现 → 收集证据 → 缩小范围 → 定位根因 → 最小修复 → 验证。别让 AI"猜着改"。

相关：[debugging](../best-practices/debugging.md)、coding-constitution 第 7 条

## 发版前到底要检查什么

按发版检查清单逐条核：代码已评审、测试全绿、构建成功、配置和密钥正确、有回滚预案、人审批。没有回滚预案的发版等于裸奔。

相关：[deployment](../best-practices/deployment.md)

## Agent 能不能全自动发版

不能。发版是不可逆的高危动作，宪法第 9 条要求必须人批准。Agent 可以跑检查清单、准备回滚方案，但"按下发版键"必须人来。

相关：[agent](../concepts/agent.md)、[deployment](../best-practices/deployment.md)

## Skill 和 Prompt 啥区别

Prompt 是单次指令，用完即弃；Skill 是把反复出现的指令+步骤+验收打包成可复用的能力包。同类活干第三次，就该考虑抽成 Skill。

相关：[skill](../concepts/skill.md)、[prompt](../concepts/prompt.md)

## 更多问题请到 Discussions。
