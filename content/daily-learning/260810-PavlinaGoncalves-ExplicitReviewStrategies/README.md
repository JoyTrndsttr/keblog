# Do Explicit Review Strategies Improve Code Review Performance? Towards Understanding the Role of Cognitive Load

> 精读日期：2026-08-10  
> 论文：*Do Explicit Review Strategies Improve Code Review Performance? Towards Understanding the Role of Cognitive Load*  
> 作者：Pavlína Wurzel Gonçalves, Enrico Fregnan, Tobias Baum, Kurt Schneider, Alberto Bacchelli  
> Venue：Empirical Software Engineering 27(4), 2022  
> DOI / 原文：[10.1007/s10664-022-10123-8](https://doi.org/10.1007/s10664-022-10123-8)  
> 来源：从 `dialog.md` 的每日学习历史迁移  

## 一句话价值

随机比较自由审查、普通清单和引导式清单，显示干预效果会随任务复杂度改变。

## 历史精读正文

### 论文信息

**题目：** *Do Explicit Review Strategies Improve Code Review Performance? Towards Understanding the Role of Cognitive Load*
**作者：** Pavlína Wurzel Gonçalves、Enrico Fregnan、Tobias Baum、Kurt Schneider、Alberto Bacchelli
**期刊：** *Empirical Software Engineering*，27(4)，Article 99，2022
**类型：** 随机分组实验；研究设计曾以 Registered Report 形式在 MSR 2020 预注册
**原文：** [期刊与 DOI](https://doi.org/10.1007/s10664-022-10123-8)｜[复现包](https://doi.org/10.5281/zenodo.5653341)｜[预注册](https://doi.org/10.17605/OSF.IO/5FPTJ)

#### 一句话结论

审查辅助不是越强制、越细粒度越有效：普通清单在复杂任务中表现较好，而逐步引导仅在简单任务中显出优势，说明**任务难度和审查者自主性可能是重要的效应修饰变量**。

### 速读导航

| 章节                | 建议 | 需要带走什么                             |
| ------------------- | ---- | ---------------------------------------- |
| Introduction        | 快读 | 问题是“指导是否通过降低认知负荷改善审查” |
| Sec. 2.1            | 扫读 | 认知负荷、工作记忆和缺陷发现的关系       |
| Sec. 3              | 必读 | Treatment、Outcome 和预期中介机制        |
| Sec. 4.2–4.5        | 必读 | 三种干预、任务设计、指标和随机分组       |
| Fig. 8              | 扫图 | 完整实验流程                             |
| Sec. 4.6–4.7        | 必读 | 原计划的中介分析为何无法执行             |
| Table 6、Fig. 10–12 | 必读 | 各任务的低基准表现和异质性               |
| Table 8–11          | 快读 | 回归结果；不必逐项解读所有系数           |
| Sec. 6              | 必读 | 自主性、任务难度与认知投入的解释         |
| 公式和附录          | 可跳 | 不是论文的关键贡献                       |

**如果只有30分钟：**Sec. 3 → Sec. 4.2–4.7 → Table 6 → Table 8 → Sec. 6。

### 研究问题与因果结构

论文实际研究两条路径：

```text
审查指导方式 ─────────→ 审查效果/效率
      └→ 认知负荷 ───→ 审查效果/效率
```

- Treatment：
  1. 自由审查；
  2. 普通清单；
  3. 引导式清单。
- Mediator：审查过程中的认知负荷。
- Outcomes：
  - effectiveness：发现缺陷的比例；
  - efficiency：单位时间发现的缺陷数。
- 潜在 effect modifiers：
  - 任务复杂度；
  - 审查经验；
  - 对目标系统的熟悉程度。

引导式清单不只是提供相同内容，还会逐类、逐方法控制审查顺序、突出当前代码块并隐藏无关信息。因此它改变了指导强度、交互流程、耗时和自主性，而不是单纯改变“是否有清单”。

### 实验设计

- 共招募70名具有专业Java开发经验的参与者；
- 清洗后分析67人；
- 71.6%的参与者很少或从不进行代码审查，可视为新手审查者；
- 参与者随机分配到三个 treatment；
- 每人完成三个审查任务：
  - 一个较小变更；
  - 两个较复杂变更；
- 每次审查后使用标准化问卷测量认知负荷；
- 清单和引导式清单均包含相同的18个检查项。

主要分析包括 ANOVA、Tukey 检验和回归；作者原计划做中介分析，但前置条件没有满足。

### 核心结果

1. 三个任务的平均缺陷发现率都很低：

   - 小变更：12.5%
   - Large Change A：7.53%
   - Large Change B：2.41%

2. 在最复杂的 Large Change B 中：

   - 普通清单对效率的回归结果达到 `p < 0.05`；
   - 对效果仅达到 `p < 0.1`；
   - 引导式清单没有稳定优势。

3. 引导式清单在小任务中的效果与更高 effectiveness 存在 `p < 0.05` 的关系，但加入控制变量后，该关系消失。

4. 普通清单在 Large Change B 中降低了认知负荷（`p < 0.01`），但整体上无法证明：

   > 指导 → 降低认知负荷 → 提高审查表现

5. 引导式清单组平均多花约30分钟；两种工具的可用性均被评为 D，属于较差水平。

这些结果更适合称为“初步和情境依赖的证据”，不能总结成“清单能普遍改善代码审查”。

### 最值得反思的设计问题

#### 1. 中介效应并未得到验证

作者原本想验证“指导通过降低认知负荷改善表现”，但 treatment 与 outcome 缺少稳定的总效应，加之 outcome 方差过低，最终没有完成正式中介分析。

因此，“认知负荷是机制”仍属于未确认假设。

#### 2. 审查时间可能不是普通混杂变量

引导式清单本身使参与者多花约30分钟，因此 review time 很可能是 treatment 的结果：

```text
指导方式 → 审查时间 → 缺陷发现
```

如果在回归中直接控制审查时间，可能阻断一部分真实效应；若审查时间还受其他未测因素影响，也可能引入 collider bias。未来实验应事先明确它究竟是：

- outcome；
- mediator；
- 成本指标；
- 还是确实需要调整的 pre-treatment confounder。

#### 3. 任务难度是核心效应修饰变量

简单任务和复杂任务出现相反模式，不应只报告总体平均效应。更合理的是预先定义：

\[
CATE(d)=E[Y(1)-Y(0)\mid Difficulty=d]
\]

即分别估计不同难度下的条件平均处理效应。

### 与 Causality for Code Review 的联系

这篇论文可以直接启发你的干预实验，例如研究 repository context、call graph 或 LLM review guidance：

- Treatment：无仓库上下文、静态仓库上下文、交互式/逐步上下文；
- Outcome：review-point hit rate、误报率、审查时间；
- Mediator：代码理解程度、认知负荷、查看文件数量；
- Moderator：任务难度、缺陷是否跨文件、审查者经验；
- Cost outcome：token、等待时间和人工操作次数。

最重要的是，不要默认“更多上下文/更多指导必然更好”。它可能提高简单任务表现，却在复杂任务中因增加流程负担而降低效果。

### 可直接借鉴的三点

1. 使用 **3-arm randomized experiment**，把“无辅助、轻量辅助、强引导辅助”分开。
2. 将任务难度预注册为 effect modifier，报告分层效应而不只报告总体均值。
3. 同时测量质量和成本，但不要把可能由 treatment 造成的时间、token 或操作次数随意当作混杂变量控制。

### 最终 Takeaway

- 随机分组使 treatment 的总效应具备因果解释基础。
- 结果没有证明细粒度指导普遍有效。
- 任务复杂度和审查者自主性可能决定干预效果。
- 极低的缺陷发现率使中介分析失效，也削弱了统计功效。
- 对你的研究而言，最有价值的是“分层处理效应＋明确中介变量”的实验设计。

> **如果一周后只记得一件事：代码审查辅助的效果取决于任务难度；更强的引导可能同时增加帮助和干扰。**

**阅读优先级：★★★★★**
**建议时间：30—45分钟**
**值得阅读全文：**方法与讨论值得读，背景和公式可以跳过。
