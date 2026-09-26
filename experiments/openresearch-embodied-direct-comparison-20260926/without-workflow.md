# 具身智能发展脉络研究报告：从 Transformer 到通用机器人基础模型

> 本报告追溯具身智能（embodied AI）自 Transformer 架构引入后的主要技术路线，解释每条路线**为什么出现**、**解决了什么问题**、**仍面临哪些限制**，并在文末附可核查的公开来源（arXiv / alphaXiv 链接）。所有结论均基于原始论文摘要与全文的核对，未核对处会明确标注。

---

## 0. 摘要与范围说明

**一句话脉络**：Transformer 把"序列建模"变成了通用接口；具身智能的研究者沿这条主线，先尝试把"决策"本身当作序列（Decision Transformer / Gato），再尝试给大模型"接上身体"（SayCan / PaLM-E），随后用互联网视频补足数据（VPT），最后收敛到两条至今仍在竞合的主线——**视觉-语言-动作（VLA）模型**（RT-1 → RT-2 → OpenVLA/Octo → π0）与**世界模型 / 生成式交互环境**（Genie 等）。当前（2026）的前沿是"大规模、跨本体、世界模型闭环"的通用机器人基础模型。

**范围取舍（应你要求说明）**：
1. **起点定为 Transformer（Vaswani et al., 2017, "Attention Is All You Need"）**，因此不含更早的经典控制 / 传统模仿学习脉络，只在其作为"被替代对象"出现时提及。
2. 重点放在**机器人操作（manipulation）与通用策略**这条主线；自动驾驶、四足/人形运动控制等专门领域只作旁注。
3. 每条路线选取**奠基性、可核查**的代表作（论文，而非博客或产品宣称）。2026 年的最新工作仅用于说明"当前限制与走向"，不作为已被广泛验证的结论。
4. 本报告是**综述性研究报告**，非学术论文；图表可从各链接直接查阅原始论文，未做二次绘制。

---

## 1. 起点：Transformer 与"序列建模即一切"

Vaswani 等人在 2017 年提出的 Transformer 引入了自注意力机制，使得模型可以并行地、以统一方式处理任意长度的 token 序列。这一架构随后在 GPT、BERT 等语言模型中被证明具有极强的**可扩展性**（scalability）：只要把问题表示成"预测下一个 token"，数据量和参数量就能近乎单调地转化为能力提升。

对具身智能而言，Transformer 的关键意义不是某个具体算法，而是确立了一个**范式**：*把原本需要专门设计的模块（感知、规划、控制）统一成一个"序列到序列"的预测问题*。这成为后续所有技术路线的共同底层假设。

> 本报告以 Transformer 为起点，但需说明：Transformer 本身不解决"机器人数据从哪来""如何接地到物理世界"等具身智能的核心难题，这些正是后续各条路线要依次攻克的。

**来源**：Vaswani et al., *Attention Is All You Need*, 2017. https://arxiv.org/abs/1706.03762

---

## 2. 技术路线一：把"决策"做成序列建模（Decision Transformer → Gato）

**为什么出现**：传统强化学习（RL）依赖拟合价值函数或计算策略梯度，样本效率低、对稀疏奖励敏感。既然 Transformer 在语言上证明了序列建模的威力，一个自然的问题是：*能否干脆把强化学习也变成"条件序列生成"，从而复用 Transformer 的可扩展性？*

**解决了什么**：
- **Decision Transformer（2021）** 把 RL 抽象为条件序列建模：用一个因果掩码的 Transformer，输入"期望回报（return）+ 过去状态 + 过去动作"，直接输出未来动作。作者原文："Unlike prior approaches to RL that fit value functions or compute policy gradients, Decision Transformer simply outputs the optimal actions by leveraging a causally masked Transformer."（不像以往拟合价值函数或算策略梯度的方法，Decision Transformer 仅靠一个因果掩码 Transformer 直接输出最优动作。）它在 Atari、OpenAI Gym 上达到或超过当时的无模型离线 RL 基线，且更简单、更稳定。
- **Gato（2022）** 把这一思想推向极致：*同一个网络、同一组权重*，既能玩 Atari、给图片配字幕、聊天，也能控制真实机械臂堆方块，按上下文决定输出文本、关节力矩还是按键 token。这确立了"多模态、多任务、多本体通用策略"的雏形。

