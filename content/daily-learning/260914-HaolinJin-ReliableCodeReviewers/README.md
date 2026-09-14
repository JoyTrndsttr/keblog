# Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement

> **作者**：Haolin Jin; Huaming Chen  
> **年份**：2026  
> **原文**：[arXiv:2603.00539](https://arxiv.org/abs/2603.00539)  
> **代码 / 复现包**：[GitHub](https://github.com/HollinJ3177/Are-LLMs-Reliable-Code-Reviewers-Systematic-Overcorrection-in-Requirement-Conformance-Judgement)  
> **主题**：LLM Code Review、Requirement Conformance、False Rejection、Prompt Framing、Executable Verification

## 论文地图

这篇论文研究一个很容易被自动代码审查系统默认、但实际上并不可靠的前提：**给定自然语言需求和实现代码，LLM 能否在不运行程序的情况下可靠判断代码是否满足需求？**

作者没有只比较不同模型，而是进一步操纵审查 Prompt：从“只判断 YES / NO”，到“判断并解释”，再到“判断、解释并提出修复”。结果显示，要求更多解释和修复并不一定让审查更可靠，反而可能把模型推向更保守的决策边界：真实错误更少被放过，但正确代码被误判为错误的比例显著增加。论文把这一现象概括为 **systematic overcorrection**。

对 Causality for Code Review 最重要的启发不是某个具体 FNR 数字，而是：**Prompt framing 本身就是 Treatment，并且可能与 Context Treatment 发生交互。**

## 1. 研究问题与动机

自动 Code Review 常使用类似要求：

- 仔细检查所有潜在问题；
- 不要遗漏任何 bug；
- 解释原因；
- 如果有问题，给出修复。

这些要求看起来都在增强审查质量，但它们隐含了一个未经验证的假设：**要求模型“更认真地解释和修复”，只会提升推理质量，不会改变模型的判定倾向。**

作者关注的核心风险是两类错误：

- **False Positive / Unsafe Acceptance**：错误代码被判断为满足需求；
- **False Negative / False Rejection**：正确代码被判断为不满足需求。

后者在真实 Code Review 中会表现为大量 false comments、无谓返工以及开发者对自动审查工具信任的下降。

## 2. 实验设计

作者在 HumanEval、MBPP 和 QuixBugs 上构造正确实现与 buggy implementation 的配对数据，并评测五个 LLM。

关键干预是三种 Prompt：

### Direct

只要求判断代码是否满足需求，输出 YES / NO。

### Direct + Explain

要求判断并给出解释。

### Full

要求判断、解释，并在认为代码有问题时给出修复。

因此可以把实验抽象成：

~~~
Treatment 0: Judge only
Treatment 1: Judge + Explain
Treatment 2: Judge + Explain + Fix
~~~

输入中的 Requirement 和 Implementation 保持不变，变化的是审查指令本身。

## 3. RQ1：LLM 作为 requirement-conformance judge 靠谱吗？

结论是：**即便在最简单的函数级 benchmark 上，LLM 也远不能被当作可靠 correctness oracle。**

论文报告，GPT-4o 在 Direct Prompt 下的 False Negative Rate 仍然很高：

- HumanEval：26.2%
- MBPP：35.9%
- QuixBugs：35.0%

更弱模型的 false rejection 更严重。例如 Llama-3.1-8B 在 MBPP Direct 设置上的 FNR 达到 74.7%。

这说明一个基础问题：LLM 不只是会“漏掉 bug”，它也会系统性地**把正确实现想象成有缺陷**。

## 4. RQ2：要求解释和修复，会改善判断吗？

这是全文最关键的结果。

以 GPT-4o 在 MBPP 上为例：

| Prompt | FPR | FNR |
|---|---:|---:|
| Direct | 3.70% | 35.9% |
| Direct + Explain | 0% | 74.1% |
| Full | 0.20% | 87.9% |

表面上看，更复杂 Prompt 把 FPR 从 3.7% 压到接近 0，意味着更少“放过”错误代码。

但代价是 FNR 从 35.9% 上升到 87.9%，模型几乎变成“宁可错杀，不能放过”。

从实际错误数量看也一样。GPT-4o 在 MBPP 上：

~~~
Direct:
FN = 184
FP = 19

Direct + Explain:
FN = 451
FP = 0
~~~

也就是说，为了少掉 19 个 unsafe acceptance，系统额外制造了 267 个 false rejection。

这意味着 Code Review Prompt 的优劣不能只用“是否更严格”判断，而应看具体成本函数。安全漏洞审查可能愿意牺牲 precision，而日常 PR Review 中大量 false comments 会迅速降低可用性。

## 5. 一个可能的机制：Critique Demand

为什么“Judge + Explain + Fix”会比“Judge only”更容易产生 false rejection？

一个合理机制是：

~~~
Fix Requirement
      ↓
Critique Pressure
      ↓
Search for Possible Defects
      ↓
Plausible Bug Narrative
      ↓
NO
~~~

也就是说，Prompt 不只是让模型表达已有判断，而可能暗示：

> 你应该找到一个值得解释、值得修复的问题。

这会推动模型主动构造“看起来合理”的 defect narrative。

需要注意：论文观察到了现象并分析了错误类型，但没有把 critique pressure 作为独立中介变量进行随机操纵，所以这一部分应当视为**机制解释**，而不是已经完成的 mediation identification。

## 6. RQ3：False Rejection 的解释都在说什么？

作者分析了 false-negative rationale，发现四类模式占全部 FN 的 87.2%。

### Logic Error：48.2%

模型声称算法逻辑有问题、遗漏步骤或条件，但经常没有提供可验证的反例。

### Added Requirement：14.1%

模型自己增加 Requirement 中根本不存在的约束。这可以理解为 requirement hallucination。

### Boundary Error：13.2%

模型高度警惕边界值、空输入、长度条件、< 与 <= 等问题，即使当前实现实际上正确。

### Misread Spec：11.7%

模型直接误解自然语言需求。

这里最值得注意的是：主导错误不是“变量名不好”一类 style nitpick，而是模型构造出了**貌似合理的功能性缺陷**。

## 7. Bug Prior：能力也可能变成偏差

LLM 训练中见过大量 off-by-one、missing validation、null handling、exception cases 和 boundary bugs。

这些知识本来是能力，但在 Code Review 中可能变成一种过强的 prior：

~~~
“这种地方经常出 bug”
        ↓
“所以这里应该有 bug”
~~~

而实际上：

> Risk ≠ Evidence。

这提示自动 Code Review 应明确区分 possible risk 和 confirmed violation。

## 8. RQ4：解释写得好，就更可信吗？

不一定。

作者做了两类分析。

### Self-consistency

检查 explanation 是否真的支持 verdict。结果显示模型会出现 verdict 与 rationale 不一致的情况。

### Fault-awareness

在真实 buggy implementation 上检查模型是否真的识别出错误原因。论文发现，模型通常更容易识别 **failure symptom**，但对真正 bug type / root cause 的判断明显更弱。

因此：

> 发现现象 ≠ 正确诊断。

这在 Code Review 中非常重要，因为错误诊断会直接导致错误 Fix。

## 9. Fix-guided Verification：拿模型自己的修复去验证它

Full Prompt 已经要求模型在认为代码有问题时提出修复。作者把这个 Fix 从“建议文本”变成了可执行证据。

比较：

~~~
Original Code c
vs.
Proposed Fix ĉ
~~~

然后运行测试。

### Case 1：原代码和 Fix 都通过，且行为一致

说明 Fix 很可能没有必要，可以把原来的 NO 翻转为 YES。

### Case 2：两者都失败

证据仍不充分，可以把 failed tests 返回给模型继续判断和修复。

### Case 3：原代码通过，Fix 失败

这是很直接的 over-repair evidence：模型声称在修复问题，结果改完反而坏了，因此原 NO 应被质疑。

### Case 4：原代码失败，Fix 通过

说明修复获得了一定执行证据支持，可以保留 NO。

## 10. 为什么称为 Executable Counterfactual Evidence？

模型提出 Fix，相当于提出一个假设：

~~~
Current Code
→ Behaviour A

Modified Code
→ Behaviour B
~~~

把两份程序实际运行，就能对这个假设进行外部检验。

这比“请你再仔细想想”多了关键的一层：**External Evidence**。

它和 Agent 中的 compiler feedback、test feedback、runtime observation 属于同一种证据增强方式。

## 11. Filter 的效果

论文报告，五个模型平均 FNR 经 Fix-guided Verification 后明显下降：

- HumanEval：54.8% → 16.3%
- MBPP：69.0% → 28.9%
- QuixBugs：51.0% → 24.0%

例如：

- Llama-3.1-8B 在 MBPP：90.8% → 23.6%
- GPT-4o 在 MBPP：88.7% → 40.0%

这说明大量 NO 并不是模型发现了真正可执行的违反需求行为，而是纯文本推理把自己带偏。

## 12. Filter 的边界

Fix-guided Verification 并不是完美 oracle。

如果测试集不完整：

~~~
Buggy Code
↓
碰巧通过现有 Tests
~~~

Filter 仍可能把错误实现误判为正确。

因此更准确的结论是：

> Execution Evidence 通常比 Pure Textual Reasoning 更可靠，但 Tests 本身并不等于完美 Ground Truth。

## 13. 一个额外构念效度问题：扩展测试也是 GPT-4o 生成的

作者除 benchmark tests 外，还使用 specification-constrained augmented tests，而扩展测试由 GPT-4o 统一生成。

这有一个优点：所有 Judge Model 使用相同过滤器。

但也带来风险：

- generated tests 可能遗漏语义；
- 可能增加错误约束；
- coverage 可能不足；
- mitigation 并未完全脱离 LLM。

所以 Filter 是更强的 evidence source，但不是完全独立的 ground truth。

## 14. 外部有效性：这不是完整真实 PR Review

论文题目使用 Code Review，但实验主体来自 HumanEval、MBPP 和 QuixBugs。

这些是函数级 program correctness tasks，而不是真实的 PR + Diff + Repository + Issue + Multi-file Dependency + Reviewer Comment 场景。

因此这篇论文真正证明的是：

> LLM requirement-conformance judgement 存在 systematic overcorrection。

它没有证明所有真实 repository-level Code Review 系统都有相同误判率。

## 15. “Counterfactual” 与严格因果识别的边界

作者把 Original 与 Fixed implementation 的比较称为 executable counterfactual，这作为工程术语是合理的。

但从因果推断角度：

- c → ĉ 往往同时改变多个 statement、branch、variable 或 control flow；
- Treatment 不是单一、最小化、可清晰解释的 intervention；
- Outcome 只在有限测试输入上观测。

所以更准确的表述是 **Executable Counterfactual Evidence**，而不是 **Identified Causal Effect**。

## 16. 对 Causality for Code Review 的直接启发

### 16.1 Prompt 本身必须进入因果变量表

当前研究若比较：

~~~
Diff only
vs.
Diff + Call Graph
~~~

但 Prompt 固定写成“仔细检查所有潜在问题，并对每个问题解释原因和提供 Fix”，那么其实同时存在另一个机制：

~~~
Prompt
→ Critique Intensity
→ Bug Prior
→ False Comments
~~~

因此观察到 CG 条件性能下降，可能有至少三种解释：

1. Call Graph 本身引入噪声；
2. Call Graph × Prompt 发生交互；
3. Prompt 自己就引起 over-correction。

### 16.2 更值得做的是析因实验

可以设计：

| Context \ Prompt | Judge only | Explain + Fix |
|---|---:|---:|
| Diff only | A | B |
| Relevant CG | C | D |
| Full CG | E | F |

形式上研究：

Y = Context + Prompt + Context × Prompt

真正有价值的是 interaction。

如果发现 Diff + Judge 稳定、Diff + CG + Judge 仍稳定、而 Diff + CG + Explain/Fix 显著下降，那么故事会从“Call Graph 有噪声”升级为：

> **Structural Context 与 Review Instruction 发生交互，共同推动模型产生未经证实的 defect narratives。**

### 16.3 Evidence Grounding 可以成为机制变量

论文发现大量 FN 是没有可证伪证据的 Logic Error。

因此可以要求自动 Code Review Agent 为每条评论提供：

~~~
Claim
↓
Exact Evidence
↓
Affected Execution / Dependency Path
↓
Concrete Failure Scenario
↓
Optional Fix
~~~

对于 Call Graph Context，还可以要求每条 Review Comment 必须引用具体 call edge、repository symbol 或 dependency path。

然后测：

> Evidence Grounding 是否中介 Context → Review Quality。

这比只统计 comment 数量或 precision/recall 更接近机制研究。

## 17. 作者真正证明了什么？

1. 五个 LLM 在三个函数级 benchmark 上都存在明显的 requirement-conformance 判断错误。
2. 要求 explanation 和 repair 经常系统性提高 FNR，而不是统一改善准确性。
3. 87.2% 的 false rejection rationale 集中在四种主要模式，尤其是未经证实的 Logic Error 和额外 Requirement。
4. 长 explanation 并不能保证 verdict 与理由一致，也不能保证根因诊断正确。
5. 利用模型自己的 Fix 作为可执行假设，并结合 tests 验证，可以大幅降低 over-correction。

## 18. 作者没有证明什么？

1. 没有证明真实 repository-level Code Review 的误判率等于实验中的数字。
2. 没有证明所有复杂 Prompt 都必然有害。
3. 没有证明 rationale 是造成错误 verdict 的唯一 causal mechanism。
4. 没有证明 Fix-guided Filter 已经形成可靠完整的 Oracle。
5. 没有证明“内部多思考”有害；论文操纵的是外显 Prompt 输出要求，而不是独立 reasoning effort。

## 19. 真正应该记住什么

第一，**Code Review 里的“更严格”不等于“更准确”。**

第二，**Prompt 是正式实验变量，不能只放在 Implementation Details。**

第三，要求模型解释和修复，本身可能诱导模型主动寻找一个并不存在的问题。

第四，Review Comment 最重要的不是写得多专业，而是有没有可验证 Evidence。

第五，对当前 Context Causality 研究，Context × Prompt 很可能比单独的 CG / No-CG 更值得做。

把最近几篇工作串起来，可以得到一个更成熟的研究框架：

~~~
Task Demand
×
Context Treatment
×
Prompt Framing
↓
Agent Behaviour
↓
Evidence Exposure / Defect Narrative
↓
Review Outcome
~~~

最终问题不再只是“Call Graph 到底有没有用”，而是：

> **在什么任务需求和审查指令下，额外结构上下文会帮助或伤害 Reviewer；这种异质效应又通过怎样的 Evidence Exposure 和 Critique Behaviour 产生？**
