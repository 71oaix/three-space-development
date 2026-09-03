---
title: SDD Handoff Contract
source: three-space-development
type: contract
status: active
created: 2026-09-03
updated: 2026-09-03
contract-version: 0.1.0
producer: three-space-development
consumer: sdd-development
---

# SDD Handoff Contract

## 目的

定义三空间 Skill 交给 sdd-development 的最小、稳定、可审查输入。

## 交接条件

只有同时满足以下条件，才可以生成 Handoff：

- Problem、Intention 和 Specification 已经清楚；
- In Scope 和 Out of Scope 已明确；
- 输入、输出、核心行为和失败行为已明确；
- 验收标准可测试；
- Solution Architecture 已记录关键取舍；
- 用户已经批准规格；
- 未决事项为空，或明确标记为不阻塞实现。

## Handoff 最小结构

~~~yaml
handoff_version: 0.1.0
handoff_status: ready
problem_statement: ...
intention_summary: ...
approved_specification:
  scope:
    in_scope: []
    out_of_scope: []
  inputs: []
  outputs: []
  behaviors: []
  rules: []
  failure_behaviors: []
solution_architecture:
  decision: ...
  alternatives_considered: []
  rationale: ...
acceptance_criteria: []
known_risks: []
open_decisions: []
traceability:
  intention_ids: []
  specification_ids: []
  acceptance_ids: []
~~~

## SDD 必须检查

SDD 收到 Handoff 后，必须确认：

- handoff_version 是否支持；
- handoff_status 是否为 ready；
- 必填部分是否完整；
- acceptance_criteria 是否可执行；
- open_decisions 是否为空或不阻塞；
- 方案是否允许进入 implementation plan。

不满足时，SDD 不得假装进入实现，应返回规格变更请求。

## SDD 输出

SDD 应产生：

- Implementation Issue；
- Implementation Plan；
- Tests；
- Verification Evidence；
- 必要时的 Specification Change Request。

## 变更规则

- Patch：不改变字段和语义；
- Minor：新增可选字段或兼容行为；
- Major：删除字段、改变语义或改变交接流程。

生产方先提交 Contract Change Request，消费方先评估兼容性；破坏性变更必须先让 SDD 支持新旧版本，再切换生产方。

## 变更边界

三空间 Skill 拥有 Handoff Contract 的定义权。SDD 拥有消费、实现和反馈权。任何一方都不得通过未记录的直接修改改变另一方的职责。