**限制**：
- 两者本质上仍是**离线 / 演示驱动**：Decision Transformer 依赖已有数据集的条件生成，不与环境交互，泛化到分布外状态困难；Gato 的"通用"更接近"多任务模仿"，未证明能在新任务上自主探索。
- 都没有解决**物理世界的接地（grounding）**问题——它们把动作当 token，但"这个 token 对应现实世界里的什么动作、能不能执行"仍悬而未决。

**来源**：
- Chen et al., *Decision Transformer: Reinforcement Learning via Sequence Modeling*, 2021. https://www.alphaxiv.org/abs/2106.01345
- Reed et al., *A Generalist Agent* (Gato), 2022. https://www.alphaxiv.org/abs/2205.06175

---

## 3. 技术路线二：给大语言模型"接上身体"——语义接地（SayCan → PaLM-E）

**为什么出现**：大语言模型（LLM）里编码了大量关于世界的语义知识（比如"怎么清理洒出的液体"），但这些知识**没有经历过真实世界**，给出的回答未必适用于特定机器人、特定环境。直接的"LLM 输出动作"会在物理上不可行。

**解决了什么**：
- **SayCan（2022）** 提出用**预训练技能的价值函数**做接地：LLM 只负责在"高层次语义"上提议下一步做什么，而每个候选技能的可执行性（affordance）由一个价值函数打分，两者结合决定真实动作。作者原文："The robot can act as the language model's 'hands and eyes,' while the language model supplies high-level semantic knowledge about the task."（机器人充当语言模型的"手和眼"，语言模型提供关于任务的高层语义知识。）这使得移动操作机器人能够完成长时程、抽象的自然语言指令。
- **PaLM-E（2023）** 进一步提出"具身语言模型"：把视觉、连续状态估计、文本等**多模态句子**直接端到端地接进预训练大模型，在机器人规划、视觉问答、字幕等多个具身任务上联合训练，并观察到**正向迁移**——跨互联网规模的语言、视觉、视觉-语言数据联合训练能让单一模型受益。最大版本 PaLM-E-562B 同时还是视觉-语言通才。

**限制**：
- SayCan 的"技能"仍是**预定义、离散**的，不能生成全新的低层动作；语言模型与低层控制仍是两段式，语义与执行之间存在"接缝"。
- PaLM-E 参数量巨大（最高 562B），推理成本高，且这种"把感知塞进 LLM"的路径后来被更简洁的 VLA 路线（见第 5 节）取代或融合。

**来源**：
- Ahn et al., *Do As I Can, Not As I Say: Grounding Language in Robotic Affordances* (SayCan), 2022. https://www.alphaxiv.org/abs/2204.01691
- Driess et al., *PaLM-E: An Embodied Multimodal Language Model*, 2023. https://www.alphaxiv.org/abs/2303.03378

---

## 4. 技术路线三：从互联网视频学"行为先验"（VPT）

**为什么出现**：机器人、游戏等序贯决策领域**缺乏带标签的行为数据**——互联网上有海量视频，但没有"每个画面当时按下了什么键/施加了什么力矩"的标签。文本/图像可以大规模预训练，行为先验却不行。

**解决了什么**：
- **VPT（Video PreTraining，2022）** 用**半监督模仿学习**破局：先用少量带标签数据训练一个**逆动力学模型（IDM）**，让它的预测精度足以"回填"海量无标签互联网视频的动作标签（这里用的是人类玩 Minecraft 的键鼠操作视频），再在这些自动标注数据上训练通用行为先验。
- 成果：该行为先验有非平凡的**零样本**能力，并且可以用模仿学习 + 强化学习微调到"从零靠 RL 根本学不会"的困难探索任务；作者报告"首次训练出能制作钻石工具的智能体，而熟练人类完成此任务需约 20 分钟（24,000 步环境动作）"。

