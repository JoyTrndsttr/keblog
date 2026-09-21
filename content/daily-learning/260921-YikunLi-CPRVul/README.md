# CPRVul：Beyond Function-Level Analysis: Context-Aware Reasoning for Inter-Procedural Vulnerability Detection

> 精读日期：2026-09-21  
> 简称：CPRVul  
> arXiv：2602.06751  
> 主题：Inter-Procedural Vulnerability Detection、Repository Context、Context Selection、Structured Reasoning

## 一句话结论

CPRVul 最值得当前研究借鉴的不是“跨函数上下文有用”，而是一个更强的反例：**即使 caller / callee / global context 已经经过 profiling 与 relevance selection，直接交给传统分类器仍可能降低性能；真正的大幅增益主要来自把这些 context 组织成显式的漏洞推理过程。** 因此 Relevant Context 并不等于 Useful Context，context availability 与 context utilization 应拆开研究。

## 1. 论文地图：过去 → 问题 → 解法

传统函数级漏洞检测默认漏洞证据主要存在于目标函数内部，但很多漏洞需要 caller state、callee behavior、global state 或跨过程数据/控制依赖才能判断。

直觉上可以把更多 caller / callee context 直接塞给模型，但 CPRVul 的 preliminary experiment 表明：raw inter-procedural context 对 CodeBERT / UniXcoder 并没有稳定帮助，甚至会降低准确率。

因此论文的问题不是简单的“如何拿到更多上下文”，而是：

> **如何把跨过程 context 变成模型真正能够利用的漏洞证据？**

CPRVul 的回答分成两阶段：

1. Context Profiling and Selection：从程序图中提取 caller、callee、global variable，并转成安全相关 profile 后筛选；
2. Structured Reasoning：训练模型显式连接 target function 与这些外部 evidence，再完成漏洞判断。

## 2. 作者与团队背景

第一作者 Yikun Li 的公开研究轨迹主要位于 AI × Software Engineering × Cybersecurity，早期涉及 Self-Admitted Technical Debt，近年的工作明显集中在 vulnerability datasets、LLM vulnerability detection、reasoning 与 secure coding agent。

论文作者来自 Singapore Management University、Monash University、GovTech Singapore 等机构，团队中包含长期从事 AI4SE、代码智能与漏洞检测的研究者。论文公开版本没有明确标出通讯作者，因此这里不根据末位作者位置自行推断 corresponding author。

从研究连续性看，CPRVul 不是孤立地做一次 context engineering，而是沿着“漏洞数据质量 → 漏洞推理 → 跨过程 context reasoning”的路线继续推进。

## 3. 为什么 Function-Level 不够

典型问题是：目标函数本身的操作可能看起来合理，但 vulnerability condition 来自 caller。

例如 target function 对传入指针执行某种操作，真正的危险条件却是某个 caller error path 可以传入 NULL。

因此漏洞判断可能需要：

caller state → argument → target operation

这种 evidence chain 无法只从目标函数内部恢复。

论文因此显式考虑三类 inter-procedural context：

- caller functions；
- callee functions；
- global variables。

## 4. Preliminary Finding：直接加 Context 反而下降

论文最值得注意的起点，是直接把 raw context 加给传统模型并没有带来提升。

以 UniXcoder 为例：

| Dataset | Function only | + Raw Context |
|---|---:|---:|
| PrimeVul | 56.65 | 54.22 |
| TitanVul | 63.68 | 62.87 |
| CleanVul | 58.24 | 55.22 |

三个数据集全部下降。

更关键的是：即使 Phase I 已经对 context 做过 security profiling 与 relevance selection，但如果仍然直接交给传统 classifier，结果依旧下降：

| Dataset | Function only | + Processed Context |
|---|---:|---:|
| PrimeVul | 56.65 | 55.26 |
| TitanVul | 63.68 | 62.88 |
| CleanVul | 58.24 | 54.75 |

所以论文真正暴露出的现象不是“raw context 有噪声”这么简单，而是：

> **把 context 筛干净，并不保证模型知道如何利用它。**

## 5. Phase I：Context Profiling and Selection

作者首先构建 Code Property Graph（CPG，代码属性图），从 target function 周围提取 caller、callee 与 global variable。

