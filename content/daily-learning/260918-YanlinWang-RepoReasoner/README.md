# RepoReasoner：长上下文模型真的会做仓库级代码推理吗？

> **论文**：Yanlin Wang, Suiquan Wang, Yanli Wang, Bowen Zhang, Daya Guo, Jiachi Chen, Zibin Zheng. *RepoReasoner: Evaluating Repository-Level Code Reasoning Ability of Long-Context Language Models*. FSE 2026 / Proc. ACM Softw. Eng. 3, Article FSE124. DOI: 10.1145/3808131；arXiv:2607.25996。  
> **代码与数据**：https://github.com/DeepSoftwareAnalytics/RepoReasoner  
> **今天为什么读它**：它几乎正面击中当前“repository context 何时帮助、何时伤害”的问题：一方面用 Oracle context 把 retrieval 与 reasoning 拆开；另一方面直接比较 10k/30k retrieval context，并在 Call Chain Prediction 中显式操纵 signal/noise ratio。它不是因果论文，但实验结构非常适合改造成 context intervention。

## 一句话先记住

RepoReasoner 最重要的不是又造了一个 benchmark，而是把“仓库级能力”拆成了两个更干净的问题：**给你正确上下文，你到底会不会跨文件推理？给你带噪仓库上下文，你能不能找全真正参与执行的依赖？** 结果显示两件事同时成立：Oracle context 下模型仍会失败，而更多 retrieval context 对部分模型还会变差。因此“检索到了更多代码”与“模型真正利用了这些代码”必须分开研究。

## 作者与团队背景

论文署名中明确用星号标出的通讯作者是 **Jiachi Chen（陈嘉驰）**，论文单位为浙江大学；其公开主页把研究兴趣列为 Software Security、Smart Contract Security、AI for Security、Security for AI。近年的工作同时覆盖智能合约安全、LLM+程序分析、代码生成与 repository-level coding。FSE 2026 还包括 *Odyssey*、代码补全 local-cloud cascading、*SWE Data Construction, Automatically!* 等工作。这里更值得关注的是：他并非只做传统“代码理解 benchmark”，而是长期把程序分析/软件安全和 AI4SE 结合。

第一作者 **Yanlin Wang（王焱林）** 来自中山大学，公开主页显示其近期研究已经形成很明显的 repository-level / agentic SE 主线：除 RepoReasoner 外，还有 **MCR-Bench**（多轮代码审查）、**SWE Data Construction, Automatically!**、repository-level retrieval、SWE agent benchmarking、PhoenixRepair 等。换句话说，这不是一个偶然碰到 repository context 的团队，而是持续在做 repository-level code intelligence、benchmark 与 agent evaluation。

末位作者 **Zibin Zheng（郑子彬）** 是中山大学软件工程方向教授，团队近年在 FSE/ASE 等软件工程会议持续布局代码智能、软件安全、智能合约和 LLM4SE。就“软工圈”而言，这个团队比前面读到的一些从 AI robustness 跨进 coding agent 的团队更直接属于软件工程研究脉络。RepoReasoner 与他们此前的 RLCoder、RepoTransBench、MCR-Bench 等工作也能串成一条线：**从 repository-level generation/translation，走向 repository-level reasoning 与 agent evaluation。**

## 1. 论文到底想解决什么？

过去很多 code reasoning benchmark 的单位仍然是一个函数或一小段代码：题目把必要信息基本都摆在眼前，模型只需在局部范围内推理。真实软件工程不是这样。一个结果可能取决于另一个文件里的构造函数、父类方法、配置常量、运行时 dispatch，以及多跳调用。

RepoReasoner 因此把 repository-level reasoning 拆成两个互补能力：

1. **Output Prediction**：微观、状态化执行推理。给定测试函数，把 assertion 的 expected value 替换成 MASK，让模型跨文件追踪执行并预测最终值。
2. **Call Chain Prediction**：宏观、架构依赖推理。给定测试函数和一个混有相关/无关文件的 file pool，让模型预测运行时真正涉及哪些文件。

