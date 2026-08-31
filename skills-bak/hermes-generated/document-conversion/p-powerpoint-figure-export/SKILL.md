---
name: p-powerpoint-figure-export
description: "通过 PowerPoint COM 导出并验证幻灯片或图形。"
---

# PowerPoint Figure Export

## 核心流程

1. 在目标虚拟环境中导入 COM 依赖，只启动一个 PowerPoint 实例。
2. 使用稳定的页码或对象命名，逐页或逐对象导出到明确目录。
3. 导出后用 Pillow `Image.verify()` 检查每张图片，并核对尺寸、数量和非空内容。
4. 在 `finally` 中关闭演示文稿和 PowerPoint；失败时保留已成功导出的文件和清单。

## 易踩点

- 不为每页重复启动 PowerPoint。
- 不先清空整个输出目录；只覆盖明确目标或输出到新目录。
- Git Bash 下要转换 Windows 路径，并确认使用的是安装了 `pywin32` 的解释器。
- COM 返回成功不保证图片有效，必须重新读取验证。
