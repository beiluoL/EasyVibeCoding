# 验证 - AI Agent

⚠️ Verification Pending。本案例未实际执行以下步骤。

## Expected Verification Steps
1. 给一个需 2 步 + 调工具的任务（如"查北京明天天气并算温差"），看是否正确串起来
2. 给一个工具做不了的任务（如"预测股票"），看是否承认而非乱编
3. 触发需 confirm 的工具，看是否要先人批
4. 故意制造死循环（让 Planner 反复同一步），看是否被上限拦住
5. 计时单任务是否 < 30s

## 未验证项
- 工具 SDK 版本兼容性
- 真实 LLM 调用成功率
- 权限确认 UI

❌ 不得标注 Verified / ✅ Tested / 已部署。
