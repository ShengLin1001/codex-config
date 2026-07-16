---
name: p-plot-figure
description: PJ 用 mymetal 风格画科研出版级 matplotlib 图时的固定绘图约束。当为 PJ 写任何 matplotlib 绘图代码时使用：工作流后处理出图、收敛/NEB/拉伸/能量分解等曲线、DOS/能带、带 colorbar 或断轴的图、多子图版式、给已有图加箭头/色带/编号/文字标注，或在 mymetal/universal/plot 下新增绘图函数。规则从 PJ 满意的 mymetal 绘图代码提炼并内联，配合 p-code-style 使用。
---

# P Plot Figure

给 PJ 画 matplotlib 图时，**初版就按下面写**。风格从 `mymetal/universal/plot`
（`general.py` / `plot.py` / `workflow.py` 等）提炼，目标是"出版级、跨图一致、开箱即用"。
工程与命名习惯继承 `p-code-style`（`path_*` / `l` 前缀 / `dict_*` / 注释写为什么 / 声称完成前真验证），本文只补绘图专属约束。

## 最常见的返工点（别犯）

裸 `plt.subplots()` 从零调样式 · 手动散设 fontsize/linewidth 而不用统一入口 ·
覆盖默认字号/线宽/画布尺寸却无数据或版式理由 · 画完图例不 `general_modify_legend` ·
导出叠 `fig.tight_layout()` 破坏绝对版式 · 用 `plt.savefig` 而漏 `bbox_inches='tight'` 致标注被裁 ·
把绘图逻辑写进 `mymetal/post`（应只备数据）· 自己重写已有的 `add_* / general_* / generate_*` 助手。

## 起手式：两个标准入口，二选一

1. **`my_plot()`** —— 直接拿到已配好样式的 `fig, ax`，最常用：
   ```python
   from mymetal.universal.plot.plot import my_plot
   from mymetal.universal.plot.general import general_modify_legend

   fig, ax = my_plot()                       # 单图
   fig, axes = my_plot(fig_subp=[2, 3], fig_sharex=False)  # 多子图，axes 可 .flatten()
   ax.plot(lx, ly, marker='o', label='...')
   ax.set_xlabel('...'); ax.set_ylabel('...')
   general_modify_legend(ax.legend())        # 画完图例必须再 modify
   fig.savefig(path_out, bbox_inches='tight')
   ```
2. **`general_set_all_rcParams()`** —— 只改全局 rcParams，自己 `plt.subplots()`；
   返回一个 `_general_modify_legend` 闭包，画完图例用它。两者效果基本等价，`my_plot` 更省事。
   ```python
   from mymetal.universal.plot.general import general_set_all_rcParams
   lg = general_set_all_rcParams(figure_subp=(2, 2))
   fig, axes = plt.subplots(2, 2)
   ...
   lg(ax.legend())
   ```

**不要**从裸 `plt.subplots()` 手调样式重造这套默认值。

## 多子图：共享轴才压间距，否则保持默认

默认 `wspace/hspace` 是给"每个子图都带 xlabel/ylabel"留的空间。分两种情况：

- **正常多子图**（每个子图都有各自 xlabel、ylabel，不共享轴）→ **保持默认值**，别动间距，
  直接 `fig.savefig(path_out, bbox_inches='tight')`。
- **共享 x/y 轴**（`fig_sharex=True` 等，只在边缘子图标一次 xlabel/ylabel）→ 中间那些 label 和刻度被省掉，
  默认间距会留下大片空白。此时**在 `my_plot()` 之后**用 `plt.subplots_adjust` 把对应方向间距调小，
  再用 tight 兜底自动裁掉多余白边：
  ```python
  fig, axes = my_plot(fig_subp=[3, 1], fig_sharex=True)   # 竖排共享 x 轴
  # ... 各 ax 绘图，只有最下面的 ax 设 xlabel ...
  fig.subplots_adjust(hspace=0.05)     # 共享 x → 压缩行间距（共享 y 则压 wspace）
  fig.savefig(path_out, bbox_inches='tight')   # tight 尺寸兜底，裁掉多余空白
  ```
  只调实际共享的那个方向（共享 x 压 `hspace`、共享 y 压 `wspace`）；`bbox_inches='tight'` 是必须的兜底。

## 默认风格（有数据/版式理由才覆盖）

