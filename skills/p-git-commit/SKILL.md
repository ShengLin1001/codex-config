---
name: p-git-commit
description: Generate concise Chinese commit messages that follow Conventional Commits v1.0.0, the @commitlint/config-conventional type enum, and official gitmoji shortcode meanings. Use when the user asks to write, format, polish, choose, or create a git commit message.
---

# P Git Commit

## Overview

Generate concise, Chinese, easy-to-scan Git commit messages. By default, output only the suggested commit message. Run `git add` or `git commit` only when the user explicitly asks to commit.

This skill follows three layers of conventions:

- Conventional Commits v1.0.0: format, `feat`, `fix`, and `BREAKING CHANGE` semantics.
- `@commitlint/config-conventional`: common type enum.
- Official gitmoji list: shortcode meanings.

## Workflow

1. Inspect the changes first:

```bash
git status --short
git diff --stat
git diff
```

2. Choose a type. Prefer the 11 types from `@commitlint/config-conventional`:

- `feat`: a new feature. Corresponds to MINOR in Conventional Commits.
- `fix`: a bug fix. Corresponds to PATCH in Conventional Commits.
- `build`: build system or external dependency changes, such as make, npm, pip, or docker.
- `chore`: miscellaneous changes that do not modify src or test files.
- `ci`: CI configuration or script changes.
- `docs`: documentation-only changes.
- `perf`: performance improvements.
- `refactor`: code changes that neither fix a bug nor add a feature.
- `revert`: revert a previous commit.
- `style`: formatting, whitespace, punctuation, or style changes that do not affect code meaning.
- `test`: add missing tests or correct existing tests.

3. Add a scope only when there is a clear module, such as `DFT`, `Lammps`, `N2P2`, `plot`, or `workflow`. Omit the scope when there is no clear module.

4. For breaking changes, mark them with either of these forms:

- Add `!` after the type or scope: `feat(api)!: :boom: 修改配置格式`
- Add a footer: `BREAKING CHANGE: <description>`

5. Choose a gitmoji shortcode that expresses the intent of the change. Do not mechanically map only by type when another shortcode is more accurate.

## Output Format

Use this header format:

```text
<type>(<scope>): <emoji-code> <Chinese title>
```

Without a scope:

```text
<type>: <emoji-code> <Chinese title>
```

For breaking changes:

```text
<type>(<scope>)!: <emoji-code> <Chinese title>
```

If a short body is needed, add one Chinese sentence after a blank line. Do not write long paragraphs:

```text
feat(DFT): :sparkles: 添加收敛状态检查

支持批量扫描子任务结果，并在提交前给出简洁统计。
```

## Type To Emoji Defaults

These are the default preferred choices. If the concrete change is better represented by another gitmoji, choose by the specific intent.

- `feat`: `:sparkles:`
- `fix`: `:bug:`
- `build`: `:package:`, `:heavy_plus_sign:`, `:heavy_minus_sign:`, `:arrow_up:`, `:arrow_down:`
- `chore`: `:wrench:`, `:hammer:`
- `ci`: `:construction_worker:`, `:green_heart:`
- `docs`: `:memo:`
- `perf`: `:zap:`
- `refactor`: `:recycle:`
- `revert`: `:rewind:`
- `style`: `:art:`
- `test`: `:white_check_mark:`, `:test_tube:`

## Gitmoji Reference

The official gitmoji shortcode meanings are listed below. Use shortcodes in commit messages, not Unicode emoji.

