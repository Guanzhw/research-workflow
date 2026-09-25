# Autoresearch 类方法的跨领域研究选型

核查日期：2026-09-26。本文面向“学习一个领域、动手实现、做可复核的小实验”的工作流，例如 Windows 上以 CPU 运行 MetaDrive 闭环练习；目标产物是问题、代码、完整轨迹与有边界的结论。以下依据项目原始仓库、原始技能文件和官方文档核查，尚未在本机安装或运行这些候选框架。项目 README 中的性能、成功率和费用是作者报告，不能视为本工作流的实测结果。

## 先确定共同的研究边界

一个可移植的循环应当是：**提出可证伪问题 → 冻结评估与预算 → 改一个受控因素 → 调用现有项目 CLI → 核对原始证据 → 记录保留、放弃或失败 → 确认运行 → 人工审查结论**。领域可以是驾驶、机器人、数据分析或模型训练；评估器、数据和终止语义必须由该领域的项目拥有，代理只在明示的可变范围内探索。CPU 可执行、有限轮次、完整失败记录比无人值守运行时长更适合目前的学习和工程实践。

## 原始项目逐项核查

| 项目 | 实际循环及可变／固定边界 | 前提、许可证与本场景取舍 |
|---|---|---|
| [karpathy/autoresearch](https://github.com/karpathy/autoresearch)／[program.md](https://github.com/karpathy/autoresearch/blob/master/program.md) | 人先确定范围；代理只改 `train.py`，不能改含数据准备、训练预算及 `evaluate_bpb` 的 `prepare.py`，也不能增依赖。每轮提交代码、运行 5 分钟训练，从 `run.log` 取 `val_bpb` 和显存，向 `results.tsv` 写 `keep`、`discard` 或 `crash`；坏结果回退，超过 10 分钟视为失败。原提示要求启动后持续循环，使用时应另设总预算。 | [README](https://github.com/karpathy/autoresearch#quick-start)要求单 NVIDIA GPU，标明在 H100 上测试；它是单训练任务、单主指标的实现，不能把训练代码搬到 CPU MetaDrive 闭环。可直接采用“可改文件白名单、固定评估器、每次尝试留痕”的方法。README 的 [License 小节](https://github.com/karpathy/autoresearch#license)写 MIT，但截至核查日[仓库文件树](https://api.github.com/repos/karpathy/autoresearch/git/trees/master?recursive=1)无 LICENSE/COPYING/NOTICE，GitHub [许可证元数据](https://api.github.com/repos/karpathy/autoresearch)为空；**不能据此认定代码复制或再分发已获清晰的 MIT 授权**。 |
| [Sakana AI Scientist v1](https://github.com/SakanaAI/AI-Scientist) | 以人工编写的 `experiment.py`、`plot.py`、`prompt.json` 和 LaTeX 模板限定领域；先在每台机器运行 `run_0` 基线，再做创意生成、文献新颖性查询、实验、论文及模型评审。基线对运行时间的比较有实际作用。 | [README Requirements](https://github.com/SakanaAI/AI-Scientist#requirements)明确设计目标为 Linux、NVIDIA CUDA/PyTorch，现有模板在纯 CPU 上可能耗时不可行，其他系统需较大调整；运行会执行模型生成代码，官方要求容器与网络限制。其[自定义 Source Code License](https://github.com/SakanaAI/AI-Scientist/blob/main/LICENSE)含使用限制及论文／报告 AI 披露要求。适合研究模板和论文生成，不适合直接接管当前原生 Windows CPU 课程。 |
| [Sakana AI Scientist v2](https://github.com/SakanaAI/AI-Scientist-v2) | 去掉 v1 的人工代码模板，以实验管理代理和渐进式树搜索生成、调试、选择实验；`bfts_config.yaml` 配置工作者、节点步数、种子及失败节点调试深度。它借用了 [AIDE](https://github.com/WecoAI/aideml) 的树搜索底座。 | [README](https://github.com/SakanaAI/AI-Scientist-v2#requirements)仍指定 Linux/CUDA；作者也明确写出：有强起始模板时 v1 可能成功率更高。官方示例给出主实验约 15–20 美元 API 费、写作约 5 美元、整个流程通常数小时；这是其所列模型与配置的估计，不是当前价格或本机实测。沿用 [AI Scientist 自定义许可](https://github.com/SakanaAI/AI-Scientist-v2/blob/main/LICENSE)和模型代码执行风险。可借“失败节点仍进入搜索树”的方法，不宜引入整套系统。 |
| [Agent Laboratory](https://github.com/SamuelSchmidgall/AgentLaboratory) | 文献综述、实验、报告三个阶段由专门代理协作；支持 Co-Pilot 模式和检查点恢复。研究者可在任务笔记中指定计算资源与实验要求。 | [README](https://github.com/SamuelSchmidgall/AgentLaboratory#installation)推荐 Python 3.12、模型 API；编译报告才需要可选 LaTeX。仓库有 [MIT LICENSE](https://github.com/SamuelSchmidgall/AgentLaboratory/blob/main/LICENSE)。阶段交接有参考价值，但完整框架不会自动继承本项目已冻结的轨迹指标和运行证据；目前无需替换现有 CLI。 |
| [OpenRepro-Agent](https://github.com/SHENAO1/OpenRepro-Agent) | 针对论文复现：摄取 PDF／文本、提取候选公式和参数，经人工批准后生成实验脚手架，再验证输入、显式运行、质量检查及打包证据。默认 mock provider，真实 API 须选择启用。 | [README](https://github.com/SHENAO1/OpenRepro-Agent#install)支持 Python 3.10+ 与 Windows PowerShell；有 [MIT LICENSE](https://github.com/SHENAO1/OpenRepro-Agent/blob/main/LICENSE)。作者把当前版本称为 alpha 工程脚手架，并明说玩具运行不证明论文已复现。若日后要逐条复现外部论文，可在**独立工作区**试点；把其整套目录移入四个已有练习会重复现有运行器。 |
| [AIDE ML](https://github.com/WecoAI/aideml) | 搜索树中的每个节点是一段候选 Python 代码；代理提出草案、调试或改进，执行后比较指标，并保存最佳代码与树图。步数、初始草案数可配置。[源码](https://github.com/WecoAI/aideml/blob/main/aide/agent.py)显示反馈模型可从运行输出报告数值与方向；因此应由外部固定评估器复算，而非让代理自报的指标成为最终证据。 | 提供 `pip install aideml`、模型 API 和本地兼容端点路径；仓库有 [MIT LICENSE](https://github.com/WecoAI/aideml/blob/main/LICENSE)。当某一 CPU 实验已收敛为可快速重复的**单目标**优化时可小规模试点；多指标闭环、安全约束及保留测试仍由原项目负责。未在 Windows/MetaDrive 上实测其安装和执行。 |
| [MLAgentBench](https://github.com/snap-stanford/MLAgentBench)／[ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench) | 两者主要是**评测代理**：MLAgentBench 将代理可见的 `env/` 与隐藏 `script/eval.py` 分开，保留代理状态、工具日志、工作区快照、时间和错误；ScienceAgentBench 从多个学科论文组织任务，评估生成程序、执行结果及成本，并在 2026-04-30 发布 verified split 以减少误判。 | MLAgentBench 提供 Python 3.10、Docker 和 Windows PowerShell 容器示例；两仓库均有 MIT LICENSE（[MLAgentBench](https://github.com/snap-stanford/MLAgentBench/blob/main/LICENSE)、[ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench/blob/main/LICENSE)）。借用“代理看不到答案、全部尝试可审计”和独立质量核查；不要把其任务或单一提升阈值当成本项目的驾驶评价标准。 |
| [OpenHands SDK](https://github.com/OpenHands/software-agent-sdk)／[代理架构文档](https://github.com/OpenHands/docs/blob/main/sdk/arch/agent.mdx) | 通用推理—行动循环：事件历史、工具调用、结果或错误事件、上下文压缩，以及执行前的安全分析／确认模式；每步可中断与恢复。 | SDK 有 [MIT LICENSE](https://github.com/OpenHands/software-agent-sdk/blob/main/LICENSE)。它能在代理数量、工具种类、长时恢复或独立沙箱成为真实需求时提供执行底座；它不定义科研问题、匹配种子、驾驶终止口径或证据解释。当前已有编码代理与项目 CLI 时，不必为四个单元先部署第二套代理平台。 |

补充：[SMAIRT 原始研究技能](https://raw.githubusercontent.com/PNNL-CompBio/smairt-template/main/skills/smairt-research/SKILL.md)描述“假设→脚本→日志→分析”，[论文驱动技能](https://raw.githubusercontent.com/PNNL-CompBio/smairt-template/main/skills/smairt-paper-driven/SKILL.md)强调新迭代不覆盖旧迭代。这些思想适合跨领域交接；但其 [README](https://github.com/PNNL-CompBio/smairt-template/blob/main/README.md)虽写 MIT，[仓库文件树](https://api.github.com/repos/PNNL-CompBio/smairt-template/git/trees/main?recursive=1)无许可证正文且 GitHub [许可证元数据](https://api.github.com/repos/PNNL-CompBio/smairt-template)为空，README 推荐的 [`biodataganache/smairt-cookiecutter`](https://api.github.com/repos/biodataganache/smairt-cookiecutter) 在核查日返回 404。因此只引用方法，不复制技能文件，也不把文档中的安装命令视为已验证可用。

## 建议的落地路径

1. **复用现有项目入口。** 教学仓库继续以 `research/studies/*.md`、`research/AGENT_PROTOCOL.md` 和 `scripts/run_research.py` 作为设计与执行入口。其他领域只需提供同等的“研究卡 + 现有 CLI + 解析原始证据的适配器”；不要求复制 MetaDrive 的文件结构。
2. **冻结评估边界。** 每轮开始前记录主要终点、护栏指标、配对种子／数据划分、预算、停止条件、允许修改的源码路径，以及评估器、环境配置和依赖的版本或哈希。候选代码不得改评估器、保留测试集或产物校验。评价口径改变时，新开设计版本并重跑基线。
3. **让代理做有限搜索。** 先试 2–3 个有预先解释的候选，每个候选用独立分支或工作树、同一 CLI 和匹配条件执行。每次运行均保留命令、代码状态、配置、标准输出／错误、退出码、耗时、资源、完整轨迹和部分产物。失败、重试、未改善及超预算尝试都写入 trial ledger，不只保留最好一次。ledger 至少含候选假设、可变文件、基线／候选 run ID、评价版本、数值、失败、总成本及 `keep/discard/retry` 理由。
4. **确认后才保留。** 从 trace 独立重算主要指标和终止类型；用预先规定的配对条件及护栏决定“暂时保留”，在未参与候选选择的种子／场景上做确认运行。若结果不稳、破坏安全指标或超预算，记录为放弃或未决。学习者与独立 Reviewer 审查因果解释、反例与适用范围后，再决定是否进入课程主线。
5. **按实际负载升级工具。** 只有当单目标、快速、重复的代码调参成为瓶颈，才在隔离环境中试接 AIDE 的候选搜索，并继续由固定 CLI 和 trace 适配器判定。只有当多代理工具执行、恢复、权限和沙箱管理明显超过现有编码代理能力，才评估 OpenHands SDK。论文复现另在 OpenRepro-Agent 工作区试点；跨学科代理性能声明可用 ScienceAgentBench 一类外部基准核查。

本次是源码／文档核查：**没有安装、运行、计时或安全测试任何外部候选**，也没有在 Windows CPU MetaDrive 上测量其正确率、总 token、失败重试或端到端成本。采纳前应先用一个已交付单元做小样本实测，并将准备成本与全部尝试计入比较。
