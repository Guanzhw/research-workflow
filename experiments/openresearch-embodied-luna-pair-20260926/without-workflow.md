# 从 Transformer 到具身智能：技术路线、动因与未解问题

**研究范围：** 2017—2026 年 9 月 26 日。本文以通用机器人操作与控制为主线，解释 Transformer 如何进入机器人系统，以及视觉语言行动模型、连续动作生成和世界模型为何相继出现。高层语言规划作为并行路线简述；机器人导航、自动驾驶、人形机器人全身控制、经典控制与硬件演进不作系统综述。文中对 2026 年新作均按预印本或早期研究看待。

## 核心判断

具身智能并非 Transformer 自然扩展后的单一路线。研究大致分成三类并逐渐融合：用语言模型组织既有感知模块和技能；直接从视觉与指令预测机器人动作；在动作策略之外学习环境动态，以预测动作后果。它们分别针对任务组合、数据与语义迁移、物理后果预测等不同瓶颈。

Transformer 提供了处理长序列与多模态输入的可扩展架构，但真正决定机器人能否落地的仍有数据覆盖、动作表达、实时推理、闭环纠错和真实环境评测。参数规模本身不会自动带来物理技能。

## 技术演进

### 1. Transformer：可并行的序列建模底座（2017）

Transformer 最初面向机器翻译等序列转换任务。论文指出，循环网络逐位置处理序列，训练样本内部难以并行；自注意力允许序列位置直接交互，并提高训练并行度。作者概括其出发点为：“This inherently sequential nature precludes parallelization within training examples.” [《Attention Is All You Need》原文](https://www.alphaxiv.org/pdf/1706.03762)

这解决的是序列建模和训练效率问题，为后来的语言模型、视觉语言模型以及机器人策略提供了统一的序列处理器。它本身并不理解机器人身体，也不把图像、自然语言和马达控制自动接到一起。标准全注意力的计算量随 token 数近似二次增长；**由此推得**，多相机、高分辨率视觉和较长历史会加重推理与显存压力。该复杂度是架构层面的约束，不是 2017 年论文对机器人系统的实测结论。

### 2. 模块组合与语言规划：先复用已有能力（2022 起）

大语言模型擅长处理指令与任务分解，视觉模型更擅长视觉输入，但这些模型通常没有机器人低层控制能力。模块式方案因此让预训练模型通过语言提示交换信息，再调用感知、数据库或机器人动作接口；这样可以组合现成能力，无须先收集大规模端到端机器人数据。《Socratic Models》把新任务表述为多个预训练模型与其他模块之间的语言交换，并展示机器人感知和规划用例。[《Socratic Models》原文](https://www.alphaxiv.org/pdf/2204.00598)

这一路线主要改善“听懂任务并编排已会技能”，可沿用现有控制器和动作库。限制在于，高层计划仍须由感知、技能接口和执行器落实；**推论：** 若语言描述的场景状态过时，或某项技能的前置条件不成立，模块之间的误差会传到执行端。它适合长程任务编排，却不等同于从相机画面直接学会连续操控。

### 3. 直接预测动作：从 RT-1 到 RT-2（2022—2023）

RT-1 把机器人示范转成可供 Transformer 学习的输入输出：视觉观测与自然语言指令进入模型，模型逐时刻输出机器人动作。它的 TokenLearner 等设计压缩视觉表示，目标是在多任务学习的同时满足在线控制速度。作者用 13 台机器人、约 17 个月收集约 13 万条示范，覆盖 700 多条任务指令；论文报告训练指令任务的成功率为 97%。这条路线针对两个现实问题：机器人数据远少于互联网文本/图像数据，而且机器人需要可闭环执行的低层动作，而不只是文本计划。[《RT-1: Robotics Transformer for Real-World Control at Scale》原文](https://www.alphaxiv.org/pdf/2212.06817)

RT-1 显示更广的真实机器人示范能支持多任务策略，但数据收集成本仍高，覆盖范围也依赖实验环境、物体和指令。它说明扩大模型之外，还必须扩大且组织好数据。

RT-2 接着把视觉语言模型的网络预训练带到机器人控制：模型同时学习机器人轨迹和视觉语言任务，并将动作表示为文本 token，让动作预测与语言生成共享接口。作者报告了对新物体、场景和指令的泛化提升；但也明确限定：“the model’s physical skills are still limited to the distribution of skills seen in the robot data.” 换言之，互联网视觉语言数据扩展语义知识，不能替代真实动作示范。较大的模型还带来部署代价：该研究最大的模型为 550 亿参数，依赖云端多 TPU 服务支持机器人闭环推理。[《RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control》原文](https://www.alphaxiv.org/pdf/2307.15818)

### 4. 跨机器人数据：从单一平台走向共享经验（2023）

RT-X / Open X-Embodiment 针对机器人数据按机构、任务和机型分散的问题，汇集并标准化多个实验室的数据。论文报告数据集覆盖 22 种机器人、21 家机构、527 种技能和 160,266 个任务；在多个机器人上训练的 RT-X 展示了跨平台经验带来的正迁移。[《Open X-Embodiment: Robotic Learning Datasets and RT-X Models》原文](https://www.alphaxiv.org/pdf/2310.08864)

这推进了“先在多种机器人数据上训练，再迁移到目标机器人”的路线，也让社区可以共享基准和训练材料。数据格式统一并不意味着机器人动作空间、相机视角、夹爪和动力学相同。**推论：** 跨具身迁移仍要处理本体差异、动作映射和数据质量差异；数据规模的提升不会自动抹去这些差异。

### 5. 连续动作生成：扩散与流匹配（2023—2025）

机器人动作是连续的，动作序列也可能有多种合理执行方式。Diffusion Policy 将视觉运动策略表示为条件去噪扩散过程，以表达多峰动作分布和高维动作序列；它加入 receding-horizon control，使机器人执行一段动作后重新观测、再规划。这条路线针对单一动作回归难以表达多种示范策略的问题，同时尝试兼顾动作连贯与闭环响应。[《Diffusion Policy: Visuomotor Policy Learning via Action Diffusion》原文](https://www.alphaxiv.org/pdf/2303.04137)

随后 π₀ 将预训练视觉语言模型与连续动作专家结合，用流匹配生成高频动作块。π₀ 的预训练混合包含来自 7 种机器人配置、68 项任务的约 10,000 小时灵巧操作数据，并进一步用高质量数据微调复杂多阶段任务。[《π₀: A Vision-Language-Action Flow Model for General Robot Control》原文](https://www.alphaxiv.org/pdf/2410.24164)

它试图同时保留视觉语言知识和细粒度的连续控制能力，适合折叠衣物、装盒等需要连贯动作的任务。代价是数据和训练流程更复杂，推理速度也需要与控制频率配合。作者指出：“our experiments do not yet provide a comprehensive understanding of how the pre-training datasets should be composed”；他们也说部分任务仍不稳定，跨操作领域的通用性尚待验证。因此，“能生成平滑动作”不等于已经获得稳定、可恢复的通用机器人能力。

### 6. 世界模型与动作联合建模：显式学习动作后果（至 2026）

直接策略通常从当前观测映射到动作；世界模型路线增加一个预测问题：给定当前状态和动作，预测环境后续会如何变化。它的动机是让系统学到一些动作与物理结果之间的关系，为计划、筛选动作或改进策略训练提供预测信号。

2026 年预印本 WorldDiT 展示了一种紧耦合形式：同一扩散 Transformer 生成连续动作块，并预测未来相机图像的 RGB patch。其预测目标用于训练；执行时模型只输出动作，每执行三个动作后重新观测和规划。作者在 LIBERO 的四个**仿真**套件上评测一个 3.99 亿参数配置，并将结果报告为参数量与平均成功率的 Pareto 前沿之一。[《WorldDiT: A Unified Diffusion Architecture for World and Action Modeling》原文](https://www.alphaxiv.org/pdf/2607.23909)

这代表了“动作 + 未来状态预测”的融合方向，但证据仍早：该论文明确把单一配置称为后续 scaling study 的基线；其结果来自仿真，而非真实机器人部署。**推论：** 预测图像逼真并不保证预测遵循可执行的物理约束；若模型用于规划，还需验证预测误差是否会导致错误动作，以及候选动作搜索的计算成本是否可接受。WorldDiT 的训练期图像预测本身也不应误读为已经实现了部署时的模型预测控制。

## 贯穿各阶段的限制

- **数据依然是硬瓶颈。** 机器人示范成本高，场景与动作覆盖有限；跨机器人汇集扩大了多样性，但不同本体与采集条件仍不一致。RT-1 和 π₀ 的数据规模及作者讨论都说明，数据组成和质量本身就是方法的一部分。
- **语义知识与物理技能不是同一件事。** RT-2 展示了从网络预训练获得的语义泛化，同时限定低层动作技能受机器人训练分布约束。
- **通用性需要以闭环和真实部署验证。** 模型必须在观测变化、接触误差和意外情况中持续纠错；公开结果常来自有限任务集或模拟器。WorldDiT 当前所报告的证据属于模拟操作基准。
- **算力和响应时间受约束。** Transformer 序列长度、生成式动作采样和大视觉语言骨干都会影响控制周期；RT-2 使用云端 TPU 服务，是扩大模型能力与机器人端资源之间张力的具体例子。
- **预测不是物理保证。** 世界模型能提供有用的未来状态信号，但图像预测指标、动作成功率与真实物理规律遵循程度并非同一个指标。后一句是基于模型目标与评测范围的判断，需要进一步实验验证。

## 结论

从 Transformer 开始的具身智能发展，关键不只是“把模型做大”，而是逐步补上序列模型通向现实行动所缺的环节：模块规划补任务编排，RT-1/RT-2 把模型接到动作并迁移语义知识，跨具身数据扩大经验覆盖，扩散/流匹配更直接地表示连续动作，世界模型则尝试补上对行动后果的显式预测。

截至 2026 年 9 月，较有把握的结论是这些组件开始形成可复用的技术栈；“单一模型能在开放世界中可靠完成任意任务”仍不是现有证据支持的结论。眼下最关键的研究问题是如何采集覆盖失败与恢复的数据、如何在异构本体间保持可执行动作，以及如何证明模型预测在真实交互中可靠。

## 证据范围与图示说明

报告优先使用原始研究论文，2026 年工作明确视为早期预印本。原计划裁切 RT-1 与 WorldDiT 的原论文图用于架构对照；当前会话无法取得 arXiv PDF 二进制文件（本机 HTTPS 下载遇到 Windows TLS 凭据错误，网页 PDF 获取超过工具大小上限），因此未内嵌裁图，也未用重绘替代。可在[RT-1 原文](https://www.alphaxiv.org/pdf/2212.06817)与[WorldDiT 原文](https://www.alphaxiv.org/pdf/2607.23909)查看论文图示。本文结论依据可读取的原论文全文与论文报告的评测范围。

## 主要原始来源

1. Vaswani et al., 2017. [Attention Is All You Need（arXiv:1706.03762）](https://www.alphaxiv.org/pdf/1706.03762)
2. Zeng et al., 2022. [Socratic Models: Composing Zero-Shot Multimodal Reasoning with Language（arXiv:2204.00598）](https://www.alphaxiv.org/pdf/2204.00598)
3. Brohan et al., 2022. [RT-1: Robotics Transformer for Real-World Control at Scale（arXiv:2212.06817）](https://www.alphaxiv.org/pdf/2212.06817)
4. Brohan et al., 2023. [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control（arXiv:2307.15818）](https://www.alphaxiv.org/pdf/2307.15818)
5. Open X-Embodiment Collaboration, 2023. [Open X-Embodiment: Robotic Learning Datasets and RT-X Models（arXiv:2310.08864）](https://www.alphaxiv.org/pdf/2310.08864)
6. Chi et al., 2023. [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion（arXiv:2303.04137）](https://www.alphaxiv.org/pdf/2303.04137)
7. Black et al., 2024 preprint / 2025 RSS. [π₀: A Vision-Language-Action Flow Model for General Robot Control（arXiv:2410.24164）](https://www.alphaxiv.org/pdf/2410.24164)
8. Wang et al., 2026 preprint. [WorldDiT: A Unified Diffusion Architecture for World and Action Modeling（arXiv:2607.23909）](https://www.alphaxiv.org/pdf/2607.23909)

