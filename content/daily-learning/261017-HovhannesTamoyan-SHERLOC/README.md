# 论文精读：SHERLOC: Structured Diagnostic Localization for Code Repair Agents

> 精读日期：2026-10-17  
> 作者：Hovhannes Tamoyan；Sean Narenthiran；Erik Arakelyan；Mira Mezini；Boris Ginsburg（原文未明确标注通讯作者）  
> 机构：NVIDIA；TU Darmstadt；hessian.AI；ATHENE  
> 原文：[arXiv:2606.24820](https://arxiv.org/abs/2606.24820) · [完整 HTML v2](https://arxiv.org/html/2606.24820v2) · [PDF](https://arxiv.org/pdf/2606.24820)  
> 版本：arXiv v2，2026-08-31  
> 代码与配方：[NVIDIA-NeMo/Skills — SHERLOC](https://github.com/NVIDIA-NeMo/Skills/tree/main/recipes/sherloc)  
> Tags：`2026` `arXiv` `Code Localization` `Code Repair Agent` `Diagnostic Context` `Repository Exploration` `SWE-bench Verified` `Chunk Coverage` `Negative Transfer`

## 先说结论：定位不是“给一个文件名”，而是交付可验证的诊断

SHERLOC 把代码定位从检索问题改写为诊断问题。传统指标只问是否命中 gold 文件或函数；修复 Agent 真正需要的却是：哪段代码为什么可疑、根因是什么、应该怎样改、牵涉哪些依赖、如何验证。论文用一个不训练的单 Agent 系统，把固定的四种仓库工具、自恢复机制和五字段诊断输出组合起来，再把这份诊断直接注入 SWE-Agent 与 OpenHands。

结果分成三层。第一，Qwen3-235B 配置在 SWE-bench Verified 达到 81.27% file-level recall@1，约 30B 的匹配规模配置仍有 75.07%。第二，文件命中远非终点：在“预测文件完全正确”的 371 个实例中，行块完整覆盖与不完整覆盖的平均修复率仍相差 22.6 个百分点。第三，高质量诊断可以提高修复率并节省搜索成本，但坏诊断会负迁移；MiniMax-M2.5 的两个框架分别下降 4 和 5 个百分点。

对当前研究最有价值的不是又一个定位 SOTA，而是一个更精确的实验对象：**function identity hit、实际可见代码块、诊断可执行性是三种不同处理**。论文支持把“Agent 是否看见足以行动的证据”作为主要中间变量，但它没有做严格的等 token、等位置随机干预，因此仍不能单独回答外设上下文的因果效应。

## 理解全文所需的五个概念

### 1. Location 与 finding

Location 是文件或行号；finding 是带解释的诊断对象。SHERLOC 的 finding 固定包含五项：位置解释、根因、解决思路、依赖、测试影响。两者不能互换：正确位置加错误根因仍可能把修复 Agent 引向错误补丁。

### 2. File-level、chunk-level 与 actionability

- file-level 衡量是否命中正确文件；
- chunk-level 直接在 `(start_line, end_line)` 区间上衡量 gold 编辑块覆盖、精度与紧致度；
- actionability 衡量诊断是否足以指导下一步修复。

函数或类不是总能对应真实编辑目标：补丁可能落在 import、类字段、配置分支，或跨多个函数协调修改。因此论文使用结构无关的行块指标，是对纯 function-level 评估的重要补充。

### 3. Tightness 与 coverage

把整文件都返回，可能覆盖全部 gold 行，却没有真正缩小搜索空间。Coverage 问“关键块是否被看见”，tightness/precision 问“附带了多少无关代码”。二者构成召回与上下文污染之间的张力。

### 4. Diagnostic transfer

定位输出只有被下游 Agent 使用并改变修复结果，才完成 transfer。论文因此不仅评估 SHERLOC 自身，还把同一份 finding 注入五个修复模型、两个框架并观察 held-out tests 是否通过。

### 5. Negative transfer

额外上下文并非总有帮助。若诊断自信却错误，它会缩窄下游搜索、占据上下文并制造锚定。论文用 shuffled finding 与低质量 finding 展示了这种风险。

## 顶层证据链

```text
缺口：现有定位主要奖励“命中文件”
  ↓
设计：单个推理模型 + 四种只读工具 + 自恢复
  ↓
输出：行块位置 + 五字段结构化诊断
  ↓
自身评估：文件指标、行块覆盖、隐式知识控制、组件消融
  ↓
下游干预：将 finding 注入 5 个模型 × 2 个修复框架
  ↓
结果：多数设置修复率提高、token 降低；错误诊断会负迁移
  ↓
边界：相关质量门控是事后分析，未解决在线可信度估计
```

## SHERLOC 怎样运行

### 初始化：先给地图，不一次装入代码

系统过滤文档、构建产物、依赖目录和版本控制元数据，再把精简仓库树、issue、工具说明及输出格式放入初始提示。这里提供的是全局导航图，不是把所有文件塞进上下文。

### 四个工具各自承担什么

1. **View File**：读取文件或指定行区间，并对近似路径给出纠正建议；
2. **Codebase Search**：仓库级字面搜索，返回匹配位置和周边片段；
3. **Repository Tree**：重新查看过滤后的文件层级，恢复全局定位；
4. **Connected Tree**：沿 import 正向和反向关系查看依赖。

工具集合刻意保持小而只读。模型决定查什么，确定性执行器负责校验和运行，避免原始 shell 带来的命令构造、转义和调试故障。

### 有界循环与自恢复

每个实例最多 20 轮。模型每轮要么调用一个工具，要么返回位置和五字段 finding。历史观察保留在对话中，没有额外外部记忆。自恢复包括上下文裁剪、循环检测、隐式/畸形工具调用修复、响应长度管理，以及预算将尽时强制综合已有证据的 final-turn prompt。

这不是附属工程细节。100 个 SWE-Gym 开发样本上的消融显示：删除 View File 使 F1 下降 7.0pp，删除 final-turn prompt 下降 5.0pp；完整系统的 F1 为 63.19，去掉隐式工具检测、上下文管理和响应长度管理后分别降到 59.14、59.84 和 60.62。

## 实验坐标系

### 数据与模型

- 定位主评估：SWE-bench Lite 与 500 个 SWE-bench Verified 实例；
- 本体消融：100 个均匀抽取的 SWE-Gym 开发实例；
- 定位 backbone：Qwen3-235B、Qwen3-30B Thinking、Qwen3-30B Instruct、DeepSeek-V3、DeepSeek-R1；
- 下游修复：SWE-Agent 与 OpenHands，跨五个 repair backbone；
- 定位每配置 3 个 seed；下游修复表的每个 cell 是 500 实例上的完成运行。

主定位配置温度 0.99、top-p 0.95、最多 20 轮、每次生成上限 81,920 token；修复 Agent 使用各框架的 stock 配置。高温和超长上限意味着“4.7 轮”不等于低生成成本，作者也明确披露头部配置依赖 235B 模型。

### 指标为什么分三层

- 文件集合：precision、recall、F1、exact match、hit@1；
- 行块：coverage recall、precision、average tightness；
- 下游：补丁通过 held-out tests 的 resolve rate，以及首个源代码编辑前的定位 turn/token 和全程 token。

论文还用 GPT-5.2 在已知 gold patch 的条件下，对 499 份 finding 的根因正确性、位置准确性和方案可执行性各打 1–5 分。这个 judge 可用于分析，却不是部署时可得的在线门控器。

## RQ1：单模型、固定工具能否达到强定位

### 问题

不做微调、不做强化学习、也不使用多 Agent 辩论，单个推理模型是否能靠受控工具获得竞争力？

### 设计

作者在 Lite 和 Verified 上运行四个主 backbone、三个 seed，并与 SWERank、LocAgent、SWE-Agent、OpenHands、Agentless、RepoSearcher/ToolTrain 等既有结果比较。同时报告约 30B 的匹配规模结果，避免只用 235B 对 32B 基线做不公平归因。

### 结果

- Lite：Qwen3-235B accuracy@1 为 **84.33±0.72%**，平均 5.0 轮；
- Verified：Qwen3-235B recall@1 为 **81.27±1.16%**，平均 4.7 轮；
- 约 30B 的 Qwen3 配置为 **75.07±1.24%**，高于论文所列 ToolTrain-32B 的 68.03%；
- DeepSeek-V3 为 **79.53±0.47%**，说明结构可跨模型家族迁移。

但行块指标明显低于文件指标：235B 在 Verified 上 chunk coverage recall 只有 **41.28%**，precision 为 **53.47%**。也就是说，系统很擅长指出“去哪”，却常没有完整交付“具体看什么”。

### 意义

SHERLOC 证明受控的仓库浏览协议本身很有价值，但不能把文件级 81.27% 解释为关键代码可见率 81.27%。这正是当前研究中必须避免的粒度偷换。

## RQ1 的有效性控制：模型是不是背过 SWE-bench

当工具、仓库树、issue 中的文件与模块路径全部被遮蔽时，模型仅凭 issue 文本仍有 **57.86% recall@1**；在 scikit-learn 和 requests 上甚至达到 85%–88%。论文把它主要解释为对流行开源仓库和特征性错误信息的参数熟悉度。

当仅遮蔽 issue 中显式路径、但保留工具与仓库树时，SHERLOC 达到 **79.96%**，只比完整系统低 1.3pp。这个控制说明主动探索恢复了大部分表面路径泄漏信号，但不能消除训练数据熟悉度；真正隔离污染仍需私有或可证明未见仓库。

## RQ2：定位与诊断能否转化为修复收益

### 问题

更好的定位是否真的让下游修复 Agent 更容易成功，并降低搜索成本？

### 设计

每个 repair 模型×框架比较六种条件：原始 Baseline、路径/仓库名遮蔽、随机错配的 Shuffled finding、完整 SHERLOC finding、质量过滤 QF SHERLOC、以及基于 gold patch 的 Oracle。正式可部署条件是未过滤 SHERLOC；QF 使用 gold-patch-conditioned judge，是事后敏感性分析。

### 结果

未过滤 SHERLOC 在 10 个 cell 中 8 个提高或维持点估计，平均提高 **4.39pp**；若每个 cell 事后取 SHERLOC 与 QF 的较好者，平均为 **+5.95pp**。代表性结果：

| Repair backbone / 框架 | Baseline | SHERLOC | 变化 |
|---|---:|---:|---:|
| Qwen3-Coder-30B / SWE-Agent | 44.7 | 54.0 | +9.3pp |
| Qwen3-Coder-Next / OpenHands | 44.6 | 53.2 | +8.6pp |
| Qwen3-Next-80B / OpenHands | 38.6 | 50.4 | +11.8pp |
| MiniMax-M2.5 / OpenHands | 72.2 | 67.2 | -5.0pp |
| Qwen3-Coder-480B / SWE-Agent | 63.0 | 63.0 | 0.0pp |

配对 bootstrap 与 Holm 校正显示，较弱模型上的多项收益显著；MiniMax/OpenHands 的 -5.0pp 在校正后仍为 p=0.0168，而 480B 的变化不显著。错误的 shuffled finding 通常更差，说明收益不是“随便给一点上下文”产生的。

成本方面，完整 pipeline（含独立 SHERLOC localizer）平均减少 **36.7% 定位 token** 和 **23.1% 总 token**。例如 Qwen3-Coder-30B/SWE-Agent 从 101.8k 降到 65.8k 定位 token、resolve 从 44.7% 升至 54.0%。但 OpenHands/Qwen3-Coder-Next 的全程 token 反而增加 1.4%，因此平均节省不应被理解为每个设置都节省。

### 意义

诊断上下文最帮助“定位 headroom 大”的模型；对本来已经很强的修复模型，错误锚定可能抵消节省的搜索。外部定位器应该是可拒绝的建议，而不是硬门禁。

## Figure 与 Table 怎么读

### Figure 1：方法图的重点是执行边界

图中推理 LLM 只选择固定工具，执行器验证参数并返回有界观察，自恢复层包围交互循环。真正的设计主张不是工具名字新，而是把开放式仓库操作压缩成可读、可恢复、可审计的协议。

### Figure 2：文件 SOTA 不能替代行块证据

图 2 展示 file-level accuracy/recall 的领先结果；Table 3 却显示不同 backbone 的 chunk 行为不同。DeepSeek-V3 的 coverage 与 precision 较高但 tightness 仅约 10%–15%，而 Qwen3-235B 的 tightness 为 27%–36%。同样“命中”可以来自很宽或很窄的可见区间。

### Figure 3 与 Table 11：收益高度异质

热力图最显眼的是弱模型增益，但 MiniMax 的两行下降同样重要。不存在“好定位对所有 Agent 都单调有益”的结论；消费者能力和 finding 质量共同决定 transfer。

### Figure 7 与 Table 7：质量不是装饰变量

499 个 finding 中，270 个落在 Very High，55 个落在 Low。Very High 组 resolve 为 75.9%，Low 组只有 20.0%，低于 61.6% baseline；质量分与是否解决的点二列相关为 0.45，solution actionability 单项为 0.46。

这不是质量的因果效应：高分 finding 也可能对应更容易的任务。但结合 shuffled 控制、组件消融和下游注入，它足以说明质量门控是必要研究问题。

### Table 13：最贴近当前实验的结果

作者只保留“预测文件集合完全正确”的 371 个实例，再按 gold 编辑块是否完整覆盖划分。144 个 complete coverage 实例平均 resolve **82.5%**，227 个 incomplete 为 **59.9%**，差 **22.6pp**；每个模型×框架 cell 的差都在 18.8–27.4pp。

这直接否定“文件对了就等于看见了关键代码”。不过 coverage 不是随机分配，容易任务可能同时更易覆盖和修复，因此该差值仍是关联，不是 coverage 的因果效应。

## 组件消融与失败机制

### 工具与恢复机制

View File 的消融损失最大，说明仓库树和搜索只负责候选生成，真正读取代码仍不可替代。final-turn prompt 次之，说明长轨迹不仅要收集证据，还要被迫把证据压缩成可交付对象。

### finding 字段消融

组件实验保持同一组位置，只删减文本字段，因此比“换整个定位器”更接近诊断内容的干预。结果显示仅给 solution idea 或只给 location explanation + root cause 的收益不稳定；完整诊断更可靠，但高质量过滤仍是关键。

### 零召回失败分类

55 个零召回实例中，40% 是“已经看见正确文件，却最终选错”，27% 是正确目录下选错文件，25% 是完全错误模块；真正的探索不足只有 2%。瓶颈更多在证据选择与最后综合，而不是无限增加浏览深度。

## Evidence Audit：证明了什么

1. **证明了 file-level 与可执行诊断不等价。** 文件召回很高时，行块覆盖仍有限；相同正确文件集合下，完整与不完整块覆盖对应显著不同的修复率。
2. **证明了结构化 finding 可对部分下游 Agent 产生实际收益。** 注入实验跨两个框架与五个 backbone，配对不确定性分析支持多个弱/中等模型上的正向变化。
3. **证明了负迁移真实存在。** shuffled finding 普遍有害，MiniMax 的未过滤 SHERLOC 也下降；所以额外诊断必须允许拒绝。
4. **证明了小型固定工具与恢复机制足以形成强基线。** 工具和恢复组件均有消融贡献，约 30B 配置也保持竞争力。
5. **证明了 token 节省来自缩短下游搜索，而不是零成本。** 成本表把 standalone localizer 纳入完整 pipeline，并保留注入后仍需验证文件和测试的定位前缀。

## 没有证明什么

1. **没有证明 chunk coverage 对修复率的因果效应。** Table 13 是条件关联，没有在等任务、等预算下随机控制可见行块。
2. **没有证明 QF SHERLOC 可在线部署。** 质量分依赖 gold patch conditioned GPT-5.2 judge，阈值切换是事后选择。
3. **没有证明对私有、多语言或非 Python 仓库泛化。** 主评估仍是公开 SWE-bench Verified；Connected Tree 的 import parser 也需要语言适配。
4. **没有证明头部 SOTA 全由框架产生。** 235B 与 30B 相差 6.2pp，模型规模贡献不可忽略。
5. **没有解决上下文污染的净因果问题。** finding 同时改变位置、文本、token 长度和下游搜索路径，尚未隔离每个成分。

## 作者与团队背景

第一作者 Hovhannes Tamoyan 是 TU Darmstadt 博士生，并在 NVIDIA 从事应用研究；个人主页列出的长期兴趣是 LLM 的代码与科学推理，此前也参与 ATHENE 资助的 Code Transformer 项目。SHERLOC 把代码表示、仓库探索和推理模型工具使用结合在一起，与这条研究路径直接相关。

论文作者横跨 NVIDIA 与 TU Darmstadt：Mira Mezini 团队长期研究软件工程、程序理解与可信软件，NVIDIA 侧则提供大模型、推理服务和 Agent 工具链积累。论文的固定工具协议与 NVIDIA-NeMo/Skills 公开配方，也体现了研究与可复用 Agent 工程之间的衔接。

原文作者栏、arXiv 页面与公开 HTML 均未显式标注通讯作者；因此这里不按末位作者推定通讯关系。

## 对当前研究的直接启发

### 1. 把三层 exposure 分开记录

当前 860 个语义单元审计可以形成三张表，而不是一个“命中”列：

- identity hit：方法是否返回目标函数/类身份；
- visible span coverage：实际送入模型的行块是否覆盖关键语句；
- diagnostic actionability：上下文是否足以支持正确根因与修改方向。

Azure 案例中 BM25 命中函数名却只暴露 174–233 行、漏掉 278–282 行的 `WriteFile`，正属于 identity hit=1、key-span exposure=0；不能把它计为完整处理。

### 2. 主实验单位改为“实际可见块”

SHERLOC 的 structure-agnostic chunk 适合补充现有函数/类语义单元。建议对每个检索结果同时保存 `(file, start, end, token_position)`，再与 D/S/P/I/M/U 标注的关键块求 coverage，而不是从函数身份反推模型看见了什么。

### 3. 下一步做等 token、等位置的增量对照

论文没有完成这一步，正好留下当前研究的增量：在已经成功暴露 Core 的实例中，固定 Core 内容、总 token 和上下文位置，只随机加入已冻结的 Peripheral 候选；比较 repair/review 结果、根因正确性与行动路径。这样才能区分“覆盖关键块”与“附加外围信息”的效应。

### 4. 将坏诊断视为潜在负处理

SHERLOC 的 MiniMax 结果说明，强消费者不一定受益于外部提示。实验不应只统计平均提升，还应报告：何种 baseline 能力、何种诊断质量、何种覆盖状态下发生反转；N/A 的预算耗尽继续与真实零分分开。

## 最终评价

SHERLOC 最重要的贡献，是把代码定位的成功标准从“返回了正确实体”推进到“下游能否据此行动”。它用跨框架注入实验、行块覆盖与负迁移证据，说明文件/函数命中只是暴露链条的第一层。

对当前研究而言，这篇论文提供了一个很好的测量桥梁，但不是最终因果答案。最值得继承的是 line-span exposure、structured diagnosis 和 downstream transfer 三层记录；最需要补上的则是等 token、等位置、同实例内的随机增量控制，以及不依赖 gold patch 的在线质量门控。
