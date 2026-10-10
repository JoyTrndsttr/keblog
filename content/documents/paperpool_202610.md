# Paper Pool · 2026-10

> 2026 年 10 月完整精读记录。当前月份每日精读只需读取本文件；跨月永久去重读取 `paperpool_short.md`。

## 已精读论文

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
