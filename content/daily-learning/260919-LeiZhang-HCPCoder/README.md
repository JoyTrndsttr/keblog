# HCP-Coder：Hierarchical Context Pruning

> 精读日期：2026-09-19
> 正式发表：AAAI 2025, 39(24):25886–25894
> 第一作者：Lei Zhang
> 通讯作者：Min Yang（论文明确以 * 标注）
> DOI：https://doi.org/10.1609/aaai.v39i24.34782
> arXiv：https://arxiv.org/abs/2406.18294
> 代码：https://github.com/Hambaobao/HCP-Coder

## 一句话结论

HCP-Coder 最重要的发现不是“做了一个新的 RAG”，而是把 repository context 拆成了两个不同维度：**文件之间的拓扑/依赖结构应该尽量保留，但依赖文件内部的具体实现可以大幅裁掉。** 作者据此把约 50k token 的 full-repository context 压到约 8k token，并在六个 repository-pretrained Code LLM 上取得五个模型优于已有方法的结果。对当前 VLocBench 研究最有价值的启发是：**node selection 和 node representation 必须分开干预；“这个文件/函数应不应该出现”和“它出现时展示多少实现细节”不是同一个 treatment。**

## 1. 作者与团队

第一作者 Lei Zhang 来自中国科学院深圳先进技术研究院（SIAT）高性能数据挖掘相关团队，同时隶属中国科学院大学。正式 AAAI 版本明确标注 Min Yang 为通讯作者；作者团队还包括 NUS/USTC、UCI、中国科学院自动化所等机构成员。

这篇工作的研究风格偏 LLM/code intelligence + repository context optimization。它不是 Agent 论文，也不是安全漏洞定位论文，而是 repository-level code completion：给定当前文件中的补全位置，研究如何组织跨文件 context，使 repository-pretrained Code LLM 更有效地利用仓库知识。

对我们来说，它的价值主要是**context representation 的实验设计**，不是任务本身。

## 2. 为什么作者认为 Full Repository Context 不好？

作者研究的是已经经过 repository-level code 预训练的 Code LLM。直觉上，这些模型应该能直接吃整个仓库；但真实 repository 很容易超过 context window，而且长 prompt 会显著增加 latency。

论文的 preliminary study 更进一步：问题不只是“装不下”。作者观察到，直接把 repository code 大量拼进去会导致 completion accuracy 下降。因此他们问的核心问题是：

> 仓库上下文里，哪些结构信息必须保留，哪些代码内容可以删掉？

这和我们现在的“context expansion 为什么可能 hurt”非常接近，但他们的目标是工程优化，而不是识别 context degradation 的因果机制。

## 3. Preliminary Study：HCP 的依据来自哪里？

论文先做三类分析，而不是直接提出算法。

### 3.1 Completion error analysis

六个 Repo-Code LLM 在 CrossCodeEval 上的错误中，作者认为至少约 30% 与 cross-file information 有关。这说明 repository context 确实重要：不能简单退回只看当前文件。

### 3.2 Topological dependency analysis

作者根据代码文件之间的依赖关系进行 topological sorting，并改变 prompt 中跨文件代码的组织方式。实验发现：**维持文件依赖拓扑顺序能提高 completion accuracy。**

这里的“topological”不是我们现在 GraphLocator 那种“给 LLM 一条 call path”，而更接近：仓库中的文件有 dependency relation，prompt 的组织应该尊重这种 dependency structure。

所以他们得到第一个设计原则：

> Structure matters.

### 3.3 Cross-file content analysis

然后作者逐步删除 dependent files 中的代码内容，观察哪些信息真的需要。

核心发现非常关键：跨文件上下文中，大量 global context 可以删除；甚至对依赖文件里的函数和类方法，**具体 implementation body 可以大幅裁掉，而不显著降低 completion accuracy**。

也就是说，对很多 repository completion 样本，模型需要的可能主要是：

- 文件存在；
- 文件之间怎么依赖；
- 有哪些 class / function / method；
- signature / declaration / structural skeleton；

而不是每个函数的完整实现。

这得到第二个原则：

> Content density matters, but implementation detail is not uniformly valuable.

## 4. HCP 到底怎么做？

HCP = **Hierarchical Context Pruning（分层上下文裁剪）**。

