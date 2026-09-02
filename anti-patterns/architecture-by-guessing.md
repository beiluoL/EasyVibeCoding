# Architecture by Guessing（靠猜搭架构）

> 反模式：没设计、没选型、没看复用点就开写，让 AI 靠猜定架构——重复造轮子、模块混乱、难维护。

## Bad Approach

一句话需求到手，直接让 AI "开始写"，不画模块图、不定技术栈、不查项目里已有什么能复用。常见表现：

- 不先设计，让 AI 边写边定结构
- 不选型，AI 用啥就用啥（这次 React，下次 Vue）
- 不看项目已有的工具/组件，AI 又造一遍
- 模块边界靠 AI 临场发挥，越写越糊

## Why It Looks Reasonable

- "需求简单，不需要画架构图"——感觉过度设计。
- 以为 AI 会自己选合理的模块结构和复用点。
- 小项目时靠猜确实能跑通，让人误以为规模大了也行。

## Why It Fails

- **重复造轮子**：项目已有 `request()` 封装、已有 `Pagination` 组件，AI 不知道又写一个，违反原则 03 Reuse before reinvent。
- **模块混乱**：没有预先定的边界，A 模块直接改 B 的数据，耦合越缠越紧。
- **难维护**：结构是临时凑的，加新功能时要迁就旧结构，越加越乱。
- **技术栈漂移**：没定选型，AI 每次按自己偏好来，项目里冒出多种风格、多套依赖。

靠 AI 猜出来的架构，短期看着能跑，长期全是债。

## Better Approach

动手前先用 architecture-design 定好骨架：

1. **画模块图**：定清楚有哪些模块、各自职责、谁调用谁。
2. **定技术栈**：框架、数据层、状态管理、样式方案，一次定死，全项目遵循。
3. **标复用点**：列出现有的工具函数、组件、配置，新功能先从这里找。
4. **定边界**：模块之间只通过明确接口通信，不互相伸手。

## Example

需求：给笔记应用加"标签管理"。

❌ 靠猜：

```
给笔记应用加标签功能，开始写吧。
```

AI 自己定了：标签存到 note 对象里、自己写一个 `TagInput` 组件、自己发请求——结果项目已有 `TagPicker` 组件和 `tags` 表没用上，标签数据散落在 note 里，后面要做"按标签搜"得重写。

✅ 先设计：

```
先用 architecture-design 定方案：
- 现有组件：TagPicker（在 components/）
- 现有数据层：tags 表 + tagService
- 模块边界：标签走 tagService，note 不直接碰 tag 表
- 复用点：TagPicker 直接用，别造新的
方案定了再实现。
```

模块边界清晰，复用点明确，加"按标签搜"时顺着 tagService 加一个查询就行。

## Prevention

- 动手前先列模块清单：有哪些模块、各自职责、谁调用谁。
- 检查 AI 产出是否复用已有工具/组件，而不是又造一个。
- 技术栈和目录约定写进 `AGENTS.md`，AI 每次遵循，不会漂移。

## Related Skill

- [architecture-design](../skills/core/architecture-design/SKILL.md) —— 先定模块图与复用点
- [brainstorming](../skills/core/brainstorming/SKILL.md) —— 选型前先发散方案
- [design-architecture](../prompts/architecture/design-architecture.md) —— 让 AI 按既有结构设计
- 原则 03 Reuse before reinvent：项目根 `README.md`
