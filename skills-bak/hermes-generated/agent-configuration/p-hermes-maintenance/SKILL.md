---
name: p-hermes-maintenance
description: "排查 Hermes 配置、skill 来源和跨设备同步问题。"
---

# Hermes Maintenance

## 核心流程

1. 先运行 `hermes config path`，以实际配置目录为准，不猜测 `HERMES_HOME`。
2. 区分配置值来自文件、环境变量、默认值还是 CLI 覆盖；区分 skill 来自 npm 链接、Hub、内置包或 agent 自生成目录。
3. 优先使用 `hermes config get/set`；CLI 不支持时，只定点修改唯一键，并先保存该文件副本。
4. 用户通用 skill 放用户级；任务或项目专用 skill 放项目级。自生成 skill 的唯一维护源是本仓库 `skills/hermes-generated`。
5. 修改后同时核对配置文件、`hermes config get`、`hermes skills list`，必要时用新会话验证。

## 易踩点

- 文件中的值可能被环境变量或运行参数覆盖。
- 不用宽泛 `sed` 替换重复键；不在配置、skill 或同步包中保存密钥。
- 同步成功只说明文件到位，不证明运行时已加载。
- npm skill 链接和 Hermes 原生 skill 是两套来源，不要混为一谈。
