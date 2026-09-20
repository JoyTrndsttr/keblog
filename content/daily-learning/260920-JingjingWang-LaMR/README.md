# LaMR：Context Pruning for Coding Agents via Multi-Rubric Latent Reasoning

> 精读日期：2026-09-20
> 论文状态：arXiv 预印本（2026）
> arXiv：2605.15315
> 作者：Jingjing Wang; Xiwen Chen; Wenhui Zhu; Huayu Li; Zhengxiao He; Feiyang Cai; Ana S. Carreon-Rascon; Xuanzhao Dong; Feng Luo
> 机构：Clemson University、Morgan Stanley、Arizona State University、University of Arizona

## 一句话结论

LaMR 最值得当前研究借鉴的不是“又一个 context pruner”，而是把代码上下文相关性拆成两个不同角色：**semantic evidence（直接回答任务的语义证据）**与 **dependency support（使这些证据可正确理解的依赖/结构支撑）**。这意味着 repository context 的价值不是每段代码独立相加：一段 dependency code 是否有价值，取决于它所支撑的 evidence 是否同时存在。

## 1. 论文地图：过去 → 问题 → 解法

LLM Coding Agent 在 repository-level 任务中需要不断读取代码文件，大量 Token 花在 context acquisition 上。已有 learned pruner 通常把“是否保留某行代码”建模成单一 relevance score 或单一序列标注问题。

LaMR 认为这里存在建模瓶颈：不同类型的有用代码具有不同的序列模式。直接语义证据通常形成连续代码块，而 import、class header、definition、控制流 companion 等 dependency support 往往稀疏地散落在文件中。用一个统一 transition prior 同时建模两者，会倾向保留连续 semantic spans，却漏掉结构上必要但语义相似度不高的支撑行。

因此作者提出 **Latent Multi-Rubric（LaMR，潜在多准则）**：将代码 relevance 拆成多个 rubric，并用专门的结构模型分别建模，再根据 query 动态融合。

## 2. 两种 Context Role

### Semantic evidence

Semantic evidence 是直接回答当前 query、bug、issue 或任务的代码。

例如任务涉及 JWT validation，那么实际执行 token decode / validation 的函数体属于 direct evidence。这类代码往往连续出现，因此其 keep/prune pattern 具有明显局部连续性。

### Dependency support

Dependency support 自己未必回答问题，但缺少它以后 evidence 会变得难以正确解释，例如：

- import；
- class / function definition header；
- scope information；
- 被引用的定义；
- 与保留代码配对的 try / except / finally；
- 必要的 control-flow companion。

它们通常在文件中分散，因此与 semantic evidence 的序列分布完全不同。

这一区分对 repository-context intervention 很重要：

> **“与任务语义相似”与“理解任务证据所必需”不是同一个概念。**

## 3. LaMR 方法

LaMR 首先从代码编码器不同层抽取 representation，并进行 multi-layer feature fusion，使表示同时包含较浅层 syntax、较中层 structure 与较深层 semantics。

随后设置独立的 rubric heads。

### Conditional Random Field（CRF，条件随机场）

作者分别用 CRF 建模 semantic evidence 和 dependency support。

CRF 的关键作用不是单独给每一行打分，而是显式考虑相邻 keep/prune 标签之间的 transition。

对于 semantic evidence，常见模式可能是：

keep → keep → keep

因为相关代码通常连续。

对于 dependency support，则更可能：

keep → prune → prune → keep

因为 import、definition、control-flow companion 可能相隔很远。

如果只使用一个 CRF transition matrix，这两种模式会互相冲突。

### Mixture-of-Experts（MoE，混合专家）gate

两个 rubric 的输出不会简单相加。LaMR 使用 query-adaptive MoE gate，根据当前任务动态决定 semantic 与 dependency 两种信号的权重。

最后再通过一个 fused CRF 输出最终 keep/prune sequence。

所以完整逻辑是：

query + code
→ multi-layer representation
→ semantic CRF / dependency CRF
→ query-adaptive gating
→ fused CRF
→ pruned context

## 4. Rubric-Guided Labeling

已有训练数据只有 binary keep/prune mask，并没有“这是 semantic evidence”或“这是 dependency support”的人工标签。

作者因此利用 **Abstract Syntax Tree（AST，抽象语法树）** 做程序分析，从已有 teacher mask 向外恢复结构依赖，例如 definition、import、scope、call site 和 control-flow companion。

这一步同时承担两个作用：

1. 从 binary label 构造 multi-rubric supervision；
2. 修复 teacher 可能漏掉的结构必要代码。

因此 LaMR 的 supervision 并不是人工标注的真实 causal role，而是一种由 teacher mask + AST rule operationalize 出来的 context-role label。这个证据边界非常重要。

## 5. 实验

论文在四个 benchmark 上测试：

- SWE-Bench Verified；
- SWE-QA；
- LCC；
- LongCodeQA。

覆盖 multi-turn Coding Agent 与 single-turn code understanding/completion。

论文报告，在 multi-turn 对比中 LaMR 在 16 个 head-to-head setting 中赢得 12 个，并可进一步降低 Token；single-turn 任务中 Exact Match 最高提升约 3.5。

### SWE-Bench Verified

Claude Sonnet 4.5：

- Full Context：70.6% solve rate，约 0.911M Token；
- LaMR：71.8%，约 0.633M Token。

即 Token 大约下降 30.5%，同时成功率没有下降。

