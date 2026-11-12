---
name: p-pdf-annotate
description: "Use ONLY when the user explicitly asks to annotate an academic PDF with highlights and notes. Writes a new annotated PDF next to the original: Do NOT invoke merely because a paper, PDF or summary request appears, and NEVER overwrite the original PDF. 触发：标注文献、给 PDF 加高亮批注、生词和语法注释、图注解读、读论文并标出重点、给论文加阅读指引。"
---

# 学术 PDF 高亮批注

读一篇论文，写出 spec（标哪里、写什么），由 `scripts/annotate_pdf.py` 定位原文并另存一份标注版 PDF：

- 首页便签：研究工作总结和它对我们的用处；
- 语言注释：标题、摘要、引言、结论和图注里的生词与难句；
- 图解读：每张图一条批注；
- 重点内容：按颜色高亮，批注写解释和它与我们工作的关系。

## 触发条件

只在用户显式调用时执行：Claude Code 输入 `/p-pdf-annotate`，Codex 写 `$p-pdf-annotate`。

## 约定

- 原版不动。标注版写到 `<PDF 所在目录>/annotated/<同名>.pdf`，spec 存为同目录的 `<主名>.annot.json`，以后增删标注时改 spec、从原版重跑。项目规则另有位置约定时按项目规则放。
- 运行用 `codexpy` 环境，带上 `-X utf8`，否则 Windows 控制台打印中文时会报 `UnicodeEncodeError`：

```bash
PY=~/mysoft/env/pyenv/codex/Scripts/python
"$PY" -X utf8 <skill-dir>/scripts/annotate_pdf.py -input <原版.pdf> -dump > <scratchpad>/<主名>.txt
"$PY" -X utf8 <skill-dir>/scripts/annotate_pdf.py -input <原版.pdf> -spec <主名>.annot.json \
    -output <目录>/annotated/<同名>.pdf -render_dir <scratchpad>/render
```

spec 格式写在脚本 docstring 里。`note_place` 默认 `inline`（批注挂在高亮上，适合 Zotero、Acrobat）；用户在 Edge 里看时设成 `margin`：高亮不带文字，批注放到同一行页边的便签图标里，因为 Edge 会在带批注的高亮开头画评论图标、盖住上一行的字。margin 模式按阅读顺序给每页的批注编号，页边图标旁和高亮左上角写同一个号，便签正文以 `[号]「原文」` 开头。脚本会在首页便签所在页的页边空白自动画一排颜色图例（批注对象，不改原文）；空白放不下时会给出 ⚠️，图例只留在便签第一行，交付时告诉用户。

## 流程

1. **弄清"我们"是谁。** 读当前项目的 README、CLAUDE.md 和近期交付说明，确认这篇文献是为哪个问题读的。上下文里看不出来就问用户。批注里涉及我们自己的数字，要能在项目文件里查到出处。
2. **通读全文、看图。** 用 `-dump` 导出文字通读，SI 也要看。把含图的页渲染成 PNG 逐张看（`page.get_pixmap(dpi=130)`），图解读要基于图本身，不能只转述图注。`-dump` 输出为空说明是扫描版、没有文字层，告诉用户先做 OCR，然后停下。
3. **写 spec。**
   - `summary`：按 `【一句话】【做了什么】【关键结果】【对我们的用处】【重点页】` 写，每项 1–2 句。"对我们的用处"要点名具体的结论、参数或做法，不写"有参考价值"这类空话。出版商在前面加了封面页时，把 `summary_page` 设成正文首页。
   - 语言注释的范围是标题、摘要、引言、结论和全部图注，不限数量。读者是中文母语的材料或物理方向博士生。
     - `vocab`：标对这位读者生僻的单词、短语、固定搭配，以及领域外的术语。同一个词只在第一次出现处标。批注格式：`词 /音标/ 词性 中文释义；本文语境…`。
     - `grammar`：标长难句和关键句式，例如插入语隔开主谓、分词状语、`as` / `which` 引导的从句、倒装（`Should X stall, …`）、`not … alone` 这类限定。批注格式：`【语法】主干 = …；<成分> 是 …，修饰 …；译：…`。正文里被标成重点、但句式难懂的句子也加一条。
   - `figure`：每张图一条，锚点放在图注开头（如 `FIG. 3. Comparison of the`），不要用正文里的 `Fig. 3`。批注按 `【作用】【推进论点】【子图】(a)… (b)…【值得注意】` 写：这张图要证明什么，它在论证链里推进了哪一步，每个子图得出什么结论，读图时该看哪里（离群点、与我们数据的对照）。从图上读出的数值标"约"；SI 表格里有精确值的，引用表格。
   - 重点内容（`key` / `number` / `definition` / `caution`）：宁少勿多，一篇通常 8–20 处。

     | kind | 样式 | 标什么 |
     |---|---|---|
     | `key` | 黄高亮 | 核心结论、能支撑我们论点的原文 |
     | `number` | 绿高亮 | 数字、参数、可以拿来对照的量级 |
     | `definition` | 蓝高亮 | 定义、方法原理 |
     | `caution` | 红高亮 | 限定条件、局限、与我们做法不同的地方 |
     | `figure` | 橙高亮 | 图注开头，批注写整张图的解读 |
     | `vocab` | 紫高亮 | 生词 |
     | `grammar` | 紫下划线 | 语法、难句 |

     一种样式只表示一种含义。批注以 `【标签】` 开头，用自己的话解释"这句说了什么、对我们意味着什么"，不要照抄原文。
   - 锚点：`start` 和 `end` 从 dump 里原样抄连续词。生词的锚点可以只有它自己；句子的锚点取 3–8 个词，保证在该页唯一。行尾断字也照抄（如 `are com-`），不要拼回完整单词。一条标注不能跨栏或跨页，需要时拆成两条。同一页里重复出现的短语用 `n` 指定第几次出现。
4. **运行并核对。** 退出码为 0 才算全部落位。逐条看 ✅ 行回显的原文是不是想标的那句。再 Read 1–2 张渲染图，确认高亮没有偏行、没有漏行。❌ 行要改锚点后从原版重跑；脚本会拒绝在已经有同作者批注的 PDF 上叠加标注。
5. **交付。** 在聊天里给出：研究工作总结、对我们的用处、标注清单（页码、颜色、要点）、标注版和 spec 的路径。本 skill 不改 Zotero。用户要替换 Zotero 附件时，先确认再操作。
