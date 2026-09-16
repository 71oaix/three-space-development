---
title: 对抗性规格审查
source: three-space-development
type: reference
---

# 对抗性规格审查

## 读取时机

当存在两个或多个可行方案、重要架构决策、明显风险或用户要求钢人式比较时读取。

## 方法

1. 列出候选方案及共同目标。
2. 为每个方案构造最强版本，不比较稻草人。
3. 检查正确性、可验证性、成本、时延、可维护性、扩展性和失败模式。
4. 构造反例、边界条件和最坏情况。
5. 说明推荐方案胜出的条件，以及放弃其他方案的原因。
6. 将仍需用户决定的取舍单独列出。

## 是否值得创建 ADR

以下启发式改编自 [Matt Pocock 的 domain-modeling ADR 规则](https://github.com/mattpocock/skills/tree/main/skills/engineering/domain-modeling)。当前在 Three-Space 中属于 `trial`，不是已验证的强制文档规范。

只有以下条件同时满足时，才建议创建 ADR：

1. 决定难以逆转，之后改变的代价明显；
2. 没有上下文时，未来读者会对这个选择感到意外；
3. 存在真实可行的替代方案，并且选择来自具体取舍。

否则把决定、理由和替代方案保留在已有的 Specification Package 或 Solution Architecture Decision 中，不为形式完整创建 ADR。需要 ADR 时按项目既有目录和 `doc-contract` 约定 lazy 创建；不擅自引入 Matt 的目录或模板。

## 禁止

- 把技术偏好伪装成用户需求。
- 用“能运行”代替“符合规格”。
- 只比较方案优点，不比较失败成本。
- 在关键取舍未确认时直接进入实现。
