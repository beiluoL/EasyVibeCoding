# analyze-requirement
## Use When
你已经有了一份 Project Brief（项目简介），需要把它拆成开发能照着做的需求清单。

## Goal
把 Project Brief 拆成 FR（Functional Requirement，功能需求：用户能做什么）+ NFR（Non-Functional Requirement，非功能需求：性能 / 安全 / 兼容性等"看不见但很重要"的指标）清单，每条配验收标准。

## Input Variables
- `{{project_brief}}`：上一阶段产出的 Project Brief 文本。
- `{{constraints}}`（可选）：已知约束，如"必须用 XX 框架 / 预算 0 元 / 用户量 < 100"。

## Prompt
```
你是一位资深需求分析师，擅长把"项目简介"拆成开发能照着做的需求清单。

【角色 Role】资深需求分析师
【背景 Context】用户提供了一份 Project Brief：{{project_brief}}。已知约束：{{constraints}}。需要把模糊的"做什么"变成可验收的清单。
【目标 Goal】产出 FR + NFR 两张清单，每条需求配验收标准（怎样算做完）。
【约束 Constraints】
1. 每条需求必须能"做完 / 没做完"二选一，不要"尽量优化""做得好一点"这种模糊话。
2. FR 聚焦"用户能做什么"，NFR 聚焦"性能 / 安全 / 兼容 / 可用性"。
3. 不在这步选技术，只定义"要满足什么"。
4. 大白话，术语第一次出现配解释。
5. 每条需求标 ID（FR-001 / NFR-001），方便后续追踪。
【工作流 Workflow】
1. 从 Brief 抽出用户能做的动作 → 写 FR。
2. 对每个 FR 想可能的"坑"（慢 / 不安全 / 不兼容）→ 写 NFR。
3. 给每条写验收标准（用什么场景验证）。
4. 标优先级（P0 必做 / P1 应做 / P2 可做）。
5. 输出两张表 + 一句话"遗漏风险"。
【输出格式 Output Format】
# 需求清单

## 功能需求 FR
| ID | 需求 | 优先级 | 验收标准 |
| --- | --- | --- | --- |
| FR-001 | ... | P0 | <场景：当...时，应该...> |

## 非功能需求 NFR
| ID | 类别 | 指标 | 验收标准 |
| --- | --- | --- | --- |
| NFR-001 | 性能 | ... | <可测量的数字，如<200ms> |

## 遗漏风险
<一句话>
【验证 Verification】
- 每条需求是否都能"做完 / 没做完"二选一？
- NFR 是否给了可测量的数字，而不是"快一点"？
- 优先级是否标了 P0/P1/P2？
```

## Expected Behavior
- FR 聚焦"用户动作"，不写实现细节。
- NFR 给可测量数字（"<200ms"、"支持 100 并发"），不给形容词。
- 每条需求都能二选一判断"做完没做完"。

## Expected Output
（示例片段）
```
## 功能需求 FR
| ID | 需求 | 优先级 | 验收标准 |
| --- | --- | --- | --- |
| FR-001 | 用户能录入一条房租 | P0 | 输入金额+日期，点保存，列表出现这条 |
| FR-002 | 到期前 3 天弹通知 | P0 | 设到期日为今天+3，第二天起每次打开都提示 |

## 非功能需求 NFR
| ID | 类别 | 指标 | 验收标准 |
| --- | --- | --- | --- |
| NFR-001 | 性能 | 录入响应 < 300ms | 本地 1000 条数据下录入，响应不超 300ms |
| NFR-002 | 可用性 | 离线可录入 | 断网状态下能录入，联网后同步 |
```

## Common Mistakes
1. FR 写成实现细节（"用 Redis 缓存"），需求阶段不该选技术。
2. NFR 全是形容词（"快""安全""好用"），没法验收。
3. 不标优先级，开发做到一半才发现 P0 没做完。
4. 每条需求写得像小说，看半天不知道做完没做完。

## Related Skills
- [requirement-analysis](../../skills/core/requirement-analysis/SKILL.md)

## Related Workflows
- [feature-development](../../workflows/feature-development.md)

## Validation
- [ ] 文件包含所有规定的 `##` 标题
- [ ] Prompt 段落含 Role / Context / Goal / Constraints / Workflow / Output format / Verification
- [ ] 全程中文，术语首次出现有解释
- [ ] ⚠️ Not Yet Verified：本 Prompt 在大型企业级项目（多团队协作）上的拆分粒度尚未验证。
