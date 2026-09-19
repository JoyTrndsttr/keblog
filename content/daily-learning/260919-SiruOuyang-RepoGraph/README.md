# RepoGraph：Enhancing AI Software Engineering with Repository-level Code Graph

> 精读日期：2026-09-19
> Venue：ICLR 2025
> 作者：Siru Ouyang, Wenhao Yu, Kaixin Ma, Zilin Xiao, Zhihan Zhang, Mengzhao Jia, Jiawei Han, Hongming Zhang, Dong Yu
> 原文：https://proceedings.iclr.cc/paper_files/paper/2025/file/4a4a3c197deac042461c677219efd36c-Paper-Conference.pdf
> 代码：https://github.com/ozyyshr/RepoGraph
> arXiv：https://arxiv.org/abs/2410.14684

## 一句话结论

RepoGraph 的核心不是“把整个 repository graph 塞给 LLM”，而是先用静态代码分析构建行级 definition/reference 图，再围绕当前搜索词检索小型 k-hop ego-graph，把结构化依赖作为额外上下文提供给现有 Agent / procedural framework。对当前研究最关键的结果反而是它的消融：**1-hop flatten 最好；2-hop flatten 因上下文暴涨反而低于 baseline，而 2-hop summarization 能部分救回性能**。这直接支持“图上下文不是越深越好，depth × representation × token budget 存在交互”的研究假设。

## 1. 作者与团队画像

第一作者 Siru Ouyang 来自 UIUC，论文工作在 Tencent AI Seattle Lab 实习期间完成；作者团队横跨 UIUC、Tencent AI Seattle Lab、Rice University 和 University of Notre Dame。Jiawei Han 是 UIUC 数据挖掘/知识发现方向的代表性学者。团队整体方法风格是 LLM + structured knowledge/retrieval + software engineering agent：不重新训练代码模型，而是构建结构化 repository representation，作为可插拔检索组件增强现有系统。

对我们最有价值的是：他们把 repository structure 落实成了一个可以显式控制的 graph provider，这与当前 VLocBench 的 context-selection intervention 很接近。

## 2. 它到底解决什么问题？

作者认为 repository-level coding 的瓶颈之一是：现有方法经常把仓库当作 flat documents。

- RAG 可以找语义相似代码，但“相似”不等于真正存在程序依赖；
- Agentless 一类方法虽然会做层次化 localization，但 repository representation 仍主要是目录/文件/符号文本；
- Agent 可以自主搜索，但如果缺少全局结构，容易局部探索。

RepoGraph 因此提供 repository-wide navigation layer：让模型不仅看到某段代码，还知道这个定义在哪里被引用、调用，以及相关结构如何跨文件连接。

## 3. RepoGraph 是什么图？

这里非常容易误读：它不是纯粹的 function call graph。

作者用 tree-sitter 遍历仓库，保留函数、类等关键定义以及它们的引用/调用位置。图的基本单位是代码行，节点分成：

- def node：函数、类等实体的定义位置；
- ref node：这些实体被引用或调用的位置。

边主要有两种：

- invoke：定义与引用/调用之间的依赖；
- contain：定义与其内部组件之间的包含关系。

此外作者会过滤 Python built-in / standard library，以及由第三方库 import 引入的 repository-independent relation，尽量保留 project-dependent structure。

因此 RepoGraph 比 caller → callee call graph 更宽，它实际编码的是 definition-reference / invocation / containment repository graph。

## 4. 方法流程

### Step 1：Code line parsing
遍历代码文件，用 tree-sitter AST 找 function、class、reference 等结构，只保留与调用和依赖有关的行。

### Step 2：Project-dependent relation filtering
去掉 built-in / standard-library 关系，也排除第三方依赖关系，避免图被 repository 外部关系淹没。

### Step 3：Graph organization
构建 NetworkX 图。节点保存 file、line、kind、category 等 metadata，并通过 invoke / contain edge 连接。