Claude Opus 4.6：

- Full Context：75.6%，约 0.467M Token；
- LaMR：76.0%，约 0.453M Token。

这里节省幅度较小，但仍保持质量。

## 6. 一个非常重要的 Agent 现象：pruning 不一定真的省 Token

论文展示了一个很值得我们以后注意的现象：

如果 context pruning 删除了 Agent 真正需要的 structural support，Agent 后续可能重新搜索、重新打开文件、增加 tool rounds。

于是：

**单次输入 context 更短 ≠ 整条 agent trajectory Token 更少。**

因此未来做 agentic vulnerability localization 时，更合理的成本链条应该是：

Context Treatment
→ Evidence Availability
→ Agent Exploration / Re-read
→ Outcome + Total Cost

这里 exploration / re-read 很可能是 mediator，而不仅仅是额外成本指标。

## 7. Upstream retrieval 与 pruning 应该解耦

论文还测试了 LaMR 与 upstream context constructor 的组合。

一个重要现象是：如果 upstream 方法已经把 context 完整压缩一遍，再交给 LaMR 做第二次细粒度 pruning，效果可能明显变差；相反，让 upstream 只负责 coarse-grained function selection，再由 LaMR 负责 fine-grained line pruning，表现更合理。

这与 HCP-Coder 和 RepoGraph 放在一起后形成非常一致的研究设计原则：

> **Node selection 与 node representation / pruning 不应该混成同一个 treatment。**

否则性能变化发生后无法知道究竟是“选错节点”还是“节点内容表示错误”。

## 8. 与当前 VLocBench 实验的直接关系

当前五种 treatment：

- oracle-matched
- disturb@2
- disturb@3
- random-noise
- plausible-noise

主要操纵的是 **哪些文件 / graph nodes 进入 context**。

HCP-Coder 给出了第二维：

**进入 context 的 node 展示多少 implementation detail。**

LaMR 又给出了第三维：

**这些内容承担 semantic evidence 还是 dependency support。**

因此现在可以把 repository-context intervention space 更清楚地写成：

**Selection / Graph Depth × Representation Fidelity × Evidence-Support Composition**

这已经比“加 call graph 为什么下降”更接近一个通用 context mechanism framework。

## 9. 一个低成本可执行实验

当前阶段不建议直接训练 LaMR，这会把研究重心变成 context-pruning model。

更有价值的是把它作为 intervention design。

在现有 builder 上，对 context block 离线标记：

- semantic-evidence；
- dependency-support；
- peripheral / noise。

然后在相同 node count 与 tokenizer-aware token envelope 下构造：

1. evidence-high / support-high
2. evidence-high / support-low
3. evidence-low / support-high
4. evidence-low / support-low

最关键的问题是：

> **固定 direct evidence 后，仅删除 dependency support，模型是否下降？**

如果下降，说明结构上下文的价值不能简单由 lexical/semantic relevance 表达。

反过来，如果 support-high 但 evidence-low 仍然没有帮助，则说明：

> **graph-related ≠ task-useful。**

## 10. 与 RepoGraph、HCP-Coder 的组合

三篇现在可以形成一个二维/三维机制链。

### RepoGraph：Selection / Depth

研究 graph 上扩哪些节点、扩多远。

### HCP-Coder：Representation Fidelity

研究同一个 dependency node 是否需要 full implementation，还是 skeleton/signature 已足够。

### LaMR：Context Role

研究被保留内容究竟是 direct evidence，还是理解 evidence 所需的 structural support。

一个很自然的 interaction hypothesis 是：

> peripheral node 的 full implementation 容易产生 interference，但 skeleton 可能无害；core evidence node 则可能需要更高 representation fidelity。

进一步：

> dependency support 的价值可能是 conditional 的：只有它所支撑的 evidence 已经存在时才产生正边际价值。

这比把每个 context chunk 独立赋一个 relevance score 更接近真实 repository reasoning。

## 11. 论文没有证明什么

需要严格区分作者结果与机制解释。

第一，LaMR 没有因果证明 attention dilution。Pruned 与 full context 同时改变长度、内容组成、结构完整性和 Agent 后续行为。

第二，semantic/dependency rubric 不是真实 causal ground truth，而是 teacher mask + AST program analysis 得到的 operationalization。

第三，Agent benchmark 中最终 Token 受后续 search/re-read 行为影响，因此 context pruning 对 Token 的效果包含 trajectory-mediated effect。

第四，这篇论文是 context pruning 工作，不是 repository vulnerability localization；其结论不能直接迁移成“漏洞定位应该如何裁剪代码”。

## 12. 真正应该记住什么

LaMR 对当前研究最重要的不是性能数字，而是：

> **Context utility is conditional.**

一段代码的价值不仅取决于“它自己与任务有多相关”，还取决于当前 context 中已经有哪些 evidence，以及它是否为这些 evidence 提供必要的 dependency support。

因此下一阶段比继续增加新的 noise treatment 更有信息量的问题是：

**When does repository context form a useful evidence-support unit, and when does context expansion break that unit or dilute it with unsupported structure?**

这可以成为从“context expansion hurt”走向机制解释的重要一步。

## Tags

`2026` `arXiv/Preprint` `Coding Agent` `上下文工程` `Context Pruning` `Repository Context` `Semantic Evidence` `Dependency Support` `CRF` `Mixture-of-Experts` `AST` `Token Cost`