这两个任务不是上下级关系。模型可能猜对输出却没真正还原调用链，也可能知道调用了哪些文件但模拟错状态变化。这个拆分是全文最值得借鉴的设计之一。

## 2. Benchmark 怎么构造？

RepoReasoner 的流水线有四步。

### Stage I：Repository Collection

作者从 20 多个科学计算领域筛 Python 仓库，要求项目活跃、有标准安装配置、pytest 测试完善，并特别偏向具有复杂 cross-file dependency 的项目。这里已经带来一个选择偏差：benchmark 有意强化了“需要跨文件”的实例，因此不能把结果直接解释成一般 GitHub 任务的自然分布。

### Stage II：Execution-Based Filtering

这是方法上最扎实的一步。作者不是靠静态 call graph 猜 ground truth，而是在 Docker 中真实执行 pytest，并用 Hunter + 自定义 pytest plugin 记录运行时函数调用以及文件级 transition。100 个候选仓库最终只有 15 个成功通过测试并产生可追踪执行模式。

对我们最有价值的是：**dynamic trace 可以定义“实际需要的 repository evidence”**。如果以后做 context intervention，这比静态 call graph 更接近真正的 relevance oracle。

### Stage III：I/O Rewriting

为了减少训练数据记忆，作者提取复杂 assertion，再让 LLM 只修改输入值及对应 expected output；修改后重新执行测试，不通过就根据 AssertionError 修正 expected value，直到新测试通过。程序逻辑保持不变，但输入输出实例变成训练语料中更不熟悉的版本。

注意：这并不是“代码结构语义保持 perturbation”。函数、调用链和大部分 token 都没有变。所以它只能削弱一部分 I/O memorization，作者自己也在 Threats 中承认，未来需要 function refactoring / call-chain reorganization。

### Stage IV：Instance Collection

最终得到 14 个仓库、525 个 test functions、169 个 test files；Output Prediction 有 858 个样本，Call Chain Prediction 有 169 个样本。

## 3. 这篇论文怎样定义 Context？

这里和当前研究最相关。

### Output Prediction：Retrieval vs Oracle

**Retrieval context**：把目标 test function 当 query，仓库其他 source files 当 documents，用 BM25 排序，再按 token budget 拼接。

**Oracle context**：直接使用动态执行 trace 中真实调用到的文件。也就是说它被作者视为“minimal yet complete”：必要信息都有，同时尽量没有额外 noise。

这实际上构造了一个很有用的二分：

`Observed performance = Retrieval quality + Context utilization/reasoning`

Oracle 的目的就是尽量拿掉前一项。若 Oracle 下仍失败，就不能再简单归因于“没检索到”。

### Call Chain Prediction：显式 signal/noise

作者把真实 call-chain files 作为 signal，再随机采仓库其他文件作为 noise，在固定 20k context 下改变 signal ratio，并另设无 noise 的 Oracle。

这已经非常接近我们想做的 intervention，但还差一步：它主要改变“候选文件池组成”，而没有系统控制 graph distance、semantic similarity、hard-negative type 等噪声属性。

## 4. 实验怎么跑？

作者评估 7 个模型：Qwen-2.5-14B、R1-Distill-Qwen-14B、Qwen-2.5-Coder-14B、GPT-4.1-Mini、Gemini-2.5-Flash-no-thinking、Qwen3-235B-A22B、DeepSeek-R1。

每个实例采样 5 次，temperature=0.7，top-p=0.9。Output Prediction 用 Pass@1 / Pass@5；Call Chain Prediction 用文件集合层面的 Precision、Recall、macro-F1，以及要求完整序列一致的 EM。

这里要注意一个 metric 构念问题：Output Prediction 最终是 exact string matching，论文也承认有些失败其实是 formatting/extraction error。因此 Pass@1 并不是纯粹的“reasoning correctness”。

## 5. RQ1：给模型完美 Context，它会推理了吗？

作者用 **10k Oracle context**：只放动态 trace 中的 ground-truth files，尽量排除 retrieval failure。

