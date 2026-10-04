# Paper Pool · 2026-10

> 2026 年 10 月完整精读记录。当前月份每日精读只需读取本文件；跨月永久去重读取 `paperpool_short.md`。

## 已精读论文


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
