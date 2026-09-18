---
title: Intention 澄清协议
source: adapted from mattpocock/skills (grilling, domain-modeling)
type: reference
status: trial
created: 2026-09-16
updated: 2026-09-16
---

# Intention 澄清协议

> 本文件是按需启用的试行协议，不是新的空间，也不是独立的 `/grill` Skill。
> 它吸收了 [Matt Pocock 的 grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling) 与
> [domain-modeling](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling) 的部分机制，
> 当前尚未作为 Three-Space 的跨项目验证经验。

## 读取时机

仅在以下情况读取：

- Intention 仍有多个相互依赖的未决分支；
- 用户需要在多个真实取舍之间做决定，或要求压力测试想法；
- 领域术语含糊、重载，或与项目已有词汇冲突；
- 需要用具体场景来确认概念边界。

如果目标、参与者、场景、边界和成功标准已经清楚，且没有重要未决取舍，不为了形式完整而启动访谈。

## 1. 建立 decision tree

把每个需要确认的事项表示为一个决策节点，并记录它依赖哪些前置决定。节点至少标记为：

- `open`：尚未由用户决定；
- `settled`：用户已经明确决定；
- `fact-needed`：需要 Agent 先调查的环境事实；
- `assumption`：当前暂用但尚未确认的假设。

每一轮的 `frontier` 是所有前置依赖已经 `settled` 或已有足够事实、现在无需猜测即可回答的节点。

- 一轮一起提出当前 frontier 中的决定问题；
- 依赖本轮仍未解决节点的问题后置，不提前猜问；
- 用户回答后重算 frontier，不能沿用上一轮的顺序；
- 事实调查进行中时，只暂停依赖该事实的节点，其他 frontier 可以继续。

建议使用简短、可回填的格式：

```text
Q1 — 决策标题：需要决定什么，以及为什么现在需要决定
建议：Agent 推荐的选项和理由；同时说明主要取舍
状态：open / settled / fact-needed / assumption
```

“建议”是 Agent 的 recommendation，不是用户 decision，也不是已批准 Specification。推荐必须说明依据和放弃其他选项的主要代价。

## 2. 分开事实、建议和决定

三类内容不得混写：

| 类型 | 由谁负责 | 写入方式 |
|---|---|---|
| Fact | Agent 调查 | 记录来源、适用范围和必要的版本/时间条件 |
| Recommendation | Agent 分析 | 说明理由、取舍、风险和仍依赖的事实 |
| Decision | 用户决定 | 标记决策人、时间和影响的 Intention/Specification ID |

Agent 应自己查文件、代码、工具和一手资料，不把可以查到的事实变成用户问答题。用户仍然拥有产品目标、范围、优先级和不可逆取舍的决定权。

## 3. 用场景挑战概念，不凭空增加需求

当两个术语、状态或参与者的关系不清时，构造最小的 concrete scenario，优先覆盖：

- 正常路径；
- 一个会暴露边界的 edge case；
- 一个应该被拒绝或不允许的操作。

场景是澄清工具，必须标记为 `probe`，不能因为 Agent 提出了它就自动进入 In Scope、行为规则或验收标准。只有用户确认其重要性后，才将它转化为 Intention 或 Specification 内容。

## 4. 稳定领域词汇

若项目已有 `CONTEXT-MAP.md`，先按地图找到相关 `CONTEXT.md`；若只有根目录 `CONTEXT.md`，读取它。没有这些文件时，不为一个尚未稳定的词汇批量创建文档。

- 用户使用与既有 glossary 冲突的词时立即指出冲突；
- 对含糊或重载词提出一个 canonical term，并列出容易混用的词；
- 用户确认后再在项目既有 glossary 中记录，记录应短，只定义“它是什么”；
- glossary 只保存领域语言，不保存实现细节、规格草稿或架构决定；
- glossary 的存在不会替代 Specification，也不会替用户批准任何行为。

如果用户对系统现状的描述与代码、文档或运行证据矛盾，按 [design-evidence-protocol.md](./design-evidence-protocol.md) 处理为显式证据和待决问题，不静默选择一边。

## 5. 结束一轮和确认 shared understanding

每轮结束时汇总：

- 已 settled 的用户决定；
- Agent 查到的事实及来源；
- Agent 的建议及未解决取舍；
- 仍是 assumption 或 open 的节点；
- 下一轮 frontier，以及它们依赖的节点。

在进入 Specification 形成前确认 shared understanding。这个确认表示 Intention 已可理解，是 Gate 1 的证据；它不替代 Specification 的独立审查、用户批准和 Gate 2。

如果仍有会改变系统边界、核心行为、失败行为、验收标准或高层架构的未决节点，不把它藏在措辞里，继续留在 decision tree 中并阻塞相应 Gate。