结果最强的 DeepSeek-R1：
- Pass@1 = **69.1%**
- Pass@5 = **80.3%**

GPT-4.1-Mini Pass@1 66.6%，Gemini-2.5-Flash 62.4%，Qwen3-235B 60.7%。Qwen-2.5-Coder-14B 51.9%，只略高于 Qwen-2.5-14B 的 50.8%。

**真正的结论**：retrieval 不是唯一瓶颈。即便相关文件已经给全，仍约三成 Output Prediction 失败。

但不要把它说成“证明 LLM 不会 repository reasoning”。Oracle context 是文件级 oracle，不等于信息呈现方式最优；10k 截断、文件排序、prompt、状态追踪难度、输出格式都会影响结果。

## 6. RQ2：模型真的理解 Call Chain 吗？

这是我认为对当前研究第二重要的实验。

在固定 20k context 下，作者测试 25% signal、50% signal 和 Oracle。普遍现象是 **precision 高、recall 低**。

例如 GPT-4.1-Mini：
- 25% signal：P=0.801，R=0.312，F1=0.388
- 50% signal：P=0.814，R=0.318，F1=0.397
- Oracle：P=0.912，R=0.355，F1=0.511

Qwen3-235B Oracle precision 0.913，但 recall 只有 0.387。DeepSeek-R1 Oracle precision 0.952，recall 0.357。

最好的 Oracle F1 是 Gemini-2.5-Flash 的 **0.663**，但 EM 也只有 **0.213**。

这说明模型往往能找到一些“明显相关”的文件，却**找不全多跳依赖**。从你的研究角度看，这提示“call graph 给了有没有用”和“模型自己能不能 reconstruct call graph”是两个不同 Treatment：如果直接把显式 call graph 提供给模型，可能是在补偿它的结构恢复缺陷；但如果 call graph 里混入大量不必要邻居，又可能产生新的 context harm。

## 7. RQ3：是在推理，还是在背？

作者在 10k Oracle context 下比较 Original 与 I/O-Rewritten。

所有模型都下降。例如：
- GPT-4.1-Mini：66.6% → **58.8%**
- DeepSeek-R1：69.1% → **65.0%**
- Qwen-2.5-14B：50.8% → **42.0%**

因此可以说模型利用了熟悉模式，rewrite 后性能普遍降低。

但论文把这个结果进一步解释成 memorization，需要谨慎。I/O rewrite 不仅降低记忆匹配，也可能改变数值、边界情况和实际执行难度。因此它提供的是**与 memorization hypothesis 一致的证据**，不是严格识别出来的“记忆因果效应”。

## 8. RQ4：更多 Context 会更好吗？

这是今天最值得带走的一张表。

作者保持 Retrieval-based strategy 不变，只把 token budget 从 **10k 增到 30k**：

| 模型 | Original 10k → 30k Pass@1 | 变化 |
|---|---:|---:|
| Qwen-2.5-14B | 36.0% → 40.3% | +4.3pp |
| R1-Distill-Qwen-14B | 34.1% → 36.7% | +2.6pp |
| Qwen-2.5-Coder-14B | 40.4% → 37.8% | **-2.6pp** |
| GPT-4.1-Mini | 54.1% → 55.0% | +0.9pp |
| Gemini-2.5-Flash | 53.9% → 52.0% | **-1.9pp** |
| Qwen3-235B | 50.7% → 51.9% | +1.2pp |
| DeepSeek-R1 | 58.5% → 58.3% | -0.2pp |

所以“more context hurts”这个现象是存在的，但**不是统一方向**。同样从 10k→30k，有的模型升、有的降。

论文把下降解释为 noise / attention dilution。这是合理假设，但从实验设计上还没有被单独识别：扩大 BM25 budget 同时改变了 token 数、相关文件覆盖率、无关文件数量、文件排序位置和 relevant-evidence density。我们真正可以接着做的，正是把这些东西拆开。

## 9. RQ5：失败到底失败在哪里？

作者人工检查 200 个 Output Prediction failures 和 100 个 Call Chain failures。

Output Prediction 主要包括：
- Formatting / extraction error；
- Identifier confusion；
- Wrong value。