最终覆盖 883 个 repository、23,904 个 labelled functions，并抽取约：

- 19,858 caller functions；
- 187,170 callee functions；
- 132,633 global variables。

callee 数量远高于 caller，本身就说明沿调用关系扩张很容易迅速产生大量候选 context。

### Security Profiling

CPRVul 不直接把每个邻居的完整 source code 塞给 detector，而是先让 LLM 生成 security-oriented profile。

caller profile 关注：

- 数据从哪里进入；
- 是否来自 user/network；
- 是否经过 sanitization；
- target 的返回值如何被使用。

callee profile 关注：

- 是否包含危险 memory operation；
- 是否有 bounds check；
- 是否存在安全敏感行为。

global variable profile 则描述：

- 它代表什么状态；
- 是否涉及 permission、credential 或 shared state。

这一步本质上是一次 **representation intervention**：

raw code → security-oriented abstraction。

### Relevance Ranking

profile 生成后，作者再根据 security relevance 对候选 context 排序，只保留高相关部分。

所以 Phase I 同时改变：

- node selection；
- representation；
- context length；
- relevance distribution。

因此它不是一个可以直接解释为“纯 noise removal effect”的单变量实验。

## 6. Phase II：Structured Reasoning

CPRVul 的主要性能增益来自这里。

训练阶段 reasoning generator 可以利用：

- vulnerable code；
- fixed code / diff；
- CVE description；
- Common Weakness Enumeration（CWE，共同弱点枚举）；
- commit message；
- selected context。

这些信息帮助生成结构化漏洞 reasoning trace。

随后作者用 reasoning data fine-tune Qwen2.5-Coder。

需要注意的是，推理阶段不会继续提供 fix、CVE description 或 commit message；inference 主要使用 target function 与 processed context。因此这些 metadata 更像 training-time privileged supervision，而不是部署时输入。

## 7. 整体结果

Qwen2.5-Coder-32B 的 CPRVul 在三个数据集上取得：

| Dataset | UniXcoder | CPRVul |
|---|---:|---:|
| PrimeVul | 56.65 | 67.78 |
| TitanVul | 63.68 | 73.76 |
| CleanVul | 58.24 | 64.94 |

PrimeVul 上作者还比较了多个 LLM-based baseline：

- LLMxCPG：50.36；
- CoT：51.26；
- GPTLens：51.84；
- VulTrial：55.17；
- CPRVul：67.78。

这些结果说明完整系统有效，但不能把全部增益归因于 context selection，因为模型、训练方式和 structured reasoning 也同时发生了变化。

## 8. 异质效应：什么漏洞更需要 Context

CPRVul 的 CWE 分析很适合当前研究借鉴。

### CWE-264：Access Control

PrimeVul 从 52.08 提升到 79.17，约 +27.09 points。

这类漏洞天然可能依赖 caller authentication / authorization state，因此跨函数 evidence 很重要。

### CWE-399：Resource Management

TitanVul 从 56.45 提升到 71.88；PrimeVul 从 50.00 提升到 70.00。

### CWE-415：Double Free

TitanVul 却从 68.97 降到 62.07，约 -6.90。

论文给出的一个可能解释是：CPRVul 更擅长 spatial inter-procedural relation，而 Double Free 更需要 temporal state reasoning——不仅要知道谁调用谁，还要知道对象在不同路径和时间点是否已经被释放。

这提示当前 VLocBench 的 effect modifier 不应只写成“graph relevance 高/低”，还可以区分：

- spatial dependency requirement；
- temporal/state-flow requirement。

## 9. Context Placement 也是 Treatment

论文比较三种 context placement：

- Insert-Before；
- Insert-After；
- As-Comments。

PrimeVul 分别为 65.60 / 67.78 / 64.60，TitanVul 为 72.00 / 73.76 / 72.26。

Insert-After 在这些实验中最好。

这说明 prompt layout 本身可能影响 context utilization。对当前实验而言，context ordering / layout 应固定，否则它会成为隐藏 treatment。

## 10. 最关键的 Ablation

完整 CPRVul：

PrimeVul：67.78。

去掉 Phase I：

65.42，只下降 2.36 points。

去掉 Phase II reasoning：

52.54，下降 15.24 points。

