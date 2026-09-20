# Paper Pool · 2026-08

> 2026 年 8 月完整精读记录。新增/修改历史月份内容时维护本文件；日常去重优先读取 `paperpool_short.md`。

## 已精读论文

### 2026-08-31

- **RovoDev Code Reviewer: A Large-Scale Online Evaluation of LLM-based Code Review Automation at Atlassian**
  - 简称：[RovoDev Code Reviewer](https://38-76-161-31.sslip.io/daily-learning/?paper=260831-KlaTantithamthavorn-RovoDev)
  - Tags：`2026` `ICSE-SEIP` `代码评审` `LLM代码评审` `工业实践` `在线评测` `开发者行为` `Pull Request` `因果识别`
  - 作者：Kla Tantithamthavorn; Yaotian Zou; Andy Wong; Michael Gupta; Zhe Wang; Mike Buller; Ryan Jiang; Matthew Watson; Minwoo Jeong; Kun Chen; Ming Wu
  - Venue / 年份：ICSE-SEIP 2026
  - DOI / 原文：[10.1145/3786583.3786851](https://doi.org/10.1145/3786583.3786851)
  - 主题：工业代码审查、在线部署、LLM评论、工作流影响、因果识别
  - 一句话价值：逾1900个仓库的一年部署显示38.70%的机器评论随后对应代码修改，但PR周期和人工评论下降来自观察性队列及中断时间序列，能支持真实关联与可用性，尚不能独立识别RovoDev的纯因果效应。

### 2026-08-30

- **Code Review Comprehension: Reviewing Strategies Seen Through Code Comprehension Theories**
  - 简称：[Code Review Comprehension](https://38-76-161-31.sslip.io/daily-learning/?paper=260830-PavlinaGoncalves-CodeReviewComprehension)
  - Tags：`2025` `ICPC` `代码评审` `代码理解` `认知模型` `审查策略` `开发者行为` `质性研究`
  - 作者：Pavlína Wurzel Gonçalves; Pooja Rani; Margaret-Anne Storey; Diomidis Spinellis; Alberto Bacchelli
  - Venue / 年份：ICPC 2025
  - DOI / 原文：[10.1109/ICPC66645.2025.00068](https://doi.org/10.1109/ICPC66645.2025.00068)
  - 主题：代码审查、代码理解、认知模型、审查策略、质性研究
  - 一句话价值：真实观察显示专家审查并非简单线性读diff，而是先建立上下文，再按复杂度机会式组合线性阅读、难度优先、分块、测试与讨论；该模型适合提出机制假设，但不能直接证明哪种策略提高审查质量。

### 2026-08-29

- **The Effect of Complexity and Provenance on Code Review Decisions: Evidence from a Controlled Experiment**
  - 简称：[Complexity & Provenance](https://38-76-161-31.sslip.io/daily-learning/?paper=260829-NehaSingh-ComplexityAndProvenance)
  - Tags：`2026` `FSE` `代码评审` `受控实验` `任务复杂度` `AI代码` `Provenance` `Automation Bias` `因果推断`
  - 作者：Neha Singh; Francesco Sovrano; Vincent J. Hellendoorn; Alberto Bacchelli
  - Venue / 年份：FSE 2026 / Proceedings of the ACM on Software Engineering 3
  - DOI / 原文：[10.1145/3808165](https://doi.org/10.1145/3808165)
  - 主题：代码审查、受控实验、复杂度、AI 来源标签、过度服从
  - 一句话价值：2×2×2 随机实验发现高复杂任务包与接受错误修订相关，而 AI/人类标签无主效应；但每个复杂度只有一个不同代码片段且缺陷类型不同，不能把差异纯归因于复杂度。

### 2026-08-28

- **EntailLLM: Verifying LLM-Generated Vulnerability Discovery Paths with Domain Knowledge via Logic Programming**
  - 简称：[EntailLLM](https://38-76-161-31.sslip.io/daily-learning/?paper=260828-KaustuvMukherji-EntailLLM)
  - Tags：`2026` `arXiv/Preprint` `漏洞检测` `漏洞路径` `调用图` `逻辑推理` `领域知识` `LLM验证` `软件安全`
  - 作者：Kaustuv Mukherji; Jaikrishna Manojkumar Patil; Colton Payne; Paulo Shakarian; Dana Warmsley; Nigel Stepp; Evelyn Kim
  - Venue / 年份：arXiv 预印本 / 2026
  - DOI / 原文：[arXiv:2608.01763](https://arxiv.org/abs/2608.01763)
  - 主题：漏洞路径、调用图、领域知识、逻辑蕴涵、LLM验证
  - 一句话价值：将LLM路径实例化到真实调用图，再用CWE知识做可解释逻辑蕴涵过滤；但Outcome是规则一致性而非漏洞真实性，且同一领域知识同时影响生成与验证，高一致率不等于独立验证。

### 2026-08-27

- **DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection**
  - 简称：[DREA](https://38-76-161-31.sslip.io/daily-learning/?paper=260827-MingyangSun-DREA)
  - Tags：`2026` `Internetware` `arXiv/Preprint` `漏洞检测` `多智能体系统` `Coding Agent` `仓库级搜索` `推理与探索` `软件安全` `上下文工程`
  - 作者：Mingyang Sun; Guozhu Meng
  - Venue / 年份：Internetware 2026 / arXiv 2026
  - DOI / 原文：[arXiv:2607.13439](https://arxiv.org/abs/2607.13439)
  - 主题：仓库级漏洞检测、推理探索解耦、RepoPairBench、Lucky Hits、成本
  - 一句话价值：结构化、按假设驱动的仓库探索比函数或整文件上下文更可靠，且可把93%以上token卸载给本地Explorer；但角色解耦与模型差异、信息压缩和预算同时变化，尚不能单独识别解耦本身的因果效应。

### 2026-08-26

- **AACR-Bench: Evaluating Automatic Code Review with Holistic Repository-Level Context**
  - 简称：[AACR-Bench](https://38-76-161-31.sslip.io/daily-learning/?paper=260826-LeiZhang-AACRBench)
  - Tags：`2026` `arXiv/Preprint` `代码评审` `自动代码评审` `上下文工程` `仓库级上下文` `多语言` `专家标注` `Benchmark`
  - 作者：Lei Zhang; Yongda Yu; Minghui Yu; Xinxin Guo; Zhengqi Zhuang; Guoping Rong; Dong Shao; Haifeng Shen; Hongyu Kuang; Zhengfeng Li; Boge Wang; Guoan Zhang; Bangyu Xiang; Xiaobin Xu
  - Venue / 年份：arXiv 预印本 / 2026
  - DOI / 原文：[arXiv:2601.19494](https://arxiv.org/abs/2601.19494)
  - 主题：自动代码审查评测、仓库级上下文、多语言基准、专家核验、语义评价
  - 一句话价值：用多模型发现和双人专家核验补全PR缺陷并标注上下文层级，但模型生成型ground truth、选择性PR抽样与非对称检索预算使评价更全面却不天然中立。

### 2026-08-25

- **OpenCodeReview: Determinism over Non-Determinism for Cost-Effective Agent-Based Code Review**
  - 简称：[OpenCodeReview](https://38-76-161-31.sslip.io/daily-learning/?paper=260825-ZhengfengLi-OpenCodeReview)
  - Tags：`2026` `arXiv/Preprint` `代码评审` `Coding Agent` `多智能体系统` `仓库级上下文` `确定性工程` `反思` `推理成本`
  - 作者：Zhengfeng Li; Lei Zhang; Xianwei Wu; Zhengqi Zhuang; Yingjie Xu; Boge Wang; Shaofei Zhu; Chuan Wang; Peng Zhao; Xinyu Zheng; Guoping Rong
  - Venue / 年份：arXiv 预印本 / 2026
  - DOI / 原文：[arXiv:2608.09290](https://arxiv.org/abs/2608.09290)
  - 主题：Agent 代码审查、仓库上下文、确定性工程、反思过滤、成本
  - 一句话价值：确定性规则分派、受限仓库探索与非对称信息反思在系统级对比中改善精度和成本，但尚缺组件消融与跨运行稳定性验证。

### 2026-08-24

- **Does Developer Familiarity Hasten Bug Resolution? A Causal Inference Perspective**
  - 简称：[Developer Familiarity](https://38-76-161-31.sslip.io/daily-learning/?paper=260824-ReshmaRoychoudhuri-DeveloperFamiliarity)
  - Tags：`2026` `EMSE` `缺陷修复` `因果推断` `IPTW` `开发者熟悉度` `开发者行为` `异质效应`
  - 作者：Reshma Roychoudhuri; Michael Chen; Subhajit Datta; Subhashis Majumder  - Venue / 年份：Empirical Software Engineering 31:111 / 2026
  - DOI / 原文：[10.1007/s10664-026-10852-0](https://doi.org/10.1007/s10664-026-10852-0)
  - 主题：缺陷修复、开发者熟悉度、因果推断、IPTW、异质效应
  - 一句话价值：用 IPTW 估计开发者熟悉度对缺陷解决时间的影响，并揭示跨软件生态的明显异质性。

### 2026-08-23

- **An Exploratory Study of Bug-Introducing Changes: Exploring Relationships in Bug-Introducing Changes Towards Causal Understanding**
  - 简称：[Bug-Introducing Changes](https://38-76-161-31.sslip.io/daily-learning/?paper=260823-LukasSchulte-BugIntroducingChanges)
  - Tags：`2026` `EMSE` `缺陷引入` `因果推断` `因果图` `混杂因素` `实证软件工程` `变量关系`
  - 作者：Lukas Schulte; Anamaria Mojica-Hanke; Mario Linares-Vásquez; Steffen Herbold
  - Venue / 年份：Empirical Software Engineering 31:114 / 2026
  - DOI / 原文：[10.1007/s10664-026-10822-6](https://doi.org/10.1007/s10664-026-10822-6)
  - 主题：缺陷引入变更、因果理解、变量关系、混杂因素、实证软件工程
  - 一句话价值：梳理缺陷引入变更周围的 81 个变量及候选关系，为后续因果图、混杂控制与代码审查效应研究提供变量基础。

### 2026-08-10

- **Do Explicit Review Strategies Improve Code Review Performance? Towards Understanding the Role of Cognitive Load**
  - 简称：[Explicit Review Strategies](https://38-76-161-31.sslip.io/daily-learning/?paper=260810-PavlinaGoncalves-ExplicitReviewStrategies)
  - Tags：`2022` `EMSE` `代码评审` `受控实验` `认知负荷` `审查策略` `任务复杂度` `异质效应`
  - 作者：Pavlína Wurzel Gonçalves; Enrico Fregnan; Tobias Baum; Kurt Schneider; Alberto Bacchelli
  - Venue / 年份：EMSE 2022
  - DOI / 原文：[10.1007/s10664-022-10123-8](https://doi.org/10.1007/s10664-022-10123-8)
  - 主题：代码审查、随机实验、认知负荷、异质效应
  - 一句话价值：随机比较自由审查、普通清单和引导式清单，说明审查干预的效果取决于任务复杂度且机制分析容易因低基准表现失效。

### 2026-08-07

- **Mitigating Omitted Variable Bias in Empirical Software Engineering**
  - 简称：[OVB in ESE](https://38-76-161-31.sslip.io/daily-learning/?paper=260807-CarloFuria-OmittedVariableBias)
  - Tags：`2026` `EMSE` `因果推断` `遗漏变量偏差` `DAG` `敏感性分析` `混杂因素` `实证软件工程`
  - 作者：Carlo A. Furia; Richard Torkar
  - Venue / 年份：EMSE 2026
  - DOI / 原文：[10.1007/s10664-026-10851-1](https://doi.org/10.1007/s10664-026-10851-1)
  - 主题：因果推断、遗漏变量偏差、敏感性分析
  - 一句话价值：用DAG、调整集和tipping-point分析评估观察性软工研究对未测混杂的稳健性。

### 2026-08-06

- **3100 Opinions on Code Review in an AI World: Building Causal Theory from Practitioner Discourse**
  - 简称：[3100 Opinions](https://38-76-161-31.sslip.io/daily-learning/?paper=260806-ShyamAgarwal-3100Opinions)
  - Tags：`2026` `arXiv/Preprint` `代码评审` `AI代码评审` `因果理论` `开发者观点` `质性研究` `因果图` `人机协作`
  - 作者：Shyam Agarwal; Courtney Miller; Christian Kästner; Bogdan Vasilescu
  - Venue / 年份：arXiv 2026
  - DOI / 原文：[arXiv:2607.07980](https://arxiv.org/abs/2607.07980)
  - 主题：AI代码审查、因果理论、从业者话语
  - 一句话价值：提出包含26个构念和67条关系的候选因果理论，但尚未识别实际因果效应。

### 2026-08-03

- **Think Like Human Developers: Harnessing Community Knowledge for Structured Code Reasoning**
  - 简称：[Think Like Human Developers](https://38-76-161-31.sslip.io/daily-learning/?paper=260803-ChengranYang-ThinkLikeHumanDevelopers)
  - Tags：`2026` `ICSE` `代码推理` `代码智能` `社区知识` `结构化推理` `LLM4SE` `模型微调` `代码生成`
  - 作者：待核验
  - Venue / 年份：ICSE 2026
  - DOI / 原文：待核验
  - 主题：结构化代码推理、社区知识、LLM4SE
  - 一句话价值：利用开发者社区知识构造更接近人类开发者的代码推理过程。

## 待精读论文

> 待精读候选统一维护在当前月份文件；本历史文件不维护待精读列表。
