# Codex 全局约束

## 文件删除安全

不要批量删除文件或目录。

不要使用：

- `del /s`
- `rd /s`
- `rmdir /s`
- `Remove-Item -Recurse`
- `rm -rf`

删除文件时，每次只删除一个明确的文件路径。

正确示例：

~~~powershell
Remove-Item "C:\path\to\file.txt"
~~~

如果需要批量删除文件，停止操作，并要求用户手动删除这些文件。

## 平台环境

当前平台是 CentOS HPC 环境。当某个必要命令缺失，或其版本不合适时，应先检查是否可以通过 `module avail` 找到合适的软件。

## Python 环境

对于之后与 Codex 相关的 Python 操作，默认使用以下隔离虚拟环境：

- Python：`/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python`
- pip：`/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python -m pip`

不要将 Codex 相关的包安装到其他虚拟环境中。

## Git 环境

On CentOS, use the local Git and curl runtime that work on this host:

```bash
export PATH=/public3/home/scg6928/mysoft/tools/git/2.43.7/bin:$PATH
export LD_LIBRARY_PATH=/public3/soft/curl/lib:$LD_LIBRARY_PATH
```

## Git Commit

生成 Git commit message 时，默认使用 `$p-git-commit` skill。