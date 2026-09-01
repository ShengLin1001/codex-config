# codex-config

本仓库用于维护个人 Codex 配置、全局说明、恢复脚本和自定义 skills。它的目的是让同一套 Codex 设置可以方便地在当前 CentOS HPC 主机或新的环境中恢复。

## 仓库内容

- `AGENTS.md`：本仓库的协作和更新规则。
- `codex/config.toml`：`~/.codex/config.toml` 的仓库副本。
- `codex/AGENTS.md`：`~/.codex/AGENTS.md` 的仓库副本，用于保存 Codex 全局说明。
- `skills/`：本仓库维护的自定义 Codex skills。
- `skills-using/root/`：跨项目通用、适合用户级安装的 skill 源码；保存在这里不等于已经安装。
  **用户级 skill 只从这里安装**，不从其他仓库装。其中 `p-literature-download` 由
  git subtree 从上游 `ShengLin1001/p-literature-download` 同步，维护方式见 `AGENTS.md`。
- `skills-using/project/*/explicit/`：只通过 `$skill-name` 显式调用的项目级 skills。
- `skills-using/project/*/implicit/`：可按任务语义自动匹配的项目级 skills。
- `scripts/copy-codex-files.sh`：将 `~/.codex` 中的 `AGENTS.md` 和 `config.toml` 复制到本仓库的 `codex/` 目录。
- `scripts/restore-codex-files.sh`：从本仓库将 Codex 配置恢复到 `~/.codex`。
- `scripts/pei_ai_univ_reinstall`：从本仓库的 `skills-using/` 安装 skills。`-root` 装 `skills-using/root/`，`-project <域>...` 装 `skills-using/project/<域>/`，`-global` 装成用户级（不给则装进当前项目），`-clean` 先清空，`-list` 只列不装。
- `scripts/sync-hermes-generated-skills.sh`：将明确指定的 Hermes 自生成 skill 归档到仓库，不提供反向安装。

## 常用工作流

### Skill 调用策略

安装层级由 `skills-using/root/` 与 `skills-using/project/` 区分；是否允许自动匹配由各 skill 的 `agents/openai.yaml` 决定。显式 skill 只有用户明确点名时才加载，例如：

~~~text
$p-article-evaluated 检查这篇论文，只诊断不改写
$p-article-polishing 润色这段英文论文
$p-code-review 审查当前代码变更，只报告问题
~~~

每个显式 skill 的 `agents/openai.yaml` 都必须设置：

~~~yaml
policy:
  allow_implicit_invocation: false
~~~

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

### 重新安装用户级 Skills

用户级 skill 的唯一来源是本仓库的 `skills-using/`。从仓库根目录运行：

~~~bash
./scripts/pei_ai_univ_reinstall -global -root                            # skills-using/root/ 全部
./scripts/pei_ai_univ_reinstall -global -root -project academic python   # 再带上两个项目域
./scripts/pei_ai_univ_reinstall -global -clean -root                     # 先移除已装的再装
./scripts/pei_ai_univ_reinstall -root -list                              # 只列出会装什么
~~~

`-project` 后跟一个或多个域名，对应 `skills-using/project/<域>/`。skill 名是按目录里的
`SKILL.md` 现找的，新增 skill 不用改脚本。`skills/`、`skills-generating/`、
`skills-bak/` 是归档目录，脚本不会碰。

### 只装进某一个项目

不给 `-global` 就是项目级安装，落点是**当前工作目录**（`./.claude/skills` 等），
只对这个项目生效，不污染别的项目：

~~~bash
cd <项目根>
/path/to/codex-config/scripts/pei_ai_univ_reinstall -root -project python
~~~

`-project` 选的是「装哪些」，`-global` 选的是「装到哪」，两个维度互不相干。

默认目标是 Codex、Claude Code、OpenClaw 和 Hermes Agent；用 `AGENTS` 缩小范围：

~~~bash
AGENTS="hermes-agent" ./scripts/pei_ai_univ_reinstall -global -root
AGENTS="codex claude-code" ./scripts/pei_ai_univ_reinstall -global -root -project academic
~~~

该脚本不修改 Claude plugins、Codex plugins 或 Hermes 原生 skills。Codex 本地的 Ponytail 属于 Codex plugin，与 npm 用户级 skill 清理相互独立。

### 同步 Hermes 生成的自定义 Skills

Hermes 原生的 `skill_manage` 会把新 skill 写入 Hermes 自己的 skills 根目录；实际位置以 `hermes config path` 为准。这些技能不是 `npx skills` 的锁文件内容，自定义内容应版本化到本仓库。

`skills/hermes-generated/` 只作为本地与 zcm6 历史自生成 skills 的归档。skill 按主题分目录，名称统一为 `p-*`；只保留触发条件、核心流程、必要命令和易踩点，不保存工作日志、机器快照或一次性修复记录，也不重新安装到 Hermes。

在产生或修改一个值得保留的 Hermes skill 后，明确导出该 skill 的相对路径（路径相对 Hermes 的 `skills/` 根目录）：

~~~bash
./scripts/sync-hermes-generated-skills.sh export research/my-new-skill
git add skills/hermes-generated/research/my-new-skill
git commit -m "feat(skills): 同步 my-new-skill"
git push
~~~

关闭 Hermes 自动创建和维护 skill：

~~~bash
hermes config set skills.creation_nudge_interval 0 --force
hermes config set skills.write_approval true
hermes config set curator.enabled false
~~~

`creation_nudge_interval=0` 关闭自动 skill review 触发，`curator.enabled=false` 关闭自动整理，`write_approval=true` 阻止 Hermes 静默写入。同步脚本默认拒绝覆盖仓库已有目录；确认新归档应替换旧版本时才追加 `--force`，旧副本会移动到 `.archive/`，不会递归删除。

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

安装或刷新允许的 skill：

~~~bash
NODE_OPTIONS=--use-env-proxy npx --yes skills add ShengLin1001/codex-config -g --agent codex --skill p-code-style p-plot-figure p-git-commit --yes
~~~

更新已经由 CLI lock 跟踪的 skills：

~~~bash
NODE_OPTIONS=--use-env-proxy npx --yes skills update -g -y
NODE_OPTIONS=--use-env-proxy npx --yes skills update p-code-style -g -y
~~~

查看已安装 skills：

~~~bash
npx --yes skills list -g -a codex
~~~

移除指定 skill：

~~~bash
npx --yes skills remove p-code-style -g -y
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

