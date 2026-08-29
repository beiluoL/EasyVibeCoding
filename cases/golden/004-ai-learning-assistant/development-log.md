# 开发日志 - 学习助手

⚠️ 本日志为开发步骤说明，未实际执行。

## Step 1 用户画像
定义画像结构（水平 / 目标 / 偏好），写提取 prompt。
链：[prompts/learning-profile.md](../../../prompts/learning-profile.md)

## Step 2 知识库建
把学习路线 / 概念切块向量化存库。
链：[skills/ai/rag.md](../../../skills/ai/rag.md)

## Step 3 检索
按用户问题 + 画像检索相关块。
链：[skills/ai/rag.md](../../../skills/ai/rag.md)

## Step 4 记忆读写
存已学 / 已问，读取上次内容。
链：[skills/ai/memory.md](../../../skills/ai/memory.md)

## Step 5 个性化 prompt
把画像 + 记忆 + 检索结果拼进 prompt。
链：[prompts/learning-answer.md](../../../prompts/learning-answer.md)

## Step 6 答疑
LLM 回答，引用知识库内容。
链：[skills/ai/rag.md](../../../skills/ai/rag.md)

## Step 7 练习生成
按当前阶段生成匹配练习。
链：[prompts/learning-answer.md](../../../prompts/learning-answer.md)

## Step 8 进度更新
更新记忆中的已学标记。
链：[skills/ai/memory.md](../../../skills/ai/memory.md)

⚠️ 未实际执行验证。
