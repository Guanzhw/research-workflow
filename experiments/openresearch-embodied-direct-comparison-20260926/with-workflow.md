# 具身智能（Embodied Intelligence）发展脉络研究报告

**——从 Transformer 出发，梳理主要技术路线的因果演进**

> 报告语言：中文　|　信息检索截止：2026-09-26　|　来源以 arXiv / 顶会论文与综述的原始摘要为主，全部可核查。

---

## 0. 研究范围与取舍说明（Scope）

具身智能是一个跨度极大的交叉领域，从硬件本体（机械臂、足式、人形机器人）、感知（视觉/触觉/力觉）、规划、控制、到学习范式与数据生态，任何一条都无法在一份报告中穷尽。为保持"因果脉络"清晰、结论可核查，本报告做如下**明确取舍**：

1. **时间起点**：以 Transformer（2017）为锚点，往前只做必要的前史铺垫（概念起源、深度强化学习时代），不做完整回顾；往后延伸至 2026 年中的最新工作。
2. **技术主线**：聚焦"大模型 × 机器人"这一条核心主线，即**用大规模预训练（语言/视觉/多模态）模型来驱动具身智能**。这正好是 Transformer 之后才成为可能、也最能解释"为什么是现在"的那条线。
3. **子领域取舍**：以**机械臂操作（manipulation）**为最主要载体展开（因为它是 VLA/数据规模化争论的主战场），导航、自动驾驶、人形机器人整体控制作为并行路线在相应位置点到为止。
4. **不覆盖**：经典控制论、传统 SLAM/运动规划、具体的电机/减速器/传感器硬件工程、以及商业公司的产品细节（除非与某条技术路线直接相关）。
5. **证据等级**：所有"某某路线解决了某某瓶颈"的判断，都尽量落回对应论文的原文动机（abstract 中的问题陈述）；论文发表时间与"实际被广泛采用的时间"是两回事，报告中会分别标注，并明确区分**历史事实**与**我的解读**。

---

## 1. 摘要（TL;DR）

具身智能在 2017 年之后的发展，本质上是把 NLP/CV 里已被验证的"**预训练 + 规模化 + 通用底座**"范式，一步步搬进机器人。这一搬运过程沿着一条清晰的因果链展开：

- **Transformer（2017）**让序列建模可并行、可扩展 → 催生了大语言模型（LLM）与视觉 Transformer（ViT）→ 带来了"互联网规模预训练出的常识与语义"这一新资源。
- 第一个缺口是**语言不接地气**：LLM 能说"把苹果放进抽屉"，但不知道机器人此刻能不能做、怎么做。→ **SayCan**（2022）用"可负担性（affordance）+ 价值函数"给语言落地。
- 第二个缺口是**动作不是文本**：机器人输出的是连续关节量，不是 token。→ 先有 **Gato/RT-1**（2022）把动作 token 化；再有 **RT-2**（2023）把动作**写回文本 token**，直接共微调视觉语言模型，确立了 **VLA（Vision-Language-Action）**范式。
- 第三个缺口是**数据无法共享**：每个机器人、每个任务单独训练。→ **Open X-Embodiment / RT-X**（2023）标准化跨本体数据集，证明"跨机器人正迁移"；随后 **Octo / OpenVLA**（2024）把它开源化、可微调化。
- 第四个缺口是**动作生成的表达力**：离散 token + 自回归会损失精度、无法表达"同一状态多种正确动作"的多模态分布。→ **Diffusion Policy**（2023）引入扩散；随后 **flow matching（π₀）**、**双系统架构（GR00T N1）**成为主流动作头。
- 第五个缺口是**物理直觉与数据瓶颈**：真实数据稀缺、难以试错。→ **世界模型 / World Action Model**（2024–2026）用视频生成预测"动作的后果"，用于合成数据、评估与规划；**具身推理模型（Embodied Reasoning / EFM）**（2026）把空间推理内化进 VLM。
- 贯穿始终的**未被解决的问题**：数据稀缺与"具身数据金字塔"、跨本体鸿沟（embodiment gap）、分布外泛化、长程任务与记忆、推理延迟与实时控制、以及安全。

