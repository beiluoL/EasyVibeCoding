# Skill 模板说明（Skill Template）

本目录提供 Skill 的**规范模板**。每个 Skill 是一个独立目录，放在 `skills/<category>/<skill-name>/` 下。

## 目录约定

```text
skills/
├── core/                      # 非 AI、确定性技能
│   └── my-skill/
│       ├── SKILL.md           # 规范说明（必需）
│       ├── README.md          # 人读概览（推荐）
│       └── examples/          # 可选的示例
└── ai/                        # LLM 驱动技能
    └── another-skill/
        └── ...
```

- `<category>` 取 `core`（非 AI、确定性）或 `ai`（LLM 驱动）。
- `<skill-name>` 用 kebab-case，**必须**与 `SKILL.md` 里 `name` 字段一致。
- `SKILL.md` **必须**以规范 YAML 前置元数据开头——直接复制 [`SKILL.md`](SKILL.md)。
- `verified` **必须**保持 `false`，直到该技能被真正运行并观察到有效；之后才能设 `verified: true` 并填写 `last_verified`。

## 如何新增一个 Skill

1. 复制 [`SKILL.md`](SKILL.md) 到 `skills/<core|ai>/<your-skill-name>/SKILL.md`。
2. 填写前置元数据（`name` / `description` / `difficulty` / `status` 等）。
3. 编写正文各小节。
4. （可选）添加 `README.md` 与 `examples/`。
5. 在 [`../../registry/skills.yaml`](../../registry/skills.yaml) 注册该技能，`path` 指向技能目录。
6. 运行校验：

   ```bash
   python3 ../../scripts/validate-skill.py
   python3 ../../scripts/validate-registry.py
   ```

7. 运行 [`../../scripts/check-links.py`](../../scripts/check-links.py) 检查失效链接与密钥泄露。

## 相关

- 技能校验器：[`../../scripts/validate-skill.py`](../../scripts/validate-skill.py)
- 注册表：[`../../registry/skills.yaml`](../../registry/skills.yaml)
- 规范来源：[`../../AGENTS.md`](../../AGENTS.md) 的 Skill Standards 小节
