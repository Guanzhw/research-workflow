# Research Workflow

一套可跨领域复用的 **快速入门 + 工程研究流程**，以 Codex skill 插件交付。刚进入一个领域时，先建立问题与方法地图；技术主题还要查证方法为何演进。随后按自己的基础学习关键机制并检查是否理解。已有具体工程问题时，先调查现成方案；需要验证改动时，再在项目中做有界实验并根据证据决定下一步。

本项目的核心是轻量指导与模板。它不要求把已有项目迁到某个框架，也不引入新的 LLM 服务、数据库或实验平台。已有 CLI、notebook、测试、数据工具和审查规则仍是项目的执行依据。[验证记录](docs/validation.md)区分了插件结构检查、跨领域纸面迁移与真实实验。

## 按目标选择路径

```text
快速入门：学习起点 → 领域地图 → 技术演进脉络（技术主题）→ 先修学习路线
          → 机制与小例子 → 独立解释或迁移检查 → 下一步

工程研究：具体问题 → 查找并试用现有方案 → 选用方案或提出待验证预测
          → 必要时冻结评价、运行基线与有界实验 → 核对证据 → 下一轮决定
```

**技术演进脉络**回答“当时遇到什么约束，为什么出现新方法，它解决了什么、又付出什么代价”；**先修学习路线**回答“我应先理解什么，才能学会下一项”。两者顺序可能不同，也可能有并存分支，不能用一条年份列表代替。关键转折应附原始来源，区分有记录的事实与后来的解释。具体核查方法见[技术演进参考](skills/research-workflow/references/technology-evolution.md)。

| 路径与交付物 | 回答的问题 |
|---|---|
| 快速入门：领域入门图 | 这个领域解决什么问题？有哪些主要路线，为什么演变成今天这样？ |
| 快速入门：先修路线与理解检查 | 我现在该学什么？能否不用提示解释转折、用小例子说明机制并迁移到新场景？ |
| 工程研究：研究简报与来源矩阵 | 要解决什么工程问题，哪些原始资料和现成工具可靠？ |
| 工程研究：冻结设计与完整运行记录 | 评价和预算是什么？每次尝试的结果、成本和失败在哪里？ |
| 工程研究：分析与下一轮决定 | 原始证据支持什么，最小的下一步是什么？ |

快速入门可以停在有来源的理解成果，无须假造实验。动手型任务应从项目真实的脚本、数据和运行记录出发。自动研究只在预先限定的可编辑范围和预算内循环，保留失败与未改善的尝试。关于具体设计见[插件说明](skills/research-workflow/SKILL.md)与[有界自动研究约定](skills/research-workflow/references/autoresearch-boundary.md)。

## 复用优先

领域入门先核查关键概念、技术转折与学习资料的原始出处，给每份必读资料一个明确用途。工程选型先调查原始文档、开源实现、许可、维护状态、依赖与最小可运行示例；针对真实任务试跑候选方案。能直接满足需求就采用，能小幅适配就做适配，只有明确缺口才补一层薄工具。调研分别见[学习工作流对照](docs/learning-workflows.md)、[综合工具与方法矩阵](docs/landscape.md)和[自动研究系统比较](docs/autoresearch-options.md)。

工程路径的现有选型：用 [The Turing Way](https://book.the-turing-way.org/) 学习研究设计与复现，用 [Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science) 给全新数据项目起步；已有仓库优先沿用自己的运行器。需要大量文献管理时可试 [research-hub](https://github.com/WenyuChiou/research-hub) 的单项技能；多阶段重算、大量数据版本或运行检索出现时，再分别评估 Snakemake、DVC 或 MLflow。自动研究借鉴 [autoresearch](https://github.com/karpathy/autoresearch) 的有界循环设计，不移植其 GPU 专用代码。

## 作为 Codex 插件使用

仓库根目录包含 `.codex-plugin/plugin.json`，可作为插件源。安装方式取决于你的 Codex 环境与 marketplace 配置；[官方插件文档](https://developers.openai.com/plugins/concepts/plugins)说明插件结构。也可以直接把 `skills/research-workflow` 放进个人技能目录。

调用示例：

> 用 `$research-workflow` 帮我快速入门一个技术领域。我有一点相关基础，想先看清主要问题和方法族、技术为何演变，再得到按先修关系安排的短学习路线。用一个小例子讲清关键机制，并检查我能否独立解释和迁移；给关键转折附来源。

> 用 `$research-workflow` 为这个仓库设计两轮自动研究。先读取本地协议和现有 CLI，冻结基线、测试集、主要指标、可改文件、单次超时和总尝试数；每轮输出完整记录和下一步决定。

模板在 [`skills/research-workflow/templates/`](skills/research-workflow/templates/)；按任务取用，不强制增加整套目录。自动循环中涉及发布、外部写入或付费资源的动作仍按实际任务的授权范围处理。

## 在 OpenResearch 中使用

OpenResearch CLI v0.2.10 支持将完整技能 ZIP 导入所有项目。先把 `skills/research-workflow/` 打包，再导入；单独导入 `SKILL.md` 会缺少模板与参考文件：

```sh
python scripts/package_openresearch.py -o research-workflow-openresearch.zip
orx skills add research-workflow-openresearch.zip
```

打包脚本按固定文件顺序和时间戳写入当前技能目录的所有文件，ZIP 内保留 `research-workflow/SKILL.md`、`references/` 和 `templates/` 的相对路径。`orx skills add` 返回保存的名称及是否替换旧版本；上传技能随后进入 OpenResearch 会话的原生技能目录。导入后，在新会话的技能列表选择 `research-workflow`，核对会话目录中的 `SKILL.md`、`references/openresearch.md` 和 `templates/domain-onboarding.md`，再运行一次只需领域入门的任务，检查实际答复中的方法地图、先修路线和理解题。`orx skill <name>` 只读取 OpenResearch 内置技能，不能用来检验这次导入。运行分工与 A/B 隔离见[OpenResearch 适配说明](skills/research-workflow/references/openresearch.md)。

Windows 上以 Codex 运行会话时，若使用自定义 `ORX_DATA_DIR`，将它放在 `CODEX_HOME` 所在磁盘；当前 OpenResearch 在无符号链接权限时会改用硬链接，跨盘会话启动可能失败。

## 真实项目适配

[自动驾驶模型开发教程](https://github.com/Guanzhw/autonomous-driving-model-development-tutorial)是第一个实例：四个已交付单元各有研究设计卡，既有 MetaDrive CLI 提供真实闭环，`scripts/run_research.py` 为每次运行保留来源、日志和轨迹；学习者再从 trace 复核指标并做下一轮决定。插件只规定跨领域的研究决策，驾驶领域的地图、`env.step`、指标和失败口径由该项目负责。

## 边界与许可

本仓库的插件代码和原创文档按 [MIT](LICENSE) 发布。调研只引用第三方链接与概念，没有复制许可不明的模板或代码。外部工作流文档中的能力描述不是亲自验证的学习效果；[学习工作流对照](docs/learning-workflows.md)与[工程调研记录](docs/landscape.md)注明核查范围。工程结论仍须来自具体数据、运行和审查。
