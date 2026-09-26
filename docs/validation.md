# 插件验证与迁移试用

日期：2026-09-26。

## 本地验证

- `python C:\Users\QQ110\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\research-workflow` → `Skill is valid!`
- `python C:\Users\QQ110\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .` → `Plugin validation passed`
- 独立 Reviewer 核对插件 manifest、技能与模板的相对链接，并复查关键上游许可与 autoresearch 原始流程；发现的确认集隔离、候选失败处理、候选源码保存三项问题已回写技能与有界循环参考。

上述检查验证插件结构、说明和审查处理，不等于外部研究框架已安装或在本机可运行。详细外部核查层级见[生态矩阵](landscape.md)与[自动研究比较](autoresearch-options.md)。

## 快速入门路径更新（v0.3.0）

2026-09-26 的本地检查：

- `python C:\Users\QQ110\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills\research-workflow` → `Skill is valid!`
- `python C:\Users\QQ110\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .` → `Plugin validation passed`
- 核对 README、新的学习工作流调查、本验证记录、技能入口、领域入门模板和技术演进参考中的相对 Markdown 链接 → 6 个文件，0 处断链。
- 独立审查发现模板原先只容纳旧／新方法对照、缺少实际作答记录，以及 README 将方案调查误写成必经实验；这些问题已分别改为通用机制例子、明确记录未作答／反馈，并将实验设为按需分支。
- 独立前向试用：给只懂 Python 和少量机器学习、希望在两小时内了解 RAG 且暂不做项目实验的学习者生成首轮答复。初版把多篇证据论文都排进必读路线；据此收紧技能指令，区分引用与必读材料，并单列当前方法族地图。复测答复包含当前方法地图、注明来源的技术演进、小例子、限时必读／选读路线和标为未作答的迁移题，没有强制安排工程实验。

这些检查证明技能结构、文件链接及该案例中的指令行为；它们未测量学习者的理解、速度或长期保持，也不构成对 RAG 示例每项事实的独立审校。

## OpenResearch v0.2.10 接入烟测

2026-09-26 在 Windows 上安装官方 `orx 0.2.10` 发行包，核对包的 SHA-256 为 `d85247f8b1d17a1bf0fc649ae8320f8d55388ecb376bb29696d4a70791d16fad`。从本技能目录生成 ZIP；最终包 SHA-256 为 `a9ebfaa5b9e4a7dc6c7bb72f1002780b4b850615c0925ebbe503f19f79ea6a7c`。

- `orx skills add` 返回 `name=research-workflow`，上传目录的 12 个文件与 ZIP 逐字节一致；OpenResearch 的“自定义”页面显示该技能，聊天中的 `/research-workflow` 选择器也能找到它。
- 在隔离数据目录中以 Codex 新建“RAG 入门技能接入烟测”会话；会话工作树包含 `.agents/skills/research-workflow/` 及所需的参考、模板。实际答复引用了主技能、`references/openresearch.md` 和 `templates/domain-onboarding.md`，UI 显示本轮用时 1 分 43 秒。此任务只检验接入，不评价 RAG 内容质量或学习效果。
- 工具活动显示三次失败的文件定位或读取操作后，代理才用绝对路径读到上传版本；其中一次尝试访问本机旧版插件目录。这证实相同名称的已安装插件仍可能干扰技能定位；对照试验必须隔离并核查两臂的真实技能来源。此烟测没有 A/B 对照。
- 最初将 `ORX_DATA_DIR` 放在与 Codex 登录目录不同的 Windows 盘符，启动会话时因跨盘硬链接失败；把试点数据目录放到同盘后成功。这个限制来自当前 OpenResearch 的 Windows 链接回退路径。

本轮未运行工程实验，也未测量 tokens 或总成本；不能据此断言研究质量或效率提升。

## 跨领域纸面迁移

独立 Reviewer 使用“提升 JSON 解析服务吞吐量，同时保持正确输出和内存限制”检验此技能是否依赖驾驶术语：

1. **学习：**解释解析器的输入、错误语义、分配与吞吐瓶颈；对照原始文档和一组小输入，用现有实现复现结果。
2. **复用：**检查已有解析器、基准工具和配置选项的版本、许可、数据形状与最小试验；有合适方案就先试用。
3. **冻结：**固定真实请求分布、正确性语料、主要吞吐指标、内存护栏、测量次数和机器环境；把一部分任务留作确认。
4. **有界迭代：**只允许改解析路径的指定文件，逐候选保存完整 patch、命令、原始输出、耗时、失败及资源成本；崩溃候选计入预算并回到已知状态。
5. **判断：**从原始响应重新核对正确性，在保留任务上确认获选改动；不以代理自报的单个吞吐数字代替匹配条件的证据。

这是流程迁移检查，未运行 JSON 服务或宣称任何性能改进。驾驶项目的第一轮真实运行与分析见[课程实例](https://github.com/Guanzhw/autonomous-driving-model-development-tutorial/blob/main/research/analyses/first_loop_2026-09-26.md)。
