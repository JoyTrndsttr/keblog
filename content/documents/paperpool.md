# Paper Pool

## 2026-09-11 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-09-11 | On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation | Jia Feng; Zhanyue Qin; Cuiyun Gao; Ruiqi Wang; Chaozheng Wang; Yingwei Ma; Xiaoyuan Xie | arXiv cs.SE / 2026 | [arXiv:2604.13725](https://arxiv.org/abs/2604.13725) | 仓库级上下文、上下文压缩、噪声、代码生成、异质效应 | 系统比较 Text-to-Text、Text-to-Vector 与 Text-to-Image 压缩，发现部分 T2V 设置超过 Full Context，而部分文本压缩甚至低于 No Context；它为“额外仓库上下文可能主动伤害模型”提供重要现象证据，但尚未单独识别 denoising 的因果机制。 | 已精读 |

## 2026-09-10 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-09-10 | Causal Software Engineering: A Vision and Roadmap | Roberto Pietrantuono; Luca Giamattei; Stefano Russo; Julien Siebert; Neil Walkinshaw | FSE 2026 Ideas, Visions and Reflections | [10.1145/3803437.3805585](https://doi.org/10.1145/3803437.3805585); [arXiv:2605.02454](https://arxiv.org/abs/2605.02454) | 因果软件工程、干预、反事实、因果可观测性、可信评测 | 把软件工程中的代码、配置、测试、部署和修复统一视为干预，提出 Causal Design Spec、Intervention Log、Living Causal Model 与四条路线；其价值是给 Causality for Code Review 提供方法论总框架，而非已经验证的因果效果。 | 已精读 |

## 2026-09-08 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-09-08 | Explaining Explanations: An Empirical Study of Explanations in Code Reviews | Ratnadira Widyasari; Ting Zhang; Abir Bouraffa; Walid Maalej; David Lo | TOSEM 34(6), Article 177 / 2025 | [10.1145/3708518](https://doi.org/10.1145/3708518) | 代码审查解释、审查沟通、LLM生成、经验差异、因果实验设计 | 从793条“有用”首轮行内评论中归纳七类解释，并验证GPT-3.5可按指定类型改写；它建立了可操作的解释分类，但尚未证明解释会改善采纳、效率或代码质量，适合作为后续随机干预的Treatment设计基础。 | 已精读 |

## 2026-09-07 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-09-07 | What Makes a Code Review Useful to OpenDev Developers? An Empirical Investigation | Asif Kamal Turzo; Amiangshu Bosu | Empirical Software Engineering 29(1):6 / 2024；FSE 2024 Journal First | [10.1007/s10664-023-10411-x](https://doi.org/10.1007/s10664-023-10411-x); [arXiv:2302.11686](https://arxiv.org/abs/2302.11686) | 代码审查有用性、混合方法、调查、回归、Outcome构念 | 把“作者是否采纳/承认”与评论类别评分组合成有用性指标，并发现若干上下文关联；它最重要的价值是暴露了代码审查Outcome构造、后处理变量与观察性回归被误读为因果效应的风险。 | 已精读 |

## 2026-09-04 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-09-04 | SeRe: A Security-Related Code Review Dataset Aligned with Real-World Review Activities | Zixiao Zhao; Yanjie Jiang; Hui Liu; Kui Liu; Lu Zhang | ICSE 2026 | [10.1145/3744916.3764557](https://doi.org/10.1145/3744916.3764557); [Replication Package](https://github.com/caagc/Sere) | 安全代码审查、主动学习、数据集构建、LLM评测、选择偏差 | 以主动学习和五模型投票从373,824条审查记录中提取6,732条安全审查；高精度筛选适合构建干净语料，但42.38%召回率和条件化抽样意味着它更像“高置信安全审查子集”，不能代表安全问题的完整真实分布。 | 已精读 |

## 2026-09-03 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-09-03 | From Static to Dynamic: Benchmarking Real-World Code Review with MCR-Bench | Dewu Zheng; Yanlin Wang; Xiwen Wang; Kefeng Duan; Hongyu Zhang; Xilin Liu; Yuchi Ma; Zibin Zheng | ISSTA 2026 / Proceedings of the ACM on Software Engineering 3 | [10.1145/3832219](https://doi.org/10.1145/3832219); [arXiv:2608.27442](https://arxiv.org/abs/2608.27442) | 多轮代码审查、动态缺陷状态、LLM评测、长程记忆、benchmark | 2,269个真实多轮PR任务把评价从单轮缺陷命中扩展到New/Open/Resolved/Reopened状态追踪；模型随轮次的表面退化很有启发，但轮次与任务构成、样本量和难度共同变化，不能直接解释成长程记忆的因果效应。 | 已精读 |

