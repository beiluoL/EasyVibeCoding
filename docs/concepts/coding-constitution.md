# AI Coding Constitution AI 编程宪法

> 用 AI 写代码的人，应当遵守以下宪法。

AI 让写代码的门槛大幅降低，但也让"看起来像代码"的东西大量涌入项目。这份宪法把工程化的底线写成 10 条，每条一句话原则、一句解释、一句违背后果。读完请到文末的承诺清单确认。

## 十条宪法

### 1. Understand before coding
写代码前先理解需求。
不弄清"到底要解决什么、给谁用、什么算成功"就动手，方向一错后面全是返工。
**违背后果**：代码可能很漂亮，但解决的不是真正的问题。

### 2. Plan before implementing
实现前先有计划。
先想清楚分几步、每步依赖什么、谁先做，再下笔。
**违背后果**：做到一半才发现步骤对不上，反复推翻重来。

### 3. Prefer small changes
优先小步改动。
一次只改一小块、能独立验证的改动，别一口气重写半个模块。
**违背后果**：大改动一出问题很难定位，回滚也难。

### 4. Reuse existing patterns
先复用既有模式。
项目里已有的写法、已有的工具函数，先拿来用，再造轮子。
**违背后果**：同一种功能出现 N 种写法，维护成本翻倍。

### 5. Never trust unverified output
永不轻信未验证输出。
AI 说"做完了"只是声明，要看客观证据（见 [verification](./verification.md)）。
**违背后果**：把"看起来对"的代码合进去，线上才暴雷。

### 6. Every feature needs acceptance criteria
每个功能都要有验收标准。
开工前就写清"做到什么算完成"，而不是做完才想。
**违背后果**：做完了说不清算不算好，验收靠感觉。

### 7. Every bug needs a reproducible cause
每个 Bug 都要可复现的根因。
先能稳定复现、再定位根因、最后才修，而不是乱改试运气。
**违背后果**：改了表象过几天又犯，或改坏别的地方。

### 8. Every completed task needs verification
每个完成的任务都要验证。
任务收尾必须有客观证据证明它真的完成了。
**违背后果**：任务在"薛定谔状态"下被合入，问题到下游才暴露。

### 9. High-risk actions require human approval
高风险动作必须人批准。
删文件、发版、改生产配置、动数据库，这些事 AI 不能自作主张。
**违背后果**：AI 一时"自信"可能造成不可逆的线上事故。

### 10. Every repeated mistake should become knowledge
每个重复错误都应变成知识。
同一个坑踩两次就该记下来（见 [memory](./memory.md)），第三次就是失职。
**违背后果**：团队反复踩同一个坑，时间白白浪费。

## 七大原则对照

这 10 条宪法脱胎于项目的七大原则，对应关系：

| 宪法条目 | 对应原则 |
| --- | --- |
| 1 Understand before coding | 01 Understand before coding |
| 2 Plan / 3 Small changes / 4 Reuse | 02 Small tasks、03 Reuse before reinvent |
| 5 Never trust / 8 Every task verified | 04 Evidence over claims |
| 9 Human approval | 05 Human owns decisions |
| 10 Mistake becomes knowledge | 06 Every mistake becomes knowledge |
| 6 验收标准 / 7 根因 / 8 验证 | 贯穿 04、07 From Prompt to Production |

## 我承诺遵守

复述清单，确认即承诺：

- [ ] 我会先理解需求，再写代码
- [ ] 我会先有计划，再实现
- [ ] 我会优先小步、可独立验证的改动
- [ ] 我会先复用项目既有模式，再造轮子
- [ ] 我永不轻信 AI 未经验证的输出
- [ ] 我会给每个功能写验收标准
- [ ] 我会让每个 Bug 都有可复现的根因
- [ ] 我会验证每个完成的任务
- [ ] 我会让高风险动作经过人批准
- [ ] 我会把重复错误沉淀成知识

## 相关资源

- 验证：[verification](./verification.md)
- 记忆与知识沉淀：[memory](./memory.md)
- 系统化调试：[debugging](../best-practices/debugging.md)
- 发版检查：[deployment](../best-practices/deployment.md)
- 七大原则全文：项目根 `README.md`
