# Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?

> Thibaud Gloaguen, Niels Mündler, Mark Müller, Veselin Raychev, Martin Vechev  
> arXiv:2602.11988v2 [cs.SE], 2026；MemAgents @ ICLR 2026（Oral & Runner-up Best Paper）  
> 原文：https://arxiv.org/abs/2602.11988  
> PDF：https://arxiv.org/pdf/2602.11988

## 一句话论文地图

过去大家默认 `AGENTS.md` / `CLAUDE.md` 这种 repository-level context file 能帮助 Coding Agent 理解仓库；这篇论文第一次把这个工程惯例当成可干预变量系统评测。结论并不是“上下文一定有害”，而是：**LLM 自动生成的 context file 没有显著提高成功率，却稳定让 Agent 做更多探索、测试和推理，使成本上升 20%+；人工 context file 略好，但对 None 的提升仍不显著。**

这篇和最近的 RepoMirage、Context Compression、SWE-Skills-Bench 能串成一条很清楚的研究线：**额外 context → 行为改变是确定的；performance gain 却不是确定的。真正需要解释的是 context 如何改变 Agent 的探索与决策过程。**

## 作者与课题组背景

### 第一作者：Thibaud Gloaguen

Gloaguen 自 2025 年 5 月起是 ETH Zürich Secure, Reliable, and Intelligent Systems Lab（SRI Lab）的博士生，导师是 Martin Vechev；此前在 ETH 读 Statistics MSc，并有 École Polytechnique 应用数学背景。公开发表轨迹目前主要集中在 LLM security、watermarking 和 Coding Agent，因此个人仍处博士早期阶段，**目前更值得记住的是他所在的 SRI Lab / Vechev 学术谱系，而不是把他本人当成已经形成独立地位的软工学者。**

### Senior / 末位作者：Martin Vechev

论文页面没有标注通讯作者，因此这里不把末位作者 Martin Vechev 擅自称为“通讯作者”。Vechev 是 ETH Zürich 计算机系 Full Professor、SRI Lab 负责人，也是 INSAIT 的 Founder and Architect。其根基并不是传统 empirical software engineering，而是 **Programming Languages、program analysis、program synthesis、formal reasoning 与 AI for code**；他获得过 ACM SIGPLAN Robin Milner Young Researcher Award，并曾任 PLDI 2017 Program Chair。

对你来说，这个组非常值得认识，但要把位置说准确：**它不是 Bacchelli / Storey / Hassan 那种传统 code review / empirical SE 学派，而是 PL + program analysis + AI for code 的强组，并且很早把研究产业化。** Vechev 团队孵化过 DeepCode（2020 被 Snyk 收购）、ChainSecurity、LatticeFlow；Veselin Raychev 的博士论文 *Learning from Large Codebases* 获 ACM Doctoral Dissertation Award Honorable Mention。Raychev 后来共同创办 DeepCode，目前又与 Vechev、Mark Müller 等做 LogicStar，方向直接进入 autonomous software maintenance、Coding Agent evaluation 和真实代码库上的 agent optimization。

因此今天这篇不是“传统软工组突然研究 AGENTS.md”，而更像是 **一个长期研究程序分析/代码智能、又真正做过工业代码分析产品的团队，开始系统审计 Coding Agent 的工程惯例。** 这也是它值得你认真看的原因。

代表性的近年相关工作包括：BaxBench（ICML 2025 Spotlight，LLM 生成 backend 的正确性与安全性）、CodeTaste（ICML 2026，LLM refactoring）、Coding Agents Don't Know When to Act（COLM 2026），以及今天的 AGENTS.md 工作。SRI Lab 页面将本文列为 MemAgents @ ICLR 2026 Oral & Runner-up Best Paper。

## 先看大图：作者到底怎么评 AGENTS.md？

