# 具身智能报告：两份独立内容审阅

原始用户任务：

> 研究一下具身智能的发展脉络，从 Transformer 开始。请给我一份中文研究报告，解释主要技术路线为什么出现、解决了什么问题、还面临哪些限制，并附可核查的公开来源。若范围需要取舍，请在报告中说明。

更上层的问题是：OpenResearch 的现有研究流程是否值得补充 Research Workflow。最终的报告价值由用户判断；这两份审阅提供可追溯的内容核查。

| 生成条件 | 原始报告 | 匿名审阅 |
| --- | --- | --- |
| OpenResearch 现有流程 | [without-workflow.md](../openresearch-embodied-direct-comparison-20260926/without-workflow.md) | [review-01.md](review-01.md) |
| 现有流程 + 显式调用 Research Workflow | [with-workflow.md](../openresearch-embodied-direct-comparison-20260926/with-workflow.md) | [review-02.md](review-02.md) |

两位 reviewer 各自只收到一份逐字节复制、以中性名称保存的报告和同一段任务说明；未获知生成条件或另一份报告，也没有互相阅读审阅意见。两位均按报告内容、时间与因果脉络、机制与限制、引用是否支持结论等方面核查原始论文，给出行号、严重程度、来源链接、优点和未核查范围。没有数字评分，也没有要求 reviewer 判定哪组获胜。

共同发现是：两份报告都具备可读的范围和路线结构，也都把部分并行发展的技术写成过于整齐的线性继承。第一份还需修正 Gato 接地与世界模型前史等解释，并补足跨本体数据路线；第二份需优先修正“Transformer 必须离散化动作”“离散自回归不能表达多峰动作”等机制断言，以及 Octo/OpenVLA 的架构混用。具体证据与限定条件见各自审阅正文。