一句话：**从"给语言落地"到"把动作 token 化"到"共享数据"到"生成式动作"到"世界模型与具身推理"，每一步都是对上一步暴露出的瓶颈的直接回应。**

---

## 2. 背景与前史（Transformer 之前，简述）

"具身智能"（Embodied Intelligence / Embodied AI）作为理念远早于 Transformer。罗德尼·布鲁克斯（Rodney Brooks）在 1986 年《Intelligence without Representation》与 1991 年《Intelligence without Reason》中提出：智能不应是脱离身体的符号推理，而应来自身体与物理环境的持续交互。这是今天"具身"一词的思想源头，也是本报告前史部分唯一需要记住的坐标点。

随后三十年的主流路线是**模块化 + 深度强化学习（DRL）**：感知、规划、控制各自独立，策略用 RL 在仿真中训练（如 2016–2018 年的抓取、灵巧手工作）。这套范式的根本瓶颈是**每换一个任务/本体/环境就要重训一次，且真实世界数据采集极其昂贵**——这恰恰是后面每一条新路线试图打破的东西。

**Transformer（2017）**：Vaswani et al. *Attention Is All You Need*（arXiv:1706.03762）。它用自注意力替代循环结构，带来两个决定性属性：**可并行训练**与**随规模近乎单调提升的能力**。正是这两点，让"用海量互联网数据预训练一个通用底座"从幻想变成工程现实。

由此催生的两个关键后果：
- **大语言模型**：GPT（2018）→ GPT-3（2020，arXiv:2005.14165）展现出"少样本/涌现式常识与推理"；
- **视觉 Transformer**：ViT（2020，arXiv:2010.11929）把同一套架构搬到图像，为后来的多模态（视觉-语言）模型铺路。

> 关键理解：Transformer 本身不是"具身"技术，但它制造了一个**新资源**——"从互联网预训练出来的常识、语义、世界知识"。具身智能随后五年的全部故事，都是围绕"**如何把这个新资源接进物理世界**"展开的。

---

## 3. 因果演化总览（Causal Map）

| 节点与时间 | 此前的瓶颈 / 约束 | 新机制 | 带来什么 / 代价 / 并存的旧路线 | 关键证据 |
|---|---|---|---|---|
| Transformer（2017） | RNN/LSTM 长序列难并行、难扩展 | 自注意力 + 并行 + 可扩展 | 规模化预训练成为可能；代价是计算需求大 | arXiv:1706.03762 |
| LLM / ViT（2018–2020） | 语言与视觉各自为战，无统一底座 | 大规模自监督预训练 | 产生"常识/语义"新资源 | arXiv:2005.14165；arXiv:2010.11929 |
| SayCan（2022） | LLM 输出文本动作，不落地、不知可行性 | LLM 打分 × affordance/价值函数打分 | 让语言可执行；代价是依赖手工技能库、底层仍需 RL | arXiv:2204.01691 |
| Gato / RT-1（2022） | 动作非文本，无法进 Transformer | 动作 token 化 + 高容量架构 | 证明通用策略可扩展；单任务仍不如专家 | arXiv:2205.06175；arXiv:2212.06817 |
| RT-2（2023） | 机器人数据少，需借用网络知识 | 动作写成文本 token，共微调 VLM（**VLA 范式**） | 涌现语义推理；代价是闭源、离散化、延迟 | arXiv:2307.15818 |
| Open X-Embodiment / RT-X（2023） | 每机器人单独训练，数据孤岛 | 跨 22 机器人标准化数据集 + 通用策略 | 证明跨本体正迁移；代价是需统一数据格式 | arXiv:2310.08864 |
| Octo / OpenVLA（2024） | VLA 闭源、难复现、难微调 | 开源 7B VLA + LoRA 微调 | 预训练+微调范式落地；代价是性能/算力门槛 | arXiv:2405.12213；arXiv:2406.09246 |
| Diffusion Policy（2023） | 离散 token 损失精度、无法表达多模态动作 | 动作=条件去噪扩散过程 | 处理多模态/高维动作、训练稳；代价是迭代采样慢 | arXiv:2303.04137 |
| π₀ / GR00T N1（2024–2025） | 扩散慢、需端到端统一 | flow matching + 双系统（VLM 推理 + 扩散动作） | 更快采样 + 人形机器人落地 | arXiv:2410.24164；arXiv:2503.14734 |
| 世界模型 / WAM（2024–2026） | 真实数据稀缺、缺物理直觉 | 动作条件视频生成预测未来 | 合成数据/评估/规划；代价是幻觉、物理不保真 | arXiv:2606.17030 等 |
| 具身推理 / EFM（2026） | VLA 只学动作，不学"为什么" | 把空间/任务推理内化进 VLM | 更强指令遵循与长程任务；尚在早期 | arXiv:2606.11324 等 |

