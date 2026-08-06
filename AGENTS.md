# 项目协作说明

本仓库用于维护 Codex 配置、恢复脚本和自定义 skills。

## 范围

保持此文件聚焦于仓库级规则和 skill 路由。不要重复 `skills/*/SKILL.md` 中已经包含的详细流程。

## Skill 仓库跟踪

安装新的 skill 仓库后，将其仓库地址记录到 `scripts/reinstall-skills.sh` 中的 `repos` 数组里。如果该仓库已经列出，则不要重复添加。

## Hermes 配置同步

`hermes/<device>/` 下按设备管理各台机器的 Hermes Agent 配置文件，直接用 git 版本控制。当前已落地设备：`zcm6`。

### 同步工作流

```bash
# 本机 → 仓库（安全方向，默认）
bash scripts/sync-hermes-device.sh pull zcm6

# 预览（不实际复制）
bash scripts/sync-hermes-device.sh pull zcm6 --dry

# 仓库 → 本机（恢复/迁移，需确认）
bash scripts/sync-hermes-device.sh push zcm6

# 比较差异
bash scripts/sync-hermes-device.sh status zcm6
```

### Skills 分类

- **自建 skill**（真实目录，非 symlink）：直接同步到 `hermes/<device>/skills/`
- **bundled skill 被修改**（如 `ocr-and-documents`）：直接同步，作为 fork 分支管理
- **git 安装的 skill**（symlink → `~/.agents/skills/`）：仅记录到 `.skill-lock.json` 索引，不复制内容

### 安全规则

- 不收录 `.env`、`auth.json`、`*.db`、`*.lock`、`*.bak`、`sessions/`、`state.db`、`cache/`、`logs/`
- `config.yaml` 中密钥通过 `key_env` 引用环境变量，无明文密钥
- 同步前确认无敏感信息泄露

### 新增设备

1. 在 `hermes/` 下创建 `<device>/` 目录
2. 运行 `bash scripts/sync-hermes-device.sh pull <device>`
3. 提交并 push

## 其他说明

在未显式说明更新时，不要按照上述工作流运行。例如 “生成 commit” 意味着无须执行 `git pull` 或 `git push`，只需生成 commit message 并运行 `git commit` 即可。