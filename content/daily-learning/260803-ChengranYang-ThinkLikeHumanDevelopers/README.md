# Think Like Human Developers: Harnessing Community Knowledge for Structured Code Reasoning

> 精读日期：2026-08-03  
> 论文：*Think Like Human Developers: Harnessing Community Knowledge for Structured Code Reasoning*  
> 作者：Chengran Yang, Zhensu Sun, Hong Jin Kang, Jieke Shi, David Lo  
> Venue：ICSE 2026 Research Track  
> DOI / 原文：[arXiv:2503.14838](https://arxiv.org/abs/2503.14838)  
> 来源：从 `dialog.md` 的每日学习历史迁移  

## 一句话价值

把开发者社区讨论重组为结构化推理监督，复杂任务受益明显，但简单任务可能因过度推理退化。

## 历史精读正文

**Think Like Human Developers: Harnessing Community Knowledge for Structured Code Reasoning**

- 作者：Chengran Yang、Zhensu Sun、Hong Jin Kang、Jieke Shi、David Lo
- Venue：ICSE 2026 Research Track
- 类型：研究论文、ACM SIGSOFT Distinguished Paper
- [论文原文](https://arxiv.org/abs/2503.14838)
- [ICSE 2026 官方程序](https://conf.researchr.org/track/icse-2026/icse-2026-research-track)

**一句话结论**

将开发者社区中的问题分析、方案讨论和修正过程整理成结构化推理监督，可以显著增强代码模型处理复杂问题的能力，但简单任务可能因为过度推理而退化。

**方法概览**

1. 收集编程问题、参考答案和开发者讨论。
2. 过滤低质量或缺乏解释的讨论。
3. 按“理解、计划、设计、实现、测试、改进”重组推理过程。
4. 根据问题难度动态增加反思和修订轮次。
5. 扰动函数封装、输入输出和脚本格式，提高模型鲁棒性。
6. 使用 12,444 条增强样本微调 Qwen2.5-32B-Instruct，得到 CodeThinker。

**实验设置**

- 评测集：LiveCodeBench。
- 从 713 道题中筛选 562 道，以降低训练数据污染风险。
- 基线包括 Qwen2.5-Instruct-32B 和 Qwen2.5-Coder-32B-Instruct。
- 主要指标：`pass@1`，并按题目难度分类。

**主要结果**

- 中等难度任务相比基础模型提升 42.86%。
- 相比 Qwen2.5-Coder-32B-Instruct 提升 34.62%。
- 非 LeetCode 中等难度任务相比基础模型提升 78.01%。
- 非 LeetCode 简单任务下降 4.44%，说明复杂推理并非总是有益。

**与 MARC 的联系**

可以把 GitHub PR 审查讨论转化为如下结构化监督链：

> 理解变更意图 → 定位跨文件依赖 → 提出风险假设 → 检索证据 → 验证问题 → 生成评论 → 根据反馈修订

MARC 还可以根据变更复杂度选择不同流程：简单修改采用快速审查，跨文件或高风险修改才启动完整的多智能体推理，从而减少不必要的成本和“过度审查”。

**可借鉴的实验**

1. 比较原始审查讨论、结构化审查链、结构化链加多轮验证。
2. 按修改文件数和依赖范围分层，评估自适应推理深度。
3. 使用 GitHub 训练、Gerrit 测试，验证跨平台泛化能力。

**阅读优先级：高**
预计完整阅读时间：45–60 分钟。
