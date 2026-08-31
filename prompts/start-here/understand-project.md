# understand-project
## Use When
你接手了一个已有项目（同事离职交接、开源项目上手、老项目维护），需要快速搞懂"这玩意儿是干嘛的、怎么跑起来的、代码在哪"。

## Goal
产出一份项目结构总览：模块清单、数据流向、入口位置、关键依赖。让一个新人看完能在 30 分钟内知道改哪里、怎么改。

## Input Variables
- `{{project_path}}`：项目根目录的绝对路径，例如 `/Users/xxx/my-project`。

## Prompt
```
你是一位资深技术负责人，擅长用最短时间把一个陌生项目讲明白。

【角色 Role】资深技术负责人
【背景 Context】用户刚接手一个项目，路径是 {{project_path}}。他需要一份"上手地图"：知道模块边界、数据怎么流、入口在哪、依赖什么。这份地图会指导他后续每一次改动。
【目标 Goal】产出一份项目结构总览，让人 30 分钟内能定位"改哪里"。
【约束 Constraints】
1. 不要把每个文件都列出来，只讲"模块边界 + 数据流 + 入口 + 关键依赖"。
2. 全程大白话，专业术语第一次出现配一句解释。
3. 依赖只列"会让项目跑不起来"的关键依赖，不列全部 package。
4. 不要建议重构，这一步只做"理解现状"。
【工作流 Workflow】
1. 读 package.json / go.mod / pom.xml 等，判断技术栈和入口。
2. 浏览顶层目录，按职责分组（页面 / 接口 / 数据 / 工具）。
3. 找入口文件（main / index / app），追一条从"用户请求到数据落库"的主链路。
4. 标出关键依赖（数据库、缓存、第三方服务）。
5. 输出总览 + 一句话"要改 X 应该去 Y 目录"。
【输出格式 Output Format】
# 项目结构总览

## 一句话定位
<这项目是干嘛的>

## 技术栈
<语言 / 框架 / 关键库，每项一句话>

## 模块清单
| 模块 | 路径 | 职责 |
| --- | --- | --- |
| ... | ... | ... |

## 主链路（一条用户请求怎么走完）
1. 用户点 X →
2. 路由到 Y →
3. 调用 Z →
4. 落库到 W

## 关键依赖
- 数据库：...
- 第三方：...

## 改动导航
- 改页面 → 去 ...
- 改接口 → 去 ...
- 改数据 → 去 ...
【验证 Verification】
- 一个新人照着这份能不能在 30 分钟内找到"改登录页"该去哪个文件？
- 主链路是否真的从入口走到了落库？
- 关键依赖是否标了"挂了会怎样"？
```

## Expected Behavior
- 不逐文件罗列，只讲边界和流向。
- 找一条真实主链路，不画理想图。
- 给出"改 X 去 Y"的导航，让总览能直接用。

## Expected Output
（示例片段）
```
# 项目结构总览
## 一句话定位
一个团队周报收集与汇总的工具，前端表单 + 后端定时汇总。
## 技术栈
- Node.js + Express（后端 API）
- Vue 3（前端页面）
- SQLite（嵌入式数据库，一个文件搞定）
## 模块清单
| 模块 | 路径 | 职责 |
| --- | --- | --- |
| 前端 | /web | 表单提交、报告展示 |
| API | /server/routes | 接收周报、查询 |
| 汇总 | /server/jobs | 每周五定时跑 |
## 改动导航
- 改提交表单字段 → /web/src/Form.vue
- 改汇总逻辑 → /server/jobs/weekly.js
```

## Common Mistakes
1. 把每个文件都列出来，文档变成"目录树"，新人看了等于没看。
2. 只画理想架构图，不追真实主链路，跟代码对不上。
3. 不标关键依赖，新人不知道"改这里要先把数据库起起来"。
4. 顺手建议重构，偏离"理解现状"目标，打乱交接节奏。

## Related Skills
- [requirement-analysis](../../skills/core/requirement-analysis/SKILL.md)
- [brainstorming](../../skills/core/brainstorming/SKILL.md)

## Related Workflows
- 暂无对应 workflow，可参考 [start-project](../../workflows/start-project/README.md) 的"理解现状"环节。

## Validation
- [ ] 文件包含所有规定的 `##` 标题
- [ ] Prompt 段落含 Role / Context / Goal / Constraints / Workflow / Output format / Verification
- [ ] 全程中文，术语首次出现有解释
- [ ] ⚠️ Not Yet Verified：本 Prompt 尚未在多种类型项目（前端 / 后端 / 全栈 / 单体 / 微服务）上统一验证。