> **解读（非事实）**：这张表里的"因果箭头"多数是"新方法直接回应了上一行的明确瓶颈"，但也存在**并行演进**（扩散动作头与自回归 VLA 长期并存）与**混合**（GR00T N1 = VLA 推理 + 扩散动作）。不能把这张表读成"后一个取代了前一个"的单线叙事。

---

## 4. 六条主要技术路线的详细分析

### 路线一：把语言"接上"物理世界（LLM 规划器）

**为什么出现？** Transformer 之后的 LLM 有了常识和语言理解，但存在一个尖锐的 gap：模型输出的"动作"只是文本（"打开抽屉"），它**既不知道这个动作在当前场景里是否物理可行，也不知道机器人有没有这个技能**。纯粹的 LLM 规划会生成不可执行的计划。

**解决了什么？** **SayCan**（Ahn et al., 2022，arXiv:2204.01691，CoRL 2022）提出"**Do As I Can, Not As I Say**"：每一步候选技能，同时用 LLM 给一个"语义合适度"打分、用基于 RL 的价值函数/可负担性（affordance）给一个"当前可行性"打分，两者相乘选出既合理又可执行的技能。这是"语言落地（grounding）"的标志性方案。

**带来什么 / 代价？** 它把 LLM 变成了可执行规划器的"大脑"，但代价明显：**技能必须是预先定义好的离散集合**（本质是"从技能库里挑"，不能创造新动作），底层执行仍依赖手工训练或 RL 的专用技能。后续工作（如 Code as Policies，2022；PaLM-E，2023）逐步把规划能力内化进多模态模型，减少对手工技能库的依赖。

**并存的旧路线**：传统 Task-and-Motion Planning（TAMP）在结构化、几何约束精确的场景里仍然有效，两者长期并存——TAMP 保证几何/运动学可行性，LLM 负责语义/常识层面。

**证据**：SayCan 论文（arXiv:2204.01691）；其问题陈述在后续大量论文中被反复引用为"语言不落地"的代表性困境（如 ConceptBot、AutoGPT+P 等 2025 年工作仍以其为对照基线）。

---

### 路线二：把动作 token 化——通用智能体与机器人 Transformer

**为什么出现？** 上一路线的瓶颈是"动作不是文本、进不了序列模型"。要把整个"感知→决策→动作"塞进同一个 Transformer，就必须把**连续动作离散化、token 化**，与图像、语言放在同一个序列里。

**解决了什么？** 两步走：
- **Gato**（Reed et al., 2022，arXiv:2205.06175，DeepMind）：把文本、图像、Atari 按键、关节力矩全部 token 化，**同一套权重**做多模态、多任务、多本体策略。价值在于**概念验证**——证明"通用策略"这条路走得通。
- **RT-1**（Brohan et al., 2022，arXiv:2212.06817，Google）：**Robotics Transformer**，在 13 万条真实机器人演示上训练，系统研究了模型/数据/多样性三者对泛化的影响，第一次给出机器人领域的"规模化"证据：高容量架构能吸收大规模异构机器人数据。

**带来什么 / 代价？** 确立了"**机器人数据 + Transformer = 可扩展通用策略**"的可行性。代价：这类早期模型**每个任务仍不如专用专家**，且动作离散化会损失控制精度。

