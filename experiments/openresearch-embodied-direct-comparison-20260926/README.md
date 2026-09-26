# 具身智能发展脉络：OpenResearch 原始报告对照

这两份报告均由 OpenResearch v0.2.10 中的 OpenCode 会话实际生成，使用相同的 `deepseek/deepseek-v4-pro` 模型和以下共同任务：

> 研究一下具身智能的发展脉络，从 Transformer 开始。请给我一份中文研究报告，解释主要技术路线为什么出现、解决了什么问题、还面临哪些限制，并附可核查的公开来源。若范围需要取舍，请在报告中说明。

| 条件 | 原始报告 | OpenResearch 会话 |
| --- | --- | --- |
| 未加载 Research Workflow | [without-workflow.md](without-workflow.md) | `chat_dfeb8730-edac-4089-b90a-65f080016794` |
| 显式加载 Research Workflow | [with-workflow.md](with-workflow.md) | `chat_ffcc9d2f-0439-4156-a62f-bf55c3d4c912` |

两份 Markdown 均逐字节复制自各自会话工作树，未编辑报告正文。两组都调用了 OpenResearch 现有的 `orx-lit-review` 技能。A 会话完成时，OpenCode 技能列表及会话工作树均没有 `research-workflow`，工具记录也没有读取该技能；B 会话调用了 `skill({id: "research-workflow"})` 并读取其参考文件。这里比较的是现有流程与“额外提供并显式调用 Research Workflow”的流程。B 结束后，用户的全局技能库仍保留该技能，文件内容与实验前的 ZIP 逐文件哈希一致。

两位 reviewer 已分别对匿名报告做[独立内容审阅](../openresearch-embodied-review-20260926/README.md)，核查关键论文并标出具体问题；最终使用价值仍由用户判断。这里不附数字打分。两份报告仅代表各自一次运行，不足以估计结果的统计稳定性。

| 文件 | 字节数 | SHA-256 |
| --- | ---: | --- |
| `without-workflow.md` | 19,644 | `5EF297155ED636682BAF984EA85D33C12F32B5A42104ADA94ABC8E51011E2E23` |
| `with-workflow.md` | 26,885 | `D0CF09CBBC6DB258A9A43AC430E9578A7F06DB2B2C3CE1EFB3193F4B20B65AF4` |
