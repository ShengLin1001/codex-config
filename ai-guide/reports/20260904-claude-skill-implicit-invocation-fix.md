# p-code-style 隐式调用问题：根因、实测与修复方案

承接 [20260901-codex-p-code-style-invocation-audit.md](20260901-codex-p-code-style-invocation-audit.md)。
那份报告确认了漏调用的存在，并指出源码/安装副本存在漂移，因而无法把问题归因于 description 精简。
本文补上三件那份报告没有的东西：**漂移的确切机制**、**可复现的量化对比**、**已落地的修复**。

---

## 1. 结论

1. **漂移的机制是安装源**：`scripts/pei_ai_univ_reinstall` 从 **GitHub** 装
   （`npx skills add ShengLin1001/codex-config`）。改了仓库不 commit + push，
   重装拿回来的仍是旧版。这不是"忘了重装"。
2. **隐式调用没有保证，且 description 的语气是主导变量**。实测三臂对比：
   长描述句 43%、短描述句 17%、**英文祈使句 + 中文触发词 100%（7/7）**。
   变量不是长度，是语气。
3. **漏调用集中在"改已有代码"**。旧 description 下新建脚本 4/4 命中、改已有脚本 0/2 全漏；
   祈使句版把 `including a one-line fix / 改已有脚本、小修一处` 写进 description 后两个都命中。
   这正是审计报告里"后续 `sbatch_retry` 修改漏调用"的模式。
4. **要"必定加载"只能靠 hook**。description 是概率性路由，Anthropic 官方文档明确
   deterministic guardrail 只有 hooks 和 permissions 两条路。
5. **两层分工不同**：description 层**机制盲**（不管之后用 Write 还是 heredoc 还是 `python -c`），
   hook 层**机制绑定**（只拦看得见的写法）。所以 description 优先，hook 兜底。

---

## 2. 测量方法

新增 `tests/skill-trigger/`，口径与审计报告一致：

- 对每条固定提示词起一个 `claude -p` **全新会话**，回读该会话 transcript。
- 只认真实的 `Skill(skill=…)` tool_use，**不 grep skill 名**——启动清单本身就含所有
  skill 名，grep 必然假阳性。
- 按"首次真实 Skill 调用" vs "首次代码写入"的先后判 **提前 / 过晚 / 未调用**。
- 7 个 case 覆盖审计里的漏调用类别：新建 Python / 新建 Bash / Slurm 提交 /
  argparse CLI / 用 Python 生成 bash / 改已有脚本 / 小修一处。
- 提示词刻意不含 "skill"、"风格" 等词，否则测的是显式调用而非隐式路由。

```bash
codexpy run_skill_trigger_test.py -tag <标签>                    # 测已安装的用户级副本
codexpy run_skill_trigger_test.py -tag <标签> -skill_src <仓库目录>  # 测仓库源文件，绕开漂移
codexpy run_skill_trigger_test.py -check_parse <jsonl>           # 自检：只跑事件提取
```

### 项目级隔离的两个坑（实测）

`-skill_src` 把仓库源码装成该 case 的**项目级** skill，从而不必先重装。实现时踩到：

| 现象 | 实测结论 |
|---|---|
| 同名项目级 skill 放进 `.claude/skills/` | **不生效**，用户级那份赢（放了 MARKER description，清单里根本不出现） |
| `skillOverrides: {"p-code-style": "off"}` | **按名字关，两份一起关掉**，清单里一个都不剩 |

可行配方：项目副本改名 `p-xxx` → `pj-xxx`（自动改写 frontmatter 的 `name`），
同时 `off` 掉用户级那份。harness 已内建。

---

## 3. 实测数据

### 3.1 三臂 A/B（同一 harness、同一项目级模式，只有 description 不同）

| case | arm_old<br>长描述句 187 字 | arm_short<br>短描述句 26 字 | arm_new<br>祈使 + 中文触发词 357 字 |
|---|:---:|:---:|:---:|
| new_python | ❌ | ❌ | ✅ |
| new_bash | ❌ | ❌ | ✅ |
| new_slurm | ✅ | ✅ | ✅ |
| new_argparse | ✅ | ➖ 没写代码 | ✅ |
| new_genbash | ✅ | ❌ | ✅ |
| edit_existing | ❌ | ❌ | ✅ |
| small_fix | ❌ | ❌ | ✅ |
| **提前调用率** | **3/7 = 43%** | **1/6 = 17%** | **7/7 = 100%** |