它首先把 repository 建模到 function level，并保留 file dependency topology。然后根据与当前补全位置的相关性，把不同文件/函数放在不同信息层级，而不是所有节点都给完整代码。

可以把思想简化为：

**当前文件：高保真、保留充分的 prefix/suffix**
→ **高度相关的跨文件节点：保留更多实现**
→ **依赖图上相关但距离/相关度较低的节点：只保留 signature / skeleton**
→ **更无关的代码：删除**

官方代码的 sample 很直观：HCP 输出中的一些 cross-file 文件 value 直接是空字符串，一些文件只留下函数/类定义与截断后的结构，而不是完整 source file。

代码实现还提供 top-p 和 top-k，用来控制相关 context 的保留范围，并使用 embedding retriever 辅助相关性判断。

因此 HCP 不是单纯“按 embedding Top-K 检索”，而是：

**dependency topology + hierarchical code representation + semantic retrieval/pruning**。

## 5. 为什么它叫 Hierarchical？

这里的 hierarchy 不是 directory hierarchy，也不是简单的 1-hop / 2-hop。

它真正强调的是**信息保真度层级**：

- 当前 completion point 周围的信息最完整；
- 相关 cross-file context 次之；
- 更外围 dependency 只保留抽象结构；
- 不重要的实现被 prune。

换句话说，同一个 repository node 可以有不同的 representation fidelity。

这恰好对应我们研究记录 §59/§60 中给 HCP-Coder 的定位：**同一节点、不同代码粒度的 context intervention。**

## 6. 实验结果

正式 AAAI 论文在 CrossCodeEval 上评估六个 repository-pretrained Code LLM。论文报告 HCP 相比已有 prompt/context construction 方法，在六个模型中的五个取得更高 completion accuracy。

更有工程意义的是 context size：full repository code 平均大约 **50k token**，HCP 将 prompt 控制到约 **8k token**，同时提高 completion throughput。citeturn0search2turn0search24

官方代码还包含 CrossCodeEval 与 RepoBench 的预处理、HCP 输入构造、completion 和 evaluation pipeline，说明方法不是只停留在论文伪代码层面。citeturn0search0

这里需要注意：它的主实验比较的是“完整策略”，HCP 同时改变了 selection、ordering、representation 和 token length。因此不能从最终 accuracy improvement 直接推出其中任何一个组件具有独立因果效应。

## 7. 对我们真正重要的不是 HCP 赢了，而是它揭示的反直觉现象

HCP 和刚读的 RepoGraph 放在一起非常有意思。

RepoGraph 告诉我们：

> graph 上结构相关的节点扩得太远，仍然可能伤害模型。

HCP 告诉我们：

> 即使一个 dependency node 值得保留，也不代表它的完整 implementation 都值得保留。

因此 repository context 至少应该拆成两个正交维度：

### A. Node selection
**哪些节点进入 context？**

例如：
- oracle node
- 1-hop
- 2-hop
- plausible distractor
- random distractor

### B. Node representation
**进入 context 的节点展示多少？**

例如：
- full implementation
- function body slice
- signature + docstring
- declaration/skeleton
- summary

这是我们目前实验设计里非常值得正式化的一点。

## 8. 和当前 VLocBench v5 的直接关系

当前 v5 五条件主要在控制 **selection**：

- oracle-matched
- disturb@2
- disturb@3
- random-noise
- plausible-noise

而且当前 node-level content policy 基本保持一致。

HCP 提醒我们，下一阶段完全可以保持 node set 不变，只改变 representation：

**同一组文件 / 同一组 graph nodes：**

Full body
→ Local slice
→ Signature + declaration
→ Skeleton
→ Summary

并且仍然做 tokenizer-aware matching。

这样就能研究：

> context degradation 是因为模型看到了错误的 node，还是因为正确/相关 node 中携带了过多无用 implementation detail？

这比继续无止境加 disturb 条件更有机制价值。

## 9. 一个很适合论文的二维实验框架

结合 RepoGraph + HCP，可以把 treatment 组织成二维：

| | 高保真 Full | 中等 Slice | 低保真 Skeleton |
|---|---|---|---|
| Oracle / relevant nodes | A1 | A2 | A3 |
| 1-hop expansion | B1 | B2 | B3 |
| 2-hop expansion | C1 | C2 | C3 |
| Plausible noise | D1 | D2 | D3 |

