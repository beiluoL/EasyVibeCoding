# Diagrams

## 目的

存放项目用到的 Mermaid 源文件与导出的图片（PNG / SVG）。便于在文档中复用，也方便单独审阅与版本管理。

## 状态

**No diagrams yet; Mermaid lives inline in docs.**

当前所有图都以 Mermaid 代码块直接嵌在文档里（见 [README.md](../../README.md) 的两幅图）。未来若需要导出图片，统一放本目录，并在对应文档中以图片形式引用。

## 命名约定（未来使用）

- Mermaid 源：`<name>.mmd`
- 导出图片：`<name>.png` / `<name>.svg`
- 建议在文件头注释一行说明图的用途与引用位置。

> ⚠️ 不要提交来源不明的截图或伪造的导出图。导出图应能由对应 `.mmd` 重新生成。

相关：[README.md](../../README.md) · [assets/screenshots/](../screenshots/)
