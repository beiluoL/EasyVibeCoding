# B04 — 搭建最小可用 RAG（文档问答 + 引用）

> ⚠️ Not Yet Verified — 此任务尚未在真实模型上跑过分。以下所有"Expected / Acceptance / Evaluation"都是对目标行为的**期望定义**，不代表任何模型已经实现或得分。

## Task

给定一个 **Markdown 文档集合** + 一个 **LLM API Key 占位**，实现一个**最小可运行的 RAG（检索增强生成）**系统。处理流程必须完整覆盖：
**文档切块 → 向量化 → 存入向量库 → 检索 TopK → 拼 Prompt → 生成回答并附原文引用。**

- RAG（大白话解释）：**先让 AI 从"自己的文档库"里搜出最相关的几段，再把这几段连同问题一起发给大模型，让大模型"按资料"回答，而不是靠记忆胡说八道。**
- 向量化 / Embedding（大白话解释）：**把一段文字变成一串数字（向量）**，两段文字意思越像，它们的向量距离就越近——这样"搜相关段落"就变成了数学计算。

## Difficulty

**advanced**

## Goal

- 命令行入口 `node rag.js ask "我的问题"` 能：
  1. 在本地文档里搜 Top 3 相关片段；
  2. 调用 LLM 生成回答；
  3. 回答末尾附上引用：`[1] 文件名.md # 第 X-Y 行` 格式。
- 对**文档内能回答的问题**：回答正确 + 引用能对应到原文的行号范围（误差 ≤ 3 行）。
- 对**文档范围外的问题**（文档里根本没有，例如问"2025 年某公司股价"）：**诚实拒答**（不胡编），类似输出：「我手头的资料里没找到相关内容，无法回答。」
- 所有文档内容来自 `docs/` 目录，AI 代码里**不允许硬编码任何文档内容**（防止作弊）。

## Input

### 1）项目骨架

```
easyvibe-b04/
├── package.json        ← 已声明：axios、dotenv、（可选）sqlite3 存向量、（可选）faiss-node
├── .env.example        ← 内容见下方
├── docs/               ← 5 篇 MD 文档（真实内容由验收端注入，见下"文档集合说明"）
│   ├── company.md      ← 公司简介 / 团队 / 成立时间
│   ├── pricing.md      ← 产品价格 / 套餐对比
│   ├── roadmap.md      ← 季度路线图 / 已发布功能
│   ├── security.md     ← 安全合规 / 数据区域 / 认证
│   └── changelog.md    ← 最近 5 次版本更新记录
├── rag.js              ← 空文件：要实现 `node rag.js index` 与 `node rag.js ask "xxx"`
└── data/
    └── .gitkeep        ← 向量库/索引文件输出目录
```

### 2）.env.example（原样注入）

```env
# LLM 供应商：允许 anthropic / openai / deepseek 三选一
LLM_PROVIDER=deepseek
LLM_API_KEY=sk-xxxxxxxxxxxxxxxx（占位，不要写真实 key，代码里读 process.env）
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_CHAT_MODEL=deepseek-chat
LLM_EMBED_MODEL=deepseek-embed
# 其他
TOP_K=3
CHUNK_SIZE=500        # 字符数，允许 AI 代码调整
CHUNK_OVERLAP=50
```

### 3）文档集合说明（验收端注入真实文本）

- 5 篇文档的真实内容在验收时会**动态替换**，目的是防止 AI 在代码里死记答案。
- 但每篇会保证至少 3 个独特的"事实锚点"（例如 `company.md` 有「成立时间 = 2023-04-01」「CEO = 张三」「总部 = 杭州」），这些锚点只出现一次、其他文档不重复。
- 用于诚实拒答的问题，答案不可能从这 5 篇 MD 中得到。

### 4）约束

- 必须使用「嵌入模型 API 调向量化」，**不能**用本地词袋 / TF-IDF / 纯字符串相似度替代；
- 切块算法：按字符 `CHUNK_SIZE=500` + `CHUNK_OVERLAP=50`，且块边界不能断在半行（尽量按 `\n`）；
- 向量库允许两种实现方式二选一：
  - A 方案：SQLite 存 `(chunk_id, doc, start_line, end_line, vector_blob)` + 自己算欧氏距离 TopK；
  - B 方案：`faiss-node` 建 IndexFlatL2 + 另外一个 JSON 存 `chunk_id -> metadata`；
- 禁止使用 LangChain / LlamaIndex 等框架（目的是考 AI 自己把 5 步拼起来）。

## Expected Behavior

1. **索引阶段**：`node rag.js index`
   - 扫描 `docs/` 下 5 篇 MD；
   - 按 `CHUNK_SIZE` / `CHUNK_OVERLAP` 切块；
   - 为每块计算 embedding + 写入向量库 `data/`；
   - 每块 metadata 包含：`doc`（相对路径）、`start_line`、`end_line`（1-based，闭区间）、`text`（块原文）。
   - 输出 `Indexed N chunks from 5 docs.`

