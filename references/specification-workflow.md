---
title: 从意图形成规格
source: three-space-development
type: reference
---

# 从意图形成规格

## 读取时机

当用户的目标仍然模糊，或需要把自然语言目标变成可测试系统定义时读取。

## 步骤

> 来源与验证属性：第 5 步的依赖式前置决定、第 6 步的复用已确认对话，分别吸收自 [Matt Pocock 的 grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) 与 [to-spec](https://github.com/mattpocock/skills/tree/main/skills/engineering/to-spec)。它们已被裁剪为兼容 Three-Space 的工作规则，但仍应通过真实项目持续验证；绝不意味着跳过本 Skill 的 Specification Package、审查、批准或 Gate 2。

1. 提取目标、参与者、触发场景和期望结果。
2. 区分目标、约束、假设和实现偏好。
3. 明确非目标和范围边界。
4. 列出歧义、冲突、缺失信息和需要用户决定的事项。
5. 如果存在依赖关系，按 references/intention-clarification-protocol.md 的 frontier 先完成会阻塞后续判断的 Intention 决策。
6. 将已经确认的 Intention 决定直接综合为候选 Specification，不重复询问已经 settled 的问题；只重新打开会改变边界、行为、失败处理、验收或高层架构的事项。
   只有实际复用了已确认决定并减少重复提问时，才将 `spec.no-repeat` 记为已使用；记录对应的决定与规格条目。
7. 形成输入、输出、状态、规则、失败行为和验收标准。
8. 标注每项规格的来源和决策状态：Fact、Agent Recommendation、User Decision、Assumption 或 Open Decision。
9. 如需外部事实、代码现状、testing seam 或 prototype，读取 references/design-evidence-protocol.md；证据用于支持判断，不替代用户批准。
10. 检查是否达到 Gate 0、Gate 1 和 Gate 2。

## 从对话到 Specification 的边界

“综合已有对话”只是一种减少重复访谈的工作方式，不是批准规格的快捷路径。Specification 仍必须满足本 Skill 的输入输出、行为、规则、失败行为、NFR、Acceptance Contract、Traceability、Solution Architecture、独立语义审查和用户批准要求。

如果转换过程中出现新的事实、代码冲突或未决取舍，应将其标回对应的 Intention/Specification 节点；不得为了让文档看起来完整而默认为用户做决定。

## 规格质量检查

- 可理解：不同读者对行为有相同解释。
- 可审查：关键假设和替代方案显式可见。
- 可测试：每个重要行为有正例、负例或边界例。
- 可实现：没有隐藏的不可行要求。
- 可追溯：目标、规格、测试和实现可以相互关联。
