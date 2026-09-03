---
title: Specification Package（Intention → SDD 交接模板）
source: three-space-development
type: template
status: active
created: 2026-09-04
updated: 2026-09-04
contract-version: 0.1.0
tags: [specification, handoff, sdd, three-space]
---

# Specification Package

> 三空间 Skill 交给 SDD Skill 的正式交接文档模板。
>
> 用用户和系统可观察的语言填写；可以写高层架构边界，但不要写函数、类、代码步骤或具体实现计划。
> draft 不能进入 SDD；只有用户批准且所有阻塞项清零后才改为 ready。

## 1. 交接控制信息

| 字段 | 内容 |
|---|---|
| package_id | SP-YYYYMMDD-XXX |
| handoff_version | 0.1.0 |
| handoff_status | draft / ready / returned |
| title |  |
| owner |  |
| created / updated |  |
| source_problem_id |  |
| supersedes | 无 / 旧 Package ID |

- draft：仍在澄清或审查，SDD 不得开始实现；
- ready：规格已经批准，可以进入 SDD Preflight；
- returned：SDD 发现规格问题，退回三空间修改。

## 2. Problem Space

### 2.1 问题陈述

当前发生了什么问题？谁受到影响？如果不解决会怎样？

### 2.2 当前环境与证据

- 当前系统或流程：
- 触发事件：
- 主要参与者：
- 已有解决方式及其不足：

| Evidence ID | 证据或观察 | 来源 | 备注 |
|---|---|---|---|
| E-001 |  |  |  |

## 3. Intention Space

### 3.1 意图摘要

用一句话说明用户真正想达成的结果，不写解决方案。

### 3.2 目标

- I-001：
- I-002：

### 3.3 参与者与典型场景

| Actor ID | 角色 | 目标或关切 | 参与方式 |
|---|---|---|---|
| A-001 |  |  |  |

#### Scenario S-001：场景名称

- 前置条件：
- 用户意图：
- 期望结果：
- 不希望发生：

### 3.4 成功定义与非目标

- Success-001：
- N-001：本次明确不解决的内容。

## 4. Approved Specification

### 4.1 系统边界

#### In Scope

- SPEC-001：
- SPEC-002：

#### Out of Scope

- SPEC-OUT-001：
- SPEC-OUT-002：

边界判定：系统负责什么、系统不负责什么、与外部系统或人工的分界是什么？

### 4.2 输入与输出

| Input ID | 输入名称 | 来源 | 形式 | 必填 | 有效性要求 |
|---|---|---|---|---|---|
| IN-001 |  |  |  | 是/否 |  |

| Output ID | 输出名称 | 接收者 | 形式 | 必须保证 |
|---|---|---|---|---|
| OUT-001 |  |  |  |  |

### 4.3 核心行为

#### Behavior B-001：行为名称

- 触发：
- 前置条件：
- 系统必须：
- 系统不得：
- 结果与可观察证据：

### 4.4 领域规则与不变量

这里写必须遵守的事实、标准、约束和关系，不要改写成代码步骤。

| Rule ID | 规则 | 来源或依据 | 违反时处理 |
|---|---|---|---|
| R-001 |  |  |  |

### 4.5 失败行为与边界情况

| Failure ID | 触发条件 | 系统行为 | 用户可见结果 | 是否阻塞 |
|---|---|---|---|---|
| F-001 | 输入缺失 |  |  | 是/否 |
| F-002 | 输入冲突 |  |  | 是/否 |
| F-003 | 外部依赖不可用 |  |  | 是/否 |

### 4.6 非功能要求与接口语义

| NFR ID | 类别 | 要求 | 度量或验证方式 |
|---|---|---|---|
| NFR-001 | 性能/安全/可靠性/审计 |  |  |

- 核心实体与标识唯一性：
- 数据生命周期：
- 外部接口的语义约束：
- 兼容性要求：

本节描述语义和契约，不规定具体类名、函数名、数据库表名或框架。

## 5. Solution Architecture

### 5.1 推荐方案

- Architecture decision：
- 系统边界与主要组件：
- 组件之间的关系：
- 外部依赖：
- 关键不变量：

### 5.2 候选方案与取舍

| Option | 方案摘要 | 优点 | 缺点或风险 | 结论 |
|---|---|---|---|---|
| A |  |  |  | 采用/不采用 |
| B |  |  |  | 采用/不采用 |

### 5.3 给 SDD 的自由度与约束

SDD 可以决定：技术组件、模块内部组织、函数或文件划分、测试实现方式。

SDD 不得擅自改变：系统边界、核心行为、输入输出语义、失败行为、验收标准和已批准领域规则。

## 6. Acceptance Contract

每条验收标准必须关联 intention 或 specification，并能通过测试、检查或人工观察判定。

| Acceptance ID | Given 前置条件 | When 触发 | Then 可观察结果 | 追踪 |
|---|---|---|---|---|
| AC-001 |  |  |  | I-001 / SPEC-001 |
| AC-002 |  |  |  | B-001 / R-001 |

- 已覆盖的目标：
- 未覆盖的目标及原因：
- 需要人工确认的验收项：

## 7. 风险与未决事项

| Risk ID | 风险 | 可能性 | 影响 | 缓解方式 | 是否阻塞 |
|---|---|---|---|---|---|
| RISK-001 |  | 高/中/低 | 高/中/低 |  | 是/否 |

| Decision ID | 未决问题 | 选项 | 决策人 | 截止条件 | 是否阻塞 SDD |
|---|---|---|---|---|---|
| OD-001 |  |  |  |  | 是/否 |

handoff_status 为 ready 时，阻塞性 open_decisions 必须为空。

## 8. Traceability

| Intention | Specification | Behavior 或 Rule | Acceptance | Future Issue 或 Plan |
|---|---|---|---|---|
| I-001 | SPEC-001 | B-001 / R-001 | AC-001 | 待 SDD 填写 |

## 9. Approval

- specification_review：通过 / 退回
- approved_by：
- approved_at：
- approval_note：
- handoff_to：sdd-development
- handoff_date：

## 10. SDD 接收记录

- preflight_status：pending / accepted / returned
- compatibility：supported / unsupported
- received_at：
- implementation_issue：
- implementation_plan：
- specification_change_request：
- SDD 备注：

## Ready Gate 自查

- [ ] Problem、Intention、Specification 都已清楚。
- [ ] In Scope 和 Out of Scope 已明确。
- [ ] 输入、输出、核心行为和失败行为已定义。
- [ ] 领域规则和不变量有来源或明确依据。
- [ ] 验收标准可执行、可观察、可追踪。
- [ ] Solution Architecture 有推荐方案、候选方案和取舍理由。
- [ ] SDD 的自由度与不可擅自改变的内容已写清。
- [ ] 所有阻塞性未决事项已清零。
- [ ] 用户已经批准本 Specification Package。
