---
title: 三空间模型
source: three-space-development
type: reference
---

# 三空间模型

## Intention Space

描述用户想解决什么问题，包括原始目标、场景、参与者、约束、成功标准、非目标和歧义。这里允许自然语言和不完整信息，但必须显式标记不确定性。

## Specification Space

描述系统必须满足什么，包括边界、行为、数据、流程、规则、不变量、失败条件、安全约束、验收标准和追踪关系。Specification Space 是开发架构，不等于某个运行时 JSON，也不等于实现代码。

## Implementation Space

描述如何用软件实现 Specification，包括模块、接口、代码、配置、测试、部署和运行时证据。

## 空间转换

~~~text
Intention → 澄清和形式化 → Specification → SDD 实现 → Implementation
                                      ↑                         ↓
                                      └──── 测试证据和偏差反馈 ────┘
~~~

实现不得无记录地发明规格行为。实现发现规格缺失或冲突时，应回到 Specification Space 修订。
