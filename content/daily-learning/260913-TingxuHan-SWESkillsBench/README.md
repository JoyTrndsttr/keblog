# SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering?

> 精读日期：2026-09-13  
> 作者：Tingxu Han, Yi Zhang, Wei Song, Chunrong Fang, Zhenyu Chen, Youcheng Sun, Lijie Hu  
> arXiv：[2603.15401](https://arxiv.org/abs/2603.15401)

## 一句话价值

这篇论文把 Agent Skill 视为一个可控的 Context Treatment，系统比较同一真实软件工程任务在 With-Skill 与 No-Skill 条件下的表现。作者构建 SWE-Skills-Bench，覆盖 49 个公开 SWE Skill 和约 565 个真实仓库任务；平均 Pass Rate 仅从 89.8% 提高到 91.0%（+1.2%），39/49 个 Skill 没有提升，平均 Token 成本却增加 10.5%，且有 3 个 Skill 让性能下降。它对 repository context / call graph 研究最重要的启发是：**额外上下文应该测 marginal utility，而且 context 可能是 redundant、irrelevant，甚至 conflicting。**

## 论文地图

过去常见假设是：Skill 里有专业知识，所以注入 Agent Context 就应该提升能力。作者真正检验的是这个假设是否成立。

整体流程：

```text
公开 Skills
→ 筛选可测试的 SWE Skills
→ 匹配真实 GitHub Repository
→ 固定 Requirement + Acceptance Tests
→ 同一任务配对运行 With Skill / Without Skill
→ 比较 Pass Rate 与 Token Cost
```

Skill 不改模型参数，本质上是运行时 Context Treatment。作者用确定性测试作为 Outcome，因此比 LLM-as-Judge 更适合做 treatment contrast。

## 为什么这个实验设计重要

同一任务中固定 Repository、Requirement、Agent 和验证器，只改变 Skill 是否存在：

```text
Same Repository
Same Requirement
Same Agent
Same Verification
        ↓
Skill Present / Skill Absent
```

这比跨数据集或跨系统比较干净得多。对 Call Graph 研究可以直接映射为：

```text
Same PR
Same Model
Same Prompt
Same Tool
Same Budget
T0: Diff only
T1: Diff + Call Graph
```

Task Difficulty 由配对天然控制，而不需要再找两个“难度相似”的数据集。

## 关键结果一：绝大多数 Skill 没有提高成功率

49 个 Skill 中，39 个的 ΔP=0，约占 80%。其中很多任务在有无 Skill 时都能 100% 通过。这说明 Base Agent 已经掌握了所需知识时，额外 Skill 没有明显边际价值。

但“没有提升”不等于“没有成本”。总体 Pass Rate 只提高约 1.2%，平均 Token 却增加 10.5%。因此 Outcome Effect 与 Behaviour/Cost Effect 必须分开。

## 关键结果二：少数 Specialized Skill 真正有用

最突出的是 `risk-metrics-calculation`：No-Skill 70%，With-Skill 100%，即 +30%。这类结果说明 Skill 在模型缺少 specialized procedural knowledge 时可以提供真正新增的信息。

所以真正的问题不是“Skill 有用吗”，而是：

> **在什么任务条件下，Skill 拥有 Marginal Information Value？**

## 关键结果三：Skill 可以主动伤害 Agent

`springboot-tdd`、`linkerd-patterns`、`django-patterns` 等 Skill 出现约 -9% 到 -10% 的负效果。作者给出的主要解释是 version-mismatched guidance：Skill 描述的框架版本、API 或约定与 Repository 当前环境不兼容。

机制可以写成：

```text
Additional Context
→ 与本地 Repository Evidence 冲突
→ Agent 过度相信外部指导
→ 错误 API / Convention / Assumption
→ Failure
```

这与 repository-level context 中的 misleading evidence 很接近，但论文没有进一步用独立 mediation experiment 证明 version conflict 是全部负效果的唯一原因。

## 证据边界

### Agent 随机性

如果每个任务每个 Treatment 只运行一次，那么 With-Skill / No-Skill 的差异可能混入 trajectory stochasticity。更理想的设计应是 Task × Treatment × Multiple Seeds，再估计任务级成功概率差。

### Skill-conditioned selection

Benchmark 是先有 Skill，再找匹配 Project 并设计 Requirement，因此 +1.2% 不能视为现实世界所有 SWE Task 的总体 ATE。但反过来，即使在刻意匹配 Skill Domain 的任务上平均收益仍很小，也说明 blanket skill injection 值得怀疑。

### Ceiling effect

No-Skill 平均 Pass Rate 已经很高。很多 ΔP=0 可能只是模型已达上限，因此不能据此证明 Skill 在速度、稳健性或代码质量上完全没有价值。

### Token 只是 Cost Proxy

Token 多可能是无效探索，也可能是更多验证，所以不能直接把 Token 增加解释为 reasoning 变差。

## 对 Causality for Code Review 的直接启发

Context 不应该只分 Relevant / Irrelevant，更应该区分：

```text
Missing Knowledge   → 可能明显帮助
Redundant Knowledge → Outcome 不变但增加成本
Irrelevant Knowledge→ 可能稀释注意力
Conflicting Knowledge→ 可能主动误导
```

对 Call Graph 可设计：

```text
T0  Diff only
T1  Diff + Correct Call Graph
T2  Diff + Pruned Relevant Graph
T3  Diff + Full Graph
T4  Diff + Perturbed / Irrelevant Graph
```

固定 Model、Prompt、Tool 与 Budget，再估计 treatment contrast。

平均效果也远远不够。SWE-Skills-Bench 中不同 Skill 的效果从约 -10% 到 +30%，说明异质效应非常强。你的研究更适合估计：

\[
CATE=E[Y(1)-Y(0)|X]
\]

其中 X 可以包括 Context Need、Spread、Centrality、repository size、call-chain depth、evidence density 和 task type。

再进一步，可把 Agent Behaviour 当 Mediator：

```text
Context Treatment
→ Relevant / Irrelevant Evidence Exposure
→ Exploration Breadth / Search Allocation
→ Review Outcome
```

这样“Context Noise”才从 Discussion 中的解释词变成真正可测的机制变量。

## 作者证明了什么

1. 在 SWE-Skills-Bench 当前设置中，Skill 的平均边际收益很小，约 +1.2%。
2. 39/49 个 Skill 没有改变 Pass Rate，blanket skill injection 缺乏经验支持。
3. 少数 specialized Skill 能产生明显正收益，最高约 +30%。
4. Skill 即使不改变 Pass Rate，也可能显著增加 Token Cost。
5. 部分不兼容 Skill 与性能下降同时出现，说明 Context Injection 存在 interference risk。

## 作者没有证明什么

1. 没证明现实世界所有 SWE Task 上 Skill 的总体效果只有 +1.2%。
2. 没证明所有 ΔP=0 的 Skill 都完全没用。
3. 没完全排除单次 trajectory 随机性。
4. 没建立完整的 Context Interference 因果机制。
5. 没证明 Token 增加本身导致性能下降。
6. 没证明 version conflict 是所有负效果实例的唯一原因。

## 真正应该记住什么

- **Context 的价值应测 Marginal Utility，而不是只问其中有没有有用信息。**
- **额外 Context 可能是 Missing、Redundant、Irrelevant 或 Conflicting，不能默认统一正向。**
- **平均 Treatment Effect 很容易掩盖强烈异质性。**
- **这篇最值得复制的是同一 Task 的 With / Without Context 配对实验设计。**
- **对 Causality for Code Review，真正的问题是：什么任务需要什么 Context，为什么不需要时会受伤，以及这种伤害通过什么 Agent 行为产生。**
