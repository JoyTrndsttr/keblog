# SecureReviewer：通过安全感知微调增强大语言模型的安全代码审查能力

> **论文**：[SecureReviewer: Enhancing Large Language Models for Secure Code Review through Secure-aware Fine-tuning](https://arxiv.org/abs/2510.26457)  
> **作者**：Fang Liu, Simiao Liu, Yinghao Zhu, Xiaoli Lian, Li Zhang  
> **单位**：北京航空航天大学计算机学院、复杂关键软件环境全国重点实验室  
> **会议**：ICSE 2026  
> **DOI**：[10.1145/3744916.3773191](https://doi.org/10.1145/3744916.3773191)  
> **代码与数据**：[SIMIAO515/SecureReviewer](https://github.com/SIMIAO515/SecureReviewer)

## 先用三句话建立论文地图

SecureReviewer 研究的是：只给代码 diff 时，怎样让大语言模型不仅生成“像代码审查”的文字，还能判断是否存在安全问题、说明影响并给出修复建议。作者从 CodeReviewer 数据中筛选并重写出 4,674 条结构化安全审查数据，在 7B 代码模型上加入安全关键 token 加权损失，再用检索到的安全评论模板辅助最终生成；同时提出 SecureBLEU，试图弥补普通 BLEU 只看表面措辞的问题。主结果显示三种 SecureReviewer 的安全问题检测 F1 约为 71.6–72.0，明显高于最佳 baseline 的 61.46；但论文同样报告了一个很重要的反例：检索增强对已完成领域微调的模型没有稳定收益，部分指标反而下降。

全文的证据链是：

```text
通用代码审查数据噪声大、安全评论稀缺
                  ↓
从 CodeReviewer 中用关键词与 CWE 语义匹配召回候选
                  ↓
GPT-4o 判别、结构化重写 + 专家抽检/测试集修订
                  ↓
把安全评论操作化为 ST / D / I / A 四个字段
                  ↓
领域微调 + 安全关键 token 加权 + 模板检索生成
                  ↓
用分类指标、BLEU、SecureBLEU 与人工评分评价
                  ↓
判断安全专门化是否改善检测与评论质量
```

理解论文需要先分清四个概念：

1. **安全代码审查**：本文不是在完整仓库中自主找漏洞，而是给定代码 diff，输出是否存在某类安全问题、问题描述、影响与修复建议。
2. **Common Weakness Enumeration（CWE，通用缺陷枚举）**：MITRE 维护的弱点分类体系。本文用 CWE 描述做语义筛选，也用安全类别对应的关键词构造评价指标。
3. **安全感知损失（Secure-Aware Loss，SA-Loss）**：仍然训练模型生成整段评论，但对安全类别 token 和评论中提到的代码标识符额外加权。
4. **Retrieval-Augmented Review Generation（RARG，检索增强审查生成）**：模型先预测安全类别，再只在该类别的模板中检索相似代码案例，将其评论模板放入第二阶段 prompt 后重新生成。

## 1. Research Gap：为什么通用 Code Review 模型不够

已有自动代码审查方法已经能从 diff 生成评论，CodeReviewer、LlamaReviewer 也提供了专门预训练或微调方案。但作者指出，将这些系统直接用于安全审查会遇到两个具体问题。

第一是数据。公开 code review 数据包含大量姓名、格式讨论、“Looks good to me”或“为什么需要这个”等普通协作内容，安全评论在真实社区里本就稀少。通用模型即使学会评论语气，也未必学会识别 race condition、访问控制、输入验证和资源泄漏。

第二是评价。BLEU 统计预测与参考文本的 n-gram 重叠；如果模型用了不同措辞表达正确安全判断，BLEU 可能很低。反过来，一条评论只要复用了参考文本的普通词语，即便安全类别判断错了，也可能得到较高 BLEU。Figure 1 展示的例子正是如此：模型把“访问控制与信息安全”误判为“类型与数据处理”，普通 BLEU 仍有 26.44，而 SecureBLEU 降至 12.12。

因此论文真正的 gap 不是简单地“再微调一个模型”，而是同时补齐三个环节：安全专用训练数据、安全专用优化目标、安全专用评价指标。这里也埋下一个后续构念风险：数据、训练和指标使用了同一套安全类别与关键词，三者可能相互强化，而不一定等价于真实开发者认为评论有效。

## 2. 数据集怎样从 13.8 万条评论变成 4,674 条样本

### 2.1 原始数据与两条候选召回路径

作者以 CodeReviewer 的 review comment generation 和 code change quality estimation 数据为源。约 13.8 万条原始评论不可能逐条人工筛选，因此使用两条互补路径召回安全候选。

**关键词路径**使用既有研究整理的 122 个关键词、15 类安全缺陷，去掉过于宽泛的 common keywords 后，将类别映射到 CWE。评论经过小写化、词干化和标点清理后，先得到 10,840 条候选。GPT-4o 再同时读取 diff、完整评论和命中的安全类型，判断评论是否真的描述相应安全问题，最终保留 1,995 条。

**语义路径**希望找出没有显式写出 security keyword 的评论。作者用面向软件工程文本训练的 SO_word2vec 表示评论和 CWE-699 描述，计算余弦相似度，以 70% 为阈值，再经过同一个 GPT-4o judge，得到 2,771 条安全评论。

两条路径合计 4,766 条，去重与合并相近类别后剩 4,089 条。它们被归并为七类：异常处理、并发、输入验证、访问控制与信息安全、资源管理、状态管理、类型与数据处理。

### 2.2 “Non-Issue” 类怎样加入

为了让任务不至于变成“已知一定有漏洞时做七分类”，作者从 CodeReviewer 的 code change quality estimation 数据中选取 585 条没有 review comment 的变更，作为第八类 Non-Issue。最终 4,674 条的类别分布中，输入验证占 17.52%，访问控制与信息安全占 17.01%，状态管理占 15.83%，Non-Issue 占 12.52%，其余类别约为 6.25%–11.38%。

这一步让模型可以输出“无问题”，但标签强度有限：**没有评论不等于经过安全审计后确认没有问题**。它可能只是没有人评论、审查者没发现，或评论未进入该数据源。因此 Non-Issue 的构念更接近“未观察到评论的变更”，论文没有额外用静态分析、测试或专家逐条证明其安全。

### 2.3 GPT-4o 把评论重写成四个字段

作者把每条安全评论统一定义为：

\[
R=(ST,D,I,A),
\]

其中：

- \(ST\)：Security Type，安全问题类型；
- \(D\)：Description，根因描述；
- \(I\)：Impact，潜在影响；
- \(A\)：Advice，可执行的修复建议。

GPT-4o 通过 one-shot prompt 将原评论重写成这一结构。这样做有两个直接好处：训练输出格式稳定，评价时也能分别检查类别、解释、影响和建议。代价是 ground truth 不再是原始开发者评论，而是 LLM 基于原评论扩写出的规范化答案；它可能提高完整性，也可能把模型生成的表述偏好带进训练和评价。

### 2.4 质量控制

作者从 4,089 条重写后的安全数据中随机抽取 351 条，由两名具有六年以上开发经验的专家独立检查四个字段，Cohen's Kappa 为 0.74；333 条、即 95% 同时满足四项质量要求。随后数据划分为 4,074 条训练、300 条验证和 300 条测试。

测试集中 38 条是 Non-Issue，其余 262 条由同两名专家全部复核；其中 83 条被进一步澄清或增强。初始质量评估约耗费 98 人时，测试集修订约 87.3 人时；GPT-4o 筛选与重写按论文当时价格约花费 46 美元。

这证明测试参考答案经过较强人工质量控制，但论文没有清楚展示 repository-level 或时间切分，也没有系统报告跨 split 的近重复 diff、同项目相似变更或模板泄漏检查。去重主要发生在筛选结果合并阶段，因而“对未见项目的泛化”不能从现有证据直接推出。

## 3. SecureReviewer 从输入到输出怎样运行

```text
代码 Diff
   ↓
7B 代码模型 + LoRA 领域微调
   ↓
SA-Loss 强调安全类别和关键标识符
   ↓
第一次生成：预测 ST / D / I / A
   ↓
按预测 ST 缩小模板库，以 Diff 为 query 做 BM25
   ↓
返回最相似的安全评论模板
   ↓
Diff + 模板进入第二阶段 Prompt
   ↓
最终结构化安全审查评论
```

### 3.1 领域微调

论文分别使用 CodeLlama-7B、DeepSeek-Coder-6.7B 和 Qwen2.5-Coder-7B 作为 backbone，以 Low-Rank Adaptation（LoRA，低秩适配）训练。LoRA rank 为 8，alpha 为 16，dropout 为 0.05；最大长度 2,048 tokens，batch size 4，梯度累积 8，学习率 3e-4。模型用 greedy decoding 做确定性推理。

微调首先教会模型识别 diff 格式、八类标签和四字段输出。后面的 ablation 会显示，这其实是全部增益中最大的一步。

### 3.2 SA-Loss 为什么不仅是普通交叉熵

普通生成损失把每个输出 token 大致平等处理。作者认为，安全类别词和与漏洞直接相关的代码标识符更重要，因此定义两组 token：

- \(\mathcal I_V\)：评论中引用到的 diff 标识符；
- \(\mathcal I_{ST}\)：安全类别名称 token。

目标函数在全评论对数似然之外，对两组 token 再加权：

\[
-\mathcal L_{SA}=\sum_{t\in R}\log P(x_t|x_{<t})
+\alpha\sum_{t\in\mathcal I_V}\log P(x_t|x_{<t})
+\beta\sum_{t\in\mathcal I_{ST}}\log P(x_t|x_{<t}).
\]

论文取 \(\alpha=2\)、\(\beta=5\)。直觉上，类别错了会连带影响描述与建议，所以类别权重最大；代码标识符让评论更具体，因此也比普通连接词更重要。这个 loss 能提高同一任务定义下的类别与关键词表现，但不能单独证明模型理解了漏洞机制：模型也可能更擅长复现标签词与显眼标识符。

### 3.3 RARG 的两阶段检索

作者从训练集人工制作 261 个高质量模板，覆盖所有安全类型，分布尽量接近训练数据。第一次生成先给出预测安全类型；第二阶段只在该类型对应的模板中，以当前 diff 为 query，用 BM25 找最相似模板，再要求模型参考该模板重写最终评论。

这里检索的是“相似 diff 对应的评论写法”，不是当前仓库的 caller、callee、测试或运行证据。因此 RARG 补的是领域表达与处置建议，并没有扩大程序语义的观察范围。如果第一次类型预测错了，检索还会被路由到错误类别的模板库。

## 4. SecureBLEU 究竟奖励什么

SecureBLEU 由两部分等权组成：

\[
\mathrm{SecureBLEU}=0.5\cdot score_{bleu}+0.5\cdot score_{keywords}.
\]

第一部分对四字段分别评分：ST 必须精确匹配，匹配得 100，否则为 0；D、I、A 使用 BLEU-4，再按字段权重合并。第二部分在参考评论的 D、I、A 中抽取与真实安全类型对应的词典关键词，计算预测评论覆盖了多少。

如果模型预测 Non-Issue，算法直接返回 0。权重 0.5/0.5 是在人工评价样本上从 0.2/0.8 到 0.8/0.2 搜索后选择的，和人工分数 Pearson 相关达到 0.7533；普通 BLEU 的相关为 0.4026。

它确实比纯 BLEU 更关注安全类别与术语，但仍有三个边界：

1. 安全类型被同时用于训练、检索路由和评价，类别正确会对总分产生多重影响。
2. 关键词覆盖可奖励“说到了正确术语”，未必验证根因链或修复建议能否真正消除漏洞。
3. 0.5/0.5 权重是在同一组 262 条人工评价上选出的，再用同一相关性说明合理性，缺少独立验证集，因此 0.7533 可能带有权重选择后的乐观偏差。

## 5. 实验坐标系与 baseline 公平性

测试集有 300 条，问题检测做八分类；评论生成排除 38 条 Non-Issue，使用 262 条。指标包括 Precision、Recall、F1、Accuracy、BLEU-4 和 SecureBLEU。

Baseline 分为三组：专门的 CodeReviewer 与 LlamaReviewer；未经本任务微调的 CodeLlama、DeepSeek-Coder、Qwen2.5-Coder；以及 GPT-4o、Claude-3.5-Sonnet、DeepSeek-V3/R1。CodeReviewer 按官方配置微调，LlamaReviewer 与三个 backbone 尽量使用相同 LoRA 配置。API 模型 temperature=0.7、top-p=0.7、frequency penalty=0.5，独立运行三次并报告均值和标准差；所有模型统一输出 ST/D/I/A 格式。

最公平的比较是“同一 7B backbone 逐步加微调、SA-Loss、RARG”，因为模型容量和数据基本固定。SecureReviewer 与大型 API 模型的总表则同时改变参数规模、训练方式、是否见过任务数据和解码方式，更适合比较系统结果，不宜解释成某个组件单独胜过更大模型。

## 6. RQ1：整体检测与评论生成效果如何

### 问题与设计

RQ1 分成两部分：八分类安全问题检测是否更准，以及生成评论是否更像高质量安全审查。Table 2 把检测指标放左侧、生成指标放右侧；阅读时应先比较经过同数据微调的 CodeReviewer/LlamaReviewer，再看三种 SecureReviewer 是否跨 backbone 稳定。

### 关键结果

| 模型 | F1 | Accuracy | BLEU | SecureBLEU |
|---|---:|---:|---:|---:|
| CodeReviewer | 59.03 | 58.53 | 8.66 | 21.31 |
| LlamaReviewer | 61.46 | 61.20 | 9.20 | 24.56 |
| DeepSeek-V3 | 53.31 | 53.56 | 10.80 | 21.84 |
| SecureReviewer-CL | **71.98** | 71.91 | **11.34** | **29.31** |
| SecureReviewer-DS | 71.62 | **72.24** | 11.01 | 29.23 |
| SecureReviewer-QW | 71.60 | 71.33 | 9.35 | 28.76 |

三种 backbone 的 F1 聚集在 71.60–71.98，说明增益并非只出现在一个底座。相对最佳 baseline LlamaReviewer，最高 F1 提高约 17%，Accuracy 提高约 18%；最高 SecureBLEU 29.31，相对 24.56 提高约 19%。

但生成结果也说明 BLEU 与安全评价不完全同步。DeepSeek-V3 的 BLEU 为 10.80，已经接近 SecureReviewer；Qwen 版本 SecureBLEU 很高，BLEU 只有 9.35。该结果支持“普通措辞重合不足以评价安全评论”，但由于 SecureBLEU 与训练标签共享设计，它还不能独立证明评论会在真实 review 中发现更多可执行漏洞。

**Takeaway：领域数据与任务化输出带来稳定的大幅检测增益；评论质量增益在安全定制指标上比普通 BLEU 更明显。**

## 7. RQ2：真正贡献最大的组件是什么

Table 3 是全文最需要认真看的表，因为它保留了负结果。作者按固定顺序逐步加入领域微调、SA-Loss 和 RARG。

### 7.1 领域微调是主要增益来源

以 DeepSeek-Coder 为例，F1 从 15.58 上升到 68.90，SecureBLEU 从 16.00 上升到 26.27；CodeLlama 的 F1 从 6.22 上升到 71.09，SecureBLEU 从 11.68 上升到 27.88；Qwen 的 F1 从 38.57 上升到 68.84。

这些提升非常大，但它们同时包含三件事：学会输出格式、学会八类标签、学会安全评论内容。因此不能把全部提升解释成“更深的安全推理”；尤其 CodeLlama 原模型经常复述代码、不遵循指令，微调也修复了基本 task alignment。

### 7.2 SA-Loss 提供较小但一致的增益

在三个已微调 backbone 上加入 SA-Loss 后，F1 分别从 68.90、71.09、68.84 上升到 71.62、71.98、71.60；SecureBLEU 从 26.27、27.88、27.61 上升到 28.79、29.69、29.21。结果支持“给类别和标识符更高权重有帮助”。

不过这是增量消融而不是完整析因实验：没有单独报告“原模型 + SA-Loss 但无领域微调”，也没有改变组件加入顺序，因此不能估计组件之间的独立效应和交互。

### 7.3 RARG 对微调模型没有稳定收益

加入 RARG 后：

- DeepSeek 的 SecureBLEU 从 28.79 小幅升到 29.23，但 BLEU 从 11.27 降到 11.01；
- CodeLlama 的 SecureBLEU 从 29.69 降到 29.31，BLEU 从 12.46 降到 11.34；
- Qwen 的 SecureBLEU 从 29.21 降到 28.76，BLEU 从 9.47 降到 9.35。

这不是“每个组件都稳定贡献”的证据。更准确的结论是：RARG 对已经用相同领域数据微调的模型大多冗余，训练时不看模板、推理时突然插入模板还造成输入分布变化。

对未微调的大模型，RARG 的 SecureBLEU 提升较明显：GPT-4o 19.33→23.93，Claude 19.54→29.34，DeepSeek-V3 21.84→25.64；但三者 BLEU 都略降。论文没有对这些 RARG 对比做配对人工评价，也没有直接测 hallucination rate，所以它证明的是“模板让 SecureBLEU 更高”，不是“检索已经被证明减少幻觉”。

**Takeaway：领域微调贡献最大，SA-Loss 有一致的小幅收益；RARG 是依赖模型状态的异质性 intervention，对已有领域知识的模型可能无益甚至干扰。**

## 8. RQ3：不同安全类型上是否同样有效

Figure 5 有三个子图：分别画各安全类型的检测 F1、SecureBLEU 和 BLEU。阅读顺序应先看 F1 的类别差距，再看 SecureBLEU 是否跟随，最后检查 BLEU 是否呈现同样趋势。

三种 SecureReviewer 在多数类型上比四个强 baseline 更均衡，但 State Management、Resource Management 和 Concurrency 仍然困难。作者解释这些问题需要理解线程同步、状态转换、资源生命周期，以及 diff 之外的执行流和跨过程依赖。SecureBLEU 的类别趋势与 F1 高度一致，而 BLEU 的差距小得多。

这里“F1 与 SecureBLEU 同步”部分是指标设计的自然结果：安全类别预测正确会直接提高 SecureBLEU 的 ST 字段和关键词选择。因此这不完全是两种独立证据相互验证。真正有价值的发现是 failure cases 指向更大语义范围：模型会看到 `map` 或 mutex 就套用并发模式，也会因为不知道数组在其他函数如何初始化而漏掉越界问题。

**Takeaway：SecureReviewer 提高了类别整体表现，但最依赖跨过程和生命周期语义的类别仍暴露出 isolated diff 的上限。**

## 9. 人工评价与 Figure 6、7

两名具有六年以上 Java/Python、代码审查与 CWE 经验的软件工程师对 262 条 SecureReviewer-DS 评论评分，维度为清晰性、相关性、完整性、可操作性，均使用 1–5 分。平均分依次为 3.93、4.06、3.98、3.90，评审者 Cohen's Kappa 为 0.66。

Figure 6 展示四维平均分总体接近 4；Figure 7 将人工总分分别与 BLEU、SecureBLEU 作散点比较。BLEU 图中有大量“人工高分、BLEU 低分”的左上点，SecureBLEU 的高人工分样本更集中在高分区域；相关系数分别为 0.4026 和 0.7533。

这是 SecureBLEU 有效性的正面证据，但人工评价只评了 SecureReviewer-DS 的输出，没有同盲评 baseline，也没有报告 RARG 开关前后的人工差值。因此它可以说明该系统输出在四个主观维度上总体不错，不能单独证明 SecureReviewer 比 baseline 的真实开发价值高 19%。

## 10. Failure Cases：为什么“更像安全评论”仍可能判断错

作者归纳两类失败。

第一是**表面模式匹配**。模型看到 `map`、删除操作或 mutex 等词法/语法迹象，就倾向输出并发问题，实际根因却可能是输入验证或数组边界。这说明安全类别和关键词加权有可能放大 shortcut。

第二是**上下文不足**。输入只有 isolated diff，模型看不到全仓库执行流、跨函数依赖和变量生命周期。例如数组边界是否安全，常常取决于其他函数中的初始化与修改；diff 内没有这些证据时，模型无法可靠判断。

这两类错误共同限制了论文的“SOTA”：系统更擅长在既定八类 taxonomy 内生成结构完整、术语充分的评论，但对真正需要 repository context 的 case，它仍可能在错误机制上给出很完整的解释。

## 11. 作者与团队背景

五位作者均来自北京航空航天大学计算机学院与复杂关键软件环境全国重点实验室。第一作者是 **Fang Liu**；公开论文页面没有提供足以可靠重建其个人长期研究履历的详细主页，因此不额外推断其职称或研究年限。

论文明确用星号标出 **Li Zhang 为通讯作者**，不是根据末位顺序猜测。团队在本工作中把研究链条覆盖到 CodeReviewer 数据筛选、LLM 结构化标注、参数高效微调、RAG 和安全评价，公开仓库也包含采集、训练、推理与评测代码；从可核验成果看，其直接积累集中在自动代码审查、软件安全与 LLM 专门化评估的交叉处。本文与该积累的关系是把通用 review generation 收窄为安全问题检测与结构化修复建议。

## 12. 论文证明了什么，没有证明什么

### 有证据支持的结论

1. 在作者构建的 300 条测试集与八分类定义上，领域微调能显著提高三个 7B backbone 的安全问题检测和结构化评论生成表现。
2. 对安全类别和关键标识符加权的 SA-Loss，在三个 backbone 上都带来较小但一致的 F1 与 SecureBLEU 增益。
3. SecureBLEU 在当前 262 条样本上与两位专家的人工评价相关性高于普通 BLEU。
4. RARG 对通用 API 模型提高 SecureBLEU，但对已微调模型没有稳定增益。
5. 并发、状态和资源管理仍然受到 isolated diff 与跨过程语义缺失的限制。

### 尚未被证明的结论

1. 没有证明 SecureReviewer 能在完整 pull request 或仓库中自主定位安全问题；输入已经是待审 diff。
2. 没有证明生成建议经编译、测试或安全分析后能够真正修复漏洞。
3. 没有证明 RARG 减少了幻觉；论文只报告自动指标，没有专门定义和统计 hallucination。
4. 没有证明 585 条 Non-Issue 都无安全问题，也没有证明测试集代表真实安全审查分布。
5. 没有证明 SecureBLEU 可以跨 taxonomy、跨项目直接泛化；其类别与关键词词典和当前数据构造紧密耦合。
6. 没有把“安全数据”“结构化输出”“SA-Loss”“模板检索”做完整析因分解，不能把最终总增益平均归功于所有组件。

## 13. 真正应该记住什么

- SecureReviewer 最主要的能力增益来自高质量领域数据和 task alignment，不是 RAG。
- 把评论拆成“类型—描述—影响—建议”使训练和评价更清晰，但也把模型限制在预定义 taxonomy 中。
- 安全关键词指标比普通 BLEU 更贴近人工判断，却仍不能替代可执行验证或真实开发者采纳结果。
- 检索增强不是天然有益：领域模型可能认为模板冗余，prompt 分布变化还会干扰输出。
- isolated diff 可以支持大量模式型安全审查，但跨函数、状态和生命周期问题需要更广且更准确的程序证据。

## 14. 对当前研究的启发

最新研究记录已经把主线从通用 SWR-Bench 转向 secure code review / vulnerability repair，并发现 SecureReviewer 数据对 security baseline 很合适，却缺少 commit SHA、PR、file path 等 repository provenance。本文全文进一步确认了这个定位：它是**安全 reviewer baseline**，不是 repository-level context benchmark。

第一，它可以提供一个可复现的 diff-only control。当前若研究额外 repository context 的作用，可先复现 SecureReviewer 或其 prompt/task schema，固定 diff 与输出四字段，再增加 caller/callee、生命周期或其他仓库证据。这样 treatment 是上下文变化，而不是同时换任务定义和评价格式。

第二，四字段可以进一步拆成当前因果分析需要的 outcome：ST 对应漏洞类型判断，D 可编码 mechanism correctness，I 对应后果链，A 对应修复行动。尤其可以把“ST 正确但 D 的代码归因错误”单独建模，而不是让 SecureBLEU 的单分数掩盖机制偏移。

第三，论文的 RARG 负结果几乎是 plausible-context hypothesis 的现成机制先例：模板与任务高度相关、看起来合理，但对已经内化领域知识的模型可能冗余，甚至因训练—推理格式不一致而降低表现。不过它只能证明系统级异质性，不能作为“仓库代码 plausible noise 会误导”的直接证据，因为检索对象是评论模板，不是程序依赖证据。

第四，Concurrency 值得作为优先子集，但不能把整个 SecureReviewer test 当作 call-graph-heavy benchmark。研究记录已抽查到前 20 条并发样本中强 call-graph/callee-semantics 相关约 7 条；更合理的下一步是从全数据按 evidence need 重标，再设 diff-only、diff+required repository evidence、diff+plausible matched context 三个条件，而不是把所有安全类型一起平均。

最后，当前最大的工程障碍仍是 provenance。公开 SecureReviewer 数据没有稳定 commit SHA、PR number 与 file path，无法直接冻结 repository snapshot。若不能重建上游 CodeReviewer case，就应保守地把它用于 baseline 与 outcome schema；真正的 repository-level 因果干预应转向有可回放 snapshot 的数据，或单独构建一个经人工证据审计的小型 SecureReviewer-derived 子集。
