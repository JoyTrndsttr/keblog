# OpenCodeReview: Determinism over Non-Determinism for Cost-Effective Agent-Based Code Review

> 精读日期：2026-08-25  
> 论文：*OpenCodeReview: Determinism over Non-Determinism for Cost-Effective Agent-Based Code Review*  
> 作者：Zhengfeng Li, Lei Zhang, Xianwei Wu, Zhengqi Zhuang, Yingjie Xu, Boge Wang, Shaofei Zhu, Chuan Wang, Peng Zhao, Xinyu Zheng, Guoping Rong  
> Venue：arXiv, 2026  
> DOI / 原文：[arXiv:2608.09290](https://arxiv.org/abs/2608.09290)  
> 来源：从 `dialog.md` 的每日学习历史迁移  

## 一句话价值

以确定性规则分派、受限仓库探索和反思过滤改善 Agent 代码审查的精度与成本。

## 历史精读正文

### 4. 每日顶会 / 顶刊论文极速精读

#### 论文信息

- **标题**：OpenCodeReview: Determinism over Non-Determinism for Cost-Effective Agent-Based Code Review
- **作者**：Zhengfeng Li、Lei Zhang、Xianwei Wu、Zhengqi Zhuang、Yingjie Xu、Boge Wang、Shaofei Zhu、Chuan Wang、Peng Zhao、Xinyu Zheng、Guoping Rong
- **来源**：arXiv预印本，2026
- **原文**：[arXiv:2608.09290](https://arxiv.org/abs/2608.09290)
- **一句话结论**：相比让Agent自由规划整个审查过程，把规则选择、文件分派和工具边界工程化，可以大幅降低成本并提高评论精度；但现有实验只能证明整个系统有效，不能证明哪个设计真正产生了提升。

#### 速读导航表

| Section                    | 阅读建议          | 只需要带走什么                                     |
| -------------------------- | ----------------- | -------------------------------------------------- |
| 1 Introduction             | **快读**          | 作者认为自由规划造成重复探索、规则漂移和成本不可控 |
| 2 Background               | **跳过 / 扫一眼** | 了解Agent代码审查与reflection背景即可              |
| 3.1 Overview               | **必读**          | 三阶段架构及“确定性边界”位于何处                   |
| 3.2 Rule-Guided Dispatch   | **必读**          | 规则优先级、文件过滤和按文件并行分派               |
| 3.3 Grounded File Review   | **必读**          | 受限仓库工具、ReAct循环和评论行定位                |
| 3.4 Independent Reflection | **必读**          | 反思器为何只做证伪、不生成新意见                   |
| 4.1 Evaluation Setup       | **快读**          | AACR-Bench、模型、基线及LLM裁判                    |
| 4.2–4.4                    | **扫表 / 扫图**   | 重点看Table 3和Figure 3                            |
| 5 Discussion               | **快读**          | 系统设计与模型能力的作者解释                       |
| 6 Threats                  | **必读**          | ground truth和语义裁判的局限                       |
| 7 Conclusion               | **跳过 / 扫一眼** | 与摘要基本重复                                     |

**如果只有20–30分钟，按这个顺序读：**

Sec. 3.1 → Sec. 3.2 → Sec. 3.4 → Table 3 → Figure 3 → Sec. 4.1 → Sec. 6

#### 核心机制一：把Agent自由决策改成确定性调度

系统按四级优先级解析审查规则：

1. 临时规则；
2. 项目级规则；
3. 用户全局规则；
4. 内置规则。

随后按照文件类型、include/exclude条件、二进制文件、生成文件、测试夹具和超大diff等规则过滤文件，再为每个待审文件启动独立子Agent。

这里的“determinism”应准确理解为：

> 在相同输入和规则下，待审文件与适用规则的分配保持稳定。

它不意味着底层LLM每次都会生成同样的评论。

**读完这一节，你只需要记住：作者把最容易漂移的“审查什么、使用什么规则”从LLM手中收回，交给普通程序完成。**

#### 核心机制二：受限、可落地的仓库探索

每个文件Agent使用ReAct循环，最多30轮，并通过六种受限工具读取文件、搜索代码、读取diff和提交评论。工具具有明确边界，例如单次文件读取最多500行、搜索结果最多100项，并设置超时和上下文压缩。

这一设计的实际价值不在于提出了新的推理算法，而在于缩小Agent的动作空间：

**输入**：单个变更文件、diff、适用规则
→ **操作**：有限的仓库读取和代码搜索
→ **输出**：绑定具体文件及行号的审查评论

**读完这一节，你只需要记住：成本下降很可能来自“限制Agent能做什么”，而不只是更聪明的提示词。**

#### 核心机制三：非对称信息反思

反思Agent只看到diff和已生成评论，看不到原审查Agent探索过的全部仓库信息。它采用“证伪优先”：

- 只删除能被diff直接反驳的评论；
- 不能核验的仓库上下文主张予以保留；
- 不生成新意见；
- 解析失败时保持原评论。

这避免反思器凭借另一套不完整上下文重写答案，但也意味着它很难识别依赖跨文件上下文的隐蔽错误。

**读完这一节，你只需要记住：这是一个保守的precision filter，而不是第二轮完整审查。**

#### Research Question与证据链

**完整系统是否优于通用Coding Agent？**
→ 在相同200个PR上比较OpenCodeReview、Claude Code和Codex
→ 使用AACR-Bench的1,505条专家核验评论及语义匹配裁判
→ OpenCodeReview在六个模型上的SEM-F1为17.90%–25.10%
→ 可以支持“该完整实现与这些基线相比更有效率”，但不能支持“某个单独设计导致提升”。

**系统是否更省成本？**
→ 比较token和运行时间
→ 对Claude Code使用同类模型进行对照
→ 论文报告约5–15倍token节省
→ 成本优势明显，但基线拥有不同的工具、控制流程和上下文策略，不能视为只改变了“确定性”这一个因素。

**precision与recall如何权衡？**
→ 依据Figure 3比较评论数量和语义命中
→ OpenCodeReview precision为25.20%–37.80%，recall为11.70%–20.00%
→ Claude Code在部分设置中召回更高，但生成大量低精度评论
→ 说明系统偏向减少噪声，并不意味着同时占优于所有precision-recall工作点。

#### 数据集、基线与指标

- **Dataset**：AACR-Bench，200个真实PR、50个开源仓库、10种语言、1,505条专家核验评论，保留完整仓库。
- **Baselines**：Claude Code `/code-review`与Codex `/review`。
- **Models**：Claude-4.6-Opus、Claude-4.8-Opus、GPT-5.5、GLM-5.1、Qwen3.7-Max、Deepseek-V4-Pro。
- **Metrics**：语义precision、recall、SEM-F1，以及token和时间。
- **Judge**：Qwen3-235B-A22B-Instruct；每种配置重复裁判五次后取均值。该操作降低随机波动，但不能消除裁判的系统性偏差。

#### 可核验的核心结果

- Claude-4.6-Opus上，OpenCodeReview的SEM-F1为**25.10%**，Claude Code为**11.57%**，约为其2.17倍。
- 同一模型下，OpenCodeReview使用**385K tokens、1分23秒**；Claude Code为**5,664K tokens、13分06秒**。
- GPT-5.5上，OpenCodeReview为**21.00% SEM-F1**，Codex为**8.36%**；token分别为422K和525K。
- OpenCodeReview最高precision出现在Claude-4.8-Opus：**37.80%**，但recall只有**11.70%**。
- Claude Code在Claude-4.6-Opus上的recall达到**28.90%**，高于OpenCodeReview的20.00%，但precision仅**7.23%**。
- 六个模型下OpenCodeReview结果差距相对有限，但这只能说明该系统在这些配置中较稳定，不能等同于系统输出具有跨运行确定性。

#### 局限与可质疑点

**作者承认的局限**

- benchmark的ground truth可能遗漏合理评论；
- LLM语义裁判可能产生判断误差；
- benchmark规模和项目分布限制外部效度。

**从研究设计还可以进一步质疑**

1. **没有组件消融**
   规则分派、文件并行、工具限制、上下文压缩、反思过滤同时变化，无法识别各组件的独立效应。

2. **没有真正验证“确定性”**
   论文没有对相同PR重复运行多次并报告评论集合的一致性、方差或成本波动。确定性的直接证据只覆盖调度层。

3. **baseline并非单因素公平对照**
   系统之间的动作空间、工具、预算和上下文都不同，属于整套干预包，而不是严格控制实验。

4. **缺少不确定性估计**
   Table 3主要给出点估计，没有PR级置信区间、配对bootstrap或显著性检验。

5. **聚合结果隐藏异质性**
   没有按语言、PR大小、跨文件依赖程度或任务难度报告效果，平均值可能由简单任务主导。

6. **benchmark开发者重叠风险**
   AACR-Bench与本论文存在部分作者重叠。这不等于数据泄漏，但需要额外考察设计熟悉度和benchmark selection bias。

因此，这不是因果研究。论文对“系统设计比模型选择更重要”的结论，目前应理解为描述性证据，而不是已识别的因果效应。

#### 与 Causality for Code Review 的具体联系

这篇论文很适合作为你后续研究中的“待解耦干预包”。

可以构造一个三因素实验：

- **A：规则确定性分派**，开/关；
- **B：受限仓库探索工具**，开/关；
- **C：独立反思过滤**，开/关。

在同一模型、temperature、token预算、时间预算和PR集合下进行 \(2^3\) factorial design，并重复运行多个随机种子。

可定义：

- **Treatment**：A、B、C及其交互；
- **Outcome**：precision、recall、真实开发者有用性、token、时间、跨运行一致性；
- **Moderator**：PR难度、变更文件数、跨文件依赖、语言、ground-truth评论类型；
- **需要控制的条件**：模型版本、上下文预算、工具调用上限、生成评论数量。

这样才能回答论文目前回答不了的问题：

> 确定性调度本身是否提高审查质量，还是它只是通过减少探索、降低评论数量而提高precision？

#### 可直接借鉴的三点

1. 把“稳定性”变成正式Outcome：同一PR运行10次，计算评论语义集合的Jaccard、一致命中率及成本方差。
2. 使用PR级配对bootstrap报告效果差和95%置信区间，不只报告聚合SEM-F1。
3. 将PR的跨文件依赖程度作为effect modifier，检验受限工具在简单局部缺陷与复杂仓库级缺陷上的异质处理效应。

#### 最终Takeaway

- 论文的真正创新主要是Agent工程约束，而不是新的模型或推理算法。
- 系统在AACR-Bench上的质量—成本权衡明显优于两个通用Coding Agent。
- 最好的结果是25.10% SEM-F1，但绝对召回率仍不高。
- 最大的证据缺口是没有消融，也没有直接评估跨运行稳定性。
- 对你最有价值的是：它天然提供了一个可以被因果实验拆解的三组件干预框架。

> **如果一周后只记得这篇论文的一件事：先把Agent系统的自由度变成可控组件，再用因子实验判断究竟是哪种约束真正改善代码审查。**

- **阅读优先级**：★★★★★
- **建议投入时间**：30分钟
- **是否值得阅读全文**：否，先读核心8页即可
- **时间有限时读**：Sec. 3.2、Sec. 3.4、Table 3、Sec. 6