**证据**：Gato（arXiv:2205.06175）原文自称"multi-modal, multi-task, multi-embodiment generalist policy"；RT-1（arXiv:2212.06817）摘要明确论证"open-ended task-agnostic training + high-capacity architectures"是泛化的关键。

---

### 路线三：VLA 范式——把网络知识写进动作（RT-2）

**为什么出现？** 机器人真实数据稀缺，但互联网上的语言/视觉数据近乎无限。问题变成：**能不能让"预训练在网络数据上"的模型，直接把学到的知识用于机器人控制？**

**解决了什么？** **RT-2**（Brohan et al., 2023，arXiv:2307.15818）给出了一个极简而关键的配方：**把动作表示成文本 token，直接混进 VLM 的训练集里**，和自然语言 token 一视同仁地共微调。于是"视觉-语言-动作"（Vision-Language-Action，**VLA**）这个类别正式诞生。结果是涌现能力：能识别训练数据里没见过的物体、理解"放到数字 3 上"这类抽象指令、甚至做"挑一个能当锤子的石头"这种多步语义推理（配合思维链）。

**带来什么 / 代价？** VLA 成为此后三年机器人学习的主范式。代价：RT-2 本身**闭源**、基于 PaLI-X/PaLM-E 这类超大模型、动作离散化、推理有延迟。这些代价正好是下一条路线的起点。

**证据**：RT-2 摘要（arXiv:2307.15818）原文："we express the actions as text tokens and incorporate them directly into the training set… We refer to such category of models as vision-language-action models (VLA)"。这是"VLA"一词的来源出处。

---

### 路线四：数据规模化与跨本体共享（Open X-Embodiment → Octo / OpenVLA）

**为什么出现？** 直接回应 VLA 时代暴露的两个代价：**① 数据孤岛**（每个机器人/任务单独训，无法互相借力）；**② 闭源不可复现**（RT-2 无法被社区使用和微调）。

**解决了什么？**
- **Open X-Embodiment / RT-X**（Open X-Embodiment Collaboration, 2023，arXiv:2310.08864）：联合 **21 家机构、22 种机器人、527 个技能、16 万任务**，统一数据格式，训练 **RT-X** 通用策略，**首次系统证明"跨机器人正迁移"**——把别的平台的经验搬过来能提升本平台能力。
- **Octo**（2024，arXiv:2405.12213）：800k 轨迹的**开源**通用策略，支持语言或目标图像指令，能在消费级 GPU 上几小时内微调到新传感/新动作空间。
- **OpenVLA**（Kim et al., 2024，arXiv:2406.09246）：**7B 开源 VLA**（Llama 2 + DINOv2/SigLIP 视觉编码器），970k 演示训练，**用 1/7 的参数（55B → 7B）在 29 个任务上比闭源的 RT-2-X 高 16.5%**；并验证了 LoRA 微调 + 量化可在消费级 GPU 上运行。

**带来什么 / 代价？** 把机器人学习从"每个任务从零训练"推进到"**预训练 + 轻量微调**"的范式，与 NLP/CV 的 consolidation 对齐。代价：数据仍需人工收集、跨本体对齐仍有工程成本、开源模型的绝对性能与延迟仍是问题。

**证据**：三篇论文摘要均明确陈述上述动机与数字（RT-X 的 22 robots/527 skills/160266 tasks；OpenVLA 的 16.5% / 7× fewer parameters / 970k demonstrations）。

---

### 路线五：动作生成范式——从离散自回归到扩散 / 流匹配

**为什么出现？** VLA 把动作离散成 token、自回归生成，带来三个深层问题：**① 离散化损失控制精度**（2026 年的 M²Tok、ActionPiece 等工作仍在专门处理这个"discretization bottleneck"）；**② 自回归误差累积**；**③ 无法表达"同一个状态下存在多种都正确的动作"（多模态动作分布）**——回归/单高斯假设会塌缩到平均，导致抓取这类多解任务失败。