## 2026-09-02 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-09-02 | Can We Benchmark Code Review Studies? A Systematic Mapping Study of Methodology, Dataset, and Metric | Dong Wang; Yuki Ueda; Raula Gaikovina Kula; Takashi Ishio; Kenichi Matsumoto | Journal of Systems and Software 180 / 2021 | [10.1016/j.jss.2021.111009](https://doi.org/10.1016/j.jss.2021.111009) | 代码审查、系统映射、benchmark、数据复现、指标构念 | 对2011–2019年112篇高影响代码审查研究的映射发现，仅42/84篇定量或混合研究公开可复用数据，31篇定量研究使用了457个指标；指标存在局部共识，但数据、任务与构念尚不足以形成统一benchmark。 | 已精读 |

## 2026-09-01 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-09-01 | Quality Gatekeepers: Investigating the Effects of Code Review Bots on Pull Request Activities | Mairieli Wessel; Alexander Serebrenik; Igor Wiese; Igor Steinmacher; Marco A. Gerosa | Empirical Software Engineering 27:108 / 2022 | [10.1007/s10664-022-10130-9](https://doi.org/10.1007/s10664-022-10130-9) | 代码审查机器人、工具采用、分段回归、混合方法、PR活动 | 1,194个GitHub项目的采用前后分析显示覆盖率机器人上线后合并PR增多、未合并PR减少且合并PR人工评论下降；但采用时点并非随机，结果仍依赖无同期干预等识别假设，访谈提供的是机制解释而非中介效应证明。 | 已精读 |

## 2026-08-31 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-31 | RovoDev Code Reviewer: A Large-Scale Online Evaluation of LLM-based Code Review Automation at Atlassian | Kla Tantithamthavorn; Yaotian Zou; Andy Wong; Michael Gupta; Zhe Wang; Mike Buller; Ryan Jiang; Matthew Watson; Minwoo Jeong; Kun Chen; Ming Wu | ICSE-SEIP 2026 | [10.1145/3786583.3786851](https://doi.org/10.1145/3786583.3786851) | 工业代码审查、在线部署、LLM评论、工作流影响、因果识别 | 逾1900个仓库的一年部署显示38.70%的机器评论随后对应代码修改，但PR周期和人工评论下降来自观察性队列及中断时间序列，能支持真实关联与可用性，尚不能独立识别RovoDev的纯因果效应。 | 已精读 |

## 2026-08-30 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-30 | Code Review Comprehension: Reviewing Strategies Seen Through Code Comprehension Theories | Pavlína Wurzel Gonçalves; Pooja Rani; Margaret-Anne Storey; Diomidis Spinellis; Alberto Bacchelli | ICPC 2025 | [10.1109/ICPC66645.2025.00068](https://doi.org/10.1109/ICPC66645.2025.00068) | 代码审查、代码理解、认知模型、审查策略、质性研究 | 真实观察显示专家审查并非简单线性读diff，而是先建立上下文，再按复杂度机会式组合线性阅读、难度优先、分块、测试与讨论；该模型适合提出机制假设，但不能直接证明哪种策略提高审查质量。 | 已精读 |

## 2026-08-29 已精读补录

