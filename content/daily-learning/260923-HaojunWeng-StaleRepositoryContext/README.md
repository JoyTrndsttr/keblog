# When Retrieval Hurts Code Completion：A Diagnostic Study of Stale Repository Context

> 精读日期：2026-09-23  
> 简称：Stale Repository Context  
> arXiv：2605.14478v1  
> 状态：2026-05-14 提交；作者注明已投 Information and Software Technology  
> 作者：Haojun Weng; Qianqian Yang; Hao Fu; Haobin Pan; Xinwei Lv  
> 主题：Code RAG、Repository Context、Temporal Validity、Plausible Misleading Context、Controlled Intervention

## 一句话结论

这篇对当前研究非常直接：它不是证明“没有 context 会变差”，而是固定同一个本地代码任务，只把跨文件 retrieval evidence 的**时间有效性**从 current 改成 stale。stale snippet 来自同一项目、同一 helper 的旧版本，因而高度 plausible，却会把模型从“不会做”主动推向“按旧仓库状态做错”。Qwen2.5-Coder-7B-Instruct 在 stale-only 下 15/17 生成旧签名调用，gpt-4.1-mini 为 13/17；current-only 两者都是 0/17 stale reference。

对我们的核心启示是：**repository-native plausible noise 不必是人工伪造的错误代码；真实仓库历史本身就能提供高度相关、语法合理、但对当前决策无效甚至冲突的 context。**

## 1. 顶层研究设计：作者到底在隔离什么？

### Research Gap

Code RAG 已经知道 cross-file context 可以帮助 completion，也已有 filtering/selective retrieval 工作证明 retrieved chunks 有正、负或中性贡献。但这些结果把很多因素混在一起：检索相关性、是否拿到必要 evidence、repository snapshot、context amount 等。

作者把问题收窄成一个很干净的诊断变量：

> 当 retrieved snippet 看起来完全像“正确项目上下文”，但来自旧 commit 时，它只是无用噪声，还是会主动把模型引向过时实现？

这与普通 random noise 不同。旧代码具有三个危险属性：

1. 来自同一个真实 repository；
2. 与当前 helper/function 高度语义和结构相关；
3. 曾经确实是正确实现，只是在当前 snapshot 已失效。

因此它天然是一类 **plausible but invalid context**。

### Research Object

作者选择生产代码中的 helper signature change：父提交中的 helper signature 作为 stale state，子提交中的 signature 作为 current state。

模型看到一个 local wrapper task，再给不同 retrieval evidence：

- `current_context_only`：Control；
- `stale_context_only`：Treatment；
- `no_retrieval`：Baseline；
- `current-top1 + stale-top2`：Mixed robustness；
- `stale-top1 + current-top2`：Mixed robustness。

所以核心因果结构可以写成：

`Temporal Validity of Retrieved Context → Generated Helper Call → Current/Stale/No-match Outcome`

### 为什么要隐藏 freshness？

作者前期发现，如果 prompt 明确告诉强模型目标 API/version/current state，模型可能自行纠错。因此正式实验使用 **No-Target-Anchor Prompting**：不告诉模型哪个 snippet 新、哪个旧，不暴露 commit freshness，也不直接给 expected current signature。

这一步很关键：否则测到的是“模型会不会服从显式版本提示”，而不是“retrieved code 本身如何影响决策”。

## 2. 数据怎么构造？为什么不是随便找旧代码？

最终只有 17 个样本，来自五个真实 Python repository：click、flask、httpx、requests、rich。

作者从 commit history 中挖 production helper 的 signature changes：parent commit 提供 stale signature，child commit 提供 current signature。样本经过质量门控，排除 test helper 等不适合作为 production dependency 的候选。

每个实例都有两套静态 call-pattern oracle：

- current oracle：符合 child commit 当前签名；
- stale oracle：符合 parent commit 旧签名。

输出因此被分为 current match、stale reference、fail-no-match。

这不是一个大 benchmark，而是一个**小规模、强控制的 diagnostic study**。论文自己也没有把 17 个 signature changes 包装成通用 Code RAG benchmark。

## 3. RQ1：stale context 是“没帮助”，还是“主动误导”？

