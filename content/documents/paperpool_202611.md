# Paper Pool · 2026-11

> 2026 年 11 月精读记录。11 月 1 日为用户指定的计划外精读；其余条目按每日计划归档。

## 已精读论文

### 2026-11-14

- **SWE-agent: Agent-Computer Interfaces Enable Automated Software Engineering**
  - 简称：[SWE-agent](https://38-76-161-31.sslip.io/daily-learning/?paper=261114-JohnYang-SWEAgent)
  - Tags：software engineering agents; agent-computer interface; tool feedback; context management
  - 作者：John Yang、Carlos E. Jimenez（共同一作、明确通讯联系人）、Alexander Wettig、Kilian Lieret、Shunyu Yao、Karthik Narasimhan、Ofir Press
  - Venue / 年份：NeurIPS 2024
  - DOI / 原文：10.52202/079017-1601；arXiv:2405.15793；https://proceedings.neurips.cc/paper_files/paper/2024/file/5a7c947568c1b1328ccc5230172e1e7c-Paper-Conference.pdf
  - 主题：以专用搜索、行范围编辑、错误恢复和历史管理改善语言模型的软件工程操作接口。
  - 一句话价值：同一 GPT-4 Turbo 在 SWE-bench Lite 上由 Shell-only 11% 提高到18%；逐条搜索反而只有12%，说明接口应帮助证据收敛而不是增加操作。

### 2026-11-13

- **Demystifying LLM-Based Software Engineering Agents**
  - 简称：[Agentless](https://38-76-161-31.sslip.io/daily-learning/?paper=261113-ChunqiuStevenXia-Agentless)
  - Tags：`2025` `FSE` `Hierarchical Localization` `Context Representation` `Patch Selection` `Benchmark Validity`
  - 作者：Chunqiu Steven Xia; Yinlin Deng; Soren Dunn; Lingming Zhang（前两位同等贡献；正式论文未明确标注通讯作者）
  - Venue / 年份：FSE 2025，Proceedings of the ACM on Software Engineering 2(FSE)，Article FSE037，24页
  - DOI / 原文：[10.1145/3715754](https://doi.org/10.1145/3715754)；[正式PDF](https://lingming.cs.illinois.edu/publications/fse2025.pdf)；[arXiv:2407.01489](https://arxiv.org/abs/2407.01489)（预印本题名：Agentless: Demystifying LLM-based Software Engineering Agents）；[代码](https://github.com/OpenAutoCoder/Agentless)
  - 主题：固定三阶段流水线、目录与向量检索结合、文件骨架、分支修复、复现/回归测试选择、SWE-bench Lite-S与Verified。
  - 一句话价值：骨架表示保留率56.67%→62%；同40补丁下独立分支修好96题、先合并上下文85题，揭示表示时机与候选汇合方式比单纯增删上下文更值得研究。

### 2026-11-12

- **OrcaLoca: An LLM Agent Framework for Software Issue Localization**
  - 简称：[OrcaLoca](https://38-76-161-31.sslip.io/daily-learning/?paper=261112-ZhongmingYu-OrcaLoca)
  - Tags：`2025` `ICML` `Issue Localization` `Code Graph` `Action Scheduling` `Context Pruning`
  - 作者：Zhongming Yu; Hejia Zhang; Yujie Zhao; Hanxian Huang; Matrix Yao; Ke Ding; Jishen Zhao（Zhongming Yu 与 Hejia Zhang 共同一作；明确通讯作者：Jishen Zhao）
  - Venue / 年份：ICML 2025，PMLR 267:73416–73436
  - DOI / 原文：[PMLR正式发表页](https://proceedings.mlr.press/v267/yu25x.html)；[arXiv:2502.00350v2](https://arxiv.org/abs/2502.00350v2)；[完整20页PDF](https://arxiv.org/pdf/2502.00350v2)；[代码](https://github.com/fishmingyu/OrcaLoca)
  - 主题：动态搜索优先级、实体去重、类/文件与歧义分解、代码图距离上下文裁剪、辅助复现器；定位/修复指标分离、93题消融与成本证据。
  - 一句话价值：同模型及修复后端下解决率由34.67%升至41.00%，搜索安排与上下文管理已有直接先例；对当前文件级定位更重要的缺口是范围证据、竞争机制和最终选择之间的传递。

### 2026-11-11

- **Issue Localization via LLM-Driven Iterative Code Graph Searching**
  - 简称：[CoSIL](https://38-76-161-31.sslip.io/daily-learning/?paper=261111-ZhonghaoJiang-CoSIL)
  - Tags：`2025` `ASE` `Issue Localization` `Code Graph` `Iterative Search` `Context Pruning`
  - 作者：Zhonghao Jiang; Xiaoxue Ren; Meng Yan; Wei Jiang; Yong Li; Zhongxin Liu（明确通讯作者：Zhongxin Liu）
  - Venue / 年份：ASE 2025 Research Papers，3034–3045
  - DOI / 原文：[10.1109/ASE63991.2025.00249](https://doi.org/10.1109/ASE63991.2025.00249)；[arXiv:2503.22424v3](https://arxiv.org/abs/2503.22424v3)；[完整17页PDF含补充材料](https://arxiv.org/pdf/2503.22424v3)；[论文工件](https://github.com/ZJU-CTAG/CoSIL)
  - 主题：文件导入关系扩展、函数级迭代搜索、相关性裁剪与短上下文反思；四个RQ、修复与定位指标分离、跨模型成本及新旧实现核对。
  - 一句话价值：32B函数Top-1比最强基线高18.6/12.0个百分点，消融以迭代搜索贡献最大；为搜索中上下文管理提供直接近邻，并将可恢复证据状态与方向提示、正文过滤区分开。

### 2026-11-10

- **Causal Agent Replay: Counterfactual Attribution for LLM-Agent Failures**
  - 简称：[Causal Agent Replay](https://38-76-161-31.sslip.io/daily-learning/?paper=261110-JaineetShah-CausalAgentReplay)
  - Tags：`2026` `arXiv` `Causal Attribution` `Counterfactual Replay` `Shapley Value` `Stochastic Policy`
  - 作者：Jaineet Shah（唯一作者；原文机构与通讯作者均未明确标注）
  - Venue / 年份：arXiv cs.LG / cs.AI，2026；未核实正式发表 venue
  - DOI / 原文：[arXiv:2606.08275v1](https://arxiv.org/abs/2606.08275v1)；[完整5页PDF](https://arxiv.org/pdf/2606.08275v1)；[固定版本工件](https://github.com/jaineet17/causal-agent-replay/tree/db90fa28b97164c35e7c524e4597b8cbdb3035af)
  - 主题：五类Agent步骤干预、同策略重采样、最后可救援点、Monte Carlo Shapley交互分配、合成验证与回放/语义对齐边界。
  - 一句话价值：为GraphLocator同状态分叉区分救援位置、内容处理效应与交互归因；合成机制的0.91总效果不证明真实Agent唯一根因，绝对步骤对齐也不保证状态一致。

### 2026-11-09

- **Attributing Agent Failures to Their History Needs an Executed Counterfactual: Toward a Reporting Standard**
  - 简称：[Executed Counterfactual](https://38-76-161-31.sslip.io/daily-learning/?paper=261109-EgorPakhomov-ExecutedCounterfactual)
  - Tags：`2026` `IAB Workshop` `Causal Attribution` `Counterfactual Replay` `History Intervention` `Measurement Validity`
  - 作者：Egor Pakhomov; Erik Nijkamp（Salesforce AI Research；原文未明确标注通讯作者）
  - Venue / 年份：NeurIPS 2026 Interpreting Agent Behavior（IAB）Workshop，非归档
  - DOI / 原文：[arXiv:2611.05650v1](https://arxiv.org/abs/2611.05650v1)；[完整20页PDF](https://arxiv.org/pdf/2611.05650v1)；[完整HTML](https://arxiv.org/html/2611.05650v1)
  - 主题：历史因果归因的回放验证标准；载体分类混杂、快照遗漏随机流、原运行对照、TRACE复现、未执行八臂设计与二手文献编码边界。
  - 一句话价值：把“分支彼此一致”与“恢复忠实于原轨迹”分开，为GraphLocator同状态决策分叉提供前置验证依据；模型无关警示测量不证明真实Agent历史污染的效应。

### 2026-11-08

- **Separating Semantic Competition from Context Length in RAG Reading**
  - 简称：[Semantic Competition](https://38-76-161-31.sslip.io/daily-learning/?paper=261108-VyzantinosRepantis-SemanticCompetition)
  - Tags：`2026` `arXiv` `RAG` `Controlled Evaluation` `Semantic Competition` `Matched Context`
  - 作者：Vyzantinos Repantis; Ameya Gawde; Harshvardhan Singh; Rohit Alekar; Cien Zhang; Svetlana Karslioglu; Akash Vishwakarma（Meta Platforms；原文未明确标注通讯作者）
  - Venue / 年份：arXiv cs.CL / cs.IR，2026；未核实正式发表 venue
  - DOI / 原文：[arXiv:2605.27294v1](https://arxiv.org/abs/2605.27294v1)；[完整 PDF](https://arxiv.org/pdf/2605.27294v1)；[作者实验工件](https://github.com/repantis-ai/rag-semantic-competition)
  - 主题：固定二十片段与近似平均输入长度，用真实远排名材料替换高排名负例；覆盖保留率、右删失半衰点、配对统计、片段设置敏感性及公开工件审计。
  - 一句话价值：给 token 与材料数量分离提供直接对照先例；工件揭示 gold 位置未配对固定、跨长度解码与评分变化，不能夸为纯语义竞争的完整因果识别。

### 2026-11-07

- **Right for the Wrong Reasons: Diagnosing Syntactic Heuristics in Natural Language Inference**
  - 简称：[HANS](https://38-76-161-31.sslip.io/daily-learning/?paper=261107-RThomasMcCoy-HANS)
  - Tags：`2019` `ACL` `Controlled Evaluation` `NLI` `Shortcut Learning` `Generalization`
  - 作者：R. Thomas McCoy; Ellie Pavlick; Tal Linzen（Johns Hopkins University、Brown University；原文未明确标注通讯作者）
  - Venue / 年份：ACL 2019，3428–3448
  - DOI / 原文：[10.18653/v1/P19-1334](https://doi.org/10.18653/v1/P19-1334)；[正式21页PDF](https://aclanthology.org/P19-1334.pdf)；[数据与代码](https://github.com/tommccoy1/hans)
  - 主题：三种句法捷径的受控挑战、正反例、人类检验、训练增强、五组类别留出与外部迁移。
  - 一句话价值：用能区分替代解释的对照审查高分，避免把模板记忆或新捷径当作鲁棒理解；为盲化输入与答案空间控制提供方法论参照，不直接证明代码上下文的因果效应。

### 2026-11-06

- **The Powerless Noise: How Experimental Settings Shape the Reported Power of Noise**
  - 简称：[Powerless Noise](https://38-76-161-31.sslip.io/daily-learning/?paper=261106-MichalMazuryk-PowerlessNoise)
  - Tags：`2026` `SIGIR` `Reproducibility` `RAG` `Noise` `Prompting` `Evaluation`
  - 作者：Michał Mazuryk; Fleur Dolmans; Louis Gehringer; Ina Klaric; Jia-Huei Ju; Mohammad Aliannejadi（University of Amsterdam；原文未明确指定通讯作者）
  - Venue / 年份：SIGIR 2026 Reproducibility Track
  - DOI / 原文：[10.1145/3805712.3808556](https://doi.org/10.1145/3805712.3808556)；[arXiv:2607.03615v2](https://arxiv.org/abs/2607.03615v2)；[完整 HTML](https://arxiv.org/html/2607.03615v2)；[复现代码](https://github.com/ina0105/The-Power-of-Noise-Reproduction)
  - 主题：复现随机检索噪声收益，分离量化、模型、聊天模板、输出上限与任务指令的影响；覆盖附录输出错误及跨表报告不一致。
  - 一句话价值：先核查短输出截断和评分协议，再解释上下文干扰曲线；噪声收益对配置敏感，但不能据此断言随机上下文永远无用。

### 2026-11-05

- **Making Retrieval-Augmented Language Models Robust to Irrelevant Context**
  - 简称：[Retrieval Robustness](https://38-76-161-31.sslip.io/daily-learning/?paper=261105-OriYoran-RetrievalRobustness)
  - Tags：`2024` `ICLR` `RAG` `Irrelevant Context` `NLI` `Multi-hop Reasoning` `Robustness`
  - 作者：Ori Yoran; Tomer Wolfson; Ori Ram; Jonathan Berant（Tel Aviv University、Allen Institute for AI；原文未明确指定通讯作者）
  - Venue / 年份：ICLR 2024
  - DOI / 原文：[arXiv:2310.01558v2](https://arxiv.org/abs/2310.01558v2)；[完整 HTML](https://arxiv.org/html/2310.01558v2)；[代码、数据与模型](https://github.com/oriyor/ret-robust)
  - 主题：五类问答任务中的检索干扰、NLI回退与混合噪声微调；覆盖附录中的跨任务泛化、错误分析及提示配置。
  - 一句话价值：把“检索看起来相关”“能直接推出答案”和“实际上帮助回答”分开；小规模混合训练增强鲁棒性，但不能据此认证仓库Core充分或断言P普遍有害。

### 2026-11-04

- **Lost in the Middle: How Language Models Use Long Contexts**
  - 简称：[Lost in the Middle](https://38-76-161-31.sslip.io/daily-learning/?paper=261104-NelsonFLiu-LostInTheMiddle)
  - Tags：`2024` `TACL` `Long Context` `RAG` `Position Bias` `Controlled Evaluation`
  - 作者：Nelson F. Liu; Kevin Lin; John Hewitt; Ashwin Paranjape; Michele Bevilacqua; Fabio Petroni; Percy Liang（Stanford University、Samaya AI；原文未明确指定通讯作者）
  - Venue / 年份：Transactions of the Association for Computational Linguistics 12:157–173, 2024
  - DOI / 原文：[正式全文](https://aclanthology.org/2024.tacl-1.9.pdf)；[书目信息](https://aclanthology.org/2024.tacl-1.9/)；[代码与数据](https://github.com/nelson-liu/lost-in-the-middle)
  - 主题：多文档问答与随机键值检索中的证据位置效应、上下文长度、干扰类型和查询感知提示；完整覆盖附录 A–E。
  - 一句话价值：以正确证据始终在场的受控实验区分“能容纳”与“会利用”上下文；为位置匹配的 P/I 对照提供设计参照，但不证明仓库任务中的 P 必然比 I 更有害。

### 2026-11-01

- **The Agent in the Middle: A Security and Privacy Analysis of Android AppFunctions**
  - 简称：[AppFunctions Security](https://38-76-161-31.sslip.io/daily-learning/?paper=261101-TautvydasJackevicius-AppFunctionsSecurity)
  - Tags：`2027` `PETS` `Android` `AppFunctions` `Agent Security` `Permissions` `Cross-App Collusion` `Prompt Injection`
  - 作者：Tautvydas Jackevičius; Aniketh Girish; Vinuri Bandara; Guillermo Suarez-Tangil; Juan Tapiador; Narseo Vallina-Rodriguez（IMDEA Networks、Universidad Carlos III de Madrid；原文未标注通讯作者）
  - Venue / 年份：Proceedings on Privacy Enhancing Technologies 2027(1)
  - DOI / 原文：[机构论文](https://dspace.networks.imdea.org/handle/20.500.12761/2072)；[实验工件](https://github.com/appfunc/app-functions-security-analysis)
  - 主题：Android AppFunctions 的信任边界、权限再委托、七类攻击、商业设备验证及 APK 生态测量（计划外精读）
  - 一句话价值：作者验证七种代表性攻击（其中三种在受约束商业部署中复现），扫描 248,557 个 APK，并明确将多恶意 Provider 共谋留作未研究问题；有助于区分现有权限传递攻击与尚待验证的新组合攻击。

## 待精读论文

- 暂无。
