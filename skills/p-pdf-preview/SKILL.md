---
name: p-pdf-preview
description: Use when the user wants to organize academic literature tasks into a standard `literatures` directory structure, either for a single paper DOI or for a literature investigation topic. This skill (a.k.a. literature-folder-builder) only creates folders, DOI list files, and preliminary summaries; it does not download PDFs. It is the upstream of p-pdf-download.
---

# Literature Folder Builder

## 目标

当用户要求：

1. 下载或整理**单篇文献**；
2. 围绕某个主题进行**文献调研**；
3. 为后续脚本准备 DOI 输入文件；

使用本 skill 在指定的 `literatures` 目录下创建标准化目录结构。

本 skill **只负责目录组织、DOI 文件和调研摘要记录**，不负责下载 PDF。

## 下游对接

本 skill 是 **p-pdf-download** 的前置程序，产物 `dois_row.txt` 由其 `scripts/pdf_download.py` 消费。对接契约（务必保持一致）：

* DOI 文件名固定为 `dois_row.txt`；
* 单篇：文件只含 1 行 DOI，PDF 会落在该 `dois_row.txt` 同级目录；
* 多篇：每行 `DOI<TAB>子目录名`，下载脚本据第二列建子目录、把对应 PDF 落进去；
* `summary.md` 仅供人看，下载脚本不读、不动它。

建好结构后，由用户运行 `pdf_download.py <YYMMDD_目录>` 完成下载（见 p-pdf-download skill）。

---

## 根目录

默认根目录为：

```bash
literatures
````

如果用户指定其他目录，则使用用户指定的目录。

若根目录不存在，应先创建：

```bash
mkdir -p literatures
```

---

## 日期格式

所有新建子目录均使用当前日期前缀：

```text
YYMMDD
```

例如：

```text
260630
```

---

# 模式一：单篇文献

## 触发条件

当用户提供单篇文献的信息，例如：

* DOI；
* 论文题目；
* 论文链接；
* 论文标题和摘要；
* “帮我下载这篇文献”；
* “为这篇文章创建下载目录”；

使用单篇文献模式。

## 目录结构

在 `literatures` 下创建：

```text
literatures/
└── YYMMDD_简练中文名/
    └── dois_row.txt
```

其中：

```text
YYMMDD_简练中文名
```

为根据文章内容生成的目录名。

## 目录命名规则

目录名由两部分组成：

```text
YYMMDD_简练中文名
```

其中 `简练中文名` 应满足：

* 使用中文；
* 简短明确；
* 能概括文章核心内容；
* 避免过长；
* 不要机械翻译英文标题；
* 不要包含文件系统非法字符，例如：

```text
/ \ : * ? " < > |
```

推荐长度：6–20 个中文字符。

示例：

```text
260630_金纳米线相变
260630_机器学习势模拟多相金
260630_层错能与强韧化
```

## DOI 文件

在该目录下创建：

```text
dois_row.txt
```

内容为 DOI，一行一个 DOI。

单篇文献模式下该文件只包含 1 行：

```text
10.xxxx/xxxxx
```

不要添加额外注释、编号、标题或空行。

## 单篇文献示例

用户输入：

```text
帮我整理这篇文章：DOI 10.1016/j.actamat.2024.xxxxxx
```

应创建：

```text
literatures/
└── 260630_金薄膜相变/
    └── dois_row.txt
```

`dois_row.txt` 内容：

```text
10.1016/j.actamat.2024.xxxxxx
```

---

# 模式二：多篇文献调研

## 触发条件

当用户要求围绕某个主题调研文献，例如：

* “帮我调研……”
* “搜索……相关文献”
* “整理……方向的文献”
* “找一批……论文”
* “检索 MD/DFT/机器学习势相关文献”

使用多篇文献调研模式。

## 目录结构

在 `literatures` 下创建：

```text
literatures/
└── YYMMDD_investigate_主题/
    ├── dois_row.txt
    └── summary.md
