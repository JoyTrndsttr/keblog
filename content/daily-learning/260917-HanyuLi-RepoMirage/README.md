# RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations

> Hanyu Li, Yichi Zhang, Speed Zhu, Hang Su, Jun Zhu, Yinpeng Dong  
> arXiv:2605.26177, 2026  
> 原文：https://arxiv.org/abs/2605.26177  
> 阅读依据：arXiv 完整 HTML 原文（含正文、表格与附录信息）

## 一、先把论文地图建立起来

这篇论文问了一个非常关键、也很容易被现有 benchmark 掩盖的问题：**Coding Agent 在 SWE-bench 上把 issue 修好，是否真的意味着它理解了 repository context？** 作者观察到，成功案例往往只读很少文件：GPT-5 成功实例平均访问约 2.15 个文件，DeepSeek-V3.2 约 3.97 个；GPT-5 的成功案例中 53.8% 只检查一个文件，88.0% 不超过三个文件。

因此作者没有再造一个完全不同的新 benchmark，而是对同一批 SWE-Bench Verified 实例做**语义保持的仓库级 perturbation**：保持 issue、功能和测试不变，只把原本局部可见的证据变得更分散、更需要跨文件推理。如果 Agent 真有稳定的 repository-context reasoning，理论上不应因为“同样的信息被换了位置或增加了结构间接层”就大幅失效。

结果非常明显：8 个模型平均 resolved rate 从 **66.80% 降到 49.78%**，同时平均访问文件数从 **4.77 增至 13.24**。更重要的是，Agent 虽然读得更多，却更容易陷入持续搜索而不是进入编辑阶段。作者把这种现象称为 **exploration drift**。

这篇论文对我们当前“为什么加 repository context / call graph 反而下降”的研究非常直接：它把“更多 context 导致性能下降”进一步拆成了一个机制问题——**瓶颈可能不是拿不到 context，而是拿到以后无法组织成可用于决策的结构。**

## 二、过去的方法哪里不够？

现有 repository-level benchmark 通常把能力压缩成一个最终 Outcome：

```text
Issue + Repository
        ↓
      Agent
        ↓
Patch passes tests ?
```

这会把很多不同能力混在一起：定位、局部修改、记忆 benchmark pattern、跨文件追踪、运行时目标判断、依赖关系理解等。一个任务最终通过测试，并不能说明 Agent 真正使用了仓库级结构。

作者尤其指出一个构念效度问题：SWE-Bench Verified 中超过 80% 的实例最终只修改一个文件，而且 issue 文本往往已经暴露较强的局部线索。因此“repository-level benchmark”这个 nominal label，并不保证每个实例真的需要 repository-level reasoning。

所以 RepoMirage 的核心不是提高 leaderboard，而是**改变测量工具**：在尽量保持任务本身不变的情况下，提高 repository-context reasoning 的需求，再观察同一个 Agent 是否稳定。

## 三、三个必须理解的概念

### 1. Repository Context Reasoning

作者把它定义为：识别任务相关的多文件信息，并对文件之间的关系进行推理。重点不是“读了多少文件”，而是能否把分散证据组织起来支持正确行动。

因此：

```text
More files accessed ≠ Better repository reasoning
```

这正是全文后面 exploration drift 的关键。

### 2. Semantics-preserving Perturbation

作者有意不改变原 issue 的功能语义和测试，只改变信息的暴露方式。它类似一个 controlled intervention：

```text
原任务语义 / Ground Truth：尽量保持不变
Repository evidence layout：改变
Agent outcome：观察变化
```

这样比直接比较两个不同 benchmark 更容易把性能差异归因到 context demand 的变化。

### 3. Exploration Drift

更强 context demand 出现后，Agent 会搜索更多文件、花更多步骤探索，但这些额外探索并没有有效转化为编辑决策。表现为：

```text
Explore → Explore  概率上升
Explore → Edit     概率下降
```

这意味着问题不是简单的 retrieval failure，而可能是 **evidence integration / structural organization failure**。

## 四、RepoMirage-Perturb：作者到底怎么做干预？

作者设计了三类仓库级 perturbation。

### 1. Dependency-path indirection

原来代码可能直接 import 真正依赖：

```text
A → D
```

作者把它改成四层代理链：

