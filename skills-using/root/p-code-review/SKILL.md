---
name: p-code-review
description: "Use ONLY when the user explicitly asks to run this review on code changes — a diff, working tree, branch, or PR — for correctness, repo conventions, and requirement consistency. Reports problems only, never edits. Do NOT invoke on your own while writing code, for a syntax check, or just because a diff or PR exists. 触发：用 p-code-review 审这个改动、$p-code-review 看下 diff/PR。"
---

# 代码审查

## 触发条件

只在用户显式调用时执行：Claude Code 输入 `/p-code-review`，Codex 写 `$p-code-review`。
用户没点名时（哪怕贴了 diff、说"看看这段代码"），不要自动启动。

## 确定范围

- 用户指定基点时，先验证该引用，再比较其 merge-base 到 `HEAD` 的变更。
- 审查当前工作区时，同时查看未暂存和已暂存 diff，并保留用户已有改动。
- 读取适用的 `AGENTS.md`、贡献规范、测试配置以及用户提供的需求或规格。

## 审查维度

1. **正确性**：错误结果、边界条件、回归、异常路径、资源泄漏、安全或数据丢失风险。
2. **需求一致性**：遗漏、部分实现、超出范围的行为，以及与用户选择冲突的改动。
3. **仓库规范**：只检查工具无法自动判定的约定；仓库明确规则优先于通用偏好。
4. **验证质量**：测试是否覆盖真实失败模式，是否可能在实现错误时仍然通过。

## 输出

先列 findings，按严重程度排序。每项包含文件与行号、可触发场景、影响、证据和最小修正方向；没有可靠证据的问题不写。若没有发现，明确说明，并列出尚未验证的范围或残余风险。

审查本身保持只读。只有用户另行要求时才修改代码；只有用户明确要求委派时才使用子 agent。