```

其中：

```text
YYMMDD_investigate_主题
```

为调研任务目录。

## 目录命名规则

目录名格式固定为：

```text
YYMMDD_investigate_主题
```

其中 `主题` 应满足：

* 使用简洁中文；
* 能概括调研方向；
* 不要过长；
* 不要包含文件系统非法字符；
* 可以保留必要英文缩写，如 DFT、MD、MLP、SFE、FCC、HCP。

示例：

```text
260630_investigate_DFT_MD多相强韧化
260630_investigate_机器学习势多相模拟
260630_investigate_FCC_HCP相变机制
```

---

## DOI 文件格式

多篇文献调研模式下创建：

```text
dois_row.txt
```

每一行格式为：

```text
DOI<TAB>子目录名
```

即 DOI 和子目录名之间必须使用一个制表符 `\t` 分隔。

示例：

```text
10.1016/j.actamat.2024.xxxxxx     金薄膜相变
10.1016/j.commatsci.2023.xxxxxx	  机器学习势多相模拟
10.1038/s41524-2024-xxxxx       	神经网络势界面性质
```

注意：

* 不要使用空格代替 TAB；
* 不要添加表头；
* 不要添加编号；
* 不要添加 Markdown 表格；
* 每篇文献一行；
* 子目录名应简短，供后续下载脚本创建单篇文献子目录使用。

---

## 子目录名规则

`dois_row.txt` 第二列的子目录名应满足：

* 简洁中文；
* 反映该文献核心内容；
* 不必包含日期；
* 不必包含 DOI；
* 不要包含非法路径字符；
* 尽量避免多个文献使用完全相同的名字。

推荐示例：

```text
金薄膜FCC_HCP相变
纳米孪晶强韧化
机器学习势多相模拟
层错能调控塑性
固液界面熔化机制
```

---

# summary.md 要求

多篇文献调研模式必须创建：

```text
summary.md
```

该文件用于记录调研阶段的初步结果。

即使尚未阅读全部 PDF，也应基于检索到的题目、摘要、图文信息、公开页面、数据库信息和初步判断，写入阶段性总结。

## summary.md 推荐结构

```markdown
# 调研主题

## 1. 调研目标

简要说明本次调研希望回答的问题。

## 2. 初步结论

用条目总结当前已经得到的主要判断。

## 3. 重要文献列表

### 3.1 文献一：简短中文名

- DOI:
- 主要内容:
- 与本课题的相关性:
- 后续是否值得精读:

### 3.2 文献二：简短中文名

- DOI:
- 主要内容:
- 与本课题的相关性:
- 后续是否值得精读:

## 4. 主题脉络

总结这些文献之间的关系，例如：

- 研究对象；
- 计算方法；
- 实验方法；
- 关键物理机制；
- 与用户课题的关系。

## 5. 后续阅读建议

列出最值得优先阅读的文献，并说明原因。
```

---

# 执行原则

## 必须做

* 创建 `literatures` 根目录；
* 根据任务类型创建标准子目录；
* 创建 `dois_row.txt`；
* 多篇调研时创建 `summary.md`；
* DOI 文件必须是纯文本；
* 多篇 DOI 文件必须使用 `DOI<TAB>子目录名` 格式；
* 目录名和子目录名应简洁、可读、适合文件系统使用。

## 不要做

* 不要下载 PDF；
* 不要调用外部下载脚本；
* 不要把 DOI 文件写成 Markdown 表格；
* 不要在 `dois_row.txt` 中加入注释；
* 不要把文献标题原样生硬翻译成很长的中文目录名；
* 不要使用非法路径字符；
* 不要把 `summary.md` 写成最终综述论文，它只是调研阶段记录。

---

# Bash 创建示例

## 单篇文献

```bash
mkdir -p "literatures/260630_金薄膜相变"
printf "%s\n" "10.1016/j.actamat.2024.xxxxxx" > "literatures/260630_金薄膜相变/dois_row.txt"
```

## 多篇调研

```bash
mkdir -p "literatures/260630_investigate_DFT_MD多相强韧化"

cat > "literatures/260630_investigate_DFT_MD多相强韧化/dois_row.txt" <<'EOF'
10.1016/j.actamat.2024.xxxxxx	金薄膜相变
10.1016/j.commatsci.2023.xxxxxx	机器学习势多相模拟
10.1038/s41524-2024-xxxxx	神经网络势界面性质
EOF

cat > "literatures/260630_investigate_DFT_MD多相强韧化/summary.md" <<'EOF'
# DFT/MD 多相强韧化调研

## 1. 调研目标

本次调研关注 DFT、MD 和机器学习势在多相金属强韧化设计中的应用。

## 2. 初步结论

- 多相结构可通过界面、层错、孪晶或相变机制影响强度和塑性。
- DFT 适合分析相稳定性、层错能和相变路径。
- MD 适合研究大尺度形变、界面迁移和温度效应。
- 机器学习势有潜力连接 DFT 精度与 MD 尺度。

## 3. 重要文献列表

待补充。

## 4. 主题脉络

待补充。

## 5. 后续阅读建议

待补充。
EOF
```

---

# 质量检查

完成后应检查：

```bash
find literatures -maxdepth 2 -type f
```

并确认：

* 单篇任务只有一个 `dois_row.txt`；
* 多篇调研任务同时包含 `dois_row.txt` 和 `summary.md`；
* `dois_row.txt` 中没有多余表头；
* 多篇调研的 DOI 与子目录名之间是 TAB，而不是空格。
