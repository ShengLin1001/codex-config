---
name: p-mathtype-docx
description: "在 Word 中将文本或 LaTeX 公式转换为 MathType 公式。"
---

# MathType DOCX

## 核心流程

1. 保留原始 DOCX，先在副本中用 Word COM 打开并定位目标公式。
2. 将公式归一化为 MathType 可接受的短 token，再调用 `MTCommand_TeXToggle` 转换。
3. 每次转换后确认公式对象存在；批量结束后检查对象类型包含 `Equation.DSMT4`。
4. 保存、关闭文档和 Word 进程，重新打开文件抽查公式、分页和可编辑性。

## 易踩点

- 长 `aligned`、嵌套环境和复杂颜色语法可能卡住或转换失败，先拆成小公式。
- Word/MathType 的模态对话框会阻塞自动化，设置超时并保留未处理 token。
- 不只检查页面看起来像公式；必须验证嵌入对象类型。
- 无论成功失败都要确定性关闭 COM 对象，避免残留 `WINWORD.EXE`。
