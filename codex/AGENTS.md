# Codex 全局约束

## 文件删除安全

禁止批量删除文件或目录。

不要使用：

- `del /s`
- `rd /s`
- `rmdir /s`
- `Remove-Item -Recurse`
- `rm -rf`

需要删除文件时，只能一次删除一个明确路径的文件。

正确示例：

```powershell
Remove-Item "C:\path\to\file.txt"
```

如果需要批量删除文件，应停止操作，并向用户请求，让用户手动删除。

## 平台环境

当前平台是 CentOS 超算平台。调用命令时如果命令不存在或版本不符合要求，先检查是否可以通过 `module avail` 调用合适的软件。

## Python 环境

后续 Codex 相关 Python 操作默认使用隔离虚拟环境：

- Python: `/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python`
- pip: `/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python -m pip`

不要把 Codex 相关包安装到主要使用的 `/public3/home/scg6928/mysoft/env/pyenv/dft` 虚拟环境中。

## Git Commit

生成 Git commit 信息时，默认使用 `$p-git-commit` skill 的规范。
