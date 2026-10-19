# 论文精读：Evaluating the Impact of Experimental Assumptions in Automated Fault Localization

> 精读日期：2026-10-19  
> 作者：Ezekiel Soremekun；Lukas Kirschner；Marcel Böhme；Mike Papadakis（原文未明确标注通讯作者）  
> 论文机构：Royal Holloway, University of London；SnT, University of Luxembourg；Saarland University；Max Planck Institute for Security and Privacy；Monash University  
> Venue：ICSE 2023 Research Track  
> 原文（CC BY 4.0）：[DOI: 10.1109/ICSE48619.2023.00025](https://doi.org/10.1109/ICSE48619.2023.00025) · [作者版 PDF](https://mboehme.github.io/paper/ICSE23-debug-assumptions.pdf)  
> 复现材料：[Debugging Assumptions Artifact](https://debugging-assumptions.github.io/)  
> Tags：`2023` `ICSE` `Automated Fault Localization` `Ground Truth` `Construct Validity` `Automated Program Repair` `Developer Study`

## 先说结论：补丁位置、根因位置和“足够开始调试的位置”是三个不同构念

自动故障定位（Automated Fault Localization, AFL）常用三个看似合理的简化：命中第一个 faulty statement 就算成功；把开发者修改的位置当作根因位置；把故障假定为单一连续区域。本文没有再提出一个定位算法，而是把这些评价假设本身作为处理变量，在“有假设”和“无假设”两种设置中重新评估定位器、自动修复器和开发者判断。

结果说明这些简化会系统改变结论。作者调查的实验中，55% 至少使用一种假设；在四个数据集的 970 个 bug×assumption 判定单元中，49% 受到相应实验假设影响。19 种定位技术的测得有效性平均被抬高约 13%，单项最高达 38%。但传到自动程序修复（Automated Program Repair, APR）后，方向并不相同：较窄诊断减少了搜索成本，也阻止了一些可修复位置进入搜索，使两个 APR 工具在无简化假设时完成的修复总数多 125%，同时耗时和执行次数显著增加。

这篇论文对当前研究的直接价值很具体：**历史 patch、机制 root cause、完整 repair footprint 和 Agent 所需的最小可行动入口不能共用一套 gold。** 0b、T0、BQ、F2 的人工审定正在做的正是构念拆分。论文支持保留多层 gold 与多套指标，但它使用的是较小的 C 程序和传统 AFL/APR，不能直接证明 LLM Agent 上会出现相同数值。

## 理解全文所需的五个概念

### 1. Fault location 与 fix location

Fault location 指解释失败起因的代码位置；fix location 指开发者实际改动以消除症状的位置。两者可能重合，也可能相距很远。修改缓冲区上限可以阻止溢出，但真正根因可能是静态分配尺寸不足；以 diff 为 gold 会奖励“能修的位置”，不一定奖励“解释原因的位置”。

### 2. Perfect Bug Understanding（PBU）

PBU 假设认为，开发者看见排序中第一个 faulty statement 后，就能理解整个 bug。传统 wasted-effort 指标常因此只计算走到首个故障语句的检查量。若修复实际需要同一区域内的多条语句，这会过早宣布定位成功。

### 3. Single Fault Location

该假设把根因当成单个连续代码区域。现实中同一错误机制可能跨多个不连续位置，例如多处分支都使用了错误的边界条件。命中其中一个位置不代表完整诊断。

### 4. Diagnosis contract

定位结果交给谁、用于什么动作，决定什么才叫成功。给人类调试时，根因解释和完整位置更重要；给搜索式 APR 时，过窄候选会漏掉可修空间，过宽候选则增加生成、执行与时间成本。同一 gold 对不同消费者可能不公平。

### 5. Construct validity

构念效度问的是“指标是否真的测到了声称要测的东西”。Top-1、first-hit 或 patch overlap 都是可计算代理；只有先说明目标是启动调查、解释根因、覆盖完整机制还是找到任意可行修复，这些代理才有明确含义。

## 顶层证据链

```text
现实问题：AFL/APR 评价依赖简化假设
  ↓
研究对象：PBU、fix=causal、single-location 三个假设
  ↓
普遍性：63 篇论文 + 4 个 bug 数据集
  ↓
工具实验：19 个 AFL 配置在有/无假设下配对比较
  ↓
下游实验：GenProg、Angelix 使用两类诊断运行
  ↓
人因验证：76 名参与者评价 16 份诊断
  ↓
结论：假设改变工具排名、成本和开发者感知，应保守报告多层结果
```

## 三个评价假设从哪里来

### PBU：把起点当成终点

若排序把三条共同构成错误的语句排在第 1、30、50 位，first-hit 只记“检查 1 条”。作者的无 PBU 版本要求走到最后一个必要位置，度量的是完整故障集合被覆盖以前的检查量。两者回答不同问题：前者是导航入口，后者是完整诊断。

### Fix location：把治疗位置当病因位置

开发者补丁是常见且廉价的 gold 来源，但它混合了根因修复、症状规避、兼容处理、重构、测试和配置更新。论文只在根因与修复位置不相交时把该 bug 视为会受到此假设影响，这种定义相对保守，但根因标注本身仍需人工判断。

### Single location：把分布式机制压成一个点

当多个不连续区域共同导致失败时，只命中任一位置会夸大定位完整性。作者以“一个连续区域”对“所有连续区域”构造对照；它不要求所有修改行都进入 gold，而是关注所有被认定的 fault regions。

## RQ1：这些假设到底有多普遍

### 设计

作者先用 13 组调试关键词检索 2017 年至 2022 年 6 月的 ICSE、FSE、ASE、MSR、TSE、EMSE 和 TOSEM，共获得 212 篇候选；逐篇核验后保留 63 篇真正包含 AFL/APR 实验的论文。统计单位不是论文，而是论文中可辨识的实验设置。

数据层使用 SIR、IntroClass、Codeflaws 和 CoREBench，覆盖 46 个 C 程序与 352 个进入主实验的 bug；Table IV 同时披露了数据集规模、通过/失败测试数和程序长度。PBU 看故障是否含多条语句，fix-location 看根因与补丁是否不相交，single-location 看是否存在多个连续故障区。

### 结果

Table III 显示，204 个可编码实验设置中 113 个（55.4%）至少带有一种假设。fix-location 最常见，占相关实验的 **75.86%**；PBU 为 **47.67%**，single-location 为 **46.67%**。

Table V 中共有 970 个 bug×assumption 判定单元，其中 471 个（49%）受相应假设影响。PBU 影响 284/352（81%），fix-location 为 136/266（51%），single-location 为 51/352（14%）。分母不同，不能把三列直接相加，也不能把 970 误读成独立缺陷数。

### 含义

这一步证明的是评价风险具有现实规模，不证明每个使用 patch gold 的实验都错误。若研究问题本来就是“定位开发者最终改了什么”，fix-location 是合理构念；问题出在把它解释为因果根因。

## RQ2：假设如何改变 AFL 的测得有效性

### 实验坐标系

作者实现动态切片和 18 个统计故障定位公式，共 19 种 AFL 配置。统计方法按失败/通过测试中的覆盖差异给语句 suspiciousness；动态切片按失败观测点的反向依赖距离排序。程序、测试、定位算法保持不变，改变的是成功集合与 wasted-effort 终点。

有 PBU 时，有效性为 `1 - S_first`，其中 `S_first` 是到首个 faulty statement 前需检查的代码比例；无 PBU 时换为 `1 - S_all`，要求到最后一个 fault location。fix-location 对照使用开发者 root-cause 标注与补丁位置；single-location 对照使用一个区域与全部区域。

### 结果

Table VI 报告全部 19 种技术以及 Naish1、Kulczynski2、dynamic slicing 三个强配置。所有技术从“有假设”切换到“无假设”后，测得有效性都下降；三类假设平均夸大约 **13%**，单个配置最高 **38%**。按假设汇总，PBU 和 single-location 的平均差约为 **12%** 与 **16%**，fix-location 约为 **9%**。

38% 不是准确率下降 38 个百分点。它来自相对 wasted-effort 有效性变化，直觉是开发者为了找到完整目标，需要额外检查约五分之二的程序语句。论文的语言偶尔把相对差写成“effectiveness by 38%”，阅读时必须保留指标定义。

### 证据强度

这是同一工具、同一程序上的评价终点干预，能够证明实验假设会改变测得分数；它不能证明无假设版本就是唯一正确 gold，因为人工 root cause 与“全部 fault statements”同样是构念选择。

## RQ3：为什么传到 APR 后，方向会反过来

### 设计

作者把每类诊断作为候选修复位置交给 GenProg 和 Angelix。GenProg 在 IntroClass 与 Codeflaws 上运行，Angelix 只跑 Codeflaws，以避免为 IntroClass 人工改造工具链与测试 oracle。所有条件使用 30 分钟、15 代上限，记录代数、完整测试套件执行次数、时间和正确修复数。

PBU 对照给一个 faulty statement 或全部 faulty statements；fix-location 对照给补丁位置或人工 root cause；single-location 对照给一个区域或全部区域。也就是说，处理不只改变“评价标签”，还改变了 APR 实际可搜索的程序位置。

### 结果

Table VII 汇总中，有假设条件完成 **24** 个正确修复，无假设条件完成 **54** 个，多 **125%**。与此同时，无假设条件的总测试执行次数从约 1,970 增至 4,664，时间从约 148 秒增至 656 秒；作者概括为修复耗时最高约增加 3 倍。

细看异质性很重要：GenProg 的 fix-location 条件从 2 个修复增至 11 个，Angelix 从 2 增至 21；但 Angelix 的 single-location 条件却从 3 降至 2。不存在“更完整诊断对每个工具都单调更好”。候选空间变宽既恢复可修位置，也增加搜索难度。

### 含义

这正是 handoff contract 的下游效应。AFL 指标把窄目标视为容易，所以分数被抬高；APR 消费者却可能因窄门禁看不到替代修复位置，所以修复数被压低。单独优化上游定位分数可能损害整条流水线。

## RQ4：开发者想要什么样的诊断

### 设计

76 名有效参与者调试 8 个程序、评价 16 份诊断。160 份原始答卷中，84 份因约 10 个验证题未达到 75% 正确率而被排除；有效样本中 58% 是职业开发者或测试人员，约半数有至少三年经验。前两部分不告诉参与者诊断对应哪种假设，以减少需求特征。

参与者分别评价 usefulness、与自己理想诊断的 closeness、两份诊断偏好，以及三个假设的 soundness/severity。定量结果按频率汇总，自由文本由两名研究者独立编码后协商。

### 结果

- 无假设诊断有 **80%** 被评为中等到最有用；有假设诊断对应为 **63%** 的中等到最不有用。
- 无假设诊断有 **81%** 被评为中等到最接近参与者自己的诊断。
- 总体偏好为无假设 **66.23%**、有假设 **33.77%**。
- single-location 差异最大：82.89% 偏好多位置诊断；fix-location 的偏好差最小，为 53.95% 对 46.05%。
- 38% 的参与者把 fix-location 评为最不现实且最严重的假设；自由文本中 60% 对这些假设表达负面担忧。

### 边界

问卷样本只有 8 个程序和 16 份诊断，且 84/160 份回复被过滤，可能留下更熟悉 C 或更善于答题的参与者。Likert 频率也不是客观调试耗时。它支持“开发者感知和偏好发生变化”，不能证明生产环境效率会按相同比例改变。

## Figure 与 Table 怎么读

### Figure 1：一张图里其实有三种不同研究方法

图从三项假设出发，横向连接四个 RQ：文献/数据审计、19 种 AFL split test、两种 APR 工具 split test、76 人用户研究。它提醒读者不要把整篇论文误称为单一受控实验；RQ1 是观察性编码，RQ2/3 是工具配置对照，RQ4 是问卷实验。

### Table I：最重要的是“同一 bug 有多个正确视角”

三个小程序分别展示首个位置对完整位置、fix 对 root cause、单区域对多区域。表格意图不是宣布右侧永远是真理，而是说明左侧代理会漏掉一部分诊断目标。

### Table VI：固定工具，改变评价终点

这张表真正控制的是 AFL 输出排序；变化的是 gold 和停止位置。因此它最强地证明指标构造会改变性能叙事。不要把差异归因为定位算法本身变差。

### Table VII：Gold 已经变成工具输入

APR 表中的 diagnosis 进入实际搜索过程，因此同时改变可达修复与搜索成本。这里不是纯测量敏感性分析，而是上游交接干预；54 对 24 的修复差与时间增长必须一起解读。

### Table VIII/IX：平均偏好掩盖假设差异

single-location 的偏好差巨大，fix-location 则接近五五开。开发者可能认为 fix 位置是有用入口，即便它不等于根因。总体 66% 不能替代逐假设分析。

## Evidence Audit：论文证明了什么

1. **证明了三种简化假设很常见。** 在经人工核验的 63 篇论文中，55.4% 的实验设置至少包含一种。
2. **证明了 gold/终点定义会系统改变 AFL 分数。** 同一排序在完整 fault set 下需要检查更多代码，平均分下降约 13%。
3. **证明了上游诊断粒度会改变 APR 的成功与成本。** 更完整候选带来更多修复，也带来更多运行和更长时间。
4. **证明了开发者通常更偏好完整诊断。** 76 份有效答卷中，66.23% 选择无简化假设版本。
5. **证明了“定位评估”至少包含导航、解释和修复入口三种用途。** 三者对 gold 与指标的要求不同。

## 论文没有证明什么

1. **没有证明所有 patch location 都不是 root cause。** 只有两者不相交的 bug 才进入相应对照，很多修复确实发生在根因处。
2. **没有给出唯一客观的 root-cause ontology。** 一部分根因由既有开发者提供，其余由两名作者人工判断；多种合理机制解释仍可能存在。
3. **没有证明结果可直接泛化到大型多语言仓库或 LLM Agent。** 主体是开源 C 小程序、传统统计定位和搜索式 APR。
4. **没有隔离候选集合大小与语义完整性的作用。** APR 的“无假设”条件同时扩大候选空间，修复数和成本变化不能全归因于更正确语义。
5. **没有客观测量生产调试时间。** 用户研究主要是判断与偏好，不是长期现场实验。

## 作者与团队背景

第一作者 Ezekiel Soremekun 在论文发表时来自 Royal Holloway 与 University of Luxembourg SnT，现为 Singapore University of Technology and Design 助理教授。他长期研究软件验证，具体包括自动调试、软件测试、程序分析与软件安全，也研究 AI/ML 系统的正确性、鲁棒性和公平性。此前与同一团队完成 DBGBench 和 program slicing fault localization 研究，因此本文不是临时转向，而是持续追问“定位输出与真实开发者诊断是否一致”。

Lukas Kirschner、Marcel Böhme 与 Mike Papadakis 分别带来程序切片、统计调试、基准可靠性和自动修复方面的积累。公开复现站点提供文献编码、Docker 实验与用户研究材料，ICSE Artifact Evaluation 将其评为 Available 与 Reusable。

原文作者栏使用符号区分机构，没有信封、星号说明或 corresponding-author 脚注；因此本文不按末位作者推定通讯作者。

## 对当前研究的直接启发

### 1. 建立三层 gold，不再让 patch 一列承担所有含义

建议每个案例分别保存：

- `mechanism_gold`：解释漏洞成立所必需的函数/RDFS 节点；
- `repair_footprint`：开发者补丁修改、新增、测试与伴随重构节点；
- `actionable_entry`：足以让 Agent 启动正确调查的最小入口。

0b 的 `sanitize`、T0 的 `serialize`、BQ 的 `stringConcat` 属于用户已审定的 mechanism gold；配置、helper 和伴随重构是否属于 repair footprint 另行记录。三个集合允许重叠，不强求相等。

### 2. 将 first-hit 与 complete-mechanism 分开报告

函数节点主表至少同时报告 `Hit@k`、mechanism-node precision/recall/F1、all-mechanism recall。一个父函数或任一旧行命中只能证明找到了入口；若多个独立校验共同阻断漏洞，就不能用 PBU 假设把首个节点当完整定位。

### 3. 嵌套函数要保留身份与归属，不用父源码包含替代命中

T0 中父函数源码包含 `replacer` 与 `serializeFunc`，但它们在 CIG 中有独立 ID。输入可按行去重，评分仍应按冻结实体身份；否则父函数命中会自动吞并子目标，重现 PBU 与 single-location 假设。

### 4. “机制 gold”需要双人或规则化裁定

论文自身的人工 root cause 也存在主观性。当前 15 例可先由用户和独立审查者分别给出 `support / counterexample / uncertain`，冲突保留，不为了增加成功 Core 强行合并。最终同时公开 adjudicated gold 与原始 patch mapping。

### 5. 下游实验必须写清 handoff contract

若节点列表只是 soft candidate，首个正确入口可能已经有价值；若它限制后续可见范围，则需完整 mechanism recall 与 escape hatch。后续 Peripheral 干预实验应固定同一 access contract，避免把 gold、候选宽度和工具权限一起改变。

## 最终评价

这篇论文的价值不在于告诉我们哪一种故障定位算法最好，而在于指出：实验分数往往由研究者选择的成功定义决定。首个 faulty statement、开发者修改行和单一连续区域都可以是有用代理，却不能在没有声明用途时被解释为完整根因。

当前研究已经进入必须处理这一问题的阶段。下一步不宜继续用旧行 F1 或 patch-node F1 给“成功 Oracle”盖章，而应冻结机制、修复足迹和可行动入口三套对象，再让指标与下游契约对应。这样即使某个 Agent 只找到入口、没有覆盖完整机制，结果也能被准确描述，而不会被简单记成满分或失败。
