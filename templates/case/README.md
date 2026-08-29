# Case 模板说明（Case Template）

一个「案例（Case）」是一次可复现的、端到端的软件构建故事。每个案例目录**必须**包含以下 6 个文件：

| 文件 | 用途 |
| --- | --- |
| `README.md` | 概览 + 下文列出的全部必需小节。 |
| `requirements.md` | 做什么、为什么。 |
| `architecture.md` | 系统设计与关键决策。 |
| `development-log.md` | 按时间顺序的构建日志。 |
| `lessons.md` | 哪些有效、哪些失败、可复用什么。 |
| `verification.md` | 是否真正跑通。**未验证时必须写 `⚠️ Verification Pending`。** |

## 目录约定

```text
cases/
├── golden/              # 已验证、高质量案例
│   └── <case-name>/
│       ├── README.md
│       ├── requirements.md
│       ├── architecture.md
│       ├── development-log.md
│       ├── lessons.md
│       └── verification.md
├── beginner/            # 入门级案例
└── intermediate|advanced/
```

- `golden` 案例的 `verification.md` 强制必需（已包含在上表）。
- 案例应能**端到端跑通**；跑通前 `verification.md` 必须含 `⚠️ Verification Pending`。

## README.md 必需小节

一个案例的 `README.md` **必须**包含以下小节：

1. **Project Goal（项目目标）** — 项目交付什么。
2. **Difficulty（难度）** — beginner / intermediate / advanced。
3. **Prerequisites（前置条件）** — 假设的技能 / 知识。
4. **Tech Stack（技术栈）** — 语言、框架、服务。
5. **User Scenario（用户场景）** — 谁用、怎么用。
6. **MVP** — 最小可行范围。
7. **Architecture（架构）** — 高层设计。
8. **Workflow（工作流）** — 构建步骤 / 使用的技能链。
9. **Prompts（提示词）** — 用到的提示词（链接到 `prompts/`）。
10. **Skills（技能）** — 应用的技能（链接到 `skills/`）。
11. **Testing（测试）** — 如何检查正确性。
12. **Verification（验证）** — 运行证据；**诚实规则**：未真正验证前写 `⚠️ Verification Pending`。
13. **Known Limitations（已知局限）** — 不做什么。
14. **Lessons Learned（经验总结）** — 提炼（链接到 `lessons.md`）。

## 诚实规则（Honesty）

`verification.md` 必须包含 `⚠️ Verification Pending`，直到该案例被真正运行并观察到通过。绝不在没有运行证据时宣称成功。

## 相关

- 案例校验器：[`../../scripts/validate-case.py`](../../scripts/validate-case.py)
- 注册表：[`../../registry/cases.yaml`](../../registry/cases.yaml)
