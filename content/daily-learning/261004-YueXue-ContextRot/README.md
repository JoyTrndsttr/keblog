# When and How Context Rot Appears in Coding Agents: A White-Box Study of Agent Skills in Code Auditing

> 精读日期：2026-10-04  
> 作者：Yue Xue  
> 署名机构：Independent Researcher；作者主页显示现任 CertiK Head of AI Research，长期从事 blockchain/software security、smart-contract analysis 与 LLM-based auditing  
> 通讯作者：原文未明确标注，不额外推定  
> Venue / 年份：arXiv cs.SE / 2026，v2（2026-08-01）  
> 原文：https://arxiv.org/abs/2607.17937  
> Tags：Coding Agent · Long Context · Agent Skills · Code Auditing · Context Rot · Controlled Experiment · Failure Analysis

这篇论文研究的不是“模型最多能塞多少 token”，而是：**当 coding agent 已经加载正确 Skill、面对固定任务和明确要求时，周围上下文变长后，可靠性会在哪一步开始丢失？** 作者把一个 production-derived code-audit workflow 白盒化，将规范翻译成 24 个可执行 critical checks，只改变 surrounding context，再追踪失败最早出现的位置。

最重要的结果是：主任务中 clean context 10 次通过 8 次，而约 299K 字符的 relevant-long 和等长 irrelevant-long 都只通过 3 次；但第二个任务三个条件全部通过。因此证据支持“某些 model-task pair 会出现高方差的长上下文可靠性损失”，**不支持普遍 context-length threshold，也不支持 relevant/plausible context 必然比 random irrelevant context 更危险。**

## 一、全文的证据链

```text
Research Gap
最终 patch / pass-fail 看不到 agent 在哪里开始失效
        ↓
Research Object
固定 Skill 驱动的白盒 code-audit workflow
        ↓
Operationalization
24 个 deterministic critical checks
+ 四类 first-visible failure location
        ↓
Treatment
clean / relevant-long / equal-length irrelevant-long
        ↓
Outcome
RequirementCoverage + strict TaskSuccess
+ artifact / tool log / completion record
        ↓
Claim
主任务存在明显但不确定的 long-context reliability loss；
效应具有任务异质性；显式 checklist 可缓解遗漏
```

四个关键概念：

- **Agent Skill**：版本化的指令与支持文件，规定 agent 读什么、改什么、收集什么证据以及何时完成。加载 Skill 不等于每条 obligation 始终保持活跃。
- **White-box evaluation**：不是读取隐藏 chain-of-thought，而是观察 instruction package、workspace、tool activity、编辑文件和 completion，从而定位可见失败。
- **Requirement Coverage**：适用 critical checks 中通过的比例，衡量“做对多少”。
- **Task Success**：全部 critical checks 通过才为 1。审计场景里 23/24 仍可能因一个关键遗漏而无效。

## 二、Research Gap：为什么最终成功率不够

coding-agent benchmark 常用最终 repository state、patch 或测试通过率评价系统，但同一个失败 outcome 可能来自完全不同的过程：一开始忘掉 requirement、记得要求却编辑漂移、工具已经暴露错误但 self-check 没反应，或者 evaluator/runtime 本身出错。

长上下文研究说明 advertised context window 不等于 uniformly usable context；agent 场景又额外混入工具调用、状态累积和完成条件。作者因此选择范围较窄但可观测性很强的 code-audit workflow：输出是结构化 artifact，要求可以在运行前枚举并写成 assertions。

这牺牲了外部效度，却换来更强的过程诊断能力。

## 三、24 个检查如何构造

作者从工作流中提取五类规范：显式要求、禁止事项、条件分支、字段数量限制和完成规则，再把每条改写成可观察 predicate。

例如，“plural evidence fields 必须是 arrays，即使无证据也要为空数组”会变成 presence + type check；“不得修改 protected core”会变成初始与最终 subtree 的 equality check。

checker 不规定唯一 reasoning trace，不同工作计划都能过；反过来，JSON 语法正确也不够，缺字段、改 protected value 或解决邻近但不同的问题都会失败。主 checker 有 **24 个等权 critical checks，覆盖四个 audit tasks**。

作者还用 positive/targeted-negative fixtures 验证 checker。曾有 semantic matcher 把等价措辞误判为错误，作者修 evaluator 后重新评分，而不是把 evaluator fault 算成 agent failure。

## 四、真正的 treatment：只改 surrounding context

主比较尽量固定 task、starting artifact、Skill、tools、model settings 和 frozen checker，每次重新构造 sanitized、answer-free workspace，只改变 context：

| 条件 | 含义 |
|---|---|
| clean | 约 10,991 characters 的最小工作上下文 |
| relevant-long | 约 299,140 characters，来自同一 production workflow 的相关材料 |
| irrelevant-long | 与 relevant-long 等长的自然但无关 archival text |

