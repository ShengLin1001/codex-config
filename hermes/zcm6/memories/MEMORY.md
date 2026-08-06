Two skills overlap and may need consolidation: `vault-integration` (curator-managed, comprehensive, with references/) and `vault-source-integration` (category: vault, errors on skill_view with "Object of type date is not JSON serializable" — confirmed still broken as of 2026-08-06). The `vault-integration` skill is the richer, maintained one; `vault-source-integration` has a date-type field in frontmatter that breaks JSON serialization. Flagged for background curator review.
§
## 工作约定（来源：memories-zcm6/codex/memories/memory_summary.md；2026-08-04 快照）
- 中文沟通；用户给出的确切路径、脚本和“参考的工作流”优先，先核验当前源/帮助/产物，不臆测。
- 要求修改源码、生成文件、配置或报告时，完成真实变更并用可复现的文件、CLI、构建、调度器或 Git 证据验证；不要仅写说明。
- Git：先用 `git rev-parse --show-toplevel` 确认仓库。多个候选或目标不明确时，只列路径和改动摘要并等待确认；暂存显式白名单，排除 scratch/生成物；提交前检查 `git diff --check` 与 `git diff --cached --check`。
- 调用 `p-git-commit` 默认执行检查、按语义暂存、验证、commit、`git pull --ff-only`、push；仅在用户明确只要 message/预览、仓库不明确、无改动或校验/同步失败时不继续写入。
- 安全敏感的认证/供应商任务：确认实际生效配置；不打印凭据，未经批准不撤销或登出现有认证。
- 宿主的持久软件环境改动放在 `~/.bash_soft_env`，不直接写入 shell 启动文件。