另有一次独立 baseline：**已安装的用户级长 description 版 4/7 = 57%**。

Fisher 精确检验（双尾）：

| 对比 | p |
|---|---:|
| arm_new vs arm_old | 0.070（n 太小，单独比不显著） |
| arm_new vs (arm_old + arm_short 合并) | **0.0047** |
| 同一长 description 两次跑（4/7 vs 3/7） | 1.0（43%↔57% 的波动是噪声） |

**可以说的**：祈使句版显著优于两个描述句版（p<0.005）。
**不能说的**：7/7 只是"7 个样本没漏"，不等于 100% 置信；要坐实需 `-repeat 5`。

### 3.2 两个次级观察

- **命中即第一动作**：所有命中的 case 都是 `skill@1`，没有一例"过晚"。
  行为是二元的——要么开场就调，要么整轮不调。因此 hook 只需接住"整轮不调"这一类。
- **与审计报告的关系**：报告说"已观察到的漏调用不可能由短 description 造成
  （它从没装上）"——仍然成立。本文补充的是"短 description 一旦装上会更糟"（43% → 17%）。
  两句同时为真。

### 3.3 社区实测数据（交叉参考）

| 手段 | 实测 | 出处 |
|---|---:|---|
| 无干预 baseline | 55% → 50%（两轮） | Spence，22 prompts × 5 配置 |
| passive description（官方文档风格） | 77% 干净 / **37% 有 hook 时** | Seleznov，650 trials |
| **directive description**（"ALWAYS invoke… Do NOT X directly"） | **100%**（bare），OR 20.6，p<0.0001 | 同上 |
| CLAUDE.md 加一条简单指令 | 59% → 50% | Spence |
| 关键词型 hook（skill-rules.json / type-prompt） | 55% → **41%** | Spence |
| forced-eval hook | 100% → 100% / 另一实验 84% | Spence / Seleznov |
| LLM-eval hook | 100%，但无关 query 上 80% 假阳性 | Spence |
| PreToolUse deny | 确定性，非概率 | Anthropic 官方博客 |

两条反直觉但要记住的：**CLAUDE.md 加指令 ≈ 无效**；**关键词型 hook 可能比不做还差**。
另外 passive + hook 掉到 37% 说明**两层会互相干扰，不是单调叠加**。

---

## 4. 已验证的平台事实

| 事实 | 影响 |
|---|---|
| `when_to_use` 只有 Claude Code 认；OpenAI 官方 skill-creator 明确只允许 `name` + `description`（"Do not include any other fields"） | 全部信息塞进 `description` 一个字段，三家通用。Claude Code 反正也是把 `when_to_use` 拼在 description 后面进清单 |
| `description` + `when_to_use` 合计在清单里截断于 1536 字符 | 15 个 description 全部 ≤385 字符，留足余量 |
| skill 清单预算为上下文 1% ，超了按"最少用的先丢 description" | 用 `/doctor` 查；skill 多时是隐性风险 |
| `allow_implicit_invocation`（openai.yaml）只管 Codex | Claude Code 侧 15 个**全是隐式的**，因为没有 SKILL.md 设 `disable-model-invocation` |
| `skillOverrides` 支持 `"off"` / `"user-invocable-only"`，可在 Project / Local / User 任一层 | 用它翻译上面那个不一致，不必往 SKILL.md 加第三个字段 |
| `npx skills add` **接受本地路径** | `-local` 的基础，治漂移根因 |
| `paths` frontmatter 是**限制器**（"limit when this skill is activated"） | 不用它：会让"还没碰文件"的请求不再触发，是收紧不是加固 |

---

## 5. 修复方案（三层）

### 层① description 规范化（已落地，15 个全部）

两套模板，按调用意图选：

| 模板 | 用于 | 骨架 |
|---|---|---|
| gate（必须先加载） | p-code-style / p-plot-figure / p-git-commit / p-agent-doc-writing / p-page-creator | `ALWAYS invoke BEFORE <动作>. Do NOT <动作> without loading this skill first.` |
| scoped（匹配才触发，防误触） | 其余 10 个 | `Use when …` 或 `Use ONLY when the user explicitly asks …`；配 `Do NOT invoke for <反例>.` |