```text
A → Proxy1 → Proxy2 → Proxy3 → D
```

功能保持一致，但 Agent 不能再从一个 import 直接看到真实依赖，必须跨文件追踪 dependency path。

### 2. Runtime-target masking

文件名和路径经常直接提示哪个文件最可能需要改。作者把真实 target 重命名，再在旧位置创建同名 module directory，通过 `__init__.py` re-export 真正 target，同时加入表面上相似的 fake files。

于是 Agent 必须区分：

```text
Textually plausible file
        vs
Actual runtime target
```

这是非常好的干预，因为它专门破坏“文件名相似度 = 运行时相关性”这一 shortcut。

### 3. Local-value externalization

原本目标文件附近的 constant 被移动到外部 JSON，再由程序运行时加载。

原来：

```text
target.py
  ├ logic
  └ constant
```

变成：

```text
target.py ──load──> config.json
```

程序行为不变，但理解逻辑必须跨文件恢复 value relationship。

三类 perturbation 分别操纵 dependency、runtime target 和 distributed value，针对的是三种不同的“局部捷径”。

## 五、实验设计为什么比普通 benchmark 对比更干净？

作者以 SWE-Bench Verified 为 seed benchmark，统一使用 mini-swe-agent 的 bash-only setting，并记录完整 trajectory。这样 Agent framework 被固定，减少“不同 Agent harness”带来的混杂。

被测 8 个模型包括 GPT-4.1、GPT-5、Gemini-3.1-Pro、Claude-Sonnet-4.6、DeepSeek-V3.2、MiniMax-M2.7、Qwen3-Coder-Next、Qwen3.6-35B-A3B。

关键比较是同一类原始实例：

```text
Original SWE-Bench instance
            vs
Semantically equivalent perturbed instance
```

Outcome 仍然是原 issue-resolution 的 resolved rate，同时额外测量 accessed files 和 trajectory transitions。

这比“Benchmark A 比 Benchmark B 难”更有解释力，因为 task formulation、issue 和验证协议尽量保持不变。

## 六、RQ / 实验一：提高 context demand 后，Agent 会怎样？

最核心的 Table 1：

| Model | Original Resolved | Perturbed | Relative Drop |
|---|---:|---:|---:|
| GPT-4.1 | 38.40% | 18.20% | -52.60% |
| GPT-5 | 65.00% | 49.00% | -24.61% |
| Gemini-3.1-Pro | 70.60% | 54.40% | -22.95% |
| Claude-Sonnet-4.6 | 75.20% | 63.20% | -15.96% |
| DeepSeek-V3.2 | 70.00% | 52.00% | -25.71% |
| MiniMax-M2.7 | 78.20% | 65.40% | -16.37% |
| Qwen3-Coder-Next | 69.20% | 42.60% | -38.44% |
| Qwen3.6-35B-A3B | 67.80% | 53.40% | -21.24% |

平均 resolved rate 从 **66.80% → 49.78%**。

同时平均访问文件数：

```text
4.77 → 13.24
```

也就是说，Agent 明显知道“需要去别处找”，但找得更多并没有抵消性能下降。

这与“context 越多越好”的朴素假设相反。真正瓶颈可能是：

```text
Context Access
    ↓
Evidence Organization   ← 这里失败
    ↓
Decision
    ↓
Edit
```

消融结果也显示三种 perturbation 单独使用都会降低性能，三者组合进一步下降，说明并非某一种特殊改写独占结果。

## 七、RepoMirage-Extend：为什么作者还要再造四类显式任务？

Perturb 实验仍然用“issue 是否修好”作为最终 Outcome，因此作者进一步把被 perturbation 暴露出来的结构瓶颈直接变成任务。

四类任务是：

1. **Multi-File Issue Resolution**：保留真实需要多文件修改的实例；
2. **Proxy Chain Completion**：补全被删除的代理链 import；
3. **Runtime Target Identification**：找出真正运行时 target；
4. **Missing-Constant Recovery**：跨文件恢复被外置 constant 的 key-value 关系。

这里的思想很重要：不是继续用一个笼统的“repo-level capability”，而是把它拆成可测的结构能力。

## 八、显式测 repository reasoning 后，性能掉得更厉害

八个模型在原始 issue-resolution 上平均 **66.80%**，在 RepoMirage-Extend 上平均只有 **25.25%**。

