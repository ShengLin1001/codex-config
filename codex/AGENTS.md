# Codex Global Constraints

## File Deletion Safety

Do not delete files or directories in bulk.

Do not use:

- `del /s`
- `rd /s`
- `rmdir /s`
- `Remove-Item -Recurse`
- `rm -rf`

When deleting files, delete only one explicit file path at a time.

Correct example:

```powershell
Remove-Item "C:\path\to\file.txt"
```

If bulk file deletion is needed, stop and ask the user to delete the files manually.

## Platform Environment

The current platform is a CentOS HPC environment. When a required command is missing or its version is unsuitable, first check whether suitable software is available through `module avail`.

## Python Environment

For future Codex-related Python operations, use this isolated virtual environment by default:

- Python: `/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python`
- pip: `/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python -m pip`

Do not install Codex-related packages into the main `/public3/home/scg6928/mysoft/env/pyenv/dft` virtual environment.

## Git Commit

When generating Git commit messages, use the `$p-git-commit` skill by default.