**限制**：
- 依赖一个**足够准的 IDM** 来给视频打动作标签，标签噪声会向上游传播。
- 训练在**人类原始交互界面**（20Hz 键鼠）上进行，与现实机器人/不同本体之间存在**跨本体鸿沟**，不能直接迁移到物理操作。
- 它是"数据管线"的突破，而非"架构"的突破；其价值更多体现在后续被世界模型与视频-动作模型吸收。

**来源**：Baker et al., *Video PreTraining (VPT): Learning to Act by Watching Unlabeled Online Videos*, 2022. https://www.alphaxiv.org/abs/2206.11795

---

## 5. 技术路线四：视觉-语言-动作（VLA）模型（RT-1 → RT-2 → OpenVLA/Octo → π0）

**为什么出现**：前面三条路线要么把动作当"离散 token 序列"、要么把语义理解与低层控制分成两段。一个更彻底的想法是：*让一个预训练的视觉-语言模型（VLM）直接输出机器人的动作 token*，从而把互联网规模知识**端到端**地接到低层控制上。

**解决了什么**（分阶段）：
- **RT-1（2022）** 先用真实机器人大规模收集数据，证明"开放式的、任务无关的训练 + 高容量 Transformer 架构"能吸收多样的机器人数据，展现出随数据量、模型大小、数据多样性扩展的规律，为"机器人 Transformer"定调。
- **RT-2（2023）** 引入 **Vision-Language-Action（VLA）模型**这个术语本身：把机器人动作离散成 token，让预训练 VLM（PaLI-X / PaLM-E）直接预测动作 token，再解 token 成连续动作执行。关键技巧是**协同微调（co-fine-tuning）**——同时喂机器人演示数据（约 10 万 episode）和互联网视觉-语言数据，避免"只练机器人数据导致通用知识遗忘"。由此出现若干**涌现能力**：理解"把香蕉放到 2+1 的位置"这类需要推理的指令、识别品牌 logo / 国旗 / 人名等符号、以及链式推理。
- **Octo（2024）/ OpenVLA（2024）** 解决 **VLA 的封闭与昂贵**问题。OpenVLA 是一个 7B 参数的开源 VLA，基于 Llama 2 + DINOv2/SigLIP 视觉编码器，在 97 万条真实机器人演示上训练；作者报告其在 29 个任务、多个本体上"比封闭的 RT-2-X（55B）绝对成功率高出 16.5%，参数量却少 7 倍"，并比 Diffusion Policy 高 20.4%。Octo 则把"可微调到新传感器与动作空间"作为设计目标，在 9 个机器人平台上验证了通用策略初始化的可行性。
- **π0（2024，Physical Intelligence）** 代表 VLA 2.0：用**流匹配（flow matching）**取代自回归离散化来生成**连续、高频的动作块（chunk，50Hz）**，叠加跨本体（单臂/双臂/移动操作）的大规模预训练 + 后训练配方（1 万小时以上机器人数据），瞄准灵巧、长时程任务。

**限制**：
- **数据瓶颈**仍是根本：VLA 的能力高度依赖"跨本体、带语言标注的机器人演示"，采集成本极高（这正是 OpenVLA 转向开源、π0 强调数据配方的原因）。
- **推理延迟/能耗**：几十亿参数的 VLM 骨干每步都前向，实时控制压力大（有 2026 年工作专门指出 VLA 推理延迟会破坏 RL 所需的马尔可夫假设）。
- **动作表征之争未定**：自回归离散化有"离散化瓶颈"（重建误差），扩散/流匹配又有多步采样成本，两个方向仍在博弈。
- 语义能力虽强，**几何与物理直觉**仍偏弱（依赖演示覆盖的场景姿态范围）。

**来源**：
- Brohan et al., *RT-1: Robotics Transformer for Real-World Control at Scale*, 2022. https://www.alphaxiv.org/abs/2212.06817
- Brohan et al., *RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control*, 2023. https://www.alphaxiv.org/abs/2307.15818
- Ghosh et al. (Octo Model Team), *Octo: An Open-Source Generalist Robot Policy*, 2024. https://www.alphaxiv.org/abs/2405.12213
- Kim et al., *OpenVLA: An Open-Source Vision-Language-Action Model*, 2024. https://www.alphaxiv.org/abs/2406.09246
- Black et al., *π0: A Vision-Language-Action Flow Model for General Robot Control*, 2024. https://www.alphaxiv.org/abs/2410.24164