四类任务平均成功率分别约为：

| Task | Mean Success |
|---|---:|
| Multi-File Issue Resolution | 17.86% |
| Proxy Chain Completion | 17.19% |
| Runtime Target Identification | 28.26% |
| Missing Constant Recovery | 33.94% |

最难的是 Proxy Chain：也就是沿跨文件依赖链恢复结构关系。

更有意思的是模型排名并不稳定。例如 MiniMax-M2.7 在原始 issue task 很强，但在 Extend 上下降很明显。这进一步说明：

> SWE-Bench 的最终修复能力与 repository-context reasoning 不是同一个构念。

## 九、机制实验：为什么“读更多”没有帮助？

作者把 trajectory 操作分为：

```text
explore / edit / test
```

然后比较 perturbation 前后的状态转移。

在更强 context demand 下，GPT-5 和 DeepSeek-V3.2 都表现出：

- 编辑前访问文件数增加；
- pre-edit exploration stage 变长；
- `Explore → Explore` 增加；
- `Explore → Edit` 减少。

这就是 exploration drift。

注意作者真正观察到的是**行为模式变化**。它强烈支持“额外 context 没有被有效转化为行动”的解释，但仍不能把某个内部认知机制直接当作已经被识别的中介变量。比如 attention dilution、working-memory overload、错误 hypothesis accumulation 都仍可能是更深层原因。

## 十、RepoAnchor：结构 scaffold 能不能救回来？

作者进一步给 Agent 显式 structural hints，并实现 RepoAnchor：先探索并总结任务相关 repository structure，再进入下游 problem solving。

逻辑从原来的：

```text
Search ↔ Read ↔ Search ↔ Edit
```

变成：

```text
Structure Exploration
        ↓
Repository Summary / Scaffold
        ↓
Problem Solving
        ↓
Edit & Test
```

结构提示能显著改善 RepoMirage-Extend 上的表现，这为 exploration drift 的诊断提供了额外证据：**问题至少部分来自结构组织不足，而不仅仅是模型完全找不到文件。**

不过 RepoAnchor 仍是 prototype。它同时改变了 workflow、信息组织方式和推理阶段，因此不能把提升严格解释为某一个单独机制的 causal effect。

## 十一、从因果实验角度审计这篇论文

### Treatment 是什么？

RepoMirage-Perturb 可以近似看成：

```text
T = repository evidence exposure / structural accessibility
```

原始组中关键信息较局部、路径直接；干预组保持功能语义，却增加 indirection、runtime masking 或 cross-file externalization。

### Outcome 是什么？

主要 Outcome 是 resolved rate，辅以 files accessed、exploration stage、action-transition probability。

### 最大优势：Ground-truth-preserving intervention

它没有简单比较“简单 repo”和“复杂 repo”，而是尽量在同一实例上改变 evidence structure。这避免了一个我们一直担心的问题：

```text
Hard Task → needs more context
Hard Task → lower performance
```

如果直接观察自然数据，就会把 task difficulty 与 context need 混在一起。RepoMirage 的 paired perturbation 明显更接近可识别的干预设计。

### 但它并不是严格的单变量 Treatment

每个 perturbation 仍可能同时改变：

- 文件数量；
- 路径长度；
- token 成本；
- 搜索空间；
- lexical cues；
- action budget 消耗；
- Agent 对 repository topology 的感知。

因此结果更准确的解释是：

> 增加特定类型 repository-context reasoning demand 会降低成功率。

而不是：

> “多读一个文件”的纯因果效应是多少。

## 十二、这篇论文和 AACRBench 能怎么接？

AACRBench 已经把 review issue 按 context need 分成 diff / in-file / repo。RepoMirage 提供了一个更进一步的实验哲学：**不要只接受 benchmark 天然给你的 context need，而要主动制造 ground-truth-preserving context intervention。**

例如对一个 Diff-level review issue，可以保持 defect ground truth 不变，只加入：

```text
T0: Diff only
T1: Diff + irrelevant caller
T2: Diff + irrelevant caller/callee
T3: Diff + larger irrelevant call-graph neighborhood
```

如果 Review Quality 随噪声剂量下降，就得到 dose-response。

而对 Repo-level issue，可以做：

