# Prompt 模板说明（Prompt Template）

一个「提示词（Prompt）」是**真正可复制粘贴**的指令。复制下方的模板正文到 `prompts/<category>/<prompt-name>.md` 并填空即可。

## 要求

- 提示词必须真正可复制粘贴——禁止「自行判断」式的含糊表述。
- 必须包含 7 个构建块：**Role / Context / Goal / Constraints / Workflow / Output format / Verification**。
- 校验器 [`../../scripts/validate-prompt.py`](../../scripts/validate-prompt.py) 要求以下 `##` 小节存在（缺一即 FAIL）：`Use When` / `Goal` / `Input Variables` / `Prompt` / `Expected Behavior` / `Expected Output` / `Validation`。
- 以下小节缺失仅告警（不 FAIL）：`Common Mistakes` / `Related Skills` / `Related Workflows`。
- 小节标题可用双语（如 `## Use When（何时使用）`），校验器按前缀匹配，不影响通过。

## 模板正文（复制下方内容到你的提示词文件）

~~~markdown
# {{Prompt Name（提示词名称）}}

## Use When（何时使用）

> 何时使用本提示词。

## Goal（目标）

> 本提示词要达成的结果。

## Input Variables（输入变量）

- `{{VAR1}}`：说明。
- `{{VAR2}}`：说明。

## Prompt（提示词正文）

```
Role: ...
Context: ...
Goal: ...
Constraints: ...
Workflow: ...
Output format: ...
Verification: ...
```

## Expected Behavior（期望行为）

> 模型应当做什么。

## Expected Output（期望输出）

```
<正确输出示例>
```

## Validation（验证）

> 如何核对结果正确。

## Common Mistakes（常见错误）

- ...

## Related Skills（相关技能）

- `skills/<category>/<skill-name>/SKILL.md`

## Related Workflows（相关流程）

- `workflows/<workflow-name>/README.md`
~~~

## 相关

- 提示词校验器：[`../../scripts/validate-prompt.py`](../../scripts/validate-prompt.py)
- 注册表：[`../../registry/prompts.yaml`](../../registry/prompts.yaml)
