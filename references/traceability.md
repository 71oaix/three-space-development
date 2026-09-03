---
title: 规格追踪
source: three-space-development
type: reference
---

# 规格追踪

## 读取时机

当任务需要证明需求已被规格覆盖、规格已被测试验证，或需要把实现结果反向追溯到用户目标时读取。

## 最小追踪链

~~~text
Intention ID → Specification ID → Acceptance ID → Test ID → Implementation ID
~~~

每个关键规格至少应有一个验收标准。每个验收标准应能映射到测试或明确的人工审查。实现偏差必须记录为变更或回到规格重新决策。
