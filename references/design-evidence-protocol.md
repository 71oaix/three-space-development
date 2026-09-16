---
title: Specification 设计证据协议
source: adapted from mattpocock/skills (domain-modeling, to-spec, prototype, research)
type: reference
status: trial
created: 2026-09-16
updated: 2026-09-16
---

# Specification 设计证据协议

> 本文件是按需启用的试行协议。它规定证据如何帮助 Three-Space 澄清和审查设计，
> 不授权本 Skill 进入正式实现，也不改变 Specification Package、Gate 2 或 SDD Handoff Contract。

## 读取时机

当 Specification 或 Solution Architecture 仍需要以下证据之一时读取：

- 外部事实、标准、API 或领域规则；
- 用户表述与当前代码/文档/运行行为的关系；
- 验收应在哪个最高层可观察边界验证；
- 一个明确的逻辑、状态模型或 UI 设计问题值得用 throwaway prototype 先回答。

没有这些不确定性时，不创建研究笔记、原型或额外的上下文文档。

## 1. 研究事实：Agent 调查，用户决定取舍

本协议不新增搜索入口，也不替代已有的 `web`、`read`、`learn` 或 `openai-docs` 能力；它只规定进入 Three-Space 的证据如何被记录和使用。

研究只回答“世界或当前系统是什么样”，不替用户选择产品优先级或架构取舍。

1. 将问题拆成可验证的事实主张。
2. 优先使用拥有该事实的一手来源：官方文档、标准、源代码、第一方 API 或原始数据。
3. 为每条会影响 Specification/Architecture 的主张记录来源、适用范围、版本/时间条件和不确定性。
4. 将 `Fact`、`Recommendation` 和 `User Decision` 分开；研究结论不是用户决定。

默认把结果写入 Specification Package 的 Evidence 表。只有研究较大、会被多次复用或需要独立审查时，才 lazy 创建一份带引用的 Markdown 研究记录；不要求每次研究都创建新文档。后台委派 Agent 可以作为效率手段，但不是 Gate 条件，也不能降低来源要求。

## 2. 代码现状是证据，不是自动规格

当任务针对现有项目时，先检查相关代码、配置、文档、测试和运行说明，再冻结对现状的描述。

- 用户说法与代码一致时，记录为可支持该判断的证据；
- 用户说法与代码冲突时，列出冲突的双方、证据和影响；
- 不因为代码现在这样就静默把目标改成现状，也不因为用户这样说就静默声称代码已经支持；
- 如果冲突影响边界、行为、失败处理或验收，回到 Intention/Specification 让用户决定，或提交 Specification Change Request。

代码现状可以约束可行 Architecture，但不能绕过用户批准或把实现细节倒灌成需求。

## 3. testing seam 只作为可观察性证据

在 Specification/Architecture 阶段，勾勒验收能够观察到的最高现有 seam：

- 优先使用已有的、能观察完整外部行为的边界；
- 尽量减少跨系统或跨层 seam；
- 如果现有 seam 不足，只记录“需要新增一个什么可观察边界”及其架构取舍；
- 不写模块、函数、文件、测试实现或执行步骤；这些属于 SDD 的 Implementation Space。

seam 是为了证明验收可判定，不是预先编写测试计划。若新增 seam 会改变用户可见行为、成本或系统边界，必须作为用户可决定的 Architecture trade-off 呈现。

## 4. throwaway prototype 只能回答一个设计问题

只有当纸面讨论无法可靠判断一个具体逻辑/状态/UI 问题时，才考虑原型。原型本轮默认保持 `trial`，并遵守以下边界：

### 4.1 先声明问题并选择形状

- “这个逻辑/状态模型在边界场景下是否成立？”使用 logic prototype；
- “这个界面在真实页面密度和信息层级下应该怎样组织？”使用 UI prototype；
- 如果问题不明确，先回到 Intention，不先写 demo。

原型顶部或可见入口必须写出它要回答的问题、假设和不回答的内容。一个原型只回答一个问题，不扩展成“以后也许支持”的需求列表。

### 4.2 Logic prototype

- 代码从第一天起标为 throwaway，状态默认只在内存中；
- 把要验证的 reducer、状态机或纯函数与页面壳分开；
- 每次操作展示完整相关状态；
- 至少走过 happy path、一个 tricky edge case 和一个应拒绝的操作；
- 不接生产数据库、不添加正式测试、不做与问题无关的抽象或 polish。

### 4.3 UI prototype

- 若存在合适的现有页面，优先在同一页面、同一数据和路由上下文中比较结构明显不同的变体；
- 没有合适宿主时才使用明显标注的 throwaway route；
- 变体应改变布局或信息层级，而不只是颜色和文案；
- 原型开关和变体不进入生产路径，变更默认只读；
- 不把原型页面直接当作生产 UI。

### 4.4 回填规格并隔离原型

原型完成后记录：问题、观察到的行为、结论、用户确认的决定，以及受影响的 Intention/Specification/Architecture ID。

原型结论是 Specification evidence，不是批准本身；必须把结论转写到正式 Specification/Architecture 并经过原有审查和用户批准。原型壳可以保留在明确的 throwaway 分支或其他项目既有隔离位置，主分支只保留经过确认的决定；不得把原型 HTML 或未经重写的 demo 当正式实现交给 SDD。