这是整篇最重要的结果。

在 `current_context_only` 下，两种模型 stale reference 都是 0/17。

换成 `stale_context_only`：

- Qwen2.5-Coder-7B-Instruct：15/17 = 88.2%；
- gpt-4.1-mini：13/17 = 76.5%。

更重要的是 `no_retrieval`：两种模型同样都是 0/17 stale reference，但只有 1/17 passing completion，大多数输出是 fail-no-match。

因此 stale context 的作用不是简单的：

`没有正确 evidence → 模型失败`

而是：

`提供高度 plausible 的旧 evidence → 错误类型被定向改变 → 模型按历史 repository state 生成`

这对我们比最终 accuracy drop 更重要，因为它证明了 **context can redirect the error mode**。

作者进一步分析 28 个 stale-positive outputs，其中 22 个主要错误是遗漏当前 helper 新增的参数，直接沿用了旧签名。这不是随机 hallucination，而是和 treatment 内容一致的定向错误。

## 4. RQ2/RQ3：如果正确 evidence 和错误 plausible evidence 同时存在呢？

作者做两个 mixed conditions，并交换 current/stale 的 Top-1/Top-2 顺序。

结果有两个信息。

第一，**rank order 在这个 setup 中不是主要因素**：两种模型的 aggregate rank-order delta 都是 0.0 percentage points。不能据此推广为“position 永远不重要”，只能说在这个小型双-snippet实验里没有观察到稳定 rank effect。

第二，**current evidence 的 presence 很重要**。加入有效 current snippet 后：

- Qwen stale-reference rate 从 88.2% 降到约 23.5%，下降 64.7 pp；
- gpt-4.1-mini 从 76.5% 降到约 29.4%，下降 47.1 pp。

因此作者最稳妥的机制结论不是“stale 总能压过 current”，而是：

> stale-only 会强烈诱导错误状态；当 valid current evidence 同时存在时，大多数 stale-only failure 可以被 rescue。

这和我们当前设想存在一个关键差别：我们的目标恰恰是进一步问，**当 sufficient evidence C* 已经固定存在时，plausible distractor 是否仍然比 random distractor 更危险。** 这篇 mixed result 表明这个命题并非自动成立，必须实测。

## 5. RQ4：这是单模型偶然现象吗？

不是完全独立。Qwen 在 15 个样本触发 stale reference，GPT 在 13 个样本触发；两模型 stale-triggering samples 的 Jaccard overlap 为 75%。

这说明 vulnerability 有相当一部分是 instance-specific，而不只是某个模型特有行为。但只有两个模型、17 个实例，因此不能宣称跨模型普遍规律。

## 6. 这篇与 First Drop of Ink 的关系

两篇刚好形成互补。

**First Drop of Ink**：gold evidence 固定存在；用 semantic hard distractor 替换 random/easy distractor；固定总 context length；研究低剂量 hard noise 的 nonlinear degradation，并观察 retrieval-head attention competition。

**Stale Repository Context**：真实 code repository；用同一项目旧 commit 的真实 helper code 作为 plausible conflicting evidence；重点研究错误是否被定向到 stale state；但没有做 random-vs-plausible matched comparison，也没有严格构造固定 sufficient C* 后的 dose-response。

所以对我们的 novelty 边界非常清楚：

> “plausible code context can actively mislead” 已经不能作为新 claim。

真正还可以做的是：

> **在 current/sufficient evidence 固定存在、token/file/node budget 匹配时，repository-native plausible-but-non-decisive context 是否比 matched random code 产生更强 interference；这种 interference 发生在 mechanism understanding 还是 evidence/file attribution。**

## 7. 对我们当前 VLocBench 实验最直接的改变

### 7.1 Treatment taxonomy 要加入“真实冲突证据”

目前的 random / structural sibling / plausible sibling 可以保留，但这篇提醒我们再增加一类非常强的 treatment：

`historically-valid / counterfactual-valid code`

也就是来自真实 repository lineage、在另一个 snapshot 曾经正确，但对当前漏洞 snapshot 不再决定任务的代码。

它比人工 fake distractor 更自然，也更容易回答审稿人的“这种噪声现实中会出现吗”。