![Figure 1 — Evaluation pipeline](https://arxiv.org/html/2602.11988v2/Overview.png)

**这张图先抓住三个 treatment。** 对同一个真实 repository state 和 issue，作者让 Agent 面对三种环境：①仓库原本就有的 developer-provided context file；②把 context file 拿掉（None）；③按 Coding Agent 官方推荐方式自动生成一个 context file（LLM）。之后 Agent 正常解决 issue，作者同时看最终 patch 是否通过测试，以及 action trace 怎么变化。

这比简单比较“用了 AGENTS.md 的项目 vs 没用的项目”强很多，因为后者会严重混入项目类型、团队成熟度、任务难度等差异。这里的核心思想是：**尽量保持 task / repository 不变，只操纵 context-file availability。**

> 注：本次从完整 PDF 核对了 Figure 1 与 Figure 3；当前 GitHub 连接器只能写 UTF-8 文本、不能上传二进制截图，因此正文暂时直接嵌入 arXiv 官方 HTML 从论文原图提取出的 Figure 1，而不是自己重画。后续连接器支持二进制资产时应改为仓库本地图片。

## 1. 它到底在问什么？

AGENTS.md 的逻辑看起来很自然：模型不知道项目结构，那就提前告诉它目录、测试命令、代码风格、设计约束。问题是，这里偷偷把两个命题混在了一起：

1. Agent 会不会遵循这些信息？
2. 遵循以后会不会更容易完成任务？

论文最关键的贡献就是把两者拆开。实验显示 **Agent 确实会遵循 context file**，但“遵循”主要表现为更多测试、更多文件遍历、更多专用工具调用和更多 reasoning；这些额外行为并没有稳定转化成更高 task success。

这和你的研究问题非常接近：`Context → Behavior` 可能是强效应，但 `Context → Outcome` 可以接近 0，甚至为负。真正值得研究的是中间的 mediator。

## 2. CTXbench 为什么要重新造？

现成 SWE-bench 有一个硬伤：经典任务的 repository state 太早，当时还没有开发者真正提交的 AGENTS.md / CLAUDE.md。作者因此新建 CTXbench：从带 developer-committed context file 的真实 Python 仓库里找历史 PR。

最终 CTXbench 有 **138 个实例、12 个仓库**，从 5,694 个 PR 中筛出；任务同时包括 bug fixing 和 feature addition。平均 codebase 有 3,337 个文件，gold patch 平均改 2.5 个文件、118.9 行；context file 平均 641 词、9.7 个 section。

数据构建并非完全“天然”：作者用 LLM 标准化 issue 描述，也为很多 PR 生成回归测试，然后验证测试在 base state 失败、gold patch 后通过，并人工检查过拟合测试。这提高了可执行性，但也引入一个需要记住的构念风险：**CTXbench 衡量的是被重新规格化、被生成测试约束后的 task resolution，而不是原始 GitHub issue 的全部真实语义。**

## 3. Treatment、Outcome 和实验配置

作者在两个 benchmark 上做实验：SWE-bench Lite 300 个任务用于测试 LLM-generated context；CTXbench 138 个任务可以同时测试 None、LLM-generated 和 developer-provided context。

四个模型/Agent 配对是 Claude Code + Sonnet-4.5、Codex + GPT-5.2、Codex + GPT-5.1 mini、Qwen Code + Qwen3-30B-Coder。主 Outcome 是 tests 全过的 success rate；同时记录 steps 和 inference cost。每个 agent/instance/configuration **只采样一次**，这点很重要：temperature 虽然多数设为 0，但 Agent 仍可能存在工具环境与模型层面的非确定性，因此单次运行限制了对方差的估计。

## 4. 最核心结果：加 context 没显著变强，但一定更贵

PDF Figure 3 和 Table 2 是全文最该看的结果。

在 SWE-bench 上，LLM-generated context 相对 None 的平均 success rate **下降 0.5 个百分点**；在 CTXbench 上下降 **2 个百分点**。两者都不显著：p=0.87 和 p=0.37。

但成本效应非常稳定：LLM-generated context 在两个 benchmark 上平均分别多 **2.45 / 3.92 steps**，推理成本平均增加 **20% / 23%**，成本差异显著。也就是说最稳的 treatment effect 不是“准确率下降”，而是：

```text
Context File
    ↓
Agent 遵循更多指令
    ↓
更多 exploration / testing / reasoning
    ↓
Steps ↑  Token/Cost ↑
    ↓
Success Rate ≈ 没有稳定改善
```

Developer-provided context 比 LLM-generated context 好：在 CTXbench 上平均高约 7 个百分点，二者差异 p=0.038。但 **Dev vs None 仅平均 +2.4 个百分点，p=0.21，不显著**；同时 Dev 仍平均增加 3.34 steps，成本最高增加约 19%。所以不能把论文概括成“人工 AGENTS.md 有用”：证据只支持“人工的比自动生成的好”，不支持“人工的一定比没有更好”。

## 5. 为什么会这样？行为轨迹比最终分数更重要

作者进一步看 action traces。一个非常直观的指标是：Agent 第一次碰到 gold PR 实际修改文件之前走了多少步。没有 context file 时通常更早触达这些文件；有 context 后，Agent 会先花更多动作理解仓库、运行测试、执行 context 中要求的流程。

因此这里出现一个和 RepoMirage 几乎同构的现象：**更多 context 让 Agent 更“勤奋”，但勤奋不等于有效。** RepoMirage 里是 repository evidence 被结构性分散后 exploration drift；这里则是 context file 主动注入额外要求，诱发 broader exploration。

这给你一个非常好的统一机制候选：

```text
Additional Context
      ↓
Instruction / Evidence Exposure
      ↓
Exploration Breadth ↑
      ↓
Relevant Evidence Hit Time ↑ ?
Decision Latency ↑ ?
      ↓
Useful Evidence Conversion 不升反降 ?
      ↓
Outcome 不改善 / 下降
```

注意后面带 `?` 的链条是你可以研究的，不是本文已经证明的。

## 6. 一个容易被标题带偏的地方

标题很容易被二手文章写成“AGENTS.md makes agents worse”。论文证据其实更克制。

严格说：

- LLM-generated context 在 5/8 个 model×benchmark setting 中下降，但平均 success-rate 差异**不显著**；
- developer context 对 None 平均 +2.4pp，同样**不显著**；
- 最强、最稳定的结论是 **context file 增加 steps / inference cost**；
- developer context 显著优于 LLM-generated context，但这不等于显著优于 None。

因此如果你以后引用它，最好写：**context files did not significantly improve task success, while consistently increasing agent effort and inference cost**，不要写成“context files causally reduce performance”。

## 7. 因果与证据审计

### 做得好的地方

**Treatment 很清楚。** None / LLM / Dev 是实际可操作的 intervention，不是观察性标签。

**Outcome 可执行。** patch 通过测试比 LLM-as-a-judge 更硬。

**机制数据存在。** trace 让研究不止停在 success rate，而能观察 context 如何改变行为。

**跨模型/Agent。** Claude Code、Codex、Qwen Code 减少了单一 harness 偶然性的担忧。

### 仍然没有解决的地方

**一次运行。** 每个配置只 sample once，不足以分解 agent stochasticity。

**Context 不是单一变量。** 一个文件同时包含 overview、commands、style、testing、workflow 等多种内容；整体 treatment 不能告诉你到底哪类信息有害。

**任务与测试经过 LLM 构造。** CTXbench 的 issue refinement 和 generated tests 可能改变原任务构念。

**只看 Python。** 外部有效性不能直接推广到 Java/C++/大型企业 monorepo。

**Mediator 仍偏粗。** “更多 steps / 更多 testing”能解释成本，却还不能证明为什么 performance 没涨；例如真正需要的是 relevant-evidence precision、first useful evidence time、错误 hypothesis persistence 等更细的变量。

## 8. 对你当前 Causality for Code Review 最直接的价值

这篇比单纯“Full Repo 比 Diff 差”更值得借鉴，因为它展示了一个很干净的研究范式：**把 context 当 Treatment，把 trajectory 当 Mediator，把任务质量当 Outcome。**

你在 AACRBench 可以进一步做得比它更细。不要只设 `Diff / In-file / Repo` 三档，而是拆出：

```text
T1: relevant context only
T2: relevant + redundant context
T3: relevant + irrelevant context
T4: relevant + misleading-but-plausible context
T5: relevant context with graph structure
```

然后记录：

```text
M1 = files inspected
M2 = relevant evidence hit rate
M3 = first relevant evidence step
M4 = Explore → Explore transition
M5 = Explore → Review/Comment transition
M6 = unsupported hypothesis count
M7 = evidence actually cited/used in final review
Y  = defect detection / precision / review quality / cost
```

这样你的论文就不再只是“context 越多越差”，而会变成：**什么类型的 context，通过什么行为机制，在什么 task-demand 条件下产生正/负 treatment effect。**

尤其值得做 `Context Need × Context Relevance` 的异质效应：对真正需要 repo evidence 的任务，relevant context 应该有正效应；对 diff-local 任务，同样的 repository context 可能主要增加 exploration burden。如果这个 interaction 稳定，你的结论会比“call graph 有没有用”强很多。

## 9. 作者证明了什么 / 没证明什么

**证明得比较扎实的：** context file 会真实改变 Agent 行为；自动生成的 context file 没有带来显著 success-rate 提升；额外 context 会稳定增加 steps 和推理成本；人工 context 显著优于自动生成 context。

**没有证明的：** context 越多性能一定越差；repository overview 本身是性能下降的因果原因；attention dilution 是机制；人工 AGENTS.md 一定提升性能；这些结论能直接推广到 code review。

## 10. 真正应该记住的

如果只记一句：

> **“模型会不会用 context”与“context 会不会帮到模型”是两个完全不同的问题。**

这篇最有价值的不是告诉工程师“删掉 AGENTS.md”，而是把一个行业默认最佳实践改造成了可检验的 intervention。对你当前研究，下一步也应该从“加 Call Graph 后分数为什么掉”转向：**Context Treatment → Exploration / Evidence Utilization → Review Outcome**，并把 task-level context need 作为 effect modifier。