四条硬要求：

1. **只用 `description` 一个字段**（可移植性，见 §4）。
2. **骨架用英文祈使句 + 否定约束**（实测差距见 §3）。
3. **触发词用中文**——PJ 用中文提需求，清单要匹配他实际会说的话。
4. **显式覆盖"改已有代码 / 小修一处"**——漏调用几乎全在这一类，只写 writing 会漏 editing。

这四条已写进 `p-agent-doc-writing` 的编写流程第 3 条，否则下次它会把约定改回去。

校验：15 个 SKILL.md frontmatter 只含 `name` + `description`、YAML 可解析、均 ≤1536 字符。

### 层② PreToolUse 确定性门（已落地）

对**所有 skill 通用**，规则表驱动。`claude/hooks/gate.json`：

```json
"gates": {
  "p-code-style":        ["**/*.py", "**/*.sh", "**/*.bash", "**/*.ps1", "**/*.slurm", "**/*.sbatch"],
  "p-plot-figure":       ["**/*plot*.py", "**/*fig*.py", "**/plot/**/*.py"],
  "p-agent-doc-writing": ["**/SKILL.md", "**/AGENTS.md", "**/CLAUDE.md", "**/.claude/rules/*.md"]
},
"command_gates": {
  "p-git-commit":        ["*git commit*"]
}
```

两张表分工：`gates` 判**写入目标路径**，`command_gates` 判 **shell 命令整条**——
`git commit` 这类动作不写文件，路径表看不见它。

`require_skill.py` 的三个关键取舍：

- **判"已加载"认 transcript 里真实的 `Skill` tool_use**，不 grep skill 名（同 §2 口径）。
- **每个 skill 每会话最多拦一次**（two-try，marker 按 `session_id + skill` 存）。模型不配合时
  死循环比漏调用更糟：拦一次给足信息，之后无条件放行。marker 必须带 skill 名——按会话存一个的话，
  写 `.py` 拦掉的那次会把后面 `git commit` 的额度也吃光。
- **匹配写入目标路径，不匹配 prompt 关键词**。关键词型 hook 实测 55% → 41%；
  写入目标是确定事实，不是猜意图。

覆盖的写入方式：`Write` / `Edit` / `NotebookEdit`，以及 `Bash` 里的重定向 / `tee` / `sed -i`；
命令侧覆盖 `Bash` / `PowerShell` 里的 `git commit`（含 `git add -A && git commit -m …` 这种串联）。

**关于每次 edit 是否都要重调 skill**——不会，三个数分开看：

| | 次数 |
|---|---|
| hook 执行 | = 受管文件写入次数（每次几十毫秒，纯本地读文件） |
| **skill 加载** | **≤ 1 次/会话**（加载后 skill 正文整会话都在，再调是浪费） |
| **拦截** | **≤ 1 次/会话/skill**（marker 生效） |

稳态：写第一个 `.py` 时拦一次 → 模型加载 → 后续写入静默通过。

### 层③ 安装合并进 `pei_ai_univ_reinstall`（已落地）

```bash
./scripts/pei_ai_univ_reinstall -global -root -local -hook
```

| 开关 | 作用 |
|---|---|
| `-local` | 从本地工作树 `skills-using/` 装，不用先 commit/push（治 §1.1 的根因） |
| `-hook` | 拷 `claude/hooks/*` 到配置目录，并**合并**进 `settings.json` |

`-hook` 写入两处，都从仓库数据**推导**，不另维护清单：

1. `hooks.PreToolUse` 注册 → 指向刚拷过去的 `require_skill.py`。
   解释器用 `sys.executable` 固化：安装是每台机器各跑一次，把当机可用的解释器写死
   最稳，不依赖 PATH 上有没有 `python3`（zcm6 上可能要先 `module load`）。
2. `skillOverrides: <skill>=user-invocable-only` → 凡 `agents/openai.yaml` 里
   `allow_implicit_invocation: false` 的，翻译成 Claude Code 侧等价设置。
   单一来源仍是 openai.yaml。

已实测性质：**幂等**（第二次跑报"已是目标状态"）、**不碰其他配置**
（`model` / `env` / 已有 `skillOverrides` 全部保留）、**可反注册**
（`-uninstall` 回到原状且不删任何文件）、只给 `-hook` 时完全跳过 `npx skills add`。