TitanVul 中去掉 reasoning 的下降更大，可达到约 21.38 points。

因此论文最重要的实验证据是：

> **profiling / selection 有贡献，但 structured reasoning 的贡献明显更大。**

这也解释了为什么“processed context + traditional classifier”仍然下降：context 本身没有自动转化为可用 evidence。

## 11. 对当前 VLocBench 实验的直接解释

当前已有 treatment：

- oracle-matched；
- disturb@2；
- disturb@3；
- random-noise；
- plausible-noise。

这些实验主要操纵 context composition。

已有多实例结果表明，平均 official F1 出现差异，但若干实例完全不变，而且已有下降更多体现在外围 caller / patch-file 是否被报告，而不是核心漏洞机制完全丢失。

CPRVul 提供了一个重要 alternative hypothesis：

不是简单的：

Noise → Attention Dilution → Wrong Vulnerability Mechanism

而可能是：

Context Composition
→ Evidence Utilization Strategy
→ Which Evidence Becomes Localization Output

也就是说，模型可能仍然理解核心漏洞机制，但不同 context 改变了它最终选择报告哪些 supporting files。

## 12. 一个低成本的新 Treatment

现阶段比继续增加 disturb@4 / disturb@5 更有价值的是加入 reasoning treatment。

### Direct

context → predict vulnerable files

### Evidence-grounded reasoning

context
→ identify vulnerability mechanism
→ cite supporting context blocks
→ predict vulnerable files

保持：

- context 相同；
- model 相同；
- temperature 相同；
- token budget 尽量匹配。

于是形成：

| Context | Direct | Evidence-grounded reasoning |
|---|---:|---:|
| Oracle | ✓ | ✓ |
| Disturb | ✓ | ✓ |
| Random | ✓ | ✓ |
| Plausible | ✓ | ✓ |

真正值得测试的是 **Context Treatment × Reasoning Treatment** interaction。

如果 reasoning 后 noise effect 明显减弱，更支持 evidence-utilization failure。

如果 reasoning 后 plausible noise 仍明显伤害结果，才更支持 misleading evidence / semantic interference。

## 13. 与 RepoGraph、HCP-Coder、LaMR 的组合

最近四篇论文现在形成了一条很清楚的方法链。

### RepoGraph：Selection / Depth

哪些 graph nodes 被选中、扩多远。

### HCP-Coder：Representation Fidelity

同一个 dependency node 展示 full implementation、slice、signature 还是 skeleton。

### LaMR：Evidence Role

context 是 direct semantic evidence，还是 dependency support。

### CPRVul：Reasoning Interface

模型是否显式把这些 evidence 组合成任务判断。

因此 repository-context intervention framework 可以进一步写成：

**Selection × Representation × Evidence Role × Reasoning Interface**

Outcome 也可以拆成：

**Mechanism Correctness → Evidence Utilization → File Reporting → Official Patch-F1**

这比直接把所有下降解释成 attention dilution 更可检验。

## 14. 论文没有证明什么

第一，论文没有直接证明 attention dilution。作者讨论 signal dilution、spurious correlation、attention erosion 和 noise，但没有直接测 attention，也没有构造严格 token-matched counterfactual context。

第二，完整 CPRVul 的提升不是 context selection 的纯因果效应，因为 representation、reasoning supervision 和 detector 都同时变化。

第三，Phase I 的 profiling + ranking 同时改变多个变量，因此无法从该实验单独识别“去噪”机制。

第四，CPRVul 是 vulnerability detection，而当前任务是 vulnerability localization；其机制可以作为 intervention hypothesis，但不能直接视为 VLocBench 上已经验证的结论。

## 15. 真正应该记住什么

这篇论文最值得记住的是：

> **Relevant Context ≠ Useful Context.**

更完整地说：

> **Context utility = evidence quality × representation × reasoning capability × task requirement.**

所以当前实验下一步不应急于把 F1 下降写成“noise hurts”，而应该验证：

> **同样的 repository evidence，在模型被要求建立 evidence → vulnerability mechanism → localization 的推理链后，context treatment effect 是否发生变化？**

如果这个交互成立，研究就能从“观察 context degradation”进一步走向“解释 context utilization mechanism”。
