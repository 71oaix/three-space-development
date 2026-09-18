# three-space-development

这是三空间开发 Skill 的正式源仓库。

## 作用

本 Skill 负责：

Problem → Intention → Specification → Solution Architecture

然后通过 SDD Handoff Contract 交给 sdd-development。

它不负责具体实现、代码调试、测试交付和合并。

## 目录职责

- SKILL.md：触发边界和路由入口；
- references/：按需加载的深度规则；
- templates/：意图、规格和追踪模板；
- gotchas.md：经用户确认的高信号踩坑记录；
- .run-log.jsonl：append-only 运行日志；
- examples/：跨项目案例。

## 源代码与安装副本

本目录是可编辑、可审阅、可回滚的 Git 源仓库。

运行时安装副本位于 Codex 的用户技能目录：

`<Codex skills directory>/three-space-development`

安装副本不直接编辑。源仓库完成合并、验证和版本标记后，才同步安装。

## 与 sdd-development 的协作

本仓库拥有 SDD Handoff Contract 的定义权。

- 本仓库负责定义交接包内容和版本；
- sdd-development 负责消费交接包并执行；
- SDD 发现规格问题时提交 Specification Change Request；
- 不通过共享未提交文件进行协作。

当前契约文件：

references/sdd-handoff-contract.md

## 公开仓库治理

- 本仓库是公开的技能源仓库；`main` 只接受通过 PR 和 CI 的变更；
- 本仓库是可编辑源，Codex 用户技能目录中的副本是安装产物；
- 不直接编辑运行时副本，也不把其他项目内的旧副本当作维护源；
- 涉及 Handoff Contract 的 PR 必须说明契约版本、兼容性和对 `sdd-development` 的影响；
- 合并并验证后才能创建版本标签并同步运行时副本。

## GitHub 更新流程

1. 从 main 创建任务分支；
2. 只修改本 Skill 职责范围内的文件；
3. 小步提交，提交信息说明真实变更；
4. 推送分支并创建 PR；
5. Review、验证并合并到 main；
6. 创建版本标签；
7. 再更新运行时安装副本。

main 不直接提交。涉及 SDD Handoff Contract 的变更，PR 必须注明契约版本和对 SDD 的影响。

## 版本规则

- Patch：文字、示例或不改变语义的修正；
- Minor：新增兼容字段或兼容行为；
- Major：删除字段、改变语义或改变交接流程。

## 当前远程

https://github.com/71oaix/three-space-development.git
