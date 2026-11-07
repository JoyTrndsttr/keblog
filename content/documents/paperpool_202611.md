# Paper Pool · 2026-11

> 2026 年 11 月精读记录。11 月 1 日为用户指定的计划外精读；其余条目按每日计划归档。

## 已精读论文

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