这里回答两个不同问题：

**横向：representation effect**
同一 node set，代码越详细是否越好？

**纵向：selection/depth effect**
同一 representation，graph expansion 是否越深越好？

然后检查 interaction：

> 2-hop full implementation 可能 hurt，但 2-hop skeleton 是否不 hurt，甚至 help？

这其实就是 RepoGraph Table 4 与 HCP 思想交叉后最有价值的 hypothesis。

## 10. 可以形成什么机制假设？

我认为至少可以形成三个可检验假设，而不是只做 benchmark comparison。

### H1：Signal dilution
当额外 context 增加的 token 主要来自与任务弱相关的 implementation detail 时，相关证据占比下降，性能降低。

### H2：Structural cue preservation
如果保留 dependency node 与 signature 等结构 cue，同时删除低价值 implementation，模型可以维持甚至提高定位表现。

### H3：Representation × relevance interaction
representation fidelity 的最优值取决于 node relevance：

- oracle/core node：过度 pruning 可能损害必要机制信息；
- peripheral/plausible node：full body 更容易造成 interference，skeleton 可能足够。

这比简单说“context 越多越差”强很多，因为它开始回答 **什么 context、以什么表示、对什么节点会 hurt**。

## 11. HCP 论文自身的证据边界

这篇论文对我们有用，但不能把它包装成已经证明“context noise mechanism”。

主要限制有四个：

1. **任务是 line-level code completion**，不是漏洞定位；completion 对 signature/API information 的需求天然可能比漏洞推理更高。
2. HCP 同时改变 topology ordering、semantic selection、code pruning 和 token length，主实验不是单因素 intervention。
3. “删除 function implementation 不显著掉点”是 benchmark/model 分布下的经验结论，不能直接泛化为 repository reasoning 永远不需要 implementation。
4. CrossCodeEval 的 ground truth 是目标 completion，不等价于我们 VLocBench 的 patch-derived vulnerable-file GT。

因此它对我们是**mechanism inspiration + intervention design evidence**，而不是直接的外部因果验证。

## 12. RepoGraph + HCP + PhantomCall 三篇现在怎么串起来？

这三篇其实已经形成一条非常清楚的方法链：

**RepoGraph：扩哪些结构节点？**
→ graph depth / structural relevance

**HCP-Coder：每个节点展示多少内容？**
→ representation fidelity / pruning

**PhantomCall：能否真正改变底层 graph，同时保持程序行为？**
→ topology intervention / semantic fidelity

对应我们可以形成三层实验：

1. **Context-selection intervention**：固定 repository，只改 visible node set；
2. **Context-representation intervention**：固定 node set，只改每个 node 的信息粒度；
3. **Repository-topology intervention**：未来才改真实 repository/call graph，并验证行为保持。

这比把三篇都归类成“context engineering”更有用。

## 13. 当前最值得落地的一步

我不建议现在直接把完整 HCP pipeline 接进 VLocBench。

成本最低、证据最干净的做法是，在现有 v5 builder 上增加一个 representation policy：

- full
- slice
- skeleton

**先固定完全相同的 node set 和 token envelope**，只比较 representation composition。

尤其值得先测：

> plausible-noise/full vs plausible-noise/skeleton

以及：

> disturb@3/full vs disturb@3/skeleton

如果 full 会导致 degradation、skeleton 恢复，而 oracle/core node 不呈现同样模式，就会比“加 context 后掉点”多出非常重要的一层机制证据。

## 14. 最终定位

**Tags：** 2025 / AAAI / Repository-level Code Completion / Context Engineering / Context Pruning / Repository Dependency / Long Context / Code LLM / Cross-file Context / Context Representation

**对当前研究的重要性：高。**

它最值得我们拿走的一句话不是“把 50k 压到 8k”，而是：

> **Relevant node ≠ all content inside that node is relevant.**

当前研究如果能把 **node relevance × representation fidelity × graph depth** 三者拆开，就会比单纯研究“加 call graph 为什么下降”更完整，也更接近一个可以泛化到 repository-level SE 的 context mechanism framework。
