# 项目协作说明

本仓库用于维护 Codex 配置、恢复脚本和自定义 skills。

## 范围

保持此文件聚焦于仓库级规则和 skill 路由。不要重复 `skills/*/SKILL.md` 中已经包含的详细流程。

## Skill 仓库跟踪

安装新的 skill 仓库后，将其仓库地址记录到 `scripts/pei_ai_univ_reinstall` 中的 `lnormal_repos` 数组里。如果该仓库已经列出，则不要重复添加。

## Skill 路由

`skills-using/root/` 保存跨项目通用、适合用户级安装的 skill 源码；该位置不表示已经安装。`skills-using/project/` 保存只应随特定类型项目加载的 skill。

调用方式由各 skill 的 `agents/openai.yaml` 控制。任何只允许通过 `$skill-name` 调用的显式 skill 都必须保持：

```yaml
policy:
  allow_implicit_invocation: false
```

