---
name: p-tdd
description: "Use ONLY when the user explicitly asks for test-driven, test-first, or red-green-refactor work. Do NOT invoke to add tests after the fact, or when the user just wants the feature implemented. 触发：TDD、测试驱动、测试先行、先写测试再实现、red-green-refactor。"
---

# 测试驱动开发

## 触发条件

只在用户显式调用时执行：Claude Code 输入 `/p-tdd`，Codex 写 `$p-tdd`。
事后补测试、只要求实现功能，不走本流程。

## 循环

1. 读取现有测试结构和命令，确认本次要验证的公共接口与行为边界。
2. 写一个能因缺失行为而失败的测试，并实际观察它失败；失败原因必须与目标行为一致。
3. 只实现让该测试通过的最少代码，再运行相关测试确认变绿。
4. 在全绿状态下整理重复与命名，然后进入下一个纵向切片。
5. 完成后运行最小相关测试集；风险较高时再扩大到项目级检查。

## 测试质量

- 测试可观察行为和公共接口，不绑定私有实现细节。
- 预期值来自规格、已知样例或独立事实，不能用被测算法重新计算预期值。
- mock 只隔离昂贵、不可控或真正跨边界的依赖，不模拟内部调用链。
- 一次完成一个可验证的纵向切片，不预写整批尚未实现的测试。

不因采用 TDD 而更换测试框架、扩展任务范围或重构无关代码。
