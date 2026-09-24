# RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views

> 精读日期：2026-09-24  
> 简称：RepoAtlas  
> arXiv：2609.16936v1（2026-09-15）  
> 作者：Yunxiang Zhang; Haiquan Wang; Jiawei Guo; Hanyang Xia; Yan Chen; Tong Chen; Zhang Zhiwei; Junchen Ye  
> 通讯作者：Yan Chen（论文明确标注）  
> 机构：Beihang University；另有 Independent Researcher 署名  
> 主题：Coding Agent、Repository Context、Code Graph、Dynamic Context、Multimodal Repository View、Context Budget

## 一句话结论

RepoAtlas 的真正价值不是“把代码图画成图片”，而是把 repository context 从一次性检索结果改写成一个随 agent trajectory 演化的**受预算约束的状态变量**：每一步决定保留什么结构、怎样呈现、什么时候刷新。对我们当前研究最重要的启发是，它提供了一个真实 context provider 的反例：更多 graph context 并不天然更好，去掉 15-node budget 反而让 SWE-bench Verified resolve rate 从 63.1% 降到 59.8%；而每轮都刷新 context 更糟，降到 51.0%。这支持把 provider 的 selection / representation / refresh 拆开做 treatment，而不是只比较“有无 repo context”。

## 1. 顶层研究设计：作者到底在解决什么问题？

### Research Gap

Repository-level issue resolution 的难点不是单纯“仓库太大”，而是 relevant evidence 会随着 agent 搜索、读文件、修改代码和跑测试不断变化。现有 graph-based agent 常见两类做法：把图关系线性化成文本，或按当前 query 一次性渲染局部图。前者隐藏拓扑并增加阅读负担，后者随着探索推进会逐渐与当前 focus 脱节。

作者因此把现实问题重新抽象为：**agent 需要维护一个 sufficient-but-focused repository view，而不是不断往 prompt 里追加更多 context。**

### Research Object

研究对象不是完整 repository graph，而是随时间变化的 task-conditioned view：

`Global Repository Graph G + Issue q + Exploration State s_t + Budget B → View G_t`

这里 exploration state 包含最近访问文件、已识别实体、上一轮 view，以及 Localize / Edit / Test 三个阶段。换句话说，context 本身被显式建模成 trajectory-dependent object。

### Operationalization

作者把这个问题拆成三个决策：

1. **Select**：固定 node/edge budget 下，到底选哪些结构；
2. **Project**：同一结构怎样分配到视觉拓扑与文本索引；
3. **Refresh**：什么时候旧 view 已经不够用了，需要更新。

实验随后分别用 end-to-end SWE-bench Verified、LocBench selection 指标和组件消融去验证这三个环节。

### Evidence → Claim

核心证据不是单一 resolve rate，而是三层：

- 三个 Vision-Language Model（VLM，视觉语言模型）上 end-to-end resolve 都提高，同时 token / calls 下降；
- selection 在固定 15-node budget 下优于 fixed k-hop；
- 去掉 budget、模态或 refresh policy 都掉点，说明收益不是简单来自“多给一张图”。

因此论文能支持的 claim 是：**动态、预算化、任务条件化的 repository view maintenance 比静态/局部 graph interface 更有效。** 它不能证明视觉图普遍优于文本，也不能证明 graph context 对所有 SE task 都有帮助。

## 2. 方法：Select–Project–Refresh 到底怎么工作？

### 2.1 Global graph

固定 repository snapshot 上先离线构造有向 typed graph。节点包括 module、class、callable、variable；边包括 containment、inheritance、call、import、override、symbol use。每个节点保留 qualified name、signature 和 source location。

这里值得注意：作者没有修改 repository，也没有引入历史版本或人工伪造节点；context 全来自当前 snapshot。这一点和我们昨天讨论的 stale-context treatment 有本质区别。

### 2.2 Select：不是 k-hop，而是“相关性场 + 预算”

节点 direct relevance 来自三种信号：lexical、semantic、trajectory。作者用 node-wise max 而不是求和：

`a_t(v) = max(a_lex, a_sem, a_traj)`

直觉是避免多个弱信号叠加后压过一个强的精确命中。

随后在 repository graph 上做 Personalized PageRank（个性化 PageRank，一种从 seed 沿图传播相关性的随机游走方法），把直接 evidence 向 dependency-linked nodes 扩散。最终 relevance 仍然取 direct 与 propagated 的 max。

真正的 selection 不是“取 Top-k 节点”而是在 node/edge budget 内寻找高 relevance 的 connected region；必要时把一组节点压成 supernode，并暴露其中最高分的 concrete representative，保证 agent 还能跳到真实源码位置。

这和我们的实验非常相关：**graph expansion 本身并不是 treatment，selection policy 才是。** 同样的 seed，fixed k-hop 和 budgeted relevance propagation 会产生完全不同的 context composition。

