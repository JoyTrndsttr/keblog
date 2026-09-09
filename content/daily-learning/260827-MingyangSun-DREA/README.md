# DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection

> 精读日期：2026-08-27  
> 论文：*DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection*  
> 作者：Mingyang Sun, Guozhu Meng  
> Venue：Internetware 2026 / arXiv 2026  
> DOI / 原文：[arXiv:2607.13439](https://arxiv.org/abs/2607.13439)  
> 来源：从 `dialog.md` 的每日学习历史迁移  

## 一句话价值

将安全推理与仓库探索解耦，在提高检测效果的同时把多数 token 成本卸载给轻量模型。

## 历史精读正文

### 4. 每日顶会 / 顶刊论文极速精读

#### 论文信息

- **标题**：DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection
- **作者**：Mingyang Sun、Guozhu Meng
- **来源**：Internetware 2026；arXiv预印本
- **发布日期**：2026年7月15日
- **原文**：[arXiv:2607.13439](https://arxiv.org/abs/2607.13439)
- **一句话结论**：让强模型负责提出和修订安全假设、让轻量模型按需探索仓库，可以提高漏洞检测并显著降低付费API成本；但更多上下文并不能弥补模型本身的安全推理缺陷。

#### 速读导航表

| Section                  | 阅读建议                | 只需要带走什么                                           |
| ------------------------ | ----------------------- | -------------------------------------------------------- |
| 1 Introduction           | **快读**                | 固定上下文无法适应跨文件漏洞，且直接让强模型探索成本过高 |
| 2 Motivating Example     | **必读**                | 为什么只看目标函数会把授权漏洞误判为安全                 |
| 3.1 DREA                 | **必读**                | Planner—Explorer循环及信息边界                           |
| Algorithm 1              | **快读 / 算法细节可跳** | 理解hypothesis → request → evidence → revision即可       |
| 3.2 RepoPairBench        | **必读**                | 漏洞—修复配对设计及BENIGN标签的实际含义                  |
| 3.3 Reasoning Evaluation | **必读**                | Lucky Hit与Reasoning Accuracy怎么定义                    |
| 4.1 Setup                | **必读**                | 四个设置到底改变了哪些变量                               |
| 4.3 Judge Reliability    | **扫表**                | 看一致率和Cohen’s κ                                      |
| 5.1 RQ1                  | **必读**                | 看Table 1–3，核心效果与消融                              |
| 5.2 RQ2                  | **扫表**                | 看Table 4，成本结论                                      |
| 5.3 RQ3                  | **扫图 / 快读**         | 看Figure 3，关注CWE异质性                                |
| 5.4 RQ4                  | **必读但要质疑**        | “探索越多越差”存在任务难度混杂和反向因果                 |
| 5.5 RQ5                  | **必读**                | 看Figure 4，26%–55%的正确标签属于Lucky Hits              |
| 6 Discussion             | **快读**                | 信息获取不是唯一瓶颈，安全推理能力更重要                 |
| 8 Limitations            | **必读**                | Python、100个CVE pair、公开CVE污染及判定规则             |
| Related Work             | **跳过 / 扫一眼**       | 非核心贡献                                               |

**如果只有25–30分钟，按这个顺序读：**

Motivating Example
→ Figure 2与Sec. 3.1
→ Sec. 3.2–3.3
→ Table 1
→ Table 3
→ Table 5
→ Figure 4
→ Sec. 8

#### 核心一：DREA到底解耦了什么

##### Planner

由GPT-5.2、DeepSeek-V3.2或GLM-4.7等较强模型承担：

1. 检查目标函数；
2. 提出漏洞假设；
3. 判断缺少什么仓库证据；
4. 向Explorer发出探索请求；
5. 根据返回证据修订假设；
6. 输出VULNERABLE或BENIGN及其理由。

VULNERABLE结论需要描述从攻击者可控输入到危险操作或安全边界违规的合理路径；BENIGN则需要说明相关操作受到何种保护。

##### Explorer

固定使用本地部署的4-bit GLM-4.7-Flash，通过四种只读工具工作：

- `ls`
- `glob`
- `grep`
- `read_file`

它返回三类结构化信息：

- Repository Context；
- Code Evidence；
- Security Findings。

虽然论文把Explorer定位为“只检索、不作最终安全判断”，但`Security Findings`已经包含“缺失检查”“可疑数据流”等带有分析性质的内容。因此两个角色并非完全意义上的reasoning/retrieval纯净分离。

> **读完Sec. 3.1，你只需要记住：DREA的关键不是简单使用两个Agent，而是用强模型控制调查方向，用轻量模型压缩仓库证据后再反馈。**

#### 核心二：RepoPairBench解决了什么

RepoPairBench包含：

- 100个Python漏洞—修复pair；
- 共200个实例：100个漏洞函数、100个修复函数；
- CVE年份为2021–2025；
- 覆盖48个CWE类别；
- 每个实例保留对应版本的完整仓库快照。

每个pair由修复提交的父版本和修复后版本组成。模型从目标函数及文件路径出发，可以按需探索相应仓库。

最重要的标签限定是：

> 修复后的函数被标记为BENIGN，只表示不存在该CVE所描述的特定漏洞，并不表示代码没有其他漏洞。

如果模型在修复版本中发现了另一个真实问题，仍被计为false positive。这是严格的配对协议，但存在construct validity损失。

#### 核心三：Lucky Hit为何重要

论文不只看预测标签，还判断解释是否符合已知漏洞机制。GPT-4.1裁判获得：

- CVE描述；
- 修复提交信息；
- 漏洞与修复代码diff；
- CWE标签；
- 模型最终分析。

裁判检查漏洞类型、相关代码、根因和利用机制是否正确。

定义：

\[
LHR=\frac{\text{预测标签正确但推理错误的漏洞样本}}
{\text{所有True Positives}}
\]

\[
RA=1-LHR
\]

裁判在50个分层抽样案例上进行了人工验证：

- 与两名安全研究人员的一致率分别为96%和94%；
- Cohen’s κ分别为0.92和0.88；
- 两名人工标注者之间一致率92%，κ为0.84。

这说明裁判对样本中的二元判断较可靠，但50个样本仍不足以保证不同CWE和不同模型上的分组可靠性。

> **读完Sec. 3.3，你只需要记住：标签正确可能只是猜对了；代码审查评价也应该检查评论所依赖的调用路径和证据是否真实。**

### Research Question与证据链

#### RQ1：DREA是否提升检测可靠性？

**怎么实验**

同一backbone比较：

- Function-only；
- Whole-file；
- Single-agent；
- DREA。

主要指标包括Recall、FPR、F1、Pair-Correctness和Youden’s \(J\)。

**核心结果**

| Planner       | Function-only P-C | DREA P-C |   变化 |
| ------------- | ----------------: | -------: | -----: |
| DeepSeek-V3.2 |               19% |      42% | +23 pp |
| GLM-4.7       |               26% |      34% |  +8 pp |
| GPT-5.2       |               21% |      30% |  +9 pp |

DeepSeek-V3.2的详细结果：

- Function-only：Recall 39%、FPR 32%、F1 45.6%、P-C 19%；
- DREA：Recall 80%、FPR 45%、F1 71.1%、P-C 42%。

DREA并不是纯粹降低误报：DeepSeek的FPR上升13个百分点，但Recall上升41个百分点，因此整体判别改善。

**结论能有多强**

同backbone的Function-only对照支持“增加仓库级agentic exploration改善结果”。但它同时引入Explorer、工具、结构化压缩、多轮交互和更大计算预算，不能识别其中哪个组件是原因。

#### 消融：结构化探索是否比简单增加上下文更好？

DeepSeek-V3.2结果：

| 设置          | Recall |  FPR |    F1 |  P-C | API tokens/样本 |
| ------------- | -----: | ---: | ----: | ---: | --------------: |
| Function-only |    39% |  32% | 45.6% |  19% |              3K |
| Whole-file    |    57% |  41% | 57.6% |  26% |             20K |
| Single-agent  |    73% |  64% | 61.6% |  24% |            442K |
| DREA          |    80% |  45% | 71.1% |  42% |             88K |

这支持两个判断：

- 简单加入整文件有帮助，但远不如DREA；
- 让单个强模型直接探索会获得很高召回，却产生大量误报和上下文膨胀。

但DREA与Single-agent的差异不只是“角色是否分离”：

- DREA引入额外的GLM-4.7-Flash；
- 原始代码被转化成结构化证据；
- Planner实际看到的token显著减少；
- 两个设置的模型调用、提示和信息形式不同。

论文脚注也承认模型级差异无法完全隔离。因此“角色分离造成提升”仍不是完全识别的因果效应。

#### RQ2：成本是否降低？

平均每个样本：

| Planner       |  总tokens | Planner tokens | Explorer tokens | 付费API比例 |
| ------------- | --------: | -------------: | --------------: | ----------: |
| DeepSeek-V3.2 | 1,397,669 |         87,847 |       1,309,822 |        6.3% |
| GLM-4.7       | 1,560,519 |         32,557 |       1,527,962 |        2.1% |
| GPT-5.2       |   345,691 |          8,357 |         337,334 |        2.4% |

因此93.7%–97.9%的token被转移至本地Explorer，作者估计付费API成本降低16–48倍。

但这个数字不包括：

- 本地A800 GPU成本；
- 推理时延；
- 能源和运维成本；
- 不同API模型的输入、输出价格差异。

因此准确说法应是“减少付费Planner API token成本”，而不是完整系统成本降低16–48倍。

#### RQ3：哪些漏洞容易检测？

DREA对具有明确source–sink结构的问题表现较好：

- DeepSeek在CWE-79上的P-C为69.2%；
- CWE-94为71.4%；
- CWE-502在不同模型上为42.9%–57.1%。

需要推断“本该存在但缺失的保护措施”的问题较难：

- CWE-284仅0%–20%；
- CWE-20为14.3%–28.6%。

不过这些CWE子组只有3–13个pair，不能把数值差异视为稳定效应。

#### RQ4：探索更多是否改善分析？

作者发现：

- DeepSeek的false negative平均使用1.70M tokens；
- true positive平均使用1.24M，失败样本高约37%；
- token数量与预测正确性的Pearson \(r\approx-0.34\)；
- 不同结果的工具调用数都约为9.2–10.0次。

论文据此认为“更多探索并不可靠地改善分析”。

这里必须区分关联与因果。更合理的DAG是：

\[
TaskDifficulty\rightarrow ExplorationLength
\]

\[
TaskDifficulty\rightarrow Failure
\]

困难样本让Agent持续搜索，同时也更容易失败。因此，观察到长轨迹与失败相关，不能推出“延长探索导致失败”。

此外，是否继续探索由Planner根据当前证据决定，Exploration Length还是一个动态的post-treatment变量。

要真正回答这个RQ，应随机设置最大轮数或token预算，例如2、5、10、15轮，再比较同一实例的结果。

#### RQ5：标签正确是否代表推理正确？

DREA中Lucky Hit Rate：

- DeepSeek-V3.2：55.0%；
- GLM-4.7：45.8%；
- GPT-5.2：32.1%。

所有设置综合来看，26%–55%的true positives带有错误推理。

DREA的Reasoning Accuracy有时低于Function-only。例如：

- DeepSeek：45% vs 59%；
- GPT-5.2：68% vs 74%。

作者认为这是composition effect：DREA发现了更多困难漏洞，所以新增TP更难解释。这个解释合理，但未通过相同样本的配对推理质量分析完全验证。

不过DREA产生的“正确标签且正确推理”绝对数量仍更多：

- DeepSeek：36 vs 23；
- GPT-5.2：36 vs 31；
- GLM：32 vs 29。

### 数据集、基线与指标

- **Dataset**：100个Python CVE漏洞—修复pair，200个实例，48个CWE。
- **Planner**：GPT-5.2、DeepSeek-V3.2、GLM-4.7。
- **Explorer**：本地4-bit GLM-4.7-Flash，A800 GPU。
- **Baselines**：Function-only、Whole-file、Single-agent。
- **检测指标**：Recall、FPR、F1、Youden’s \(J\)。
- **配对指标**：Pair-Correctness，以及P-V、P-B、P-R。
- **推理指标**：Reasoning Accuracy、Lucky Hit Rate。
- **成本指标**：Planner/Explorer tokens及估算的付费API比例。

### 局限与可质疑点

#### 作者承认的局限

- 只有100个CVE pair；
- 仅覆盖Python；
- 每个CWE只有3–13个样本；
- GPT-4.1裁判仅人工核验50例；
- 公开CVE可能进入模型训练数据；
- Explorer偶尔产生不正确的工具调用；
- 修复版本发现其他真实漏洞仍会被计作误报。

#### 进一步值得质疑

1. **公开CVE泄漏不能由同backbone对照完全排除**
   配对对照能减轻总体记忆优势，却不能排除仓库探索帮助模型定位记忆中的特定CVE。

2. **Single-agent消融不是纯角色干预**
   模型数量、信息压缩、上下文形式和API预算同时变化。

3. **默认解码参数可能导致不可复现**
   论文没有报告每个样本的重复运行次数及跨seed方差。

4. **成本比较缺少统一资源口径**
   只计算付费API token，没有计算本地GPU和时间。

5. **Reasoning Accuracy存在选择条件**
   RA仅在true positives中计算。不同方法选出的TP集合不同，直接比较RA会受到selection bias。

6. **“更多探索效果更差”不具因果识别**
   任务难度和Planner停止策略共同决定轨迹长度与结果。

7. **Pair-Correctness严格但仍不等于实际价值**
   没有评估开发者是否接受报告、定位是否可操作或修复建议是否正确。

### 与 Causality for Code Review 的具体联系

DREA最适合迁移到你的“仓库上下文干预”实验。

可以设计：

- **Treatment A**：是否提供调用图；
- **Treatment B**：固定检索还是假设驱动检索；
- **Treatment C**：原始代码直接输入还是结构化证据摘要；
- **Outcome**：评论正确性、证据路径正确性、误报率、成本；
- **Mediator**：检索到的相关文件比例、实际token、工具调用轨迹；
- **Moderator**：缺陷是否跨文件、调用距离、变更规模、任务难度；
- **Confounder/固定条件**：模型、温度、预算、提示和仓库版本。

特别值得移植Lucky Hit：

> 一条代码审查意见即使指出了真实问题，如果引用了错误调用关系、错误变量传播或不存在的仓库事实，也应被判为“评论正确但证据错误”。

这可以拆成两个Outcome：

1. `Issue Correctness`
2. `Evidence/Path Correctness`

避免仅凭最终评论语义匹配高估模型能力。

### 可直接借鉴的三点

1. 构造“变更前—修复后”或“有调用图—无调用图”的配对实例，使用Pair-Correctness避免模型始终报告有问题。
2. 随机操纵探索轮数或token预算，真正估计探索深度的剂量—反应关系，不对自然产生的轨迹长度作因果解释。
3. 将审查评论分解为结论、根因、调用路径和修复机制四个维度，单独报告Lucky Review比例。

### 最终Takeaway

- DREA提出强Planner与轻量Explorer协作的假设驱动仓库探索。
- Pair-Correctness从19%–26%提高到30%–42%，改善在三个Planner模型上均出现。
- 93%以上token被卸载给本地Explorer，但16–48倍仅指估算的付费API成本。
- 26%–55%的正确漏洞标签具有错误推理，单看Recall会严重高估能力。
- 最大的因果问题是角色分离、模型、信息压缩和预算没有完全解耦，轨迹长度分析还受到任务难度混杂。

> **如果一周后只记得这篇论文的一件事：不要只验证Agent最后说对了什么，还要验证它引用的仓库证据和调用路径为什么能支持这个结论。**

- **阅读优先级**：★★★★☆
- **建议投入时间**：30分钟
- **是否值得阅读全文**：否
- **时间有限最应该读**：Sec. 3.1–3.3、Table 3、Table 5、Figure 4
