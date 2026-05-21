# codex-config

Personal Codex configuration and skills sync repository.

This repository keeps the Codex files that are useful to restore quickly on a
new host:

- `codex/config.toml`: Codex configuration snapshot.
- `codex/AGENTS.md`: global operating instructions.
- `skills/p-skill-installer`: locally authored Codex skill.
- `memories/`: curated Codex memory registry and rollout summaries.
- `scripts/reinstall-skills.sh`: reinstall external skills with `npx skills`.
- `scripts/restore-codex-files.sh`: copy this repository's Codex files into
  `~/.codex`.

## Restore

From the repository root:

```bash
bash scripts/restore-codex-files.sh
bash scripts/reinstall-skills.sh
```

On the CentOS HPC host, Codex-related Python tooling should use:

```bash
/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python
```

Do not install Codex-related Python packages into the `dft` environment.
