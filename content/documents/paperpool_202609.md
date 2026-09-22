# Paper Pool · 2026-09

> 2026 年 9 月完整精读记录。当前月份每日精读只需读取本文件；跨月永久去重读取 `paperpool_short.md`。

## 已精读论文

### 2026-09-22

- **The First Drop of Ink: Nonlinear Impact of Distracting Information in Long-Context Reasoning**
  - 简称：[First Drop of Ink](https://38-76-161-31.sslip.io/daily-learning/?paper=260922-MuhanGao-FirstDropInk)
  - Tags：`2026` `ICML` `Long Context` `RAG` `Hard Distractor` `Attention Mechanism` `Context Interference` `因果实验设计` `Plausible Noise`
  - 作者：Muhan Gao; Zih-Ching Chen; Kuan-Hao Huang
  - Venue / 年份：ICML 2026
  - DOI / 原文：[arXiv:2605.10828](https://arxiv.org/abs/2605.10828)
  - 主题：Long-Context Reasoning、Hard Distractor、Attention Competition、Controlled Context Intervention
  - 一句话价值：在固定 gold evidence 与总 context length 下，以 random/easy distractors 替换为 BM25 高相关但不含答案的 hard distractors，发现伤害高度前置且非线性；retrieval-head logit 分析显示 hard token 的 softmax competition 可远强于 easy token。对当前研究最关键的启发是将 plausible repository noise 设计成 gold-fixed、budget-matched 的 dose-response intervention，并重点检验“第一个少量 plausible distractor”与 mechanism→attribution 位移。

- **Agent Retrieval Bench: Evaluating Repository Context Retrieval for Coding Agents**
  - 简称：[ARB](https://38-76-161-31.sslip.io/daily-learning/?paper=260922-BowenQin-AgentRetrievalBench)
  - Tags：`2026` `arXiv/Preprint` `Coding Agent` `Repository Context` `Context Retrieval` `上下文工程` `代码定位` `Agent Trajectory` `Evidence Acquisition` `Benchmark`
  - 作者：Bowen Qin; Yi Xie
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2607.24882](https://arxiv.org/abs/2607.24882)
  - 主题：Repository Context Retrieval、Coding Agent、Context Acquisition、Trajectory、Evidence Localization
  - 一句话价值：把 repository context acquisition 从最终 patch outcome 中独立出来评测，并通过 fixed-agent seed intervention 显示 initial context 会改变 evidence hit、后续探索成本与最终定位；对当前研究最关键的启发是把 Context Treatment → Evidence Acquisition → Exploration → Utilization → File Reporting 建成机制链。
### 2026-09-21

- **Beyond Function-Level Analysis: Context-Aware Reasoning for Inter-Procedural Vulnerability Detection**
  - 简称：[CPRVul](https://38-76-161-31.sslip.io/daily-learning/?paper=260921-YikunLi-CPRVul)
  - Tags：`2026` `arXiv/Preprint` `漏洞检测` `Inter-Procedural Analysis` `Repository Context` `Context Selection` `Structured Reasoning` `Code Property Graph` `Context Utilization`
  - 作者：Yikun Li; Ting Zhang; Jieke Shi; Chengran Yang; Junda He; Xin Zhou; Jinfeng Jiang; Huihui Huang; Wen Bin Leow; Yide Yin; Eng Lieh Ouh; Lwin Khin Shar; David Lo
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2602.06751](https://arxiv.org/abs/2602.06751)
  - 主题：Inter-Procedural Vulnerability Detection、Repository Context、Security Profiling、Context Selection、Structured Reasoning
  - 一句话价值：raw caller/callee/global context 甚至经过 profiling 与 selection 后直接交给传统分类器仍可能降性能，而 structured reasoning 带来主要增益；对当前研究最关键的启发是把 context availability 与 evidence utilization 拆开，并测试 Context Treatment × Reasoning Treatment 的交互。

### 2026-09-20

- **Context Pruning for Coding Agents via Multi-Rubric Latent Reasoning**
  - 简称：[LaMR](https://38-76-161-31.sslip.io/daily-learning/?paper=260920-JingjingWang-LaMR)
  - Tags：`2026` `arXiv/Preprint` `Coding Agent` `上下文工程` `Context Pruning` `Repository Context` `Semantic Evidence` `Dependency Support` `CRF` `Mixture-of-Experts`
  - 作者：Jingjing Wang; Xiwen Chen; Wenhui Zhu; Huayu Li; Zhengxiao He; Feiyang Cai; Ana S. Carreon-Rascon; Xuanzhao Dong; Feng Luo
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2605.15315](https://arxiv.org/abs/2605.15315)
  - 主题：Context Pruning、Coding Agent、Semantic Evidence、Dependency Support、Repository Context
  - 一句话价值：把代码上下文相关性拆成 semantic evidence 与 dependency support，并用独立 CRF + query-adaptive MoE 建模；对当前研究最关键的启发是 context utility 具有条件性，可将 node selection、representation fidelity 与 evidence-support composition 拆成独立 treatment。

### 2026-09-19

- **Hierarchical Context Pruning: Optimizing Real-World Code Completion with Repository-Level Pretrained Code LLMs**
  - 简称：[HCP-Coder](https://38-76-161-31.sslip.io/daily-learning/?paper=260919-LeiZhang-HCPCoder)
  - Tags：`2025` `AAAI` `仓库级代码补全` `上下文工程` `上下文裁剪` `Repository Dependency` `长上下文` `Code LLM` `Cross-file Context` `Context Representation`
  - 作者：Lei Zhang; Yunshui Li; Jiaming Li; Xiaobo Xia; Jiaxi Yang; Run Luo; Minzheng Wang; Longze Chen; Junhao Liu; Qiang Qu; Min Yang
  - Venue / 年份：AAAI 2025
  - DOI / 原文：[DOI:10.1609/aaai.v39i24.34782](https://doi.org/10.1609/aaai.v39i24.34782); [arXiv:2406.18294](https://arxiv.org/abs/2406.18294); [Code](https://github.com/Hambaobao/HCP-Coder)
  - 主题：Hierarchical Context Pruning、Repository Dependency、Cross-file Context、Code Completion、Context Representation
  - 一句话价值：将 repository context 拆成依赖结构与节点内部表示粒度，在保留文件拓扑关系的同时大量裁掉依赖文件的具体实现，把约 50k token 的 full-repository prompt 压到约 8k；对当前研究最关键的启发是把 node selection 与 node representation 分成独立 treatment，检验 relevance × representation fidelity 的交互。

- **RepoGraph: Enhancing AI Software Engineering with Repository-level Code Graph**
  - 简称：[RepoGraph](https://38-76-161-31.sslip.io/daily-learning/?paper=260919-SiruOuyang-RepoGraph)
  - Tags：`2025` `ICLR` `仓库级代码图` `上下文工程` `Coding Agent` `SWE-bench` `图检索` `上下文噪声` `Context Depth` `代码定位`
  - 作者：Siru Ouyang; Wenhao Yu; Kaixin Ma; Zilin Xiao; Zhihan Zhang; Mengzhao Jia; Jiawei Han; Hongming Zhang; Dong Yu
  - Venue / 年份：ICLR 2025
  - DOI / 原文：[ICLR Paper](https://proceedings.iclr.cc/paper_files/paper/2025/hash/4a4a3c197deac042461c677219efd36c-Abstract-Conference.html); [arXiv:2410.14684](https://arxiv.org/abs/2410.14684); [Code](https://github.com/ozyyshr/RepoGraph)
  - 主题：Repository Graph、Graph Retrieval、Repository Context、Coding Agent、Context Expansion
  - 一句话价值：用行级 definition/reference 图为 SWE-bench 系统提供 k-hop ego-graph 上下文；最关键的消融显示 1-hop flatten resolve rate 为 29.67%，2-hop flatten 扩张到约 10.5k token 后反降至 26.00%，而 summary 可部分恢复，直接暴露 graph depth、token dilution 与 representation 之间尚未识别的机制。

### 2026-09-18

- **PhantomCall: Evading ML Malware Detectors via Function Call Graph Perturbation**
  - 简称：[PhantomCall](https://38-76-161-31.sslip.io/daily-learning/?paper=260918-MdAjwadAkil-PhantomCall)
  - Tags：`2026` `arXiv/Preprint` `软件安全` `恶意软件检测` `对抗机器学习` `Function Call Graph` `图结构扰动` `语义保持干预` `黑盒攻击` `因果实验设计`
  - 作者：Md Ajwad Akil; Adrian Shuai Li; Imtiaz Karim; Arun Iyengar; Ashish Kundu; Elisa Bertino
  - Venue / 年份：arXiv cs.CR / 2026
  - DOI / 原文：[arXiv:2609.00705](https://arxiv.org/abs/2609.00705)
  - 主题：Function Call Graph、Adversarial Malware、Semantics-Preserving Perturbation、Graph Topology、Black-box Search
  - 一句话价值：通过在真实可执行 Windows PE 中注入 dummy functions，显式操纵 FCG 的节点、边、注入量与拓扑，同时用 sandbox 验证行为保持；对当前研究最关键的启发是把 call-graph intervention 拆成 dose × topology × location，并将 treatment fidelity、semantic fidelity 与 matched budget 分开验证。

- **RepoReasoner: Evaluating Repository-Level Code Reasoning Ability of Long-Context Language Models**
  - 简称：[RepoReasoner](https://38-76-161-31.sslip.io/daily-learning/?paper=260918-YanlinWang-RepoReasoner)
  - Tags：`2026` `FSE` `仓库级推理` `上下文工程` `长上下文` `调用链` `动态执行` `代码理解` `LLM评测` `Benchmark`
  - 作者：Yanlin Wang; Suiquan Wang; Yanli Wang; Bowen Zhang; Daya Guo; Jiachi Chen; Zibin Zheng
  - Venue / 年份：FSE 2026 / Proc. ACM Softw. Eng. 3, FSE124
  - DOI / 原文：[DOI:10.1145/3808131](https://doi.org/10.1145/3808131); [arXiv:2607.25996](https://arxiv.org/abs/2607.25996); [Code](https://github.com/DeepSoftwareAnalytics/RepoReasoner)
  - 主题：Repository-Level Reasoning、Long Context、Call Chain、Context Noise、Oracle Context
  - 一句话价值：用动态执行 trace 构造 Oracle context 与 call-chain ground truth，并比较 10k/30k retrieval context，显示完美相关文件并不能消除跨文件推理失败，更多 context 对不同模型还呈正负异质效应；对当前研究最关键的是把“relevant evidence 是否到场”和“模型能否利用 evidence”分开，并把 signal/noise、dependency depth 改造成可控 context intervention。

- **Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?**
  - 简称：[AGENTS.md](https://38-76-161-31.sslip.io/daily-learning/?paper=260918-ThibaudGloaguen-AgentsMD)
  - Tags：`2026` `arXiv/Preprint` `ICLR Workshop` `上下文工程` `Coding Agent` `仓库级上下文` `AGENTS.md` `Agent行为` `推理成本` `Benchmark`
  - 作者：Thibaud Gloaguen; Niels Mündler; Mark Müller; Veselin Raychev; Martin Vechev
  - Venue / 年份：MemAgents @ ICLR 2026 / arXiv 2026
  - DOI / 原文：[arXiv:2602.11988](https://arxiv.org/abs/2602.11988)
  - 主题：Coding Agent、Repository Context、AGENTS.md、CTXbench、行为轨迹、成本
  - 一句话价值：在 SWE-bench Lite 与新建 CTXbench 上操纵 None/LLM-generated/developer context file，发现 context file 不显著提高成功率，却稳定增加探索步骤与 20%+ 推理成本；对 Causality for Code Review 的关键启发是把 Context 作为 Treatment、trajectory 作为 Mediator，并区分“模型会遵循上下文”与“上下文真正改善 Outcome”。

### 2026-09-17

- **RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations**
  - 简称：[RepoMirage](https://38-76-161-31.sslip.io/daily-learning/?paper=260917-HanyuLi-RepoMirage)
  - Tags：`2026` `arXiv/Preprint` `上下文工程` `Coding Agent` `仓库级推理` `语义保持扰动` `反事实干预` `探索漂移` `SWE-bench` `Agent行为`
  - 作者：Hanyu Li; Yichi Zhang; Speed Zhu; Hang Su; Jun Zhu; Yinpeng Dong
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2605.26177](https://arxiv.org/abs/2605.26177)
  - 主题：Repository Context、Coding Agent、语义保持扰动、探索漂移、构念效度
  - 一句话价值：通过保持 issue/功能/测试不变、只改变仓库证据暴露方式的 perturbation，RepoMirage 发现 8 个模型平均 resolved rate 从 66.80% 降到 49.78%，同时访问更多文件并出现 exploration drift；对 Causality for Code Review 的关键启发是用 ground-truth-preserving context intervention 与 trajectory mediator 分析 repository context 何时、为何伤害审查。

### 2026-09-16

- **A Causal Learning Framework for Enhancing Robustness of Source Code Models**
  - 简称：[CausalCode](https://38-76-161-31.sslip.io/daily-learning/?paper=260916-JunyaoYe-CausalCode)
  - Tags：`2025` `FSE` `因果学习` `代码智能` `模型鲁棒性` `语义保持干预` `对抗鲁棒性` `表示学习` `代码模型`
  - 作者：Junyao Ye; Zhen Li; Xi Tang; Deqing Zou; Shouhuai Xu; Weizhong Qiang; Hai Jin
  - Venue / 年份：FSE 2025 / PACMSE 2, Article FSE117
  - DOI / 原文：[10.1145/3729387](https://doi.org/10.1145/3729387); [Code](https://github.com/CGCL-codes/CausalCode)
  - 主题：因果学习、代码模型鲁棒性、语义保持干预、伪相关、表示不变性
  - 一句话价值：CausalCode 通过梯度引导的语义保持 intervention 与 paired representation regularization 显著降低所测攻击族的 ASR；最值得借鉴的是 ground-truth-preserving intervention 设计，但其 RQ2 更直接证明 intervention invariance，而非已识别真正程序因果语义。

### 2026-09-15

- **AI-Assisted Code Review as a Scaffold for Code Quality and Self-Regulated Learning: An Experience Report**
  - 简称：[AI-Assisted Code Review](https://38-76-161-31.sslip.io/daily-learning/?paper=260915-EduardoOliveira-AIAssistedCodeReview)
  - Tags：`2026` `ICSE-SEET` `代码评审` `LLM代码评审` `软件工程教育` `真实工作流` `行为轨迹` `开发者行为` `经验报告`
  - 作者：Eduardo Oliveira; Michael Fu; Patanamon Thongtanunam; Sonsoles López-Pernas; Mohammed Saqr
  - Venue / 年份：ICSE-SEET 2026
  - DOI / 原文：[10.1145/3786580.3786956](https://doi.org/10.1145/3786580.3786956); [arXiv:2604.23251](https://arxiv.org/abs/2604.23251)
  - 主题：AI代码审查、真实PR工作流、行为轨迹、Self-Regulated Learning、Outcome构念
  - 一句话价值：两个真实capstone cohort中，成功AI review后约三分之一PR出现后续commit；最值得借鉴的是trace-based Action Rate，但该指标只能证明反馈后的活动关联，不能证明评论被采纳或质量提升。对Causality for Code Review的启发是建模 Context→Comment/Evidence→Developer Action→Quality 的机制链，并处理AI调用的自选择。

### 2026-09-14

- **Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement**
  - 简称：[Reliable Code Reviewers](https://38-76-161-31.sslip.io/daily-learning/?paper=260914-HaolinJin-ReliableCodeReviewers)
  - Tags：`2026` `arXiv/Preprint` `代码评审` `LLM代码评审` `Prompt Engineering` `过度纠正` `需求一致性` `误报` `可执行验证`
  - 作者：Haolin Jin; Huaming Chen
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2603.00539](https://arxiv.org/abs/2603.00539); [Code](https://github.com/HollinJ3177/Are-LLMs-Reliable-Code-Reviewers-Systematic-Overcorrection-in-Requirement-Conformance-Judgement)
  - 主题：LLM代码审查、Requirement Conformance、Prompt Framing、False Rejection、可执行验证
  - 一句话价值：系统操纵 Judge / Explain / Fix 三类审查指令，发现更强的解释与修复要求会显著提高对正确代码的误拒绝率；Fix-guided execution 可降低 overcorrection。对 Causality for Code Review 的关键启发是把 Prompt 作为正式 Treatment，并检验 Context × Prompt 的交互及 Evidence Grounding 机制。

### 2026-09-13

- **SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering?**  - 简称：[SWE-Skills-Bench](https://38-76-161-31.sslip.io/daily-learning/?paper=260913-TingxuHan-SWESkillsBench)
  - Tags：`2026` `arXiv/Preprint` `Coding Agent` `Agent Skill` `上下文工程` `软件工程Agent` `异质效应` `Token成本` `Benchmark`
  - 作者：Tingxu Han; Yi Zhang; Wei Song; Chunrong Fang; Zhenyu Chen; Youcheng Sun; Lijie Hu
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2603.15401](https://arxiv.org/abs/2603.15401)
  - 主题：Agent Skill、Context Treatment、配对实验、上下文干扰、异质效应
  - 一句话价值：49 个 SWE Skill 在约 565 个真实任务上的 With/Without-Skill 配对实验显示平均 Pass Rate 仅提升约 1.2%，39/49 个 Skill 无提升且平均 Token 成本增加约 10.5%，部分不兼容 Skill 还会让性能下降；对 Causality for Code Review 的关键启发是把 context 的 marginal utility、compatibility 和 heterogeneous treatment effect 作为正式研究对象。

### 2026-09-12

- **What Does an Agentic Software Engineering Benchmark Measure? Profiling Task Demands and Agent Behaviour Beyond What Category Labels Reveal**
  - 简称：[SNC](https://38-76-161-31.sslip.io/daily-learning/?paper=260912-RadinShayanfar-AgenticBenchmarkMeasure)
  - Tags：`2026` `arXiv/Preprint` `软件工程Agent` `Benchmark` `任务难度` `Agent行为` `行为轨迹` `构念效度` `异质效应`
  - 作者：Radin Shayanfar; Keheliya Gallaba; Ahmed E. Hassan
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2609.01271](https://arxiv.org/abs/2609.01271); [Code](https://github.com/radinshayanfar/task_snc)
  - 主题：Agentic SE benchmark、任务需求、SNC、Agent行为、构念效度、异质效应  - 一句话价值：用 Spread–Novelty–Centrality 刻画 5 个 benchmark 的 2,487 个任务，并分析 14,922 条 Agent trajectory，表明 nominal category 远不足以代表真实 task demand；对 Causality for Code Review 的关键启发是把结构需求作为 effect modifier、trajectory 作为 mediator，而不是把 task difficulty 当成单一标量。

### 2026-09-11

- **On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation**
  - 简称：[Context Compression](https://38-76-161-31.sslip.io/daily-learning/?paper=260911-JiaFeng-ContextCompression)
  - Tags：`2026` `arXiv/Preprint` `上下文工程` `仓库级任务` `上下文压缩` `长上下文` `代码生成` `噪声` `表示学习`
  - 作者：Jia Feng; Zhanyue Qin; Cuiyun Gao; Ruiqi Wang; Chaozheng Wang; Yingwei Ma; Xiaoyuan Xie
  - Venue / 年份：arXiv cs.SE / 2026
  - DOI / 原文：[arXiv:2604.13725](https://arxiv.org/abs/2604.13725)
  - 主题：仓库级上下文、上下文压缩、噪声、代码生成、异质效应  - 一句话价值：系统比较 Text-to-Text、Text-to-Vector 与 Text-to-Image 压缩，发现部分 T2V 设置超过 Full Context，而部分文本压缩甚至低于 No Context；它为“额外仓库上下文可能主动伤害模型”提供重要现象证据，但尚未单独识别 denoising 的因果机制。

### 2026-09-10

- **Causal Software Engineering: A Vision and Roadmap**
  - 简称：[Causal SE](https://38-76-161-31.sslip.io/daily-learning/?paper=260910-RobertoPietrantuono-CausalSoftwareEngineering)
  - Tags：`2026` `FSE` `因果软件工程` `因果推断` `反事实` `干预` `因果可观测性` `研究方法论`
  - 作者：Roberto Pietrantuono; Luca Giamattei; Stefano Russo; Julien Siebert; Neil Walkinshaw
  - Venue / 年份：FSE 2026 Ideas, Visions and Reflections
  - DOI / 原文：[10.1145/3803437.3805585](https://doi.org/10.1145/3803437.3805585); [arXiv:2605.02454](https://arxiv.org/abs/2605.02454)
  - 主题：因果软件工程、干预、反事实、因果可观测性、可信评测
  - 一句话价值：把软件工程中的代码、配置、测试、部署和修复统一视为干预，提出 Causal Design Spec、Intervention Log、Living Causal Model 与四条路线；其价值是给 Causality for Code Review 提供方法论总框架，而非已经验证的因果效果。

### 2026-09-08

- **Explaining Explanations: An Empirical Study of Explanations in Code Reviews**
  - 简称：[Explaining Explanations](https://38-76-161-31.sslip.io/daily-learning/?paper=260908-RatnadiraWidyasari-ExplainingExplanations)
  - Tags：`2025` `TOSEM` `代码评审` `审查解释` `LLM代码评审` `实证研究` `开发者沟通` `可解释性`
  - 作者：Ratnadira Widyasari; Ting Zhang; Abir Bouraffa; Walid Maalej; David Lo
  - Venue / 年份：TOSEM 34(6), Article 177 / 2025
  - DOI / 原文：[10.1145/3708518](https://doi.org/10.1145/3708518)
  - 主题：代码审查解释、审查沟通、LLM生成、经验差异、因果实验设计
  - 一句话价值：从793条“有用”首轮行内评论中归纳七类解释，并验证GPT-3.5可按指定类型改写；它建立了可操作的解释分类，但尚未证明解释会改善采纳、效率或代码质量，适合作为后续随机干预的Treatment设计基础。

### 2026-09-07

- **What Makes a Code Review Useful to OpenDev Developers? An Empirical Investigation**
  - 简称：[Useful Code Review](https://38-76-161-31.sslip.io/daily-learning/?paper=260907-AsifTurzo-UsefulCodeReview)
  - Tags：`2024` `EMSE` `FSE Journal First` `代码评审` `审查有用性` `Outcome构念` `实证研究` `开发者行为` `观察性研究`
  - 作者：Asif Kamal Turzo; Amiangshu Bosu
  - Venue / 年份：Empirical Software Engineering 29(1):6 / 2024
  - DOI / 原文：FSE 2024 Journal First；[10.1007/s10664-023-10411-x](https://doi.org/10.1007/s10664-023-10411-x); [arXiv:2302.11686](https://arxiv.org/abs/2302.11686)
  - 主题：代码审查有用性、混合方法、调查、回归、Outcome构念
  - 一句话价值：把“作者是否采纳/承认”与评论类别评分组合成有用性指标，并发现若干上下文关联；它最重要的价值是暴露了代码审查Outcome构造、后处理变量与观察性回归被误读为因果效应的风险。

### 2026-09-06

- **Antares: Foundation Models for Agentic Vulnerability Localization**
  - 简称：[Antares / VLoc Bench](https://38-76-161-31.sslip.io/daily-learning/?paper=260906-SupritiVijay-AntaresVLocBench)
  - Tags：`2026` `Technical Report` `漏洞定位` `Coding Agent` `仓库级搜索` `上下文工程` `VLoc Bench` `任务难度` `Signal Dilution` `Benchmark`  - 作者：Supriti Vijay; Aman Priyanshu; Didier Chapoteau; Arthur Goldblatt; Jianliang He; Kimia Majd; Fraser Burch; Baturay Saglam; Takahiro Matsumoto; Zhuoran Yang; Amin Karbasi
  - Venue / 年份：Cisco Foundation AI Technical Report / 2026
  - DOI / 原文：[VLoc Bench Technical Report](https://cisco-foundation-ai.github.io/vulnerability-localization-benchmark/technical-report.pdf)
  - 主题：漏洞定位、Agent、仓库级搜索、VLoc Bench、任务难度、signal dilution
  - 一句话价值：VLoc Bench 将漏洞定位建模为固定工具预算下的仓库探索任务；结果显示 repository structure、size 与多文件证据比 CVSS severity 更能解释难度，并将大仓库失败归因于 signal dilution。对 Causality for Code Review 的关键启发是把 relevant-evidence density、search strategy 与 repository structure 建模为机制和异质效应变量，而不是只证明 call graph 有用。

### 2026-09-04

- **SeRe: A Security-Related Code Review Dataset Aligned with Real-World Review Activities**
  - 简称：[SeRe](https://38-76-161-31.sslip.io/daily-learning/?paper=260904-ZixiaoZhao-SeRe)
  - Tags：`2026` `ICSE` `代码评审` `安全代码评审` `软件安全` `数据集` `主动学习` `选择偏差` `Benchmark`
  - 作者：Zixiao Zhao; Yanjie Jiang; Hui Liu; Kui Liu; Lu Zhang
  - Venue / 年份：ICSE 2026
  - DOI / 原文：[10.1145/3744916.3764557](https://doi.org/10.1145/3744916.3764557); [Replication Package](https://github.com/caagc/Sere)
  - 主题：安全代码审查、主动学习、数据集构建、LLM评测、选择偏差
  - 一句话价值：以主动学习和五模型投票从373,824条审查记录中提取6,732条安全审查；高精度筛选适合构建干净语料，但42.38%召回率和条件化抽样意味着它更像“高置信安全审查子集”，不能代表安全问题的完整真实分布。

### 2026-09-03

- **From Static to Dynamic: Benchmarking Real-World Code Review with MCR-Bench**
  - 简称：[MCR-Bench](https://38-76-161-31.sslip.io/daily-learning/?paper=260903-DewuZheng-MCRBench)
  - Tags：`2026` `ISSTA` `代码评审` `多轮代码评审` `LLM代码评审` `状态追踪` `长程记忆` `Benchmark`
  - 作者：Dewu Zheng; Yanlin Wang; Xiwen Wang; Kefeng Duan; Hongyu Zhang; Xilin Liu; Yuchi Ma; Zibin Zheng
  - Venue / 年份：ISSTA 2026 / Proceedings of the ACM on Software Engineering 3
  - DOI / 原文：[10.1145/3832219](https://doi.org/10.1145/3832219); [arXiv:2608.27442](https://arxiv.org/abs/2608.27442)
  - 主题：多轮代码审查、动态缺陷状态、LLM评测、长程记忆、benchmark
  - 一句话价值：2,269个真实多轮PR任务把评价从单轮缺陷命中扩展到New/Open/Resolved/Reopened状态追踪；模型随轮次的表面退化很有启发，但轮次与任务构成、样本量和难度共同变化，不能直接解释成长程记忆的因果效应。

### 2026-09-02

- **Can We Benchmark Code Review Studies? A Systematic Mapping Study of Methodology, Dataset, and Metric**
  - 简称：[Code Review Benchmarking](https://38-76-161-31.sslip.io/daily-learning/?paper=260902-DongWang-CodeReviewBenchmarking)  - Tags：`2021` `JSS` `代码评审` `系统映射研究` `Benchmark` `数据集` `评测指标` `构念效度` `实证软件工程`
  - 作者：Dong Wang; Yuki Ueda; Raula Gaikovina Kula; Takashi Ishio; Kenichi Matsumoto
  - Venue / 年份：Journal of Systems and Software 180 / 2021
  - DOI / 原文：[10.1016/j.jss.2021.111009](https://doi.org/10.1016/j.jss.2021.111009)
  - 主题：代码审查、系统映射、benchmark、数据复现、指标构念
  - 一句话价值：对2011–2019年112篇高影响代码审查研究的映射发现，仅42/84篇定量或混合研究公开可复用数据，31篇定量研究使用了457个指标；指标存在局部共识，但数据、任务与构念尚不足以形成统一benchmark。

### 2026-09-01

- **Quality Gatekeepers: Investigating the Effects of Code Review Bots on Pull Request Activities**
  - 简称：[Quality Gatekeepers](https://38-76-161-31.sslip.io/daily-learning/?paper=260901-MairieliWessel-QualityGatekeepers)
  - Tags：`2022` `EMSE` `代码评审` `Code Review Bot` `Pull Request` `开发者行为` `中断时间序列` `因果推断` `实证研究`
  - 作者：Mairieli Wessel; Alexander Serebrenik; Igor Wiese; Igor Steinmacher; Marco A. Gerosa
  - Venue / 年份：Empirical Software Engineering 27:108 / 2022
  - DOI / 原文：[10.1007/s10664-022-10130-9](https://doi.org/10.1007/s10664-022-10130-9)
  - 主题：代码审查机器人、工具采用、分段回归、混合方法、PR活动
  - 一句话价值：1,194个GitHub项目的采用前后分析显示覆盖率机器人上线后合并PR增多、未合并PR减少且合并PR人工评论下降；但采用时点并非随机，结果仍依赖无同期干预等识别假设，访谈提供的是机制解释而非中介效应证明。

## 待精读论文

- 暂无已指定待精读论文