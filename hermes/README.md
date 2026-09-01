# Hermes 配置同步

本目录按设备管理各台机器上 Hermes Agent 的配置文件，直接用 git 版本控制，而非复制快照。

## 核心理念

每个设备的 hermes 配置直接作为 `hermes/<device>/` 下的文件管理。本机直接在该目录里编辑配置 → git push 同步。其他设备 git pull 即可收到更新。是否合并、如何合并，可后续由大语言模型判断。

## 目录结构

```
hermes/
├── README.md          # 本文件（约束与说明，所有设备共用）
└── <device>/          # 每个设备一个子目录（如 zcm6, pc, macbook）
    ├── config.yaml    # ~/.hermes/config.yaml 的副本
    ├── SOUL.md        # 系统提示词
    ├── memories/      # MEMORY.md + USER.md（跨会话记忆）
    ├── cron/          # jobs.json（定时任务定义）
    ├── skills/        # Skills（见下分类）
    │   ├── <自建skill>/       # 真实目录直接同步
    │   ├── <bundled-modified>/ # 被修改的原生 skill
    │   └── .skill-lock.json   # git 安装 skill 的来源索引
    └── .last_pull     # 最近同步时间戳
```

## Skills 分类与管理策略

| 类型 | 同步方式 | 后续管理 |
|------|---------|---------|
| 自建 skill（真实目录，非 symlink） | 直接同步整个目录 | 留在设备目录中 |
| bundled skill 被修改（如 ocr-and-documents） | 直接同步整个目录 | 作为上游 fork 分支管理 |
| git 安装的 skill（symlink → ~/.agents/skills/） | 仅记录 .skill-lock.json 索引 | 通过 reinstall-skills.sh 从上游安装 |

### Skill 沉淀规则

在执行任务中产生的自建 skill，先同步到 `hermes/<device>/skills/`，后续应：

1. 改名为 `p-` 前缀（本项目自建 skill 命名规范）
2. 移动到仓库根目录的 `skills/` 目录（即 codex-config/skills/）
3. 此后通过 `scripts/reinstall-skills.sh` 作为 git 仓库索引管理

### git 安装 skill 的修改

通过 git 仓库安装的 skill（vercel-labs, nature-*, p-*, academic-research-suite 等）或原生 bundled skill，
被修改后也应直接同步到当前设备目录。我们本质上是上游仓库的一个 fork/分支，修改在此仓库中维护。

## 同步脚本

脚本位于仓库根目录 `scripts/sync-hermes-device.sh`：

```bash
# 本机 → 仓库（安全方向，默认）
bash scripts/sync-hermes-device.sh pull zcm6

# 预览（不实际复制）
bash scripts/sync-hermes-device.sh pull zcm6 --dry

# 仓库 → 本机（恢复/迁移，需确认）
bash scripts/sync-hermes-device.sh push zcm6

# 比较差异
bash scripts/sync-hermes-device.sh status zcm6

# 列出已管理设备
bash scripts/sync-hermes-device.sh list-devices
```

## 安全约束

- **不收录**：`.env`、`auth.json`、`*.db`、`*.lock`、`*.bak`、`sessions/`、`state.db`、`cache/`、`logs/`、`audio_cache/`、`image_cache/`
- `config.yaml` 中的 API 密钥通过 `key_env` 引用环境变量，不包含明文密钥
- 每次同步前脚本自动跳过敏感文件
- `.gitignore` 中已配置 `hermes/**` 下的敏感文件排除规则

## 跨设备合并工作流

1. 在仓库中修改配置内容（直接编辑或 LLM 辅助判断合并）
2. 提交并 push 到远程
3. 在目标设备执行 `git pull` 然后 `bash scripts/sync-hermes-device.sh push <device>`

## 新增设备

1. 在 `hermes/` 下创建 `<device>/` 目录
2. 运行 `bash scripts/sync-hermes-device.sh pull <device>`
3. 提交并 push

## 设备命名

设备名应具有可识别性，建议使用：
- 主机名简称（如 zcm6）
- 或 hermes sync device label（如 ln2-e061a7）
- 或自定义易记名称（如 pc, macbook, server）
