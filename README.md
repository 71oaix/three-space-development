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
- references/intention-clarification-protocol.md：Intention 的依赖式分轮澄清、事实/决定分工和领域词汇试行协议；
- references/design-evidence-protocol.md：研究、代码现状、testing seam 和 throwaway prototype 的设计证据试行协议；
- references/retrospective-protocol.md：trial 机制的按需结构化复盘和晋级判断协议；
- templates/：意图、规格和追踪模板；
- gotchas.md：经用户确认的高信号踩坑记录；
- .run-log.jsonl：append-only 运行日志，使用 trial 机制时可附结构化 `retrospective`；
- examples/：跨项目案例（当前为空，按需添加）。

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

本轮从外部工程实践吸收的协议均保留在 references/，并在文件 frontmatter 或正文标记 `trial`；它们不改变三空间边界，也不替换 Specification Package。

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
