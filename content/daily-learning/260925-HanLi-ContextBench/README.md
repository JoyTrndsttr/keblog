# ContextBench：A Benchmark for Context Retrieval in Coding Agents

> 精读日期：2026-09-25  
> arXiv：2602.05892  
> 第一作者：Han Li  
> 主题：Coding Agent、Repository Context Retrieval、Gold Context、Evidence Acquisition、Evidence Utilization

## 一句话结论

ContextBench 最重要的贡献不是再做一个 SWE-bench 式最终成功率榜单，而是把 repository context 本身变成可评测对象：区分模型是否找到正确证据、是否保留并利用证据，以及最终 patch 是否成功。对当前研究最直接的价值，是把“额外 context 是否伤害结果”拆成 Context Exposure → Evidence Acquisition → Evidence Retention → Attribution → Final Outcome。

## 1. 为什么需要 ContextBench

现有 coding-agent benchmark 通常只看最终 patch 是否通过测试。这样无法回答：agent 是否找到了解题所需的文件、函数和代码行？失败究竟来自没找到 evidence，还是已经看到 evidence 却没有正确使用？

ContextBench 因此构建 repository-level gold context，并在 file、definition-level block、line 三个粒度评估 retrieval precision/recall/F1。论文报告的数据规模为 1,136 个 issue、66 个 repository、8 种语言，并包含数千文件、数万个 definition-level blocks 与大量 gold lines。

## 2. Gold Context 的关键设计

它没有简单把 patch files 当作全部 ground truth。标注从 gold patch 出发，再沿函数/类调用、继承、控制流、数据流及模块内语义关系寻找真正解决 issue 所需的 evidence，同时尽量删除冗余内容。

更重要的是，作者用强模型只提供候选 context、不给完整仓库，尝试独立生成 patch；只有至少一次通过官方测试的 context 才通过 feasibility 检查，并继续检查 compactness。

这对我们的实验很重要，因为它强调：

Patch-derived File GT ≠ Mechanism Evidence Context ≠ Final Attribution。

## 3. 为什么它支持“固定 reviewer、比较 context provider”

ContextBench 的结果显示，不同 agent scaffold 的 context retrieval precision/recall 差异明显，复杂 agent 并不自动意味着更好的 context quality。因此，把 OpenCodeReview、PR-Agent 或 graph-based method 直接当黑盒比较，会把 retrieval policy、context composition、reasoning policy 和 reviewer 能力混在一起。

更干净的实验结构应是：

Provider A → Context A → fixed reviewer

vs.

Provider B → Context B → fixed reviewer。

这样最终性能差异才更容易归因到 context。

## 4. 现实中的额外 context

论文的一个重要现象是，coding agents 为了提高 recall，会读取大量 compact gold reference 之外的代码。这里不能直接把这些内容叫 useless noise：reference 外代码可能对探索过程仍有帮助。

但它提供了一个关键现实性证据：在正确 repository snapshot 上运行的正常 agent，本来就会自然产生大量“与搜索相关但不属于最小必要 evidence”的 context。

这比人为把旧 commit API 注入当前任务更贴近我们关心的 plausible-but-non-decisive repository context。

## 5. Usage Drop：最值得借鉴的中间变量

ContextBench 不只记录 agent 曾经看过什么，还比较它最终声明的重要 context。论文观察到明显的 Usage Drop：一部分 gold evidence 曾经进入 agent trajectory，却没有保留到最终有效 context。

因此我们可以把 outcome 从单一 File F1 拆成：

1. GT evidence acquired?
2. GT evidence retained / used?
3. final attribution 指向哪里？
4. 最终 file/block prediction 是否正确？

尤其值得检验：

P(GT acquired = 1, GT retained/attributed = 0 | plausible)

是否高于 matched random context。

这能检测一种更细的 interference：模型已经看到了正确 evidence，但额外 plausible evidence 改变了最终证据权重或 attribution。

## 6. 对 VLocBench treatment 的直接启发

当前 treatment 可以继续保留 C* only、C* + matched random、C* + plausible repository neighbors，但需要增加 evidence-level outcome。

plausible candidate 也不应因为“不在 GT”就自动视为噪声。更合理的是先做 incremental-evidence audit，将候选划为 necessary / potentially useful / non-decisive / conflicting / unknown。

如果最终能够证明，在 current snapshot、固定 sufficient evidence、固定 token/node budget 下，plausible-but-non-decisive context 比 random context 更容易造成 evidence retention 或 attribution shift，那么结论会比单纯“more context hurts”更有解释力。

## 7. 作者与团队背景

论文明确标注通讯作者时才按论文标记记录，不依据末位作者推断。公开信息显示该工作来自南京大学与 UCL 相关合作，研究主题与 coding agents、repository context retrieval 和 agent process evaluation 直接相关。对于无法可靠消歧的个人履历，不强行拼接同名作者资料。

## 8. 证据边界

ContextBench 本身不是 context-noise 因果实验。它不能证明 high recall 导致 low precision，也不能证明 reference 外 context 导致 Pass@1 下降，更没有证明 plausible context 比 random context 更危险。

它真正提供的是三样东西：现实 agent 的 context acquisition 分布、可复用的 compact evidence reference 构造方式，以及 evidence acquisition / utilization 的中间评价层。

## 9. 对当前研究最值得保留的机制链

Repository Context Provider
→ Retrieved Context
→ Gold Evidence Coverage
→ Evidence Retention / Usage Drop
→ Attribution
→ Final Outcome

下一步最缺的不是再造一种 noise，而是把 Evidence Retention 与 Attribution 做成稳定、可自动评分的 outcome。

## 原文

- arXiv: https://arxiv.org/abs/2602.05892
- GitHub: https://github.com/EuniAI/ContextBench