**解决了什么？**
- **Diffusion Policy**（Chi et al., 2023，arXiv:2303.04137，Columbia/Toyota）：把策略表示为**条件去噪扩散过程**，在 12 个任务、4 个基准上平均比 SOTA 提升 **46.9%**。核心优势：天然处理多模态动作分布、适合高维动作空间、训练稳定（配合 receding-horizon、视觉条件化、时间序列扩散 Transformer）。
- 后续用**流匹配（flow matching）**替代扩散以加快采样：**π₀**（Physical Intelligence, 2024，arXiv:2410.24164）即"视觉-语言-动作流模型"。
- **GR00T N1**（NVIDIA, 2025，arXiv:2503.14734）：把两种思想合流——**System 2（VLM 推理）+ System 1（扩散 Transformer 生成动作）**双系统、端到端联合训练，专攻人形机器人，用真实轨迹 + 人类视频 + 合成数据混合训练。

**带来什么 / 代价？** 扩散/流匹配成为当代 VLA 的**主流动作头**。代价：**迭代采样带来推理延迟**，与实时高频控制冲突。这正是 2026 年一大波工作的目标——单步生成（IMLE-VLA，把 π₀.5 的推理频率从 15Hz 提到 55Hz）、蒸馏与量化加速（FoldQuantVLA 用 W4A4）、轻量架构（TurboVLA 32Hz / <1GB 显存）。这些工作本身说明"**延迟**"已成为当前最现实的瓶颈之一。

**证据**：Diffusion Policy 摘要（arXiv:2303.04137）明确列出"multimodal action distributions / high-dimensional action spaces / training stability"三大优势与 46.9% 数字；GR00T N1（arXiv:2503.14734）明确其 dual-system 架构。

---

### 路线六：世界模型、具身推理与"具身基础模型"（2024–2026，当前前沿）

**为什么出现？** 前几条路线解决了"怎么动"，但还有两个根本缺口：**① 物理直觉缺失**——模型不理解"我的动作会导致什么后果"；**② 真实数据瓶颈**——采集真实演示昂贵，仿真与现实有 gap。此外，VLA 只学会"从观察到动作"的映射，没有显式的任务推理与空间推理能力。

**解决了什么？（三条并行子路线）**
1. **世界模型 / World Action Model（WAM）**：用**动作条件的视频生成**预测"未来的视觉状态"，从而（a）合成训练数据、（b）在想象中评估策略、（c）提供规划信号。代表如 Qwen-RobotWorld（2026，arXiv:2606.17030，语言条件视频世界模型）、Riemann-1.0（2026，"causal autoregressive World Action Model"，同时可作策略与多本体仿真器）、CLAP（跨本体视频世界模型）。
2. **具身推理模型（Embodied Reasoning / EFM）**：把空间推理、任务分解、纠错、指向（pointing）内化进 VLM，使模型"理解为什么这么做"。代表如 Embodied-R1.5（2026，arXiv:2606.11324，8B 参数在 24 个具身 VLM 基准的 16 个上 SOTA，Planner-Grounder-Corrector 闭环）、Capek 0.5（执行中心的能力分类法）、LightNav-0（把 VLM 的空间智能直接用于导航）。
3. **数据合成与跨本体**：把人类自我中心视频（egocentric video）通过"具身对齐"变成机器人可用的监督（如 HumanEgo、AtomEgo），以及统一的"具身数据金字塔"框架（Data Pyramid survey，arXiv:2607.24744）。

**带来什么 / 代价？** 这是 2026 年最活跃、也最未收敛的方向。代价与风险同样突出：**世界模型的"幻觉"**（生成的未来在物理上不保真，会误导策略学习）、**评估基准混乱**、**跨本体对齐仍无统一标准**。一篇 2026 年的综述（*A Comprehensive Review of Generative Physical AI*，arXiv:2609.18111）用五分类来概括当代格局：RFM（跨平台技能迁移）、VLA（端到端感知控制）、LBM（类人运动生成）、DPM（扩散策略）、WFM（世界基础模型）。

**证据**：上述论文摘要均明确其动机与贡献；"Toward Unified Robot Learning"综述（arXiv:2609.03927）把当代方法组织为"representation learning（理解）/ VLA（行动）/ world models（推理）"三轴，并指出"这些范式各自孤立发展"是当前碎片化的根源。

---

## 5. 仍面临的核心限制（贯穿各路线）