### Step 4：Subgraph retrieval
给定搜索词，检索以该词为中心的 k-hop ego-graph。

### Step 5：接入现有框架
两种方式：
1. Procedural framework：在 localization / editing 等阶段主动检索 RepoGraph，把 flatten 后的子图追加进 prompt；
2. Agent framework：增加 search_repograph(term) 工具，由 Agent 自己决定什么时候调用。

所以 RepoGraph 更准确的定位是 context provider / navigation plug-in，而不是完整 Agent。

## 5. 主实验：有没有用？

SWE-bench Lite 上，RepoGraph 被接入四种 baseline：

| Baseline | 原 Resolve Rate | +RepoGraph | 变化 |
|---|---:|---:|---:|
| RAG + GPT-4 | 2.67 | 5.33 | +2.66 |
| Agentless + GPT-4o | 27.33 | 29.67 | +2.34 |
| AutoCodeRover + GPT-4 | 19.00 | 21.33 | +2.33 |
| SWE-agent + GPT-4o | 18.33 | 20.33 | +2.00 |

四种组合都提升，但提升并不是免费的：例如 Agentless 平均 token 从 42,376 增至 47,323；SWE-agent 从 498,346 增至 518,792。因此“图有用”不能脱离额外 context/cost 来理解。

定位层面，RepoGraph 对 file-level localization 的提升最明显，例如 Agentless 从 68.7 提升到 74.3；function-level 51.0→54.0；line-level 34.3→36.7。作者也强调：localization improved 并不自动等于最终 patch 成功，最终结果仍依赖 backbone LLM 的推理和编辑能力。

## 6. 对我们最关键的 Table 4：更多 hop 反而更差

| Context 形式 | 平均节点 | 平均边 | Token | Resolve Rate |
|---|---:|---:|---:|---:|
| 1-hop + flatten | 11.6 | 37.1 | 2,310.7 | **29.67** |
| 1-hop + summary | 11.6 | 37.1 | 717.5 | 28.33 |
| 2-hop + flatten | 54.5 | 89.9 | 10,505.3 | **26.00** |
| 2-hop + summary | 54.5 | 89.9 | 1,229.2 | 28.67 |

作者没有继续测试 k≥3，因为 ego-graph 会快速膨胀并引入 noise / irrelevant nodes。

最关键的现象是：**1-hop flatten = 29.67，而 2-hop flatten = 26.00。** 把结构相关上下文从一跳扩展到两跳，节点从约 12 个增加到约 55 个，token 从约 2.3k 增长到约 10.5k，性能反而下降，而且低于 Agentless baseline 的 27.33。

再看 summary：
- 2-hop：summary 把 10.5k 压到 1.2k，26.00 → 28.67，明显恢复；
- 1-hop：summary 把 2.3k 压到 718，却从 29.67 → 28.33。

因此不能简单得出“压缩越多越好”。更合理的机制解释是：当 context 本身已经紧凑、signal density 高时，summary 会损失有效信息；当 graph expansion 已经产生大量冗余/噪声时，summary 的 denoising 收益可能超过 information loss。

这正是我们当前实验应该显式拆开的 graph depth × information density × representation。

## 7. CrossCodeEval 外部验证

RepoGraph 还在 CrossCodeEval Python 子集 2,665 条上测试。DeepSeek-Coder 的 Code Match EM 从 10.2 提升到 19.7；GPT-4o 从 10.5 提升到 28.7，Identifier Match 也明显提高。

这说明结构化 repository context 的作用不只存在于 SWE-bench issue resolving，但这里仍然是“方法组合效果”，不能直接解释为 graph context 的纯因果效应。

## 8. 论文真正证明了什么，没有证明什么？

### 论文支持的事实
1. 静态 definition/reference graph 可以作为通用 plug-in 改善多种 repository-level system。
2. graph context 对 localization 有帮助，尤其是较粗粒度 file localization。
3. graph expansion 存在明显的 depth / budget 问题：2-hop raw context 可以比 1-hop 更差。
4. representation 会改变 expansion 的结果：summary 对大 context 有帮助，对小 context 反而可能伤害。

