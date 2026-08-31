---
name: p-vault-source-import
description: "将外部资料去重并可追溯地导入 Markdown vault。"
---

# Vault Source Import

## 核心流程

1. 将源仓库和原文件视为只读，先清点格式、编码、时间和已有重复项。
2. 原始材料进入 archive/source 层；标准化元数据和链接进入 ingest 层；主题知识进入 wiki 层。
3. 用稳定来源标识、相对路径或哈希去重，frontmatter 记录来源、导入时间和状态。
4. 更新 manifest 或 import log，抽查附件、内部链接、CJK 编码和可重跑性。

## 易踩点

- 导入阶段不提前写综合结论；归档与知识合成分开。
- 不改写源仓库，也不把派生产物写回源目录。
- 同名文件不等于同一来源；去重时保留 provenance。
- 读取中文旧文件失败时先判断编码或 BOM，不直接判为空文件。
