---
name: p-vasp-job-monitor
description: "监控 Slurm 上的 VASP 作业进度、错误和收敛状态。"
---

# VASP Job Monitor

## 核心流程

1. 用 `squeue` 定位作业，再用 `scontrol show job <id>` 获取真实 `WorkDir`。
2. 从 `OSZICAR` 的 `F=` 行判断离子步进度；用 `tail -30 OUTCAR` 查看最新电子收敛、计时和结束状态。
3. 用精确错误模式检查 stderr、stdout 和 OUTCAR，避免宽泛关键词误报。
4. 同时确认正常退出标志与目标精度；只有两者都满足才报告完成并收敛。
5. 多阶段工作流还要确认提交脚本实际包含并执行 `-phase_check` 等阶段检查参数。

## 易踩点

- 不对巨大 OUTCAR 做无界全文 `grep`；先看尾部和明确模式。
- `kinetic energy error` 等正常文本不能被模糊的 `error` 搜索误判。
- 调度器显示 `COMPLETED` 不等于 VASP 达到物理或数值收敛。
- wrapper 或下一阶段启动成功不证明前一阶段产物有效。
