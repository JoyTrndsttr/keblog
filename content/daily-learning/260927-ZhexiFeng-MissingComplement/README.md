# The Missing Complement: State-Conditioned Minimal Sufficient Evidence for Coding Agents

论文由 Zhexi Feng、Ruiyi Zhang、Yongbo Yang 和 Pengtao Xie 完成，2026 年 9 月 17 日提交 arXiv，共 32 页。四位作者均来自 University of California San Diego 的 Electrical and Computer Engineering 系；论文脚注明确标注 Pengtao Xie 为通讯作者。

- 原文：[arXiv:2609.20050](https://arxiv.org/abs/2609.20050)
- 代码与 Benchmark：[SERBench](https://github.com/LordTARN1SHED/SERBench)

## 先把整篇论文装进脑子里

这篇论文提出一个很具体的问题：

> Coding Agent 已经搜索、读文件并形成当前假设以后，检索器下一次应该继续给它什么？

传统检索器通常仍然拿 issue 或当前 query 去给每个代码片段独立打“相关性分”。作者认为这里遗漏了两个事实。

第一，Agent 已经读过一些内容。一个片段即使与 issue 高度相关，只要它重复已知信息，对当前决策的新增价值就可能为零。

第二，决策往往需要一组互补事实共同成立。例如要决定修改某个调用点，可能同时需要：

- 被调用函数的真实行为；
- caller 对返回值的假设；
- 配置分支何时启用。

如果 Top-5 全是第一类事实的近似副本，单条相关性都很高，整个集合仍然不充分。

作者因此把目标从 passage relevance 改成 **state-conditioned minimal sufficient evidence recovery**：给定 Agent 当前可见状态，检索一个紧凑证据组合，使它覆盖“下一决策尚未解决的所有必要事实组”。

全文的顶层证据链是：

```text
逐片段相关性排序
        ↓
可能重复已知信息，也可能只覆盖一个事实
        ↓
把 Agent 当前状态与已观察证据显式记录下来
        ↓
为下一决策标注尚缺的多个证据组
        ↓
SERBench 评价返回集合是否完整覆盖所有组
        ↓
MSS-Complement 以“当前集合还缺什么”为目标迭代选证据
        ↓
用 matched control、drop-one-group、定位与真实测试验证
        ↓
完整证据组合比相似片段堆叠更能支持下一步决策
```

理解全文需要先分清四个概念。

### 1. State-conditioned

检索目标不是固定由 issue 决定，而是由 Agent 当前状态决定。论文把状态写成：issue、当前信息需求、可见 trajectory 摘要、已经观察到的源代码证据、当前假设和子目标。

同一个 issue 在搜索前、读完一个文件后和准备编辑前，需要的证据可能完全不同。Figure 1 用两个时刻说明：在 `t1` 同时缺错误处理与日志证据，到 `t2` 错误处理已经被观察，只剩日志事实仍未解决。

### 2. Evidence group

一个证据组代表一个必须被支持的事实角色。组内可以有替代来源，组间则通常是合取关系。

例如：

```text
Group A：证明 parser 的实际行为
  parser.py 的实现 OR 对应规范化测试

Group B：证明 caller 依赖某个返回语义
  caller_1.py OR caller_2.py

充分集合 = 覆盖 A AND 覆盖 B
```

这比把所有“相关文件”平铺成一个 Gold 列表更接近真实决策，因为同一事实可以有替代证据，但两个不同事实不能互相抵消。

### 3. Minimal sufficient evidence

这里的 minimal 不是说算法返回了全局数学最小集合。它主要约束标注证书：只有删除后会削弱下一决策支持的 requirement 才应该保留。

论文真正评价的是：返回集合是否在 budget 内覆盖一个充分组合。作者很谨慎地指出，这不是证明返回集合本身最小。

### 4. Complement

Complement 指相对于已观察证据的“缺口”。检索不再只问：

> 哪段代码最像当前 query？

而是问：

> 当前已选集合和 Agent 已知状态还缺哪个事实，什么代码能补上它？

## Research Gap：为什么普通 Top-k 相关性不够？

现有 repository retrieval 已经可以使用 issue、reasoning trace、symbol、dense embedding 或 reranker。问题是这些方法大多把每个候选独立评分。

这种做法隐含了一个假设：

> 只要把最相关的若干片段排在前面，它们自然会组成足够支持决策的集合。

论文指出这个假设有两个失败模式。

### 失败模式一：重复已观察内容

作者在 21 个状态的 pilot 中发现，未屏蔽已观察内容时，state-conditioned query 的 Top-10 有 **53.3%** 已经被 Agent 看过；只按 issue 检索时是 18.1%。

这说明把 trajectory 写进 query 虽然更贴近当前推理，也可能让检索器反复返回 trajectory 刚刚提到的内容。

### 失败模式二：单条相关，集合不充分

相似度只能说某一项和 query 的关系，不能表达：

```text
至少需要一个 A 类证据
并且至少需要一个 B 类证据
```

最大边际相关性（Maximal Marginal Relevance，MMR）看似能增加多样性，但“文本不相似”不等于“补齐了不同的决策事实”。论文中 MMR 在 calibration 上选出的系数最终是 1.0，等价于原 reranker 顺序，并没有解决 joint sufficiency。

因此真正的 research gap 不是“还缺一个更强 embedding”，而是：

> 缺少以 Agent 精确决策状态为条件、显式记录已观察证据、并在集合层面评价充分性的代码检索任务。

## 任务形式化：Complete-MSS 到底算什么？

设某个状态有若干证据组。第 `j` 个组包含一组可接受证据 ID，并规定至少命中 `q_j` 个才算覆盖。

当 `q_j = 1` 时，组内是 OR；不同必需组之间是 AND。

直觉上：

```text
GroupCoverage_j = 当前 Top-k 是否满足第 j 组门槛

Complete-MSS@k = 所有必需组是否都被覆盖
```

只要缺一个必需组，Complete-MSS 就记 0。论文还允许登记完整替代分支，但 Test500 的替代分支本身也都满足 grouped requirements，所以主结果实际由“所有组同时覆盖”决定。

这与普通 Recall 有根本差别。一个三组任务命中两组时：

```text
Group Recall = 2/3
Complete-MSS = 0
```

作者同时报告 Group Recall 和 necessity-weighted recall，避免完全丢掉部分进展；但主指标故意严格，因为一项决策可能正是由于缺最后一个条件而无法成立。

## SERBench 是怎样构建的？

Figure 2 应该分三层读：

```text
真实 issue + 冻结仓库快照
        ↓
运行可记录工具行为的 Coding Agent
        ↓
在四类决策边界截取 trajectory prefix
        ↓
形成 State Card，并对齐已观察源码 Ot
        ↓
人工标注下一决策尚缺的 evidence groups
        ↓
形成私有 sufficiency certificate
        ↓
公开候选池评集合恢复；全仓库轨道评发现+选择
```

### 第一步：生成可审计 trajectory

作者使用专门 instrumented harness。Agent 会先做计划，然后执行两次搜索、每次返回八个 chunk；最多读取三个此前未打开的文件，每次约 120 行；每次观察后重新生成 retrieval intent、information need、hypothesis 和 subgoal。

Test500 使用 DeepSeek-v4-Flash、temperature 0.1、关闭 thinking。每个 issue 运行一条 trajectory，在真正提交修改前停止。

这意味着 SERBench 研究的是“准备做下一步决策时缺什么”，不是完整 patch 生成轨迹。

### 第二步：截取四类决策状态

Test500 有 500 个状态，来自 242 个真实 issue、45 个 repository：

| 决策边界 | 状态数 |
|---|---:|
| 搜索前 | 200 |
| 搜索后 | 124 |
| 文件检查后 | 104 |
| 计划编辑前 | 72 |

每个状态都带固定 base commit、issue、可见工具历史、已打开文件、搜索结果、最新测试输出、当前 diff、假设和子目标。

这里的关键是 epistemic boundary：Agent 在计划里写到某个文件，并不意味着它已经获得该文件证据；只有工具输出真正暴露源码后，才进入 observed evidence。

### 第三步：把源码切成 provenance-preserving units

仓库源码被切成保持路径、行范围、symbol、证据类型和重建来源的单元。文件读取和搜索结果再对齐到这些单元，得到 Agent 已观察集合。

重叠 chunk 会归并成 canonical unit；如果多段代码独立支持同一个事实，它们在证书中登记为 alternatives，而不是奖励重复命中。

### 第四步：标注 grouped sufficiency certificate

标注者先明确下一步 action boundary，再问：当前可见状态还缺哪些事实？每个事实由哪些源码单元支持？是否存在替代来源？至少需要几个？

一个 requirement 只有在“删除它会削弱下一步 grounded action 的支持”时才保留。证书中还记录 semantic role、necessity weight、rationale 和 source quotations。

Test500 的 required group 数量分布是：

- 1 组：216 个状态；
- 2 组：135 个；
- 3 组：121 个；
- 4 组：22 个；
- 5 组：5 个；
- 6 组：1 个。

平均 1.936 组，**284/500 的状态需要至少两个相互独立的事实组**。这也解释了为什么集合级检索不是小众边缘情况。

### 第五步：建立 Cal500 与 Test500

Cal500 有 500 个公开带证书状态，来自 174 个 repository，用于开发与调参。Test500 有另外 500 个状态，45 个 repository，与 Cal500 在 state、issue instance 和 repository 三个层面都不重叠；其证书留在私有 evaluator 中。

原始 Test500 issue pool 在生成 trajectory 前就冻结：362 个候选 issue、70 个 repository，其中 320 来自 Multi-SWE-bench、42 来自 SWE-bench-Live。经过 trajectory 完整性、状态质量、候选池可评分性和证书审核后，留下 500 个状态。

### 第六步：候选池和全仓库轨道分开

主任务提供每个状态 20–120 个候选源码单元，平均 81.01。这个池由 gold-blind 全仓库检索、后续 trajectory、gold patch 和 test patch 中发现的单元取并集，再删除来源标签。

这样做的好处是把问题拆开：

- 主轨道：候选已包含答案时，能否选出充分组合？
- Gold-blind 轨道：从完整冻结仓库出发，发现与集合选择合在一起效果如何？

但主轨道也因此不是纯现实检索。它的候选池被设计成 recall-complete，并利用了 future trajectory、gold patch 和 test patch 来确保候选可达。作者没有掩盖这一点，而是用单独全仓库诊断补外部有效性。

## 标注质量控制是否可信？

论文的 governance 比普通 LLM 标注工作严得多。

先由 Grok 4.6 和 Gemini 3.6 Flash 独立审查 500 个证书，Claude Sonnet 5 对 455 条提供 source-constrained arbitration 信号。模型结论不自动改标签，只用于暴露问题。

随后两名人类专家独立复核全部 500 个状态，再由一名 senior expert 在不知道模型判定的情况下仲裁。最终累计发生 232 次 certificate repair 和 93 次 replacement decision / mapping。

冻结后，另两名不参与构造的专家随机审计 80 个状态：

- 双方共同接受 77/80，状态级 raw agreement 96.25%；
- 155 个 group 中 151 个在八个字段上完全一致，group-level agreement 97.42%；
- 没有一个状态被两人同时标记为需要修改或重建。

作者没有用 Cohen’s kappa 粉饰结果。由于两位审计者几乎都选择 accept，类别极不平衡会产生 kappa paradox，所以论文同时报告 raw agreement 和 prevalence-adjusted 指标。

不过，高一致性只能说明按照既定规则可稳定标注，不能自动证明这些证据组具有客观因果必要性。这一点后面仍要单独讨论。

## MSS-Complement 方法从输入到输出怎样运行？

Figure 3 是方法总图，核心不是一个新 embedding，而是三次集合级语义调用：

```text
State Card + 候选证据
        ↓
九种检索视图 + Reciprocal Rank Fusion
        ↓
Proposal：先提出一个共同充分的 8-unit 集合
        ↓
Expansion：阅读当前集合，寻找仍缺的事实
        ↓
Finalization：合并、去重复、检查联合支持
        ↓
返回 4–8 个完整源码单元，≤ 6,144 source tokens
```

### Stage 0：九视图候选融合

作者对 question、full state、prior actions、observations 做多路 BM25 / TF-IDF，再加入 dense similarity、entity overlap 和 recency，共九个视图。Reciprocal Rank Fusion（倒数排名融合）把多路排序合并，最多形成 384 个候选。

这一步提供 breadth，不负责判断集合是否充分。

### Stage 1：Proposal

DeepSeek-v4-pro 读取状态、当前问题和前部候选卡片，选出八个单元，目标不是单项最相似，而是共同覆盖准确回答所需的实体、数值、条件、时间点和因果联系。

### Stage 2：Expansion

DeepSeek-v4-flash 读取 Proposal 已选集合和更深候选，明确寻找“当前集合还不支持的事实”，如缺失 endpoint、条件或状态转移。

这一步体现 complement：它必须看到当前选择，才能判断下一项的边际证据价值。

### Stage 3：Finalization

第二次 Flash 调用读取 Proposal、Expansion 候选和 reserve，并知道候选来自哪个阶段。它检查联合支持、删除重复事实、重排，最终输出 4–8 个证据单元。

只有最终完整源码单元会进入下游模型；中间候选卡片只是 controller 输入。最终 renderer 强制 source context 不超过 6,144 tokens。

### 信息访问边界

方法在推理时看不到 private certificate、group 数量、gold evidence ID、答案、reward 或 judge output。后两阶段虽然能看到当前已选集合，但不能看到“正确组还缺几个”的标签。

所有主要参数在 Cal500 固定，然后原样迁移到 Test500、全仓库诊断、AMA-Bench、Prospective44 和 Action52。

## 实验坐标系：比较对象和公平性

主实验在相同 500 个 Test500 状态和相同冻结候选池上比较 12 类方法：

- 经典 lexical / dense / sparse：BM25、BGE-large、SPLADE++、ColBERTv2；
- 现代通用或代码检索：ReasonIR、SweRankEmbed、Qwen3 Embedding；
- embedding + Qwen3 reranker；
- Agent-aware retrieval：AgentIR、Agent-ModernColBERT；
- MSS-Complement。

外部 retriever 的 query 表示只在 repository-disjoint 的 Cal500 子集上选定。语义调用 temperature 为 0。Test500 和全仓库结果使用 20,000 次、按 repository 聚类的 paired bootstrap 置信区间。

作者还设计三类关键对照：

1. **Independent similarity control**：仍用三次调用、同类 controller 和相同候选上限，但每次独立按 similarity 选，不让后续阶段看当前集合，也不使用 sufficiency objective。
2. **No-feedback / fixed-size / single-stage ablation**：拆开集合目标、selected-set feedback 和 adaptive output size。
3. **Oracle-minus-one-group**：从完整 Oracle 证据中删除一个必要组的所有替代证据，再用其他代码补满空位，使证据数量和 token ceiling 尽量保持一致。

第三类是全文对当前研究最重要的设计，因为它不再只问“好检索器是否更强”，而是直接操纵集合是否缺少一个必需事实。

## RQ1：在紧预算下能否恢复完整证据集合？

Table 1 固定相同 Test500 和候选池，改变 retrieval method。先看 Complete-MSS@5，再看 @8，最后看部分组覆盖。

关键结果：

| 方法 | Complete-MSS@5 | Complete-MSS@8 | Group Recall@5 |
|---|---:|---:|---:|
| Qwen3 Embedding + Reranker | 61.4% | 72.4% | 72.45% |
| MSS-Complement | **73.0%** | **80.6%** | **82.03%** |

在 Top-5 下提升 11.60 个百分点，95% CI 为 `[+6.89, +17.21]`；Top-8 提升 8.20 点，区间 `[+4.91, +13.85]`。

Uniform random 选择五个单元的精确期望只有 5.17%；候选池 Oracle 在 Top-5 可达 99.8%。因此 73% 虽明显更好，但距离上限仍很远。

Table 12 进一步按 source token 对齐：

- 5 items：+11.60；
- 8 items：+8.20；
- 4,096 tokens：+8.80；
- 每状态匹配 token：+11.40；
- 6,144 tokens：只剩 +0.60。

这说明优势主要发生在紧凑工作上下文，而不是预算足够大以后仍有巨大绝对差距。当 Qwen 在 6,144 tokens 下接近塞满预算时，也能达到 80.0%。

### 多组任务是否真的更受益？

是。Table 16 按 required group 数分层：

- 单组：Top-5 提升 7.41 点，区间跨 0；
- 两组：提升 15.56 点，区间完全大于 0；
- 三组及以上：提升 14.09 点，区间完全大于 0。

这与方法机制一致：当只需一个事实时，集合级策略接近普通 Hit@k；当需要多个互补事实时，逐项相似度更容易把预算浪费在同一组的变体上。

**Takeaway：** MSS-Complement 的优势主要是用有限位置覆盖互补 requirement，而不是简单找到更多“相关代码”。

## RQ2：完成证书真的会改变下一步定位吗？

作者建立 Action52：52 个任务来自 52 个不同 repository，每个任务固定一个中间状态和 repair reference。两种 executor——DeepSeek-v4-flash 与 Claude Sonnet 5——只能看提供的证据，不能继续浏览仓库，然后输出下一步应检查的 production-code targets。

所有 learned retrieval condition 在每个 task 中使用相同数量的证据单元，5–8 个，总计都为 395 个，并受 6,144 token ceiling 约束。

Table 2 左半部分的主要结果：

| Evidence condition | Complete MSS | Group Recall | DeepSeek target precision | Claude target precision |
|---|---:|---:|---:|---:|
| Qwen3 Embedding | 21.15% | 41.60% | 48.54% | 54.39% |
| Qwen3 + Reranker | 32.69% | 52.44% | 51.46% | 54.39% |
| MSS-Complement | 51.92% | 70.74% | **64.33%** | **58.48%** |
| Oracle − 1 group | 0% | 48.27% | 52.63% | 55.56% |
| Oracle-MSS | 100% | 100% | 64.91% | 66.67% |

相对 reranker，MSS-Complement 在 DeepSeek 下 fixed-budget target precision 提升 12.87 点，区间 `[+5.39, +20.36]`；Claude 下提升 4.09 点，但区间跨 0。

更关键的是 paired missing-group control。完整 Oracle 与 Oracle-minus-one 的证据数量相同，只删除 necessity weight 最大的一个组并用其他源码补位：

- DeepSeek precision 下降 12.28 点；
- Claude 下降 11.11 点。

这比“检索分高的方法定位也更好”更强，因为 evidence volume、状态、prompt、target cap 和 executor 都固定，真正变化的是一个证据组是否被覆盖。

但仍不能把它解释成每个 group 都是独立因果变量：删除规则总是选 necessity weight 最大的组，不是随机抽组；组内容类型可能系统性更关键。同时，public state 中仍保留 issue 自带的修复提示，某些被删除事实可能从状态文本间接推断。

**Takeaway：** 对下一步定位来说，“是否补齐全部事实组”比一般 group recall 更接近有决策意义的处理变量；删除一个高必要性组会在两个 executor 上一致降低局部目标精度。

## RQ3：能否影响真正执行测试的修复结果？

Fresh23 是 23 个冻结任务的 end-to-end 小型 cohort。每个任务执行：

```text
检索证据 → Executor 生成 patch → 应用 patch → 跑 repository tests
```

Strict resolution 要求 fail-to-pass tests 转绿，同时选定的 pass-to-pass 邻域继续通过。

| Condition | Strict resolved | Fail-to-pass | Mean API tokens |
|---|---:|---:|---:|
| BM25 | 5/23 | 8/23 | 133,775 |
| Qwen3 + Reranker | 6/23 | 10/23 | 126,261 |
| MSS-Complement | **8/23** | 10/23 | **118,351** |
| Oracle − 1 group | 7/23 | 8/23 | 98,121 |
| Oracle-MSS | 8/23 | 11/23 | 99,655 |

MSS-Complement 的 strict resolution 达到 Oracle 的 8/23，并且是三种 deployable condition 中平均 API token 最低的。但样本只有 23，MSS 对 reranker 的 strict difference 为 +8.70 点，95% interval 是 `[-13.04, +30.43]`，明显不能宣称稳定显著提高 end-to-end repair。

Oracle-minus-one 相对 Oracle 在 fail-to-pass 上少 3 个成功，差值 +13.04 点，bootstrap 下界恰为 0；在 strict resolution 上只差一个，区间跨 0。

另一个重要 negative result 是 candidate target-file hit 并不按最终修复率排序：BM25 命中 22/23 个 reference file，却只严格解决 5 个；MSS-Complement 命中 20 个，却解决 8 个。找到“patch 涉及的文件”不等于提供了支持正确修改的充分证据。

**Takeaway：** Fresh23 给出了方向一致的 downstream validation，但样本太小，只能作为支持性证据；它最清楚地说明 file hit 是很粗的 mediator，不能替代 evidence sufficiency。

## RQ4：能否迁移到全仓库发现和长轨迹 QA？

### Gold-blind full-repository

从冻结仓库源码开始，BM25 Top-1000 中只有 333/500 状态包含完整 certificate。所有状态上，MSS-Complement 的 Complete-MSS@5 为 38.8%，reranker 为 33.8%，提升 5.00 点；只看 coverable 333 个状态时是 58.26% vs 50.75%，提升 7.51 点。

这一区分很重要：

- All-500 结果混合 candidate discovery 与 set selection；
- Coverable-333 条件化于 discovery 已成功，只评价后续选择。

不能只报 coverable 结果并说真实全仓库性能提高 7.51 点，因为它排除了发现失败的状态。

### AMA-Bench

在 208 个真实 agent episode、2,496 个问题上，MSS-Complement 用统一 answer model 和 judge 得到 56.05%，AMA-Agent 为 53.97%，差 2.08 点，episode-clustered interval `[-0.16, +4.37]`。

它的 answer prompt 从 13.06K 降到 3.10K，缩小 76.2%；但构造这个紧凑 prompt 需要平均 29.62K controller tokens，总 online total 33.57K，反而高于 AMA-Agent 的 13.95K。

所以正确结论是：

> 它用更多 acquisition computation 换来更小的 answer-visible context。

不能简化成“总体 token 更省”。

### Controller family

在 44 个 prospective states 上，将 controller 从 DeepSeek 换成 Claude，Complete-MSS@5 从 45.45% 变为 52.27%。这说明策略不完全依赖单一模型家族，但 44 个状态不足以比较两种 controller 谁更强，而且服务端、成本和延迟都不同。

**Takeaway：** 集合级目标能跨候选池、任务与 controller 复现方向，但 discovery ceiling 和 controller cost 仍是主要约束。

## RQ5：提升到底来自哪里？

Table 4 是全文最重要的 attribution 表。它固定 Test500、候选生成、controller 分配、source ceiling 和大部分调用预算，逐步拆组件。

| Variant | MSS objective | Selection feedback | Complete@5 | Mean source context |
|---|---|---|---:|---:|
| Qwen reranker fixed-7 | — | — | 61.4% | 3,781 |
| Independent similarity fixed-7 | 否 | 否 | 66.6% | 3,595 |
| No feedback fixed-7 | 是 | 否 | 69.8% | 3,797 |
| No feedback adaptive 4–8 | 是 | 否 | 72.8% | 3,907 |
| Single-stage MSS proposal | 是 | 不适用 | 70.0% | 4,139 |
| MSS-Complement | 是 | 是 | 73.0% | **3,663** |

Full policy 相对 independent-similarity control 提升 6.40 点，区间 `[+3.42, +10.46]`。这说明不是单纯多花三次 semantic call。

逐步看：

- MSS objective 本身约 +3.20 点，但区间稍跨 0；
- adaptive sizing 再约 +3.00 点，区间大于 0；
- selected-set feedback 只再加 0.20 点，区间很宽、跨 0；
- expansion + finalization 相比 single-stage proposal 总计 +3.00 点。

因此不能写成“反馈机制是主要贡献”。主证据支持的是整个 set-level policy 优于 matched independent similarity；单独 feedback 的增益没有被这组 ablation 清楚识别。

还有一个很漂亮的机制检查：Top-1 时 full policy 比 independent similarity 低 1.40 点且区间跨 0；当 prefix 允许容纳多个 requirement 后，顺序才反转。这与“集合互补性只在多项选择中发挥作用”的理论预期一致。

**Takeaway：** 证据最强的是 set-level policy 的整体收益；单个子组件中 adaptive sizing 较清楚，selected-set feedback 的独立贡献尚不确定。

## Baseline 是否公平？

主候选池实验总体公平性较好：相同状态、相同候选池、相同证书和成对统计；query 表示在 disjoint calibration subset 上选；对三调用方法还构造了 matched-call independent-similarity control。

但仍有三点需要注意。

第一，MSS-Complement 使用 DeepSeek-v4-pro + 两次 Flash，很多 baseline 是无需生成调用的固定 retriever。论文通过 matched semantic-call control 识别“多调用”不是全部原因，却不意味着工程成本相同。

第二，作者自己的方法看到多路 fusion 候选和丰富 state card，不同 external retriever 的原生接口与表示能力并不完全一致。Agent-aware baselines 也可能未针对 SERBench 的 grouped target 重新训练。

第三，主候选池来自 recall-complete construction，离真实全仓库发现仍有明显距离：Oracle 在池内几乎 100%，而 gold-blind BM25 Top-1000 只有 66.6% 状态可覆盖完整证书。

因此主结果最稳妥的含义是：

> 当候选发现已经给出足够覆盖时，集合级选择比逐项相关性排序更有效。

它不等于已经解决 repository-scale discovery。

## 论文最重要的 Negative Results 和边界

### 1. 更高 Group Recall 不保证 downstream 显著提升

Reranker 相比 plain embedding 明显提高 evidence completion 和 group recall，但两个 executor 的 target precision 差异都不显著。检索指标和 action outcome 之间不是机械一一对应。

### 2. 完整证据也不保证修复成功

Oracle-MSS 在 Action52 的 Complete-MSS 为 100%，但 fixed-budget target precision 只有 64.91% 和 66.67%；Fresh23 的 Oracle strict resolution 也只有 8/23。

证据充分性是 reasoning / editing 的输入条件，不是 patch success 的充分条件。

### 3. 6,144-token 宽预算下主优势几乎消失

在统一 6,144 source-token ceiling 下，MSS-Complement 80.6%，Qwen reranker 80.0%，只差 0.6 点。论文的价值主要在紧 budget 下组合证据，而不是证明所有预算下都压倒强 reranker。

### 4. AMA 的 answer context 更小，但总在线 token 更多

76.2% smaller prompt 很醒目，但如果实际系统成本关心 controller + answer 全链路，MSS-Complement 更贵。它优化的是工作上下文，不是总计算。

### 5. Fresh23 很小，多个区间跨 0

End-to-end repair 的结果不能当成定论。作者将其称为支持性 action evidence 比较合适。

## 最大的构念风险：这些 certificate 真的是“必要且充分”吗？

SERBench 的证书经过严格 source-first annotation 与审计，但“最小充分”仍是相对于：

- 一个特定 trajectory prefix；
- 一个特定下一步 action boundary；
- 标注者认可的 repair 路径；
- 切分后的证据单元；
- 公开候选池中的可见 alternatives。

它不是对整个任务所有可能推理路径的数学证明。

尤其有四个风险。

第一，Agent 的 information need、hypothesis 和 subgoal 本身由 benchmark harness 中的模型生成。状态定义如果偏了，后续“缺什么”也会围绕这个偏置状态构建。

第二，Test500 trajectory 只来自 DeepSeek-v4-Flash。其他 Agent 可能形成不同中间状态或采用不同 solution path。Cal500 的 planner 更多样，但主测试状态的生成分布仍较单一。

第三，证据 alternatives 很难穷举。随机审计中少量分歧也主要出现在 acceptable-evidence completeness、source grounding 和 joint sufficiency。

第四，Oracle-minus-one 删除的是标注证书中的一个组，不等于从模型内部知识中删除该事实。Executor 可能从 issue、命名或预训练知识中重建它。

因此论文最强的表述是：

> 这些是经过 source-grounded audit、对指定决策具有高可信度的 sufficient evidence certificates。

而不是：

> 它们证明了代码证据在一般意义上的因果必要性。

## 作者与团队背景

第一作者 Zhexi Feng 来自 UC San Diego ECE。公开可核验资料目前主要集中在本论文和 SERBench 项目，没有足够证据把他包装成已经形成长期独立研究线的资深研究者。

通讯作者 Pengtao Xie 是 UC San Diego ECE Associate Professor，官方主页列出的长期方向包括机器学习、自然语言处理，以及受人类学习机制启发的模型设计；其个人主页近年的兴趣进一步包括 AI Agents、LLM 和 foundation models，并有医疗与生物领域应用积累。

这篇论文与团队传统的连接点不是纯软件工程，而是：把“学习/推理还缺什么证据”形式化为可评价、可干预的集合问题，再用代码 Agent 作为具体场景。SERBench 的 benchmark governance、私有 certificate evaluator 和多模型 controller 也体现了偏机器学习评测与系统构造的研究风格。

## 作者证明了什么？

1. 代码 Agent 的检索可以被形式化为状态条件下的“剩余证据集合恢复”，而不只是 issue-to-passage ranking。
2. 在 500 个 held-out states 的 recall-complete 候选池上，集合级策略在 Top-5 和 Top-8 下显著优于强 Qwen3 embedding + reranker，优势集中在需要多个证据组的状态。
3. 三调用 matched control 表明收益不只是更多 semantic computation；整体 set-level objective、adaptive size 与 staged revision 共同贡献。
4. 在 Action52 中，从相同数量的完整 Oracle 证据删除一个必要组，会在两个 executor 上分别损失约 12.3 和 11.1 个百分点的目标精度。
5. 全仓库、AMA-Bench、prospective controller-family 和 Fresh23 提供了方向一致但强度不同的外部与下游证据。

## 作者没有证明什么？

1. 没有证明 certificate 中每个组在所有模型、所有 solution path 下都具有普遍因果必要性。
2. 没有证明 MSS-Complement 已解决全仓库 candidate discovery；主任务首先假定 recall-complete pool。
3. 没有证明 selected-set feedback 单独是核心贡献；它的独立 ablation 增益只有 0.2 点且区间跨 0。
4. 没有证明更高 Complete-MSS 必然带来更高 end-to-end repair；Fresh23 很小，Oracle 也远未达到 100% 修复。
5. 没有证明方法总体更省 token 或成本；answer-visible context 更小，但 acquisition controller 消耗更大。
6. 没有研究 plausible-but-non-decisive context 是否比随机上下文更有害。它主要研究 missing decisive evidence，而不是 extra distractor 的干扰效应。

## 真正应该记住什么？

1. **相关性是单项属性，充分性是集合属性。** Top-k 每项都很像 query，仍可能漏掉一个决定性事实。
2. Agent 的证据需求随 trajectory 改变；同一 issue 不应该从头到尾使用同一个静态 Gold Context。
3. Grouped certificate 用“组内 OR、组间 AND”表达替代证据与互补事实，比平铺 Gold 文件列表更贴近决策。
4. Complete-MSS 是严格的 sufficiency endpoint，Group Recall 是部分进展；两者都需要，不能相互替代。
5. Drop-one-required-group 是连接 benchmark metric 与下游 action 的关键实验，比单纯相关性分析更接近机制验证。
6. 即使证据完整，定位和修复仍会失败；evidence acquisition、reasoning、editing 和 validation 必须分开评价。

# 对当前研究的启发

这篇论文与当前 VLocBench 主线最直接的连接，不是照搬 MSS-Complement，而是重构实验中的“Core”定义。

## 1. 把 Core 从节点列表改成 decision-specific evidence groups

当前 patch-aware node context 容易形成：

```text
Patch node 1
Patch node 2
Path bridge
Seed node
```

但这些是来源类别，不一定等于决策需要的事实类别。更稳妥的表示是：

```text
Decision：判断漏洞机制并定位 patch-associated node

G1：危险行为实际在哪里发生
G2：输入/状态如何到达该行为
G3：哪条约束没有被满足
G4：为什么 sibling 不是决定性位置
```

每组再绑定一个或多个 RDFS / source units。这样才有可能区分：

- 同一事实的冗余证据；
- 不同事实的互补证据；
- 看起来相关但没有新增 requirement coverage 的 plausible context。

## 2. sufficient-core gate 应该发生在具体 outcome 之前

不能笼统问“core-only 能不能解题”。至少要拆成：

```text
Core → Mechanism Correctness M
Core → Attribution Correctness A
Core → Patch-node / Patch-file localization
```

一个 context 可能足够判断机制，却不足够定位文件；也可能足够定位文件，却不足够解释根因。

因此每个实验实例应先声明 decision boundary，再验证相应 sufficiency。否则 `core + plausible` 的下降可能只是 baseline core 本身缺证据。

## 3. 直接加入 Oracle-minus-one-group 对照

现有五条件可以扩展为：

```text
core-complete
core-minus-Gj
core + plausible
core + matched-random
core + potentially-useful
```

其中 `core-minus-Gj` 必须：

- 固定文件数或节点数；
- 固定 token budget；
- 用其他非该组代码补位；
- 检查被删除组是否通过重叠 window 泄漏；
- 不改变 prompt、顺序分布和模型参数。

如果删掉任何组都不影响 M/A/localization，就说明当前“Core”标签可能只是 patch-associated，而不是 decision-relevant。

## 4. plausible-but-non-decisive 可以定义为“高相关、零增量组覆盖”

SERBench 给出了比“非 GT sibling”更可审计的定义：

> 一个候选与 state/query 高度相关，但在当前已选集合下，不覆盖任何尚未满足的 evidence group，也不构成新的完整替代分支。

这正好对应当前要研究的 plausible context。它比以下定义更稳：

```text
non-GT = distractor
非路径节点 = 无用
sibling = plausible
```

因为 structural sibling 可能恰好提供缺失事实，而 retrieval-plausible 也可能只是重复已知证据。必须先做 group-level incremental evidence audit。

## 5. 把实验效应拆成 acquisition、retention 与 attribution

结合 ContextBench、SWE-Explore 和本文，可以形成更完整的 mediator chain：

```text
Treatment：extra context type
        ↓
Required-group coverage / Complete certificate
        ↓
Evidence retained or cited
        ↓
Mechanism correctness M
        ↓
Attribution correctness A
        ↓
Patch-node / file outcome
```

当前最值得观察的仍是 `P(M=1, A=0)`：模型机制判断正确，但把责任归到 plausible sibling。如果 Complete certificate 在所有 condition 中保持不变，而 attribution 只在 plausible 下偏移，才更接近“额外可信相关上下文造成归因干扰”的机制证据。

## 6. 这篇论文同时构成一个反方向提醒

SERBench 的主要收益来自补齐 missing decisive evidence；在 6,144-token 宽预算下，强 reranker 与 MSS-Complement 几乎持平。它没有证明多余 context 本身会伤害模型。

因此当前论文故事仍不应预设：

> plausible context 一定比 random 更坏。

更稳妥的主假设是：

> 在 decision-specific sufficient core 已经成立、预算与排序匹配时，plausible-but-non-decisive context 是否比 matched random context 更容易造成 evidence attribution shift？

如果结果是 plausible ≈ random，也仍然有解释价值：说明决定性能首先受 missing evidence 支配，而不是被少量 plausible context 轻易干扰。

**这篇论文最值得带走的不是 73.0% 这个数字，而是一套实验纪律：先明确当前决策，记录模型已经看过什么，用组内替代、组间互补的 certificate 定义“还缺什么”，再通过 drop-one-group 检查这些证据是否真的有下游决策价值。对当前 VLocBench，下一步最重要的升级是把 patch-aware Core 从结构节点集合提升为经过 sufficiency 和 deletion test 的 decision-specific evidence groups；只有在这一步成立后，plausible-vs-random 才能被解释为额外上下文干扰，而不是缺失证据差异。**
