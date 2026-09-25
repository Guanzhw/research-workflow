# 跨领域 Research Workflow 开源生态：复用优先调查

核查日期：**2026-09-26**。目标是支持学习者提出问题、动手实验、复现工程结果并沉淀认识；论文写作和投稿只占较低权重。本调查读取项目原始 README、关键文件、官方文档与 GitHub REST API；没有安装或执行候选运行时。下文的命令是**上游文档给出的入口**，不能当作本机运行通过的证据。GitHub `pushed_at` 只代表仓库有推送，不能替代测试、发布或维护质量判断。

## 比较口径

“来源／引用”区分文献引用与代码、数据、运行来源。“设计”区分普通计划与看结果前冻结的假设或正式预注册。“人审”只在产品明确设置人的决定环节时标为内建。接入难度针对已有 Python、生成式 notebook 与多个实验 CLI 的课程仓库；新项目脚手架的难度另行说明。

| 一手项目／定位 | 跨领域、学习与动手 | 执行、来源、设计、人审 | 许可证与维护信号 | Codex 接入／判断 |
|---|---|---|---|---|
| [The Turing Way](https://book.the-turing-way.org/)：研究、项目设计、协作和交流手册 | 高；适合教学与反思，非运行器 | 讲复现、引用、项目设计与开放审查；不自动冻结本项目实验 | [文档 CC-BY、软件 MIT](https://github.com/the-turing-way/the-turing-way/blob/main/LICENSE.md)；[仓库 9-21 推送](https://api.github.com/repos/the-turing-way/the-turing-way) | **采纳方法**，低；把章节作为学习与审查资料 |
| [The Turing Way 项目模板](https://github.com/the-turing-way/reproducible-project-template/blob/main/README.md)：仓库结构 | 高；适合新项目起步，非实验执行器 | `data/raw`、`data/processed`、`src/`、`project-management/`；无内建预注册或运行验证 | [代码 MIT、文档 CC-BY](https://github.com/the-turing-way/reproducible-project-template/blob/main/LICENSE.md)；[2025-03-19 推送](https://api.github.com/repos/the-turing-way/reproducible-project-template) | **按需取清单**，低；现有仓库不重排 |
| [Project TIER 4.0](https://www.projecttier.org/tier-protocol/protocol-4-0/)：计算证据包协议 | 统计实证研究为主；“从原始数据到结果”的验收观念通用 | 要求数据、脚本、支持信息、输出和 Master Script；不提供通用 CLI、假设登记或内建科学审查 | 官网页脚链接 CC BY-NC 4.0；相关 [R 模板](https://github.com/ProjectTIER/ProjectTIER_R) [2017-06-20 后未推送](https://api.github.com/repos/ProjectTIER/ProjectTIER_R)，不可当作 4.0 活跃代码 | **采纳复算原则**，低；勿复制未确认许可的正文 |
| [Cookiecutter Data Science v2](https://github.com/drivendataorg/cookiecutter-data-science/blob/master/README.md)：工程脚手架 | 高；直接生成数据、源码、notebook、报告、测试和 Makefile | 数据目录和命令入口清晰；`references/` 保存资料，但无内建假设冻结、文献核验或人审 | [MIT；2026-08-07 推送](https://api.github.com/repos/drivendataorg/cookiecutter-data-science) | **新项目采用**，低；迁入现有仓库为高成本 |
| [SMAIRT](https://github.com/PNNL-CompBio/smairt-template/blob/main/README.md)：假设循环模板 | 标称支持计算生物、物理、化学、工程等；方法与课程问题贴近 | `hypotheses/`→`experiments/`→`results/logs/`→`analysis/`，另有人类贡献记录；上游安装命令失效 | [仓库 API 许可证为空，2026-08-24 推送](https://api.github.com/repos/PNNL-CompBio/smairt-template)；递归树无根 LICENSE/COPYING/NOTICE | **只参考方法**；暂不复制模板或依赖其安装路径 |
| [research-hub](https://github.com/WenyuChiou/research-hub)：研究技能、CLI、MCP | 跨学科文献比较、问题设计、项目定向和知识交接较强；实验仍依赖项目代码 | 文献矩阵、设计 brief、`.research/` 状态、八阶段工作流和人的决定关口；不是正式预注册服务 | [MIT；2026-09-21 推送](https://api.github.com/repos/WenyuChiou/research-hub) | **选择性复用 skill**，低；完整状态机及外部服务中高 |
| [OpenRepro-Agent](https://github.com/SHENAO1/OpenRepro-Agent/blob/main/README.md)：论文复现工作区 | 可借鉴证据打包，课程学习适配偏低 | 来源摄取、候选人工批准、实验 spec、运行 manifest 和质量门；其示例不证明论文复现 | [MIT；2026-06-09 推送](https://api.github.com/repos/SHENAO1/OpenRepro-Agent) | **延后整合**，高；其运行器绑定专属目录和模板 |
| [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory)：文献→实验→报告代理 | 自动科研叙事较完整，学习者主导的反思较弱 | 有代理阶段和代码；不能由报告生成推断科学正确性或人的充分审查 | [MIT；2025-08-20 推送](https://api.github.com/repos/SamuelSchmidgall/AgentLaboratory) | **低优先级**，高；论文导向且维护信号较旧 |
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch)／[program.md](https://github.com/karpathy/autoresearch/blob/master/program.md)：有界自动迭代实例 | 可教固定评估器、预算、失败记录；任务特定，不是通用科研工作流 | 单目标训练迭代；不覆盖文献、预注册、多指标教学判断 | [仓库 API 许可证为空、树无根 LICENSE/COPYING/NOTICE；2026-03-26 推送](https://api.github.com/repos/karpathy/autoresearch) | **只参考控制思想**；不复制代码或流程文本 |
| [OSF 项目与注册](https://help.osf.io/article/330-welcome-to-registrations)：正式登记 | 跨学科；适合把探索性和事先计划区分开，不执行实验 | 可生成带时间戳、只读的预注册；项目文件、协作者及 DOI；登记审批不等于科学同行审查 | [服务代码 Apache-2.0、2026-09-25 推送](https://api.github.com/repos/CenterForOpenScience/osf.io)；所引支持文章标 CC0 | **按需采用**，外部服务接入中等 |
| [ELIXIR RDMkit](https://rdmkit.elixir-europe.org/data_life_cycle)：数据管理指南 | 以生命科学社群为中心，生命周期原则可跨域；非运行器 | 数据计划、管理、共享指导，不追踪具体运行 | [文档 CC-BY、软件 MIT](https://github.com/elixir-europe/rdmkit/blob/master/LICENSE)；[2026-09-17 推送](https://api.github.com/repos/elixir-europe/rdmkit) | **参考**，低 |
| [Snakemake](https://snakemake.readthedocs.io/en/stable/tutorial/basics.html)：依赖图执行 | 高；多阶段动手项目可自动部分重算 | 规则连接输入、输出、命令及日志；不管文献、预注册、人审 | [MIT；2026-09-20 推送](https://api.github.com/repos/snakemake/snakemake) | **按触发条件采用**，中：真实 DAG 和重复部分重算出现时 |
| [DVC](https://doc.dvc.org/user-guide/experiment-management)：数据与实验版本 | 高；适合较大数据／模型项目 | Git 对齐的数据、参数、指标和实验比较；不管研究问题或人审 | [Apache-2.0；2026-09-21 推送](https://api.github.com/repos/treeverse/dvc) | **按触发条件采用**，中：产物超出 Git／运行比较变复杂时 |
| [MLflow Tracking](https://mlflow.org/docs/latest/ml/tracking/)：ML 运行记录 | 模型实验较强；非完整研究生命周期 | 参数、指标、artifact、run 查询；文献、设计冻结和人审外置 | [Apache-2.0；2026-09-25 推送](https://api.github.com/repos/mlflow/mlflow) | **按触发条件采用**，中：大量运行需要查询面板时 |
| [Kedro](https://docs.kedro.org/en/stable/getting-started/kedro_concepts/)：数据管线 | 高；面向较复杂工程数据流 | 节点、数据 catalog、配置与管线；不自动审查科学解释 | [Apache-2.0](https://github.com/kedro-org/kedro/blob/main/LICENSE.md)；[2026-09-24 推送](https://api.github.com/repos/kedro-org/kedro) | **延后**，高：需重构现有 CLI 与数据组织 |
| [RO-Crate](https://www.researchobject.org/ro-crate/specification/1.3/index.html)：研究对象元数据 | 高；适合跨机构交换成果，非执行器 | 以机器可读关系打包数据、软件、人员、来源；不规定假设或审查 | [Apache-2.0；2026-09-24 推送](https://api.github.com/repos/ResearchObject/ro-crate) | **按需采用**，中：对外发布证据包时 |
| [DataLad](https://www.datalad.org/)：数据版本与可复算命令 | 高；大数据／多来源工作流 | 数据版本、运行记录、来源；不管文献或人的解释 | [MIT](https://github.com/datalad/datalad/blob/maint/COPYING)；[2026-09-25 推送](https://api.github.com/repos/datalad/datalad) | **延后**，中高：大数据需求确立时 |
| [Jupyter Book](https://jupyterbook.org/stable/get-started/build-websites/)／[Quarto](https://quarto.org/docs/books/)：可执行学习出版层 | 跨领域；把 notebook、叙述、图和引用组合成可浏览教材 | 能构建展示物；运行真实性仍取决于实验 CLI 与 trace 核查 | Jupyter Book [BSD-3-Clause、9-23 推送](https://api.github.com/repos/jupyter-book/jupyter-book)；Quarto [MIT](https://github.com/quarto-dev/quarto-cli/blob/main/COPYING.md)、[9-25 推送](https://api.github.com/repos/quarto-dev/quarto-cli) | **按需采用**，中：统一导航、构建与发布成为需求时 |

## 三项优先复用：关键文件与边界

### 1. The Turing Way：采用教学方法；改编模板清单

官方[项目设计概览](https://book.the-turing-way.org/project-design/pd-overview/)可用作“为什么记录问题、来源、失败和决策”的学习材料。[模板 README](https://github.com/the-turing-way/reproducible-project-template/blob/main/README.md)建议通过 GitHub **Use this template** 新建项目；实际树有 `CONTRIBUTING.md`、`LICENSE.md`、`project-management/`、`data/{raw,processed}/` 与 `src/`。仓库树**没有** README 示意中的 `docs/`、`notebooks/`、`reports/` 或可运行实验脚本。其价值在项目治理和复现清单；现有课程已具备更具体的 notebook 生成、实验运行和审查结构，应直接借鉴章节和核对问题。

### 2. Cookiecutter Data Science v2：新项目直接使用；现有项目取工程约定

[README](https://github.com/drivendataorg/cookiecutter-data-science/blob/master/README.md)明确 v2 命令为 `pipx install cookiecutter-data-science` 后运行 `ccds`，不是旧版的裸 `cookiecutter`。递归树核对到真实模板 `{{ cookiecutter.repo_name }}/Makefile`、`data/{raw,interim,processed}/`、`references/`、`notebooks/`、`reports/`、Python 包及 [生成测试](https://github.com/drivendataorg/cookiecutter-data-science/blob/master/tests/test_creation.py)；`ccds/__main__.py` 指向该模板仓库。它解决新项目组织、构建命令和工程一致性，未解决“先定假设与主要终点”或“从完整轨迹核对科学主张”。已有课程不宜重建目录。

### 3. research-hub：先复用单项技能；状态机需验证净收益

[研究设计技能](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-design-helper/SKILL.md)引导可证伪问题、机制、识别、验证与风险；[文献矩阵技能](https://github.com/WenyuChiou/research-hub/blob/master/skills/literature-triage-matrix/SKILL.md)可从手工论文清单启动；[项目定向技能](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-project-orienter/SKILL.md)和[上下文压缩技能](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-context-compressor/SKILL.md)服务知识交接。README 给出 `pip install research-hub-pipeline`、`research-hub install --platform codex`；[安装测试](https://github.com/WenyuChiou/research-hub/blob/master/tests/test_skill_installer.py)含 Codex 目标路径。

完整 [orchestrator](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-workflow-orchestrator/SKILL.md)和[工作流契约](https://github.com/WenyuChiou/research-hub/blob/master/skills/research-workflow-orchestrator/references/workflow-contract.md)使用 `.research/workflow_state.yml`，并将执行交给项目特定工具。[运行时文档](https://github.com/WenyuChiou/research-hub/blob/master/docs/workflow-runtime.md)列出 `research-hub workflow init|status|validate|decide|resume|migrate`。已有课程的 `PROJECT_REFERENCE.md`、研究卡和 `scripts/run_research.py` 已保存类似事实；全套状态机可能造成双重维护。建议先在一次新问题上试用设计／文献技能，比较学习者的设计质量和实际工作量，再决定是否接入运行时。仓库 `pyproject.toml` 标 1.2.0，而 [GitHub 最新正式 release](https://api.github.com/repos/WenyuChiou/research-hub/releases/latest) 为 v1.0.0；安装前要固定实际可得版本并运行真实用例。

## 已做的直接核查与尚缺证据

| 只读核查 | 结果 |
|---|---|
| `Invoke-RestMethod https://api.github.com/repos/{owner}/{repo}`，读取 `pushed_at`、`license.spdx_id`、`archived` | 上表仓库均非 archived；时间和 API 许可字段见逐行链接。对 `NOASSERTION` 仓库继续读许可证文件。 |
| `Invoke-RestMethod https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1` | 核对 CCDS 真正模板文件、Turing 模板实际目录、research-hub 的 `SKILL.md`／测试，以及 SMAIRT、autoresearch 缺少根许可证。 |
| 读取上游 raw README、SKILL、许可与关键 Python 文件 | [OpenRepro runner](https://github.com/SHENAO1/OpenRepro-Agent/blob/main/src/openrepro/experiment_runner.py)只执行其项目 `experiments/<id>/runner.py`，先要求 `--confirm` 并验证输入和 spec；不能直接替代现有课程 CLI。其 README 自称 alpha，且明确玩具运行不证明论文复现。 |
| 检查 README 所给地址与发布元数据 | SMAIRT 的 `cookiecutter gh:biodataganache/smairt-cookiecutter` 目标在核查时返回 GitHub 404；[OpenRepro 最新正式 release](https://api.github.com/repos/SHENAO1/OpenRepro-Agent/releases/latest) 为 v0.4.0，而 main 的 `pyproject.toml` 为 1.26.0，文档／发布版本不一致。 |

**未做的验证：**没有在本机运行 `ccds`、research-hub、OpenRepro、Snakemake、DVC 或其他候选；没有测量生成结果、运行成本、失败率或学习效果。仓库代码和 README 证明其设计和可检查入口，不证明它们在当前课程环境可用。若下一阶段要采用某项工具，先在隔离目录固定版本，执行最小真实任务，再与现有流程比较总时间、失败、输出质量和维护成本。

## 复用次序与引入触发条件

1. **现在：**以 The Turing Way 的问题／证据／反思章节和现有研究卡教学；将 research-hub 的设计与文献矩阵技能用于一轮有界试学。当前实验继续使用已存在的 CLI、独立 run、完整 trace 与人的解释。
2. **新仓库：**直接用 CCDS v2 起步，再加入课程特有的假设卡、轨迹复核和学习反思。SMAIRT 只作方法参照，直到安装入口和许可可核实。
3. **出现真实复杂度时：**多阶段部分重算用 Snakemake；大数据和模型版本用 DVC 或 DataLad；大量运行查询用 MLflow；对外交换机器可读证据包用 RO-Crate；正式冻结探索前设计用 OSF；统一可执行教材发布层可评估 Jupyter Book 或 Quarto。每项都应先有实际消费者，再引入依赖。

[OpenAI 官方技能文档](https://developers.openai.com/plugins/concepts/skills)将 skill 定义为复用流程指令与资源的层；[插件架构文档](https://developers.openai.com/plugins/concepts/plugins)建议在现有工具足够时从纯 skill 开始，需要外部服务连接或受控动作时再加 MCP。因此这里的优先方案是**复用现有教材、模板和技能，并让现有实验代码承担运行事实**；新插件首先组织这些来源和验收步骤，不另造实验运行时。
