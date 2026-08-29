# 贡献指南

感谢你有兴趣为 EasyVibeCoding 贡献内容！本仓库的核心资产是**可复用的知识**：Skill、Prompt、Case、Workflow、Failure、Anti-Pattern。本文说明如何正确地添加它们。

## 总原则

- **先复用，再新增**：投稿前先搜索仓库是否已有同类内容，避免重复。
- **诚实标注验证状态**：未经运行验证的内容必须标 `⚠️ Not Yet Verified`、`status: experimental`。**禁止**把未验证内容标成 `✅ Tested / Verified / Production Ready`。
- **小步提交**：一个 PR 聚焦一类资产（一个 Skill 或一个 Case），便于评审。
- **中文为主**：正文用中文，必要时保留英文术语；多用示例 / 表格 / Mermaid，少空洞套话。

## 目录约定

| 资产类型 | 路径 | 模板 |
| --- | --- | --- |
| Skill | `skills/<category>/<skill-name>/SKILL.md` | `templates/skill/SKILL.md` |
| Prompt | `prompts/<category>/<prompt-name>.md` | `templates/prompt/PROMPT.md` |
| Case | `cases/<level>/<case-name>/README.md` | `templates/case/CASE.md` |
| Workflow | `workflows/<workflow-name>.md` | `templates/workflow/WORKFLOW.md` |
| Failure | `failures/<failure-name>.md` | `templates/failure/FAILURE.md` |
| Anti-Pattern | `anti-patterns/<name>.md` | `templates/anti-pattern/ANTI_PATTERN.md` |

> 术语小贴士：**Registry**（注册表）= `registry/*.yaml`，集中登记所有资产元数据，便于检索与 CI 校验。

## 添加一个 Skill（示例流程）

1. 复制 `templates/skill/SKILL.md` 到 `skills/<category>/<skill-name>/SKILL.md`。
2. 填写 YAML 元数据（字段见 [AGENTS.md](AGENTS.md) 的 Skill Standards），**不要删字段**。
3. 写正文：目标 / 适用场景 / 步骤 / 示例 / 输出 / 验证状态。
4. 运行校验：`python3 scripts/validate-skill.py skills/<category>/<skill-name>/SKILL.md`
5. 在 `registry/skills.yaml` 注册条目。
6. 提交 PR，描述这个 Skill 解决什么问题。

Prompt / Case / Workflow / Failure / Anti-Pattern 的流程类似，只是校验器与模板不同。

## 必须运行的校验器

提交前请运行（按需）：

```bash
python3 scripts/validate-skill.py   <path-to-skill>
python3 scripts/validate-prompt.py  <path-to-prompt>
python3 scripts/validate-case.py    <path-to-case>
python3 scripts/validate-registry.py
```

> ⚠️ Not Yet Verified：V0.1 阶段校验器本身也未经完整运行验证，如遇报错请提 issue。

## 更新 Registry

每新增一个资产，都要在对应的 `registry/*.yaml` 增加一条记录，字段与资产 YAML 头保持一致。未注册的资产不会被 CI 识别。

## 验证状态标注规则

| 状态字段值 | 含义 | 可用措辞 |
| --- | --- | --- |
| `verified: true` + 附证据 | 已验证 | `✅ Verified` |
| `verified: false` | 未验证 | `⚠️ Not Yet Verified` |
| `status: experimental` | 实验性 | `Status: experimental` |

**严禁**对 `verified: false` 的内容使用 `✅ Tested / Verified / Production Ready`。详见 [AGENTS.md](AGENTS.md) 的 Verification Rules。

## 投稿 Checklist

- [ ] 已读 [README.md](README.md) 与 [AGENTS.md](AGENTS.md)
- [ ] 使用了对应 `templates/` 模板，未删 YAML 字段
- [ ] 正文中文为主，配示例 / 表格 / Mermaid
- [ ] 运行了相关校验器且通过
- [ ] 更新了 `registry/*.yaml`
- [ ] 验证状态标注属实（未验证标 ⚠️）
- [ ] 无密钥 / 凭据 / 敏感信息（见 [SECURITY.md](SECURITY.md)）
- [ ] PR 描述写清“解决什么问题 + 如何复现验证”

---

感谢你的贡献！每一个被沉淀的 Skill / Failure，都会让下一个小白少踩一次坑。
