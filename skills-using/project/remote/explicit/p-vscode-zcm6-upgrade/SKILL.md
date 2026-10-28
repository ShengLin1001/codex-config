---
name: p-vscode-zcm6-upgrade
description: "Use ONLY when the user explicitly invokes this skill to upgrade local Windows VS Code together with the patched VS Code Server on zcm6 (CentOS 7, from MikeWang000000/vscode-server-centos7). Do NOT invoke on your own, for VS Code extension updates, or for other remote hosts. 触发：/p-vscode-zcm6-upgrade、$p-vscode-zcm6-upgrade、用这个 skill 升级 VS Code 和 zcm6 的 server。"
---

# 升级本地 VS Code + zcm6 打补丁的 VS Code Server

## 触发条件

只在用户显式调用时执行：Claude Code 输入 `/p-vscode-zcm6-upgrade`，Codex 写 `$p-vscode-zcm6-upgrade`。仅 Windows。

## 决定顺序的事实

- zcm6 是 CentOS 7（glibc 2.17），官方 server 跑不起来。`~/.vscode-server` 用开源仓库 https://github.com/MikeWang000000/vscode-server-centos7 的发布包：自带 `gnu/` sysroot，`code-<commit>` wrapper 用 patchelf 改写 node 等二进制。
- 每个包只对应一个 VS Code commit，wrapper 遇到别的 commit 报 `unknown commit_id`，Remote-SSH 会改去拉官方 server 而连不上。所以**目标版本以补丁仓库已发布的为准，先装 zcm6，再升本地**。
- 本地是 user 版安装器，装在 `D:\software\Microsoft_VS_Code`。

## 1. 定目标版本

```bash
code --version                                                   # 当前版本和 commit
ver=$(gh release view -R MikeWang000000/vscode-server-centos7 --json tagName -q .tagName)
gh release view "$ver" -R MikeWang000000/vscode-server-centos7 --json assets -q '.assets[]|.name+" "+.digest'
curl -s "https://update.code.visualstudio.com/api/versions/$ver/win32-x64-user/stable"
```

最后一条返回本地安装包的 `url`、`version`（新 commit）和 `sha256hash`。`$ver` 等于当前版本就告诉用户无需升级并停下。release 的 tag 不带 `v`（标题 `v1.143.1`，tag `1.143.1`），下载 URL 用 tag，带 `v` 会 404。

## 2. zcm6：装同版本 server

```bash
ssh zcm6 'export http_proxy=http://127.0.0.1:37897 https_proxy=http://127.0.0.1:37897
  mkdir -p ~/mysoft/pkgs/vscode-server && cd ~/mysoft/pkgs/vscode-server \
  && curl -fL -sS -o vscode-server_<ver>_x64.tar.gz \
       https://github.com/MikeWang000000/vscode-server-centos7/releases/download/<ver>/vscode-server_<ver>_x64.tar.gz \
  && sha256sum vscode-server_<ver>_x64.tar.gz \
  && tar xzf vscode-server_<ver>_x64.tar.gz -C ~/.vscode-server --strip-components 1 \
  && ~/.vscode-server/code-latest --patch-now \
  && c=$(readlink ~/.vscode-server/code-latest) && ~/.vscode-server/bin/${c#code-}/bin/code-server --version'
```

- sha256 和第 1 步 `digest` 不一致就停下，不要解压。
- 包里没有 `data/`、`extensions/`，覆盖解压不动已装插件和设置。`--patch-now` 会顺带给远端插件的原生二进制打补丁（如 Claude Code 的 `resources/native-binary/claude`）。
- 装好的标准：`--patch-now` 打印 `Success`，`code-server --version` 输出新版本号。node 补丁失败会直接报 glibc 错误。
- 以后远端插件更新后报 glibc 错误，再跑一次 `~/.vscode-server/code-latest --patch-now`。

## 3. 本地：静默升级

1. `Get-Process Code` 有输出就请用户先关 VS Code，不要替用户结束进程（可能有未保存的文件）。本会话若跑在 VS Code 集成终端里，安装会把自己关掉，改到 WezTerm 里执行。
2. 安装包下到 scratchpad，`sha256sum` 对照第 1 步的 `sha256hash`。
3. 安装（`!runcode` 防止装完自动启动，`/DIR` 固定安装位置）：

```powershell
Start-Process <path>\VSCodeUserSetup-x64-<ver>.exe -ArgumentList '/VERYSILENT','/NORESTART','/SP-','/SUPPRESSMSGBOXES','/MERGETASKS=!runcode','/DIR="D:\software\Microsoft_VS_Code"' -Wait
```

4. `code --version` 的 commit 要等于 zcm6 上 `readlink ~/.vscode-server/code-latest` 里的 commit。

## 4. 清理旧版 server

等用户连一次 zcm6 确认新版能用、并同意清理后再做。先确认旧版没在跑：`pgrep -u $USER -af "[S]table-<旧commit>"` 无输出。`[S]` 防止匹配到 ssh 的 `bash -c` 自身；同一条命令里若还写了旧目录路径（如 `d=...Stable-<旧commit>`）仍会自匹配，这时把脚本走 `ssh zcm6 'bash -s' <<'EOF'` 从 stdin 传。

- 单个文件逐个 `rm`（都在 `~/.vscode-server/` 下）：`.<旧commit>.log`、`.pid`、`.token`，`code-<旧commit>`，`code-<旧commit>-cli`，`.code-<旧commit>-cli.patchbak`，`.code-<旧commit>-cli.patched`，符号链接 `bin/<旧commit>`（不带结尾 `/`），以及 `~/mysoft/pkgs/vscode-server/` 里装过的 tarball。
- `cli/servers/Stable-<旧commit>/` 是整棵目录树，按全局删除规则交给用户手动执行：`! ssh zcm6 'rm -rf ~/.vscode-server/cli/servers/Stable-<旧commit>'`。
