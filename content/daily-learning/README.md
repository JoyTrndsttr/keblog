# 每日学习索引

这里是论文精读归档的 Markdown 索引。每次完整精读使用独立目录，目录名固定为 `YYMMDD-第一作者英文名-论文简称`。

> 已归档：**103 次精读**，覆盖 **2026-08-03—2026-11-27**。
> 去重说明：`Quality Gatekeepers` 在 2026-08-19 与 2026-09-01 各有一次精读，为忠实保留学习历史而分别归档；选新论文时仍按同一 DOI 永久去重。

## 固定执行计划

每天 08:30（北京时间）生成技术情报简报，最后完整精读一篇论文。论文永久去重，用户指定选题优先。

[查看完整每日计划](./PLAN.md)

## 已完成

| 精读日期 | 目录 | 论文 | 第一作者 | Venue / 年份 | 状态 |
|---|---|---|---|---|---|
| 2026-11-27 | [261127-AoqiHu-RepoEviAgent](./261127-AoqiHu-RepoEviAgent/README.md) | RepoEviAgent: Scalable Synthesis of Evidence-Grounded Repository-Level Question Answering Tasks | Aoqi Hu | arXiv 2026 | 已精读（完整 v1 10 页，图 1–6、表 1–2） |
| 2026-11-26 | [261126-FeiDing-DependencyMismatch](./261126-FeiDing-DependencyMismatch/README.md) | Edit-Induced Dependency Mismatch: Propagation Omissions, Recovery, and Evaluation Blind Spots in Coding Agents | Fei Ding（一作、通讯） | arXiv 2026 | 已精读（完整43页 v1：图1–3、表1–24与附录A–J；终态/恢复、局部重放与提示词对照） |
| 2026-11-25 | [261125-NickHeiner-SudoL7](./261125-NickHeiner-SudoL7/README.md) | sudo L7: Can Coding Agents Act Like Staff Engineers? | Nick Heiner（原文仅列团队邮箱） | NeurIPS 2026 IAB Workshop | 已精读（完整12页v1、图1、表1–5及附录A–C；评分门槛、重复尝试、失败案例及裁判效度） |
| 2026-11-24 | [261124-MarkusBorg-EchoesOfAI](./261124-MarkusBorg-EchoesOfAI/README.md) | Echoes of AI: Investigating the downstream effects of AI assistants on software maintainability | Markus Borg（一作、通讯） | Empirical Software Engineering 2026 | 已精读（正式刊版78页；两阶段随机设计与DAG、效率及质量四指标、贝叶斯敏感性和证据边界） |
| 2026-11-23 | [261123-XiaoFan-ClaimLockedReporting](./261123-XiaoFan-ClaimLockedReporting/README.md) | Provenance Before Prose: Claim-Locked Reporting for Statistical Text Generation | Xiao Fan（通讯作者 Jingyuan Li、Yi Zhang） | EMNLP 2026 主会 | 已精读（完整15页、图1–2、表1–6/A1–A5及附录A–F；结论锁定、方向人审、数字告警校准与工件范围） |
| 2026-11-22 | [261122-DangfengPan-CommentContent](./261122-DangfengPan-CommentContent/README.md) | Talking to Itself While Coding: What Makes Comments Help Code Generation? | Dangfeng Pan（通讯作者 Zhensu Sun） | Findings of EMNLP 2026 | 已精读（完整25页、图1–2、表1–19及附录A–D；最小语义改写、等长噪声、仓库级复现与提示异质性） |
| 2026-11-21 | [261121-ZeruiYang-AnytimeStopping](./261121-ZeruiYang-AnytimeStopping/README.md) | Done, But Still Working: Anytime Evaluation of When Coding Agents Should Stop | Zerui Yang（与 Chaorui Zhang 为通讯作者） | arXiv 2026 | 已精读（完整22页v1、图1–6、表1–8及附录A–T；停止与回选、配对重放、补丁评分审计及蒸馏的质量边界） |
| 2026-11-20 | [261120-ZeruiYang-ContextPrice](./261120-ZeruiYang-ContextPrice/README.md) | Context Has a Price: Adding and Removing Context for LLM Coding Agents under Prefix Caching | Zerui Yang（与 Chaorui Zhang 为通讯作者） | arXiv 2026 | 已精读（完整25页v1、图1–10、表1–7及附录A–R；前缀缓存、行为补偿、价格反转、质量评分缺陷与原始研究记录核查） |
| 2026-11-19 | [261119-LuisWiedmann-AgentSystems](./261119-LuisWiedmann-AgentSystems/README.md) | Agents Are Systems, Not Models: Rethinking Agentic Evaluation | Luis Wiedmann（原文未单独标注通讯作者） | arXiv 2026 | 已精读（完整28页v1、图1–8、表1–24及附录A.1–A.18；重复方差、信息×预算、验证oracle、模型交互与缓存成本核查） |
| 2026-11-18 | [261118-AmanPriyanshu-VLocBench](./261118-AmanPriyanshu-VLocBench/README.md) | Vulnerability Localization Benchmark: Measuring Agentic Security Analysis at Repository Scale | Aman Priyanshu、Supriti Vijay、Kimia Majd（共同一作及通讯作者） | arXiv 2026，Foundation AI技术报告 | 已精读（加急；完整29页v1、图1–6、表1–9、附录A–E；前后修复协议、失败阴性、补丁标签、回归与官方manifest核查） |
| 2026-11-18 | [261118-RevanthGangiReddy-SweRank](./261118-RevanthGangiReddy-SweRank/README.md) | SweRank: Software Issue Localization with Code Ranking | Revanth Gangi Reddy、Tarun Suresh、JaeHyeok Doo（共同一作） | ICLR 2026 | 已精读（完整20页v2、图1–11、表1–13、附录A–I；定位监督、困难负例、候选上限、滑窗成本与固定版本代码核查） |
| 2026-11-17 | [261117-RameshArvindNaagarajan-GraphScent](./261117-RameshArvindNaagarajan-GraphScent/README.md) | GraphScent: Calibrating Directional Relevance Signals for Bounded-Context Code Localization | Ramesh Arvind Naagarajan | arXiv 2026（竞赛论文轨投稿） | 已精读（加急；完整18页v1、图1–4、表1–12、附录A–F；方向校准、定位漏斗、负面消融与公开工件核算） |
| 2026-11-17 | [261117-ZhaolingChen-LocAgent](./261117-ZhaolingChen-LocAgent/README.md) | LocAgent: Graph-Guided LLM Agents for Code Localization | Zhaoling Chen（前三位共同一作；通讯作者 Xiangru Tang） | ACL 2025 | 已精读（完整17页正式PDF、图1–8、表1–11及附录A–C；导航/可见性、训练、消融、跨任务与修复传导） |
| 2026-11-17 | [261117-WenkaiFang-NINJA](./261117-WenkaiFang-NINJA/README.md) | NINJA: A Navigator–Inspector Joint Architecture for Context-Efficient Issue Localization | Wenkai Fang | arXiv 2026 | 已精读（加急；完整v1、架构/训练、预算匹配、消融、支持位置与修复实验；会议状态未独立确认） |
| 2026-11-17 | [261117-FuweiZhang-COREBench](./261117-FuweiZhang-COREBench/README.md) | CORE-Bench: A Comprehensive Benchmark for Code Retrieval in the Era of Agentic Coding | Fuwei Zhang | EMNLP 2026 | 已精读（加急；完整29页、三层基准、轨迹标注、文件白名单验证、SFT及CPI对照） |
| 2026-11-16 | [261116-AntonisAntoniades-SWESearch](./261116-AntonisAntoniades-SWESearch/README.md) | SWE-Search: Enhancing Software Agents with Monte Carlo Tree Search and Iterative Refinement | Antonis Antoniades、Albert Örwall（共同一作、明确通讯联系人） | ICLR 2025 | 已精读（完整31页v6、图1–8、表1–4及附录A–L；状态反馈、回退、候选选择与算力公平性） |
| 2026-11-15 | [261115-FrancescoSovrano-LostInTheEnd](./261115-FrancescoSovrano-LostInTheEnd/README.md) | Large Language Models for In-File Vulnerability Localization Can Be “Lost in the End” | Francesco Sovrano | FSE 2025 | 已精读（完整24页v1、图1–5、表1–4、三项RQ及评分/显著性核验；教学式自包含讲解） |
| 2026-11-14 | [261114-JohnYang-SWEAgent](./261114-JohnYang-SWEAgent/README.md) | SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering | John Yang、Carlos E. Jimenez（共同一作） | NeurIPS 2024 | 已完成 |
| 2026-11-13 | [261113-ChunqiuStevenXia-Agentless](./261113-ChunqiuStevenXia-Agentless/README.md) | Demystifying LLM-Based Software Engineering Agents（Agentless） | Chunqiu Steven Xia（与 Yinlin Deng 共同一作） | FSE 2025 | 已精读（正式24页全文、图1–9、表1–6；分层定位、独立分支、测试选择与基准审计，手机自包含讲解） |
| 2026-11-12 | [261112-ZhongmingYu-OrcaLoca](./261112-ZhongmingYu-OrcaLoca/README.md) | OrcaLoca: An LLM Agent Framework for Software Issue Localization | Zhongming Yu（与 Hejia Zhang 共同一作） | ICML 2025 | 已精读（完整20页v2、图1–5、表1–5、算法1及附录A–G；核对正式发表版与作者背景，教学式完整精读） |
| 2026-11-11 | [261111-ZhonghaoJiang-CoSIL](./261111-ZhonghaoJiang-CoSIL/README.md) | Issue Localization via LLM-Driven Iterative Code Graph Searching | Zhonghao Jiang | ASE 2025 | 已精读（完整17页v3、图1–12、表I–X、附录A–E及新旧工件核对；教学式完整精读） |
| 2026-11-10 | [261110-JaineetShah-CausalAgentReplay](./261110-JaineetShah-CausalAgentReplay/README.md) | Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures | Jaineet Shah | arXiv / 2026 | 已精读（完整5页v1、式1、图1、两组合成验证及固定版本公开工件；教学式完整精读） |
| 2026-11-09 | [261109-EgorPakhomov-ExecutedCounterfactual](./261109-EgorPakhomov-ExecutedCounterfactual/README.md) | Attributing Agent Failures to Their History Needs an Executed Counterfactual: Toward a Reporting Standard | Egor Pakhomov | NeurIPS 2026 IAB Workshop（非归档） | 已精读（20页v1全文、图1、表1–14及附录A–F；教学式完整精读） |
| 2026-11-08 | [261108-VyzantinosRepantis-SemanticCompetition](./261108-VyzantinosRepantis-SemanticCompetition/README.md) | Separating Semantic Competition from Context Length in RAG Reading | Vyzantinos Repantis | arXiv / 2026 | 已精读（5页v1全文、式1、图1、表1–2及作者实验工件；教学式完整精读） |
| 2026-11-07 | [261107-RThomasMcCoy-HANS](./261107-RThomasMcCoy-HANS/README.md) | Right for the Wrong Reasons: Diagnosing Syntactic Heuristics in Natural Language Inference | R. Thomas McCoy | ACL 2019 | 已精读（21页正式全文、图1–3、表1–14及附录A–F；教学式完整精读） |
| 2026-11-06 | [261106-MichalMazuryk-PowerlessNoise](./261106-MichalMazuryk-PowerlessNoise/README.md) | The Powerless Noise: How Experimental Settings Shape the Reported Power of Noise | Michał Mazuryk | SIGIR 2026 Repro | 已精读（10页v2全文、图1–2、表1–7及附录A–B；教学式完整精读） |
| 2026-11-05 | [261105-OriYoran-RetrievalRobustness](./261105-OriYoran-RetrievalRobustness/README.md) | Making Retrieval-Augmented Language Models Robust to Irrelevant Context | Ori Yoran | ICLR 2024 | 已精读（22页v2全文、图1–10、表1–8及附录A.1–A.5；教学式完整精读） |
| 2026-11-04 | [261104-NelsonFLiu-LostInTheMiddle](./261104-NelsonFLiu-LostInTheMiddle/README.md) | Lost in the Middle: How Language Models Use Long Contexts | Nelson F. Liu | TACL 2024 | 已精读（正式17页全文、图1–16、表1及附录A–E；教学式完整精读） |
| 2026-11-01 | [261101-TautvydasJackevicius-AppFunctionsSecurity](./261101-TautvydasJackevicius-AppFunctionsSecurity/README.md) | The Agent in the Middle: A Security and Privacy Analysis of Android AppFunctions | Tautvydas Jackevičius | PETS 2027(1) | 计划外完整精读（20 页 PDF；七种攻击、图表与局限） |
| 2026-10-30 | [261030-YuvrajSehgal-ContextPipeline](./261030-YuvrajSehgal-ContextPipeline/README.md) | Context Is a Pipeline, Not a Window: Information Attrition in LLM Agent Harnesses | Yuvraj Sehgal | arXiv cs.SE / 2026 | 已精读（完整 arXiv v1 PDF/HTML、Figure/Table 与复现说明；教学式完整精读） |
| 2026-10-29 | [261029-HaileyJoren-SufficientContext](./261029-HaileyJoren-SufficientContext/README.md) | Sufficient Context: A New Lens on Retrieval Augmented Generation Systems | Hailey Joren | ICLR / 2025 | 已精读（完整 arXiv HTML/PDF、OpenReview 与附录；教学式完整精读） |
| 2026-10-26 | [261026-BrianSamBodden-ActContext](./261026-BrianSamBodden-ActContext/README.md) | What Context Does a Coding Agent Actually Need to Act? | Brian Sam-Bodden | arXiv cs.SE / 2026 | 已精读（完整 arXiv v1 HTML/PDF、附录与代码数据；教学式完整精读） |
| 2026-10-25 | [261025-XiaonanXu-StaleInstructionFiles](./261025-XiaonanXu-StaleInstructionFiles/README.md) | Stale Instruction Files Override the Code in Coding Agents: A One-Sentence Fix | Xiaonan Xu | arXiv cs.SE / 投稿至 SN Computer Science，2026 | 已精读（完整 arXiv v1 HTML/PDF 及附录；教学式完整精读） |
| 2026-10-24 | [261024-SaiyueLyu-InferenceTimeResources](./261024-SaiyueLyu-InferenceTimeResources/README.md) | Where Should a Stuck Agent Spend Its Next Tokens? Causal Attribution of Inference-Time Resources | Saiyue Lyu | Long-Context Foundation Models workshop / arXiv 2026 | 已精读（完整 arXiv v1 HTML/PDF 及附录；教学式完整精读） |
| 2026-10-23 | [261023-YingxinJia-ExperienceMemoryControls](./261023-YingxinJia-ExperienceMemoryControls/README.md) | When Does Experience Memory Help Closed-Loop LLM Driving Agents? A Controlled Evaluation with Resampled Warmup Pools, Token-Matched Fillers, and Audited Baselines | Yingxin Jia | ACML 2026 / PMLR 353 | 已精读（完整 arXiv v1 HTML/PDF；教学式完整精读） |
| 2026-10-22 | [261022-JosephTownsend-FaultLocalizationGranularity](./261022-JosephTownsend-FaultLocalizationGranularity/README.md) | A Study on the Impact of Fault Localization Granularity for Repository-Scale Code Repair Tasks | Joseph Townsend | arXiv cs.SE / 2026 | 已精读（完整 arXiv v1 HTML/PDF 及附录；教学式完整精读） |
| 2026-10-21 | [261021-FredaShi-IrrelevantContext](./261021-FredaShi-IrrelevantContext/README.md) | Large Language Models Can Be Easily Distracted by Irrelevant Context | Freda Shi | ICML 2023 / PMLR 202 | 已精读（完整 arXiv v3 HTML 原文及附录；教学式完整精读） |
| 2026-10-20 | [261020-MohammadRezaalipour-PythonFaultLocalization](./261020-MohammadRezaalipour-PythonFaultLocalization/README.md) | An Empirical Study of Fault Localization in Python Programs | Mohammad Rezaalipour | Empirical Software Engineering 29 / 2024 | 已精读（完整 arXiv v3 HTML 原文；教学式完整精读） |
| 2026-10-19 | [261019-EzekielSoremekun-DebuggingAssumptions](./261019-EzekielSoremekun-DebuggingAssumptions/README.md) | Evaluating the Impact of Experimental Assumptions in Automated Fault Localization | Ezekiel Soremekun | ICSE 2023 Research Track | 已精读（完整作者版 PDF；教学式完整精读） |
| 2026-10-18 | [261018-MohammadNourAlAwad-IssueLocBench](./261018-MohammadNourAlAwad-IssueLocBench/README.md) | Cost-Effective Repository Exploration for Agentic Issue Localization | Mohammad Nour Al Awad | AgenticDev 2026 | 已精读（完整 arXiv v1 PDF；教学式完整精读） |
| 2026-10-17 | [261017-HovhannesTamoyan-SHERLOC](./261017-HovhannesTamoyan-SHERLOC/README.md) | SHERLOC: Structured Diagnostic Localization for Code Repair Agents | Hovhannes Tamoyan | arXiv cs.CL / EMNLP 2026 | 已精读（完整 v2 HTML 原文及附录；教学式完整精读） |
| 2026-10-16 | [261016-ArmanBehnam-CausalMemoryPolicy](./261016-ArmanBehnam-CausalMemoryPolicy/README.md) | Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval | Arman Behnam | arXiv cs.AI / 2026 | 已精读（完整 v3 HTML 原文及附录；教学式完整精读） |
| 2026-10-15 | [261015-AmirkiaRafieiOskooei-DeepAgenticSearch](./261015-AmirkiaRafieiOskooei-DeepAgenticSearch/README.md) | Deep Agentic Search for Repository-Level Code Question Answering: An Empirical Study | Amirkia Rafiei Oskooei | arXiv cs.SE / 2026 | 已精读（完整 v1 PDF；教学式完整精读） |
| 2026-10-14 | [261014-YangzeLiu-HarnessBuy](./261014-YangzeLiu-HarnessBuy/README.md) | What Does a Harness Buy? Tokens, Mostly | Yangze Liu | arXiv cs.AI / cs.LG / cs.SE / 2026 | 已精读（完整 v1 PDF；教学式完整精读） |
| 2026-10-13 | [261013-MinxingWang-Cadence](./261013-MinxingWang-Cadence/README.md) | Cadence: Strategic Guidance for Coding Agents | Minxing Wang | arXiv cs.SE / 2026 | 已精读（完整 v1 PDF；教学式完整精读） |
| 2026-10-12 | [261012-ChaoliangYan-SkillConflict](./261012-ChaoliangYan-SkillConflict/README.md) | One Skill Too Many: How Co-Installed Skills Conflict in Coding Agents | Chaoliang Yan | arXiv cs.SE / cs.AI / 2026 | 已精读（完整 v1 PDF；教学式完整精读） |
| 2026-10-11 | [261011-KaifengHe-RepoNorm](./261011-KaifengHe-RepoNorm/README.md) | Acquiring and Verifying Repository Norms for Coding Agents | Kaifeng He | arXiv cs.SE / 2026 | 已精读（完整 v1 PDF；教学式完整精读） |
| 2026-10-10 | [261010-ZixiaoZhao-LSCR](./261010-ZixiaoZhao-LSCR/README.md) | Empowering Lightweight Language Models for Security Code Review via Context-Aware Distillation | Zixiao Zhao | ISSTA 2026 / Proc. ACM Softw. Eng. 3 | 已精读（完整 ACM PDF；教学式完整精读） |
| 2026-10-09 | [261009-YikunLi-VulContextBench](./261009-YikunLi-VulContextBench/README.md) | VulContextBench: A Benchmark for Security Context Retrieval in Coding Agents | Yikun Li | arXiv cs.CR / 2026 | 已精读（完整 v1 PDF；教学式完整精读） |
| 2026-10-08 | [261008-JiaweiHe-ProcessEvaluation](./261008-JiaweiHe-ProcessEvaluation/README.md) | What Process Evaluation of Coding Agents Actually Measures: Action, Task, and Step Are Three Different Levels | Jiawei He | arXiv cs.AI / 2026 | 已精读（完整 HTML 原文；教学式精读） |
| 2026-10-07 | [261007-JingjieNing-RulesToTools](./261007-JingjieNing-RulesToTools/README.md) | Rules to Tools: Executable Checks for LLM Agents in Scientific Computing | Jingjie Ning | arXiv cs.AI / 2026 | 已精读（完整公开原文；教学式完整精读） |
| 2026-10-06 | [261006-YuqingZhai-VerificationGuidance](./261006-YuqingZhai-VerificationGuidance/README.md) | From Verification Failures to Reusable Guidance for Coding Agents | Yuqing Zhai | arXiv cs.SE / 2026 | 已精读（完整公开原文；教学式完整精读） |
| 2026-10-05 | [261005-JiangruiZhao-HiSentinel](./261005-JiangruiZhao-HiSentinel/README.md) | Learning When and How to Intervene: A Hindsight-Distilled Sentinel for Coding Agents | Jiangrui Zhao | arXiv cs.SE / 2026 | 已精读（完整公开原文；教学式完整精读） |
| 2026-10-04 | [261004-YueXue-ContextRot](./261004-YueXue-ContextRot/README.md) | When and How Context Rot Appears in Coding Agents: A White-Box Study of Agent Skills in Code Auditing | Yue Xue | arXiv cs.SE / 2026 | 已精读（完整公开原文；教学式完整精读） |
| 2026-10-03 | [261003-MatthiasGalster-HarnessEngineering](./261003-MatthiasGalster-HarnessEngineering/README.md) | Harness Engineering for Agentic AI Coding Tools: An Exploratory Study | Matthias Galster | AIware 2026 扩展版 / arXiv v5 | 已精读（完整公开原文；教学式完整精读） |
| 2026-10-02 | [261002-YuePan-CRJudgeBench](./261002-YuePan-CRJudgeBench/README.md) | CRJudgeBench: Can AI Detect Plausible but Invalid Code Reviews? | Yue Pan | arXiv / 2026 | 已精读（完整公开原文；教学式完整精读） |
| 2026-10-01 | [261001-PrakharKhatri-ContextFiles](./261001-PrakharKhatri-ContextFiles/README.md) | Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories | Prakhar Khatri | arXiv / 2026 | 已精读（完整公开原文；教学式完整精读） |
| 2026-09-30 | [260930-WeiLiu-GraphLocator](./260930-WeiLiu-GraphLocator/README.md) | GraphLocator: Graph-guided Causal Reasoning for Issue Localization | Wei Liu | FSE 2026 Research Papers | 已精读（完整公开原文；教学式完整精读） |
| 2026-09-29 | [260929-FangLiu-SecureReviewer](./260929-FangLiu-SecureReviewer/README.md) | SecureReviewer: Enhancing Large Language Models for Secure Code Review through Secure-aware Fine-tuning | Fang Liu | ICSE / 2026 | 已精读（完整公开原文；教学式完整精读） |
| 2026-09-28 | [260928-SeonghyeonCho-SkillFollowing](./260928-SeonghyeonCho-SkillFollowing/README.md) | Skill Following: Evaluating Actual Skill Use in Retrieval-Enabled LLM Agents | Seonghyeon Cho | Findings of EMNLP / 2026 | 已精读（完整公开原文；教学式完整精读） |
| 2026-09-27 | [260927-ZhexiFeng-MissingComplement](./260927-ZhexiFeng-MissingComplement/README.md) | The Missing Complement: State-Conditioned Minimal Sufficient Evidence for Coding Agents | Zhexi Feng | arXiv / 2026 | 已精读（完整公开原文；教学式完整精读） |
| 2026-09-26 | [260926-ShaoqiuZhang-SWEExplore](./260926-ShaoqiuZhang-SWEExplore/README.md) | SWE-Explore: Benchmarking How Coding Agents Explore Repositories | Shaoqiu Zhang | arXiv / 2026 | 已精读（完整公开原文；教学式完整精读） |
| 2026-09-25 | [260925-HanLi-ContextBench](./260925-HanLi-ContextBench/README.md) | ContextBench: A Benchmark for Context Retrieval in Coding Agents | Han Li | arXiv / 2026 | 已精读（完整原文；按教学式完整精读协议重写） |
| 2026-09-24 | [260924-YunxiangZhang-RepoAtlas](./260924-YunxiangZhang-RepoAtlas/README.md) | RepoAtlas: Guiding Coding Agents via Evolving Multimodal Repository Views | Yunxiang Zhang | arXiv / 2026 | 已精读（完整 arXiv v1 HTML 原文） |
| 2026-09-23 | [260923-HaojunWeng-StaleRepositoryContext](./260923-HaojunWeng-StaleRepositoryContext/README.md) | When Retrieval Hurts Code Completion: A Diagnostic Study of Stale Repository Context | Haojun Weng | arXiv / 2026 | 已精读（完整 arXiv v1 原文） |
| 2026-09-22 | [260922-MuhanGao-FirstDropInk](./260922-MuhanGao-FirstDropInk/README.md) | The First Drop of Ink: Nonlinear Impact of Distracting Information in Long-Context Reasoning | Muhan Gao | ICML 2026 | 已精读（完整 arXiv v2 原文） |
| 2026-09-22 | [260922-BowenQin-AgentRetrievalBench](./260922-BowenQin-AgentRetrievalBench/README.md) | Agent Retrieval Bench: Evaluating Repository Context Retrieval for Coding Agents | Bowen Qin | arXiv, 2026 | 已精读（完整公开原文） |
| 2026-09-21 | [260921-YikunLi-CPRVul](./260921-YikunLi-CPRVul/README.md) | Beyond Function-Level Analysis: Context-Aware Reasoning for Inter-Procedural Vulnerability Detection | Yikun Li | arXiv, 2026 | 已精读（完整公开原文） |
| 2026-09-20 | [260920-JingjingWang-LaMR](./260920-JingjingWang-LaMR/README.md) | Context Pruning for Coding Agents via Multi-Rubric Latent Reasoning | Jingjing Wang | arXiv, 2026 | 已精读（完整公开原文） |
| 2026-09-19 | [260919-LeiZhang-HCPCoder](./260919-LeiZhang-HCPCoder/README.md) | Hierarchical Context Pruning: Optimizing Real-World Code Completion with Repository-Level Pretrained Code LLMs | Lei Zhang | AAAI 2025 | 已精读（完整 AAAI 原文） |
| 2026-09-19 | [260919-SiruOuyang-RepoGraph](./260919-SiruOuyang-RepoGraph/README.md) | RepoGraph: Enhancing AI Software Engineering with Repository-level Code Graph | Siru Ouyang | ICLR 2025 | 已精读（完整 ICLR 原文） |
| 2026-09-18 | [260918-MdAjwadAkil-PhantomCall](./260918-MdAjwadAkil-PhantomCall/README.md) | PhantomCall: Evading ML Malware Detectors via Function Call Graph Perturbation | Md Ajwad Akil | arXiv cs.CR, 2026 | 已精读（完整 PDF 原文） |
| 2026-09-18 | [260918-YanlinWang-RepoReasoner](./260918-YanlinWang-RepoReasoner/README.md) | RepoReasoner: Evaluating Repository-Level Code Reasoning Ability of Long-Context Language Models | Yanlin Wang | FSE 2026 / Proc. ACM Softw. Eng. 3 | 已精读（完整公开原文） |
| 2026-09-18 | [260918-ThibaudGloaguen-AgentsMD](./260918-ThibaudGloaguen-AgentsMD/README.md) | Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents? | Thibaud Gloaguen | MemAgents @ ICLR 2026 / arXiv 2026 | 已精读（完整 arXiv v2 原文） |
| 2026-09-17 | [260917-HanyuLi-RepoMirage](./260917-HanyuLi-RepoMirage/README.md) | RepoMirage: Probing Repository Context Reasoning in Code Agents with Perturbations | Hanyu Li | arXiv, 2026 | 已精读（完整 arXiv 原文） |
| 2026-09-16 | [260916-JunyaoYe-CausalCode](./260916-JunyaoYe-CausalCode/README.md) | A Causal Learning Framework for Enhancing Robustness of Source Code Models | Junyao Ye | FSE 2025 / PACMSE 2 | 已精读（原文 PDF） |
| 2026-09-15 | [260915-EduardoOliveira-AIAssistedCodeReview](./260915-EduardoOliveira-AIAssistedCodeReview/README.md) | AI-Assisted Code Review as a Scaffold for Code Quality and Self-Regulated Learning: An Experience Report | Eduardo Oliveira | ICSE-SEET 2026 | 已精读 |
| 2026-09-14 | [260914-HaolinJin-ReliableCodeReviewers](./260914-HaolinJin-ReliableCodeReviewers/README.md) | Are LLMs Reliable Code Reviewers? Systematic Overcorrection in Requirement Conformance Judgement | Haolin Jin | arXiv, 2026 | 已精读 |
| 2026-09-13 | [260913-TingxuHan-SWESkillsBench](./260913-TingxuHan-SWESkillsBench/README.md) | SWE-Skills-Bench: Do Agent Skills Actually Help in Real-World Software Engineering? | Tingxu Han | arXiv, 2026 | 已精读 |
| 2026-09-12 | [260912-RadinShayanfar-AgenticBenchmarkMeasure](./260912-RadinShayanfar-AgenticBenchmarkMeasure/README.md) | What Does an Agentic Software Engineering Benchmark Measure? Profiling Task Demands and Agent Behaviour Beyond What Category Labels Reveal | Radin Shayanfar | arXiv, 2026 | 已精读 |
| 2026-09-11 | [260911-JiaFeng-ContextCompression](./260911-JiaFeng-ContextCompression/README.md) | On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation | Jia Feng | arXiv cs.SE, 2026 | 已精读 |
| 2026-09-10 | [260910-RobertoPietrantuono-CausalSoftwareEngineering](./260910-RobertoPietrantuono-CausalSoftwareEngineering/README.md) | Causal Software Engineering: A Vision and Roadmap | Roberto Pietrantuono | FSE 2026 Ideas, Visions and Reflections | 已精读 |
| 2026-09-08 | [260908-RatnadiraWidyasari-ExplainingExplanations](./260908-RatnadiraWidyasari-ExplainingExplanations/README.md) | Explaining Explanations: An Empirical Study of Explanations in Code Reviews | Ratnadira Widyasari | ACM TOSEM 34(6), Article 177, 2025 | 已精读 |
| 2026-09-07 | [260907-AsifTurzo-UsefulCodeReview](./260907-AsifTurzo-UsefulCodeReview/README.md) | What Makes a Code Review Useful to OpenDev Developers? An Empirical Investigation | Asif Kamal Turzo | Empirical Software Engineering 29(1):6, 2024 / FSE 2024 Journal First | 已精读 |
| 2026-09-06 | [260906-SupritiVijay-AntaresVLocBench](./260906-SupritiVijay-AntaresVLocBench/README.md) | Antares: Foundation Models for Agentic Vulnerability Localization | Supriti Vijay | Cisco Foundation AI Technical Report, 2026 | 已精读 |
| 2026-09-04 | [260904-ZixiaoZhao-SeRe](./260904-ZixiaoZhao-SeRe/README.md) | SeRe: A Security-Related Code Review Dataset Aligned with Real-World Review Activities | Zixiao Zhao | ICSE 2026 | 已精读 |
| 2026-09-03 | [260903-DewuZheng-MCRBench](./260903-DewuZheng-MCRBench/README.md) | From Static to Dynamic: Benchmarking Real-World Code Review with MCR-Bench | Dewu Zheng | ISSTA 2026 / Proceedings of the ACM on Software Engineering 3 | 已精读 |
| 2026-09-02 | [260902-DongWang-CodeReviewBenchmarking](./260902-DongWang-CodeReviewBenchmarking/README.md) | Can We Benchmark Code Review Studies? A Systematic Mapping Study of Methodology, Dataset, and Metric | Dong Wang | Journal of Systems and Software 180, 2021 | 已精读 |
| 2026-09-01 | [260901-MairieliWessel-QualityGatekeepers](./260901-MairieliWessel-QualityGatekeepers/README.md) | Quality Gatekeepers: Investigating the Effects of Code Review Bots on Pull Request Activities | Mairieli Wessel | Empirical Software Engineering 27:108, 2022 | 已精读 |
| 2026-08-31 | [260831-KlaTantithamthavorn-RovoDev](./260831-KlaTantithamthavorn-RovoDev/README.md) | RovoDev Code Reviewer: A Large-Scale Online Evaluation of LLM-based Code Review Automation at Atlassian | Kla Tantithamthavorn | ICSE-SEIP 2026 | 已精读 |
| 2026-08-30 | [260830-PavlinaGoncalves-CodeReviewComprehension](./260830-PavlinaGoncalves-CodeReviewComprehension/README.md) | Code Review Comprehension: Reviewing Strategies Seen Through Code Comprehension Theories | Pavlína Wurzel Gonçalves | ICPC 2025 | 已精读 |
| 2026-08-29 | [260829-NehaSingh-ComplexityAndProvenance](./260829-NehaSingh-ComplexityAndProvenance/README.md) | The Effect of Complexity and Provenance on Code Review Decisions: Evidence from a Controlled Experiment | Neha Singh | FSE 2026 / Proceedings of the ACM on Software Engineering 3 | 已精读 |
| 2026-08-28 | [260828-KaustuvMukherji-EntailLLM](./260828-KaustuvMukherji-EntailLLM/README.md) | EntailLLM: Verifying LLM-Generated Vulnerability Discovery Paths with Domain Knowledge via Logic Programming | Kaustuv Mukherji | arXiv, 2026 | 已精读 |
| 2026-08-27 | [260827-MingyangSun-DREA](./260827-MingyangSun-DREA/README.md) | DREA: Decoupled Reasoning and Exploration Agents for Repository-Level Vulnerability Detection | Mingyang Sun | Internetware 2026 / arXiv 2026 | 已精读 |
| 2026-08-26 | [260826-LeiZhang-AACRBench](./260826-LeiZhang-AACRBench/README.md) | AACR-Bench: Evaluating Automatic Code Review with Holistic Repository-Level Context | Lei Zhang | arXiv, 2026 | 已精读 |
| 2026-08-25 | [260825-ZhengfengLi-OpenCodeReview](./260825-ZhengfengLi-OpenCodeReview/README.md) | OpenCodeReview: Determinism over Non-Determinism for Cost-Effective Agent-Based Code Review | Zhengfeng Li | arXiv, 2026 | 已精读 |
| 2026-08-24 | [260824-ReshmaRoychoudhuri-DeveloperFamiliarity](./260824-ReshmaRoychoudhuri-DeveloperFamiliarity/README.md) | Does Developer Familiarity Hasten Bug Resolution? A Causal Inference Perspective | Reshma Roychoudhuri | Empirical Software Engineering 31:111, 2026 | 已精读 |
| 2026-08-23 | [260823-LukasSchulte-BugIntroducingChanges](./260823-LukasSchulte-BugIntroducingChanges/README.md) | An Exploratory Study of Bug-Introducing Changes: Exploring Relationships in Bug-Introducing Changes Towards Causal Understanding | Lukas Schulte | Empirical Software Engineering 31:114, 2026 | 已精读 |
| 2026-08-19 | [260819-MairieliWessel-QualityGatekeepers](./260819-MairieliWessel-QualityGatekeepers/README.md) | Quality Gatekeepers: Investigating the Effects of Code Review Bots on Pull Request Activities | Mairieli Wessel | Empirical Software Engineering, 2022 | 已精读 |
| 2026-08-10 | [260810-PavlinaGoncalves-ExplicitReviewStrategies](./260810-PavlinaGoncalves-ExplicitReviewStrategies/README.md) | Do Explicit Review Strategies Improve Code Review Performance? Towards Understanding the Role of Cognitive Load | Pavlína Wurzel Gonçalves | Empirical Software Engineering 27(4), 2022 | 已精读 |
| 2026-08-07 | [260807-CarloFuria-OmittedVariableBias](./260807-CarloFuria-OmittedVariableBias/README.md) | Mitigating Omitted Variable Bias in Empirical Software Engineering | Carlo A. Furia | Empirical Software Engineering, 2026 | 已精读 |
| 2026-08-06 | [260806-ShyamAgarwal-3100Opinions](./260806-ShyamAgarwal-3100Opinions/README.md) | 3100 Opinions on Code Review in an AI World: Building Causal Theory from Practitioner Discourse | Shyam Agarwal | arXiv, 2026 | 已精读 |
| 2026-08-03 | [260803-ChengranYang-ThinkLikeHumanDevelopers](./260803-ChengranYang-ThinkLikeHumanDevelopers/README.md) | Think Like Human Developers: Harnessing Community Knowledge for Structured Code Reasoning | Chengran Yang | ICSE 2026 Research Track | 已精读 |

## 待读

| 计划日期 | 论文 | 来源 | 优先级 | 选择原因 |
|---|---|---|---|---|
| — | 暂无已排期论文 | GitHub Paper Pool | — | RepoGraph 与 HCP-Coder 均已于 2026-09-19 完成精读。 |

## 维护规则

- 每次完整精读对应一个目录，正文统一使用 `README.md`。
- 选题去重优先级为 DOI > arXiv ID > 规范化标题；明确重读时保留不同日期的历史版本。
- 公开笔记不得依赖本地 Zotero、个人电脑路径或任务记忆；身份与状态以 GitHub 仓库当前内容为准。
- 笔记必须区分论文报告的事实、基于证据的推断和仍待验证的判断。
- 每次精读应覆盖动机、方法链路、研究问题、实验设计、重要图表、证据边界和后续研究机会。
- 每次发布同时更新论文池、精读索引和精读正文，再 commit 并 push 到 `master`。



