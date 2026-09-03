---
title: 三空间开发生命周期
source: three-space-development
type: reference
---

# 三空间开发生命周期

## 核心链条

发现并界定问题
  ↓
澄清 Intention
  ↓
形成 Specification
  ↓
选择 Solution Architecture
  ↓
指导 Implementation
  ↓
验证
  ↓
受控演化

这是一条生命周期，不是四个或更多空间。三空间回答“内容属于哪里”，生命周期回答“开发活动如何推进”。

## 阶段与产物

| 阶段 | 主要问题 | 主要产物 |
|---|---|---|
| 发现问题 | 是否有真实问题值得解决 | Problem Brief |
| 澄清 Intention | 用户真正想要什么 | Intention Brief |
| 形成 Specification | 系统必须满足什么 | Specification |
| 选择 Architecture | 哪种总体方案最合适 | Architecture Decision |
| 指导 Implementation | 如何把批准的规格变成软件 | SDD Handoff、Issue、Plan |
| 验证 | 是否解决了问题，是否正确实现 | Validation、Verification、Evidence |
| 演化 | 新证据如何改变系统 | Change Request、新版本 |

## 空间对应

- Problem Discovery 和 Intention 主要进入 Intention Space；
- Specification 和 Solution Architecture 主要进入 Specification Space；
- Implementation 主要进入 Implementation Space；
- Verification 横跨三个空间；
- Evolution 根据变化原因返回相应空间。

## 反馈回路

- 架构不可行：返回 Specification；
- 实现发现规格缺失：提交 Specification Change Request；
- 验证发现目标错误：返回 Intention 或 Problem；
- 新场景出现：扩展 Specification，并重新判断 Architecture。

## 边界

Architecture 不是 Implementation 的细节。Solution Architecture 由本 Skill 负责，Implementation Architecture 由 SDD 负责。前者决定系统边界和总体技术路线，后者决定模块、接口、代码和测试组织。
