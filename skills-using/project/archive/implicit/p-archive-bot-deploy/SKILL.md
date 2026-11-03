---
name: p-archive-bot-deploy
description: ALWAYS invoke BEFORE deploying, restarting, reconfiguring or extending the cc-connect archive bot on the VPS — adding Discord/微信/飞书/Telegram, rotating a bot token, changing its model or prompt, or upgrading Claude Code / cc-connect there. Do NOT touch the bot's VPS setup without loading this skill first. Do NOT invoke for archiving a message (use p-archive-message). 触发：归档 bot、VPS bot、加微信/飞书/Telegram 平台、换 token、bot 不回消息、bot 私聊不了、升级 bot 的 claude、换 bot 模型。
---

# 归档 bot 部署与运维

现状：`ssh vultr-lax`，用户 `ccbot`，systemd 服务 `cc-connect-archive`，配置 `~ccbot/.cc-connect/config.toml`，密钥在同目录 `*.env`（600），仓库 `~ccbot/cc-conect-summary`。Discord 上显示名是「银月」（App 本名 `cc-connect-archive`），服务器「黄枫谷」，在 `#🏯藏经阁` 里不用 @ 就会回复。

## 硬约束

- **用非 root 用户跑**：root 下 Claude Code 会把 `bypassPermissions` 降级成 `auto`，bot 会卡在权限确认上。
- **安装位置照 zcm6**：放 `~/mysoft/tools/<name>/<version>/`，下载后核对 sha256，`~/.bash_soft_env` 写带注释的 PATH 行；systemd 不读这个文件，unit 里的 `Environment=PATH` 要同步改。Claude Code 在 `~/.claude/settings.json` 的 env 里设 `DISABLE_AUTOUPDATER=1`，否则它会自己更新到 `~/.local/share/claude`。
- **密钥不进 config**：config 里写 `token = "${XXX_TOKEN}"`，值放进 `EnvironmentFile`。
- **一个 bot token 只能接一个进程**：每个实例都要新建 bot，不能复用本机 cc-connect 的 token；微信 iLink 同一个账号也只能在一处登录。

## skill 同步到 VPS

仓库里提交的是 `.agents/skills/` 的实体副本，`.claude/skills/p-*` 在 .gitignore 里，因为本机 npx 建的是绝对路径链接。VPS 上的 Claude Code 只读 `.claude/skills`，所以每新增一个 skill，就在 VPS 上补一个相对链接：

```bash
ssh vultr-lax 'su - ccbot -c "cd cc-conect-summary && git pull -q && mkdir -p .claude/skills && for d in .agents/skills/*/; do n=\$(basename \$d); [ -e .claude/skills/\$n ] || ln -s ../../.agents/skills/\$n .claude/skills/\$n; done; ls .claude/skills"'
```

## 写入密钥

```bash
# Git Bash 里执行：从剪贴板读、校验格式、写入，全程不回显
t=$(cat /dev/clipboard | tr -d '\r\n \357\273\277')
f=/home/ccbot/.cc-connect/discord.env
printf 'DISCORD_BOT_TOKEN=%s\n' "$t" | ssh vultr-lax "cat > $f && chown ccbot:ccbot $f && chmod 600 $f"
printf ' ' > /dev/clipboard
```

不要用 PowerShell 管道写：它会在开头加 BOM，systemd 把这一行判成非法，然后**把整行连同 token 打进 journal**。一旦 token 在日志或对话里出现过，就立刻在平台上重置。

## 加一个平台

在 `[[projects]] name = "archive"` 下追加 `[[projects.platforms]]`，`allow_from` 只填用户本人的 ID，然后 `systemctl restart cc-connect-archive`。

| 平台 | 凭证 | 要点 |
| --- | --- | --- |
| Discord | Developer Portal 新建 App → Bot → 重置令牌 | 打开 Message Content Intent；用 `https://discord.com/oauth2/authorize?client_id=<ID>&scope=bot%20applications.commands&permissions=117824` 拉进服务器。浏览器操作上的坑见 `p-edge-browser` 的 site-notes |
| Telegram | BotFather 的 token | VPS 在海外，不需要 `proxy` |
| 飞书 | `cc-connect feishu setup --project archive`（扫码新建），或者 `bind --app-id/--app-secret` | `allow_from` 填的是**该应用下**的 open_id，换应用后 ID 会变 |
| 微信 | `cc-connect weixin setup --project archive --qr-image /tmp/wx.png`，扫码登录 | 不设 `proxy`。先停掉本机 `~/.cc-connect` 里同账号的 weixin project。海外 VPS 连 iLink 网关是否稳定**还没验证** |

## 排障

- **bot 收不到消息**：先把 `[log] level` 改成 `"debug"` 再重启，然后看日志。debug 下被丢弃的原因都会打出来：`without bot mention`（服务器频道里必须 @bot，或者开 `group_reply_all`）、`unauthorized user`（`allow_from` 填错了）。排查完改回 `"info"`。
- **只想在一个频道里免 @**：cc-connect 只能按服务器开（`group_reply_all_guilds = "<guild_id>"`），没有按频道的开关。所以 bot 能看到哪些频道要靠 Discord 权限限制：在「宗门」类别上给 bot 的身份组设「查看频道 ✕」，子频道同步继承；`#🏯藏经阁` 放在类别外面。新建频道放进类别里，bot 就看不到。核对方法：用 bot token 请求 `GET /channels/<id>/messages?limit=1`，看不到的频道返回 403 `Missing Access`。
- **Discord 私聊发不出去**：bot 和用户必须在同一个服务器里，所以先用 OAuth 链接把 bot 拉进服务器。
- **完成判据**：日志里出现 `message received`，然后出现 `turn response`；同时仓库 `git log` 里有 bot 的归档提交。
