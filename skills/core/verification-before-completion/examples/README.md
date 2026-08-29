# Verification Before Completion 示例 — 验收"创建笔记"3 条标准

## 输入

任务：创建笔记（POST /api/notes）。

AI 声称："已完成创建笔记功能。"

验收标准：
1. 正常请求返回 201 + 笔记数据
2. 空 title 返回 400
3. 超长 title 返回 400

不直接信"已完成"，逐条验证。

## 逐条验证

### 标准 1：正常请求返回 201 + 笔记数据

```bash
curl -X POST http://localhost:3000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"标题","content":"内容"}'
```

返回：
```json
{ "id": 1, "title": "标题", "content": "内容" }
```
HTTP 状态码 201。

测试 `test('正常创建笔记返回 201')` 通过。

→ ✅ 证据：curl 返回 201 + 笔记数据；测试通过

### 标准 2：空 title 返回 400

```bash
curl -X POST http://localhost:3000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"","content":"内容"}'
```

返回：
```json
{ "error": "title 不能为空" }
```
HTTP 状态码 400。

测试 `test('空标题返回 400')` 通过。

→ ✅ 证据：curl 返回 400；测试通过

### 标准 3：超长 title 返回 400

```bash
curl -X POST http://localhost:3000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"<10001个a>","content":"内容"}'
```

返回：
```json
{ "error": "title 过长" }
```
HTTP 状态码 400。

测试 `test('超长标题返回 400')` 通过。

→ ✅ 证据：curl 返回 400；测试通过

## 产出

```
任务：创建笔记
验收标准核对：
  1. 正常请求返回 201 + 笔记数据
     → ✅ 证据：curl 返回 201 + {id:1,...}；test('正常创建笔记返回 201') 通过
  2. 空 title 返回 400
     → ✅ 证据：curl 返回 400 + {error:"title 不能为空"}；test('空标题返回 400') 通过
  3. 超长 title 返回 400
     → ✅ 证据：curl 返回 400 + {error:"title 过长"}；test('超长标题返回 400') 通过
遗留问题：无
完成判定：完成（3/3 ✅）
```

三条标准全有可指向的客观证据（curl 结果 + 测试名），不是"我觉得做完了"。全部 ✅ → 判定完成，可以进入下一个任务。

如果标准 3 是 ❌（比如代码没加长度限制），则：

```
  3. 超长 title 返回 400
     → ❌ 原因：当前代码无长度校验，10001 字符返回 201
遗留问题：需为 title 加长度校验（>10000 返回 400）
完成判定：未完成（待修复 1 条）→ 回到 implementation 修复
```

有 ❌ 就不算完成，必须修完重新验证。
