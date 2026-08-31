---
name: p-pjvasp-docs
description: "为 pjvasp 或 mymetal 编写并验证 Sphinx 文档和示例。"
---

# PJvasp Documentation

## 核心流程

1. 先读目标函数签名、现有示例和文档目录，确认运行时实际调用而不是只看类型提示。
2. 示例优先使用小型合成数据，不依赖 VASP、Slurm 或私有计算目录。
3. 绘图脚本在导入 `pyplot` 前设置 `matplotlib` 的 `Agg` backend。
4. 运行示例并验证输出文件非空、图片可读取且无缺字警告。
5. 用 Sphinx 严格模式构建，例如 `-W --keep-going`，修正链接、引用和 API 路径。

## 易踩点

- 不为文档示例修改 `setup.py` 或引入新运行时依赖。
- 不把需要真实 VASP 文件的流程伪装成离线可运行示例。
- 文档构建成功后仍要打开关键图片或页面检查可读性。
