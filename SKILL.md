---
name: three-space-development
description: >-
  当用户提出模糊的软件目标、需求、架构方向或功能设想，需要把它澄清为可审查、可验收、可实现的系统规格时触发。关键词：意图空间、规格空间、实现空间、需求澄清、系统规格、架构决策、验收标准、需求到设计、SDD 前置分析、需求追踪。当需求已经明确且只需要写 issue、plan、代码、调试或单文件修改时不应触发；这类任务交给 sdd-development、hunt 或其他专用 skill。
---

# Three-Space Development

将软件开发中的模糊意图转化为可审查、可验收、可实现的规格，并在规格稳定后交接给 SDD。

本 Skill 是文件夹而不是单个文件。请按需读取 references，不要一次性加载全部内容。

## 文件地图

### 必须读取

- gotchas.md：执行前读取，了解已经确认的高频坑点。
- .run-log.jsonl：只作为 append-only 操作日志，不需要注入上下文。

### 按需读取

- references/space-model.md：需要界定三个空间时读取。
- references/specification-workflow.md：需要把意图整理成规格时读取。
- references/adversarial-review.md：存在多个方案、风险或重要架构决策时读取。
- references/traceability.md：需要连接意图、规格、测试和实现时读取。
- templates/intention-brief.md：需要整理原始意图时读取。
- templates/specification-brief.md：需要创建规格草案时读取。
- templates/traceability-matrix.md：需要建立追踪矩阵时读取。

## 工作边界

本 Skill 主要负责 Intention Space → Specification Space。

- 需求仍然模糊时，先澄清目标、边界、约束、成功标准和非目标。
- 不把实现方案误写成需求，不在规格未稳定前跳入代码。
- 规格达到批准门后，生成清晰的 SDD handoff，交给 sdd-development 继续处理 issue、plan、实现和测试。
- 已经明确的需求若只需要实现、调试或单文件修改，不触发本 Skill。

## 工作流程

1. 读取 gotchas.md，判断任务是否属于本 Skill 的边界。
2. 读取 references/space-model.md，定位当前内容属于哪个空间。
3. 捕获 Intention：目标、参与者、场景、约束、成功标准、非目标和未决问题。
4. 读取 references/specification-workflow.md，形成可审查的 Specification。
5. 若存在重要替代方案或风险，读取 references/adversarial-review.md，进行钢人式比较。
6. 形成验收标准和必要的追踪关系，按需读取 references/traceability.md。
7. 判断规格是否达到批准门；未达到时明确列出阻塞项，不伪装成可实现。
8. 规格获确认后，生成 SDD handoff，不直接替代 sdd-development。
9. 完成任务后检查是否发现新的候选 gotcha，并询问用户是否确认记录。
10. 追加一条 .run-log.jsonl，记录任务、成功状态和关键发现。

## 输出要求

根据任务规模，输出以下一种或多种产物：

- 意图摘要；
- 规格摘要或规格草案；
- 未决问题和非目标；
- 关键决策及替代方案；
- 验收标准；
- Intention → Specification → Test → Implementation 追踪关系；
- 交接给 SDD 的 issue/plan 输入。

## 阶段门

- Gate 0：意图可理解，目标、参与者、场景、成功标准和非目标已明确。
- Gate 1：规格可实现，输入、输出、规则、失败行为和验收标准已明确。
- Gate 2：规格已批准，关键替代方案、风险和用户决策已完成。
- Gate 3：实现已证明，实现有测试证据，并能追溯回规格。

没有通过 Gate 2 时，不开始需要用户确认的实现工作。

## 与其他 Skill 的关系

- think：需要架构判断、可行性和方案取舍时使用。
- sdd-development：规格批准后的 issue、plan、实现、测试流程。
- doc-contract：创建或修改正式项目文档时使用。
- docs-scan：项目文档结构审查和收尾时使用。
- hunt：已有错误、崩溃或回归问题需要找根因时使用。

## 自迭代规则

每次调用后，如果发现新的高频、可复现坑点，先向用户确认是否记录到 gotchas.md。确认后检查重复项，按三段式格式追加，并更新 last-updated。

累计约 10 条运行日志后，询问用户是否需要将日志提炼为新的 gotcha 或经验库条目。
