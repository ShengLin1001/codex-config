# codex-config

本仓库用于维护个人 Codex 配置、全局说明、恢复脚本和自定义 skills。它的目的是让同一套 Codex 设置可以方便地在当前 CentOS HPC 主机或新的环境中恢复。

## 仓库内容

- `AGENTS.md`：本仓库的协作和更新规则。
- `codex/config.toml`：`~/.codex/config.toml` 的仓库副本。
- `codex/AGENTS.md`：`~/.codex/AGENTS.md` 的仓库副本，用于保存 Codex 全局说明。
- `skills/`：本仓库维护的自定义 Codex skills。
- `scripts/copy-codex-files.sh`：将 `~/.codex` 中的 `AGENTS.md` 和 `config.toml` 复制到本仓库的 `codex/` 目录。
- `scripts/restore-codex-files.sh`：从本仓库将 Codex 配置恢复到 `~/.codex`。
- `scripts/reinstall-skills.sh`：通过 `npx skills` 重新安装外部 skill 仓库。
- `scripts/reinstall-plugins.sh` / `scripts/reinstall-plugins.ps1`：通过 `codex plugin` 重新注册外部 plugin marketplace 并安装插件。

## 常用工作流

### 从当前 Codex 环境同步

在修改 `~/.codex/AGENTS.md` 或 `~/.codex/config.toml` 后，从仓库根目录运行：

~~~bash
./scripts/copy-codex-files.sh
~~~

这会更新 `codex/AGENTS.md` 和 `codex/config.toml`。

### 恢复到 Codex 环境 (慎重，最好手动检查差异)

从仓库根目录运行：

~~~bash
./scripts/restore-codex-files.sh
~~~

这会将仓库中的 Codex 配置副本恢复到 `~/.codex`。

### 重新安装外部 Skills

从仓库根目录运行：

~~~bash
./scripts/reinstall-skills.sh
~~~

该脚本会读取 `scripts/reinstall-skills.sh` 中的 `repos` 数组，并通过 `npx skills add` 安装这些 skill 仓库。

安装新的 skill 仓库后，将其仓库地址添加到 `scripts/reinstall-skills.sh` 中的 `repos` 数组里。如果该仓库已经列出，则不要重复添加。

### 重新安装外部 Plugins

从仓库根目录运行：

~~~bash
./scripts/reinstall-plugins.sh
~~~

在 Windows PowerShell 中运行：

~~~powershell
.\scripts\reinstall-plugins.ps1
~~~

该脚本会注册 `scripts/reinstall-plugins.sh` / `scripts/reinstall-plugins.ps1` 中的 plugin marketplaces，并安装对应插件。目前会自动注册 `DietrichGebert/ponytail` 并安装 `ponytail@ponytail`。

### 使用 npx 管理 Skills

本机通过 `npx skills` 管理全局用户级 skills，默认安装位置是 `~/.agents/skills`。Codex 可以直接从该目录发现 skills；`npx skills list -g -a codex` 中的 `Agents: not linked` 不等于 Codex 无法使用该 skill。

由于当前 Node 需要显式读取代理环境变量，运行会访问 GitHub 的命令时建议带上：

~~~bash
NODE_OPTIONS=--use-env-proxy
~~~

如果要永久生效，可在 `~/.bashrc` 的添加：

~~~bash
export NODE_OPTIONS="--use-env-proxy"
~~~

安装或刷新某个 skill 仓库：

~~~bash
NODE_OPTIONS=--use-env-proxy npx --yes skills add ShengLin1001/codex-config -g --agent codex --skill '*' --yes
NODE_OPTIONS=--use-env-proxy npx --yes skills add owner/repo -g --agent codex --skill '*' --yes
~~~

更新已经由 CLI lock 跟踪的 skills：

~~~bash
NODE_OPTIONS=--use-env-proxy npx --yes skills update -g -y
NODE_OPTIONS=--use-env-proxy npx --yes skills update p-skill-installer -g -y
~~~

查看已安装 skills：

~~~bash
npx --yes skills list -g -a codex
~~~

移除指定 skill：

~~~bash
npx --yes skills remove p-skill-installer -g -y
~~~

不要随意运行 `npx skills remove --all -g`；该命令会移除所有全局 skills。需要批量清理时先确认列表，再逐个指定 skill 名称。

## 环境规则

与 Codex 相关的 Python, git 等其他应用路径应在 ~/.codex/AGENTS.md 中声明。

不要将 Codex 相关的 Python 包安装到其他虚拟环境中。

如果缺少某个必要命令，或其版本不合适，应先检查是否可以通过 `module avail` 找到合适的软件。

## Git 工作流

更新本仓库时，按以下顺序执行：

1. 运行 `git pull`，同步远程分支。
2. 使用 `$p-git-commit` 生成中文 commit message。
3. 运行 `git push`，将改动推送到 GitHub。

