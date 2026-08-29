# Development Log — RAG 问答应用

> ⚠️ Verification Pending — 以下步骤为**计划中的构建顺序**，尚未实际执行。每步标注了拟用的 prompt/skill，但代码未真正生成与运行。

## 构建原则

一次只做一件事、每步可验证。参考 [`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)。

## 步骤 1 — 文档加载

**做什么**：读 PDF/MD 成纯文本，保留段落分隔。PDF 用 PyMuPDF，MD 直接读。

**拟用 prompt**：[`../../../prompts/start-here/start-project.md`](../../../prompts/start-here/start-project.md)

**拟用 skill**：[`../../../skills/core/project-discovery/SKILL.md`](../../../skills/core/project-discovery/SKILL.md)

**验收点**：给一份样例文档，打印出纯文本且分段落，无乱码。

> ⚠️ 未实际执行。

## 步骤 2 — 切块

**做什么**：用递归切分器把文本切成片段（默认 500 字/块，重叠 50）。每块带编号与来源。

**拟用 prompt**：[`../../../prompts/ai-app/build-rag.md`](../../../prompts/ai-app/build-rag.md)

**拟用 skill**：[`../../../skills/ai/rag/SKILL.md`](../../../skills/ai/rag/SKILL.md)

**验收点**：打印块数与各块前 20 字，确认块大小合理、无重复无遗漏。

> ⚠️ 未实际执行。

## 步骤 3 — Embedding

**做什么**：调 Embedding API 把每块转成向量；问题也用同模型转向量。

**拟用 prompt**：[`../../../prompts/ai-app/build-rag.md`](../../../prompts/ai-app/build-rag.md)

**拟用 skill**：[`../../../skills/ai/rag/SKILL.md`](../../../skills/ai/rag/SKILL.md)

**验收点**：一块文本→一个向量，维度与模型说明一致；key 从环境变量读。

> ⚠️ 未实际执行。

## 步骤 4 — 入向量库

**做什么**：用 Chroma 本地持久化存入向量与元数据（文件名、块号、原文）。

**拟用 prompt**：[`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**拟用 skill**：[`../../../skills/core/architecture-design/SKILL.md`](../../../skills/core/architecture-design/SKILL.md)

**验收点**：入库后查 Chroma，块数与步骤 2 一致；重启程序库仍在。

> ⚠️ 未实际执行。

## 步骤 5 — 检索 Top-K

**做什么**：问题向量化 → Chroma 相似度检索 → 取 Top-K（默认 3）片段。

**拟用 prompt**：[`../../../prompts/ai-app/build-rag.md`](../../../prompts/ai-app/build-rag.md)

**拟用 skill**：[`../../../skills/ai/rag/SKILL.md`](../../../skills/ai/rag/SKILL.md)

**验收点**：问一个文档内关键词，Top-K 里含正确片段；打印各片段分数。

> ⚠️ 未实际执行。

## 步骤 6 — 拼装 Prompt

**做什么**：把检索片段作为上下文 + 用户问题 + "仅基于上下文答，无依据说不知道" + "标注出处"指令，组装成 LLM Prompt。控总长不超窗口。

**拟用 prompt**：[`../../../prompts/ai-app/build-context.md`](../../../prompts/ai-app/build-context.md)

**拟用 skill**：[`../../../skills/ai/context-engineering/SKILL.md`](../../../skills/ai/context-engineering/SKILL.md)

**验收点**：打印最终 Prompt，确认含上下文+问题+引用要求，总长在窗口内。

> ⚠️ 未实际执行。

## 步骤 7 — 问答与多轮

**做什么**：调 LLM 生成回答；保留对话历史以支持追问。

**拟用 prompt**：[`../../../prompts/coding/implement-feature.md`](../../../prompts/coding/implement-feature.md)

**拟用 skill**：[`../../../skills/core/implementation/SKILL.md`](../../../skills/core/implementation/SKILL.md)

**验收点**：问文档内问题，回答正确；追问能引用前文。

> ⚠️ 未实际执行。

## 步骤 8 — 引用来源与错误兜底

**做什么**：解析回答中引用的片段号，回链到原文展示；文档外问题应触发"未覆盖"；key 不入库自查。

**拟用 prompt**：[`../../../prompts/debugging/debug-error.md`](../../../prompts/debugging/debug-error.md) · [`../../../prompts/review/security-review.md`](../../../prompts/review/security-review.md)

**拟用 skill**：[`../../../skills/core/systematic-debugging/SKILL.md`](../../../skills/core/systematic-debugging/SKILL.md) · [`../../../skills/core/verification-before-completion/SKILL.md`](../../../skills/core/verification-before-completion/SKILL.md)

**验收点**：文档外问题回答含"未覆盖"；引用能在原文找到；grep 无真实 key。

> ⚠️ 未实际执行。

## 状态总览

| 步骤 | 状态 |
| --- | --- |
| 1 文档加载 | ⚠️ 未执行 |
| 2 切块 | ⚠️ 未执行 |
| 3 Embedding | ⚠️ 未执行 |
| 4 入库 | ⚠️ 未执行 |
| 5 检索 | ⚠️ 未执行 |
| 6 拼 Prompt | ⚠️ 未执行 |
| 7 问答 | ⚠️ 未执行 |
| 8 引用与兜底 | ⚠️ 未执行 |