- `:art:`: improve code structure or format.
- `:zap:`: improve performance.
- `:fire:`: remove code or files.
- `:bug:`: fix a bug.
- `:ambulance:`: critical hotfix.
- `:sparkles:`: introduce a new feature.
- `:memo:`: add or update documentation.
- `:rocket:`: deployment-related changes.
- `:lipstick:`: add or update UI and style files.
- `:tada:`: initialize a project.
- `:white_check_mark:`: add, update, or pass tests.
- `:lock:`: fix security or privacy issues.
- `:closed_lock_with_key:`: add or update secrets.
- `:bookmark:`: release or version tags.
- `:rotating_light:`: fix compiler or linter warnings.
- `:construction:`: work in progress.
- `:green_heart:`: fix CI builds.
- `:arrow_down:`: downgrade dependencies.
- `:arrow_up:`: upgrade dependencies.
- `:pushpin:`: pin dependencies to specific versions.
- `:construction_worker:`: add or update CI build systems.
- `:chart_with_upwards_trend:`: add or update analytics, tracking, or metrics code.
- `:recycle:`: refactor code.
- `:heavy_plus_sign:`: add a dependency.
- `:heavy_minus_sign:`: remove a dependency.
- `:wrench:`: add or update configuration files.
- `:hammer:`: add or update development scripts.
- `:globe_with_meridians:`: internationalization or localization.
- `:pencil2:`: fix typos or text mistakes.
- `:poop:`: write code that needs later improvement.
- `:rewind:`: revert changes.
- `:twisted_rightwards_arrows:`: merge branches.
- `:package:`: add or update compiled files or packages.
- `:alien:`: update code due to external API changes.
- `:truck:`: move or rename resources, such as files, paths, or routes.
- `:page_facing_up:`: add or update a license.
- `:boom:`: introduce breaking changes.
- `:bento:`: add or update assets.
- `:wheelchair:`: improve accessibility.
- `:bulb:`: add or update source comments.
- `:beers:`: write unserious or temporary code.
- `:speech_balloon:`: add or update text and literals.
- `:card_file_box:`: database-related changes.
- `:loud_sound:`: add or update logs.
- `:mute:`: remove logs.
- `:busts_in_silhouette:`: add or update contributors.
- `:children_crossing:`: improve user experience or usability.
- `:building_construction:`: architectural changes.
- `:iphone:`: responsive design changes.
- `:clown_face:`: mock-related changes.
- `:egg:`: add or update an easter egg.
- `:see_no_evil:`: add or update `.gitignore`.
- `:camera_flash:`: add or update snapshots.
- `:alembic:`: experimental changes.
- `:mag:`: improve SEO.
- `:label:`: add or update types.
- `:seedling:`: add or update seed files.
- `:triangular_flag_on_post:`: add, update, or remove feature flags.
- `:goal_net:`: catch errors.
- `:dizzy:`: add or update animations and transitions.
- `:wastebasket:`: deprecate code that should be cleaned up later.
- `:passport_control:`: authorization, role, or permission code.
- `:adhesive_bandage:`: simple fixes for non-critical issues.
- `:monocle_face:`: data exploration or inspection.
- `:coffin:`: remove dead code.
- `:test_tube:`: add a failing test.
- `:necktie:`: add or update business logic.
- `:stethoscope:`: add or update health checks.
- `:bricks:`: infrastructure-related changes.
- `:technologist:`: improve developer experience.
- `:money_with_wings:`: sponsorship or funding infrastructure.
- `:thread:`: multithreading or concurrency-related code.
- `:safety_vest:`: validation-related code.
- `:airplane:`: improve offline support.
- `:t-rex:`: add backward-compatible code.

## Style

- Keep the title around 30 Chinese characters.
- Start the title with a verb and do not end it with a full stop.
- Keep the header under 100 characters.
- Use at most one sentence in the body; for small changes, output only the header.
- Use Chinese as the main language, while preserving necessary English module names, function names, and file names.
- Do not exaggerate the change.
- Do not force multiple unrelated purposes into one commit.
- If the changes are mixed, first suggest splitting them into separate commits. If the user requires a single commit, choose the primary purpose.

## Commit

When the user explicitly asks to commit, show the message that will be used first, then stage only the relevant files.

Use this form for multi-line messages:

```bash
git commit -m "<type>(<scope>): <emoji-code> <Chinese title>" -m "<short Chinese description>"
```