2. **问答阶段**：`node rag.js ask "EasyVibeCoding 成立于什么时候？"`（举例，实际问题从文档锚点取）
   - 对问题做 embedding；
   - 检索 TopK=3 块；
   - 拼 Prompt 模板：
     ```
     你是一个基于文档的问答助手。只能根据【参考文档】回答问题；
     如果参考文档里没有答案，就说"我手头的资料里没找到相关内容，无法回答"。
     回答末尾用 [1][2][3] 形式标注引用。

     【参考文档】
     [1] company.md # 第1-40行：xxx（块原文）
     [2] pricing.md # 第20-60行：yyy
     ...
     【问题】EasyVibeCoding 成立于什么时候？
     ```
   - 调用 LLM 并把回答输出到 stdout；
   - stdout 的最后几行必须形如：
     ```
     引用来源：
     [1] docs/company.md # 第 2-6 行
     [2] ...（如果引用了多个）
     ```

3. **正确回答**：
   - 对文档内问题：内容准确（匹配锚点值）+ 引用的 `start_line`/`end_line` 范围**确实包含**该锚点（允许 ±3 行的切块误差）。

4. **诚实拒答**：
   - 对文档外问题：输出中必须出现「没找到相关内容，无法回答」或等价拒答字样；
   - 拒答不得编造任何事实。

## Acceptance Criteria

| # | 验收项 | 对应维度 |
|:---:|:---|:---|
| AC-1 | `node rag.js index` 能跑完，stdout 出现 `Indexed N chunks from 5 docs.`，且 N ≥ 10（单篇文档切块数量合理） | Correctness |
| AC-2 | `data/` 下出现向量库文件（存在 `.db` 或 `.faiss` + `*.meta.json` 任一），且块数 ≥ N | Correctness |
| AC-3 | 文档内问题 Q1（锚点 A ∈ company.md）：LLM 回答包含锚点 A 的字面文本，且引用中出现 `docs/company.md` + 正确行号区间（误差 ≤ 3 行） | Correctness |
| AC-4 | 文档内问题 Q2（锚点 B ∈ pricing.md）：同上规则 | Correctness |
| AC-5 | 文档内问题 Q3（锚点 C ∈ roadmap.md）：同上规则 | Correctness |
| AC-6 | 文档外问题 Q4（完全不在 5 篇里）：输出中出现拒答关键字（见 Expected 4），且没有出现任何编造的数字/名字/日期 | Correctness（诚实性） |
| AC-7 | 引用校验：对 Q1 的引用 `[x] docs/company.md # 第 L-R 行`，打开对应 MD 取 `L-3 ~ R+3` 行，锚点 A 确实在其中 | Correctness（引用保真） |
| AC-8 | 代码扫描：`grep -n "锚点A的字面文本" rag.js` 结果为 0（未把文档锚点硬编码进代码） | Security / Correctness（防作弊） |
| AC-9 | 删除 `data/` 后重新 `index` + 问 Q1 仍能得到正确答案（可重复） | Correctness / Maintainability |
| AC-10 | 向量检索链路真实存在：对 `rag.js ask` 执行用 mokeypatch 记录 embedding + 向量距离计算次数：embedding API 调用 = 1（对问题） + N chunks（index 时），均非 0 | Correctness（真 RAG 非假 RAG） |

## Evaluation

满分 100 分：

| AC | 小分 | 归属维度 |
|:---:|:---:|:---|
| AC-1 / AC-2 | 20 | Correctness（索引） |
| AC-3 | 15 | Correctness（Q1 答+引用） |
| AC-4 | 15 | Correctness（Q2） |
| AC-5 | 10 | Correctness（Q3） |
| AC-6 | 15 | Correctness（拒答诚实性） |
| AC-7 | 10 | Correctness（引用保真） |
| AC-8 | 5  | Security / Anti-cheat |
| AC-9 | 5  | Maintainability |
| AC-10 | 5  | Correctness（真 RAG） |

## Scoring Tie-in

| scoring 维度 | 本任务怎么评 |
|:---|:---|
| Correctness        | AC-1~7 / 9~10（占主要）：索引 + 3 条命中 + 1 条拒答 + 引用保真 + 真 RAG 链路 |
| Test Pass Rate     | 验收脚本 10 个 AC 的通过率；若 AI 自写"索引冒烟/拒答冒烟"测试也纳入 |
| Code Quality       | 5 步链路是否拆分函数；CHUNK/TOPK 等参数是否从 env 取；日志是否可诊断 |
| Security           | AC-8（没把答案硬编码进代码）+ API Key 是否只走 process.env、不打印到日志 |
| Maintainability    | Prompt 模板是否独立文件/常量；向量库实现是否可替换；错误重试机制 |
| Token Usage        | 完成 10 次 ask（3×命中+1×拒答×多轮）的总 Token |
| Latency            | `ask` 命令单问题平均墙钟时间 |
| Human Intervention | 纠偏次数（本任务较复杂，默认 3 次纠偏为 0 分线） |
