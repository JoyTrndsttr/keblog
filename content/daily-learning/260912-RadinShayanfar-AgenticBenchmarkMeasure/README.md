# What Does an Agentic Software Engineering Benchmark Measure? Profiling Task Demands and Agent Behaviour Beyond What Category Labels Reveal

> 精读日期：2026-09-12  
> 作者：Radin Shayanfar, Keheliya Gallaba, Ahmed E. Hassan  
> 机构：Queen’s University  
> arXiv：[2609.01271](https://arxiv.org/abs/2609.01271)  
> 代码：[task_snc](https://github.com/radinshayanfar/task_snc)

## 一句话价值

这篇论文真正质疑的是：**我们把 benchmark 叫做 “bug fix” 或 “feature implementation”，然后把模型分数解释成对应能力——这个解释真的成立吗？** 作者提出 Spread–Novelty–Centrality（SNC）三轴画像，对 5 个 Agentic SE benchmark 的 2,487 个任务进行刻画，又分析 Claude/Qwen 两个模型 family、三个规模，共 14,922 条 Agent trajectory。最重要的结果是：同样的类别标签远不能保证任务要求相同；而低 SNC 需求与 Agent 成功的关系反而跨 family 和规模相对稳定。

## 先建立论文地图

过去 Agent benchmark 的解释链通常是：

```text
SWE-bench = bug fix
FeatureBench = feature implementation
        ↓
模型在 FeatureBench 更高
        ↓
模型的 feature implementation 能力更强
```

问题在于，这个逻辑中间跨得太快。两个都叫 feature implementation 的 benchmark，可能采用完全不同的 PR 筛选方式、testability 条件、problem statement 重写方式、hint 与 gold solution 构造过程。

作者因此把问题拆成四层：

```text
Benchmark Construction
        ↓
Task Demand
        ↓
Agent Behaviour
        ↓
Outcome
```

并围绕三个问题展开：

1. Gold Patch 所隐含的 task demand 到底是什么？
2. Agent patch 与 trajectory 能暴露 Gold Patch 看不到的哪些要求？
3. 哪些 task demand / behaviour 与 resolved outcome 稳定相关？

## 四个最重要的概念

### 1. Nominal Category：名字不是能力本身

“bug fix”“feature implementation”只是类别标签。它没有告诉你：需要改 1 个文件还是 10 个文件、是否跨 subsystem、主要新增还是重写、改的是边缘 helper 还是系统核心、problem statement 是否已经把目标函数告诉 Agent。

所以作者实际在做的是 **construct validity**：benchmark score 到底代表什么能力？

### 2. Gold Patch：重要，但不等于任务本身

Gold patch 是开发者原来的正确 solution，可以告诉我们人类最终改了哪些地方。但正确解不唯一；Agent 可以解决同一个任务，却改不同文件、写更多或更少代码、采取不同架构。Gold 只是一个正确实现。

而且 Gold 不包含问题描述的信息量。两个最终 patch 完全一样的任务，如果一个只写“Fix parsing issue”，另一个直接告诉你“Modify `Parser.normalize_token()`”，实际 localization 难度显然不同。

### 3. Task Demand 和 Agent Behaviour 不是一回事

Task Demand 问：**任务本身要求做什么？** 作者用 SNC 来描述。

Agent Behaviour 问：**Agent 实际怎么做？** 例如最后改多少文件、多少行、多少 callable，浏览多少文件，浏览范围相对于最终 patch 有多宽。

把两者分层非常重要，否则很难判断：是任务本身困难，还是 Agent 策略有问题。

### 4. Association 仍然不是 Causation

RQ3 会发现 SNC 高的任务更容易失败，但作者没有随机把同一个任务的 Spread 从 0.2 调到 0.8。所以严格结论只能是“High Spread 与失败相关”，不能写成“High Spread 导致失败”。

## 为什么 Patch Size 不够？

两个任务都改 200 行，但一个集中在单文件、另一个分布在 10 个文件，工程协调需求显然不同。又或者一个是新增独立 helper，另一个是重写核心 parser；行数相同，但需要理解旧行为和依赖的程度完全不同。

所以作者关注的是**工程工作的形态**，而不是单纯 change volume。

## SNC：Spread–Novelty–Centrality

作者给任务定义：

\[
t_i=(Spread(P_i^*), Novelty(P_i^*), Centrality(P_i^*))
\]

其中 \(P_i^*\) 是 Gold Patch。

### Spread：任务需要跨多大的代码空间协调？

Spread 有两个指标。

**Normalized Entropy** 衡量改动量在 touched files 之间分布得均不均匀：

\[
H(P)=-\frac{1}{\log_2 n}\sum p_k\log_2p_k
\]

\[
p_k=\frac{\Delta_k}{\sum_f\Delta_f}
\]

接近 0 表示改动高度集中；接近 1 表示多个文件均匀承担改动。

**Radius** 则进一步考虑这些文件在 repository directory tree 中离得有多远。Entropy 更关心“改动量有多分散”，Radius 更关心“改动位置跨了多少结构边界”。

### Novelty：你是在创造，还是在理解并修改旧行为？

\[
Novelty=\frac{Add}{Add+Delete}
\]

接近 1 表示主要新增；接近 0.5 表示 in-place rewrite；接近 0 表示主要删除。

作者关心的不是公式本身，而是新增和 rewrite 对工程理解的要求可能不同。大量 rewrite 往往需要把新逻辑真正融合进已有行为。

### Centrality：你动的是边角，还是架构核心？

Centrality 使用四类 proxy：

- **Fan-in**：多少 module import 当前 module；
- **Fan-out**：当前 module 依赖多少 module；
- **Churn**：过去 180 天相关文件被 commit 触碰的频率；
- **Mass**：source lines 与 McCabe complexity 的组合。

这里必须强调：它主要基于 module import graph 和历史/复杂度 proxy，**不是 call graph centrality**。

## RQ1：同样叫 Feature Implementation，实际测的是同一种东西吗？

作者分析五个 benchmark：

- SWE-bench Verified；
- SWE-Gym Lite；
- FEA-Bench；
- FeatBench；
- FeatureBench。

总计 2,487 个任务。

作者先用 Conventional Commits taxonomy 检查 problem statement，发现表面标签并没有错：SWE-bench / SWE-Gym 多数确实是 fix，另外三个多数是 feat。真正的问题是：**标签太粗。**

Figure 3 用 Scott-Knott ESD 对五个 benchmark 在 Spread、Novelty、Centrality 上分簇。核心结果不是某个均值，而是：**任意两个 benchmark 至少在两个 SNC axes 上分开；三个都叫 Feature Implementation 的 benchmark 也没有形成统一的一簇。**

### Benchmark construction 会留下需求指纹

这部分是全文最值得记的地方之一。

**FeatBench** 为了 testability，只接受“修改已有函数，但不能增加或删除函数”的 PR，于是任务被结构性推向 in-place rewrite，Novelty 反而会和 bug-fix benchmark SWE-Gym Lite 落到相近 cluster。

**FeatureBench** 采用 test-first construction：先找到被 test 覆盖的代码，再 carve out implementation 留下 stub，让 Agent 补回来。因此 Gold Patch 本质上大量是“把删掉的代码重新加回来”，Novelty 被结构性推向接近 1。

**FEA-Bench** 专门选择新增函数 / class 的 PR，新组件天然 fan-in≈0、历史 churn≈0、mass 通常较低，因此会被推向 low Centrality。

真正的结论是：**benchmark construction pipeline 不是中性的“数据清洗”，而是 measurement design。**

## RQ2：Gold Patch 为什么仍然不够？

两个任务即使 Gold Patch 一样，problem statement 是否告诉你 target file/function，也会明显改变实际定位需求。因此作者进一步看 Agent patch 与 trajectory。

作者选择 Claude Opus 4.6 + Claude Code 的 resolved runs，共 1,083 个任务。只看成功 run 的原因是：如果失败时 Agent 改了很多文件，那可能只是“迷路了”；成功 run 中，Agent patch 与 Gold patch 都是有效实现，它们的 scope 差异更有解释力。

### Patch Verbosity

作者对 files / lines / callables 分别定义：

\[
\rho=\log_{10}\frac{Agent}{Gold}
\]

- \(\rho=0\)：Agent 与 Gold 规模接近；
- \(\rho>0\)：Agent over-produce；
- \(\rho<0\)：Agent 比 Gold 更紧凑。

### FeatBench：Agent 明显 over-produce

FeatBench 不提供 hint，也不提供明确 target surface。成功 Agent 往往修改比 Gold 更大的 scope。一个合理解释是：Agent 不知道 solution boundary，所以扩大搜索和修改范围。

但这不是随机 hint 实验，因此不能把差异直接归因于“没有 hint”。

### FeatureBench：Agent 反而比 Gold 小

FeatureBench 的成功 Agent patch 明显更 compact。作者进一步发现，Gold Patch 中 **33.8% 的 lines 是 comment 或 docstring**；测试不会要求 Agent 恢复这些文字，因此 Agent 可以用更小 patch 通过。

这暴露出：**Gold Patch ≠ Minimal Required Solution。** Gold 有时会被 benchmark construction inflate。

### FEA-Bench：更接近 parity

FEA-Bench 会给 function signatures 与 docstrings，solution surface 已经相对明确，因此 Agent 成功解更接近 Gold。

这说明 **task wording 本身就是 task demand 的组成部分**。

### Exploration Breadth：反直觉的“没区别”

作者计算：

\[
\rho_{explore}=\frac{Trajectory\ touched\ files}{Final\ edited\ files}
\]

结果五个 benchmark 的 exploration breadth 在 Scott-Knott 中全部进入同一 cluster，没有显著 benchmark-level 区别。

作者提出一种解释：broad reading + narrow editing 可能更像 Agent 的固有策略，而不是 benchmark-specific response。

但另一种同样值得研究的可能是：Agent 并没有很好地根据 task demand 自适应搜索。论文没有进一步区分这两种机制。

## RQ3：SNC 是否真的与成功有关？

作者使用六个配置：

Claude：Haiku 4.5、Sonnet 4.6、Opus 4.6，运行于 Claude Code；

Qwen：Qwen 3.5 9B、27B、397B-A17B，运行于 Qwen Code。

合计 14,922 条 trajectory。

### Figure 5a：成功稳定集中在 Low-SNC

作者把 SNC indicator 分成 quantile bins，再分别看 resolved 与 unresolved 的分布。结果相当稳定：**resolved runs 更多集中在低 demand bins，unresolved runs 向高 SNC 偏移。** 这一趋势跨 Claude/Qwen 和不同规模存在。

这说明 SNC 至少捕获了与任务成功高度相关的结构属性，而不是纯粹为了“把 benchmark 分开”。

### Novelty 是一个重要例外

Novelty 不是“越低越容易”。结果更像两端容易、中间难：接近纯新增或纯删除时 resolved 更多，大量 Add + Delete 的 rewrite 区域失败更多。

一种可能解释是，rewrite 需要同时理解旧行为和新行为并完成融合。但论文没有单独验证该机制。

### Figure 5b：Task-demand 规律较稳定，成功 Behaviour 却不通用

Claude 的 resolved run 随模型变大越来越靠近 Gold parity。以 Files 为例，Small Claude parity share 约 0.17，Medium 约 0.41，Large 约 0.54。

Qwen 则不同：即使模型变大，成功 runs 仍大量 over-produce，Files ratio >2× Gold 的占比大约 0.6–0.7，parity 约 0.2。

因此“Minimal Diff is always better”并不是跨 family 稳定规则。

两个 family 更一致的失败信号是 **under-editing**：Agent patch 明显小于 Gold scope 时，更容易失败。

## 主动审查：这篇论文能支持多强的 Claim？

### 1. Claude vs Qwen 同时换了模型和 harness

Claude 使用 Claude Code，Qwen 使用 Qwen Code。因此所谓 family-specific behaviour 实际上是 **model-family + harness-specific behaviour**。若要估计 Model Family 的纯效应，应该固定 harness，或做 \(Model\times Harness\) 析因实验。

### 2. Gold Patch 定义 Task Demand，有 Reference Solution Bias

如果 Gold 解改 5 个文件，而 Agent 找到一个同样正确但只改 2 个文件的解，那么这个任务究竟是“5-file spread”还是“2-file spread”？RQ2 已经表明这种情况真实存在。

所以 SNC 更准确的说法是：**Gold-solution-implied task demand**，不是唯一真实 difficulty。

### 3. Centrality 不是 Call Graph Centrality

本文 Fan-in/Fan-out 主要来自 module import graph，不是 runtime/static call graph、control dependency 或 data dependency。

因此“High Centrality 与失败相关”绝不能翻译成“Call Graph 很重要”。

### 4. Task Property 和 Information Treatment 必须分开

“某任务具有高 cross-file dependency”是 task property；“给 Agent call graph”是 intervention。本文研究的是前者与 success 的关联，没有证明提供 structural context 会改善 success。

## 对 Causality for Code Review 的直接启发

你之前的问题经常被写成：

\[
ATE=E[Y(CG)-Y(NoCG)]
\]

即“Call Graph 平均提高多少”。

但这篇论文提醒我们，所谓 Task Difficulty 可能根本不是一个标量，更适合拆成：

```text
Task Demand
├── Spread
├── Centrality
├── Cross-file dependency
├── Evidence density
├── Change type
└── Context need
```

这些变量都可以成为 effect modifier，于是更有价值的问题是：

\[
CATE(CG\mid Spread, ContextNeed, Centrality)
\]

例如：

```text
No-context-needed + Low Spread + Low Centrality
CG → -8%

Repo-level-required + High Spread + High dependency
CG → +12%
```

聚合后 ATE 可能接近 0，但真实现象是强 treatment heterogeneity。

## Agent Behaviour 可以进一步作为 Mediator

这篇论文证明 trajectory 能提供 Gold Patch 看不到的信息。你可以进一步把它放进机制链：

```text
Context Treatment
        ↓
Exploration Behaviour
        ↓
Evidence Exposure
        ↓
Review Outcome
```

可记录的 mediator 包括：

- explored files；
- opened functions；
- call graph hops；
- relevant evidence recall；
- irrelevant evidence ratio；
- repeated visits；
- search depth；
- context switches；
- token spent on irrelevant files。

这样“Context Noise”才能从 Discussion 里的解释词变成真正可测的机制变量。

## 作者证明了什么？

1. **Benchmark nominal labels 无法充分刻画真实 task demand。**
2. **Benchmark construction 会留下明显需求指纹。** Testability filter、carve-out、hints 都系统性改变 SNC 或 Agent patch。
3. **Gold Patch 不是完整 task-demand 表示。** Problem wording 会改变成功 Agent 的 solution scope。
4. **低 SNC 与成功稳定相关。** 该趋势跨两个 model family 与多个规模存在。
5. **成功 Behaviour 具有明显 family/harness specificity。** Claude 越大越靠近 Gold parity，而 Qwen 成功时仍倾向 over-produce。

## 作者没有证明什么？

1. 没有证明 SNC 是 task difficulty 的完整因果模型。
2. 没有证明高 Spread / Centrality导致失败。
3. 没有证明 Claude 与 Qwen 的差异来自 model 而不是 harness。
4. 没有证明 Gold parity 是普适最优解。
5. 没有证明 Import Graph Centrality 等价于 Call Graph / Semantic Dependency。
6. 没有研究 repository context 是否应该提供给 Agent，因此不能直接回答“更多 context 有没有帮助”。

## 真正应该记住什么

- **Benchmark label 是很粗的 proxy。**
- **Benchmark construction 本身就是 measurement design。**
- **Task property 和 Agent behaviour 必须分层。**
- **Gold Patch 不是“真实 difficulty”的唯一 ground truth。**
- **Task demand 与成功的规律可以相对跨模型稳定，但成功 strategy 未必稳定。**
- 对 Causality for Code Review，最值得借鉴的是把 Spread / Centrality / ContextNeed 变成 effect modifier，把 Agent trajectory 变成 mediator。

一个非常自然的后续实验是：

```text
同一 PR
同一 Model
同一 Prompt
同一 Budget
        ↓
T0 Diff only
T1 Diff + Relevant structural context
T2 Diff + Irrelevant structural context
T3 Diff + Full call graph
        ↓
记录 trajectory
        ↓
Relevant Evidence Coverage
Irrelevant Evidence Exposure
Exploration Breadth
        ↓
Review Precision / Recall / FP
        ↓
按 Spread / Centrality / ContextNeed 分层估计 CATE
```

这样研究的问题就不再只是“Call Graph 到底加不加”，而是：**什么任务需要什么上下文、为什么不需要时反而受伤，以及这种伤害通过什么 Agent 行为机制发生。**