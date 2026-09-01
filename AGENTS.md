# 项目协作说明

本仓库用于维护 Codex 配置、恢复脚本和自定义 skills。

## 范围

保持此文件聚焦于仓库级规则和 skill 路由。不要重复 `skills/*/SKILL.md` 中已经包含的详细流程。

## 用户级 skill 的唯一来源

用户级（全局）skill **只安装 `skills-using/root/` 下的这些 skill**，装法是：

```bash
npx --yes skills add ShengLin1001/codex-config -g --agent codex claude-code \
    --skill <skill-1> <skill-2> --yes
```

不要从别的仓库装用户级 skill。`scripts/pei_ai_univ_reinstall` 是历史脚本，
里面的 `lnormal_repos` 多仓库列表已不代表当前做法，不要再往里加条目。

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
`ShengLin1001/download_pdf` 拉取（那个仓库的根目录就是 skill 本体）。

```bash
# 拉上游更新
git subtree pull --prefix=skills-using/root/p-literature-download \
    git@github.com:ShengLin1001/download_pdf.git main --squash

# 把在本仓库里做的改动推回上游（少用；优先直接在上游仓库改）
git subtree push --prefix=skills-using/root/p-literature-download \
    git@github.com:ShengLin1001/download_pdf.git main
```

用 subtree 而不是 submodule，原因只有一个：**submodule 存的是指针，不是文件**。
`npx skills add` 克隆本仓库时不带 `--recurse-submodules`，拿到的会是一个空目录，
装出来什么都没有。subtree 把文件真实落进本仓库，所以和其他 skill 走完全同一条安装路径。

代价：`git subtree pull` 前工作区必须干净，且会产生一个合并提交。

