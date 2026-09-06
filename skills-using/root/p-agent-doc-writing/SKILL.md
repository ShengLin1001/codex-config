---
name: p-agent-doc-writing
description: "ALWAYS invoke BEFORE substantively writing or restructuring an agent instruction file — SKILL.md, AGENTS.md, CLAUDE.md, .claude/rules/*.md. Do NOT rewrite such a file without loading this skill first. Do NOT invoke for ordinary Markdown docs, reports, or README edits. 触发：写或改 skill、调 description、调整 agent 指令分层、写 AGENTS.md/CLAUDE.md 规则。"
---

# Agent 指令编写

## 核心原则

- 只保留会改变 agent 决策的规则、流程、边界和陷阱。
- 一个含义只写一次；能从代码、配置或 `--help` 直接查到的信息不重复缓存。
- 区分始终进入上下文的路由文字与按需读取的正文，前者尤其要短。
- 使用正向、明确、可验证的要求；绝对规则只用于真实风险或固定约定。

## 编写流程

1. 先读取目标文件、上层指令和相邻文档，找出重复、冲突与实际适用范围。
2. 为每条内容判断层级：所有任务都需要的放上层；特定任务才需要的放 skill；少数分支才需要的放 `references/`。
3. `description` 是唯一的路由入口，按下面这套写（实测祈使句 vs 描述句差距很大）：
   - **只用 `description` 一个字段**。Codex 官方 skill-creator 明确只允许 `name` + `description`
     （"Do not include any other fields"）；`when_to_use` 只有 Claude Code 认，拆开就不可移植。
   - 骨架用英文祈使句 + 否定约束：必须先加载的写 `ALWAYS invoke BEFORE <动作>. Do NOT <动作>
     without loading this skill first.`；容易误触发的写 `Use ONLY when …. Do NOT invoke for <反例>.`
   - **触发词用中文**，因为 PJ 是用中文提需求的，匹配的是他实际会说的话。
   - 显式覆盖"改已有代码 / 小修一处"——实测漏调用几乎全在这一类，只写 writing 会漏掉 editing。
   - 不罗列同义词或完整流程；正文才写流程。
4. 正文保留关键步骤、完成条件和易错点；删除工作日志、一次性修复、背景科普和泛化建议。
5. 只有在内容确实需要按分支加载时才拆分引用文件；不要创建占位目录或附加 README。
6. 检查名称、路径、交叉引用和调用策略。仅显式调用的 skill 必须在 `agents/openai.yaml` 设置 `allow_implicit_invocation: false`。

完成时确认：路由准确、正文自包含、没有重复规则，且删去任一句都不会损失关键决策信息。
