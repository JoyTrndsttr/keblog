# The Effect of Complexity and Provenance on Code Review Decisions: Evidence from a Controlled Experiment

> 精读日期：2026-08-29  
> 论文：*The Effect of Complexity and Provenance on Code Review Decisions: Evidence from a Controlled Experiment*  
> 作者：Neha Singh, Francesco Sovrano, Vincent J. Hellendoorn, Alberto Bacchelli  
> Venue：FSE 2026 / Proceedings of the ACM on Software Engineering 3  
> DOI / 原文：[10.1145/3808165](https://doi.org/10.1145/3808165)  
> 来源：从 `dialog.md` 的每日学习历史迁移  

## 一句话价值

受控实验发现复杂任务与接受错误修订相关，但任务材料差异限制了纯复杂度因果解释。

## 历史精读正文

## 4. 每日论文极速精读

### 复杂任务真的会让审查者更容易接受错误代码吗？

- **标题**：*The Effect of Complexity and Provenance on Code Review Decisions: Evidence from a Controlled Experiment*
- **作者**：Neha Singh、Francesco Sovrano、Vincent J. Hellendoorn、Alberto Bacchelli
- **Venue**：FSE 2026，*Proceedings of the ACM on Software Engineering*, Vol. 3
- **DOI**：[10.1145/3808165](https://doi.org/10.1145/3808165)
- **数据与材料**：[Zenodo](https://doi.org/10.5281/zenodo.19481940)

**一句话结论：** 在这项实验中，复杂任务条件下的审查者更容易接受错误修改，而“AI/人类生成”标签没有主效应；但由于复杂度条件使用了不同代码和不同缺陷，这不能被严格解释为复杂度本身的因果效应。

### 速读导航表

| Section                    | 阅读建议        | 只需要带走什么                                     |
| -------------------------- | --------------- | -------------------------------------------------- |
| Sec. 1 Introduction        | 快读            | 论文要区分代码复杂度和 AI 来源标签对审查决策的影响 |
| Sec. 2 Background          | 跳过 / 扫一眼   | 理解 automation bias、provenance、compliance 即可  |
| Sec. 3 Study Design        | **必读**        | 2×2×2 随机实验到底改变了哪些因素                   |
| Fig. 1、Table 1            | **扫图 / 扫表** | 审查界面以及八种实验条件如何组合                   |
| Sec. 4.1–4.2               | **必读**        | 复杂度主效应和来源标签零效应                       |
| Tables 4–5、8–9            | **必读**        | 原始人数分布、回归结果和效应大小                   |
| Sec. 4.3                   | 快读            | 正式交互不显著；分组显著只是探索性发现             |
| Sec. 5 Qualitative Results | 扫表            | 参与者如何解释对 AI 和人类代码的态度               |
| Sec. 6 Discussion          | 快读            | 作者怎样将结果解释为复杂度驱动的 automation bias   |
| Sec. 7 Threats             | **必读**        | 单一代码片段、缺陷不匹配和外部有效性问题           |

**如果只有 25 分钟，按这个顺序读：**

Sec. 3 实验设计
→ Fig. 1
→ Tables 4–5
→ Table 8
→ Sec. 4.3 的正式交互检验
→ Sec. 7 Threats
→ Discussion 中关于复杂度的解释

### 论文地图

过去关于 AI 辅助代码审查的讨论，常把审查错误归因于“人们是否信任 AI”。这篇论文提出另一个可能性：真正影响审查决策的可能不是来源标签，而是任务是否足够复杂。

作者采用一个 2×2×2 随机实验：

> 代码复杂度 × 显示来源 × 修改正确性 → 参与者接受或拒绝修改

最重要发现是：复杂任务条件出现更多 over-compliance；AI 标签没有显著主效应。

#### 四个必要概念

- **Compliance**：接受正确修改，或者拒绝错误修改。
- **Over-compliance**：接受了错误修改，是本文最值得关注的风险。
- **Under-compliance**：拒绝了正确修改。
- **Provenance**：界面告诉参与者建议来自“人类开发者”还是“Generative AI Bot”。实际代码全部由研究者准备，因此这只是标签干预。

### 研究动机：究竟是 AI 标签，还是任务难度？

作者的逻辑是：

1. 审查者可能因为 automation bias 而过度接受 AI 建议。
2. 复杂代码会增加认知负担。
3. 因此，复杂度可能放大人们对 AI 建议的依赖。

前两点有相关研究支持，但第三点在实验前仍属于待验证假设。

这里有一个隐藏前提：实验中的 low/high 条件必须主要只在“复杂度”上不同。实际并非如此——两组使用不同代码片段、算法结构和缺陷类型。这构成了论文最关键的识别问题。

### 方法全貌

#### 输入

- 385 名具有 Python 能力的参与者。
- 每人只审查一个修改。
- 八种随机条件：
  - 低复杂度 / 高复杂度；
  - 人类标签 / AI 标签；
  - 正确修改 / 错误修改。

#### 步骤一：随机分配实验条件

随机分配能平衡参与者经验、态度等前置差异。

**必要性：** 避免熟练参与者集中进入某个条件。

**局限：** 它只能平衡“人”，不能修复 treatment 定义。高低复杂度各自只有一个不同的程序，因此任务本身仍与复杂度完全重合。

#### 步骤二：展示代码修改和来源标签

参与者看到原代码、建议修改，以及“Human Developer”或“Generative AI Bot”标签。

这是一个 Wizard-of-Oz 设计：标签被操纵，但代码实际来源没有改变。

**因此论文估计的是：**

> 告诉审查者代码来自 AI 的效果

而不是：

> AI 实际生成的代码与人类代码质量差异所产生的效果。

#### 步骤三：记录接受或拒绝

结合修改是否正确，将决策分成 appropriate、over-compliance 和 under-compliance。

这个分类比单纯 acceptance rate 更有意义，因为“接受”只有结合代码是否正确才能判断好坏。

#### 步骤四：统计检验

- 卡方检验比较三类审查结果。
- Cramér’s V 表示效应大小。
- Logistic regression 分析接受概率。
- Log-linear model 检验 complexity × provenance × compliance 三向交互。
- Holm correction 控制多重比较。

公式推导不是创新点，可以跳过；重点看原始频数和交互检验。

### RQ1：复杂任务是否改变审查决策？

#### 实验结果

| 条件     | Under-compliance | Appropriate | Over-compliance | 合计 |
| -------- | ---------------: | ----------: | --------------: | ---: |
| 低复杂度 |               19 |         113 |              44 |  176 |
| 高复杂度 |               12 |         115 |              82 |  209 |

- 低复杂度 over-compliance：**25.0%**
- 高复杂度 over-compliance：**39.2%**
- 绝对差异：约 **14.2 个百分点**
- χ²(2)=10.306，p=.0058
- Cramér’s V=.16，属于小效应

回归中，高复杂度条件的系数为 0.853，对应接受修改的 odds ratio 约为 **2.35**。

#### 这个结果能支持多强的 claim？

**论文报告的事实：** 被分配到高复杂任务包的人更常接受修改，并出现更多 over-compliance。

**合理解释：** 较难理解的任务可能降低了参与者识别错误的能力。

**论文没有严格证明：** 单独增加代码复杂度，会导致 over-compliance 上升14.2个百分点。

原因是高低条件不仅复杂度不同，代码、算法结构和缺陷形式也不同。更准确的 causal estimand 是：

> 被分配到“高复杂度代码任务包”相对于“低复杂度代码任务包”的效果。

**读完这一部分只需要记住：** 结果很有启发，但不能把任务包差异直接等同于纯复杂度效应。

### RQ2：AI 标签是否影响审查决策？

| 标签  | Under-compliance | Appropriate | Over-compliance | 合计 |
| ----- | ---------------: | ----------: | --------------: | ---: |
| Human |               13 |         108 |              53 |  174 |
| AI    |               18 |         120 |              73 |  211 |

- χ²(2)=1.066
- p=.5867
- provenance 回归项同样不显著，p=.704

相比之下，修改本身是否正确是最强预测因素，回归 odds ratio 约为 **3.42**。

但 AI 标签操纵并不完美：AI 条件中只有 174/211，即约 **82%** 的参与者注意到了标签。

**作者证明了什么：** 在这个一次性、低风险、简化的代码审查界面中，没有观察到 AI 标签的平均主效应。

**作者没有证明什么：** 开发者在真实项目里不受 AI 来源影响，也没有证明实际 AI 生成内容与人类内容等价。

**读完这一部分只需要记住：** “来源标签无显著影响”是特定实验环境下的零结果，不能推广成“provenance 不重要”。

### RQ3：复杂度是否特别放大对 AI 的服从？

正式三向交互检验结果：

- Δχ²(2)=2.16
- p=.34

因此没有证据证明复杂度对 AI 标签存在不同于人类标签的作用。

作者进一步分组后发现：

- Human 标签组：复杂度差异不显著，p=.1139
- AI 标签组：复杂度差异显著，Holm 校正后 p=.0376

这里必须避免常见误读：

> “一个子组显著、另一个不显著”不等于“两个子组之间存在显著差异”。

真正检验两者差异的是交互项，而正式交互没有通过。因而这只能作为下一项研究的探索性线索。

### Baseline、Ablation 与证据边界

这不是模型论文，没有传统 baseline 或模块消融。三个随机因素本身承担了类似消融的作用：

- 改变 complexity：观察任务包难度差异。
- 改变 provenance：隔离标签效应。
- 改变 correctness：判断参与者是否识别建议质量。
- 检验 interaction：判断复杂度是否对 AI 标签产生条件性影响。

其中 correctness 的作用最稳定；provenance 没有观察到主效应；complexity 有统计关联，但 treatment 不够“干净”。

### 局限与可质疑点

#### 作者承认的局限

- 每个复杂度只有一个代码片段。
- 高低复杂度条件的缺陷不完全一致。
- 实验是一次性、简化的 Python 代码审查。
- 资深审查者相对较少。
- 标签并未被所有参与者注意或相信。
- 交互分析统计功效有限。

#### 进一步需要警惕

1. **刺激材料与 treatment 混杂**

   高复杂度不仅意味着更复杂，还意味着不同代码、不同算法、不同缺陷。随机化无法消除这个问题。

2. **排除参与者可能引入选择偏差**

   607 人打开实验，437 人完成，最终保留385人。52人因为用时过短、动机不足或受干扰被排除。如果任务条件影响完成时间或动机，事后排除可能改变各组构成。

3. **没有任务层面的重复**

   每个复杂度只有一个刺激材料，无法建立 snippet random effect，也无法判断结果是不是由某个特殊代码片段驱动。

4. **标签实验不等于真实来源实验**

   它隔离了 perceived provenance，却没有比较真正的 AI 代码与人类代码。

5. **外部有效性有限**

   没有真实仓库上下文、审查讨论、责任压力和迭代修改。

### 对 Causality for Code Review 的直接启发

这篇论文与当前主线高度相关，尤其适合作为“随机实验仍可能识别失败”的案例。

#### 可直接迁移的变量定义

- **Treatment**：是否向审查模型或人类提供 call graph / repository context。
- **Outcome**：是否接受错误评论、错误修复或错误修改。
- **Moderator**：任务复杂度、跨文件依赖强度、调用图深度。
- **Confounder 或设计阻断因素**：缺陷类型、代码规模、项目熟悉度、语言、测试覆盖率和原始任务难度。

#### 更可靠的实验设计

不要用“简单项目A”和“复杂项目B”代表复杂度。应当：

1. 对同一个基础任务构造多个复杂度或上下文版本。
2. 在多个 repository 和 defect 上重复。
3. 采用多层 Logistic regression：
   - participant/model 层；
   - task 层；
   - repository 层。
4. 将 `repository context` 分成：
   - 无上下文；
   - 正确相关上下文；
   - 噪声或误导上下文。
5. 预注册主效应和交互效应，按 interaction 单独进行功效分析。

还可以设计：

> complexity × call-graph context × review suggestion correctness

核心 outcome 则是：模型面对错误审查建议时是否出现 over-compliance。

### 可借鉴的三个点

1. **把 acceptance 拆成正确服从、过度服从和拒绝正确建议**
   这比只报告准确率或接受率更能揭示风险方向。

2. **同时报告原始频数、效应大小和模型结果**
   Table 4 这种频数表比只有 p-value 更容易判断实际风险。

3. **Discussion 中严格区分主效应和探索性交互**
   你的论文也应明确写出哪些是假设检验，哪些只是后续研究线索。

### 最终 Takeaway

- 作者发现，高复杂任务包下的 over-compliance 从25.0%上升到约39.2%。
- 单纯显示 AI 或 Human 标签没有显著平均效应。
- 正式的 complexity × provenance 交互不显著。
- 最大威胁是复杂度与代码片段、算法和缺陷类型同时改变。
- 对你的最大启发是：因果实验不仅要随机分配，还要保证 treatment 操纵足够单一，并在多个任务上重复。

**如果一周后只记得这篇论文的一件事：随机化能平衡参与者，却不能修复一个把复杂度、代码和缺陷捆在一起的 treatment。**

- 阅读优先级：★★★★★
- 建议投入时间：30分钟
- 是否值得阅读全文：值得，但 Related Work 和统计公式可跳
- 时间有限时读：Sec. 3、Tables 4–5、Sec. 4.3、Sec. 7
