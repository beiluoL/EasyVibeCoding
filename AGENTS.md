# AGENTS.md

> 本文件是给 AI 代理（Agent）的项目记忆。任何代理在读写本仓库前，都应先读本文。

## Project Purpose（项目目的）

EasyVibeCoding 是一套开源的「Vibe Coding 工程化方法论」——让不会编程的人，也能用 AI 按工程化方式做出真正能运行的软件。核心资产是**可复用、可沉淀、可验证的知识**：Skill / Prompt / Case / Workflow / Failure / Anti-Pattern / Benchmark。

最高优先级规则：**诚实（Honesty）**。绝不造假，未验证即标 `⚠️ Not Yet Verified` / `Status: experimental`。

## Repository Structure（仓库结构）

```text
EasyVibeCoding/
├── README.md                # 首页与导航（简体中文，默认）
├── README.en.md             # 首页（English 翻译）
├── README.zh-TW.md          # 首页（繁體中文 翻译）
├── docs/i18n-contributing.md# 多语言 / i18n 贡献指南
├── AGENTS.md                # 本文件（代理记忆）
├── CONTRIBUTING.md          # 贡献指南
├── CODE_OF_CONDUCT.md       # 行为准则
├── SECURITY.md              # 安全策略
├── SUPPORT.md               # 获取帮助
├── CHANGELOG.md             # 变更日志
├── LICENSE                  # MIT
├── .gitignore / .editorconfig / .markdownlint.yml
├── docs/                    # 文档（getting-started / learning-path / faq）
├── skills/                  # 可复用技能（core / ai / devops / ...）
├── prompts/                 # 提示词模板
├── cases/                   # 案例（beginner / intermediate / advanced / golden）
├── failures/                # 失败教训
├── anti-patterns/           # 反模式
├── workflows/               # 工作流
├── benchmarks/              # 模型基准测试
├── registry/                # *.yaml 元数据注册表
├── templates/               # 各类资产模板
├── scripts/                 # 校验器（Python）
└── assets/                  # 图表 / 截图
```

## Content Standards（内容标准）

- **中文为主**，必要时保留英文术语；专业术语首次出现配一句大白话解释。
- 多用**示例 / 表格 / Mermaid**，少空洞套话。
- 所有资产必须基于 `templates/` 模板，YAML 头字段完整。
- 每个资产必须在 `registry/*.yaml` 注册。

## Skill Standards（技能标准）

- 模板：`templates/skill/SKILL.md`
- 每个 Skill 是一个目录 `skills/<category>/<skill-name>/SKILL.md`。
- YAML 元数据字段（**全部必填或保留**，禁止删除）：

| 字段 | 说明 |
| --- | --- |
| `name` | 技能名（kebab-case） |
| `description` | 一句话说明做什么 |
| `version` | 语义化版本，如 `0.1.0` |
| `category` | 分类，如 `core` / `ai` / `backend` |
| `difficulty` | 难度，如 `beginner` / `intermediate` / `advanced` |
| `status` | `experimental` / `stable`（未验证一律 `experimental`） |
| `verified` | 布尔；未验证为 `false` |
| `compatible` | 兼容的模型 / 工具，如 `gpt-4, claude` |
| `prerequisites` | 前置技能或知识 |
| `inputs` | 输入（参数 / 文件 / 上下文） |
| `outputs` | 输出（产物 / 退出码） |
| `triggers` | 触发该技能的关键词 / 场景 |
| `validation` | 如何验证该技能有效 |
| `last_verified` | 上次验证时间；未验证填 `null` |

## Case Standards（案例标准）

- 模板：`templates/case/CASE.md`
- 路径：`cases/<level>/<case-name>/README.md`
- 必含：目标 / 适用人群 / 前置条件 / 步骤 / 期望结果 / 验证方式 / 验证状态。
- 案例应能**端到端跑通**，否则标 `⚠️ Not Yet Verified`。

## Prompt Standards（提示词标准）

- 模板：`templates/prompt/PROMPT.md`
- 路径：`prompts/<category>/<prompt-name>.md`
- 必含：用途 / 适用模型 / 输入占位符 / 示例 / 验证状态。

## Verification Rules（验证规则）

- **绝不**把未验证内容标成已验证。
- `verified: false` 时，`status` 必须为 `experimental`，措辞用 `⚠️ Not Yet Verified`。
- 禁用措辞：`✅ Tested` / `Verified` / `Production Ready`（除非附真实证据）。
- 证据包括：能复现的命令 / 测试输出 / 运行截图。无证据 = 未验证。
- 不伪造 GitHub stars、测试结果、运行数据。

## Security Rules（安全规则）

详见 [SECURITY.md](SECURITY.md)。要点：

- 禁止提交密钥 / 凭据 / 生产密钥。
- Skill 脚本必须文档化 What it does / Inputs / Outputs / Dependencies / Side Effects。
- 禁止凭据窃取 / 隐藏网络请求 / 恶意软件 / 未授权访问 / 破坏性命令。

## Contribution Rules（贡献规则）

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。要点：

- 先复用后新增；小步提交；用模板；跑校验器；更新 registry；如实标注验证状态。

## Multilingual / i18n Rules（多语言规则）

详见 [docs/i18n-contributing.md](docs/i18n-contributing.md)。要点：

- 默认首页永远是简体中文的 `README.md`（GitHub 默认读取它）。
- 其它语言使用独立文件：`README.<lang>.md`（如 `README.en.md` / `README.zh-TW.md`），**不要**创建 `zh/` 或 `en/` 子目录放 README。
- 每份 README 顶部必须放**统一格式的语言切换横幅**：`<div align="right">` 包裹，放在 README 第一行（`#` 标题之前）；当前语言项用 `<strong>` 加粗（无链接），其它语言用 `<a href="README.<lang>.md">` 链接。完整规则与三份实际横幅对照见 [docs/i18n-contributing.md](docs/i18n-contributing.md) 的「横幅规则」节。
- 修改默认 `README.md` 后，**优先同步更新** README.en.md / README.zh-TW.md，否则请在改动处留一段：
  `<!-- TODO(i18n): sync this new section to README.en.md and README.zh-TW.md -->`

- 翻译诚实标记必须保留：`⚠️ Not Yet Verified` / `Status: experimental` / `Planned`——**严禁因为翻译把“未验证”译成“已验证”**。
- 社区翻译请在横幅下方追加一行：
  `> ⚠️ Community translation, may lag the latest default (Simplified Chinese) version.`

---

## Before editing（编辑前 5 步）

任何代理在修改本仓库内容前，**必须**按序完成：

1. 读 [README.md](README.md) —— 理解项目定位与导航，并留意顶部语言横幅的多语言 README 入口。
2. 读 [AGENTS.md](AGENTS.md)（本文件）—— 理解内容标准与验证规则；若涉及多语言翻译，再读 [docs/i18n-contributing.md](docs/i18n-contributing.md)。
3. 读相关 `templates/` 模板 —— 确保字段与结构正确。
4. 读相关已有内容 —— 避免重复，保持风格一致。
5. 遵守校验规则 —— 跑 validator、更新 registry、如实标注验证状态、自查安全。
