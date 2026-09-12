# Human Approval Matrix 人工审批矩阵

> 哪些操作 AI 可以自动做？哪些需要人确认？哪些禁止？

| 操作 | AI 可自动 | 需人工确认 | 禁止 |
| --- | ---: | ---: | ---: |
| 阅读代码 | ✅ | | |
| 修改普通代码 | ✅ | | |
| 修改测试代码 | ✅ | | |
| 运行测试 | ✅ | | |
| 生成文档 | ✅ | | |
| 安装依赖 | | ✅ | |
| 删除文件 | | ✅ | |
| 修改公共接口 | | ✅ | |
| 修改数据库结构 | | ✅ | |
| 修改认证/权限 | | ✅ | |
| 创建 API Key | | ✅ | |
| 修改生产配置 | | ✅ | |
| Production Release | | ✅ | |
| 提交 Secret/凭据 | | | ✅ |
| 删除数据库数据 | | | ✅ |
| 破坏性 git 操作（force push） | | | ✅ |

## 原则

> AI 的默认行为是保守的：不确定时停下来问人。

> 人工确认不是拖慢进度，而是防止不可逆的错误。

## 延伸阅读

- [Risk-Based Verification](./risk-based-verification.md)
- [Workflow State Machine](./workflow-state-machine.md)
- [Definition of Done](./definition-of-done.md)
