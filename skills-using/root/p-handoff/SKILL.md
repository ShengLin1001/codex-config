---
name: p-handoff
description: "Use ONLY when the user explicitly asks to hand off, pack up, or carry the current session over to another agent or a later session. Do NOT invoke on your own for an ordinary summary of what was done. 触发：交接、handoff、给下一个 agent 写说明、把当前上下文打包。"
---

# 会话交接

根据用户指定的后续目标生成一份自包含、可继续执行的交接文档。

## 触发条件

只在用户显式点名时执行，例如 `$p-handoff`、"给下一个 agent 写交接"。
普通的"总结一下刚才做了什么"不走本流程。

## 必备内容

- 当前目标、明确边界和已经确认的选择。
- 已完成工作及其验证证据；把事实、推断和未验证状态分开。
- 涉及的文件、关键位置、命令和当前 Git 状态。
- 尚未完成的事项、阻塞条件、风险和最小下一步。
- 下一会话建议显式调用的 skills。

优先引用已有的提交、diff、报告或规范，不复制其完整内容。删除无助于继续工作的对话过程，并遮蔽密钥、令牌、个人信息和敏感路径。

用户指定路径时写入该路径；否则写入操作系统临时目录，不污染当前仓库。完成后报告文件位置。
