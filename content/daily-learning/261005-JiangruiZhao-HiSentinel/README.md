# Learning When and How to Intervene: A Hindsight-Distilled Sentinel for Coding Agents

> 精读日期：2026-10-05  
> 论文：**Learning When and How to Intervene: A Hindsight-Distilled Sentinel for Coding Agents**  
> 作者：Jiangrui Zhao; Chenglong Li; Meng Zhang; Xiaoting Du†  
> 机构：Beijing University of Posts and Telecommunications; Beijing University of Technology; Meta  
> 通讯作者：Xiaoting Du（原文明确以 † 标注 corresponding author）  
> Venue / 年份：arXiv cs.SE / 2026  
> 原文：[arXiv:2609.39957](https://arxiv.org/abs/2609.39957) · [HTML 全文](https://arxiv.org/html/2609.39957) · [PDF](https://arxiv.org/pdf/2609.39957)  
> Tags：Coding Agent · Trajectory · Intervention · Hindsight Distillation · Human-in-the-loop · SWE-bench · Process Supervision

这篇论文研究的不是“怎样让 coding agent 更会写代码”，而是一个更像控制系统的问题：**agent 每一步准备执行动作时，什么时候应该放行，什么时候应该阻止并纠正，什么时候必须停下来问人？**

作者提出 HiSentinel：在 agent 的动作真正执行之前，用一个很小的 0.6B/1.7B Sentinel 做三分类：`Allow / Redirect / Hard-Pause`。训练时，teacher 可以偷看未来执行结果和任务结局；部署时 student 只能看到当前 task、已经发生的 trajectory prefix 和即将执行的 action。核心思想就是把“事后才知道这一步害不害人”的 hindsight，蒸馏到“事前就要作决定”的轻量监控器里。

最值得注意的不是单纯 14 个百分点的 SWE-bench 提升，而是论文把“错误检测”重新定义成了“**此时介入是否真的比让 agent 自己继续更可能提高最终完成率**”。这使它与普通 process critic、post-hoc diagnosis 有本质区别，也与我们当前从 file F1 转向 trajectory / attribution 过程证据的研究需求直接相关。

## 一、先建立全文地图

论文的顶层证据链是：

```text
Research Gap
post-hoc critic / execution feedback 往往来得太晚
        ↓
Research Object
action proposal 与 environment execution 之间的决策边界
        ↓
Operationalization
Allow / Redirect / Hard-Pause 三类 route
        ↓
Dataset
SWE-Intervene: 6,923 个 action-level decision points
        ↓
Method
future-aware teacher → hindsight distillation → causal lightweight sentinel
        ↓
Deployment
只看 pre-action prefix + proposed action
        ↓
Evidence
static recognition + OOD diagnosis + end-to-end SWE-bench / Ask-or-Assume
        ↓
Claim
高质量、及时的 pre-execution intervention
可以提高 task completion；关键不是“多干预”，而是“干预对”
```

理解全文需要四个概念。

**Pre-execution intervention**：agent 已经提出动作，但环境还没执行。Sentinel 在这里插入控制，相当于“提交动作之前最后一次闸门”。

**Privileged information**：训练阶段 teacher 可以看到部署时不可能看到的信息，比如这一步实际执行后的结果、后续 trajectory 和最终任务结果。student 不允许看到这些未来信息。

**Hindsight distillation**：不是把 teacher 的完整推理直接照抄给 student，而是把“哪些 future evidence 真的帮助判断是否应干预”的知识蒸馏回只看因果前缀的模型。

**Hard-Pause**：不是普通 Redirect。Redirect 表示 agent 自己有能力在反馈后修正；Hard-Pause 表示缺的是人类才拥有的信息、授权或偏好，必须暂停并提问。

## 二、Research Gap：为什么“发现错误”还不够

coding agent 是长轨迹系统。一处早期错误可能先改变仓库状态，再改变后续搜索，再改变 patch，最后才在测试或最终评估里暴露。

论文引用的 Terminal-Bench 结果很好地说明了时间差：失败轨迹中，决定性错误往往在早期出现，真正不可恢复也发生得较早，而首个明显可见的 failure signal 更晚。也就是说，等错误“显现”时再纠正，成本已经很高。

已有三类方法各有缺口：

1. **execution feedback**：等命令或 patch 执行以后才知道有问题；
2. **periodic process critics**：每隔若干步看一眼，可能错过真正危险的动作；
3. **post-hoc trajectory diagnosis**：能告诉你哪里错了，但已经无法阻止这次失败。

所以作者把问题往前推一步：

> 在动作真正执行之前，仅凭当前可见状态，能否判断“现在介入会不会提高最终 task completion”？

这比“这个动作是不是局部最优”更严格。一个动作即使有点笨，只要 agent 已经在恢复，就应该 Allow；反之，一个看起来合法的动作如果会把系统带进错误状态，就值得 Redirect。

## 三、三种 route 到底是什么意思

Table 1 是方法的核心定义。

### Allow

没有足够证据说明介入会提高任务完成率，因此原 action 正常执行。

注意它不是“动作完美”。论文明确保留了一些 locally imperfect、但 agent 正在自行恢复的动作作为 Allow。这个设计避免 Sentinel 退化成“代码洁癖检查器”。

### Redirect

当前 action 被拦截，不执行；Sentinel 给出简短、可操作的纠正建议，agent 根据反馈重新提出动作。

这是主要的自动化纠错路径。

### Hard-Pause

环境暂停，Sentinel 提出一个需要用户回答的问题。适用于缺失的信息、授权或偏好不是 agent 自己能够推断出来的情况。

这三类 route 对应三种不同 control flow，因此不是普通的三分类标签游戏，而是直接改变 agent runtime。

## 四、SWE-Intervene 是怎么构造出来的

SWE-Intervene 不是从人工编造错误动作开始，而是从真实/自然的软件工程 agent trajectories 抽 decision points。

数据源包括：

- Open-SWE-Traces：3,451 个实例；
- SWE-Hero：1,089 个；
- SWE-chat：2,383 个。

合计 **6,923 个 action-level 实例**。

训练集 5,680 条，held-out test 1,243 条；测试集中 1,122 条来自自然 trajectory，121 条来自 AskUserQuestion（AUQ）交互。

### 4.1 标注单位不是“整条 trajectory”

每个实例对应一个动作即将执行前的 decision point：

```text
task u
+ trajectory prefix h_t
+ proposed action a_t
→ intervention label y_t
```

recorded future 和最终 outcome 会保留给 annotation / teacher training，但部署 student 看不到。

### 4.2 为什么不能把所有可疑动作都标 Redirect

作者给 annotator 三个核心问题：

1. 这个问题是否真的威胁最终 task completion，而不只是“不优雅”？
2. agent 是否已经意识到问题并开始恢复？
3. 相比让 agent 自己继续，介入究竟能防止什么损失或消除什么障碍？

只有能给出 completion-relevant 理由，才标 Redirect。

这一步很重要，因为 coding agent 轨迹里存在大量“绕路但最终能成功”的行为。若把所有低效动作都当错误，Sentinel 会过度干预。

### 4.3 Hard-Pause 如何得到

自然轨迹里的 Hard-Pause 很稀少，因此作者从 SWE-chat 的 AskUserQuestion 交互中重建 decision point。

关键做法是把**当前问题以及后续 human answer 从 causal input 删除**，让 student 只能根据当时真实可见状态判断“是否需要问人”。

早于当前 decision point 的历史 human answer 可以保留，因为它们已经是 legitimately observed state。

### 4.4 两阶段人工审计

这是 dataset 最值得肯定的环节之一。

初始有 **2,252 个 provisional intervention candidates**。两阶段人工复核后删除 **570 个**，即 **25.3%**。

常见被删情况包括：

- 动作虽然不理想，但可以恢复；
- agent 已经发现问题并在修；
- Hard-Pause 标得过早，实际还不需要外部信息。

因此最终 intervention label 更接近“介入有净价值”，而不是“动作有瑕疵”。

但仍要注意：这些标签是 hindsight-informed judgment，不是随机实验测出的 individual treatment effect。论文自己明确承认，每个 node 只观察到真实发生的一个 continuation，没有同时观察“介入”和“不介入”两个 counterfactual outcome。

## 五、HiSentinel：训练时看未来，部署时不能看未来

### 5.1 问题形式化

Sentinel 在 step t 只接收：

```text
x_t = (task u, history h_t, proposed action a_t)
```

然后输出 route 和必要时的反馈。

训练时额外有 retrospective evidence `e_t`，比如真实 continuation、任务结果或真实 agent-human interaction。

这里最重要的边界是：

> label 是基于 hindsight 的专家判断，不是“实测介入能提高多少成功概率”的因果效应。

因此论文里的 “causal Sentinel” 指的是部署输入只包含因果上可用的 past/present 信息，不是说作者完成了严格的 causal treatment-effect estimation。

## 六、HGID：Hindsight-Guided Intervention Distillation

论文真正的方法贡献在这一层。

### Step 1：future-aware teacher

teacher 使用 Qwen3-Coder-30B-A3B-Instruct。

teacher 同时看到：

- causal prefix；
- proposed action；
- recorded future；
- task outcome。

它只判断 binary：

```text
Allow
vs
Intervene
```

为什么 teacher 不直接做三分类？因为自然 Hard-Pause 太少，而且 AUQ 之后的 suffix 已经受 human answer 影响，不能把这段未来当成干净的 privileged evidence。

### Step 2：student 保留三分类

student 用 Qwen3-0.6B 或 Qwen3-1.7B。

它仍直接学习：

```text
Allow / Redirect / Hard-Pause
```

也就是说：

- teacher 提供“是否值得介入”的 privileged signal；
- 原始三分类标签负责告诉 student“介入后应该自己纠正还是问人”。

### Step 3：helpfulness gate

这是 HGID 最容易被忽略、但实际上很重要的一步。

作者不是无条件相信 future-aware teacher，而是同时构造一个 **outcome-masked control view**。

只有当 future-aware teacher：

1. 判断正确；
2. 且加入 future 后，对正确标签的概率高于没有 future 的 control view；

distillation 才开启。

直觉上就是：

> 未来信息如果没有真正让 teacher 变得更有把握，就不要把它蒸馏给 student。

这样避免把“teacher 本来凭 prefix 就知道”的信息冒充 hindsight benefit。

### Step 4：KL distillation

student 一边做普通 route supervision，一边在 gate 开启时，通过 KL divergence 靠近 future-aware teacher 的 binary distribution。

部署时 teacher、future evidence 全部删除。

## 七、反馈模块为什么要单独训练

只判断 Redirect 不够。agent 还需要知道怎么改。

因此作者把 feedback learning 与 routing 分开：

1. 先 SFT，学习简洁、grounded 的 correction / question；
2. 再 DPO，让 preferred feedback 胜过 rejected feedback；
3. routing 参数冻结，feedback training 不能改变 Allow / Redirect / Hard-Pause 的选择。

这个模块化设计的意义是：如果 end-to-end 性能提升，可以进一步区分：

- route 选得更准；
- 还是反馈写得更有用。

Ablation 也确实验证了这点。

## 八、实验坐标系

### Models

Privileged teacher：

- Qwen3-Coder-30B-A3B-Instruct。

Sentinel：

- Qwen3-0.6B；
- Qwen3-1.7B。

coding agents：

- Qwen3-Coder-30B-A3B-Instruct；
- Devstral-Small-2-24B-Instruct-2512；
- Claude Sonnet 4.6 作为 closed-source reference。

统一使用 mini-SWE-agent harness。

### Static evaluation

三个 benchmark：

- SWE-Intervene：三分类；
- RootSE：失败 trajectory 的 root-cause / decisive-error localization；
- R-Judge Program subset：程序相关 reasoning trajectory 的 safe/unsafe 分类。

RootSE、R-Judge 都没有用于训练，因此承担 OOD transfer 验证。

### End-to-end evaluation

- SWE-bench Verified Mini：50 tasks；
- Ask or Assume：从 500 条中按 repository / difficulty 分层抽 100 条。

每条 task 最多：

- 30 分钟；
- 100 agent steps。

### Baselines

包含：

- Step-by-Step：每步 prompt-only pre-execution checker；
- SWE-PRM：每五步 taxonomy-guided feedback；
- Steer, Don’t Solve（SDS）；
- Reflexion；
- post-hoc 的 All-at-Once、AgentRx、TrajAudit、RCTA 等。

这里有一个公平性注意点：部分 baseline 是 pre-execution，部分是 post-hoc diagnosis，它们并不是完全同一 operational objective；static benchmark 的比较更多体现“能否识别关键步骤”，而真正 runtime value 应优先看 end-to-end。

## 九、Static intervention recognition：HiSentinel 是否真的学会了“什么时候介入”

Table 3 最值得看的不是全部数字，而是三个对比。

### 0.6B

在 SWE-Intervene：

- Step-by-Step M-F1：27.23；
- HiSentinel：79.99。

Intervention F1：

- 21.21 → 75.22。

### 1.7B

HiSentinel 达到：

- M-F1 = **81.77**；
- Intervention F1 = **78.97**。

### OOD

在 RootSE，HiSentinel 的 decisive-error localization 明显优于同规模 baselines；在 R-Judge 上也保持最佳或有竞争力的 balanced accuracy / macro-F1。

但这里不能直接推出“HiSentinel 一定能提高 agent 最终成功率”。Static recognition 是中间能力，真正重要的是下一节 end-to-end。

## 十、End-to-end：它是否真的让 coding agent 更成功

### Qwen3-Coder

原始 agent：

- SWE-V Mini：30%；
- Ask or Assume：23%。

1.7B HiSentinel：

- SWE-V Mini：**44%**；
- Ask or Assume：**33%**。

即分别 +14pp 和 +10pp。

0.6B HiSentinel 也提高到：

- 36%；
- 28%。

### Devstral

原始：

- 20% / 19%。

1.7B HiSentinel：

- **30% / 27%**。

### Sonnet 4.6

原始：

- 60% / 58%。

1.7B HiSentinel：

- **66% / 61%**。

所以效果不是只绑定在 teacher 同家的 Qwen agent 上，至少在三个 agent family 上都观察到正向变化。

代价是额外 token consumption。HiSentinel 并非“免费监督”，但成本与其他 feedback-based baseline 同一量级，并没有用巨额 token 换成功率。

## 十一、Ablation：到底哪一部分有用

### 11.1 去掉 distillation

1.7B full：

- M-F1 81.77；
- I-F1 78.97。

w/o Distillation：

- M-F1 76.42；
- I-F1 73.31。

静态差距不算巨大，但 end-to-end SWE-V Mini 从：

- **44% → 34%**。

这说明静态分类小幅差异可以放大成 runtime outcome 差异。

### 11.2 用 causal teacher 替代 future-aware teacher

static：

- 77.16 / 75.08。

end-to-end：

- **36%**。

仍显著低于 full 的 44%。

这支持 privileged future 确实提供额外监督价值。

### 11.3 去 helpfulness gate

M-F1 下降到 78.72，I-F1 77.41。

幅度不大，但方向一致。它支持 gate 有帮助，却不足以单独说明它是最大贡献组件。

### 11.4 Feedback

full：

- groundedness 76.8%；
- actionability 73.5%。

w/o DPO：

- 69.4%；
- 65.8%。

joint feedback training：

- 66.9%；
- 63.2%。

这说明 routing 与 feedback 分开优化是合理设计；“一起训”并没有更好。

## 十二、最重要的分析：不是干预越多越好

这是我认为整篇最值得记的一节。

在 SWE-bench Verified Mini，HiSentinel 一共触发 242 次 interventions：

- beneficial：109（45.0%）；
- neutral：106；
- harmful：27。

最终有：

- 8 次 rescue；
- 1 次 regression；

resolved count 从 15/50 提到 22/50。

对照：

- Step-by-Step：24 次 intervention 里只有 1 次 beneficial，1 rescue；
- SWE-PRM：284 次里只有 3 次 beneficial，1 rescue，却有 **6 regressions**。

所以核心不是 intervention frequency，而是 intervention precision / utility。

这也解释了一个很重要的非对称性：

> false alarm 有时 agent 还能识别并绕过去；  
> missed necessary intervention 则会让错误 action 真的执行，后果传播。

作者因此发现 intervention recall 对 runtime success 特别重要。

## 十三、为什么作者坚持每一步重新计算 causal prefix

看起来可以对 Sentinel 的 trajectory prefix 做 KV cache 复用，以降低成本。

实验中，未截断调用能复用 86.4% 输入 token，但 1,869 次调用中有 906 次需要 left truncation，此时复用率只有 3.2%。

总体 token processing 只减少约 22%：

- 382K → 299K / task。

而 wall-clock 几乎没变：

- 757s → 763s。

更关键的是，896 个 token-identical routing calls 中仍出现：

- 13 次 route flip；
- 3 次 effective-intervention flip。

最终 SWE-V Mini resolution：

- full recomputation：22/50；
- cross-step caching：18/50。

因此作者选择每一步重新算完整 causal prefix。

这组结果提醒：agent monitoring 的工程优化本身也可能改变 decision boundary，不能只按 token saving 判断“语义等价”。

## 十四、Case Study：什么叫有效 Redirect

Figure 3 用 Sphinx issue 展示一次成功 intervention。

任务要求：

- 对 extension 自动生成文档，不报 missing-document warning；
- 对真正缺失文档，仍然保留 warning。

agent 原计划写一个 nested branch + empty `pass`，但控制流仍会落进原 warning logic。

HiSentinel 在 action 执行前阻止 patch，并指出应把 generated-document check 放到 missing-document branch 之前。

agent 重新检查代码后修正，最后：

- 目标测试通过；
- 9 个 regression tests 也通过；
- paired no-intervention run 未解决。

这是一个很好的机制案例，但仍只是 case study，不能代替总体因果证据。

## 十五、Evidence Audit：论文最大的强点和最大的边界

### 强点 1：明确区分“坏动作”与“值得干预的动作”

25.3% provisional intervention candidates 被人工删除，说明作者认真处理了 autonomous recovery 与 over-intervention。

### 强点 2：teacher 的 future advantage 有 control view

helpfulness gate 至少尝试验证“future 信息真的增加了 teacher 信息量”，比直接用全 trajectory teacher 更干净。

### 强点 3：最终看 end-to-end，而不是停在 classification F1

w/o distillation 的 static gap 不大，却导致 44% → 34% resolution，证明中间指标不能替代真实 outcome。

### 边界 1：intervention label 仍不是 causal treatment effect

最关键的一句其实在方法里：每个 decision point 只有 realized continuation。

作者不知道同一个状态下：

```text
Allow 会怎样
vs
Redirect 会怎样
vs
Hard-Pause 会怎样
```

三个 counterfactual outcome。

因此“intervention would help”是 hindsight-informed expert judgment，不是 randomized causal effect。

### 边界 2：candidate node selection 有选择机制

dataset 不是均匀抽取所有 agent steps，而是优先挑 decision-critical nodes。它很适合训练 Sentinel，但不能直接代表真实 runtime 中 intervention base rate。

### 边界 3：标签高度依赖 GPT-5.5 + 人工审核协议

虽然人工审计很严格，但仍不存在完全客观的 ground truth。特别是“agent 是否本来能自己恢复”本质上含 counterfactual judgment。

### 边界 4：SWE-bench Mini 只有 50 条

end-to-end improvement 很有说服力，但样本量仍有限，且多个 intervention 发生在同一个 task 内，不能把 action 数当独立 task 数做统计解释。

## 十六、作者与团队背景

第一作者 **Jiangrui Zhao** 在论文中署名 Beijing University of Posts and Telecommunications。公开可核验的个人研究档案有限，因此不从作者顺序或少量论文反推出其长期方向。

通讯作者 **Xiaoting Du** 是北京邮电大学计算机学院教师。其公开主页显示研究积累覆盖 software reliability、deep-learning-system bugs、software maintenance 与 LLM 相关软件工程；其近期工作也涉及模型对程序结构/语义的学习、代码生成可靠性和 dependable intelligent systems。HiSentinel 延续的是“软件系统可靠性 + 智能模型可靠性”的交叉路线：不是只追求 agent solve rate，而是研究错误如何在执行链路中被提前识别和控制。

原文明确标注 Xiaoting Du 为 corresponding author，因此这里不需要按末位作者推断。

## 十七、论文证明了什么

较强证据支持：

1. action proposal 与 execution 之间是一个有价值的 agent-control 边界。
2. future-aware supervision 经 distillation 后，可以显著提高轻量 Sentinel 的 intervention recognition。
3. HiSentinel 的提升能转化为 Qwen、Devstral、Sonnet 三类 coding agent 的 end-to-end solve-rate 增益。
4. intervention quality 比 intervention frequency 更重要；大量低质量监督可能制造 regression。
5. future-aware teacher、helpfulness gate、独立 feedback optimization 都有增益证据，其中 privileged distillation 对 end-to-end 影响尤其明显。

论文没有证明：

1. 没有测出某个 action 上 Redirect 相对 Allow 的真实 individual causal effect。
2. 没有证明三分类标签是唯一正确的 intervention taxonomy。
3. 没有证明更多 process monitoring 总是有益；论文自己记录了 harmful interventions。
4. 没有证明在漏洞定位、code review 或 repository-context retrieval 上直接成立。
5. 没有证明 teacher 的 hindsight reasoning 能完全被小模型因果地复原；观察到的是预测与 end-to-end 性能提升。

## 十八、对当前研究的启发

当前 VLocBench 主线已经明确：五例中 plausible 与 random 平均 F1 都是 0.5810，不能预设 plausible 更危险；下一步重点是区分 mechanism correctness、evidence attribution 与 final file outcome。

HiSentinel 对这个阶段有四个直接启发。

### 1. 把“何时发生 attribution shift”变成 decision-point 问题

不要只比较整条 prompt 的最终 file list。可以把模型推理过程拆成若干可观察 decision points：

```text
读取 core evidence
→ 读取新增 context
→ 提出 mechanism hypothesis
→ 选择 supporting evidence
→ 提交 files
```

然后问：**第一次 evidence attribution 被 plausible/random context 改变发生在哪里？**

这比只看 final F1 更接近 failure lifecycle。

### 2. 不要把所有偏离都叫“被误导”

HiSentinel 最大的经验之一是：locally imperfect ≠ worth intervention。

同样：

- 模型读取了 plausible node；
- 提到了 peripheral file；
- 或额外探索了 sibling；

都不自动等于 harmful attribution。

必须要求这个变化最终改变核心 evidence、mechanism 或 localization decision，才能标成真正 harm。

### 3. 现有 annotation 不等于 causal effect

HiSentinel 自己非常诚实地区分 hindsight judgment 和 counterfactual measurement。

我们的 “plausible node 是 non-decisive” 标注也应采用同样纪律：人工认为它不必要，不等于已经证明“加入它会降低 outcome”。

真正 treatment effect 仍必须靠 paired intervention：

```text
same task + same core evidence + same budget
random vs plausible
```

### 4. 可以引入 rescue / regression 指标

除了：

- official F1；
- Mechanism Correctness M；
- Attribution Correctness A；

还可以定义：

- **rescue**：control 错、某 context condition 对；
- **regression**：control 对、某 context condition 错；
- **neutral**：决策没实质变化。

对于 plausible-noise，`regression rate` 可能比平均 F1 更直接回答“它有没有把本来能做对的实例带坏”。

## 十九、真正应该记住什么

1. agent monitoring 最关键的边界可能不是执行后，而是 action proposal 与 execution 之间。
2. 判断“动作不完美”远远不够；真正问题是“现在介入是否比让 agent 自己恢复更有价值”。
3. SWE-Intervene 的 25.3% intervention-candidate rejection 是本文最重要的数据质量信号之一。
4. privileged future supervision 的 static F1 增益不算夸张，却能造成 44% vs 34% 的 end-to-end 差距。
5. 干预越多不等于越好；242 次 HiSentinel intervention 也有 27 次 harmful。
6. 对当前 repository-context 研究，最值得借鉴的是：**把最终性能差异继续向前定位到具体 decision point，并区分 harmless deviation、rescue、regression 与真正 attribution shift。**