---

## 6. 技术路线五：生成式动作表征（Diffusion Policy 与流匹配）

**为什么出现**：模仿学习（行为克隆）面临一个经典难题——人类演示的**动作分布是多峰的**（推到目标有多种合法做法），而传统的直接回归会"取平均"导致抖动，隐式策略（能量模型）又训练不稳定。同时真实任务的**动作空间高维**。

**解决了什么**：
- **Diffusion Policy（2023）** 把去噪扩散模型用于直接学习"观测 → 动作"的 visuomotor 策略：扩散模型能表达任意可归一化分布，因而能**稳健地表征多峰、高维的动作分布**，同时避免了能量模型负采样的训练不稳定问题，并针对真实机器人设计了视觉条件、滚动时域控制与位置/速度控制的选择。这是"生成式动作表征"成为主流的标志之一。
- 后续的**流匹配（flow matching）**（如 π0 的动作专家）把多步去噪换成学习向量场，在保持连续、多峰动作生成能力的同时**显著降低采样步数/推理成本**。

**限制**：
- 扩散/流匹配的**迭代采样**仍是推理成本来源；围绕"少步甚至单步生成"有大量后续工作（本报告检索中即见多个 2026 年"单步/流图一致性"变体），说明该问题尚未完全解决。
- 这类表征本质是"动作先验"的改进，**不能替代数据**：数据不足时同样会过拟合演示覆盖范围。

**来源**：Chi et al., *Diffusion Policy: Visuomotor Policy Learning via Action Diffusion*, 2023. https://www.alphaxiv.org/abs/2303.04137

---

## 7. 技术路线六：世界模型 / 生成式交互环境（Genie 及当前）

**为什么出现**：前面所有路线都要么依赖昂贵演示、要么依赖真实交互。一个更具野心的想法：*让模型从无标签视频里学出"可交互的世界"，既生成数据、又能做想象规划，甚至直接作为策略的"内心模拟器"*。

**解决了什么**：
- **Genie（2024）** 是"首个以无监督方式、从无标签互联网视频训练的生成式交互环境"：由时空视频 tokenizer + 自回归动力学模型 + 可扩展的**隐动作模型（latent action model）**组成，能在没有任何真实动作标签的情况下，让用户在生成的帧世界里**逐帧交互**；学到的隐动作空间还能用来"让智能体模仿未见视频里的行为"。
- 这条线索在 2026 年走向"世界模型闭环"：例如 **Motus2** 提出一个共享权重的世界模型同时充当"策略（世界-动作模型）+ 模拟器（动作条件世界模型）+ 评估器（价值模型）"，形成"决策—预测—评估—改进"的自进化闭环；**Hydra-0** 则把动作表示为"像素运动"（action flow），作为跨本体、跨任务的通用控制接口。

**限制**：
- **幻觉（hallucination）**：长时程的想象 rollout 会产生预测漂移、不真实的转移，反而误导策略学习（有 2026 年工作 HaWMPO 专门用"幻觉感知"来抑制不可靠动作块）。
- **物理真实性**：视频世界模型天然更擅长"画得像"，未必遵守真实物理（质量、接触、遮挡），sim-to-real 仍有鸿沟。
- 隐动作空间虽免标签，但**可控性与可解释性**弱，且如何与真实机器人动作对齐仍是开放问题。

**来源**：
- Bruce et al., *Genie: Generative Interactive Environments*, 2024. https://www.alphaxiv.org/abs/2402.15391
- Bi et al., *Motus2: A Self-Evolving General World Model for Dexterous Manipulation*, 2026. https://www.alphaxiv.org/abs/2608.30237
- Li et al., *Hydra-0: Action Flow for Generalist World Modeling and Control*, 2026. https://www.alphaxiv.org/abs/2608.18077

---

## 8. 当前前沿与仍未解决的开放问题（2026 视角）

检索到的 2026 年工作呈现几个明确趋势，同时也暴露了尚未关闭的缺口：