以下限制是**跨路线、至今未解决**的，也是当前研究最集中的开放问题（每条都附可核查来源）：

1. **数据稀缺与"具身数据金字塔"**：真实机器人数据最贵、最稀缺，往下依次是 UMI 手持采集、自我中心视频、仿真、通用视觉-语言数据——越往上越"对齐"但越难规模化，越往下越易规模化但越"不对齐"。这一张力是所有数据策略的底层约束（*Data Pyramid for Embodied Manipulation*，arXiv:2607.24744）。

2. **具身鸿沟（Embodiment Gap）**：一个模型"能泛化"不等于"能在某种新身体上跑起来"。跨本体的可复用部分（语义、感知、接口）与必须逐台重做的部分（动作空间、运动学、动力学）之间，存在难以量化的鸿沟，且成功率指标掩盖了实际的适配工作量（*The Embodiment Gap in Robot Foundation Models*，arXiv:2608.18433）。

3. **分布外（OOD）泛化有限**：VLA 的空间能力主要来自示范，超出示范覆盖的姿态/布局/光照范围就不可靠（如 SAVLA 摘要指出"仅在示范覆盖的姿态范围内可靠"，旋转后成功率从 41.5% 到 90.4% 的对比）。

4. **长程任务与记忆**：现有 VLA 通常在"当前观察基本决定下一步"的短程设定下评测；需要"记住已消失信息"的历史依赖任务上表现骤降（MEMOBench，arXiv:2609.07047 显示最强记忆基线平均成功率仅 31.9%）。

5. **推理延迟与实时控制**：扩散/流匹配的迭代采样与 VLM 的大参数量，导致推理延迟与高频闭环控制冲突。2026 年大量工作（IMLE-VLA 单步生成、TurboVLA 轻量化、FoldQuantVLA 量化）都以此为目标，说明这是当前工程上的第一瓶颈。

6. **安全（Embodied AI Safety）**：通用机器人带来的风险远超传统的碰撞/力安全，涉及语境、用户意图、难以建模的物理后果（如"漂白剂+氨水"），且"比特的安全"与"原子的安全"不可分割（*Rethinking Safety for Generalist Robots*，arXiv:2609.06326）。多个基准（SafeStage、ManiGuard）都发现"任务成功"与"安全"经常脱钩：6–21% 的"成功"回放其实违反了安全规约。

7. **评估基准不统一 / sim-to-real 不一致**：仿真评测与真机结果的相关性长期存疑，最新工作（X2Real，arXiv:2609.27449）试图用校准后的仿真达到 0.84 的线性相关，说明此前基准的忠实度不足。

---

## 6. 可核查公开来源清单（按时间）

> 所有 arXiv 链接均可直接打开核对。带 ✓ 者为本次检索中直接取得原始摘要的论文；其余为领域内公认的原始出处（ID 为规范编号，可点击验证）。

### 奠基
- **Transformer**：Vaswani et al., *Attention Is All You Need*, 2017. https://arxiv.org/abs/1706.03762
- **GPT-3**：Brown et al., *Language Models are Few-Shot Learners*, 2020. https://arxiv.org/abs/2005.14165
- **ViT**：Dosovitskiy et al., *An Image is Worth 16×16 Words*, 2020. https://arxiv.org/abs/2010.11929

### 语言落地 / 通用策略
- **SayCan**：Ahn et al., *Do As I Can, Not As I Say: Grounding Language in Robotic Affordances*, 2022. https://arxiv.org/abs/2204.01691
- **Gato** ✓：Reed et al., *A Generalist Agent*, 2022. https://arxiv.org/abs/2205.06175
- **RT-1** ✓：Brohan et al., *RT-1: Robotics Transformer for Real-World Control at Scale*, 2022. https://arxiv.org/abs/2212.06817