---

## 6. 哪些 skill 需要 hook

条件是三个**同时**满足：隐式意图 + 有硬前置 + **前置动作能被工具事件看到**。

Codex 侧现状（`agents/openai.yaml`）：

- **隐式（8）**：p-code-style、p-plot-figure、p-agent-doc-writing、p-git-commit、
  p-diagnosing-bugs、p-tdd、p-pdf2zotero、p-page-creator
- **显式（7）**：p-code-review、p-grill-me、p-handoff、p-literature-download、
  p-research、p-article-evaluated、p-article-polishing

8 个隐式里值得 gate 的：

| skill | 结论 | 理由 |
|---|---|---|
| p-code-style | ✅ 已配 | 代码后缀，判据强 |
| p-agent-doc-writing | ✅ 已配 | SKILL.md / AGENTS.md / CLAUDE.md，判据强 |
| p-plot-figure | ⚠️ 已配但弱 | 只能靠文件名 glob，`analysis.py` 里画图拦不住 |
| p-git-commit | ✅ 已配 | `command_gates` 按命令整条匹配 `*git commit*` |
| p-page-creator | 可选 | 能 gate 在 `docs/**/*.rst`、`conf.py` |
| p-diagnosing-bugs | ✗ | 任务类型 skill，无硬前置动作 |
| p-tdd | ✗ | 已改成显式调用（`allow_implicit_invocation: false`），不需要门 |
| p-pdf2zotero | ✗ | 前置是"改 Zotero 库"，不是文件写入 |

### p-agent-doc-writing 与 p-handoff 不冲突

| | 产物 | 生命周期 | 落地位置 |
|---|---|---|---|
| p-agent-doc-writing | agent 指令文件 | 持久配置 | 仓库里的 SKILL.md / AGENTS.md / CLAUDE.md |
| p-handoff | 一次性交接文档 | 用完即弃 | 默认系统临时目录，正文明确"不污染当前仓库" |

唯一擦边是 p-handoff 必备内容里"下一会话建议显式调用的 skills"——路由建议写在临时文档里，
不是规则文件，不算冲突。真正要防的是 **p-handoff 在 Codex 显式、在 Claude Code 隐式**，
"帮我总结一下"可能误触发；已两道堵上：description 的 `Do NOT invoke for an ordinary
summary` + `-hook` 设的 `user-invocable-only`。

---

## 7. 交付物

| 文件 | 行数 | 说明 |
|---|---:|---|
| `claude/hooks/require_skill.py` | 179 | 通用 PreToolUse 门（路径 + 命令两张表）|
| `claude/hooks/gate.json` | 12 | 规则表，加 skill 只改这里 |
| `claude/hooks/test_require_skill.py` | 141 | 自检，**18/18 通过** |
| `claude/hooks/install_hook.py` | 222 | 拷文件 + 幂等合并 settings.json |
| `tests/skill-trigger/run_skill_trigger_test.py` | 417 | 触发率测量 harness |
| `tests/skill-trigger/prompts.txt` | 13 | 7 个 case |
| `scripts/pei_ai_univ_reinstall` | +50 | 新增 `-local` / `-hook` |
| `skills-using/**/SKILL.md` | 15 个 | description 规范化 |

---

## 8. 部署矩阵

| | description 层 | hook 层 |
|---|---|---|
| Claude Code 本地 | ✅ | ✅ **已实测**：探针会话拦下 → 加载 → 重写成功 |
| Claude Code zcm6 | ✅ 同一份 SKILL.md | ✅ **已实测**：`-global -root -local -hook` 装完，自检 18/18，已安装副本对 `git commit` 实拦成功。注意 `/usr/bin/python3` 是 3.6，`sys.stderr.reconfigure` 要 3.7+，必须 `PYTHON_CLAUDE=<codex venv python>` |
| Codex 本地 / zcm6 | ✅ | ❌ **未做**。schema 同族（archcore 插件即有 `PreToolUse` matcher `Write\|Edit\|apply_patch`），但工具名不同（`apply_patch` / `shell`）、payload 字段未验证、且似需走 plugin 注册 |
| Hermes | ✅ | ⚠️ 有 `pre_tool_call`，wire protocol 刻意兼容 Claude Code（exit 2 阻断、消息取 stderr），改造成本低，未做 |