1. **规模化的"具身基础模型"**：Xiaomi-Robotics-1 报告用 10 万小时真实轨迹预训练并观察到稳定的扩展规律（RoboCasa365 成功率 57.4% 刷新 SOTA）；Qwen-VLA 尝试把操作、导航、轨迹预测统一进单一 VLA。**趋势**：像 LLM 那样"数据/模型规模化"。
2. **效率与延迟**：多篇工作（DEM、SLIM-0.5B、JEPA Policy）专门挑战"每次推理都要跑几十亿参数 VLM 骨干"的成本与延迟问题，证明小得多的解耦/隐式模型可在部分任务上接近大模型——**大模型并非唯一答案**。
3. **世界模型与 VLA 的合流**：从"视频生成世界模型"（Genie）演进到"策略—模拟器—评估器合一"（Motus2）与"动作流通用接口"（Hydra-0），并在真实 VLA 上做**世界模型驱动的 RL 后训练**（HaWMPO）。

**仍面临的核心限制**（跨路线共识）：
- **数据**：跨本体、带语言标注的真实操作数据仍然稀缺且昂贵；互联网视频虽多但缺少动作标签与物理可执行性。
- **接地与几何**：语义知识向 3D 几何、接触力学、力的转移仍不充分。
- **长时程可靠性**：想象与执行中的误差累积、幻觉、分布外脆弱。
- **安全与评估**：通用机器人的安全（"比特的安全与原子的安全不可分"）与跨本体、可复现的评测基准仍不成熟。

---

## 9. 附：可核查的公开来源清单

| # | 论文（年份） | 定位 | 链接 |
|---|---|---|---|
| 1 | Attention Is All You Need (2017) | Transformer 起点 | https://arxiv.org/abs/1706.03762 |
| 2 | Decision Transformer (2021) | 决策即序列建模 | https://www.alphaxiv.org/abs/2106.01345 |
| 3 | Gato: A Generalist Agent (2022) | 多模态多本体通才 | https://www.alphaxiv.org/abs/2205.06175 |
| 4 | SayCan (2022) | LLM 语义接地 | https://www.alphaxiv.org/abs/2204.01691 |
| 5 | VPT (2022) | 无标签视频行为先验 | https://www.alphaxiv.org/abs/2206.11795 |
| 6 | RT-1 (2022) | 机器人 Transformer 定调 | https://www.alphaxiv.org/abs/2212.06817 |
| 7 | PaLM-E (2023) | 具身多模态语言模型 | https://www.alphaxiv.org/abs/2303.03378 |
| 8 | Diffusion Policy (2023) | 生成式动作表征 | https://www.alphaxiv.org/abs/2303.04137 |
| 9 | RT-2 (2023) | 提出 VLA 范式 | https://www.alphaxiv.org/abs/2307.15818 |
| 10 | Genie (2024) | 生成式交互环境/世界模型 | https://www.alphaxiv.org/abs/2402.15391 |
| 11 | Octo (2024) | 开源通用策略 | https://www.alphaxiv.org/abs/2405.12213 |
| 12 | OpenVLA (2024) | 开源 VLA | https://www.alphaxiv.org/abs/2406.09246 |
| 13 | π0 (2024) | 流匹配 VLA 2.0 | https://www.alphaxiv.org/abs/2410.24164 |
| 14 | Xiaomi-Robotics-1 (2026) | 10 万小时规模化 | https://www.alphaxiv.org/abs/2607.15330 |
| 15 | Qwen-VLA (2026) | 统一具身基础模型 | https://www.alphaxiv.org/abs/2605.30280 |
| 16 | Motus2 (2026) | 自进化世界模型 | https://www.alphaxiv.org/abs/2608.30237 |
| 17 | Hydra-0 (2026) | 动作流世界模型 | https://www.alphaxiv.org/abs/2608.18077 |
| 18 | HaWMPO (2026) | 世界模型驱动 VLA 后训练 | https://www.alphaxiv.org/abs/2609.09941 |

> 说明：第 1 项（Transformer）为众所周知的奠基性论文，直接给出 arXiv 链接供核验；其余均来自本次 `orx discover` 检索并经 `orx paper` 读取摘要/全文核对。除第 1 项外，本报告未引用任何"凭记忆给出 arXiv 编号"的论文。
