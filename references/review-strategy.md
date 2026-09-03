---
title: Specification Package 审查策略
source: three-space-development
type: reference
status: active
created: 2026-09-04
updated: 2026-09-04
contract-version: 0.1.0
---

# Specification Package 审查策略

## 总原则

审查分成确定性检查和语义审查两层。确定性检查优先使用脚本；脚本不能可靠判断的内容，才交给 AI 子审查。脚本通过不等于规格正确，只表示文档具备进入语义审查的基本结构。

## 第一层：确定性脚本检查

使用 scripts/validate_specification_package.py，检查：

- frontmatter 和 contract version；
- 必需章节和交接状态；
- Acceptance Contract 是否有 Given / When / Then；
- Traceability 是否存在 Intention 到 Specification 的关系；
- Approval 字段是否存在；
- ready 状态是否仍有阻塞性未决事项；
- 是否存在明显的模板占位符。

这一层失败时，先修文档结构，不消耗 AI 子审查额度。

## 第二层：AI 子审查

脚本通过后，根据复杂度并行调用独立子审查：

### 语义完整性审查

检查目标、边界、输入输出、核心行为、失败行为是否表达了同一个系统；识别遗漏、矛盾、模糊词和未经证实的假设。

### 架构与风险审查

检查 Solution Architecture 是否回应 Specification，候选方案和取舍是否真实，是否把实现细节偷渡成规格，以及风险和未决事项是否被低估。

### 领域一致性审查（按需）

涉及强领域规则、标准、法规或安全约束时，单独审查来源、解释和适用范围。Link16 这类任务默认启用。

## 汇总规则

主 Agent 只保留有明确证据的发现，并合并重复意见。每个发现至少包含：

- finding_id；
- severity；
- evidence（章节或 ID）；
- problem；
- recommendation。

最终只输出摘要：

- overall：ready / returned；
- 脚本检查结果；
- 最重要的 1–5 个语义发现；
- 阻塞项；
- 下一步动作。

## Gate 规则

- 脚本有 ERROR：returned，不进入 SDD；
- 脚本只有 WARN：交给 AI 判断是否阻塞；
- AI 发现边界、目标、失败行为或验收标准存在实质问题：returned；
- 只有脚本通过、AI 无阻塞发现、且用户批准后：ready；
- 发现已批准规格与实现现实冲突：生成 Specification Change Request，不在实现阶段静默改规格。

## 成本控制

小规格默认使用语义完整性审查；存在多个方案、强领域约束或高风险时再增加架构与领域审查。子审查输出只返回结构化发现，不返回长篇过程记录。