### 7.2 No-context 与 random-noise 不是同一个 control

这篇用 no-retrieval 清楚显示：缺 evidence 主要产生 fail-no-match；stale evidence 则产生 treatment-aligned wrong match。

我们也应至少区分：

- `C* only`；
- `C* + random`；
- `C* + plausible`；
- `C* + competing/conflicting`。

不要把 random 当成 no-treatment。

### 7.3 Outcome 不能只有 File F1

这篇最有价值的是定义 stale-reference rate，把“错了”拆成“朝 treatment 指定的方向错了”。

对应 VLocBench，我们也需要 treatment-aligned outcome：

- 是否选中了 distractor sibling；
- 是否把漏洞 mechanism 归因到 distractor file/function；
- 是否采用 distractor 支持的 competing explanation；
- mechanism correctness 是否仍然保持；
- 最终 File F1 是否下降。

这会把 `context hurts` 升级成 `context redirects attribution`。

## 8. 因果视角：这篇强在哪里，弱在哪里？

它强在 treatment 很清楚：同一 local task、同一 helper lineage，只操纵 retrieved snippet 的 temporal validity，并加入 no-retrieval 和 mixed evidence conditions。对于这 17 个 curated instances，这是很接近 within-instance controlled intervention 的设计。

但它并没有完整识别“staleness”的纯因果效应：old/new snippets 的 token、具体参数、代码内容本身不同，temporal validity 与内容差异不可完全分离；样本还是经过 signature-change mining 与质量过滤后的选择性集合。

更重要的是 mixed condition 并未固定与 stale-only 相同的总 context budget，因此不能拿它直接回答我们想要的：

`C* fixed + plausible vs C* fixed + random under matched budget`。

所以这篇是非常强的**现象与实验范式先例**，但没有把我们的 matched counterfactual design 做完。

## 9. 作者与团队背景

公开 arXiv 页面没有给出作者机构，也没有明确标注通讯作者，因此这里不凭末位作者推断通讯作者。公开搜索对同名作者存在明显歧义：例如“Haojun Weng”可检索到复旦相关经历和其他工业资料，但无法仅凭姓名可靠确认就是本文作者；Haobin Pan 等同名结果也存在明显跨领域冲突。因此本次不强行拼接作者画像。

可以确认的是，本文的研究设计明显聚焦 Code RAG、repository evolution 与 robustness；但仅凭这一篇和歧义较大的公开作者记录，不足以声称团队长期专攻该方向。

## 10. 证据边界与审稿视角

优点很明确：问题窄、treatment 可解释、错误模式可定向归因，而且作者主动避免夸大，明确说自己不是提出新 retriever/filter，而是在隔离 temporal validity failure mode。

主要限制也很明显：

- 只有 17 个样本；
- 只覆盖五个 Python repositories；
- 只研究 helper signature change；
- temporal drift 只有 one-parent-commit；
- oracle 是静态 regex call pattern，不是执行级 correctness；
- 两个模型；
- stale/current 内容差异与“时间有效性”概念本身绑定；
- mixed evidence 的结果说明只要 current evidence 到场，很多 stale failure 会被 rescue，因此不能直接推出“plausible noise 在 gold evidence 已存在时仍然很危险”。

## 11. 真正应该记住什么

这篇最值得记住的不是“旧代码有害”，而是：

> **Repository context 的危险性可以来自它太像真的：同项目、同 helper、曾经正确。它不会只增加无关 token，而会把模型错误定向到一个具体、合理但已失效的程序状态。**

对我们来说，它同时是支持和警告。

支持：SE 场景确实存在天然的 plausible misleading context，而且可以做真实、可审计的 counterfactual intervention。

警告：当 current evidence 同时存在时，stale harm 大幅被 rescue，所以我们不能预设 `plausible > random`。真正值得发表的是严格固定 sufficient evidence 与预算后，证明是否仍有 residual interference，并进一步定位到 evidence selection、mechanism reasoning 或 file attribution。

### 原文

- arXiv：https://arxiv.org/abs/2605.14478
- arXiv DOI：https://doi.org/10.48550/arXiv.2605.14478
