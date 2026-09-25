# Research Workflow

一套可跨领域复用的 **学习 + 工程研究流程**，以 Codex skill 插件交付。它帮助你从一个问题开始，找到并复用合适的现成方法，学懂关键机制，在自己的项目中做有界实验，再根据完整证据决定下一步。目标是形成可迁移的研究能力和能运行的工程结果；写论文是可选的下游用途。

本项目的核心是轻量指导与模板。它不要求把已有项目迁到某个框架，也不引入新的 LLM 服务、数据库或实验平台。已有 CLI、notebook、测试、数据工具和审查规则仍是项目的执行依据。[验证记录](docs/validation.md)区分了插件结构检查、跨领域纸面迁移与真实实验。

## 一轮怎么做

```text
问题与学习目标 → 查找并试用现有方案 → 解释机制与写预测
              → 冻结对照、评价和预算 → 基线与有界实验
              → 核对原始证据与失败 → 人工审查 → 下一轮决定
```

| 交付物 | 回答的问题 |
|---|---|
| 研究简报 | 要学懂什么、解决什么工程问题、什么结果会改变决定？ |
| 来源与方案矩阵 | 哪些原始资料和现成工具可靠、能直接复用、还需验证什么？ |
| 学习记录 | 能否用自己的例子解释机制、重算关键步骤、指出适用边界？ |
| 冻结的实验设计 | 基线、唯一主要改动、测试条件、指标、预算和停止规则是什么？ |
| 完整运行记录 | 每次尝试用了哪个版本、命令、资源、原始产物，失败在哪里？ |
| 分析与下一轮决定 | 数据支持什么、哪些只是解释、最小的下一步是什么？ |

文献型任务不需要假造实验；动手型任务应从项目真实的脚本、数据和运行记录出发。自动研究只在预先限定的可编辑范围和预算内循环，保留失败与未改善的尝试。关于具体设计见 [插件说明](skills/research-workflow/SKILL.md) 与 [有界自动研究约定](skills/research-workflow/references/autoresearch-boundary.md)。

## 复用优先

研究开始时先调查原始文档、开源实现、许可、维护状态、依赖与最小可运行示例；针对真实任务试跑候选方案。能直接满足需求就采用，能小幅适配就做适配，只有明确缺口才补一层薄工具。调研包含 [综合工具与方法矩阵](docs/landscape.md) 和 [自动研究系统比较](docs/autoresearch-options.md)。

当前选型：用 [The Turing Way](https://book.the-turing-way.org/) 学习研究设计与复现，用 [Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science) 给全新数据项目起步；已有仓库优先沿用自己的运行器。需要大量文献管理时可试 [research-hub](https://github.com/WenyuChiou/research-hub) 的单项技能；多阶段重算、大量数据版本或运行检索出现时，再分别评估 Snakemake、DVC 或 MLflow。自动研究借鉴 [autoresearch](https://github.com/karpathy/autoresearch) 的有界循环设计，不移植其 GPU 专用代码。

## 作为 Codex 插件使用

仓库根目录包含 `.codex-plugin/plugin.json`，可作为插件源。安装方式取决于你的 Codex 环境与 marketplace 配置；[官方插件文档](https://developers.openai.com/plugins/concepts/plugins)说明插件结构。也可以直接把 `skills/research-workflow` 放进个人技能目录。

调用示例：

> 用 `$research-workflow` 研究一个新领域。先盘点成熟的开源工作流和可直接复用的工具，再帮我建立学习目标、机制练习和一个有界工程实验。保留来源、全部尝试和失败；看结果前固定评价口径。

> 用 `$research-workflow` 为这个仓库设计两轮自动研究。先读取本地协议和现有 CLI，冻结基线、测试集、主要指标、可改文件、单次超时和总尝试数；每轮输出完整记录和下一步决定。

模板在 [`skills/research-workflow/templates/`](skills/research-workflow/templates/)；按任务取用，不强制增加整套目录。自动循环中涉及发布、外部写入或付费资源的动作仍按实际任务的授权范围处理。

## 真实项目适配

[自动驾驶模型开发教程](https://github.com/Guanzhw/autonomous-driving-model-development-tutorial)是第一个实例：四个已交付单元各有研究设计卡，既有 MetaDrive CLI 提供真实闭环，`scripts/run_research.py` 为每次运行保留来源、日志和轨迹；学习者再从 trace 复核指标并做下一轮决定。插件只规定跨领域的研究决策，驾驶领域的地图、`env.step`、指标和失败口径由该项目负责。

## 边界与许可

本仓库的插件代码和原创文档按 [MIT](LICENSE) 发布。调研只引用第三方链接与概念，没有复制许可不明的模板或代码。工具 README、论文中的能力描述不是亲自验证的性能结论；[调研记录](docs/landscape.md)逐项注明验证层级。使用此流程不能自动证明模型有效，结论仍须来自具体数据、运行和审查。