等长 irrelevant control 很重要：若 relevant-long 比 clean 差，可能只是 token 数增加；只有 relevant 与等长 irrelevant 的差异才更接近“内容类型”效应。

作者也清理历史 outputs、target findings、later-cycle artifacts 等 answer-bearing material；受污染的早期 pilot 不用于独立 effect claim。

## 五、四类 failure location

作者按最早可见证据编码：

1. **Lost requirement**：mandatory item 从任务表示或最终 artifact 中消失，也看不到它仍是 active obligation。
2. **Editing drift**：要求还在，但实际编辑违反要求，例如覆盖 protected content 或解决邻近问题。
3. **Failed checking**：artifact/tool output 已暴露错误，但 validation 没重新打开并修正任务。
4. **Non-agent failure**：evaluator/runtime 问题，例如 semantic false negative 或 stream disconnect。

这些是 descriptive failure locations，不是模型内部认知 taxonomy。它们的价值在于把“最终错了”拆成可观察过程。

## 六、主结果：8/10 → 3/10，但不能夸大

主模型任务使用 Codex + gpt-5.4-mini：

| 条件 | Task Success |
|---|---:|
| clean | 8/10 |
| relevant-long | 3/10 |
| irrelevant-long | 3/10 |

观察到的下降是 **50 percentage points**，但每组只有 10 次；clean 与两个 long condition 的 two-sided Fisher test 都为 **p=0.0698**，Wilson intervals 也很宽。

所以正确结论是：主 model-task pair 出现了很大的下降趋势，但统计不确定性高。不能写成“论文证明长上下文导致成功率下降 50%”。

更有意思的是 long condition 的平均 **Requirement Coverage 仍高于 92%**。历史 mixed-condition inventory 甚至通过 97.98% 的 individual checks，却仍有 44 条失败 trajectory。这说明 failure 可以非常稀疏：agent 并非整体崩坏，只漏少数关键 obligation，就会让 strict TaskSuccess 归零。

## 七、关键反例：第二任务完全不退化

第二个任务在 clean、relevant-long、irrelevant-long 三种条件下全部通过。

因此不存在由本文证明的“299K 字符危险阈值”，也不能说 coding agent 遇到长 context 就必然 context rot。效应具有明显 task heterogeneity。

论文还做五模型 sparse probes，并在协议允许时比较不同 agent shell，但作者把这些当 boundary-condition probes，而不是完整跨模型 benchmark。

## 八、为什么它直接约束 plausible-noise 假设

主实验中 relevant-long 与 irrelevant-long 的 binary success **完全相同：3/10 vs 3/10**。

这不证明“相关性不重要”：样本小，不能做 equivalence claim；这里的 relevant material 也不是我们定义的“与 query / symbol / call graph 高度相关但 non-decisive 的 repository code”；任务还是 structured audit completion 而非 localization。

但它足以否定一种先验叙事：**不能预设 plausible context 一定比 random context 更危险，再去挑支持案例。**

更稳妥的问题应是：

> 在 core evidence 已充分、token/file/position/representation 匹配时，plausible-but-non-decisive repository context 是否比 matched random context 引起更大的 attribution shift？

若最终 plausible ≈ random，也应接受：主要机制可能是 context load / obligation competition，而不是 semantic plausibility。

## 九、Checklist mitigation：为什么“再检查一下”不够

作者比较 generic self-check 与 detailed external checklist。后者明确重新列出 24 条 obligations。

结果：**detailed checklist 10/10，generic self-check 5/10，p=0.0325**。

generic validator 常继承编辑阶段已经发生的 omission：如果 requirement X 已被忘掉，让 agent “检查所有约束”不会自动恢复 X。详细 checklist 则把 X 再次外部化。

这支持“显式外部状态可缓解遗漏”，但没有证明内部原因就是 attention dilution；checklist 同时改变了提示内容和信息显式性，因此是 mitigation evidence，不是 latent-mechanism identification。

## 十、重要图表怎样读

**Figure 1** 是全文设计核心：Skill instructions → observable requirements → fixtures → frozen verifier → sanitized workspace → context intervention → agent run → score → failure classification。关键是 treatment 在 task/checker 固定后发生，classification 又在 scoring 后发生。

主结果表先看 8/10、3/10、3/10，再立刻看 p=0.0698 和第二任务全通过：前者给 effect-size signal，后两者限制 claim。

coverage 结果说明 92%+ partial correctness 与 30% complete success 可以共存；对关键要求型任务，平均指标会掩盖稀疏致命遗漏。

mitigation 对比 10/10 vs 5/10，说明“泛化地要求检查”与“重新显式呈现每条 obligation”不是同一种 treatment。

## 十一、证据审计

