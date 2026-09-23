# 项目协作说明

本仓库用于维护 Codex 配置、恢复脚本和自定义 skills。

## 范围

保持此文件聚焦于仓库级规则和 skill 路由。不要重复 `skills/*/SKILL.md` 中已经包含的详细流程。

## 用户级 skill 的唯一来源

用户级 skill **只从本仓库的 `skills-using/` 装**，不从任何别的仓库装。
`skills/`、`skills-generating/`、`skills-bak/` 只是归档，一律不装。

```bash
./scripts/pei_ai_univ_reinstall -global -root                            # 用户级装 skills-using/root/
./scripts/pei_ai_univ_reinstall -global -root -project academic python   # 再带上两个项目域
./scripts/pei_ai_univ_reinstall -global -clean -root                     # 先清空已装的再装
./scripts/pei_ai_univ_reinstall -root -list                              # 只看会装什么
```

`-project` 后面跟一个或多个域名，对应 `skills-using/project/<域>/`（当前有
`academic`、`python`）。skill 名按目录里的 `SKILL.md` 现找，所以新增 skill
不需要改脚本。`AGENTS=` 可缩小目标 agent 范围。

只适合 Windows 的 skill（依赖本机 Edge / PowerShell）登记在 `skills-using/windows-only.txt`，
脚本在非 Windows（如 zcm6）上自动跳过。

`-global` 决定的是**装到哪**，跟 `-project` 无关：给了就装成用户级，不给就装进
**当前工作目录**那个项目（`./.claude/skills` 等），只对那个项目生效。

新增 skill 就是在 `skills-using/root/` 或 `skills-using/project/<域>/<explicit|implicit>/`
下建目录，不要再往任何仓库地址列表里登记。

### skill 目录布局是硬约束

`npx skills add` **只对「skill 位于仓库子目录」的布局拷贝完整目录**。实测：

| 布局 | 结果 |
|---|---|
| `<repo>/<任意路径>/<skill-name>/SKILL.md` + 同级 `scripts/`、`agents/` | 整个目录都装进去 ✅ |
| `<repo>/SKILL.md`（仓库根就是 skill） | **只装 SKILL.md**，`scripts/` 全丢 ❌ |

所以任何带脚本的 skill 都必须放成 `skills-using/root/<skill-name>/`，
不能指望「把某个仓库根当 skill 直接装」。

## Skill 路由

`skills-using/root/` 保存跨项目通用、适合用户级安装的 skill 源码；该位置不表示已经安装。`skills-using/project/` 保存只应随特定类型项目加载的 skill。

调用方式由各 skill 的 `agents/openai.yaml` 控制。任何只允许通过 `$skill-name` 调用的显式 skill 都必须保持：

```yaml
policy:
  allow_implicit_invocation: false
```

## 从上游仓库同步的 skill（git subtree）

`skills-using/root/p-literature-download` 用 **git subtree** 从上游
`ShengLin1001/p-literature-download` 拉取（那个仓库的根目录就是 skill 本体）。

```bash
# 拉上游更新
git subtree pull --prefix=skills-using/root/p-literature-download \
    git@github.com:ShengLin1001/p-literature-download.git main --squash

# 把在本仓库里做的改动推回上游（少用；优先直接在上游仓库改）
git subtree push --prefix=skills-using/root/p-literature-download \
    git@github.com:ShengLin1001/p-literature-download.git main
```

用 subtree 而不是 submodule，原因只有一个：**submodule 存的是指针，不是文件**。
`npx skills add` 克隆本仓库时不带 `--recurse-submodules`，拿到的会是一个空目录，
装出来什么都没有。subtree 把文件真实落进本仓库，所以和其他 skill 走完全同一条安装路径。

代价：`git subtree pull` 前工作区必须干净，且会产生一个合并提交。
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