### 论文没有识别的东西
它没有证明“call graph 本身造成性能提升”，因为：
- 图并非纯 call graph；
- baseline 与 +RepoGraph 的 token、输入信息和部分 workflow 都发生变化；
- Agent 版本加入了新的 action，trajectory 也会变化；
- 1-hop/2-hop 同时改变了节点数、token、信息组成和图距离。

所以 Table 4 是很好的现象证据，却不是干净的 causal identification。

## 9. 和我们当前 VLocBench 实验的直接关系

### 9.1 RepoGraph 可以作为独立 graph provider
当前 active graph 是 GraphLocator RDFS。RepoGraph 可以作为 shadow provider：same instance + same seed + same localizer + same budget，只替换 GraphLocator graph → RepoGraph graph。如果结论仍成立，就能减少“效果只是某一种 graph construction artifact”的风险。

### 9.2 论文天然提供一个待因果化的实验
RepoGraph 的原始比较 1-hop 2.3k token → 2-hop 10.5k token，同时改变了 depth 和 token。我们可以改成：
- 1-hop raw
- 2-hop raw
- 1-hop token-matched
- 2-hop token-matched
- 1-hop + plausible noise
- 2-hop pruned / summarized

这样才能回答：性能下降究竟来自 graph distance、token dilution，还是新增节点的语义干扰？

### 9.3 与 disturb@2/@3 的区别
当前 disturb@2/@3 控的是每层额外分支宽度，不是 hop depth。RepoGraph Table 4 控的是 hop depth。因此应区分：
- depth intervention：1-hop vs 2-hop；
- branch-width intervention：disturb@2 vs disturb@3；
- representation intervention：raw vs summary/slice；
- noise intervention：random vs plausible。

这四个轴如果混起来，很容易重新变成一个无法解释的“大 context 对比”。

## 10. 对当前研究最值得立即吸收的三点

**第一，RepoGraph 是 graph-provider robustness 的很好候选，但不要把它当新的主方法。** 现在已有 GraphLocator-based treatment，只需让 RepoGraph 产生同样可审计的 candidate graph / context blocks。

**第二，Table 4 可以成为论文 motivation 的强相关工作证据。** 它直接展示 structurally related context ≠ monotonically useful context，而且不是 random noise：2-hop 节点本身就是图邻居，却依然把性能从 29.67 拉到 26.00。

**第三，下一步最值得做的不是复现 RepoGraph 的 29.67，而是“因果化 Table 4”。** 把 1-hop/2-hop 的 token budget、seed、localizer 和 representation 控住，再观察 VLocBench 不同 context requirement 样本上的 heterogeneous treatment effect，这比单纯证明 RepoGraph 在 VLocBench 上也能涨点更贴近当前论文主问题。

## 11. 一个需要警惕的点

RepoGraph 作者把 2-hop flatten 的下降联系到 context length / noise，但实验没有把两者拆开。因此不能直接引用它作为“noise causes degradation”的证据。更严谨的表述应是：

> RepoGraph observes a non-monotonic association between graph expansion and task performance; because hop depth, context size, and content composition change together, the mechanism remains unidentified.

这恰好留下了我们要补的缺口。

## 12. 精读后的定位

**Tags：** ICLR 2025 / Repository Graph / Repository-level SE / Context Engineering / Coding Agent / SWE-bench / Graph Retrieval / Context Noise / Context Depth / Localization

**对当前项目的重要性：高。**

不是因为 RepoGraph 本身需要完整复现，而是它给出了当前研究非常漂亮的前置现象：**结构上“相关”的二跳上下文，也可能比一跳上下文更差；压缩能救大 context，却会伤小 context。**

这比“随机塞垃圾代码导致模型变差”更有研究价值，因为它把问题推进到了真正困难的版本：

> **When does structurally relevant repository context stop being useful and start becoming interference?**
