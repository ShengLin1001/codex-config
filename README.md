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

## 常用工作流

### 从当前 Codex 环境同步

在修改 `~/.codex/AGENTS.md` 或 `~/.codex/config.toml` 后，从仓库根目录运行：

~~~bash
bash scripts/copy-codex-files.sh
~~~

这会更新 `codex/AGENTS.md` 和 `codex/config.toml`。

### 恢复到 Codex 环境

从仓库根目录运行：

~~~bash
bash scripts/restore-codex-files.sh
~~~

这会将仓库中的 Codex 配置副本恢复到 `~/.codex`。

### 重新安装外部 Skills

从仓库根目录运行：

~~~bash
bash scripts/reinstall-skills.sh
~~~

该脚本会读取 `scripts/reinstall-skills.sh` 中的 `repos` 数组，并通过 `npx skills add` 安装这些 skill 仓库。

安装新的 skill 仓库后，将其仓库地址添加到 `scripts/reinstall-skills.sh` 中的 `repos` 数组里。如果该仓库已经列出，则不要重复添加。

## 环境规则

与 Codex 相关的 Python 应在 ~/.codex/AGENTS.md 中声明。

不要将 Codex 相关的 Python 包安装到其他虚拟环境中。

如果缺少某个必要命令，或其版本不合适，应先检查是否可以通过 `module avail` 找到合适的软件。

## Git 工作流

更新本仓库时，按以下顺序执行：

1. 运行 `git pull`，同步远程分支。
2. 使用 `$p-git-commit` 生成中文 commit message。
3. 运行 `git push`，将改动推送到 GitHub。

## 其他说明

在未显式说明更新时，不要按照上述工作流运行。例如 “生成commit并git commit” 意味着无须执行 `git pull` 或 `git push`，只需生成 commit message 并运行 `git commit` 即可。