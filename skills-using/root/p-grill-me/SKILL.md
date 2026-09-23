---
name: p-grill-me
description: "Use ONLY when the user explicitly asks to be questioned, challenged, or stress-tested on a plan, design, or decision before implementation. Do NOT invoke on your own for ordinary clarification during a task. 触发：追问我、拷打这个方案、压力测试这个设计、实施前先把问题问清。"
---

# 方案追问

把待定方案表示为决策树：上游选择确定后，才讨论依赖它的下游问题。

## 触发条件

只在用户显式调用时执行：Claude Code 输入 `/p-grill-me`，Codex 写 `$p-grill-me`。
任务过程中的普通澄清提问不走本流程。

## 流程

1. 从现有对话提取目标、边界、约束、验收标准和未决事项。
2. 先自行检查能从仓库、工具或权威来源获得的事实，不把可查事实变成用户问题。
3. 找出当前已具备前提的决策，同一轮集中提问；每题说明影响、互斥选项和推荐答案。
4. 根据回答更新决策树，再进入下一层。依赖尚未确定的问题留到后续轮次。
5. 当关键分支都已确定时，汇总最终选择、明确排除项和剩余风险，请用户确认。

用户确认前不开始实施。若存在必须由用户授权的外部变更，把授权本身保留为未决事项。
