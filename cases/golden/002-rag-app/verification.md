# Verification — RAG 问答应用

> ⚠️ **Verification Pending**
>
> 本案例尚未实际运行。以下为 **Expected Verification Steps**（要验证该案例需做的事），**不是**已通过的证据。在真实执行并观察到通过前，绝不标记为 Verified / ✅ Tested / 已部署。

## 当前状态

- `status: experimental`
- `verified: false`
- `last_verified: null`

## Expected Verification Steps

按序执行，每步留下可复现证据（命令输出 / 截图 / 测试结果）：

### 1. 环境准备与建库

```bash
pip install -r requirements.txt   # ⚠️ 版本需自行验证兼容性
export LLM_API_KEY=...             # key 从环境变量读，不入库
python build_index.py sample.md   # 加载→切块→Embedding→入库
```

**期望**：打印块数与入库状态；Chroma 本地库生成；无报错。

> ⚠️ 未实际执行——上述命令仅为预期步骤。

### 2. 问一个文档内有答案的问题

- 用样例文档中明确写了的事实提问
- **期望**：回答正确，且引用的片段号能在原文找到对应内容

### 3. 问一个文档外的问题

- 问文档里不可能有答案的问题
- **期望**：回答明确含"文档未覆盖/未提及"，而非编造

### 4. 核对引用是否对应原文

- 取回答中的引用片段号 → 在原文定位该片段
- **期望**：引用片段内容与回答论据一致，无张冠李戴

### 5. 多轮追问

- 紧接着追问一个依赖前文的问题
- **期望**：能引用前文，不必每次重述背景

### 6. 检索质量回归（可选）

- 准备 10-20 个已知答案的问题
- 测 Recall@K（Top-K 是否含正确片段）
- 测回答忠实度（是否含未检索到的断言）
- **期望**：⚠️ 目标准确率 ≥ 80%（NFR-02），需实测后才有结论

### 7. 检查无硬编码 key

```bash
grep -rn "sk-" --include="*.py" .
grep -rni "api_key" --include="*.py" .
```

**期望**：除环境变量读取占位符外，搜不到真实 key。`.env` 不在版本控制中。

## 诚实声明

- 以上均为"要验证该案例需做的事"，**尚未执行**。
- 不存在任何运行截图、测试通过输出、部署 URL、检索延迟/准确率实测数据。
- NFR-01（延迟 <3s）与 NFR-02（准确率 ≥80%）为目标值，未实测。
- 在拿到真实证据前，本案例保持 `⚠️ Verification Pending`。
