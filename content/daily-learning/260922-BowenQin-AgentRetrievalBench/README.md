# Agent Retrieval Bench：Evaluating Repository Context Retrieval for Coding Agents

> 精读日期：2026-09-22  
> 简称：ARB / Agent Retrieval Bench  
> arXiv：2607.24882  
> 作者：Bowen Qin; Yi Xie  
> 主题：Repository Context Retrieval、Coding Agent、Context Acquisition、Trajectory、Evidence Localization

## 一句话结论

ARB 最值得当前研究借鉴的不是“哪个 retriever 最好”，而是把 repository context acquisition 从最终 patch outcome 中独立出来测：**初始 context 会改变 Agent 后续搜索路径、首次命中关键证据的时间、额外读取成本以及最终定位结果。** 因此 context treatment 不应只看最终 File F1，还应记录 evidence hit、tool calls、read tokens 与 trajectory drift。

## 1. 论文地图：过去 → 问题 → 解法

传统 Coding Agent benchmark 通常只看最终 patch 是否成功，但失败可能来自 Retrieval → Reasoning → Editing → Validation 中任何一层。如果 Agent 一开始就没找到关键文件，后续 reasoning 再强也可能无济于事。

ARB 因此不把 patch success 当作唯一目标，而是直接研究：给定真实 workflow signal 与修复前 repository，Agent 能否找到下一步真正需要读取的文件与代码证据。

论文包含 427 个样本、25 个 repository，其中 345 个 positive retrieval 样本、50 个自然 no-gold case 和 32 个 wrong-repository counterfactual controls；语料规模约 39.2 万文件、790 万 chunks。

## 2. 作者与团队背景

第一作者 Bowen Qin 来自 National University of Singapore（NUS），Yi Xie 来自 Peking University。公开版本将联系邮箱标在 Bowen Qin。公开可核验资料里，两位作者在 AI4SE / Coding Agent 方向的长期论文谱系并不特别突出，因此这篇工作的主要价值应从 benchmark construction、实验设计与 evidence boundary 本身判断。

## 3. 四类 Retrieval Task

- **code2test**：从 PR / implementation-change signal 找相关 tests。
- **comment2context**：给 review comment 和 reviewed file，找理解或处理该 comment 所需的额外文件；reviewed file 已经属于 given context，不算 gold。
- **trace2code**：从 failure command + failure excerpt 找真正的 root-cause implementation。
- **edit2ripple**：已知一个 anchor edit，再寻找受影响的其他 source/test files。

这些任务都强调：query 中显式出现的文件并不一定是真正需要修改或理解的 gold evidence。

## 4. Agentic Relevance 不等于 Semantic Similarity

作者进一步区分 semantic-direct、structural-indirect、workflow-conventional 与 causal-indirect 等关系。它们用来诊断“为什么某种 retriever 在某类 workflow signal 上更有效”，而不是宣称这些标签是真实 latent causal class。

例如 trace2code 中，failure trace 往往直接暴露 test / stack frame / local symbol，但真正要改的是 root-cause implementation。纯 semantic embedding 容易被表面最像 query 的文件吸走；结构化 retrieval 则可能更容易跳到真正 implementation。

## 5. Budgeted Context Yield（BCY）

除了 Recall@k 与 Mean Reciprocal Rank（MRR，首个正确结果排名的倒数），论文提出 **Budgeted Context Yield（BCY）**。

它问的不是“Top-20 有没有正确文件”，而是：

> **在真实 8k / 16k 等 Token budget 下，按这个 ranking 往 prompt 里装，究竟能暴露多少 gold context？**

这个思想比简单文件数更接近 context engineering，因为 Top-5 小文件与 Top-5 巨型文件对模型而言根本不是同一种 context treatment。

需要注意的是，canonical BCY 只要求 gold file 至少有一个 content token 进入 budget 就给 exposure credit，因此它仍不能完全代表“充分 evidence 已进入 prompt”。

## 6. 没有一个 Retriever 通吃所有任务

345 个 positive samples 上，不同方法在 MRR、Recall@20 与 BCY 上的优势并不一致，而且换 task 后 winner 会变化。

尤其在 trace2code 中，结构化 RepoMap 的 MRR / Recall@20 明显优于部分 embedding 方法。这说明 repository retrieval 中“结构关系”与“语义相似度”具有显著互补性。

这与当前 VLocBench 很接近：GHSA/CWE 描述与真正 patch/root-cause location 之间也可能不是直接 semantic match。

## 7. File-Level Hit 可能严重高估真正 Evidence Hit

在带 span annotation 的 287 个样本里，gold evidence 中位只占所在文件约 **4.7%**，约 **75.7%** 的 gold-file occurrence 中真正 evidence 不超过文件的 10%。