**description 层四家通吃且已验证；hook 层在 Claude Code 本地与 zcm6 都已实测站得住。**
Codex / Hermes 侧仍只有 description 层，这就是把 description 放第一优先的理由。

### zcm6 安装的三个环境坑（都不是脚本的问题，但每次都要处理）

| 坑 | 处理 |
|---|---|
| 登录节点无 DNS，`git pull` / `npx` 全断 | 走 `ssh zcm6-proxy` 的 `RemoteForward 37897`，再 `export http_proxy=http://127.0.0.1:37897` |
| `~/.local/bin/node` 直接跑报一堆 `GLIBCXX/GLIBC not found` | 先 `source ~/mysoft/tools/nvm/load-nvm.sh && nvm use 22` |
| `/usr/bin/python3` 是 3.6.8，跑不了 `sys.stderr.reconfigure` | `export PYTHON_CLAUDE=/public3/home/scg6928/mysoft/env/pyenv/codex/bin/python`（3.10.15），installer 会把它固化进 settings.json |

另：安装当天 lustre 配额 967.9G/962G 已过软限且 grace 用尽，超过 ~3MB 的写入直接失败，
第一次 `git pull` 因此报 `Disk quota exceeded`。**已由 PJ 扩容解决**（现 1.037T 软限 / 1.086T 硬限，
20MB 写入正常）。记在这里是为了留下判据：`lfs quota` 的 used 后面带 `*` 且 grace 为 `none`，
就是这个故障，报错信息本身（`fatal: write error`）不会告诉你是配额。

---

## 9. 已知缺口与天花板

1. **hook 盖不住扒不到目标的写法**：`python -c "open('x.py','w')"`、`cp template.py dest.py`、
   PowerShell 的 `Set-Content` / `Out-File`（`>` 重定向能扒到）、编辑器写入。
   测试第 12 条钉住了这个已知行为，别当 bug 修。这类靠 description 层兜。
2. **p-plot-figure 的文件名 glob 是弱启发式**，价值明显低于 p-code-style 那条。
3. **组合效果未测**：description 与 hook 各自的数字都有了，两层合起来没测过。
   而且社区数据显示两层可能负向干扰（passive 77% → 37%）。
4. **测组合臂前必须先修 harness**：hook 拦下的 `Write` 仍会作为 `tool_use` 落进 transcript
   （`is_error=True`），排在 `Skill` 之前，现在的解析器会判成"调用过晚"——尽管那次写入
   根本没发生。需要按 `tool_use_id` 关联 `tool_result`，把被拒写入排除。
5. **7/7 是 n=1×7**，需 `-repeat 5` 复跑坐实。

### 排除的方案及理由

| 方案 | 不用的理由 |
|---|---|
| 关键词型 `skill-rules.json` + UserPromptSubmit | 实测 55% → 41%，比不做还差，且要长期养关键词表 |
| forced-eval hook | 84%（低于本地已达成的水平）、每个 prompt 收税、脚本里要再维护一份 skill 清单，形成第二张与 description 竞争的路由表 |
| 在 CLAUDE.md 加 skill 索引 | 是 description 的复写（清单启动时已在上下文）；实测 ≈ 无效；两张路由表必然漂移。CLAUDE.md 只值得写 description 表达不了的东西，如跨 skill 的组合规则 |
| `diet103/claude-code-infrastructure-showcase` | 方向对但过重：3 个 skill hook 即 1602 行 TS，Node 18+、可选 LLM API key、9 个 hook，README 明写不支持原生 Windows。值得抄的只有 two-try blocking 和 `PostToolUse` 上认 `Skill` 工具清 pending 两点 |
| skill frontmatter `paths` | 是限制器，会让"还没碰文件"的请求不再触发 |

---

## 10. 构建过程中修掉的 5 个 bug

记录在此，因为其中三个是判据本身的错误，容易再犯。