| 精读日期 | 标题 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-29 | The Effect of Complexity and Provenance on Code Review Decisions: Evidence from a Controlled Experiment | Neha Singh; Francesco Sovrano; Vincent J. Hellendoorn; Alberto Bacchelli | FSE 2026 / Proceedings of the ACM on Software Engineering 3 | [10.1145/3808165](https://doi.org/10.1145/3808165) | 代码审查、受控实验、复杂度、AI 来源标签、过度服从 | 2×2×2 随机实验发现高复杂任务包与接受错误修订相关，而 AI/人类标签无主效应；但每个复杂度只有一个不同代码片段且缺陷类型不同，不能把差异纯归因于复杂度。 | 已精读 |

> 用于每日中文技术情报简报的论文去重与候选管理。
> 去重优先级：DOI > arXiv ID > 规范化标题。已精读论文永久不重复推荐，除非明确要求重读。

## 已精读论文

| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-03 | Think Like Human Developers: Harnessing Community Knowledge for Structured Code Reasoning | 待核验 | ICSE 2026 | 待核验 | 结构化代码推理、社区知识、LLM4SE | 利用开发者社区知识构造更接近人类开发者的代码推理过程。 | 已精读 |
| 2026-08-04 | Code Review as Decision-Making: Building a Cognitive Model from the Questions Asked During Code Review | Lo Gullstrand Heander; Emma Söderberg; Christofer Rydenfält | EMSE 2026 | [10.1007/s10664-025-10791-2](https://doi.org/10.1007/s10664-025-10791-2) | 代码审查、认知模型、决策过程 | 将代码审查刻画为先定向、后分析的迭代决策过程。 | 已精读 |
| 2026-08-05 | Echoes of AI: Investigating the Downstream Effects of AI Assistants on Software Maintainability | 待核验 | EMSE 2026 | 待核验 | AI辅助开发、可维护性、实证研究 | 关注AI助手对下游软件可维护性的长期影响，而不只衡量即时生产率。 | 已精读 |
| 2026-08-06 | 3100 Opinions on Code Review in an AI World: Building Causal Theory from Practitioner Discourse | Shyam Agarwal; Courtney Miller; Christian Kästner; Bogdan Vasilescu | arXiv 2026 | [arXiv:2607.07980](https://arxiv.org/abs/2607.07980) | AI代码审查、因果理论、从业者话语 | 提出包含26个构念和67条关系的候选因果理论，但尚未识别实际因果效应。 | 已精读 |
| 2026-08-07 | Mitigating Omitted Variable Bias in Empirical Software Engineering | Carlo A. Furia; Richard Torkar | EMSE 2026 | [10.1007/s10664-026-10851-1](https://doi.org/10.1007/s10664-026-10851-1) | 因果推断、遗漏变量偏差、敏感性分析 | 用DAG、调整集和tipping-point分析评估观察性软工研究对未测混杂的稳健性。 | 已精读 |
| 2026-08-10 | Do Explicit Review Strategies Improve Code Review Performance? Towards Understanding the Role of Cognitive Load | Pavlína Wurzel Gonçalves; Enrico Fregnan; Tobias Baum; Kurt Schneider; Alberto Bacchelli | EMSE 2022 | [10.1007/s10664-022-10123-8](https://doi.org/10.1007/s10664-022-10123-8) | 代码审查、随机实验、认知负荷、异质效应 | 随机比较自由审查、普通清单和引导式清单，说明审查干预的效果取决于任务复杂度且机制分析容易因低基准表现失效。 | 已精读 |

## 候选论文

| 首次发现 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 与 Causality for Code Review 的相关度 | 入池理由 | 状态 |
|---|---|---|---|---|---|---|---|---|

### 2026-08-13 已精读补充

| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-13 | Primers or Reminders? The Effects of Existing Review Comments on Code Review | Davide Spadini; Gül Calikli; Alberto Bacchelli | ICSE 2020 | [10.1145/3377811.3380385](https://doi.org/10.1145/3377811.3380385) | 代码审查、随机实验、认知偏差、干预效应 | 随机操纵已有评论的可见性，发现罕见缺陷提示显著提高同类缺陷发现率，却未观察到挤出其他缺陷的证据。 | 已精读 |

## 维护约定

## 2026-08-16 已精读补录

| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-16 | Improving Code Reviewer Recommendation: Accuracy, Latency, Workload, and Bystanders | Peter C. Rigby; Seth Rogers; Sadruddin Saleem; Parth Suresh; Daniel Suskin; Patrick Riggs; Chandra Shekhar Maddila; Nachiappan Nagappan; Audris Mockus | TOSEM 35(1), 2026 / ICSE 2026 Journal-first | [10.1145/3736405](https://doi.org/10.1145/3736405) | 代码审查、审查者推荐、随机对照实验、工作负载、旁观者效应 | 三项生产环境 A/B 实验表明离线准确率不足以代表真实干预效果，显式责任分配可缩短审查周期。 | 已精读 |

- 新论文只有在来源可靠、与研究方向相关且值得后续精读时才进入候选区。
- 候选论文完成精读后，移动到“已精读论文”，不同时保留两个活跃条目。
- `待核验` 字段应在后续运行中通过会议、期刊、DOI 或论文官方页面补全，不得猜测。
- 每次写入前重新读取文件，保留人工修改。
- 每日简报成功发布后，再记录当日精读论文。

## 2026-08-14 已精读补录

| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-14 | Causal Testing: Understanding Defects' Root Causes | Brittany Johnson; Yuriy Brun; Alexandra Meliou | ICSE 2020 | [10.1145/3377811.3380377](https://doi.org/10.1145/3377811.3380377) | 反事实因果、软件测试、根因定位 | 最小差异通过/失败测试对提供可操作反事实解释。 | 已精读 |

## 2026-08-15 已精读补录

| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-15 | Rethinking Software Empirical Studies with Structural Causal Models | Daniel Rodriguez-Cardenas; Aya Garryyeva; David Nader Palacio; Antonio Mastropaolo; Denys Poshyvanyk | arXiv 预印本 / 2026 | [arXiv:2605.28482](https://arxiv.org/abs/2605.28482) | 因果推断、SCM、混杂控制、LLM代码生成 | 用显式DAG、识别、倾向得分估计与refutation把提示相关性改写为可审计的干预效应问题。 | 已精读 |

## 2026-08-17 已精读补录

| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-17 | Shaky Structures: The Wobbly World of Causal Graphs in Software Analytics | Jeremy Hulse; Nasir U. Eisty; Tim Menzies | EMSE 30(5), 2025 / ICSE 2026 Journal-first | [10.1007/s10664-025-10690-6](https://doi.org/10.1007/s10664-025-10690-6) | 因果发现、结构稳定性、软件分析、敏感性分析 | 四类因果发现器在23个软工数据集上对版本、项目、参数和抽样扰动高度敏感，提示自动发现的单一DAG不能直接支撑稳定因果结论。 | 已精读 |

## 2026-08-25 已精读补录

| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-25 | OpenCodeReview: Determinism over Non-Determinism for Cost-Effective Agent-Based Code Review | Zhengfeng Li; Lei Zhang; Xianwei Wu; Zhengqi Zhuang; Yingjie Xu; Boge Wang; Shaofei Zhu; Chuan Wang; Peng Zhao; Xinyu Zheng; Guoping Rong | arXiv 预印本 / 2026 | [arXiv:2608.09290](https://arxiv.org/abs/2608.09290) | Agent 代码审查、仓库上下文、确定性工程、反思过滤、成本 | 确定性规则分派、受限仓库探索与非对称信息反思在系统级对比中改善精度和成本，但尚缺组件消融与跨运行稳定性验证。 | 已精读 |

## 2026-08-26 已精读补录

| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-26 | AACR-Bench: Evaluating Automatic Code Review with Holistic Repository-Level Context | Lei Zhang; Yongda Yu; Minghui Yu; Xinxin Guo; Zhengqi Zhuang; Guoping Rong; Dong Shao; Haifeng Shen; Hongyu Kuang; Zhengfeng Li; Boge Wang; Guoan Zhang; Bangyu Xiang; Xiaobin Xu | arXiv 预印本 / 2026 | [arXiv:2601.19494](https://arxiv.org/abs/2601.19494) | 自动代码审查评测、仓库级上下文、多语言基准、专家核验、语义评价 | 用多模型发现和双人专家核验补全PR缺陷并标注上下文层级，但模型生成型ground truth、选择性PR抽样与非对称检索预算使评价更全面却不天然中立。 | 已精读 |

## 2026-08-27 已精读补录

| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-27 | DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection | Mingyang Sun; Guozhu Meng | Internetware 2026 / arXiv 2026 | [arXiv:2607.13439](https://arxiv.org/abs/2607.13439) | 仓库级漏洞检测、推理探索解耦、RepoPairBench、Lucky Hits、成本 | 结构化、按假设驱动的仓库探索比函数或整文件上下文更可靠，且可把93%以上token卸载给本地Explorer；但角色解耦与模型差异、信息压缩和预算同时变化，尚不能单独识别解耦本身的因果效应。 | 已精读 |

## 2026-08-28 已精读补录
| 精读日期 | 论文 | 作者 | Venue / 年份 | DOI / 原文 | 主题 | 一句话价值 | 状态 |
|---|---|---|---|---|---|---|---|
| 2026-08-28 | EntailLLM: Verifying LLM-Generated Vulnerability Discovery Paths with Domain Knowledge via Logic Programming | Kaustuv Mukherji; Jaikrishna Manojkumar Patil; Colton Payne; Paulo Shakarian; Dana Warmsley; Nigel Stepp; Evelyn Kim | arXiv 预印本 / 2026 | [arXiv:2608.01763](https://arxiv.org/abs/2608.01763) | 漏洞路径、调用图、领域知识、逻辑蕴涵、LLM验证 | 将LLM路径实例化到真实调用图，再用CWE知识做可解释逻辑蕴涵过滤；但Outcome是规则一致性而非漏洞真实性，且同一领域知识同时影响生成与验证，高一致率不等于独立验证。 | 已精读（取代候选区同名计划项；候选项不再活跃） |