这些默认值已在入口函数里定死，"跨图一致"靠的就是它们，别随手改：

- **画布**：单图 `one_fig_wh=[10.72, 8.205]` 英寸；坐标区 `axes_width=7.31 × axes_height=5.89`；
  `left=1.918`、`top=0.9517`；子图间距 `wspace=3.41 / hspace=2.315`（英寸）。多子图用 `fig_subp=[rows, cols]`，画布按行列自动放大。
- **字体**：Arial，`fontsize=28`；label `labelpad=15`；`my_plot` 不能在画图前 set xlim/ylim（还没画）。
- **线与点**：`linewidth=3`、`markersize=20`、`markeredgewidth=3`、`markerfacecolor='white'`、实线 `-`。
- **刻度**：`direction='in'`，开次刻度（每格 2 分）；主刻度 `length=8 width=3 pad=10`，次刻度 `length=4 width=3`；默认关顶/右刻度。
- **网格**：开，灰色 `--`，`linewidth=2`。
- **图例**：`loc='upper right'`、`fontsize=24`、`borderpad=0`、`labelspacing/columnspacing=0.5`；
  画完**必须** `general_modify_legend(legend)`（方框 Square、`pad=0.5`、边线 `2.5` 黑、白底、不透明）。
- **数学字体**：`mathtext` custom + Arial，默认斜体 `it`。
- **保存**：`dpi=300`、`transparent=False`、白底、默认 `png`。

## 导出：bbox_inches='tight'，别叠 tight_layout

- 一律 `fig.savefig(path_out, bbox_inches='tight')`：保证超出坐标区的标注/图例/长标签**仍能完整显示**。
- **不要**再调 `fig.tight_layout()`——它会推翻 `general_subplots_adjust` 精算的绝对英寸版式；两者互斥。
- 导出参数（`if_save` / `savefile`）做成函数入参，别把路径写死在函数体里。

## 文件边界（放对地方）

- **工作流后处理出图**（收敛、NEB、拉伸、能量分解、benchmark…）→ `mymetal/universal/plot/workflow.py`，
  函数名 `my_plot_<workflow>`，返回 `(fig, ax/axes)`，用 `if_save/savefile` 控制落盘。
- **某一主题**绘图函数 → 在 `universal/plot/` 下新建主题文件（参考 `energy.py`、`atominfo.py`、`n2p2.py`），
  模块 docstring 开头列 `Functions:`。
- **通用样式/修饰/标注助手** → `general.py`；**画布创建器**（`my_plot*`）→ `plot.py`。
- `mymetal/post/<name>.py` **只准备数据并调用绘图函数**，不写 matplotlib 细节。

## 复用现成助手（别重写）

先查 `general.py` / `plot.py`，常用：

- 画布：`my_plot`（标准）、`my_plot_colorbar`（带 colorbar）、`my_plot_brokenaxed`（断轴）、`my_plot_modify_ploted_figure`（改造已画好的图）。
- 图例：`general_modify_legend`。轴/刻度/边距：`general_axes`、`general_margin_bin`。
- 线与色：`general_modify_line`、`generate_gradient_colors`（渐变/cmap 采色）、`general_add_vlines_hlines`。
- 标注：`add_arrow`、`add_color_band`、`add_circle_number`、`general_adjust_text`（自动避让防重叠）。
- 命名规律：画布/工作流 `my_plot_*`、样式修饰 `general_*`、标注 `add_*`、采色 `generate_*`、自省 `get_*/check_*`。

## 交付前自检

- [ ] 用了 `my_plot()` 或 `general_set_all_rcParams()`，没从裸 `subplots` 手调样式。
- [ ] 没有无理由地覆盖默认字号/线宽/画布尺寸。
- [ ] 每个 `ax.legend()` 后都跟了 `general_modify_legend`（或闭包 `lg`）。
- [ ] 导出用 `fig.savefig(..., bbox_inches='tight')`，没有叠 `fig.tight_layout()`。
- [ ] 多子图：共享轴才 `subplots_adjust` 压对应方向间距，普通多子图保持默认间距。
- [ ] 绘图函数放对文件（workflow.py / 主题文件 / general.py / plot.py），`post` 只备数据。
- [ ] 先找了现成 `add_*/general_*/generate_*` 助手，没重复造轮子。
- [ ] `if_save/savefile` 做成入参；函数返回 `(fig, ax)`；声称"图已出"前真跑过。