因此：

> **找到正确文件 ≠ 找到正确代码。**

论文进一步显示，即使 file-level recall 看起来不错，line-level evidence F1 仍可能很低。这对当前从 VLocBench file-level GT 往 patch/function evidence 下钻，是非常直接的外部支持。

## 8. Interactive Agent 也经常根本碰不到 Gold

在 287 个 trajectory samples 上，允许 Agent 自主搜索 repository 后，仍有相当比例的任务从头到尾没有访问任何 gold file。

所以 interactive exploration 并没有消灭 context acquisition 问题；它只是把 retrieval failure 变成 retrieval failure + 后续搜索补救成本。

## 9. 最关键的实验：Seed Intervention

作者挑选 45 个样本，每类任务 15 个，并固定 Agent、工具、Docker 环境和后续预算。**唯一 intended intervention 是 initial context seed。**

条件包括：No seed、Random non-gold、Lexical、Qwen8B、RRF 与 Oracle。

结果显示 Oracle seed 的 Final F1 最高；而高质量 retrieval seed 相比 random/no-seed，通常更早碰到 gold、需要更少 tool calls 与 post-seed read tokens。

这个设计和当前 VLocBench context intervention 非常接近：固定其他条件，只改变初始 context。

## 10. Random Context 不是 Inert Placebo

论文一个很重要的现象是：Random non-gold seed 不一定简单降低最终 F1，但会明显改变 Agent 后续探索，例如增加搜索/读取次数。

因此：

> **Random context 并不是“什么都没改变”的 placebo，而是一种 active treatment。**

所以当前实验中的 `random-noise` 更准确的角色应该是 non-relevant context treatment；真正的 no-context / no-expansion baseline 仍应单独存在。

## 11. Retrieval Context 的优势可能主要体现在搜索过程

好的 retrieval seed 并不只是提高最终 File F1，更明显的变化还可能是：更早命中 gold、减少 tool calls、减少 post-seed read tokens。

因此更合理的机制链是：

**Context Treatment → Evidence Availability → Agent Exploration → Final Outcome + Total Cost**

其中 exploration / re-read 很可能是 mediator，而不是单纯附加成本。

## 12. Selective Retrieval 的反例

作者还测试能否利用 retrieval confidence 判断“当前 repository 里其实没有答案”。

如果加入明显 wrong-repository counterfactual cases，selective retrieval 看起来会改善；但去掉这些容易识别的 controls，只留下真正困难的 natural no-gold cases 后，方法并没有稳定优于 always retrieve。

这说明：识别 query 与 repository 完全不匹配，和识别“看起来合理但实际没有本地答案”，是两个不同问题。过于容易的 counterfactual control 会制造 calibration 已经成功的假象。

## 13. 与当前 patch-aware sibling disturbance 的直接连接

当前 `disturb@1/@2` 已经不再表示 hop depth，而是每条合格 semantic transition 添加多少 sibling。

ARB 给出的下一步不是继续增加 `@3`，而是给 sibling 增加 **role annotation**：

- semantic-direct-like；
- structural-indirect；
- path-support；
- plausible-but-non-decisive。

然后在相同 sibling 数和 tokenizer-aware token budget 下比较不同 role composition 是否产生不同 trajectory 与 mechanism hit。

这样研究的问题就从“加多少节点？”推进为：

> **加了什么性质的节点，为什么改变模型接下来寻找 evidence 的行为？**

## 14. 论文证明了什么

它证明 repository context acquisition 是一个可以独立测量的 Agent failure surface；不同 workflow signal 需要不同 retrieval inductive bias；结构与语义 retrieval 具有明显互补性。

controlled seed pilot 还表明，高质量 initial context 可以更高效地把 Agent 引向 gold evidence。

## 15. 它没有证明什么

论文没有证明 retrieval 更好就一定导致 patch success 更高，也没有证明 File F1 可以替代 mechanism/span localization。

Seed intervention 每个 sample × arm 只有一次 trajectory，policy sampling variance 没有被系统消除，因此这些结果更适合作为 descriptive mechanism evidence，而不能被解释成已经稳定识别的因果效应。

## 16. 真正应该记住什么

把 CPRVul 与 ARB 连起来，可以得到一条更完整的 repository-context mechanism chain：

**Context Selection → Evidence Acquisition → Agent Exploration / First Evidence Hit → Evidence Utilization / Reasoning → Mechanism Judgment → File Reporting → Official Outcome**

因此当前 VLocBench 下一阶段最值得做的，不是继续证明“某些 noise 会让 F1 掉”，而是识别：

> **同样预算下，不同 repository context composition 如何改变 evidence acquisition 与 utilization，最终才改变 localization。**