| # | bug | 后果 | 修法 |
|---|---|---|---|
| 1 | harness 的 Bash 写入判据只匹配 `>` | `grep … 2>/dev/null`（命令里恰好带 `.py` 路径）被算成代码写入，把会话误判成"过晚" | 判据落在**目标文件**上，不落在重定向符号上 |
| 2 | hook 的 stderr 未强制 utf-8 | 宿主没给 `PYTHONIOENCODING` 时，拦截消息被转义成 `\u26a0\ufe0f`（字面反斜杠序列）——而那条消息是这道门的全部价值 | `sys.stderr.reconfigure(encoding="utf-8")` |
| 3 | `fnmatch` 不认 `**`（假阴性） | `**/*.py` 编成 `.*.*/.*\.py`，硬要求路径含 `/`，`batch.py` 这种裸相对文件名一个都拦不住——而 agent 写的多是相对路径 | 见 #4 一并修 |
| 4 | `fnmatch` 不认 `**`（假阳性） | `**/*fig*.py` 变成"路径任意位置含 fig"，仓库名 `codex-con`**fig** 命中，**整个仓库的 .py 都被要求加载 p-plot-figure** | 按模式形状分流：去掉 `**/` 后不含 `/` 的是文件名模式，只比 basename；含 `/` 的才比整条路径 |
| 5 | 安装脚本只给 `-hook` 时仍跑 `npx skills add` | `--skill --yes` 空列表 | 用 `${#lskill[@]} -gt 0` 守卫整段 |
| 6 | `PreToolUse` matcher 漏了 `PowerShell` | Windows 上主 shell 就是 PowerShell，shell 那半边门（`git commit` 命令门、重定向写入）在本机等于没装 | matcher 改成 `Write\|Edit\|NotebookEdit\|Bash\|PowerShell` |
| 7 | marker 按 `session_id` 存一个 | 写 `.py` 拦掉的那一次会把同会话后面 `git commit` 的拦截额度吃光 | marker 改按 `session_id + skill` 存 |

安装当场还纠正了一条判断：**hook 装完对已开着的会话立即生效**（settings.json 会被重新读取），
本次就是被自己刚装的门拦下才发现 matcher 漏了 PowerShell。安装脚本原本打印的
"新会话生效"是错的，已改。

另记一条操作教训：`npx skills add … --dry-run` 中 **`--dry-run` 不是真实开关**，会被忽略并**实际安装**。
本次因此在仓库根产生了 `.claude/skills/p-code-style/`（2 个文件）和 `skills-lock.json`，已逐个删除；
4 个空目录待手动清理。要预演请用本脚本的 `-dry_run`，不要给 `npx` 加 `--dry-run`。

---

## 11. 待定事项

| # | 事项 | 说明 |
|---|---|---|
| ~~1~~ | ~~真装一次 `-global -root -local -hook`~~ | ✅ 已做：本地与 zcm6 各装一次，`settings.json` 里 `env`/`model`/`statusLine`/`enabledPlugins` 全部保留 |
| 2 | 修 harness 的被拒写入识别 → 测组合臂 | 见 §9.4 |
| 3 | `-repeat 5` 坐实 7/7 | 见 §9.5 |
| ~~4~~ | ~~p-git-commit 的 `Bash(git commit*)` gate~~ | ✅ 已做：`command_gates` 表 + 4 条测试 |
| 5 | Codex / zcm6 的 hook 落地 | 见 §8 |
| ~~6~~ | ~~p-tdd 改为显式调用~~ | ✅ 已做：p-tdd 与 p-diagnosing-bugs 的 openai.yaml 均已同步 |

---

## 参考来源

- [Steering Claude Code: when to use CLAUDE.md, skills, hooks, and subagents — Anthropic](https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more)
- [Extend Claude with skills — Claude Code Docs](https://code.claude.com/docs/en/skills)
- [Hooks reference — Claude Code Docs](https://code.claude.com/docs/en/hooks)
- [How Claude remembers your project（path-specific rules）— Claude Code Docs](https://code.claude.com/docs/en/memory)
- [OpenAI 官方 skill-creator（frontmatter 只允许 name + description）](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md)
- [How to Make Claude Code Skills Actually Activate (650 Trials) — Seleznov](https://medium.com/@ivan.seleznov1/why-claude-code-skills-dont-activate-and-how-to-fix-it-86f679409af1)
- [Measuring Claude Code Skill Activation With Sandboxed Evals — Scott Spence](https://scottspence.com/posts/measuring-claude-code-skill-activation-with-sandboxed-evals)
- [diet103/claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase)
- [BrokenDecoder/Skills forced-eval-hook.md](https://github.com/BrokenDecoder/Skills/blob/main/rust-skills-actionbook/docs/forced-eval-hook.md)
