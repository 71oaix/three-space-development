---
name: three-space-development
description: >-
  当用户提出模糊的软件问题、需求、架构方向或功能设想，需要经过问题界定、Intention 澄清、Specification 形成和高层 Architecture 选择时触发。关键词：意图空间、规格空间、实现空间、问题发现、需求澄清、系统规格、架构决策、验收标准、需求到设计、SDD 前置分析、规格交接、需求追踪。当规格已经批准且只需要写 issue、plan、代码、调试或交付时不应触发；这类任务交给 sdd-development、hunt 或其他专用 skill。
---

# Three-Space Development

将软件开发中的问题和模糊意图转化为可审查、可验收、可实现的 Specification，并在高层架构稳定后交接给 SDD。

本 Skill 是文件夹而不是单个文件。请按需读取 references，不要一次性加载全部内容。

## 文件地图

### 必须读取

- gotchas.md：执行前读取，了解已经确认的高频坑点。
- .run-log.jsonl：只作为 append-only 操作日志，不需要注入上下文。

### 按需读取

- references/space-model.md：需要界定 Intention、Specification、Implementation 三个空间时读取。
- references/lifecycle.md：需要按“发现问题 → 意图 → 规格 → 架构 → 实现 → 验证 → 演化”推进时读取。
- references/specification-workflow.md：需要把意图整理成规格时读取。
- references/adversarial-review.md：存在多个方案、风险或重要架构决策时读取。
- references/traceability.md：需要连接意图、规格、测试和实现时读取。
- references/sdd-handoff-contract.md：规格准备交给 SDD，或需要判断是否达到交接条件时读取。
- templates/intention-brief.md：需要整理原始意图时读取。
- templates/specification-brief.md：需要创建规格草案时读取。
- templates/specification-package.md：规格批准后，需要生成交给 SDD 的 Specification Package 时读取。
- references/review-strategy.md：需要执行交接审查，或决定脚本与 AI 子审查分工时读取。
- scripts/validate_specification_package.py：需要做交接文档结构校验时执行。
- templates/traceability-matrix.md：需要建立追踪矩阵时读取。

## 工作边界

本 Skill 负责问题界定、Intention Space、Specification Space 和 Solution Architecture。

- 需求仍然模糊时，先澄清目标、边界、约束、成功标准和非目标。
- 不把实现方案误写成需求，不在规格未稳定前跳入代码。
- 可以选择高层 Solution Architecture，但不负责具体模块、函数、代码和实现测试。
- 规格达到 Gate 2 后，按 sdd-handoff-contract.md 生成 handoff，交给 sdd-development。
- 已经明确的需求若只需要 issue、plan、实现、调试或交付，不触发本 Skill。

## 生命周期工作流

1. 发现并界定问题，区分真实问题和预设技术方案。
2. 澄清 Intention：目标、参与者、场景、约束、成功标准、非目标和未决问题。
3. 形成 Specification：系统边界、输入输出、行为、规则、失败条件和验收标准。
4. 选择并审查 Solution Architecture，记录候选方案、取舍和风险。
5. 读取 references/review-strategy.md，先执行 scripts/validate_specification_package.py 的确定性检查。
6. 脚本通过后，按任务复杂度调用 AI 子审查；只汇总有证据的语义发现。
7. 判断是否达到 Gate 2；未达到时明确阻塞项，不伪装成可实现。
6. 读取 references/sdd-handoff-contract.md，形成版本化的 SDD Handoff。
7. 将 Handoff 交给 sdd-development；不直接创建实现 issue 或修改代码。
8. 如果 SDD 反馈规格不可行或不完整，回到 Specification 或 Architecture 重新审查。
9. 完成任务后检查是否发现新的候选 gotcha，并询问用户是否确认记录。
10. 追加一条 .run-log.jsonl，记录任务、成功状态和关键发现。

## 输出要求

根据任务规模，输出以下一种或多种产物：

- Problem Brief；
- Intention Brief；
- Specification；
- Solution Architecture Decision；
- 未决问题和非目标；
- 关键决策及替代方案；
- 验收标准；
- Intention → Specification → Test → Implementation 追踪关系；
- 版本化的 SDD Handoff。

## 阶段门

- Gate 0：问题可界定，知道要解决什么问题，且没有把技术方案误当成问题。
- Gate 1：意图可理解，目标、参与者、场景、成功标准和非目标已明确。
- Gate 2：规格已批准，输入、输出、规则、失败行为、验收标准、架构取舍和用户决策已明确。
- Gate 3：实现已证明，实现有测试证据，并能追溯回规格。

没有通过 Gate 2 时，不生成可直接实现的 Handoff。

## 与其他 Skill 的关系

- think：需要架构判断、可行性和方案取舍时使用。
- sdd-development：Gate 2 之后负责 issue、plan、实现、测试和交付。
- doc-contract：创建或修改正式项目文档时使用。
- docs-scan：项目文档结构审查和收尾时使用。
- hunt：已有错误、崩溃或回归问题需要找根因时使用。

## 源仓库与安装副本

本 Skill 的源代码在独立 Git 仓库中维护。用户 Skill 目录只保存已经合并和验证的安装副本，不作为多人协作的编辑源。

跨仓库变更通过 SDD Handoff Contract、Change Request、Git 分支和 PR 协作，不通过共享未提交目录协作。

## 自迭代规则

每次调用后，如果发现新的高频、可复现坑点，先向用户确认是否记录到 gotchas.md。确认后检查重复项，按三段式格式追加，并更新 last-updated。

累计约 10 条运行日志后，询问用户是否需要将日志提炼为新的 gotcha 或经验库条目。
