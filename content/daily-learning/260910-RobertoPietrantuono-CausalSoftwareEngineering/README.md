# Causal Software Engineering: A Vision and Roadmap

> 精读日期：2026-09-10  
> 论文：*Causal Software Engineering: A Vision and Roadmap*  
> 作者：Roberto Pietrantuono, Luca Giamattei, Stefano Russo, Julien Siebert, Neil Walkinshaw  
> Venue：FSE 2026 Ideas, Visions and Reflections  
> DOI / 原文：[10.1145/3803437.3805585](https://doi.org/10.1145/3803437.3805585)；[arXiv:2605.02454](https://arxiv.org/abs/2605.02454)

## 一句话价值

这篇五页的 vision paper 不是提出又一个因果算法，而是把软件工程重新定义成“围绕干预做决策”的过程：把代码、配置、发布和修复视为 intervention，用显式假设、混杂控制、反事实和不确定性把“指标变了”升级为“这个动作究竟造成了什么”。对 Causality for Code Review 最有价值的是它给出了一套从研究问题、工程工件到 benchmark 的总框架。

## 先建立论文地图

作者真正想解决的问题是：软件工程每天都在做决策，但我们大量工具仍主要回答“什么和什么一起出现”，而工程师真正需要的是“如果我做 X，会发生什么”和“如果当时不做 X，会怎样”。作者把这一缺口概括为 **Causal Software Engineering（CSE）**，并设计了三类日常工件、四条演进路线和一套评测议程。

核心矛盾可以压成：

> 过去：监控、ML、LLM 很擅长从历史数据找相关模式  
> → 问题：工程动作发生时常伴随其他变化，相关性不足以指导下一步动作  
> → 作者：把 change 明确建模为 intervention，把假设和 confounder 写进工程流程，再用 effect estimate、counterfactual 和 refutation 支撑决策。

理解全文最需要四个概念：

1. **Intervention**：不是观察到 `X=x`，而是主动把系统设置为 `X=x`。作者用 Pearl 的 `do(X=x)` 表达这个区别。
2. **Confounder**：同时影响干预选择和结果的变量。例如一次发布期间，下游服务恰好扩容；如果不记录扩容，就可能把延迟下降错误归因于发布。
3. **Identifiability**：不是“数据够多”就能估因果效应，而是需要满足一组可说明、可检查的假设，使目标效应能从可观测数据中恢复。
4. **Counterfactual**：在同一个已经发生的事件上问“如果 X 当时不同，Y 是否仍会发生”。它比预测下一次事故更接近根因分析和事故复盘。

## 为什么单纯相关分析不够

论文用一个很简单但很有效的微服务例子说明研究 gap：团队上线新的 client-side retry policy，随后 p99 latency 下降。传统 AIOps 很容易把时间上的先后关系解释为“这个发布修好了延迟”。但同一时间，下游服务从 20 个副本扩到 40 个，流量也从热点区域迁走了一部分。

于是至少存在三条竞争解释：

```text
retry policy ──→ latency
replica count ─→ latency
region mix ────→ latency
```

如果第二、第三个变量还影响“什么时候发布/回滚”，它们就不只是背景噪声，而可能构成 confounding。作者强调，真正的问题不是模型能不能拟合更准确，而是：**你是否能识别 `P(Y | do(X=x))`，而不是只看到 `P(Y | X=x)`。**

这里的 gap 是有充分方法论依据的，但这篇论文并没有通过新实验证明“当前所有 SE 工具都存在严重因果错误”。它是一篇 vision paper，主要依据既有因果 SE 文献和典型工程场景建立研究议程，因此不能把它写成大规模实证结论。

## CSE 到底怎么落地：三个工件

作者最重要的工程化贡献，不是再画一个 DAG，而是把 causal thinking 放进三个可版本控制的工件。

```text
工程决策
  ↓
Causal Design Spec
  ↓
实际部署 / 配置 / 测试动作
  ↓
Intervention Log
  ↓
运行时数据 + 实验数据
  ↓
Living Causal Model
  ↓
effect estimate / what-if / counterfactual
  ↓
继续发布、回滚、再实验或拒绝下结论
```

### 1. Causal Design Spec：在动手前写清楚“我要估什么”

输入是一个具体工程决策，例如“启用 retry policy 是否能降低 p99 latency，同时不提高 error rate”。Spec 要记录 Treatment/Intervention、Outcome、候选 Confounders、允许的干预，以及必要的结构先验。

为什么需要它？因为很多 observational SE study 是看到数据后才决定控制哪些变量，容易混入 post-treatment variables 或遗漏关键 confounder。作者希望把因果假设像 ADR、设计文档一样提前外显并接受 review。

### 2. Intervention Log：把“发生了什么”变成可用于因果分析的记录

输入是实际执行的发布、feature flag、rollback、配置调整等。它不只记 `X` 发生了，还记录同时发生的其他变化、部署范围、时间和预期 outcome。

例如 retry policy 在 10% canary 上启用时，下游 replica 从 20→40、12% 流量离开该 region。传统 deployment log 可能只记版本号；CSE 的 log 把这些并发变化显式视为潜在 confounder。

### 3. Living Causal Model：不是一次性论文里的 DAG

它把设计 spec 的结构与运行时 telemetry、实验数据结合，持续维护 effect estimate 和 uncertainty。作者尤其强调模型可以只覆盖一个服务边界、SLO 或 incident class，不需要一开始就画整个公司的“万能因果图”。

最重要的是，它应该允许输出：

> “现有数据不足以支持这个因果 claim。”

作者明确认为，这比稳定地产生一个自信但脆弱的 attribution 更好。

## 四条 Roadmap 路线真正解决什么

### R1：Causal Observability —— 从“看见系统”到“看见可能的因果结构”

现有 logs、metrics、traces、dependency graph 已经很丰富，也存在 fault localization、RCA、configurable systems 的因果工作。但作者认为当前大量方法仍主要服务于 retrospective ranking，而不是可审计的因果 claim。

关键难点包括：从 SE artifact 中构造 causal variables、在监控数据里处理 confounder，以及系统版本变化时保持结构稳定。

这里和 repository context 很相关：**call graph 本身只是 observability/dependency artifact，不自动等于 causal graph。** 调用关系 `A calls B` 与“改变 A 会导致某个 review outcome 变化”是完全不同的语义层级。

### R2：Intervenability-by-design —— 把 CI/CD 本来就能做的改变变成实验

软件系统其实天然具备很强的 intervention infrastructure：feature flags、canary、A/B test、rollback、staged rollout。问题在于，这些工具通常被当作发布机制，而不是因果识别机制。

作者希望把它们用于安全随机/准实验、可识别的 effect estimation，以及基于 uncertainty 的 go/no-go 决策。

这对代码审查研究很重要：如果能够随机控制 context treatment，例如 diff-only / in-file / call-graph，并固定模型、prompt、预算和实例，那么代码审查本身就是一个很适合 intervention 的 SE 场景。

### R3：Counterfactual Assurance —— 从“最可能的根因”到“如果当时改变它，事故会不会消失”

传统 debugging 和 postmortem 本来就有反事实直觉，例如 `git bisect`。作者要求把这种直觉形式化，并加入 placebo、alternative adjustment sets、跨版本稳定性等 refutation checks。

这条路线的关键不是生成一个更像人的解释，而是让解释具备可证伪性。

### R4：Governance & Alignment —— 因果 claim 也要可审计

安全、fairness、合规领域最终需要回答的是“这个 mitigation 是否真的减少 harm”，而不是“指标跟 mitigation 同时改善”。作者因此提出可审计的 causal claims、human-in-the-loop causal modeling，以及受 causal constraints 约束的 LLM agent。

这是全文里 Agent 相关最有价值的一点：未来的 causal copilot 不应该只是让 LLM 自己讲因果故事，而应该在 identification 不成立时拒绝过度归因。

## Figure 1 应该怎么看

Figure 1 是 roadmap，而不是性能曲线：四条路线并行推进，并以 Causal Readiness Levels（CRLs）描述组织/工具成熟度。阅读重点不是记住每个方框，而是看能力如何逐层升级：

```text
Observe
  ↓
Intervene
  ↓
Explain & Assure
  ↓
Justify & Certify
```

最值得注意的是，作者没有把“学会一个 causal discovery 算法”放在最高层。最高层是**能否把假设、证据、不确定性和组织决策联系起来并接受审计**。这也意味着 causal readiness 不是模型 accuracy 单指标可以衡量的。

## Table 1：因果问题贯穿整个生命周期

Table 1 用 requirements、architecture、testing、debugging、operations 五类场景说明 causal question 并不限于运维：

- Requirements：改变 policy X 对 harm/fairness Y 的影响；
- Architecture：拆分 service 对 latency/incident rate 的影响；
- Testing：哪些 scenario factor 真正导致 failure；
- Debugging：如果 configuration X 不同，failure 是否仍发生；
- Operations：哪项 remediation 真正造成恢复。

表格真正想证明的是：**CSE 不是“给 AIOps 加因果模块”，而是把 SE lifecycle 的 decision question 统一重写为 intervention/counterfactual question。**

## 这篇论文没有传统 RQ，怎样理解它的证据结构

这是 Ideas, Visions and Reflections 论文，没有 Dataset、Baseline、Treatment group、Accuracy，也没有传统 RQ1/RQ2。因此不能硬套“问题→实验→结果”。更合适的是把它看成三个论证问题。

### 问题一：SE 为什么需要 causal-first workflow？

**设计**：通过典型发布场景和既有 causal SE 文献说明 correlation 与 intervention 的语义差异。

**结果**：提出把 code/config/design/testing/deployment/remediation change 统一视为 intervention。

**含义**：这是概念和方法论论证，不是一个经过受控实验验证的 treatment effect。

**Takeaway：** 作者成功说明了“决策问题”和“预测问题”不能混为一谈，但没有量化当前 SE 实践中这种错误到底多普遍。

### 问题二：怎样让 causality 进入日常工程，而不是停在论文分析阶段？

**设计**：提出 Design Spec、Intervention Log、Living Causal Model 三类工件，并把它们映射到生命周期。

**结果**：形成一个可以嵌入 version control、CI/CD、telemetry 的工作流设想。

**含义**：价值主要在 research agenda 和 systems design；论文没有实现完整工具链，也没有用户实验验证这些工件的成本。

**Takeaway：** “把 causal assumptions 变成可 review 的一等工件”是本文最可落地的 idea。

### 问题三：未来怎样判断 CSE 真的进步了？

作者提出三类 benchmark：

1. **Intervention-effect benchmarks**：已知 intervention 和 ground-truth impact，评估 effect estimation 与 uncertainty calibration；
2. **Counterfactual incident benchmarks**：带版本化 traces/logs/intervention timeline 的 incident 数据，评估“如果当时换动作会怎样”；
3. **Causal testing benchmarks**：在 simulator、fault injection 或可复制 workload 中控制 causal factors，评估能否识别真正致因因素。

此外，offline benchmark 不够，还需要 canary 等 online controlled evaluation，并常规报告 effect uncertainty、sensitivity 和 refutation。

**Takeaway：** 作者实际上在要求 causal SE benchmark 的 ground truth 从“预测标签”升级为“干预结果或可控因果机制”。

## 主动审查：这篇 vision 的证据边界在哪里

### 1. 最大优点：把 identification assumptions 放到工程流程里

很多 SE causal paper 最薄弱的一步恰好是 DAG 从哪里来、为什么调整这些变量。本文提出把 required/forbidden links、candidate confounders 和 identifiability condition 版本化，方向是对的。

### 2. 最大未解决问题：谁来保证 Causal Design Spec 是对的？

把假设写下来只解决“隐式假设不可审计”，并没有解决“假设本身可能错误”。专家知识、causal discovery、LLM extraction 都可能错。论文提出 hybrid construction 和 refutation，但没有给出一套可靠的冲突解决机制。

### 3. 软件演化导致 transportability 问题非常突出

作者自己把 “identification under evolution” 列为未来重点。一个 release 上识别的结构和 effect，不一定能直接 transport 到下一版本、另一个仓库或另一个团队。因此在 repository-level code review 中，跨项目平均 ATE 很可能掩盖强异质性。

### 4. Intervention 往往不是单一变量

真实 Agent 或 context treatment 经常同时改变 token budget、tool access、latency、prompt structure、retrieval order。若把“启用 Agent”视为一个 treatment，刺激材料可能与多个机制捆绑。这一点本文没有展开，但它直接决定后续实验能否解释机制。

### 5. Causal discovery 不是万能入口

Roadmap 明确提到 causal structure 可由 expert、data 或 hybrid 获得，同时引用了 causal graph 不稳定问题。这一点很重要：不能因为研究主题叫 Causality，就默认先跑 PC/FCI/GES 得到一张图再解释。

## Baseline 和 Ablation：本文为什么没有

这不是预测模型论文，所以没有可以拆掉的模块，也没有性能 baseline。若以后有人实现 CSE toolchain，更合理的 ablation 应该比较：无 Design Spec vs 有 Design Spec、只记录 treatment vs 同时记录 concurrent changes、point estimate vs uncertainty-aware decision、无 refutation vs placebo/sensitivity checks、static DAG vs version-aware causal model。

即使这些 ablation 有性能差异，也只能说明完整 workflow 的某个设计有帮助，不能自动证明对应的 causal assumptions 正确。

## 对 Causality for Code Review 的直接启发

你现在研究“加入 call graph / repository context 为什么可能反而下降”，可以直接借本文把问题重写成 intervention-centric design。

### 1. 把 Context Strategy 明确写成 Intervention

```text
T ∈ {diff-only, in-file, call-graph, full-repo}
```

而不是把不同 baseline 方法天然携带的不同 context 当作 treatment。否则模型、agent workflow、token budget、retrieval policy 会与 context treatment 捆绑。

### 2. Outcome 不要只留一个 accuracy

至少区分 review defect recall / precision、false positive、evidence localization、token / latency / cost，以及 review depth 或 exploration behavior。这样才能研究为什么总效果下降。

### 3. 把候选机制变成 mediator，而不是写进 Discussion

```text
Context Treatment
├─→ Relevant Evidence Coverage ─→ Review Quality
├─→ Irrelevant Token Ratio ─────→ Review Quality
├─→ Misleading Dependency ──────→ Review Quality
└─→ Search / Attention Allocation → Review Quality
```

如果只报告 `+CG` 比 `-CG` 低 2%，仍然不知道为什么；若 mediator 可干预或可靠测量，就可以进一步做 mediation / factorial experiment。

### 4. 把 Need-for-Repository-Context 看作 effect modifier

真正有价值的问题更接近：

\[
CATE(x)=E[Y(1)-Y(0)\mid X=x]
\]

其中 `X` 可以包括：是否存在跨文件依赖、调用距离、fan-out、task difficulty、change type、repository coupling 等。

### 5. 建一个 Code Review Intervention Log

如果后面做真实 PR 或 Agent online experiment，可以记录 instance/commit、treatment、model/version、prompt、context budget、retrieved files/functions、concurrent tool calls、outcome、failure/rollback。这就是本文 Intervention Log 在课题里的最小实现。

## 作者证明了什么

1. 作者建立了一个统一视角：软件工程中的 change 可以被视为 intervention，很多工程决策需要 `do` 和 counterfactual 语义，而不只是 correlation。
2. 作者给出了三类可版本化工件，将 causal assumptions、实际 intervention 和 runtime evidence 串成工程流程。
3. 作者把未来工作组织为 causal observability、intervenability、counterfactual assurance、governance 四条路线，并提出三类 benchmark 家族。
4. 作者明确要求 uncertainty、sensitivity、refutation 和“无法支持 claim”的失败模式进入评价标准。

## 作者没有证明什么

1. 没有实证证明 CSE workflow 相比现有 SE workflow 能提高质量、效率或可靠性。
2. 没有给出自动构建正确 DAG/SCM 的通用方法。
3. 没有解决大型、动态软件系统中 time-varying confounding、feedback loop 和 transportability 的全部识别问题。
4. 没有证明 LLM Agent 加 causal model 后就能可靠进行因果推理；“causal copilot”仍然是 roadmap 目标。
5. 没有提供一个可以直接拿来跑 code review 的 benchmark 或完整工具实现。

## 真正应该记住什么

- **第一件事不是选 causal estimator，而是把工程问题改写成明确的 intervention、outcome 和 assumptions。**
- **把假设写成可版本化、可审查的工件，是本文最值得借鉴的工程思想。**
- 软件本身已经有大量天然 intervention infrastructure：feature flag、canary、A/B、rollback；研究的机会是让这些机制服务于 causal identification。
- 对 Agent/Code Review 来说，“启用某方法”通常是复合 treatment，必须拆开 context、model、budget、tool access，否则难以解释 effect。
- 未来高质量 Causal SE benchmark 不应只提供 label，而应尽量提供 intervention ground truth、counterfactual evidence 或可控 causal mechanism。

## 对后续研究的一个具体落点

如果把本文真正落实到你现在的研究，我认为最值得做的不是再画一张大 DAG，而是先完成一个小而可识别的局部问题：

> **在固定模型、prompt、token budget 和代码变更的条件下，加入不必要的 call-graph context 是否通过 irrelevant/misleading evidence 改变代码审查质量？**

它天然适合配对或析因设计，也可以进一步测异质效应。相比“CG 能否提高总体 benchmark 分数”，这个问题更符合 CSE 所强调的 intervention-centric、mechanism-aware 和可证伪研究范式。
