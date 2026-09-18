---
title: Three-Space Trial 机制复盘协议
source: three-space-development
type: reference
status: active
created: 2026-09-16
updated: 2026-09-16
---

# Trial 机制复盘协议

## 读取时机

仅在本次运行实际使用了 `trial` 机制、修改了本 Skill 的机制，或用户要求复盘时读取。普通运行不需要为没有使用的机制增加记录负担。

## 目的与边界

复盘记录用来回答“这条机制在真实任务中是否有帮助”，不是把一次成功自动升级为正式规范，也不是把完整对话复制进日志。

`.run-log.jsonl` 是 append-only 源记录。保留历史记录的原有字段和格式；新记录可以继续使用 `ts`、`task`、`success`、`findings`，在确实需要评估机制时追加 `schema_version` 和可选的 `retrospective`。

## 稳定机制 ID

使用短而稳定的 ID，避免每次用自然语言重新命名同一机制：

| ID | 机制 |
| --- | --- |
| `intention.frontier` | 按依赖关系推进当前可问的 Intention 决策前沿 |
| `intention.fact-decision` | 分开记录 Agent 事实、Agent 推荐和用户决定 |
| `intention.shared-understanding` | 在离开 Intention 前用摘要确认共同理解 |
| `spec.no-repeat` | 从已确认的 Intention 形成 Specification 时不重复访谈 |
| `evidence.research` | 将外部调查作为带来源和适用范围的事实证据 |
| `evidence.code-conflict` | 发现代码/文档/运行现状冲突时回到设计判断 |
| `evidence.testing-seam` | 用最高层可观察边界检查可验证性，不提前设计实现测试 |
| `evidence.prototype` | 用一次性最小实验回答一个具体设计问题 |
| `architecture.adr-heuristic` | 只为难以逆转、易产生意外且存在真实取舍的决策建 ADR |

这些 ID 是记录索引，不改变各机制的 `trial` 或正式状态；机制的详细协议仍以对应 reference 为准。

## 记录契约

当本次确实使用了一个或多个机制，在运行日志最后追加一条结构化复盘。至少填写：

```json
{
  "schema_version": "0.2",
  "ts": "2026-09-16T18:00:00+08:00",
  "task": "完成一次 Three-Space 规格澄清",
  "success": true,
  "findings": ["..."],
  "retrospective": {
    "mechanisms": ["intention.frontier", "evidence.code-conflict"],
    "expected_effect": "减少重复提问，并及时暴露目标与现状的冲突",
    "observed_effect": "...",
    "evidence": "用户确认摘要；对照到的文件、运行结果或规格条目",
    "cost": "增加一轮摘要确认，约 3 分钟",
    "next": "keep"
  }
}
```

`next` 只允许表达本次运行后的建议：`keep`、`adjust`、`drop` 或 `collect-more`。如果多个机制同时使用，`mechanisms` 全部列出，并在 `observed_effect` 和 `evidence` 中说明哪些现象对应哪些机制；不要把无法区分的整体成功归因给每一条机制。

记录应优先写可观察证据：用户纠正、减少的往返轮次、发现的冲突、通过的检查、被排除的方案、额外耗时或上下文成本。没有证据时写明“尚无直接证据”，不要用主观印象伪装成验证结果。

## Research 的复盘字段

使用 `evidence.research` 时，只记录调查如何影响 Three-Space 判断，例如研究入口（`web`、`read`、`learn` 或 `openai-docs`）、事实问题、来源是否改变规格约束，以及哪些取舍仍由用户决定；不要把搜索结果全文重复写入 `.run-log.jsonl`。

## 何时改变正式规则

单次运行只能留下观察记录。至少积累 3 次可比较使用；若任务差异较大或机制影响较大，宜收集到约 5 次再判断。确认收益超过提问、检索、原型或上下文成本后，再由用户决定将 `trial` 改为正式协议、调整它或删除它。复盘本身也不自动产生 `gotchas.md` 条目；gotcha 仍须满足现有的高频、可复现和用户确认条件。