例如 Qwen-2.5-Coder 的 formatting error 明显少于普通 Qwen，但 wrong-value error 占比很高。这再次说明“最终答错”不是单一机制。

对我们的启发是：如果未来只看 code-review F1 / recall，就会把完全不同的 failure mechanism 混成一个 Outcome。最好进一步区分：
- evidence 没看到；
- evidence 看到了但判断错；
- 正确判断但生成/定位格式错；
- 被额外 context 引向错误证据；
- 找到正确 evidence 后又被后续探索覆盖。

## 10. 这篇论文真正证明了什么？

**论文直接支持：**
- repository-level reasoning 即使在 Oracle context 下仍有明显性能缺口；
- call-chain reconstruction 呈现明显的高 precision / 低 recall；
- I/O rewrite 后所有模型性能下降；
- retrieval context 从 10k 增至 30k 的效果具有明显模型异质性，部分模型下降。

**论文没有证明：**
- “attention dilution”就是性能下降的因果机制；
- 30k 变差是因为 token 更多本身，而不是 BM25 新加入的特定文件；
- irrelevant context 的剂量与性能存在单调因果关系；
- call graph context 一定能修复 multi-hop dependency weakness；
- I/O rewritten 的全部下降都来自 memorization 被破坏。

尤其 RQ4 是**现象证据**，不是机制识别。

## 11. 对当前研究最直接的迁移

你现在不应该简单复刻“10k vs 30k”。RepoReasoner 已经说明“更多上下文有时变差”，再做一次类似相关实验创新不够。

更值得做的是把 RepoReasoner 的两个轴组合起来：

**轴 A：Need / Oracle dependency depth**
- diff-local；
- in-file；
- 1-hop repo；
- multi-hop repo。

**轴 B：Context intervention**
- Oracle relevant only；
- Oracle + random irrelevant；
- Oracle + lexical hard negative；
- Oracle + graph-neighbor hard negative；
- Oracle + semantically plausible but causally irrelevant evidence。

这样你固定 ground truth 和真正需要的信息，只改变额外 context。Outcome 不只看最终 review quality，还记录：
- relevant evidence hit；
- false-positive evidence adoption；
- evidence→comment conversion；
- exploration length / token；
- first-correct-hypothesis time；
- 是否从正确 hypothesis 漂移到错误 hypothesis。

这就从 RepoReasoner 的“context length association”推进到更干净的 **counterfactual repository-context intervention**。

## 12. 与最近几篇论文怎么串起来？

这几天其实已经出现一条很清晰的证据链：

**AGENTS.md**：额外 developer/generated context 能被 agent 使用，但不保证改善成功率，还会增加探索与成本。  
**RepoMirage**：保持任务正确答案不变，只改变 repository evidence 的暴露方式，agent 会出现 exploration drift。  
**RepoReasoner**：即便给 Oracle files，跨文件 reasoning 仍不稳；增加 retrieval context 对不同模型可能正、负皆有。  

三篇合起来支持的研究问题比“call graph 有没有用”更强：

> **Repository context 的价值取决于任务是否需要它、其中 relevant evidence 的比例/结构距离，以及模型能否把 evidence 转化为正确行动；context expansion 的伤害可能通过 retrieval dilution、structural confusion 与 trajectory drift 等不同机制产生。**

但目前这些机制仍需要被分别干预和测量，而不能只根据最终性能下降命名。

## 13. 最后记住三件事

第一，**Oracle context ≠ Oracle performance**。把正确文件给模型，只解决“信息有没有到场”，没有解决“模型会不会组织、追踪和利用”。

第二，**context quantity 不是一个干净 Treatment**。10k→30k 同时改变很多变量，所以“更多 context hurts”只能作为现象起点。

第三，对你的研究最有价值的是 RepoReasoner 的实验骨架：**Oracle relevance + controllable noise + dependency depth + heterogeneous model response**。下一步真正有论文价值的是把这个骨架做成严格的 repository-context intervention，并解释下降到底经由哪条机制发生。
