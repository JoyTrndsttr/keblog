# Paper Pool · 2026-10

> 2026 年 10 月完整精读记录。当前月份每日精读只需读取本文件；跨月永久去重读取 `paperpool_short.md`。

## 已精读论文

### 2026-10-29

- **Sufficient Context: A New Lens on Retrieval Augmented Generation Systems**
  - 简称：[Sufficient Context](https://38-76-161-31.sslip.io/daily-learning/?paper=261029-HaileyJoren-SufficientContext)
  - Tags：`ICLR 2025` `RAG` `Context Sufficiency` `AutoRater` `Hallucination` `Abstention` `Selective Generation` `Evidence Utility`
  - 作者：Hailey Joren; Jianyi Zhang; Chun-Sung Ferng; Da-Cheng Juan; Ankur Taly; Cyrus Rashtchian（UC San Diego、Duke University、Google；原文与 OpenReview 均未单独标注通讯作者）
  - Venue / 年份：ICLR 2025
  - DOI / 原文：[arXiv:2411.06037](https://arxiv.org/abs/2411.06037); [Google Research](https://research.google/pubs/sufficient-context-a-new-lens-on-retrieval-augmented-generation-systems-2/); [完整 HTML](https://arxiv.org/html/2411.06037v2); [PDF](https://arxiv.org/pdf/2411.06037); [OpenReview](https://openreview.net/forum?id=Jjr2Odj8DJ)
  - 主题：RAG 上下文充分性、人工标注与 AutoRater、分层错误分析、拒答与幻觉、选择性生成、上下文增量价值
  - 一句话价值：论文把“检索内容是否相关”推进到“上下文是否足以回答”，并在 FreshQA、Musique、HotpotQA 上按充分性拆解正确、拒答与幻觉；结果显示长上下文提升充分率但存在收益饱和，不充分上下文仍可能因预训练记忆或局部证据答对，而充分性标签配合模型自信能提高选择性生成准确率，直接提示当前成功/失败轨迹审计应把上下文充分性、增量信息价值与模型决策效应分层记录。

### 2026-10-26

- **What Context Does a Coding Agent Actually Need to Act?**
  - 简称：[Act Context](https://38-76-161-31.sslip.io/daily-learning/?paper=261026-BrianSamBodden-ActContext)
  - Tags：`2026` `arXiv` `Coding Agent` `Repository Context` `Find/Act Boundary` `Context Compression` `SWE-bench Verified` `Pre-registration`
  - 作者：Brian Sam-Bodden（Integrallis Software；单作者；原文未单独标注通讯作者，并提供作者邮箱）
  - Venue / 年份：arXiv cs.SE v1，2026
  - DOI / 原文：[arXiv:2607.09691](https://arxiv.org/abs/2607.09691); [完整 HTML](https://arxiv.org/html/2607.09691v1); [PDF](https://arxiv.org/pdf/2607.09691); [代码与数据](https://github.com/integrallis/act-context)
  - 主题：编码代理仓库上下文、Find/Act 边界、oracle 定位、代码表示、上下文压缩、可编辑性审计、运行噪声
  - 一句话价值：在固定 gold 文件和可编辑位置的 70 个多文件 SWE-bench Verified 任务中，保留目标正文并删除外围代码以约 6.9k 平均 token 解决 25/70，结构摘要臂以约 8.6k token 解决 23/70，二者无显著差异；相同 temperature 0 输入重跑仍有 6/70 翻转，直接提示当前 P/I 研究必须把候选扩张与参考正文拆开，并先审计各臂可答性与相同输入噪声底。

### 2026-10-25

- **Stale Instruction Files Override the Code in Coding Agents: A One-Sentence Fix**
  - 简称：[Stale Instruction Files](https://38-76-161-31.sslip.io/daily-learning/?paper=261025-XiaonanXu-StaleInstructionFiles)
  - Tags：`2026` `arXiv` `Coding Agent` `Instruction Files` `AGENTS.md` `CLAUDE.md` `Context Conflict` `Instruction Hierarchy`
  - 作者：Xiaonan Xu; Wenjing Wu（原文未明确标注通讯作者）
  - Venue / 年份：arXiv cs.SE v1 / 投稿至 SN Computer Science，2026
  - DOI / 原文：[arXiv:2610.30571](https://arxiv.org/abs/2610.30571); [完整 HTML](https://arxiv.org/html/2610.30571v1); [PDF](https://arxiv.org/pdf/2610.30571); [数据与代码](https://github.com/WenJing95/stale-docs-data)
  - 主题：编码代理说明文件、过期上下文、指令层级、代码惯例冲突、旧代码重写、上下文权威
  - 一句话价值：在 40 个合成 Python 项目、Claude Code 与 Codex CLI 的 320 次运行中，代理无干预时 90.1% 的具体选择服从过期说明；一条“文档与代码冲突时以现有代码为准”的用户级规则把代码一致选择提升到 91.4%，并让 Codex 的旧代码重写从 20 次降至 0，提示当前 P/I 实验除相关性与覆盖率外还必须控制上下文的注入层级与权威。

### 2026-10-24

- **Where Should a Stuck Agent Spend Its Next Tokens? Causal Attribution of Inference-Time Resources**
  - 简称：[Inference-Time Resources](https://38-76-161-31.sslip.io/daily-learning/?paper=261024-SaiyueLyu-InferenceTimeResources)
  - Tags：`2026` `arXiv` `Coding Agent` `Inference-time Resources` `Causal Attribution` `Full Factorial` `Banzhaf Value` `SWE-bench Verified`
  - 作者：Saiyue Lyu（通讯作者）; Jerrold Huang; Yunbei Zhang; Janet Wang; Zhenting Wang; Yingqiang Ge; Haibo Zhang
  - Venue / 年份：Long-Context Foundation Models workshop / arXiv cs.SE 预印本，2026
  - DOI / 原文：[arXiv:2610.28834](https://arxiv.org/abs/2610.28834); [完整 HTML](https://arxiv.org/html/2610.28834v1); [PDF](https://arxiv.org/pdf/2610.28834)
  - 主题：代码代理推理时资源、冻结失败检查点、完整析因设计、Banzhaf 归因、仓库上下文、资源分配
  - 一句话价值：在 194 个函数级与 126 个 SWE-bench Verified 冻结失败上穷举计算/信息/反馈的 8 种组合后，参考修复导出的任务规格仍带来 0.05–0.14 的稳定收益，而公开测试反馈与五段 BM25 代码近零；这为当前 P/I 实验提供了“location × behaviour”拆分、固定状态归因及漏报/过度定位双结局的直接方法模板。

### 2026-10-23

- **When Does Experience Memory Help Closed-Loop LLM Driving Agents? A Controlled Evaluation with Resampled Warmup Pools, Token-Matched Fillers, and Audited Baselines**
  - 简称：[Experience Memory Controls](https://38-76-161-31.sslip.io/daily-learning/?paper=261023-YingxinJia-ExperienceMemoryControls)
  - Tags：`2026` `ACML` `LLM Agent` `Experience Memory` `Closed-loop Driving` `Controlled Evaluation` `Warmup Pool` `Token-matched Filler`
  - 作者：Yingxin Jia; Xuanyi Li（独立研究者；原文未明确标注通讯作者）
  - Venue / 年份：ACML 2026 / Proceedings of Machine Learning Research 353
  - DOI / 原文：[arXiv:2610.27714](https://arxiv.org/abs/2610.27714); [完整 HTML](https://arxiv.org/html/2610.27714v1); [PDF](https://arxiv.org/pdf/2610.27714)
  - 主题：闭环 LLM 驾驶代理经验记忆、热身池重采样、等 token 无关填充、谨慎行为定价、基线移植审计
  - 一句话价值：在固定规划器的 HighwayEnv 测试台上，两种检索记忆仅在 10 个热身池中的 1 个胜过无记忆，十池平均效应约为 −0.20；1,037-token 无关填充反而达到 0.80，且 15-token 谨慎指令即可达到 0.98，说明池抽样、提示组成与行为倾向足以反转“记忆有效”的单池结论，为当前共享 donor、固定总长度和 oracle-context 实验提供直接的机制鉴别先例。

### 2026-10-22

- **A Study on the Impact of Fault Localization Granularity for Repository-Scale Code Repair Tasks**
  - 简称：[Fault Localization Granularity](https://38-76-161-31.sslip.io/daily-learning/?paper=261022-JosephTownsend-FaultLocalizationGranularity)
  - Tags：`2026` `arXiv` `Fault Localization` `Automated Program Repair` `Granularity` `Perfect Localization` `SWE-bench` `Qwen3-Coder`
  - 作者：Joseph Townsend*; Chandresh Pravin*; Kwun Ho Ngan*; Matthieu Parizy（*原文标注共同贡献；原文未明确标注通讯作者）
  - Venue / 年份：arXiv cs.SE 预印本 / 2026，v1
  - DOI / 原文：[arXiv:2604.00167](https://arxiv.org/abs/2604.00167); [HTML](https://arxiv.org/html/2604.00167v1); [PDF](https://arxiv.org/pdf/2604.00167)
  - 主题：仓库级故障定位粒度、oracle / perfect localization、定位—修复交接、上下文呈现、任务异质性
  - 一句话价值：在 SWE-bench Mini 50 题上固定 Qwen3-Coder 与修复提示，只改变由真实补丁构造的行/函数/文件级上下文，函数级平均解决率为 45.6%，略高于行级 43.6% 与文件级 42.6%；更重要的是最高仍不足一半且分难度排序变化，为当前“语义对象 GT—呈现 envelope—下游成功”拆分和预算匹配干预提供了 proof of concept，而非函数级普遍最优的证据。

### 2026-10-21

- **Large Language Models Can Be Easily Distracted by Irrelevant Context**
  - 简称：[Irrelevant Context](https://38-76-161-31.sslip.io/daily-learning/?paper=261021-FredaShi-IrrelevantContext)
  - Tags：`2023` `ICML` `LLM` `Irrelevant Context` `Robustness` `Prompting` `Controlled Intervention`
  - 作者：Freda Shi; Xinyun Chen; Kanishka Misra; Nathan Scales; David Dohan; Ed H. Chi; Nathanael Schärli; Denny Zhou（原文明确列出 Freda Shi、Xinyun Chen、Denny Zhou 为 correspondence contacts；前两位等贡献）
  - Venue / 年份：ICML 2023 / PMLR 202
  - DOI / 原文：[PMLR](https://proceedings.mlr.press/v202/shi23a.html); [arXiv:2302.00093](https://arxiv.org/abs/2302.00093); [完整 HTML](https://arxiv.org/html/2302.00093v3); [数据集](https://github.com/google-research-datasets/GSM-IC)
  - 主题：大模型无关上下文鲁棒性、配对输入干预、micro/macro 一致性、prompting、Self-Consistency
  - 一句话价值：作者固定 100 道模型至少能用一种方法解出的 GSM8K 题，只改变一条不影响答案的干扰句；4,000 个派生样本显示所有 prompting 方法都会退化，且“同主题+实体重叠”的伪相关干扰最危险，为当前 C/P/I 配对干预、clean-success 条件估计和跨变体稳定性指标提供了干净机制先例，但不能替代真实仓库证据。

### 2026-10-20

- **An Empirical Study of Fault Localization in Python Programs**
  - 简称：[Python Fault Localization](https://38-76-161-31.sslip.io/daily-learning/?paper=261020-MohammadRezaalipour-PythonFaultLocalization)
  - Tags：`2024` `EMSE` `Fault Localization` `Python` `BugsInPy` `Ground Truth` `Granularity` `Empirical Study`
  - 作者：Mohammad Rezaalipour; Carlo A. Furia（原文未明确标注通讯作者）
  - Venue / 年份：Empirical Software Engineering 29, Article 92 / 2024
  - DOI / 原文：[10.1007/s10664-024-10475-3](https://doi.org/10.1007/s10664-024-10475-3); [arXiv:2305.19834](https://arxiv.org/abs/2305.19834); [HTML](https://arxiv.org/html/2305.19834v3); [复现材料](https://doi.org/10.6084/m9.figshare.23254688)
  - 主题：Python 故障定位、语句/函数/模块粒度、补丁 ground truth、适用子群、证据组合与成本—效果权衡
  - 一句话价值：对 BugsInPy 的 135 个真实缺陷比较四类七种技术发现，SBFL 是最有效的通用单独家族，组合方法进一步提高 Top-k 但扩大候选与成本；SBFL 的 Top-1 从语句级 12% 升至函数级 37%、模块级 60%主要来自答案空间折叠，直接支持当前将函数节点作为交付单位但禁止与旧行分数横比。

### 2026-10-19

- **Evaluating the Impact of Experimental Assumptions in Automated Fault Localization**
  - 简称：[Debugging Assumptions](https://38-76-161-31.sslip.io/daily-learning/?paper=261019-EzekielSoremekun-DebuggingAssumptions)
  - Tags：`2023` `ICSE` `Automated Fault Localization` `Ground Truth` `Construct Validity` `Automated Program Repair` `Developer Study`
  - 作者：Ezekiel Soremekun; Lukas Kirschner; Marcel Böhme; Mike Papadakis（原文未明确标注通讯作者）
  - Venue / 年份：ICSE 2023 Research Track
  - DOI / 原文：[10.1109/ICSE48619.2023.00025](https://doi.org/10.1109/ICSE48619.2023.00025); [作者版 PDF](https://mboehme.github.io/paper/ICSE23-debug-assumptions.pdf); [复现材料](https://debugging-assumptions.github.io/)
  - 主题：故障定位构念效度、补丁位置与根因、首命中假设、多位置诊断、AFL/APR 交接与开发者偏好
  - 一句话价值：对 63 篇论文、352 个 C bug、19 种 AFL 配置、2 个 APR 工具和 76 名参与者的研究表明，首个故障位置、fix=root-cause 与单位置假设会把 AFL 测得有效性平均抬高约 13%、最高 38%，同时让 APR 的可修复数被低估；对当前研究的直接要求是把 mechanism gold、repair footprint 与 actionable entry 分开。

### 2026-10-18

- **Cost-Effective Repository Exploration for Agentic Issue Localization**
  - 简称：[IssueLoc-Bench](https://38-76-161-31.sslip.io/daily-learning/?paper=261018-MohammadNourAlAwad-IssueLocBench)
  - Tags：`2026` `AgenticDev` `Repository Exploration` `Issue Localization` `Coding Agent` `Handoff Contract` `Cost` `SWE-bench Verified`
  - 作者：Mohammad Nour Al Awad*; Sergey Ivanov（*原文作者栏以信封符号标注通讯作者）
  - Venue / 年份：AgenticDev 2026
  - DOI / 原文：[10.1145/3843282.3844422](https://doi.org/10.1145/3843282.3844422); [arXiv:2608.29675](https://arxiv.org/abs/2608.29675); [PDF](https://arxiv.org/pdf/2608.29675); [代码与数据](https://github.com/mohammad-nour-alawad/IssueLoc-bench)
  - 主题：修复前仓库探索、文件级问题定位、软/硬交接契约、质量—成本 Pareto、失败升级与仓库聚类不确定性
  - 一句话价值：IssueLoc-Bench 将修复前探索拆成独立阶段；Qwen3-30B-A3B 在 SWE-bench 衍生任务上保留 GLM-4.7-Flash 约 89% Hit@3、92% F1，同时减少约 95% token，但论文未接固定 repairer 验证端到端效果，核心结论是先按可恢复候选或硬门禁定义 handoff contract，再选择指标与模型。

### 2026-10-17

- **SHERLOC: Structured Diagnostic Localization for Code Repair Agents**
  - 简称：[SHERLOC](https://38-76-161-31.sslip.io/daily-learning/?paper=261017-HovhannesTamoyan-SHERLOC)
  - Tags：`2026` `arXiv` `Code Localization` `Code Repair Agent` `Diagnostic Context` `Repository Exploration` `SWE-bench Verified` `Chunk Coverage` `Negative Transfer`
  - 作者：Hovhannes Tamoyan; Sean Narenthiran; Erik Arakelyan; Mira Mezini; Boris Ginsburg（原文未明确标注通讯作者）
  - Venue / 年份：arXiv cs.CL / EMNLP 2026，v2
  - DOI / 原文：[arXiv:2606.24820](https://arxiv.org/abs/2606.24820); [HTML](https://arxiv.org/html/2606.24820v2); [PDF](https://arxiv.org/pdf/2606.24820); [代码与配方](https://github.com/NVIDIA-NeMo/Skills/tree/main/recipes/sherloc)
  - 主题：仓库级故障定位、行块覆盖、结构化诊断、下游修复迁移、自恢复、负迁移与 token 成本
  - 一句话价值：SHERLOC 把定位输出从文件名扩展为行块与五字段诊断，在 SWE-bench Verified 达到 81.27% file recall@1，并在多数 repair-agent 设置中提升修复率且平均减少 36.7% 定位 token；但正确文件内完整/不完整关键块覆盖仍对应 22.6pp 修复差距，错误 finding 还会让强模型下降 4–5pp。

### 2026-10-16

- **Causal Memory Policy: Making Memory Utility Identifiable by Intervening on Retrieval**
  - 简称：[Causal Memory Policy](https://38-76-161-31.sslip.io/daily-learning/?paper=261016-ArmanBehnam-CausalMemoryPolicy)
  - Tags：`2026` `arXiv` `Causal Inference` `LLM Memory` `Retrieval` `Positivity` `Mediation` `Randomized Exposure` `Inverse Propensity Weighting` `Context Attribution`
  - 作者：Arman Behnam; Binghui Wang（原文未明确标注通讯作者）
  - Venue / 年份：arXiv cs.AI / 2026，v3
  - DOI / 原文：[arXiv:2610.02070](https://arxiv.org/abs/2610.02070); [HTML](https://arxiv.org/html/2610.02070v3); [PDF](https://arxiv.org/pdf/2610.02070)
  - 主题：LLM 长期记忆、检索中介、正值性、因果效用识别、平衡随机暴露、不可逆决策
  - 一句话价值：论文指出只在存储层加入或删除记忆无法识别从未被检索的候选效用；CMP 以已知倾向概率随机暴露候选，把 LongMemEval 上必要/非必要记忆区分 AUC 从 0.542 提高到 0.664，但逐查询效用无法预测未来未知查询，因此解决的是测量识别而非长期保留策略。

### 2026-10-15

- **Deep Agentic Search for Repository-Level Code Question Answering: An Empirical Study**
  - 简称：[Deep Agentic Search](https://38-76-161-31.sslip.io/daily-learning/?paper=261015-AmirkiaRafieiOskooei-DeepAgenticSearch)
  - Tags：`2026` `arXiv` `Repository-Level Code QA` `Semantic Search` `Deep Agentic Search` `Subagent` `Failure Taxonomy` `Context Engineering` `Cost`
  - 作者：Amirkia Rafiei Oskooei; Bora Ilci; Alperen Kayim; Mehmet Egemen Uzun; Berat Can; Kaan Emre Kara; Ozan Orhan; Mehmet S. Aktas（原文未明确标注通讯作者）
  - Venue / 年份：arXiv cs.SE / 2026，v1
  - DOI / 原文：[arXiv:2608.01507](https://arxiv.org/abs/2608.01507); [PDF](https://arxiv.org/pdf/2608.01507); [HTML](https://arxiv.org/html/2608.01507v1)
  - 主题：仓库级代码问答、语义检索、子 Agent 委派搜索、上下文交接、失败机制、成本—准确率权衡
  - 一句话价值：在 SWE-QA 的 15 个 Python 仓库、4 个模型和每条件 720 个问题上，语义检索总体 Pass 为 65.2%、委派式 Deep Agentic 搜索为 46.2%，每个正确答案成本约 0.32 对 0.74 美元；Deep 失败中 41.8% 来自主 Agent 与子 Agent 协调断裂，且 91% 仍输出流畅答案，但系统 bundle、预算不匹配和单次运行限制了纯搜索策略因果结论。

### 2026-10-14

- **What Does a Harness Buy? Tokens, Mostly**
  - 简称：[Harness Buy](https://38-76-161-31.sslip.io/daily-learning/?paper=261014-YangzeLiu-HarnessBuy)
  - Tags：`2026` `arXiv` `Coding Agent` `Harness Engineering` `SWE-bench Verified` `Evaluation Noise` `Paired Experiment` `Cost`
  - 作者：Yangze Liu; Zhongyi Han*（*通讯作者）
  - Venue / 年份：arXiv cs.AI / cs.LG / cs.SE / 2026，v1
  - DOI / 原文：[arXiv:2610.04433](https://arxiv.org/abs/2610.04433); [PDF](https://arxiv.org/pdf/2610.04433); [代码与数据](https://github.com/YangzeLiu/what-does-a-harness-buy)
  - 主题：coding-agent harness 对照、任务级重跑噪声、配对等效性、统计功效、失败恢复与 token 成本分解
  - 一句话价值：在 SWE-bench Verified 上，45 个最难任务中换 harness 与原配置重跑的中位任务翻转率同为 13%，而约 447 个配对任务才足以把 Claude Code 与 mini-SWE-agent 界定为 ±5pp 内等效；harness 仍会通过恢复和上下文策略改变失败路径，并让同模型账单相差最高约 3 倍。

### 2026-10-13

- **Cadence: Strategic Guidance for Coding Agents**
  - 简称：[Cadence](https://38-76-161-31.sslip.io/daily-learning/?paper=261013-MinxingWang-Cadence)
  - Tags：`2026` `arXiv` `Coding Agent` `Runtime Monitor` `Trajectory` `Adaptive Scheduling` `Intervention` `SWE-bench Lite`
  - 作者：Minxing Wang; He Ye; Earl T. Barr; Yintong Huo（原文未标明通讯作者）
  - Venue / 年份：arXiv cs.SE / 2026，v1
  - DOI / 原文：[arXiv:2610.12269](https://arxiv.org/abs/2610.12269); [PDF](https://arxiv.org/pdf/2610.12269); [代码与结果](https://github.com/LogAnalysisTech/Cadence)
  - 主题：coding-agent 运行时监控、两级预执行干预、自适应检查调度、轨迹健康与 token efficiency
  - 一句话价值：在 300 个 SWE-bench Lite 任务上，Cadence 将 mini-swe-agent / Moatless 相对 Vanilla 的解决率提高 25.33 / 15.67pp；相近 token 预算下动态调度比固定 7 步高 9pp，但状态代理未独立校准、单次运行与单一 Python benchmark 限制了因果和外部效度。

### 2026-10-12

- **One Skill Too Many: How Co-Installed Skills Conflict in Coding Agents**
  - 简称：[Skill Conflict](https://38-76-161-31.sslip.io/daily-learning/?paper=261012-ChaoliangYan-SkillConflict)
  - Tags：`2026` `arXiv` `Coding Agent` `Agent Skills` `Skill Conflict` `Instruction Fidelity` `Controlled Experiment` `PreToolUse Hook`
  - 作者：Chaoliang Yan; Zihao Xu; Yuekang Li; Shangzhi Xu; Yi Liu; Gelei Deng; Siqi Ma（原文未标明通讯作者）
  - Venue / 年份：arXiv cs.SE / cs.AI / 2026，v1
  - DOI / 原文：[arXiv:2610.11647](https://arxiv.org/abs/2610.11647); [PDF](https://arxiv.org/pdf/2610.11647); [复现包](https://github.com/ltroin/conflict)
  - 主题：Agent Skill 共装冲突、独占核心功能、技能路由、安装 scope、首次读取干预与过程忠实度
  - 一句话价值：在 312 对真实相似技能、6,368 次运行中，相似技能让目标技能使用率下降 19.9pp、独占核心功能忠实度下降 5.6pp，而任务完成率不降；首次读取 guard 可恢复忠实度，说明“任务成功”会系统漏掉指导替换。

### 2026-10-11

- **Acquiring and Verifying Repository Norms for Coding Agents**
  - 简称：[RepoNorm](https://38-76-161-31.sslip.io/daily-learning/?paper=261011-KaifengHe-RepoNorm)
  - Tags：`2026` `arXiv` `Coding Agent` `Repository Norms` `Repository Context` `Instruction Files` `Specification Mining` `Compliance`
  - 作者：Kaifeng He; Xiaojun Zhang; Zhenxi Chen; Christoph Treude; Mingwei Liu*（*通讯作者）
  - Venue / 年份：arXiv cs.SE / 2026，v1
  - DOI / 原文：[arXiv:2610.07757](https://arxiv.org/abs/2610.07757); [PDF](https://arxiv.org/pdf/2610.07757); [代码与数据](https://github.com/SYSUSELab/RepoNorm)
  - 主题：仓库规范获取、显式与隐式规则、适用性验证、Coding Agent 规范遵从与功能正确性
  - 一句话价值：RepoNorm 将规则、作用域、条件、例外和证据打包给 Agent，在 121 个任务上将总体规范遵从率相对提高 7.42%—10.77%、贡献规范遵从率提高 31.64%—45.44%；但功能成功差异经多重校正后不显著，默认高精度视图完整覆盖仅 21.88%，且编码 token 相对 Raw 增加 33.65%。

### 2026-10-10

- **Empowering Lightweight Language Models for Security Code Review via Context-Aware Distillation**
  - 简称：[LSCR](https://38-76-161-31.sslip.io/daily-learning/?paper=261010-ZixiaoZhao-LSCR)
  - Tags：`2026` `ISSTA` `Security Code Review` `Lightweight LLM` `Knowledge Distillation` `Repository Context` `Chain-of-Thought`
  - 作者：Zixiao Zhao; Yanjie Jiang*; Hui Liu; Lu Zhang*（*通讯作者）
  - Venue / 年份：ISSTA 2026 / Proceedings of the ACM on Software Engineering 3
  - DOI / 原文：[10.1145/3832293](https://doi.org/10.1145/3832293); [复现包](https://github.com/caagc/LSCR)
  - 主题：面向安全代码评审的仓库上下文检索、结构化推理轨迹蒸馏与轻量语言模型
  - 一句话价值：LSCR 把“证据—静态分析式推理—结论”蒸馏给三个 6.7B/7B 学生；相对 SecureReviewer，人工评价中 instrumental 评论最高相对提升 52.6%、misleading 评论最高相对下降 22.6%，但大模型仅添加上下文并不稳定受益，推理轨迹也未被独立验证。

### 2026-10-09

- **VulContextBench: A Benchmark for Security Context Retrieval in Coding Agents**
  - 简称：[VulContextBench](https://38-76-161-31.sslip.io/daily-learning/?paper=261009-YikunLi-VulContextBench)
  - Tags：`2026` `arXiv` `Security Code Review` `Coding Agent` `Context Retrieval` `Evidence Selection` `Benchmark` `Role Attribution`
  - 作者：Yikun Li*; Jinfeng Jiang*; Yieh Yuheng; Ting Zhang; Yide Yin; Leow Wen Bin; Eng Lieh Ouh; Lwin Khin Shar; David Lo（*共同贡献；原文未标明通讯作者）
  - Venue / 年份：arXiv cs.CR / 2026，v1
  - DOI / 原文：[arXiv:2609.32601v1](https://arxiv.org/abs/2609.32601v1); [PDF](https://arxiv.org/pdf/2609.32601v1); [代码与数据](https://github.com/yikun-li/vul-context-bench)
  - 主题：人工审计漏洞引入提交、两阶段安全证据检索、多粒度覆盖、四类证据角色与最终引用质量
  - 一句话价值：111 个审计 VIC、464 个角色块揭示七模型探索到的 gold 与最终声明之间约 37—73pp 的块召回缺口；位置与角色错误可拆开，但覆盖评分不证明证据真实因果贡献，27.0%→75.1% 的总体 gold 验证也不认证每例最小充分。


### 2026-10-08

- **What Process Evaluation of Coding Agents Actually Measures: Action, Task, and Step Are Three Different Levels**
  - 简称：[Process Evaluation](https://38-76-161-31.sslip.io/daily-learning/?paper=261008-JiaweiHe-ProcessEvaluation)
  - Tags：`2026` `arXiv` `Coding Agent` `Causal Inference` `Process Evaluation` `Trajectory` `Collider Bias`
  - 作者：Jiawei He; Mengyu Shi; Jie Jia; Xikai Yang*; Dong Sun*（*通讯作者）
  - Venue / 年份：arXiv cs.AI / 2026
  - DOI / 原文：[arXiv:2608.22960](https://arxiv.org/abs/2608.22960)
  - 主题：Agent 过程评估与因果归因
  - 一句话价值：同轨迹不同信息集导致评审者归因偏移，语义相关性不等于因果贡献。


### 2026-10-07

- **Rules to Tools: Executable Checks for LLM Agents in Scientific Computing**
  - 简称：[Rules to Tools](https://38-76-161-31.sslip.io/daily-learning/?paper=261007-JingjieNing-RulesToTools)
  - Tags：`2026` `arXiv` `Coding Agent` `Scientific Computing` `Executable Check` `Tool Use` `SciCode` `Verification`
  - 作者：Jingjie Ning*; Guojiang Zhao; Chen Xu; Shanshan Zhong; Xiaochuan Li; Ji Zeng; Guolin Ke*
  - Venue / 年份：arXiv cs.AI / 2026
  - DOI / 原文：[arXiv:2610.00313](https://arxiv.org/abs/2610.00313); [PDF](https://arxiv.org/pdf/2610.00313)
  - 主题：科学计算 coding-agent、公开规则可执行化、prepared checker、SciCode/PDE 修复、工具交付形式与资源成本
  - 一句话价值：两个未绑定 task-ID 队列合计从文字组 26/30 提升到工具组 29/30，但原始队列优势集中于 task 77、共享定义队列持平，且工具常以更多 public CPU 换取更少模型输出；真正结论是可执行检查的收益高度任务相关。


### 2026-10-06

- **From Verification Failures to Reusable Guidance for Coding Agents**
  - 简称：[Verification Guidance](https://38-76-161-31.sslip.io/daily-learning/?paper=261006-YuqingZhai-VerificationGuidance)
  - Tags：`2026` `arXiv` `Coding Agent` `Formal Verification` `K Framework` `Reusable Guidance` `Agent Skills` `Specification Adequacy`
  - 作者：Yuqing Zhai; Xiaohong Chen; Lingming Zhang; Sriram Vishwanath; Grigore Rosu
  - Venue / 年份：arXiv cs.SE / 2026
  - DOI / 原文：[arXiv:2609.39022](https://arxiv.org/abs/2609.39022); [PDF](https://arxiv.org/pdf/2609.39022)
  - 主题：coding-agent 形式验证、可执行语义、失败经验复用、规格充分性审计、K Framework 与验证指导
  - 一句话价值：论文把验证失败沉淀为语义与 procedure kit，但最可信的冻结三臂实验在 Luna 上正向、DeepSeek 上负向且区间均跨 0，说明指导内容、模型行为与推理预算必须分开评估。



### 2026-10-05

- **Learning When and How to Intervene: A Hindsight-Distilled Sentinel for Coding Agents**
  - 简称：[HiSentinel](https://38-76-161-31.sslip.io/daily-learning/?paper=261005-JiangruiZhao-HiSentinel)
  - Tags：`2026` `arXiv` `Coding Agent` `Trajectory` `Intervention` `Hindsight Distillation` `Human-in-the-loop` `SWE-bench`
  - 作者：Jiangrui Zhao; Chenglong Li; Meng Zhang; Xiaoting Du*
  - Venue / 年份：arXiv cs.SE / 2026
  - DOI / 原文：[arXiv:2609.39957](https://arxiv.org/abs/2609.39957); [HTML 全文](https://arxiv.org/html/2609.39957); [PDF](https://arxiv.org/pdf/2609.39957)
  - 主题：coding-agent 轨迹干预、pre-execution Sentinel、privileged hindsight distillation、错误传播与 human assistance
  - 一句话价值：HiSentinel 在动作执行前选择 Allow/Redirect/Hard-Pause，并把 future-aware teacher 的 hindsight 蒸馏给 0.6B/1.7B Sentinel；1.7B 版本将 Qwen3-Coder 在 SWE-bench Verified Mini 的 solve rate 从 30% 提到 44%，同时揭示真正重要的是 intervention quality 而非 intervention frequency。



### 2026-10-04

- **When and How Context Rot Appears in Coding Agents: A White-Box Study of Agent Skills in Code Auditing**
  - 简称：[Context Rot](https://38-76-161-31.sslip.io/daily-learning/?paper=261004-YueXue-ContextRot)
  - Tags：`2026` `arXiv` `Coding Agent` `Long Context` `Agent Skills` `Code Auditing` `Controlled Experiment` `Failure Analysis`
  - 作者：Yue Xue
  - Venue / 年份：arXiv cs.SE / 2026
  - DOI / 原文：[arXiv:2607.17937](https://arxiv.org/abs/2607.17937); [PDF](https://arxiv.org/pdf/2607.17937)
  - 主题：长上下文可靠性、Agent Skill、白盒代码审计、requirement retention、失败定位与 checklist mitigation
  - 一句话价值：固定任务与 24 个检查后，clean 8/10，而等长 relevant-long 与 irrelevant-long 都为 3/10；结果提示长上下文可能造成稀疏关键遗漏，但并不支持“相关/plausible 上下文必然比随机无关上下文更危险”。



### 2026-10-03

- **Harness Engineering for Agentic AI Coding Tools: An Exploratory Study**
  - 简称：[Harness Engineering](https://38-76-161-31.sslip.io/daily-learning/?paper=261003-MatthiasGalster-HarnessEngineering)
  - Tags：`2026` `AIware` `Agentic Coding` `Harness Engineering` `Context Files` `AGENTS.md` `Skills` `Subagents`
  - 作者：Matthias Galster; Seyedmoein Mohsenimofidi; Jai Lal Lulla; Muhammad Auwal Abubakar; Christoph Treude; Sebastian Baltes
  - Venue / 年份：AIware 2026 扩展版 / arXiv v5，2026
  - DOI / 原文：[arXiv:2602.14690](https://arxiv.org/abs/2602.14690); [HTML 全文](https://arxiv.org/html/2602.14690v5); [会议版 DOI: 10.1145/3805760.3814887](https://doi.org/10.1145/3805760.3814887); [补充材料](https://doi.org/10.5281/zenodo.18625980)
  - 主题：编码智能体 harness 配置机制、跨工具配置制品、AGENTS.md 互操作、Skills 与 Subagents 采用深度
  - 一句话价值：在 2,853 个开源仓库中，90.6% 有 Context Files，而 Skills 与 Subagents 仅见于 158 和 131 个仓库；AGENTS.md 正成为跨工具入口，但该研究只证明采用与结构，不证明任何配置会提高 agent 成功率。


### 2026-10-02

- **CRJudgeBench: Can AI Detect Plausible but Invalid Code Reviews?**
  - 简称：[CRJudgeBench](https://38-76-161-31.sslip.io/daily-learning/?paper=261002-YuePan-CRJudgeBench)
  - Tags：`2026` `arXiv` `Code Review` `Repository Context` `Agentic Judge` `Plausible Error` `Benchmark` `Action-level Distillation`
  - 作者：Yue Pan; Jiawei Li; Ziyuan Zhang; Xiangxin Zhao; He Ye*
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2609.37216](https://arxiv.org/abs/2609.37216); [HTML 全文](https://arxiv.org/html/2609.37216v1); [数据集](https://huggingface.co/datasets/dcloud347/CRJudgeBenchmark)
  - 主题：评审评论技术可信性、真实 PR 与受控扰动负例、仓库证据搜索、privileged teacher 动作蒸馏
  - 一句话价值：CRJudgeBench 以 1,199 个专家核验实例揭示模型普遍倾向接受看似合理的评审评论；Sentinel 将不可信评论召回从最强通用基线的 20.77% 提高到 37.69%，但 435 个负例中 370 个由否定、符号或位置扰动生成，现实外部效度仍需独立验证。


### 2026-10-01

- **Do Context Files Help Coding Agents? A Two-Agent Ablation Study on Real Repositories**
  - 简称：[Context Files Ablation](https://38-76-161-31.sslip.io/daily-learning/?paper=261001-PrakharKhatri-ContextFiles)
  - Tags：`2026` `Coding Agent` `AGENTS.md` `Repository Context` `Controlled Experiment` `Negative Result` `Statistical Power`
  - 作者：Prakhar Khatri
  - Venue / 年份：arXiv / 2026
  - DOI / 原文：[arXiv:2607.27250](https://arxiv.org/abs/2607.27250); [HTML 全文](https://arxiv.org/html/2607.27250v1); [代码与数据](https://github.com/codeprakhar25/context-files-coding-agents)
  - 主题：真实仓库中的上下文文件消融、任务内配对实验、coding agent 过程指标与统计功效
  - 一句话价值：在三个 Python 仓库、15/17 个真实任务和 Claude Code/Codex 两个代理上，全量常驻与选择性上下文均未稳定提高隐藏测试通过率；论文同时说明自然文档不等于任务决定性证据，地板/天花板任务与任务数不足会限制小效应识别。

## 待精读论文

- 暂无已指定待精读论文