### 2.3 Project：内容与表示分开

作者把 selected entities/relations 和 presentation specification 分开。Localization 阶段同时给：

- visual graph：拓扑、cluster、边方向、跨文件关系；
- textual index：identifier、signature、source location。

进入 Edit 阶段后则主动撤掉视觉 context，只保留围绕 patch region 的精确文本 view，因为作者认为此时视觉结构收益较低且可能造成干扰。

这实际上给我们一个很好的变量拆分：

`Context Content ≠ Context Representation`

后续研究如果只比较“graph vs no graph”，会把 node selection、representation 和 token allocation 混在一起。

### 2.4 Refresh：context 不是越新越好

RepoAtlas 不在每个 model call 后更新。它根据 exploration state 判断旧 view 是否仍覆盖当前 evidence；只有 scope 发生实质变化才重新 select + project。

Localize → 维持动态 multimodal view；Edit → 切到 focused textual view；Test → 只有测试反馈改变 impact scope 时才刷新，否则复用。

这一设计在消融里非常关键：**per-call refresh 是最差设置之一**。这说明“context freshness”不是单调正效应；频繁替换会破坏 agent 对已有 context 的连续利用。

## 3. 实验设计

### Dataset

- SWE-bench Verified：500 个真实 GitHub issue-resolution 实例，用于 end-to-end resolve；
- LocBench：560 个实例，用于隔离 view selection 能力。

### Models

三种不同规模/家族的 VLM：Qwen3.6-35B-A3B、MiMo-V2.5、Kimi-K2.5。

### Baselines

- mini-SWE-agent：text-only tool-using baseline；
- LocAgent：graph-guided textual search/traversal；
- SeeRepo：按需展示 visual repository subgraph。

默认 budget 是 15 nodes / 20 edges，每个配置运行三次。

## 4. 主结果：效果不大，但很稳定

在 Qwen3.6-35B-A3B 上：

- mini-SWE-agent：60.8% resolve；
- LocAgent：61.5%；
- SeeRepo：60.8%；
- RepoAtlas：63.1%。

MiMo-V2.5：RepoAtlas 68.0%，最强 baseline 66.9%。

Kimi-K2.5：RepoAtlas 72.4%，最强 baseline 69.4%。

论文汇总为相对 strongest multimodal graph baseline 平均 +2.4 percentage points，同时 input tokens 平均 -5.8%、model calls -7.8%。

这不是巨大提升，但方向在三个模型上一致，而且 efficiency 同时改善，所以更像 context organization 的系统性收益，而不是单纯用更多计算换准确率。

## 5. 最值得我们看的 Table 3：更多 context 和更多 refresh 都会伤害

默认 RepoAtlas：63.1%。

- w/o budget：59.8%，下降 3.3 pp；
- w/o visual：61.2%；
- w/o textual：59.2%；
- w/o adaptive layout：60.4%；
- no refresh：58.4%；
- **per-call refresh：51.0%**。

这里有两个对我们特别重要的信号。

第一，**去掉 node budget 后 token/call 几乎不变，但 resolve 下降 3.3 pp。** 因此至少在该实验里，伤害不能简单解释为“prompt 更长所以 attention dilution”。更合理的候选机制是 visual density、结构歧义或低价值节点改变了模型对结构的感知。

第二，**per-call refresh 比 no-refresh 还差很多。** 每次都给“更新后的合理 context”并不保证更好，因为 context replacement 本身可能破坏 continuity。这提示我们 context intervention 不仅要看 set composition，还要看 exposure timing。

## 6. Table 4：为什么 fixed k-hop 很值得当我们的 baseline

在 LocBench 上，所有 selector 使用同一个 repository graph、seed 和 15-node budget。

fixed k-hop：FA@3 0.256、FA@5 0.320、FR 0.222、AC 0.412。

RepoAtlas selection：FA@3 0.336、FA@5 0.392、FR 0.252、AC 0.494。

去掉 PageRank 后也下降，说明简单结构邻近不等于 task relevance。

这对我们的研究非常直接：如果我们要研究“call graph / repository expansion 为什么伤害”，**fixed k-hop 本身就是一个自然、真实、可复现的 context provider**。它会从正确 snapshot 中取出真实 dependency neighbors，但其中只有部分是 decisive evidence。相比人工构造 stale API，这种 treatment 的生态效度高得多。

## 7. Case Study：成功与失败分别说明什么

成功例 sympy-18698 中，issue 只给输入输出，仓库里存在多个同名 `sqf_list`。RepoAtlas 初始 view 没有直接暴露最终 gold helper，而是帮助 agent 区分同名入口，随后沿调用链找到真正修复点。这里 graph 的价值不是“把答案塞进 prompt”，而是降低 search ambiguity。

