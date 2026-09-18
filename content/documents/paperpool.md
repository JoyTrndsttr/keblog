# Paper Pool

> **维护约定**
> - 去重优先级：DOI > arXiv ID > 规范化标题；已精读论文永久不重复推荐，除非用户明确要求重读。
> - 新论文只有在来源可靠、与当前研究方向相关且值得后续精读时才进入“待精读论文”。
> - 完成精读后，从“待精读论文”移入对应日期的“已精读论文”，不保留重复活跃条目。
> - 每次写入前重新读取最新版，保留人工修改；待核验信息明确标记，不得猜测。
> - 已精读按日期三级标题组织；每篇论文用一个一级无序列表项，论文内部字段使用缩进的二级无序列表，同一天可有多篇。
> - 每篇论文固定保留：简称、作者、Venue / 年份、DOI / 原文、主题、一句话价值；不要把这些字段压缩到同一行。

## 已精读论文

### 2026-09-18

- **RepoReasoner: Evaluating Repository-Level Code Reasoning Ability of Long-Context Language Models**
  - 简称：RepoReasoner
  - 作者：Yanlin Wang; Suiquan Wang; Yanli Wang; Bowen Zhang; Daya Guo; Jiachi Chen; Zibin Zheng
  - Venue / 年份：FSE 2026 / Proc. ACM Softw. Eng. 3, FSE124
  - DOI / 原文：[DOI:10.1145/3808131](https://doi.org/10.1145/3808131); [arXiv:2607.25996](https://arxiv.org/abs/2607.25996); [Code](https://github.com/DeepSoftwareAnalytics/RepoReasoner)；对当前研究最关键的是把“relevant evidence 是否到场”和“模型能否利用 evidence”分开，并把 signal/noise、dependency depth 改造成可控 context intervention。
  - 主题：Repository-Level Reasoning、Long Context、Call Chain、Context Noise、Oracle Context
  - 一句话价值：用动态执行 trace 构造 Oracle context 与 call-chain ground truth，并比较 10k/30k retrieval context，显示完美相关文件并不能消除跨文件推理失败，更多 context 对不同模型还呈正负异质效应

- **Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?**
  - 简称：AGENTS.md
  - 作者：Thibaud Gloaguen; Niels Mündler; Mark Müller; Veselin Raychev; Martin Vechev
  - Venue / 年份：MemAgents @ ICLR 2026 / arXiv 2026
  - DOI / 原文：[arXiv:2602.11988](https://arxiv.org/abs/2602.11988)；对 Causality for Code Review 的关键启发是把 Context 作为 Treatment、trajectory 作为 Mediator，并区分“模型会遵循上下文”与“上下文真正改善 Outcome”。
  - 主题：Coding Agent、Repository Context、AGENTS.md、CTXbench、行为轨迹、成本
  - 一句话价值：在 SWE-bench Lite 与新建 CTXbench 上操纵 None/LLM-generated/developer context file，发现 context file 不显著提高成功率，却稳定增加探索步骤与 20%+ 推理成本

### 2026-09-17

- **RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations**
  - 简称：RepoMirage
  - 作者：Hanyu Li; Yichi Zhang; Speed Zhu; Hang Su; Jun Zhu; Yinpeng Dong
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2605.26177](https://arxiv.org/abs/2605.26177)；对 Causality for Code Review 的关键启发是用 ground-truth-preserving context intervention 与 trajectory mediator 分析 repository context 何时、为何伤害审查。
  - 主题：Repository Context、Coding Agent、语义保持扰动、探索漂移、构念效度
  - 一句话价值：通过保持 issue/功能/测试不变、只改变仓库证据暴露方式的 perturbation，RepoMirage 发现 8 个模型平均 resolved rate 从 66.80% 降到 49.78%，同时访问更多文件并出现 exploration drift

### 2026-09-16

- **A Causal Learning Framework for Enhancing Robustness of Source Code Models**
  - 简称：CausalCode
  - 作者：Junyao Ye; Zhen Li; Xi Tang; Deqing Zou; Shouhuai Xu; Weizhong Qiang; Hai Jin
  - Venue / 年份：FSE 2025 / PACMSE 2, Article FSE117
  - DOI / 原文：[10.1145/3729387](https://doi.org/10.1145/3729387); [Code](https://github.com/CGCL-codes/CausalCode)；最值得借鉴的是 ground-truth-preserving intervention 设计，但其 RQ2 更直接证明 intervention invariance，而非已识别真正程序因果语义。
  - 主题：因果学习、代码模型鲁棒性、语义保持干预、伪相关、表示不变性
  - 一句话价值：CausalCode 通过梯度引导的语义保持 intervention 与 paired representation regularization 显著降低所测攻击族的 ASR

### 2026-09-15

- **AI-Assisted Code Review as a Scaffold for Code Quality and Self-Regulated Learning: An Experience Report**
  - 简称：AI-Assisted Code Review
  - 作者：Eduardo Oliveira; Michael Fu; Patanamon Thongtanunam; Sonsoles López-Pernas; Mohammed Saqr
  - Venue / 年份：ICSE-SEET 2026
  - DOI / 原文：[10.1145/3786580.3786956](https://doi.org/10.1145/3786580.3786956); [arXiv:2604.23251](https://arxiv.org/abs/2604.23251)；最值得借鉴的是trace-based Action Rate，但该指标只能证明反馈后的活动关联，不能证明评论被采纳或质量提升。对Causality for Code Review的启发是建模 Context→Comment/Evidence→Developer Action→Quality 的机制链，并处理AI调用的自选择。
  - 主题：AI代码审查、真实PR工作流、行为轨迹、Self-Regulated Learning、Outcome构念
  - 一句话价值：两个真实capstone cohort中，成功AI review后约三分之一PR出现后续commit

### 2026-09-14

- **Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement**
  - 简称：Reliable Code Reviewers
  - 作者：Haolin Jin; Huaming Chen
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2603.00539](https://arxiv.org/abs/2603.00539); [Code](https://github.com/HollinJ3177/Are-LLMs-Reliable-Code-Reviewers-Systematic-Overcorrection-in-Requirement-Conformance-Judgement)；Fix-guided execution 可降低 overcorrection。对 Causality for Code Review 的关键启发是把 Prompt 作为正式 Treatment，并检验 Context × Prompt 的交互及 Evidence Grounding 机制。
  - 主题：LLM代码审查、Requirement Conformance、Prompt Framing、False Rejection、可执行验证
  - 一句话价值：系统操纵 Judge / Explain / Fix 三类审查指令，发现更强的解释与修复要求会显著提高对正确代码的误拒绝率

### 2026-09-13

- **SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering?**
  - 简称：SWE-Skills-Bench
  - 作者：Tingxu Han; Yi Zhang; Wei Song; Chunrong Fang; Zhenyu Chen; Youcheng Sun; Lijie Hu
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2603.15401](https://arxiv.org/abs/2603.15401)；对 Causality for Code Review 的关键启发是把 context 的 marginal utility、compatibility 和 heterogeneous treatment effect 作为正式研究对象。
  - 主题：Agent Skill、Context Treatment、配对实验、上下文干扰、异质效应
  - 一句话价值：49 个 SWE Skill 在约 565 个真实任务上的 With/Without-Skill 配对实验显示平均 Pass Rate 仅提升约 1.2%，39/49 个 Skill 无提升且平均 Token 成本增加约 10.5%，部分不兼容 Skill 还会让性能下降

### 2026-09-12

- **What Does an Agentic Software Engineering Benchmark Measure? Profiling Task Demands and Agent Behaviour Beyond What Category Labels Reveal**
  - 简称：SNC / Agentic Benchmark Measure
  - 作者：Radin Shayanfar; Keheliya Gallaba; Ahmed E. Hassan
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2609.01271](https://arxiv.org/abs/2609.01271); [Code](https://github.com/radinshayanfar/task_snc)；对 Causality for Code Review 的关键启发是把结构需求作为 effect modifier、trajectory 作为 mediator，而不是把 task difficulty 当成单一标量。
  - 主题：Agentic SE benchmark、任务需求、SNC、Agent行为、构念效度、异质效应
  - 一句话价值：用 Spread–Novelty–Centrality 刻画 5 个 benchmark 的 2,487 个任务，并分析 14,922 条 Agent trajectory，表明 nominal category 远不足以代表真实 task demand

### 2026-09-11

- **On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation**
  - 简称：Context Compression
  - 作者：Jia Feng; Zhanyue Qin; Cuiyun Gao; Ruiqi Wang; Chaozheng Wang; Yingwei Ma; Xiaoyuan Xie
  - Venue / 年份：arXiv cs.SE / 2026
  - DOI / 原文：[arXiv:2604.13725](https://arxiv.org/abs/2604.13725)；它为“额外仓库上下文可能主动伤害模型”提供重要现象证据，但尚未单独识别 denoising 的因果机制。
  - 主题：仓库级上下文、上下文压缩、噪声、代码生成、异质效应
  - 一句话价值：系统比较 Text-to-Text、Text-to-Vector 与 Text-to-Image 压缩，发现部分 T2V 设置超过 Full Context，而部分文本压缩甚至低于 No Context

### 2026-09-10

- **Causal Software Engineering: A Vision and Roadmap**
  - 简称：Causal SE
  - 作者：Roberto Pietrantuono; Luca Giamattei; Stefano Russo; Julien Siebert; Neil Walkinshaw
  - Venue / 年份：FSE 2026 Ideas, Visions and Reflections
  - DOI / 原文：[10.1145/3803437.3805585](https://doi.org/10.1145/3803437.3805585); [arXiv:2605.02454](https://arxiv.org/abs/2605.02454)；其价值是给 Causality for Code Review 提供方法论总框架，而非已经验证的因果效果。
  - 主题：因果软件工程、干预、反事实、因果可观测性、可信评测
  - 一句话价值：把软件工程中的代码、配置、测试、部署和修复统一视为干预，提出 Causal Design Spec、Intervention Log、Living Causal Model 与四条路线

### 2026-09-08

- **Explaining Explanations: An Empirical Study of Explanations in Code Reviews**
  - 简称：Explaining Explanations
  - 作者：Ratnadira Widyasari; Ting Zhang; Abir Bouraffa; Walid Maalej; David Lo
  - Venue / 年份：TOSEM 34(6), Article 177 / 2025
  - DOI / 原文：[10.1145/3708518](https://doi.org/10.1145/3708518)；它建立了可操作的解释分类，但尚未证明解释会改善采纳、效率或代码质量，适合作为后续随机干预的Treatment设计基础。
  - 主题：代码审查解释、审查沟通、LLM生成、经验差异、因果实验设计
  - 一句话价值：从793条“有用”首轮行内评论中归纳七类解释，并验证GPT-3.5可按指定类型改写

### 2026-09-07

- **What Makes a Code Review Useful to OpenDev Developers? An Empirical Investigation**
  - 简称：Useful Code Review
  - 作者：Asif Kamal Turzo; Amiangshu Bosu
  - Venue / 年份：Empirical Software Engineering 29(1):6 / 2024
  - DOI / 原文：FSE 2024 Journal First；[10.1007/s10664-023-10411-x](https://doi.org/10.1007/s10664-023-10411-x); [arXiv:2302.11686](https://arxiv.org/abs/2302.11686)；它最重要的价值是暴露了代码审查Outcome构造、后处理变量与观察性回归被误读为因果效应的风险。
  - 主题：代码审查有用性、混合方法、调查、回归、Outcome构念
  - 一句话价值：把“作者是否采纳/承认”与评论类别评分组合成有用性指标，并发现若干上下文关联

### 2026-09-06

- **Antares: Foundation Models for Agentic Vulnerability Localization**
  - 简称：Antares / VLoc Bench
  - 作者：Supriti Vijay; Aman Priyanshu; Didier Chapoteau; Arthur Goldblatt; Jianliang He; Kimia Majd; Fraser Burch; Baturay Saglam; Takahiro Matsumoto; Zhuoran Yang; Amin Karbasi
  - Venue / 年份：Cisco Foundation AI Technical Report / 2026
  - DOI / 原文：[VLoc Bench Technical Report](https://cisco-foundation-ai.github.io/vulnerability-localization-benchmark/technical-report.pdf)；结果显示 repository structure、size 与多文件证据比 CVSS severity 更能解释难度，并将大仓库失败归因于 signal dilution。对 Causality for Code Review 的关键启发是把 relevant-evidence density、search strategy 与 repository structure 建模为机制和异质效应变量，而不是只证明 call graph 有用。
  - 主题：漏洞定位、Agent、仓库级搜索、VLoc Bench、任务难度、signal dilution
  - 一句话价值：VLoc Bench 将漏洞定位建模为固定工具预算下的仓库探索任务

### 2026-09-04

- **SeRe: A Security-Related Code Review Dataset Aligned with Real-World Review Activities**
  - 简称：SeRe
  - 作者：Zixiao Zhao; Yanjie Jiang; Hui Liu; Kui Liu; Lu Zhang
  - Venue / 年份：ICSE 2026
  - DOI / 原文：[10.1145/3744916.3764557](https://doi.org/10.1145/3744916.3764557); [Replication Package](https://github.com/caagc/Sere)；高精度筛选适合构建干净语料，但42.38%召回率和条件化抽样意味着它更像“高置信安全审查子集”，不能代表安全问题的完整真实分布。
  - 主题：安全代码审查、主动学习、数据集构建、LLM评测、选择偏差
  - 一句话价值：以主动学习和五模型投票从373,824条审查记录中提取6,732条安全审查

### 2026-09-03

- **From Static to Dynamic: Benchmarking Real-World Code Review with MCR-Bench**
  - 简称：MCR-Bench
  - 作者：Dewu Zheng; Yanlin Wang; Xiwen Wang; Kefeng Duan; Hongyu Zhang; Xilin Liu; Yuchi Ma; Zibin Zheng
  - Venue / 年份：ISSTA 2026 / Proceedings of the ACM on Software Engineering 3
  - DOI / 原文：[10.1145/3832219](https://doi.org/10.1145/3832219); [arXiv:2608.27442](https://arxiv.org/abs/2608.27442)；模型随轮次的表面退化很有启发，但轮次与任务构成、样本量和难度共同变化，不能直接解释成长程记忆的因果效应。
  - 主题：多轮代码审查、动态缺陷状态、LLM评测、长程记忆、benchmark
  - 一句话价值：2,269个真实多轮PR任务把评价从单轮缺陷命中扩展到New/Open/Resolved/Reopened状态追踪

### 2026-09-02

- **Can We Benchmark Code Review Studies? A Systematic Mapping Study of Methodology, Dataset, and Metric**
  - 简称：Code Review Benchmarking
  - 作者：Dong Wang; Yuki Ueda; Raula Gaikovina Kula; Takashi Ishio; Kenichi Matsumoto
  - Venue / 年份：Journal of Systems and Software 180 / 2021
  - DOI / 原文：[10.1016/j.jss.2021.111009](https://doi.org/10.1016/j.jss.2021.111009)；指标存在局部共识，但数据、任务与构念尚不足以形成统一benchmark。
  - 主题：代码审查、系统映射、benchmark、数据复现、指标构念
  - 一句话价值：对2011–2019年112篇高影响代码审查研究的映射发现，仅42/84篇定量或混合研究公开可复用数据，31篇定量研究使用了457个指标

### 2026-09-01

- **Quality Gatekeepers: Investigating the Effects of Code Review Bots on Pull Request Activities**
  - 简称：Quality Gatekeepers
  - 作者：Mairieli Wessel; Alexander Serebrenik; Igor Wiese; Igor Steinmacher; Marco A. Gerosa
  - Venue / 年份：Empirical Software Engineering 27:108 / 2022
  - DOI / 原文：[10.1007/s10664-022-10130-9](https://doi.org/10.1007/s10664-022-10130-9)；但采用时点并非随机，结果仍依赖无同期干预等识别假设，访谈提供的是机制解释而非中介效应证明。
  - 主题：代码审查机器人、工具采用、分段回归、混合方法、PR活动
  - 一句话价值：1,194个GitHub项目的采用前后分析显示覆盖率机器人上线后合并PR增多、未合并PR减少且合并PR人工评论下降

### 2026-08-31

- **RovoDev Code Reviewer: A Large-Scale Online Evaluation of LLM-based Code Review Automation at Atlassian**
  - 简称：RovoDev Code Reviewer
  - 作者：Kla Tantithamthavorn; Yaotian Zou; Andy Wong; Michael Gupta; Zhe Wang; Mike Buller; Ryan Jiang; Matthew Watson; Minwoo Jeong; Kun Chen; Ming Wu
  - Venue / 年份：ICSE-SEIP 2026
  - DOI / 原文：[10.1145/3786583.3786851](https://doi.org/10.1145/3786583.3786851)
  - 主题：工业代码审查、在线部署、LLM评论、工作流影响、因果识别
  - 一句话价值：逾1900个仓库的一年部署显示38.70%的机器评论随后对应代码修改，但PR周期和人工评论下降来自观察性队列及中断时间序列，能支持真实关联与可用性，尚不能独立识别RovoDev的纯因果效应。

### 2026-08-30

- **Code Review Comprehension: Reviewing Strategies Seen Through Code Comprehension Theories**
  - 简称：Code Review Comprehension
  - 作者：Pavlína Wurzel Gonçalves; Pooja Rani; Margaret-Anne Storey; Diomidis Spinellis; Alberto Bacchelli
  - Venue / 年份：ICPC 2025
  - DOI / 原文：[10.1109/ICPC66645.2025.00068](https://doi.org/10.1109/ICPC66645.2025.00068)；该模型适合提出机制假设，但不能直接证明哪种策略提高审查质量。
  - 主题：代码审查、代码理解、认知模型、审查策略、质性研究
  - 一句话价值：真实观察显示专家审查并非简单线性读diff，而是先建立上下文，再按复杂度机会式组合线性阅读、难度优先、分块、测试与讨论

### 2026-08-29

- **The Effect of Complexity and Provenance on Code Review Decisions: Evidence from a Controlled Experiment**
  - 简称：Complexity & Provenance
  - 作者：Neha Singh; Francesco Sovrano; Vincent J. Hellendoorn; Alberto Bacchelli
  - Venue / 年份：FSE 2026 / Proceedings of the ACM on Software Engineering 3
  - DOI / 原文：[10.1145/3808165](https://doi.org/10.1145/3808165)；但每个复杂度只有一个不同代码片段且缺陷类型不同，不能把差异纯归因于复杂度。
  - 主题：代码审查、受控实验、复杂度、AI 来源标签、过度服从
  - 一句话价值：2×2×2 随机实验发现高复杂任务包与接受错误修订相关，而 AI/人类标签无主效应

### 2026-08-28

- **EntailLLM: Verifying LLM-Generated Vulnerability Discovery Paths with Domain Knowledge via Logic Programming**
  - 简称：EntailLLM
  - 作者：Kaustuv Mukherji; Jaikrishna Manojkumar Patil; Colton Payne; Paulo Shakarian; Dana Warmsley; Nigel Stepp; Evelyn Kim
  - Venue / 年份：arXiv 预印本 / 2026
  - DOI / 原文：[arXiv:2608.01763](https://arxiv.org/abs/2608.01763)；但Outcome是规则一致性而非漏洞真实性，且同一领域知识同时影响生成与验证，高一致率不等于独立验证。
  - 主题：漏洞路径、调用图、领域知识、逻辑蕴涵、LLM验证
  - 一句话价值：将LLM路径实例化到真实调用图，再用CWE知识做可解释逻辑蕴涵过滤

### 2026-08-27

- **DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection**
  - 简称：DREA
  - 作者：Mingyang Sun; Guozhu Meng
  - Venue / 年份：Internetware 2026 / arXiv 2026
  - DOI / 原文：[arXiv:2607.13439](https://arxiv.org/abs/2607.13439)；但角色解耦与模型差异、信息压缩和预算同时变化，尚不能单独识别解耦本身的因果效应。
  - 主题：仓库级漏洞检测、推理探索解耦、RepoPairBench、Lucky Hits、成本
  - 一句话价值：结构化、按假设驱动的仓库探索比函数或整文件上下文更可靠，且可把93%以上token卸载给本地Explorer

### 2026-08-26

- **AACR-Bench: Evaluating Automatic Code Review with Holistic Repository-Level Context**
  - 简称：AACR-Bench
  - 作者：Lei Zhang; Yongda Yu; Minghui Yu; Xinxin Guo; Zhengqi Zhuang; Guoping Rong; Dong Shao; Haifeng Shen; Hongyu Kuang; Zhengfeng Li; Boge Wang; Guoan Zhang; Bangyu Xiang; Xiaobin Xu
  - Venue / 年份：arXiv 预印本 / 2026
  - DOI / 原文：[arXiv:2601.19494](https://arxiv.org/abs/2601.19494)
  - 主题：自动代码审查评测、仓库级上下文、多语言基准、专家核验、语义评价
  - 一句话价值：用多模型发现和双人专家核验补全PR缺陷并标注上下文层级，但模型生成型ground truth、选择性PR抽样与非对称检索预算使评价更全面却不天然中立。

### 2026-08-25

- **OpenCodeReview: Determinism over Non-Determinism for Cost-Effective Agent-Based Code Review**
  - 简称：OpenCodeReview
  - 作者：Zhengfeng Li; Lei Zhang; Xianwei Wu; Zhengqi Zhuang; Yingjie Xu; Boge Wang; Shaofei Zhu; Chuan Wang; Peng Zhao; Xinyu Zheng; Guoping Rong
  - Venue / 年份：arXiv 预印本 / 2026
  - DOI / 原文：[arXiv:2608.09290](https://arxiv.org/abs/2608.09290)
  - 主题：Agent 代码审查、仓库上下文、确定性工程、反思过滤、成本
  - 一句话价值：确定性规则分派、受限仓库探索与非对称信息反思在系统级对比中改善精度和成本，但尚缺组件消融与跨运行稳定性验证。

### 2026-08-17

- **Shaky Structures: The Wobbly World of Causal Graphs in Software Analytics**
  - 简称：Shaky Structures
  - 作者：Jeremy Hulse; Nasir U. Eisty; Tim Menzies
  - Venue / 年份：EMSE 30(5), 2025 / ICSE 2026 Journal-first
  - DOI / 原文：[10.1007/s10664-025-10690-6](https://doi.org/10.1007/s10664-025-10690-6)
  - 主题：因果发现、结构稳定性、软件分析、敏感性分析
  - 一句话价值：四类因果发现器在23个软工数据集上对版本、项目、参数和抽样扰动高度敏感，提示自动发现的单一DAG不能直接支撑稳定因果结论。

### 2026-08-16

- **Improving Code Reviewer Recommendation: Accuracy, Latency, Workload, and Bystanders**
  - 简称：Reviewer Recommendation
  - 作者：Peter C. Rigby; Seth Rogers; Sadruddin Saleem; Parth Suresh; Daniel Suskin; Patrick Riggs; Chandra Shekhar Maddila; Nachiappan Nagappan; Audris Mockus
  - Venue / 年份：TOSEM 35(1), 2026 / ICSE 2026 Journal-first
  - DOI / 原文：[10.1145/3736405](https://doi.org/10.1145/3736405)
  - 主题：代码审查、审查者推荐、随机对照实验、工作负载、旁观者效应
  - 一句话价值：三项生产环境 A/B 实验表明离线准确率不足以代表真实干预效果，显式责任分配可缩短审查周期。

### 2026-08-15

- **Rethinking Software Empirical Studies with Structural Causal Models**
  - 简称：SCM for SE
  - 作者：Daniel Rodriguez-Cardenas; Aya Garryyeva; David Nader Palacio; Antonio Mastropaolo; Denys Poshyvanyk
  - Venue / 年份：arXiv 预印本 / 2026
  - DOI / 原文：[arXiv:2605.28482](https://arxiv.org/abs/2605.28482)
  - 主题：因果推断、SCM、混杂控制、LLM代码生成
  - 一句话价值：用显式DAG、识别、倾向得分估计与refutation把提示相关性改写为可审计的干预效应问题。

### 2026-08-14

- **Causal Testing: Understanding Defects' Root Causes**
  - 简称：Causal Testing
  - 作者：Brittany Johnson; Yuriy Brun; Alexandra Meliou
  - Venue / 年份：ICSE 2020
  - DOI / 原文：[10.1145/3377811.3380377](https://doi.org/10.1145/3377811.3380377)
  - 主题：反事实因果、软件测试、根因定位
  - 一句话价值：最小差异通过/失败测试对提供可操作反事实解释。

### 2026-08-13

- **Primers or Reminders? The Effects of Existing Review Comments on Code Review**
  - 简称：Primers or Reminders
  - 作者：Davide Spadini; Gül Calikli; Alberto Bacchelli
  - Venue / 年份：ICSE 2020
  - DOI / 原文：[10.1145/3377811.3380385](https://doi.org/10.1145/3377811.3380385)
  - 主题：代码审查、随机实验、认知偏差、干预效应
  - 一句话价值：随机操纵已有评论的可见性，发现罕见缺陷提示显著提高同类缺陷发现率，却未观察到挤出其他缺陷的证据。

### 2026-08-10

- **Do Explicit Review Strategies Improve Code Review Performance? Towards Understanding the Role of Cognitive Load**
  - 简称：Explicit Review Strategies
  - 作者：Pavlína Wurzel Gonçalves; Enrico Fregnan; Tobias Baum; Kurt Schneider; Alberto Bacchelli
  - Venue / 年份：EMSE 2022
  - DOI / 原文：[10.1007/s10664-022-10123-8](https://doi.org/10.1007/s10664-022-10123-8)
  - 主题：代码审查、随机实验、认知负荷、异质效应
  - 一句话价值：随机比较自由审查、普通清单和引导式清单，说明审查干预的效果取决于任务复杂度且机制分析容易因低基准表现失效。

### 2026-08-07

- **Mitigating Omitted Variable Bias in Empirical Software Engineering**
  - 简称：OVB in ESE
  - 作者：Carlo A. Furia; Richard Torkar
  - Venue / 年份：EMSE 2026
  - DOI / 原文：[10.1007/s10664-026-10851-1](https://doi.org/10.1007/s10664-026-10851-1)
  - 主题：因果推断、遗漏变量偏差、敏感性分析
  - 一句话价值：用DAG、调整集和tipping-point分析评估观察性软工研究对未测混杂的稳健性。

### 2026-08-06

- **3100 Opinions on Code Review in an AI World: Building Causal Theory from Practitioner Discourse**
  - 简称：3100 Opinions
  - 作者：Shyam Agarwal; Courtney Miller; Christian Kästner; Bogdan Vasilescu
  - Venue / 年份：arXiv 2026
  - DOI / 原文：[arXiv:2607.07980](https://arxiv.org/abs/2607.07980)
  - 主题：AI代码审查、因果理论、从业者话语
  - 一句话价值：提出包含26个构念和67条关系的候选因果理论，但尚未识别实际因果效应。

### 2026-08-05

- **Echoes of AI: Investigating the Downstream Effects of AI Assistants on Software Maintainability**
  - 简称：Echoes of AI
  - 作者：待核验
  - Venue / 年份：EMSE 2026
  - DOI / 原文：待核验
  - 主题：AI辅助开发、可维护性、实证研究
  - 一句话价值：关注AI助手对下游软件可维护性的长期影响，而不只衡量即时生产率。

### 2026-08-04

- **Code Review as Decision-Making: Building a Cognitive Model from the Questions Asked During Code Review**
  - 简称：Code Review as Decision-Making
  - 作者：Lo Gullstrand Heander; Emma Söderberg; Christofer Rydenfält
  - Venue / 年份：EMSE 2026
  - DOI / 原文：[10.1007/s10664-025-10791-2](https://doi.org/10.1007/s10664-025-10791-2)
  - 主题：代码审查、认知模型、决策过程
  - 一句话价值：将代码审查刻画为先定向、后分析的迭代决策过程。

### 2026-08-03

- **Think Like Human Developers: Harnessing Community Knowledge for Structured Code Reasoning**
  - 简称：Think Like Human Developers
  - 作者：待核验
  - Venue / 年份：ICSE 2026
  - DOI / 原文：待核验
  - 主题：结构化代码推理、社区知识、LLM4SE
  - 一句话价值：利用开发者社区知识构造更接近人类开发者的代码推理过程。

## 待精读论文

