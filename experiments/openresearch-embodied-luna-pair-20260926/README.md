# 具身智能发展脉络：Luna Max 配对报告

本目录保存 OpenResearch v0.2.10 实际运行产生的两份中文研究报告。报告正文从各项目的 artifacts 目录逐字节复制，未做内容修改。请直接阅读并自行判断哪一份更有用。

| 条件 | 原始报告 | OpenResearch 会话 |
| --- | --- | --- |
| A：未提供 Research Workflow | [without-workflow.md](without-workflow.md) | `chat_171647dc-0308-4956-9931-22111a3070bf` |
| B：提供并显式调用上传版 Research Workflow v0.3.0 | [with-workflow.md](with-workflow.md) | `chat_ba935f47-0507-461d-a707-cc5a0cf7c50f` |

## 任务与环境

两组共同任务原文：

> 研究一下具身智能的发展脉络，从 Transformer 开始。请给我一份中文研究报告，解释主要技术路线为什么出现、解决了什么问题、还面临哪些限制，并附可核查的公开来源。若范围需要取舍，请在报告中说明。

B 的首条消息在任务原文前加了 `/research-workflow`。两组都是新建的空 Git 项目和 OpenResearch Codex 会话，模型均为 `gpt-6-luna`，推理档位均为 `max`，Codex CLI 版本为 `0.158.0-alpha.2.1`。两组均可使用 OpenResearch 自带的文献检索、论文阅读、报告技能和 Codex 工具；实际使用的工具由会话自行选择。

A 运行前，OpenResearch 上传版技能被临时移除，镜像技能被排除，Codex 中旧版插件也被临时禁用。A 的技能目录没有 `research-workflow`，工具记录没有读取它。B 运行时，上传版 v0.3.0 已恢复，旧版 Codex 插件保持禁用；B 的会话技能文件与上传版哈希相同，工具记录读取了 `.agents/skills/research-workflow/SKILL.md`。实验后 Codex 插件配置已恢复到实验前的 SHA-256，上传版技能仍可用。

## 运行与费用记录

以下 token 数取自 Codex 原生 `token_count` 的最终累计值。输入总量包含缓存输入；“非缓存输入”由总输入减缓存输入得到。耗时从首条用户消息到最终助手消息完成。

| 会话 | 耗时 | 输入总量 | 缓存输入 | 非缓存输入 | 输出 | 工具记录 / 错误 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 17.6 分钟 | 3,174,668 | 3,019,520 | 155,148 | 45,699 | 63 / 12 |
| B | 37.1 分钟 | 3,707,065 | 3,506,944 | 200,121 | 80,019 | 54 / 14 |

另有一次未纳入比较的 B 预备会话 `chat_2162089a-2687-499f-be79-3dd7e20069ec`：它先读到了 Codex 插件中的旧版 v0.2.0，发现后即中止，耗用 401,389 输入（其中 368,896 缓存）及 5,381 输出 token。B 正式会话采用 OpenResearch 默认的“自动审批”权限时，工具审批触发过一次 `codex-auto-review`，耗用 19,662 输入（其中 4,864 缓存）及 138 输出 token。发现后，中止当前回合并把同一 B 会话改为 `full-access`，后续原生回合记录为 `gpt-6-luna / max`、`approval=never`、`reviewer=user`。因此，虽然两份报告正文由 Luna Max 生成，本轮执行并非严格只调用 Luna Max。

B 在首回合持续检索且迟迟未写出文件。为控制费用，向同一会话补充了停止检索、下载和配图并立即成稿的指令。B 因此比 A 多了一次成本控制指令，且后段权限不同；这会影响对报告差异的因果判断。两份原始报告仍可供用户直接评审。

## 产物校验

| 文件 | 字节数 | SHA-256 |
| --- | ---: | --- |
| `without-workflow.md` | 12,853 | `39B74AD5FE1DC291AABFCE0F101BDD3D2BBD56CEF132C2E9AC768510AD2BED95` |
| `with-workflow.md` | 17,632 | `9784A9EC150A54416632ED0B94F109BFFFD8D584D53DA2AD37CE511D4FBC860A` |

两个哈希均与 OpenResearch artifacts 原件相同。仓库用 `.gitattributes` 的 `-text` 保留原始文件字节。此次没有安排新的内容 reviewer；报告效果由用户主观评审。

自动审批阻止了清除 OpenResearch `user-skills/excluded/research-workflow` 标记，只返回 `blocked by policy`。该标记目前仍在；上传版技能和 Codex 插件配置已恢复，技能在 OpenResearch 中可见且可调用。该标记只影响将来移除上传版技能之后的镜像技能回退。
