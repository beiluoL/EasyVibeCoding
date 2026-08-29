# Changelog

本文件遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式，
版本号采用 [Semantic Versioning](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added

- EasyVibeCoding V0.1 初始 bootstrap：仓库根目录基础文件（README / LICENSE / CONTRIBUTING / CODE_OF_CONDUCT / SECURITY / SUPPORT / CHANGELOG / AGENTS / .gitignore / .editorconfig / .markdownlint.yml）。
- 内容标准骨架：Skill / Prompt / Case / Workflow / Failure / Anti-Pattern 的目录与模板约定。
- Validator 脚手架约定：`scripts/validate-skill.py`、`validate-prompt.py`、`validate-case.py`、`validate-registry.py`。
- CI 约定：registry 校验 + markdownlint。

### Notes

- **No runtime verification performed yet.**（尚未进行任何运行时验证）
- V0.1 仅完成内容标准与脚手架，所有功能标记为 `⚠️ Not Yet Verified` / `Status: experimental`。
- Roadmap 中 V0.2 及以后均为计划状态。

[Unreleased]: https://github.com/easyvibecoding/EasyVibeCoding/compare/HEAD
