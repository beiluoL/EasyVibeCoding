# AGENTS.md（项目记忆模板）

> 本文件是给 AI 代理（Agent）的**项目记忆模板**。贡献者请复制本文件到你的项目根目录，改名为 `AGENTS.md`，并把方括号 `[...]` 占位符替换为真实内容。完成后删除本段说明。
>
> This is a **template** for project memory. Copy it to your repo root as `AGENTS.md`, fill in the `[...]` placeholders, then delete this note.

## Project Purpose（项目目的）

[一段话说明：本项目是什么、面向谁、成功的标准是什么。EasyVibeCoding 是一套开源的「用 AI 工程化做软件」方法论——核心资产是可复用、可沉淀、可验证的知识：Skill / Prompt / Case / Workflow / Failure / Anti-Pattern / Benchmark。]

最高优先级规则：**诚实（Honesty）**。绝不造假，未验证即标 `⚠️ Not Yet Verified` / `Status: experimental`。

## Repository Structure（仓库结构）

```text
[你的项目名]/
├── README.md                # 首页与导航
├── AGENTS.md                # 本文件（代理记忆）
├── CONTRIBUTING.md          # 贡献指南
├── SECURITY.md              # 安全策略
├── docs/                    # 文档
├── skills/                  # 可复用技能（core / ai / ...）
├── prompts/                 # 提示词模板
├── cases/                   # 案例（beginner / intermediate / advanced / golden）
├── workflows/               # 工作流
├── registry/                # *.yaml 元数据注册表
├── templates/               # 各类资产模板
├── scripts/                 # 校验器（Python，仅标准库）
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
- YAML 元数据字段（**全部必填或保留**，禁止删除）：`name` / `description` / `version` / `category` / `difficulty` / `status` / `verified` / `compatible` / `prerequisites` / `inputs` / `outputs` / `triggers` / `validation` / `last_verified`。

## Case Standards（案例标准）

- 模板：`templates/case/README.md`
- 路径：`cases/<level>/<case-name>/`
- 必含 6 个文件：`README.md` / `requirements.md` / `architecture.md` / `development-log.md` / `lessons.md` / `verification.md`。
- 案例应能**端到端跑通**，否则 `verification.md` 必须写 `⚠️ Verification Pending`。

## Prompt Standards（提示词标准）

- 模板：`templates/prompt/README.md`
- 路径：`prompts/<category>/<prompt-name>.md`
- 必须真正可复制粘贴，含 7 个构建块：**Role / Context / Goal / Constraints / Workflow / Output format / Verification**。

## Verification Rules（验证规则）

- **绝不**把未验证内容标成已验证。
- **诚实规则（HONESTY）**：若 `verified: true`，则 `last_verified` 必须存在且非空；否则校验器拒绝。绝不让未验证内容冒充已验证。
- `verified: false` 时，`status` 必须为 `experimental`，措辞用 `⚠️ Not Yet Verified`。
- 证据包括：能复现的命令 / 测试输出 / 运行截图。无证据 = 未验证。
- 不伪造 GitHub stars、测试结果、运行数据。
- 校验器（均仅用 Python 标准库）：

```text
python3 scripts/validate-skill.py     # 校验 skills/core|ai/*/SKILL.md
python3 scripts/validate-case.py       # 校验 cases/*/<case>/ 6 个必需文件
python3 scripts/validate-prompt.py     # 校验 prompts/**/*.md 必需小节
python3 scripts/validate-registry.py   # 校验 registry/*.yaml 元数据与 path
python3 scripts/check-links.py         # 校验本地链接 + 密钥扫描
python3 scripts/build-index.py         # 生成 docs/INDEX.md
```

## Security Rules（安全规则）

- 禁止提交密钥 / 凭据 / 生产密钥。`scripts/check-links.py` 会扫描 AWS / GitHub / Slack / OpenAI 密钥与私钥。
- Skill 脚本必须文档化 What it does / Inputs / Outputs / Dependencies / Side Effects。
- 禁止凭据窃取 / 隐藏网络请求 / 恶意软件 / 未授权访问 / 破坏性命令。

## Contribution Rules（贡献规则）

- 先复用后新增；小步提交；用模板；跑校验器；更新 registry；如实标注验证状态。
- 一个 PR 只做一件事（一个 Skill / Prompt / Case）。
- 合并前所有校验器必须通过（退出码 0）。

---

## Before editing（编辑前 5 步）

任何代理在修改本仓库内容前，**必须**按序完成：

1. 读 `README.md` —— 理解项目定位与导航。
2. 读 `AGENTS.md`（本文件）—— 理解内容标准与验证规则。
3. 读相关 `templates/` 模板 —— 确保字段与结构正确。
4. 读相关已有内容 —— 避免重复，保持风格一致。
5. 遵守校验规则 —— 跑 validator、更新 registry、如实标注验证状态、自查安全。
