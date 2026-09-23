---
name: p-diagnosing-bugs
description: "Use ONLY when the user explicitly asks to diagnose or find the root cause of a bug that is hard to reproduce, has no identified cause yet, or is a performance regression. Do NOT invoke on your own for syntax errors, a clear one-line fix, a cause already established, or just because debugging is underway. 触发：帮我定位根因、查一下为什么会这样、这个偶发问题诊断一下、复现不了帮我查。"
---

# 复杂问题诊断

## 触发条件

只在用户显式调用时执行：Claude Code 输入 `/p-diagnosing-bugs`，Codex 写 `$p-diagnosing-bugs`。
语法错误、一行能改的明显问题、已知原因的修复，不走本流程。

## 核心流程

1. 准确定义用户观察到的症状、正常预期和影响范围。诊断请求只查因，不自动实施修复。
2. 建立能命中该症状的最小反馈循环：测试、CLI、HTTP 请求、固定输入或基准测量。它应尽量快速、确定并可由 agent 重复执行。
3. 复现后逐项删减输入、环境和调用链，直到剩余条件都不可再删。
4. 提出少量按可能性排序、可证伪的假设；每个假设写明如果成立应观察到什么。
5. 一次只验证一个变量。功能问题在关键边界加定向探针；性能问题先测基线，再用 profiler、查询计划或二分定位。
6. 获得修复授权后，先把最小复现转为回归测试，再做最小根因修复，并重跑原始场景。
7. 移除临时日志和诊断脚手架，报告根因、证据、验证结果与残余风险。

输出命令或日志前遮蔽密钥、认证头和个人信息。若无法建立可信复现，列出已尝试内容和缺少的访问或证据，停止猜测。
