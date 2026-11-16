---
name: p-android-phone
description: "ALWAYS invoke BEFORE operating PJ's Android spare phone — adb shell / input, mcp__mobile-mcp__* tools, or Mika tasks — including a one-off screenshot, app launch, or adb reconnect. Do NOT drive the phone without loading this skill first. 触发：备用机、在手机上查、手机 App 查价、拼多多/闲鱼/转转/1688/微信 App、adb 连手机、手机掉线、mobile-mcp、Mika、让 AI 操作手机。"
---

# 备用安卓机操作

## 设备与连接

- iQOO Neo5（V2055A），OriginOS 4 / Android 14，1080x2400，序列号 `341826557700BOO`，USB 调试已「始终允许」。
- adb 用 `D:/software/platform-tools/adb.exe`；PATH 上 vivo pcsuite 自带的 adb 不要用。Git Bash 里先 `export MSYS_NO_PATHCONV=1`，否则 `/sdcard` 会被改写成 Windows 路径。
- `offline`：先 `adb kill-server && adb start-server`，别用 `adb reconnect`（会让设备直接从列表消失）。
- `adb devices` 为空：电脑报 `Device Descriptor Request Failed` 是 USB 层没连上，请 PJ 检查数据线和 USB 口（换口解决过描述符失败），再查 vivo 办公套件的 vivoSyncService、vivoesService 是否在跑——它们抢 adb 接口，已改成手动启动，别打开 vivo 办公套件。`unauthorized` 请 PJ 在手机上允许并勾「始终允许」。

## 选工具

| 工具 | 用于 | 识别方式 |
|---|---|---|
| mobile-mcp（默认） | Claude 自己逐步操作、读数据、核对 | uiautomator 元素树，截图可选 |
| Mika（手机 App） | 派出去慢慢做的长任务（约 10+ 分钟一个） | 无障碍元素树为主，模型是 App 里配的 sub2api `Qwen3.8-Flash` |

不用：Open-AutoGLM（通用视觉模型输出格式对不上、复读、编造，只有智谱 `autoglm-phone` 才值得重测）；DSH Go（手机端 agent，电脑没有接口驱动它）。

mobile-mcp 注册在用户级（`~/.claude.json`，所有项目可用），工具名为 `mcp__mobile-mcp__*`。重装用：

```bash
claude mcp add-json -s user mobile-mcp '{"type":"stdio","command":"cmd","args":["/c","npx","-y","@mobilenext/mobile-mcp@1.0.17"],"env":{"ANDROID_HOME":"D:/software/android-sdk"}}'
```

## mobile-mcp 操作

- 读屏用 `mobile_list_elements_on_screen`（文字 + 坐标），元素树缺信息才截图。
- 点按取元素中心坐标，不硬编码：同一 App 不同页面布局会变。
- 搜索优先 deeplink，免输入。拼多多已验证：`adb shell am start -a android.intent.action.VIEW -d "'pinduoduo://com.xunmeng.pinduoduo/search_result.html?search_key=<URL 编码关键词>'"`。其他 App 的 deeplink 未验证，不行就点搜索框再输入。
- 输入文字：`mobile_type_keys` 在这台机上中文必失败（`setPrimaryClip ... got null`），PJ 的 vivo 输入法还会把英文转成中文候选。改用 ADB Keyboard：
  1. `adb shell ime set com.android.adbkeyboard/.AdbIME`
  2. `adb shell am broadcast -a ADB_CLEAR_TEXT`，再 `adb shell am broadcast -a ADB_INPUT_B64 --es msg <UTF-8 的 base64>`
  3. 密码框里广播不生效，改 `adb shell input text <ASCII>`；核对只比长度和是否一致，不在对话里显示内容。
  4. ADB Keyboard 键盘不可见但仍占位，会挡住下方元素：点页面标题等空白处收起。
  5. 密码框聚焦时切回 vivo 输入法会弹出系统「安全键盘」（`SecureInputMethod` 窗口）：它盖住下半屏，点下面的按钮没反应、`screencap` 也是空图。先按一次返回键收起，再点。
  6. 用完必须 `adb shell ime set com.baidu.input_vivo/.ImeVivoService` 切回，否则 PJ 手机上没键盘。

## Mika

- 手机重启后先启动助手，再连电脑：
  ```bash
  adb shell sh /sdcard/Android/data/com.wangzan101.mika/files/usb-start.sh
  adb shell sh /sdcard/Android/data/com.wangzan101.mika/files/connect-computer.sh
  adb forward tcp:8765 tcp:8765
  ```
- 派任务与等结果（脚本从手机读 token，不打印）：
  ```bash
  P=~/mysoft/env/pyenv/codex/Scripts/python; M=<本 skill 目录>/scripts/mika_mcp.py
  $P -I $M call mika_run_task '{"request_id":"<新 uuid>","goal":"..."}'
  $P -I $M call mika_wait_task '{"task_id":"<id>","timeout_s":50}'   # 上限 50s，循环调用
  $P -I $M tools                                                      # 列出全部工具
  ```
- goal 写清要的字段和「只看不买，不加购、不领券、不下单」。Mika 中途提问用 `mika_answer`，改方向用 `mika_steer_task`。

## mobile-mcp 与 Mika 互斥

mobile-mcp 启动的 `mobilecli DeviceServer` 占着 UiAutomation 时（闲置 30 分钟才退），Mika 的无障碍被挂起：任务报 `phone_unavailable`，`adb shell dumpsys accessibility` 里 `Bound services:{}`。切到 Mika 前：

```bash
adb shell ps -A -o PID,ARGS | grep mobilecli   # 进程名是 app_process，要看 ARGS；找到 PID 后 adb shell kill <PID>
adb shell settings put secure enabled_accessibility_services ""
adb shell settings put secure enabled_accessibility_services com.wangzan101.mika/.a11y.MikaAccessibilityService
```

## 边界

- 只看：不加购、不领券、不下单、不发消息、不登录新账号，这些先问 PJ。密码、验证码、付款永远交给 PJ。
- 收尾确认：输入法已切回 vivo 输入法；没留 mobilecli 进程，`dumpsys accessibility` 的 `Bound services` 里能看到 Mika 等服务。
