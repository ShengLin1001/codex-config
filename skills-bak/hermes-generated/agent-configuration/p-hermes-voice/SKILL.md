---
name: p-hermes-voice
description: "排查 Hermes 语音输入、朗读及 TTS/STT 问题。"
---

# Hermes Voice

## 核心流程

1. 用 `hermes config path` 和 `hermes config get` 确认 `voice.auto_tts`、`tts.provider`、`stt.enabled` 等实际值。
2. 分别测试文本生成、TTS 和 STT，先确定失败发生在哪一层。
3. 本地 provider 检查可执行文件、模型文件和 `ffmpeg`；托管 provider 检查凭据、额度和网络。
4. 用最短音频做烟雾测试，确认输出可播放、输入可转写；配置改动后新开会话复测。

## 易踩点

- “托管语音不可用”不等于本地 TTS/STT 故障。
- 自动朗读是总开关，provider 正常也可能因它关闭而无声。
- 不把 voice 名称、模型路径或设备编号写死到通用 skill。
- 不在日志中打印 API key 或完整鉴权头。
