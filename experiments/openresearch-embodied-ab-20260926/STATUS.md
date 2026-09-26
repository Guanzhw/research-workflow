# 执行状态：两份原始报告已产出，等待用户主观评审

2026-09-26。用户指定的共同任务为“研究一下具身智能的发展脉络，从 Transformer 开始”，并明确希望先阅读 OpenResearch 实际生成的两份报告，再自行判断 Research Workflow 是否带来价值。报告和运行说明见[同题直接对照](../openresearch-embodied-direct-comparison-20260926/README.md)。

两次有效运行均使用 OpenResearch v0.2.10、OpenCode harness、`deepseek/deepseek-v4-pro` 模型和相同任务正文。A 运行时暂时移除了上传的全局 `research-workflow` 技能；A 完成后，按原始 ZIP 逐文件校验并恢复了技能。B 在恢复后以 `/research-workflow` 显式调用，工具记录显示它加载技能并读取参考文件。报告文件均从会话工作树逐字节复制，未修改内容。

先前的两次 Codex 探索性运行都读取了 Research Workflow，因此只作为[非对照报告](../openresearch-embodied-report-comparison-20260926/README.md)保留。首次隔离服务启动曾被自动执行审核阻止；本次使用现有服务完成了干净的 OpenCode 条件切换，没有重试该启动操作。

两位 reviewer 已分别对匿名报告完成[独立内容审阅](../openresearch-embodied-review-20260926/README.md)，核查了关键原始论文，未做数字打分或判定胜负。本次没有把一次性输出差异解释为统计显著的效果。下一步是用户阅读报告和审阅意见并给出主观判断；若需量化稳定性，再按[方案](PLAN.md)追加重复运行。
