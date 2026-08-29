# Verification — AI 聊天应用

> ⚠️ **Verification Pending**
>
> 本案例尚未实际运行。以下为 **Expected Verification Steps**（要验证该案例需做的事），**不是**已通过的证据。在真实执行并观察到通过前，绝不标记为 Verified / ✅ Tested / 已部署。

## 当前状态

- `status: experimental`
- `verified: false`
- `last_verified: null`

## Expected Verification Steps

按序执行，每步留下可复现证据（命令输出 / 截图 / 测试结果）：

### 1. 本地起服务

```bash
# Node 版
npm install
npm start
# 或 Python 版
pip install -r requirements.txt
python app.py
```

**期望**：服务在 `localhost` 起来，无报错。浏览器打开页面能看到聊天 UI。

> ⚠️ 未实际执行——上述命令仅为预期步骤，未跑过。

### 2. 发消息看回复

- 在输入框打"你好"→ 点发送
- **期望**：几秒内消息列表出现 AI 回复，用户/AI 气泡可区分

### 3. 连续追问看历史

- 紧接着问"刚才我说了什么"
- **期望**：AI 能引用前文，历史消息全部保留可见

### 4. 断网看错误提示

- 断网（关 Wi-Fi 或停掉后端）后再发消息
- **期望**：页面显示"请求失败/超时"类提示，不白屏、不卡死

### 5. 清空历史

- 点"清空历史"
- **期望**：列表清空，再发消息从空白开始

### 6. 检查无硬编码 key

```bash
# 在仓库根目录跑，确认无真实 key
grep -rn "sk-" --include="*.js" --include="*.py" --include="*.html" .
grep -rni "api_key" --include="*.js" --include="*.py" --include="*.html" .
```

**期望**：除示例占位符（如 `process.env.API_KEY`）外，搜不到任何真实 key。`.env` 不在版本控制中。

### 7.（可选）接口测试

用 [`../../../skills/core/testing/SKILL.md`](../../../skills/core/testing/SKILL.md) 给 `POST /api/chat` 写最小测试：
- 正常消息 → 返回回复
- 空消息 → 返回 400
- key 缺失 → 返回 500 且不泄露 key

## 诚实声明

- 以上均为"要验证该案例需做的事"，**尚未执行**。
- 不存在任何运行截图、测试通过输出、部署 URL。
- 在拿到真实证据前，本案例保持 `⚠️ Verification Pending`。