**优点 1：长度控制。** relevant-long 与 irrelevant-long 等长，避免内容类型与 token 数完全捆绑。但 clean vs long 仍同时改变长度和内容，因此不能分离纯 length effect。

**优点 2：保留 clean failures。** stochastic agent 在 clean 也可能失败，作者没有丢掉“不好看”的 run。

**局限 1：统计功效。** 10 runs/condition 很小。p=0.0698 既不能解释成“差一点显著所以是真的”，也不能因 p>0.05 宣称无效应。

**局限 2：TaskSuccess 很严格。** all-checks-pass 会放大单个 omission；这符合 audit artifact 的业务语义，但外推到普通 code generation 时必须同时看 coverage。

**优点 3：second-task counterexample。** 它阻止作者把一个 task 的强结果包装成 universal context rot。

**优点 4：基础设施失败单列。** 论文审计了 28 个 resultless/unusable attempts，并维护 equivalent-cost ledger。把它们全部计为 reasoning failure 会混淆 runtime reliability；完全删除又会美化系统表现。

## 十二、作者背景

论文单作者 **Yue Xue**，正文署名 Independent Researcher。其个人主页显示现任 CertiK Head of AI Research，长期研究 blockchain security 与 AI for software security，包括 smart-contract analysis、vulnerability detection、静态分析和 LLM-based auditing，并参与/开发实际安全审计工具。

因此本文使用 production-derived white-box code-audit workflow 与其长期工程研究路线一致：不是从通用 long-context benchmark 随机抽一个任务，而是把实际审计流程中的 obligations、artifact 和 checker 变成可重复实验对象。

原文未明确标注 corresponding author；不额外推定。

## 十三、论文证明了什么

较强支持：

1. 主 gpt-5.4-mini audit task 上，两个 long condition 都观察到 8/10 → 3/10 的 reliability decline。
2. long condition 的 Requirement Coverage 仍 >92%，说明下降可由少数关键 omission 驱动。
3. 可观察失败能被拆为 lost requirement、editing drift、failed checking 与 non-agent failure。
4. 第二任务没有 long-context degradation，说明效应依赖任务。
5. 主 model-task pair 上，明确重列 obligations 的 checklist 优于 generic self-check（10/10 vs 5/10）。

没有证明：

1. 没有证明通用 context-length threshold。
2. 没有证明 relevant/plausible context 比 irrelevant/random 更危险。
3. 没有证明 attention dilution、lost-in-the-middle 等内部机制。
4. 没有证明结果可直接外推到 SWE-bench、repository retrieval、code review 或 vulnerability localization。
5. 没有把 relevant-long operationalize 成 plausible-but-non-decisive repository code。

## 十四、对当前研究的启发

最新研究记录已经把主线从“证明 plausible 比 random 更坏”修正为“固定处理前证据，优先检验机制保持但归因偏移”；五例第二轮里 random 与 plausible 平均官方 F1 都是 0.5810。本文与这个修正高度一致。

第一，不要只看最终 file F1。可以显式记录：

```text
Core Evidence Available
    ↓
Evidence Retention
    ↓
Attribution Correctness (A)
    ↓
Mechanism Correctness (M)
    ↓
File / Patch Outcome
```

尤其关注 `P(M=1, A=0)`：模型仍说对漏洞机制，但把证据归给外围 sibling / retrieval-plausible node。

第二，random control 要真正 matched：token、文件数、代码块数、position、representation 尽量一致，否则“plausible 更长/更靠前”会成为隐藏 treatment。

第三，可以把 **explicit evidence checklist** 作为机制 probe：要求模型提交前逐条列出支持每个结论的代码证据。若 plausible condition 下 attribution shift 因 checklist 明显恢复，更像 evidence retention/checking 问题，而不是机制知识彻底丢失。

第四，预注册接受 null result。本文 relevant=irrelevant，当前五例也是 plausible=random；扩大样本后若仍如此，故事可以转为：semantic plausibility 并非主要危险源，context competition/evidence dilution 才可能更一般。但这需要足够功效或等价性设计，不能把“不显著”写成“相同”。

## 十五、真正应该记住什么

1. 长上下文 failure 可能很稀疏：整体 92%+ 正确仍会因一条关键 obligation 失败。
2. 最终 pass/fail 不够，white-box requirement/evidence tracking 能定位 failure 从哪层开始。
3. relevant-long 与 equal-length irrelevant-long 同为 3/10，是对“相关噪声天然更危险”的重要反例。
4. 第二任务全通过说明 context effect 有异质性，不能寻找单一 token 阈值。
5. generic self-check 可能继承原 omission；显式 checklist 更能恢复被忘掉的 requirement。
6. 对 repository-context 因果研究，最值得借鉴的是 **固定任务 + 匹配 treatment + 中间过程指标 + failure localization + 明确反例** 的实验纪律。