失败例 sympy-17630 更有意思：真正依赖只在 runtime 注册，静态 graph 根本没有这条边。RepoAtlas 因而反复在错误 region 内刷新并越收越窄，八次运行都没打开 gold file；text baseline 反而有一次靠后期探索碰到了正确文件。

这就是非常典型的 **provider-induced anchoring**：结构化 context 不一定是随机噪声，它可能高度 coherent、看起来越来越合理，却把 exploration 锁在错误子图里。

## 8. 作者与团队背景

论文明确标注 Yan Chen 为通讯作者，并给出 Beihang University 与 Independent Researcher 两类 affiliation。公开页面没有逐作者映射 affiliation，因此不把每位作者强行对应到具体单位。

一作 Yunxiang Zhang 的同名公开资料存在歧义，不能仅凭姓名可靠拼接个人履历，因此这里只采用论文可确认的信息，不做过度作者画像。

通讯作者 Yan Chen 使用 `@buaa.edu.cn` 邮箱，论文明确对应北航。就本文可验证的研究积累而言，团队把 repository-level coding agent、code graph 与 multimodal graph reasoning 连接起来；论文 related work 直接建立在 RepoGraph、LocAgent、SeeRepo 等工作之上。现有公开检索不足以可靠确认其更长期、完整的个人研究谱系，因此不进一步推断。

## 9. 对当前 AACR / context-provider 实验最直接的启发

当前研究记录已经从“黑盒 baseline 对打”转向固定 reviewer LLM、把 OCR / PR-Agent / retrieval pipeline 拆成 context provider。RepoAtlas 正好支持这种 framing。

建议把 provider 输出拆成至少四个可观测维度：

1. **Selection**：选了哪些文件/函数/节点，GT evidence coverage 如何；
2. **Composition**：必要 evidence、plausible non-decisive evidence、明显 irrelevant evidence 各占多少；
3. **Representation**：raw code / summary / graph relation / grouped context；
4. **Dynamics**：一次性 context 还是 trajectory 中多次刷新。

这样我们真正可以问的是：

`Provider → Context Composition / Representation → Reviewer Attention or Attribution → GT Hit`

而不是简单问 `Repo Context → Review Quality`。

## 10. 一个值得直接做的受控实验

RepoAtlas 的 Table 3/4 给出一个很自然的 intervention：

固定同一 AACR instance、同一正确 snapshot、同一 seed evidence、同一 reviewer、同一 token/node budget，然后比较：

- `seed / C* only`；
- `C* + random repo nodes`；
- `C* + fixed 1-hop neighbors`；
- `C* + fixed 2-hop neighbors`；
- `C* + relevance-selected neighbors`。

所有节点都来自**正确当前版本仓库**。这样如果 1/2-hop 的真实 dependency context 比 random context 更容易让 reviewer 偏离 GT concern，就直接回答我们最关心的 plausible-but-non-decisive context 问题，而且不会遭遇 stale-version 实验的现实性质疑。

Outcome 也不只看最终 hit：同时记录 distractor attribution、GT evidence mention、provider-selected node 被引用比例、token/call、以及 review concern 是否从 GT 转向邻接但非决定性 concern。

## 11. 证据边界

这篇论文仍有几个明显限制：

- 只在 SWE-bench Verified / LocBench，不能直接推广到 code review；
- 三个模型都是 VLM，收益的一部分依赖视觉 graph interface；
- end-to-end +2.4 pp 幅度不大；
- 静态 graph 缺 runtime dependency，失败案例已经说明会系统性漏证据；
- selection、projection、refresh 虽有消融，但仍不是严格因果机制分解；
- `w/o budget` 的 3.3 pp drop 很有启发，但不能仅凭该消融断言“更多 plausible nodes 导致认知干扰”，因为视觉布局和 density 同时变化。

所以对我们最合适的使用方式不是把它当成“更多 context hurts”的直接证据，而是把它当成**真实 provider 如何控制 context composition 与 exposure 的方法学先例**。

## 12. 真正应该记住什么

RepoAtlas 最值得记住的不是 multimodal，而是三件事：

1. repository context 是随 trajectory 变化的 treatment，不只是静态 prompt；
2. fixed budget 下的 selection policy 可以比盲目 k-hop 更重要；
3. 更多节点、更频繁更新都可能降低效果，因此 context quantity / freshness 并非单调有益。

对于我们当前论文，最有潜力的连接点是：**把真实 provider 产生的“当前版本、结构相关、但非决定性”的邻接 context 作为 treatment，再用 matched budget 的 random context 做对照。** 这比构造错误 snapshot 更贴近真实 code review / coding agent pipeline。

### 原文

- arXiv: https://arxiv.org/abs/2609.16936
- arXiv HTML: https://arxiv.org/html/2609.16936v1
