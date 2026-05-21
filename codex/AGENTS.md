禁止批量删除文件或目录。
不要使用:
- `del /s`|
- `rd /s`
- `rmdir /s`
- `Remove-Item -Recurse`
- `rm -rf`
需要删除文件时，只能一次删除一个明确路径的文件。
正确示例:
Remove-Item "C:\path\to\file.txt"
如果需要批量删除文件，应停止操作，并向用户请求，让用户手动删除。
当前平台是centos超算平台, 请你需要调用命令但不存在或者版本不符合时，先检查是否可以通过module avail调用合适的软件
后续 Codex 相关 Python 操作默认使用隔离虚拟环境:
- Python: `/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python`
- pip: `/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python -m pip`
不要把 Codex 相关包安装到主要使用的 `/public3/home/scg6928/mysoft/env/pyenv/dft` 虚拟环境中。
