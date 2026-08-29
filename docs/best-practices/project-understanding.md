# Project Understanding 先读懂项目

## 是什么

动手前先把项目读一遍：用了什么技术、怎么分层、有哪些约定、关键模块在哪。大白话：进厨房前先看看锅碗在哪、调料放哪，别一上来就炒。

## 为什么重要

原则 01 Understand before coding 和原则 03 Reuse before reinvent 都建立在"先读懂"上。不读懂就动手，要么重造已有的轮子，要么写出和项目风格格格不入的代码，AI 尤其容易犯这个错——它默认不知道你的项目长什么样。

## 怎么做

1. **看入口和配置**：`README`、`package.json` / `pom.xml` / `go.mod`、构建脚本、启动入口
2. **摸目录结构**：哪放业务逻辑、哪放工具、哪放测试、哪放配置
3. **找分层约定**：Controller-Service-DAO？前后端怎么分？API 在哪定义
4. **抓一两个相似功能当样板**：要看懂"这个项目里实现一个功能的标准长啥样"
5. **记下关键事实**：技术栈、命名约定、目录用途，存进 Memory 或项目文档
6. **让 AI 也读一遍**：把上面这些喂给 AI（见 [context-engineering](../concepts/context-engineering.md)），别让它"裸写"

相关技能：[`skills/core/project-discovery`](../../skills/core/project-discovery)。

## 常见错误

- **跳过读项目直接让 AI 写**：AI 按通用模板写，和项目风格对不上，返工。
- **只看代码不看约定**：代码能跑但命名/分层不符合项目规范，评审被打回。
- **读完不记下来**：下次换会话又得重新读一遍，浪费 token 和时间。
- **把整个项目丢给 AI 让它"自己理解"**：超窗口且抓不住重点，应挑关键文件给。

## 示例

读懂一个 Spring Boot 项目，最少看这几样：

| 看什么 | 在哪 | 想知道什么 |
| --- | --- | --- |
| 技术栈和依赖 | `pom.xml` / `build.gradle` | 用了哪些框架、版本 |
| 启动入口 | `*Application.java` | 主类、扫描范围 |
| 配置 | `application.yml` | 端口、数据源、第三方配置 |
| 目录结构 | `src/main/java/...` | 分层方式（controller/service/mapper） |
| 一个完整功能 | 找一个 Controller + Service + Mapper | 标准写法长什么样 |
| 规范文档 | 项目根的规范文件 | 命名、分层、提交约定 |

## 相关资源

- 技能：[`skills/core/project-discovery`](../../skills/core/project-discovery)
- 上下文工程：[context-engineering](../concepts/context-engineering.md)
- 把项目事实记下来：[memory](../concepts/memory.md)
- 读完后拆任务：[task-decomposition](./task-decomposition.md)