```text
Relevant context available
vs
Relevant context masked / indirect
```

这样就能估计：

```text
Context Need × Context Treatment
```

的 heterogeneous treatment effect。

## 十三、对“为什么加 Call Graph 反降”的直接启发

这篇论文给了一个比 attention dilution 更可操作的候选机制：

```text
更多结构信息
   ↓
更多探索
   ↓
探索无法收敛
   ↓
编辑决策延迟 / 错误
   ↓
性能下降
```

也就是说，我们可以把机制变量从模糊的“噪声”拆成：

- `#files inspected`；
- `pre-edit exploration ratio`；
- `Explore→Explore`；
- `Explore→Edit`；
- relevant evidence hit time；
- first correct hypothesis time；
- evidence-to-comment conversion rate。

对于 Code Review Agent，最后一个尤其重要：**检索到了正确 caller/callee，不代表最终 comment 真正引用或利用了它。**

## 十四、如果沿着这篇做我们的实验，我会怎么改？

可以构造一个 2×3 或连续剂量实验：

```text
Context Need:   Local / Repository
Context Noise:  0 / Medium / High
```

或者：

```text
Relevant evidence distance = 0-hop / 1-hop / 2-hop
Irrelevant evidence ratio   = 0% / 25% / 50% / 75%
```

固定：模型、prompt、token budget、Agent harness、ground truth。

然后同时测：

```text
Treatment
   ↓
Retrieval / Exploration trajectory
   ↓
Evidence utilization
   ↓
Review comment correctness
```

这样就不只是重复 RepoMirage 的“context demand 上升会掉点”，而是进一步回答：**在哪个环节掉、为什么掉、什么任务最容易掉。**

## 十五、证据边界：作者证明了什么？

作者有力证明了三件事。

第一，在他们构造并验证语义保持的 perturbation 上，8 个 frontier model 的 issue-resolution 成功率一致下降，而访问文件明显增加。因此标准 SWE-Bench 成功并不能稳定代表 repository-context reasoning。

第二，把跨文件结构能力显式化后，模型平均成功率从原始任务的 66.8% 降至约 25.3%，尤其 proxy-chain 和 multi-file coordination 很弱。

第三，trajectory 出现稳定的 exploration drift，而 structural hints / RepoAnchor 能改善表现。因此“访问更多 context 但不能组织成结构”是一个有实证支持的机制解释。

## 十六、作者没有证明什么？

作者没有证明：

1. 所有真实 repository-level 任务都会出现同样幅度的下降；
2. 文件数本身就是性能下降的原因；
3. exploration drift 是唯一机制；
4. Agent 内部发生了 attention dilution；
5. RepoAnchor 的提升只来自 structure summary，而不是额外计算、阶段化 workflow 或 prompt 改变；
6. SWE-Bench 中只读少量文件一定是“投机”——有些任务本来就只需要局部证据；
7. repository context 越少越好。论文真正说明的是：**需要更广 context 时，当前 Agent 组织和利用它的能力不足。**

## 十七、真正应该记住什么

这篇最值得记住的不是 `66.8% → 49.78%`，而是它提供了一种很适合我们研究的实验范式：

```text
保持任务 Ground Truth
        ↓
干预 Evidence Structure / Accessibility
        ↓
记录 Agent Trajectory
        ↓
观察 Outcome 与 Mechanism
```

它与我们最近读的几篇可以串成一条很清楚的证据链：

```text
SWE-Skills-Bench
→ 额外 context/skill 平均收益很小且存在负效应

Context Compression
→ Full context 并不稳定优于压缩或无 context

RepoMirage
→ 当任务被迫真正依赖更广 repository structure 时，Agent 虽然探索更多却更容易失效

我们的下一步
→ 在 AACRBench 上控制 Context Need、Relevance、Noise、Graph Distance，识别 Review Agent 从“拿到证据”到“使用证据”的因果机制
```

因此，比“证明 Call Graph 有用”更值得做的问题已经变成：

> **在 Review Ground Truth 保持不变时，改变 repository evidence 的相关性、结构距离和噪声剂量，会如何改变 Agent 的探索收敛、证据利用与最终审查质量？**

这个问题既继承 RepoMirage 的 controlled perturbation 优势，又能进一步进入真正的 mechanism / heterogeneous treatment effect 分析。