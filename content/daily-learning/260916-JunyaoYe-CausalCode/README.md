# A Causal Learning Framework for Enhancing Robustness of Source Code Models

> **作者**：Junyao Ye; Zhen Li; Xi Tang; Deqing Zou; Shouhuai Xu; Weizhong Qiang; Hai Jin  
> **Venue**：Proceedings of the ACM on Software Engineering, Vol. 2, FSE 2025, Article FSE117  
> **DOI**：[10.1145/3729387](https://doi.org/10.1145/3729387)  
> **代码**：[CGCL-codes/CausalCode](https://github.com/CGCL-codes/CausalCode)  
> **荣誉**：ACM SIGSOFT Distinguished Paper Award

## 论文地图

过去提升代码模型鲁棒性主要靠 adversarial training 或 contrastive learning：前者把攻击样本塞回训练集，后者拉近同源变体、推远不同样本。但作者认为，两者主要在扩展数据分布，并没有从生成机制上切断“代码风格特征—标签”的伪相关。

CausalCode 的解法分两步：先把变量名、死代码等风格因素视为可干预变量，沿着能降低模型正确预测置信度的方向生成语义保持的 intervention examples；再让原样本与其干预版本在表示空间中靠近，同时保留任务损失。实验覆盖 CodeBERT、GraphCodeBERT、StarCoder2-3B，四类任务和多种随机/对抗攻击。结果表明它总体上比 adversarial training、contrastive learning 和 CausalVul 更稳健，但“学到了真正因果特征”这一主张仍强于现有证据。

## 1. 论文到底想解决什么问题？

代码模型可能在正常测试集上很准，却会因变量重命名、插入不可达死代码等不改变程序语义的操作而预测翻转。作者把原因解释为模型依赖了 **spurious features**：它们在训练数据中与标签相关，却不是决定程序功能或缺陷的原因。

例如缺陷检测中，真正决定标签的可能是危险 API 调用、错误处理和数据流；变量叫 `t` 还是 `dict` 不应改变缺陷。功能分类中，循环与累加逻辑决定“求和”语义，而 `if false { ... }` 之类死代码不应改变类别。若模型会因此出错，就说明它在利用表面 shortcut。

作者指出既有方法有三点不足：

- adversarial training 和普通 augmentation 主要扩充经验分布，不保证切断伪相关；
- 代码扰动策略缺少区分 causal/spurious feature 的理论解释；
- 已有防御仍可能保持很高的 Attack Success Rate（ASR）。

因此本文的问题不是“怎样再造一种攻击”，而是：

> 能否利用代码的语义保持变换主动干预风格特征，并通过表示不变性训练，让模型减少对这些特征的依赖？

## 2. 必须先分清：这里的“因果”是哪一种因果？

这篇更接近 **causal representation learning / invariant learning**，不是估计 ATE、CATE 或处理观察数据混杂的传统 causal effect identification。

作者建立的 Structural Causal Model 包含：

- `C`：不可观测混杂，如开发者经验或开发环境；
- `S`：程序语义；
- `F`：风格因素，如 identifier、格式和死代码；
- `X_S`：由语义产生的特征；
- `X_F`：由风格产生的特征；
- `X`：最终代码输入；
- `Y`：任务标签。

其关键结构是：`C` 同时影响 `S` 和 `F`，形成 `F ← C → S` 的 backdoor path；标签 `Y` 由语义特征 `X_S` 决定，但模型训练时可能同时利用 `X_S` 与 `X_F`。

作者对 `F` 做干预：

\[
F := f, \qquad f \sim P(F)
\]

希望切断 `C → F`，使：

\[
P(S\mid do(F))=P(S)
\]

直觉是：随机改变变量名或插入语义无关代码，程序语义和标签保持不变。若模型仍保持预测，说明它较少依赖被干预的风格特征。

这里需要守住一个边界：代码变换确实能提供比自然语言更可控的“主动操纵”，但一次 rename 会同时改变 tokenization、embedding 与 attention pattern，所以它并不是只拨动一个完全隔离的因果变量，而是模型输入空间中的复合干预。

## 3. CausalCode 的整体流程

```text
原始训练集 D1 + 非鲁棒模型 M
↓
扫描可做语义保持变换的位置
↓
沿使任务损失增大的方向多步采样
↓
生成一个或多个 intervention dataset D2...DV
↓
把同一原程序及其干预版本按行对齐
↓
任务损失 + 表示距离损失联合训练
↓
周期性重生成干预数据，动态调节损失权重
↓
鲁棒模型 M+
```

它和普通 adversarial training 的关键区别，不是有没有生成困难样本，而是把同语义样本组织成明确配对，并要求其内部表示保持一致。

## 4. Step 1：怎样生成 intervention examples？

### 4.1 为什么既不是纯随机，也不是标准攻击？

纯随机扰动覆盖面广，但大多数样本对当前模型没有挑战；标准 adversarial attack 通常一旦骗过模型就停止，只探索到一条局部攻击路径。CausalCode 借鉴 PGD 的思想，在离散代码变换空间里进行多步、多路径搜索。

第 `t` 步先对当前样本的可干预位置应用候选替换，得到候选集：

\[
\mathcal{S}_t=\bigcup_{j=1}^{m} Transform(x_t,r_j)
\]

然后保留最贴近梯度方向的 Top-k 候选，并从中均匀采样下一步：

\[
x_{t+1}\sim Uniform(Top_k(\mathcal{S}_t))
\]

“Top-k 后再随机”有两个目的：维持对模型有挑战的下降方向，同时避免每次都贪心选择同一路径、陷入局部最优。

### 4.2 候选怎么评分？

论文用候选与原样本 embedding 差向量，和任务损失相对原 embedding 的梯度做对齐：

\[
SC(x_{ij}^{s},x_i)=
\frac{v(x_{ij}^{s})-v(x_i)}{\|v(x_{ij}^{s})-v(x_i)\|_2}
\cdot
\frac{\partial L(y,M(x_i))}{\partial v(x_i)}
\]

直觉上，第一项表示“这个代码变换把表示往哪里推”，第二项表示“往哪里推最能增大损失”。分数越高，变换越接近模型当前的脆弱方向。作者只需对原 identifier 计算一次梯度，因此声称开销与生成 adversarial examples 相当。

### 4.3 具体可干预什么？

正文重点展示 identifier replacement，并在实验中同时覆盖 identifier manipulation 和 dead-code insertion。所有变量名和函数名都可作为 intervention point；identifier 候选来自数据集中符合命名规则的字符串，实验把候选集上限设为 5,000。

每个样本的迭代次数在 `1...iter_max` 中随机选择。分类任务 `iter_max=30`；代码翻译为 10；代码精炼为 20。对每个原样本可生成 `V-1` 个干预版本，形成多个等规模数据集。

## 5. Step 2：怎样学习 invariant representation？

同一原程序的不同干预版本语义相同，因此作者要求它们的表示尽量接近：

\[
\mathcal{L}_{Causal}=\sum_{i,j_1\neq j_2}
dist\left(\Phi(x_i^{(j_1)}),\Phi(x_i^{(j_2)})\right)
\]

只最小化距离会出现表示塌缩：所有输入都映射成同一个向量，距离当然为零，却没有任务信息。因此还要保留分类交叉熵或生成任务损失：

\[
\mathcal{L}_{CausalCode}=\lambda\mathcal{L}_{Causal}+\mathcal{L}_{Task}
\]

训练开始时 `λ=0`，前 `N_s` 个 epoch 只学任务；之后加入 causal loss。若总损失下降，就把 `λ` 增加 0.1，直到 1；不下降则减 0.1。每隔 `r` 个 epoch 重新生成除原始集外的 intervention datasets。

这里论文正文定义的是一般距离（如 L2），核心目标是 **paired representation alignment**，并不是严格估计 Wasserstein distance，也没有直接识别一组可命名的“真实因果语义变量”。

## 6. 实验设计

### 数据集与任务

| 任务 | 数据集 | 规模 | 主要指标 |
|---|---|---:|---|
| 功能分类 | POJ-104 | 51,976 个程序，104 类 | Accuracy、Δdrop、ASR |
| 缺陷检测 | CodeChef | 33,822 个程序，OK/WA/TLE/RE 四类 | Accuracy、Δdrop、ASR |
| Java→C# 翻译 | CodeTrans | 11,800 对函数 | CodeBLEU、Δdrop |
| Java 代码精炼 | Bugs2fixs | 65,454 对 buggy/fixed 函数 | CodeBLEU、Δdrop |

分类数据按 64%/20%/16% 划分 train/test/validation。生成任务沿用 CodeAttack 配置；代码精炼使用 46,680/5,835/5,835 的 train/validation/test。作者对测试集均匀抽取 20%，重复攻击 5 次并报告均值。

### 模型、攻击与 baseline

- 模型：CodeBERT、GraphCodeBERT；缺陷检测额外测试 StarCoder2-3B。
- 随机扰动：RP-Identifier、RP-DeadCode。
- 分类攻击：MHM、CARROT-Identifier、CARROT-DeadCode。
- 生成攻击：CodeAttack；筛除语法/语义不一致样本后，为每例选 top-5 攻击样本。
- 防御 baseline：CARROT-T、ALERT-T、ContraBERT、CausalVul。

这套比较覆盖 adversarial training、contrastive learning 和既有 causal-learning defense，范围是充分的。但预算公平仍不完全透明：不同方法用多少增强样本、搜索成本、预训练成本和总 GPU 时间，没有在主表里统一报告。

## 7. RQ1：能否提升分类模型的性能与鲁棒性？

### 问题与设计

作者在功能分类和缺陷检测上，对 CodeBERT/GraphCodeBERT 施加两类随机扰动与三类高级攻击；同时在 StarCoder2-3B 的缺陷检测上重复比较。

### 结果

随机扰动下，CausalCode 相对未增强模型平均提高 Accuracy 1.25 个百分点、降低 ASR 31.95 个百分点。代表性结果包括：

- CodeBERT + POJ-104 + RP-Identifier：ASR 从 35.71% 降至 7.32%；
- GraphCodeBERT + POJ-104 + RP-DeadCode：ASR 从 13.78% 降至 2.29%；
- CodeBERT + CodeChef + RP-DeadCode：ASR 从 50.95% 降至 15.35%；
- GraphCodeBERT + CodeChef + RP-DeadCode：ASR 从 49.93% 降至 10.08%。

高级攻击下，CausalCode 在两种分类任务上也总体最优。论文汇总称功能分类中相对原模型平均降低 ASR 30.16 个百分点；死代码攻击上的提升通常强于 identifier 攻击。例如 CodeBERT 的 CARROT-Identifier ASR 从 71.97% 降至 19.82%，CARROT-DeadCode 从 27.20% 降至 5.68%。

StarCoder2-3B 并非天然稳健。在 CodeChef 上，原模型面对 CARROT-Identifier 时 Accuracy 从 77.60% 降到 3.80%（Δdrop 73.80，ASR 95.23%）；CausalCode 将 Δdrop 降到 34.42、ASR 降到 39.61%。作者同时发现 StarCoder2 在 POJ-104 上退化不超过约 10%，并明确提醒 POJ-104 属于 CodeXGLUE、进入过相关预训练数据，加之 FIM 目标可能增强局部扰动鲁棒性，因此不能把这一现象简单归因于“大模型更鲁棒”。

### 含义

CausalCode 在当前攻击族和数据集上确实提供了稳定、幅度较大的鲁棒性收益，且没有以明显牺牲 clean accuracy 为代价。但它最强地证明的是 **对所选 transformation family 的鲁棒性**，而不是一般意义上的语义理解。

## 8. RQ2：模型真的学到了 causal features 吗？

作者用 POJ-104 随机选择 5 类、每类 100 个能骗过 CodeBERT 的 adversarial examples，通过 `[CLS]` 表示做 T-SNE 和 K-means 分析。

四种方法的聚类 distortion distance 为：

| 方法 | Distortion distance（越低越好） |
|---|---:|
| ContraBERT | 0.552 |
| CARROT-T | 0.531 |
| ALERT-T | 0.380 |
| CausalCode | **0.285** |

进一步将每个 adversarial example 与原始样本做最近邻匹配：

| 模型 | Top-1 overlap | Top-10 overlap | 原样本—攻击样本平均距离 |
|---|---:|---:|---:|
| CodeBERT | 31.81% | 56.36% | 14.41 |
| +ContraBERT | 46.60% | 66.99% | 12.53 |
| +CARROT-T | 40.75% | 63.92% | 11.74 |
| +ALERT-T | 64.32% | 91.47% | 7.56 |
| +CausalCode | **93.32%** | **98.40%** | **0.94** |

这些结果很好地验证了训练目标：原样本与其语义保持变体在表示空间中更接近，同类聚类也更紧。

但 RQ2 的措辞“Can CausalCode learn causal features?”比测量证据更强。T-SNE、聚类距离和 nearest-neighbor overlap 验证的是 **intervention invariance**；它们不能排除模型改为依赖另一组未被当前变换触及的 shortcut。因此更准确的结论是：CausalCode 学到了对所选干预更稳定、与任务类别更一致的表示。

## 9. RQ3：到底是哪一部分起作用？

作者在 CodeBERT 缺陷检测上分别检查 intervention generation、regularizer 和增强数据集数量。

### 9.1 干预样本选择策略

相对 vanilla，随机样本平均降低 ASR 9.30 个百分点，adversarial examples 降低 16.70，而 CausalCode 的 causal examples 平均降低 38.18。这说明收益不能简单归因于“数据变多”；沿梯度方向但继续覆盖变换空间的选择策略更有效。

### 9.2 损失函数

移除 causal regularizer、只用 classification loss，clean accuracy 略升 0.46 个百分点，但 ASR 相比 causal loss 高 21.32 个百分点；contrastive loss 的 ASR 降幅也比 causal loss 少 33.19 个百分点。

这支持 paired invariance objective 有独立贡献。不过表 5 没有给置信区间或显著性检验，而且只在一个模型/任务组合上做消融，外推到四类任务需要谨慎。

### 9.3 增强数据量

从 1 份增强集增加到 3 份，MHM ASR 从 30.25% 降到 25.84%，CARROT ASR 从 33.76% 降到 26.98%；增加到 4 份反而略回退到 27.47% 和 28.19%。因此“更多干预样本更鲁棒”只在一定范围内成立，存在边际收益和轻微反转。

## 10. RQ4：能否扩展到代码生成？

在 clean performance 上，CausalCode 对代码翻译平均提高 CodeBLEU 1.18 个百分点，对代码精炼提高 0.43 个百分点。

| 模型 | 翻译 CodeBLEU / Δdrop | 精炼 CodeBLEU / Δdrop |
|---|---:|---:|
| CodeBERT | 82.36 / 16.26 | 87.88 / 6.13 |
| CodeBERT + CausalCode | **83.62 / 13.22** | **88.33 / 5.13** |
| GraphCodeBERT | 82.57 / 16.47 | 87.95 / 10.64 |
| GraphCodeBERT + CausalCode | **83.67 / 16.24** | **88.36 / 10.14** |

作者汇总称，相对 baseline，CausalCode 在代码翻译和精炼上分别平均降低 Δdrop 1.63 和 0.76 个百分点，优于 CARROT-T 与 ALERT-T。效果方向一致，但明显小于分类任务；GraphCodeBERT 翻译任务的 Δdrop 只改善 0.23，说明“task-agnostic”更多是可适用性，而不是各任务收益同样强。

## 11. 证据链审计

### 11.1 论文明确支持的部分

1. 语义保持代码变换可以构造标签不变、风格变化的 paired examples。
2. 梯度引导的多步干预样本选择优于本文实现的随机选择与普通 adversarial selection。
3. paired representation regularization 对鲁棒性有独立贡献。
4. 在本文四个任务、所选模型和攻击下，CausalCode 大多优于比较方法。
5. 原样本与攻击样本的表示距离显著缩小，证明优化目标确实被实现。

### 11.2 论文没有充分证明的部分

1. **没有证明模型识别了“真正的 causal program semantics”。** 当前证据也可由 attack-family-specific invariance 解释。
2. **没有做跨 intervention family 的严格外推。** 最强检验应是训练时只见 identifier rename，测试完全未见的结构或数据流保持变换。
3. **没有完整排除数据泄漏。** StarCoder2/POJ-104 的预训练重叠已被作者承认，其他预训练模型与数据集的重叠没有系统审计。
4. **没有证明预算公平。** 样本量、搜索查询、预训练成本与 GPU 时间未在主实验统一对齐。
5. **没有充分报告统计不确定性。** 随机攻击表有 ± 值，但高级攻击、生成任务和消融表缺少统一的区间与显著性分析。
6. **生成任务的语义有效性依赖筛选。** 作者剔除了 CodeAttack 中语法或语义不一致的样本，但筛选规则、人工判断一致性和选择偏差没有充分展开。
7. **缺少现代 agent/LLM 场景。** StarCoder2-3B + classification head 不能代表 instruction-tuned LLM 或 Coding Agent 的长上下文行为。
8. **Table 2 存在值得复核的异常值。** CausalVul 在 MHM 下同时出现很小的 `Δdrop`（6.52/7.08）和很高的 ASR（69.76%/64.86%），与相邻结果及两个指标通常的方向关系不协调；在作者未提供解释前，不宜据此做方法间细粒度排名。

## 12. 论文自身承认的局限

作者列出三点：干预搜索目前依赖沿梯度方向的多次随机采样，仍可研究其他 sampling；防御更多种攻击仍有挑战；因果学习可能同时改善鲁棒性与可解释性，但本文没有验证解释性。

还应补充外部有效性限制：只有两个 encoder 模型和一个 3B decoder，任务以函数级数据集为主；identifier/dead-code 不能代表所有 spurious feature；功能分类和四分类 CodeChef 与真实仓库级审查差异很大。

## 13. 与 Causality for Code Review 的关系

CausalCode 最值得借鉴的不是直接把它的 loss 移植到代码审查，而是它的实验哲学：**主动构造保持 ground truth 不变的 intervention，而不是等待自然数据里的 context variation。**

你的研究可以对应为：

```text
CausalCode：改变风格 F，保持语义 S 与标签 Y 不变

Context Causality：改变上下文 C，保持 diff 与 review ground truth 不变
```

对一个确定为 diff-local 的审查实例，可构造：

- `T0`：Diff only；
- `T1`：Diff + 1 个无关 caller；
- `T2`：Diff + caller/callee 噪声；
- `T3`：Diff + full call graph；
- `T4`：总 token 数相同，但把噪声替换为真正 relevant context。

这样能分别操纵 context relevance、noise ratio、graph distance 和 evidence density，并测量 Review Precision、false-positive narrative、证据引用、token/trajectory 分配。

AACRBench 的 diff / in-file / repo 分级还天然支持异质处理效应：

\[
Effect(Context\mid Need=1)>0
\]

\[
Effect(Context\mid Need=0)<0
\]

相较只比较 `CG vs No-CG`，更强的论文问题是：在 review ground truth 不变时，相关性、数量、结构距离与噪声比例的可控干预，如何通过 evidence use / attention allocation / reasoning trajectory 影响最终审查质量？

## 14. 真正应该记住什么

- CausalCode = **梯度引导的语义保持干预数据生成 + paired representation invariance + task loss**。
- 它不是 ATE/CATE 式因果推断，而是 causal representation / invariant learning。
- 分类任务上的鲁棒性提升很强；生成任务方向一致但幅度较小。
- RQ2 真正证明的是 representation 对所选干预更不敏感，并未证明模型已经掌握真实程序因果语义。
- 最有价值的研究方法是：主动改变疑似 spurious variable、固定语义和标签，再观察模型行为，而不是把自然相关直接解释为因果。
- 对你当前课题，最值得迁移的是 **semantic-preserving transformation → ground-truth-preserving context intervention**，并进一步加入 mediator，解释为什么无关 repository context 会让代码审查变差。
