# 多语言 / i18n 贡献指南

> Translations welcome! 欢迎贡献翻译！翻訳歓迎！번역을 환영합니다!

EasyVibeCoding 的国际化方案参考主流开源项目（如 Vue / Vite / Element Plus / Mermaid 等）：**在仓库根下放多份 `README.<LANG>.md`，并在每份 README 顶部放置统一的语言切换横幅**。

```
<div align="right">
  <strong>🌏 English</strong> · <a href="README.md">🇨🇳 简体中文</a> · <a href="README.zh-TW.md">🇹🇼 繁體中文</a>
</div>
```

当前已支持的语言（V0.1 首发）：

| 语言 | 文件 | 维护状态 |
| --- | --- | --- |
| 🇨🇳 简体中文（默认） | [README.md](../README.md) | ✅ 官方维护 |
| 🌏 English | [README.en.md](../README.en.md) | ✅ 官方翻译（V0.1 同步） |
| 🇹🇼 繁體中文 | [README.zh-TW.md](../README.zh-TW.md) | ✅ 官方翻译（V0.1 同步） |
| 🇯🇵 日本語 | `README.ja.md` | 🔜 欢迎贡献 |
| 🇰🇷 한국어 | `README.ko.md` | 🔜 欢迎贡献 |
| 🇪🇸 Español | `README.es.md` | 🔜 欢迎贡献 |
| 🇫🇷 Français | `README.fr.md` | 🔜 欢迎贡献 |

> 非官方翻译请在 README 的翻译横幅下方追加一行小字：`> ⚠️ Community translation, may lag the latest default (Simplified Chinese) version.`（社区翻译，可能落后于默认简中版本）。

---

## 命名规范

- **默认语言（简体中文）**：保留 `README.md`（GitHub 默认读取这个文件）。
- **其它语言**：`README.<lang>.md`，`<lang>` 使用 [IETF BCP 47](https://en.wikipedia.org/wiki/IETF_language_tag) 常用格式：
  - `en`（英文）
  - `zh-TW`（繁体中文，台港澳通用，**不要**用 `zh-Hant` 作为文件名——更常用可读的是 `zh-TW`；繁中内容可以写成「繁體中文」字样）
  - `ja`（日语）
  - `ko`（韩语）
  - `es`（西语）
  - `fr`（法语）

---

## 新增一个语言的翻译（5 步搞定）

1. **复制**当前最新的默认 `README.md`（简体中文，通常也是最领先的版本）到 `README.<lang>.md`。
2. **替换顶部横幅**（语言栏顺序：English · 简体中文 · 繁體中文 · …你的新语言），并把你的语言项改成 `<strong>` + emoji 高亮。
3. **正文翻译**。推荐逐段落翻译，保持原段落顺序、标题层级和链接目标不变；Mermaid 图中的标签建议也翻译。
4. **交叉更新**其它已存在的 README 语言文件顶部横幅，把新语言加到横幅里。
5. **跑校验 + 提交 PR**：
   ```bash
   # 1) 检查翻译中使用的所有相对链接是否仍存在
   python3 scripts/check-links.py .

   # 2) 可选：检查所有翻译文件都指向了同一套 docs/ skills/ prompts/ 路径
   grep -r "链接不应该出现乱码或断链" README.*.md  # 自查
   ```
   然后按 [CONTRIBUTING.md](../CONTRIBUTING.md) 流程开 PR。

---

## 翻译原则（和默认 `README.md` 一样的诚实规则！）

**最高优先级：诚实不造假。** 翻译时绝不新增任何：`✅ Verified`、`✅ Tested`、`Production Ready`、伪造的运行截图、伪造的 Benchmark 数字。如果原文写着 `⚠️ Not Yet Verified` / `Status: experimental` / `⚠️ Verification Pending`，翻译**必须保留**并给出对应的本地化用语：

| 原文 | 简体（默认） | 繁體中文 | English |
| --- | --- | --- | --- |
| Not Yet Verified | ⚠️ 尚未验证 | ⚠️ 尚未驗證 | ⚠️ Not Yet Verified |
| Verification Pending | ⚠️ 验证待补充 | ⚠️ 驗證待補充 | ⚠️ Verification Pending |
| Status: experimental | 状态：实验性 | 狀態：實驗性 | Status: experimental |
| Planned | 计划中 | 規劃中 | Planned |

> 术语统一：第一次出现专业术语时，允许保留英文词 + 本地大白话解释。推荐：同一语言文件中术语保持一致（可参考 docs/concepts/*.md 的用法）。

---

## 版本同步（如何跟上上游默认 README.md）

默认语言 `README.md` 发生变化后，其它语言可能暂时滞后。推荐的**最小同步流程**：

```bash
# 1) 检查默认 README 相比上次你的翻译，改动了哪些段落（用 git diff）
git diff HEAD~1 -- README.md

# 2) 逐段把改动同步到 README.en.md / README.zh-TW.md 等
#    若某段改到了你不确定如何译的内容，可在译文里留一段注释：
#    <!-- TODO(i18n): translate new section "Roadmap V0.6" -->

# 3) 跑完 check-links 再提交
python3 scripts/check-links.py .
```

---

## 翻译验收清单（开 PR 前请勾选）

- [ ] 顶部语言切换横幅已正确互链（所有语言文件都出现了新语言的入口）
- [ ] 默认 README.md 的主要章节（项目介绍 / 导航 / 为什么用 / 给谁用 / 快速开始 / 用户旅程 / 两幅 Mermaid / 核心目录 / 学习路径 / 诚实规则 / 贡献 / 路线图 / 7 条原则 / License）翻译中未缺漏
- [ ] 所有**相对链接**仍指向真实文件（未改 `docs/...` / `skills/...` / `prompts/...` / `cases/...` 等路径）
- [ ] Mermaid 语法未被破坏（两份翻译的 Mermaid 图可以用 Mermaid Live Editor 或 IDE Mermaid 预览自查）
- [ ] 诚实规则标记（⚠️ Not Yet Verified / Status: experimental / Planned）**保留且一致**——没有因为翻译而不小心把「未验证」翻译成了「已验证」
- [ ] 运行 `python3 scripts/check-links.py .` 无新增坏链接
- [ ] 运行 `python3 scripts/build-index.py .` 无影响（多语言 README 不应该修改 docs/INDEX.md 本身）

---

## 致谢

每一位贡献新语言或维护旧翻译同步的贡献者，都会在 README 翻译横幅背后的 CONTRIBUTORS 致谢列表中出现（V0.2 规划）。
