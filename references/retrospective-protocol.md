---
title: Three-Space Trial 机制复盘协议
source: three-space-development
type: reference
status: active
created: 2026-09-16
updated: 2026-09-24
---

# Trial 机制复盘协议

## 读取时机

真实项目中出现下表任一适用信号时，在任务结束前读取本协议并记录。维护本 Skill 时只写源仓库的 `.run-log.jsonl`，不产生项目试用样本。

## 适用信号与用户可见的痕迹

| 机制 ID | 什么时候适用 | 使用后应留下什么 |
| --- | --- | --- |
| `intention.frontier` | 多个未决问题存在前置依赖 | 当前可回答的问题和明确后置的问题 |
| `intention.fact-decision` | 可调查的事实与用户取舍混在一起 | 来源、Agent 建议和用户决定分开呈现 |
| `intention.shared-understanding` | Intention 准备进入 Specification | 可供用户纠正的意图摘要与未决项 |
| `spec.no-repeat` | 已确认的 Intention 正在转为 Specification | 已确认决定与候选规格的对应关系；只问新问题 |
| `evidence.research` | 外部事实会影响规格或架构 | 带来源和适用范围的事实及其影响 |
| `evidence.code-conflict` | 用户表述与代码、文档或运行现状冲突 | 双方证据、影响和待决定项 |
| `evidence.testing-seam` | 验收标准的观察边界不清 | 可观察边界及其架构取舍 |
| `evidence.prototype` | 一个具体设计问题经讨论仍无法判断 | 原型问题、观察、结论及隔离位置 |
| `architecture.adr-heuristic` | 重要架构决定有真实替代方案 | 三条件判断及建或不建 ADR 的理由 |

一项机制只有在真实 Three-Space 任务中出现适用信号，且留下相应动作或产物时，才记为 `used`。只阅读 reference、编写协议、做结构校验，都不算使用。如果信号出现但机制被跳过，记为 `eligible_skipped` 并说明原因；没有信号则不记。

## 记录位置与粒度

真实任务的记录写入当前项目的 `.three-space/trial-usage.jsonl`。每次任务先记一条 `run`：本次经过哪些阶段、哪些机制出现适用信号、哪些实际启用；即使没有适用信号也记空列表。每项适用机制再记一条 `observation`，说明使用或跳过的结果。`case_ref` 在同一项目中标识唯一的一次任务；后续追踪同一任务时复用该值。不要写进 Skill 安装副本或源仓库的 `.run-log.jsonl`。项目日志只存简短的判断和证据指针，不复制用户原话、凭据或研究全文。

如果任务是纯问答、只读审查，或当前没有可写的项目目录，在任务交付中给出同样的简短观察，并明确标记“未持久化”；它不能计入跨项目汇总。既有 2026-09-16 源仓库记录把九项机制列在一次协议维护任务中，不能计入任何真实使用次数。

## 一条真实观察需要什么数据

`run` 中的 `eligible_mechanisms` 是本次出现适用信号的机制，`used_mechanisms` 是其中真正留下动作或产物的机制。`observation` 中的 `trigger` 写出现的适用信号；`status` 为 `used` 或 `eligible_skipped`；`action` 和 `artifact_ref` 指向实际动作或跳过原因；`expected_effect` 是使用前的假设；`observed_effect` 写看到的结果；`evidence_ref` 指向可核对的段落、文件或对话；`cost` 记录额外轮次、时间或上下文；`verdict` 为 `helped`、`neutral`、`hurt` 或 `unknown`。没有直接证据时填 `unknown`，不能凭整体任务成功给某个机制记功。

后续出现用户确认或反证时，追加同一 `case_ref`、同一机制的新观察，不回写旧行；汇总只采用该项目中这一对标识的最后一条，保留原始变化过程。

以下两行是同一次任务的格式示例，不是真实使用记录。没有适用信号时只需第一行，两个机制列表均为空：

```json
{"schema_version":"1.0","record_type":"run","ts":"2026-09-24T10:00:00+08:00","case_ref":"SP-EXAMPLE","artifact_ref":"docs/example-intention.md","phases":["intention"],"eligible_mechanisms":["intention.frontier"],"used_mechanisms":["intention.frontier"]}
{"schema_version":"1.0","record_type":"observation","ts":"2026-09-24T10:00:00+08:00","case_ref":"SP-EXAMPLE","artifact_ref":"docs/example-intention.md#decisions","phase":"intention","mechanism":"intention.frontier","trigger":"Q2 依赖 Q1 的用户决定","status":"used","action":"先确认 Q1，后置 Q2","expected_effect":"避免过早询问 Q2","observed_effect":"Q1 的回答使 Q2 不再需要","evidence_ref":"docs/example-intention.md#decision-q1","cost":"增加一轮澄清","verdict":"helped"}
```

用 `scripts/trial_usage.py append --project-root <项目根目录>` 从标准输入读取一条 JSON 并追加；`validate <日志路径>` 同时校验字段与 run/observation 的对应关系；`summary <多个项目日志路径>` 汇总真实任务数、零信号任务数、每项机制的使用、跳过和结果。脚本只统计 `schema_version=1.0` 的真实项目日志；源仓库维护日志不作为输入。复盘时先看汇总，再读取相关的原始观察和产物。

## Research 与晋级

使用 `evidence.research` 时，把调查入口、事实问题、来源和对规格的影响写入 `action` 或 `evidence_ref`；用户决定仍留在正式 Intention/Specification 产物中。

同一机制至少积累 3 个可比较的真实任务，再审查可见收益、跳过原因和成本；任务差异很大时继续收集。是否将 `trial` 改成正式规则、简化或删除，由用户根据证据决定。项目观察不会自动产生 `gotchas.md` 条目。
