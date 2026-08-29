# 构建 RAG（build-rag）

## Use When（何时使用）

> 想让 AI 基于自己的文档回答问题（而不是靠模型自身记忆），需要搭一条最小可跑的 RAG（检索增强生成）链路。

## Goal（目标）

> 设计一个最小可运行的 RAG：文档切块 → 向量化 → 检索 → 拼 prompt → LLM 回答 + 引用来源，给出步骤、选型建议，并诚实标注未在生产验证。

## Input Variables（输入变量）

- `{{document_source}}`：知识来源（PDF/Markdown/网页/数据库等）。
- `{{question_type}}`：用户会问的问题类型（如：产品问答、内部规章查询）。
- `{{llm_available}}`：可用的 LLM 与向量模型（如：GLM/通义/本地嵌入模型）。

## Prompt（提示词正文）

```
Role: 你是一名要把 RAG 从概念落到最小可跑 demo 的工程师，务实、不堆术语。
Context: 知识来源：{{document_source}}
问题类型：{{question_type}}
可用模型：{{llm_available}}
Goal: 给出一条最小可运行的 RAG 链路设计：切块 → 向量化 → 检索 → 拼 prompt → LLM 回答 + 引用来源，含步骤、选型建议和已知风险。
Constraints:
- 必须给出最小可跑架构，而非泛泛而谈"用向量数据库"。
- 每个环节给出选型建议（嵌入模型、向量库、检索方式），并说明为什么这么选。
- 切块要给具体策略：按多大粒度切、是否重叠、如何处理表格/代码。
- 检索要说明：检索 top-k、是否重排、如何把片段拼进 prompt。
- 必须包含"引用来源"机制：回答里标注每段来自哪个文档哪一段。
- 这套设计未在生产验证，明确标注 ⚠️ Not Yet Verified，并列出需在生产前验证的事项（召回率、成本、延迟）。
- 不编造性能数字（如"准确率 95%"）。
Workflow:
1. 文档预处理：清洗、切块（给粒度与重叠参数）。
2. 向量化：选嵌入模型，说明维度与存储。
3. 存储：选最小够用的向量存储（本地文件/轻量库均可）。
4. 检索：给检索策略与 top-k。
5. 拼 prompt：给模板，含检索片段 + 问题 + 引用要求。
6. LLM 回答 + 标注来源。
7. 列出最小验证步骤和风险。
Output format:
## 最小架构（图示或文字流）
## 各环节选型与理由
## 切块策略
## 检索与拼 prompt 模板
## 引用来源机制
## ⚠️ 未在生产验证的事项
Verification: 回顾是否每环节都有具体选型而非空话、是否包含引用机制、是否诚实标注未验证事项且无编造数字。
```

## Expected Behavior（期望行为）

> 模型给出端到端最小可跑设计，每环节有选型与理由，含引用机制，并诚实标注未在生产验证、不编造指标。

## Expected Output（期望输出）

```
## 最小架构
文档 → 切块(500字+50重叠) → 嵌入(bge-small) → 存 SQLite+向量扩展 → 检索 top5 → 拼 prompt → LLM 回答+引用
## 选型理由
嵌入：bge-small 中文友好、可本地跑
存储：demo 用 SQLite 足够，生产再换
## 检索模板
[检索片段1](来源:doc.md#L12) + 问题 → LLM → 回答标注 [1]
## ⚠️ 未在生产验证
召回率、多文档混合成本、并发延迟均未实测
```

## Validation（验证）

- 五个环节（切块/向量化/存储/检索/拼 prompt）都有具体方案。
- 包含引用来源机制。
- 明确标注 ⚠️ Not Yet Verified 且无编造性能数字。

## Common Mistakes（常见错误）

- 只说"用向量数据库"不给具体选型与理由，落地无从下手。
- 切块不给粒度参数，导致要么太碎丢上下文要么太长召回差。
- 不做引用来源，AI 回答无法核对，出错也查不到来源。
- 编造"准确率 95%"等未测数字误导决策。

## Related Skills（相关技能）

- [`../../skills/ai/rag/SKILL.md`](../../skills/ai/rag/SKILL.md)
- [`../../skills/ai/context-engineering/SKILL.md`](../../skills/ai/context-engineering/SKILL.md)

## Related Workflows（相关流程）

- 暂无直接对应流程（可参考 `workflows/feature-development/` 的"实现-验证"环节）
