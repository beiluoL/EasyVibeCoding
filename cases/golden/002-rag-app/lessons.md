# Lessons — RAG 问答应用

> ⚠️ 以下为基于 [`../../../skills/ai/rag/SKILL.md`](../../../skills/ai/rag/SKILL.md) 常见坑总结的预判性教训，尚未经本案例实际运行验证。

## 易错点 → Anti-Pattern 对应

| # | 易错点 | 后果 | 对应 Anti-Pattern |
| --- | --- | --- | --- |
| 1 | 切块太大 | 召回粒度粗、命中不准 | [`../../../anti-patterns/chunk-too-large.md`](../../../anti-patterns/chunk-too-large.md) |
| 2 | 切块太小 | 上下文断裂、语义不完整 | [`../../../anti-patterns/chunk-too-small.md`](../../../anti-patterns/chunk-too-small.md) |
| 3 | 检索不准还不调 | 答非所问、引用错位 | [`../../../anti-patterns/ignore-retrieval-quality.md`](../../../anti-patterns/ignore-retrieval-quality.md) |
| 4 | 不约束"仅基于上下文" | 幻觉：答出文档没有的内容 | [`../../../anti-patterns/rag-hallucination.md`](../../../anti-patterns/rag-hallucination.md) |
| 5 | 检索片段塞太多超窗口 | 上下文溢出或信号被稀释 | [`../../../anti-patterns/context-overflow.md`](../../../anti-patterns/context-overflow.md) |
| 6 | 不引用来源 | 无法核验、幻觉无法发现 | [`../../../anti-patterns/no-citation.md`](../../../anti-patterns/no-citation.md) |

## 教训详解

### 1. 切块大小

**现象**：一块 2000 字，检索命中后整块塞进去，答得又长又跑题。

**根因**：块太大，一个向量要代表太多内容，召回粒度粗。

**正确做法**：默认 300-500 字/块，加 50 字重叠防断句。用问题集回归调参。见 [`../../../skills/ai/rag/SKILL.md`](../../../skills/ai/rag/SKILL.md) "常见错误"。

### 2. 检索不准

**现象**：Top-K 里混入无关片段，模型被带偏。

**正确做法**：打印各片段相似度分数；调 K 值；必要时加 Rerank 重排（本案例 V0.1 暂不做）。

### 3. 幻觉

**现象**：模型答出文档里根本没有的内容，还说得头头是道。

**根因**：Prompt 未约束"仅基于上下文"。

**正确做法**：Prompt 显式写"仅根据以下上下文回答；若上下文无依据，回答'文档未覆盖'"。

### 4. 上下文超限

**现象**：检索片段总长超过 LLM 窗口，请求报错或被截断丢信息。

**正确做法**：控 Top-K 与单块长度，总长留余量；参考 [`../../../skills/ai/context-engineering/SKILL.md`](../../../skills/ai/context-engineering/SKILL.md)。

### 5. 不引用来源

**现象**：回答正确但没出处，用户无法核验。

**正确做法**：Prompt 要求每条回答附"出处：文件名+片段号"；前端展示时回链原文片段。

## 可复用的知识

- "切块大小要回归调"是 RAG 通用心法
- "约束仅基于上下文"是防幻觉的通用规则
- "引用来源"让答案从黑盒变成可核验
- RAG 把"生成"建立在"检索"之上，回答才有据可依