### VLA 与数据规模化
- **RT-2** ✓：Brohan et al., *RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control*, 2023. https://arxiv.org/abs/2307.15818
- **PaLM-E** ✓：Driess et al., *PaLM-E: An Embodied Multimodal Language Model*, 2023. https://arxiv.org/abs/2303.03378
- **Open X-Embodiment / RT-X** ✓：Open X-Embodiment Collaboration, 2023. https://arxiv.org/abs/2310.08864
- **Octo** ✓：Octo Model Team, *Octo: An Open-Source Generalist Robot Policy*, 2024. https://arxiv.org/abs/2405.12213
- **OpenVLA** ✓：Kim et al., *OpenVLA: An Open-Source Vision-Language-Action Model*, 2024. https://arxiv.org/abs/2406.09246

### 动作生成范式
- **Diffusion Policy** ✓：Chi et al., *Visuomotor Policy Learning via Action Diffusion*, 2023. https://arxiv.org/abs/2303.04137
- **π₀**：Black et al., *π₀: A Vision-Language-Action Flow Model for General Robot Control*, 2024. https://arxiv.org/abs/2410.24164
- **GR00T N1** ✓：NVIDIA, *GR00T N1: An Open Foundation Model for Generalist Humanoid Robots*, 2025. https://arxiv.org/abs/2503.14734

### 世界模型 / 具身推理 / 前沿（2026）
- **Qwen-VLA** ✓：Qwen Team, 2026. https://arxiv.org/abs/2605.30280
- **Qwen-RobotWorld** ✓：Qwen Team, 2026. https://arxiv.org/abs/2606.17030
- **Embodied-R1.5** ✓：Yuan et al., 2026. https://arxiv.org/abs/2606.11324
- **Riemann-1.0** ✓（World Action Model）：2026. https://arxiv.org/abs/2608.27033
- **IMLE-VLA** ✓（单步动作生成/延迟）：2026. https://arxiv.org/abs/2609.10915
- **TurboVLA** ✓（轻量实时 VLA）：2026. https://arxiv.org/abs/2607.27205

### 综述 / 批判性来源（用于佐证"限制"与"格局"）
- **Data Pyramid for Embodied Manipulation** ✓：2026. https://arxiv.org/abs/2607.24744
- **The Embodiment Gap in Robot Foundation Models** ✓：2026. https://arxiv.org/abs/2608.18433
- **Toward Unified Robot Learning** ✓：2026. https://arxiv.org/abs/2609.03927
- **A Comprehensive Review of Generative Physical AI** ✓：2026. https://arxiv.org/abs/2609.18111
- **Rethinking Safety for Generalist Robots** ✓：2026. https://arxiv.org/abs/2609.06326

---

## 7. 不确定性与历史解释说明

1. **"为什么出现"是因果推断，不全是论文自述**：本报告把每条路线解释为"对上一步瓶颈的回应"，这是对论文动机（abstract 的问题陈述）的归纳，属于**历史解释**，而非严格可验证的因果实验结论。论文间的先后关系不必然等于因果关系。

2. **发表时间 ≠ 采用时间**：例如"VLA"作为术语由 RT-2 提出，但其思想（动作 token 化进 VLM）与 PaLM-E、Gato 有延续关系；Diffusion Policy 与自回归 VLA 长期**并存**，并非后者取代前者。报告中已把"并存的旧路线"单独列出。

3. **检索时间窗口的影响**：本次检索（2026-09-26）返回了大量 2026 年中的工作，可能**高估了"世界模型/具身推理"在当前学术生态中的占比**（新论文检索可见度天然更高）。真实产业落地进度通常慢于论文节奏。

4. **未覆盖的重要方向**：触觉/力觉融合（DeCAL、ForceU-VLA）、灵巧手、仿人全身控制（X-WBC）、多机器人协作（Embodied Collective Intelligence）、以及自动驾驶场景的 VLA 等，本报告因篇幅取舍未展开，它们与主线共享大部分底层范式。

5. **商业/产业数据未纳入证据链**：人形机器人公司（Tesla Optimus、Figure、Unitree 等）的产品与量产进度属于产业信息，本报告未将其作为技术路线的证据来源，避免把"融资/发布"与"技术成立"混为一谈。

---

*报告完。如需就某条路线（如 VLA 架构细节、世界模型、或数据策略）继续深入，或在某条"限制"上展开成专题，可在此基础上进一步检索与拆解。*
