# 004 - 个性化 AI 学习助手

## Project Goal
做一个"记得你学到哪、知道你什么水平、给个性化路线"的学习助手。你说要学什么，它基于你的水平和历史问答，给路线、出练习、记进度。

## Difficulty
intermediate（中级）

## Prerequisites
- 会 Python 基础
- 了解 RAG 与向量检索概念
- 看过 case 001 / 002 更佳

## Tech Stack
- Python 3.10+
- RAG（知识库 + 向量检索）
- Memory（用户画像 + 历史问答）
- LLM API
- ⚠️ 版本需自验，本案例未实际跑通

## User Scenario
用户说"我想学 Python"，助手：
- 评估当前水平
- 基于知识库给学习路线
- 出个性化练习
- 记住进度，下次接着学

## MVP
- 用户画像（水平 / 目标）
- 知识库检索（路线 / 概念）
- 记忆（已学 / 已问）
- 个性化输出

## Architecture
见 [architecture.md](./architecture.md)。
一句话：学习助手 = 一个"带着你的学习档案 + 历史问答 + 知识库"去问 LLM 的程序。

## Workflow
1. 收用户输入 + 读画像 + 读记忆
2. 检索知识库
3. 拼个性化 prompt
4. LLM 出答
5. 更新记忆

## Prompts
- 画像：[prompts/learning-profile.md](../../../prompts/learning-profile.md)
- 答疑：[prompts/learning-answer.md](../../../prompts/learning-answer.md)

## Skills
- [skills/ai/rag.md](../../../skills/ai/rag.md)
- [skills/ai/memory.md](../../../skills/ai/memory.md)

## Testing
- 两次同主题问答看是否记得上文
- 不同水平用户看输出是否差异化
- 问知识库外问题看是否诚实说不覆盖

## Verification
⚠️ Verification Pending。详见 [verification.md](./verification.md)。

## Known Limitations
- 个性化准确度未实测
- 记忆会膨胀需裁剪
- 检索可能不准
- 隐私数据不入库

## Lessons Learned
见 [lessons.md](./lessons.md)。
