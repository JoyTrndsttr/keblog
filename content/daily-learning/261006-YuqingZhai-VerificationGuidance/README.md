# 论文精读：From Verification Failures to Reusable Guidance for Coding Agents

> 精读日期：2026-10-06  
> 作者：Yuqing Zhai; Xiaohong Chen; Lingming Zhang; Sriram Vishwanath; Grigore Rosu  
> 机构：University of Illinois Urbana-Champaign（UIUC）  
> 版本：arXiv v2，2026-10-01  
> 原文：[arXiv:2609.39022](https://arxiv.org/abs/2609.39022) · [PDF](https://arxiv.org/pdf/2609.39022)  
> Tags：`2026` `arXiv` `Coding Agent` `Formal Verification` `K Framework` `Reusable Guidance` `Agent Skills` `Specification Adequacy`

## 先用三句话把论文讲清楚

这篇论文研究一个容易被“证明通过”掩盖的问题：coding agent 不仅要证明程序满足某个形式化规格，还必须证明这个规格确实覆盖了用户要的行为；否则，缩小输入范围或加入过强的辅助规则，都可能得到形式上成功、实质上无意义的证明。

作者把过去验证失败后的专家诊断沉淀为两类可复用资源：一类是可执行语言语义及一致性测试，另一类是指导规格构造、证明修复和充分性审计的 verification kit。论文用 HumanEval、KleverBench、带缺陷的审计对、智能合约和 Optimism 案例分别展示这套工作流。

最关键的结果却是一个负面且更可信的结论：历史 KleverBench 实验中 kit 看似把接受率从 72.6% 提到 83.9%，但在冻结规则、等长 generic advice 和单次配对运行后，GPT-5.6 Luna 上是 19/31 对 15/31，DeepSeek-V4.1-Flash 上反而是 16/31 对 17/31 或 18/31；所有配对区间都包含 0。论文证明了“失败经验可以被组织成可执行工作流”，但还没有证明固定 kit 能稳定提升新任务上的 agent 表现。

## 一、理解全文需要的四个概念

### 1. Verification 与 validation 不是一回事

**Verification（验证）**问的是：在已经写出的语义、前置条件和后置条件下，结论能否由证明器推出。**Validation（确认/充分性审计）**问的是：这些语义和条件是否真的表达了原始需求。

例如，要证明一个求和循环对所有非负整数都正确，却把前置条件写成 `n = 0`。证明器可能顺利通过，但它只证明了一个极窄的命题。本文最重要的认识，就是不能把 checker success 等同于 intent satisfaction。

### 2. K Framework

K 是一套用配置单元与重写规则描述程序语言操作语义的框架。相同的语言定义既能执行具体程序，也能对符号输入进行可达性证明，因此 agent 不必为 Python、EVM 等不同对象分别发明一套验证逻辑。

论文使用的目标是部分函数正确性：若初始状态满足前置条件、程序在给定语义下终止于某状态，那么最终状态必须满足后置条件。它不自动保证程序终止；终止性需要另行证明。

### 3. Verification kit

这里的 kit 不是一个训练后的模型，而是一组版本化的 procedures、references 和工具接口。它告诉 agent 如何界定规格作用域、构造循环不变量、检查符号执行后的残余状态、分类辅助规则、验证非空洞性，以及失败后应回到哪个阶段修复。

关键点是：kit 不只给“多检查一下”这种抽象建议，还要求保留适用条件与证据。例如，用一个 proof-only 循环替换原程序时，必须额外证明两者在完整状态与控制上下文上等价。

### 4. Specification adequacy

规格充分性指形式化规格是否覆盖了预期输入域、语言行为和目标性质。论文用具体 coverage points、独立审计、错误程序/错误后置条件负控，以及对辅助规则信任边界的检查来提供证据；这些措施可以发现部分缺口，但仍不等于把自然语言意图完全机器化证明了。

## 二、顶层证据链：作者到底如何把问题变成可测对象

```text
研究缺口
checker 通过不保证规格表达了真实需求；失败经验又容易停留在单次人工修补
    ↓
研究对象
语言语义、规格、证明扩展、审计证据，以及专家从失败中总结出的操作程序
    ↓
操作化
把经验固化为可执行语义 + verification kit；把“好不好”拆成 proof、coverage、audit
    ↓
多组研究
HumanEval 开发史 + 缺陷审计挑战 + KleverBench 冻结对照 + 合约案例
    ↓
证据
证明重放、结构/覆盖检查、AI 审计、作者审查、配对统计与失败轨迹
    ↓
可支持的结论
这套流程能产出可检查的证明包并暴露若干规格缺陷；固定指导的平均增益尚不稳定
```

这条链路很重要，因为本文不是一个干净的单一 RQ 实验。它混合了历史开发记录、受控对照、前瞻审计挑战和案例研究。每一部分回答的问题不同，不能把 164/164、12/12 和 19/31 合并成一个笼统的“方法有效”。

## 三、从一次失败到可复用程序：方法怎样运行

Figure 1 给出的流程可以分成上下两层。

下层是单个任务的生产链：

```text
程序与意图
  → 规格与作用域
  → 证明构造与检查
  → validation 与证据审计
  → 失败后返回责任阶段
```

上层是跨任务积累的资源：失败尝试、专家反馈和用户反馈不会只用于修补当前任务，而是进入 executable semantics 或 verification kit。下一次 agent 再遇到类似的不变量、输入域或桥接规则问题时，可以加载对应程序。

### 一个具体例子：`split_words`

原来的谓词只识别 CPython 29 个空白字符中的 4 个。证明仍可能在被错误建模的语义里通过，但与真实 Python 行为不一致。修复不是简单补 25 个字符，而是：固定 CPython 3.12.3 和 Unicode 15.0.0，补全 29 个成员，遍历全部 1,114,112 个码点检查，并重放所有相关 consumer。

因此被沉淀下来的经验不是“以后记得处理空白字符”，而是一个可审计程序：固定库版本、对有限域做完整比较、补边界测试、重放受影响调用者，并链接到具体修复与独立检查。

### 为什么还要给 proof extension 分类

agent 很容易为了让证明器通过而加入局部规则。论文把扩展分成四类：数学定义、可推导引理、替代执行的 operational bridge，以及显式信任的 primitive。分类决定下一步义务：

- 数学定义需要说明其方程与目标性质的关系；
- derived lemma 要在完整 guard 上证明；
- operational bridge 必须有不依赖该 bridge 的连接定理；
- trusted primitive 必须显式进入信任边界。

若不分类，一条直接“把结果改成想要值”的规则，也可能被 checker 当作合法推理的一部分。

## 四、实验坐标系：五类证据不要混在一起

| 研究部分 | 单位 | 对照/标签 | 主要回答什么 |
|---|---:|---|---|
| HumanEval 历史 campaign | 164 个 Python 任务，三种资源臂 | agent 自写语义 / supplied semantics / supplied+kit | 整套资源在开发过程中能否完成验证包 |
| 缺陷审计挑战 | 12 个 clean/defective 配对，共 24 包 | 作者预审标签；所有 K claims 均通过 | audit 能否发现“证明通过但规格有缺陷” |
| KleverBench 冻结对照 | swapped semantics 下 31 个程序 | Rules / 等长 Generic / 等长 Kit | kit 的内容是否超越完整规则与一般建议 |
| KleverBench 历史实验 | 31 程序 × 3 semantics × 4 attempts | Bare / Kit | 历史场景中 kit 与接受率是否相关 |
| 合约案例 | DSToken、DSValue、HKG、Optimism 等 | 主要是 kit 内部开发与人审，无 matched no-kit | 流程能否用于复杂 EVM 性质 |

模型和工具也不统一：HumanEval 历史 producer 是 GPT-5.6 Sol；冻结 KleverBench 使用 GPT-5.6 Luna 与 DeepSeek-V4.1-Flash；审计挑战使用 GPT-5.6 Sol；合约案例又包含独立 judge 和人工反馈。跨模型数字只能说明各自协议，不能直接横比能力。

## 五、HumanEval：164/164 应该怎样读

### 问题

当 agent 获得不同程度的语义与指导时，能否产出通过审计的实现、规格和证明包？

### 设计

三种历史条件各覆盖 164 个任务：

1. agent 自己写语义、无 kit；
2. 提供语义、无 kit；
3. 提供语义并提供 kit。

Stage 2 审计把结果分为 PASS、CONCERNS 和 FAIL。旧的 `LEGIT` 指标把 PASS 与 CONCERNS 合并，因此论文在新版表格中把三类重新拆开。

### 结果

Table 1 的决定性比较是：

- 自写语义、无 kit：23 PASS、41 CONCERNS、100 FAIL；
- supplied semantics、无 kit：37 PASS、36 CONCERNS、91 FAIL；
- supplied semantics + kit：97 PASS、67 CONCERNS、0 FAIL。

之后作者针对两个 concern 做了定向修复：Task 59 补充最大素因子的 Lean 充分性定理，Task 125 修复空白字符语义。最终 164 个选定 package 都得到 AI audit PASS。

### 证据边界

这不是随机或冻结的消融。语义、kit、修复流程和候选选择在 campaign 中共同演化，HumanEval 也参与塑造了这些资源；因此 164/164 是“开发完成度”，不是 kit 对 unseen tasks 的因果效果。

而且最终标签是 AI audit PASS，并不是 164 个任务的自然语言意图都被完整机器证明。作者明确承认，没有 benchmark-wide 的 machine-checked intent adequacy 统计。

## 六、审计挑战：为什么 proof success 仍可能是假的安全感

### 设计

作者构造 12 对 clean/defective package，缺陷分四类：弱后置条件、不受支持的 bridge、源码/证明不一致、错误语义。作者专家在看新 AI 判断前审查了每对的作用域、精确修改、反例和 replay evidence。

特别关键的是：**24 个 package 的 28 条 K claims 全部证明通过。** 因而这里不是让审计器重复判断 proof 是否成功，而是检验它能否识别“被证明的命题本身不充分”。

### 结果

原始 24 次尝试发现 10/12 缺陷并接受 12/12 clean；两个缺陷因 provider capacity error 没有返回报告。按预先追加的规则各重试一次后，完成判断为 12/12 缺陷发现和 12/12 clean 接受。每个 12/12 比例的 95% Wilson 区间仍只有 75.8%–100%。

### 怎样正确解释

这个结果证明了：中性的、面向 source correspondence、scope coverage、semantic fidelity 和 local-rule justification 的审计，能在这组人工缺陷上补充证明器。

它没有证明审计器能在真实、自然、未知分布的规格错误上达到 100%。样本只有 12 对、缺陷是人工植入、ground truth 来自一位作者专家；且总输入约 1862 万 tokens，其中约 1725 万为缓存 tokens，成本并不轻。

## 七、KleverBench：论文中最接近“kit 是否有效”的实验

### 7.1 任务为何要修改 operator semantics

KleverBench 给 agent 一个小型 imperative program 和语言语义，让其写出可达性 claim。作者设置 ordinary、renamed 与 swapped 三种语义。swapped 会让熟悉符号拥有反常含义，例如减号表示加法；这能测试 agent 是否真的读取 supplied semantics，而不是依赖预训练先验。

接受一份 claim 需要同时满足：包含给定程序、使用规定的最终状态形式、不加入禁用规则/属性、覆盖要求的具体输入点，并最终由 `kprove` 证明到 `#Top`。

### 7.2 冻结、等长的三臂对照

三组共享程序、语义、数学词汇、检查器和时间限制：

- **Rules**：完整接受规则；
- **Generic**：完整规则 + 关于计划、检查和修订的一般建议；
- **Kit**：完整规则 + 五份历史文件中的固定 procedure core。

Generic 与 Kit 都是 2,145 tokens，按同一 `o200k_base` tokenizer 计算；这控制了文本长度，但作者坦率说明没有证明 provider 内部 tokenizer 下仍严格等长。

### 7.3 主结果：方向随模型改变

Table 2：

- Luna：Rules 15/31，Generic 15/31，Kit 19/31；Kit 对两种控制都是 +12.9 个百分点；
- DeepSeek：Rules 17/31，Generic 18/31，Kit 16/31；Kit 分别是 -3.2 和 -6.5 个百分点。

四个 paired bootstrap 区间都跨 0；模型内 Holm 校正后，Luna 的 p 值为 0.775，DeepSeek 为 1.0。不能据此声称 kit 有显著提升。

DeepSeek 还暴露一个很具体的机制：在每个 trial 0.10 美元的本地 admission budget 下，Rules、Generic、Kit 分别有 14、14、23 次达到停止条件。更长、更复杂或更容易诱发探索的指导可能消耗预算，最终把潜在收益抵消掉。

### 7.4 两个相反案例

在 `add-loop` 中，两个控制都把输入缩窄到 `N ≤ 0`，独立 coverage check 将其拒绝；kit 保留完整输入域并通过。这个例子支持“procedure 能防止空洞证明”。

但在 `count-even` 中，kit 候选反而把输入缩窄到 `N ≤ 0`，两个控制却成功构造了可接受 claim。也就是说，指导不是稳定生效的规则系统；它仍要经过模型选择、理解和执行。

## 八、为什么历史实验看起来更漂亮

历史 principal experiment 每个 program-semantics 配置运行 4 次，共 372 attempts/arm。Bare 接受 270/372（72.6%），Kit 接受 312/372（83.9%），差 11.3 个百分点；在 Tier 4–5 难题上从 39.8% 提到 67.6%。Figure 2 显示增益主要集中在嵌套循环和 pipeline 的困难层级，Tier 1 几乎已经饱和。

但这组结果存在多项共同变化：

- Bare 与 Kit 生成并发分别为 4 和 6；
- 4 个被取消的 bare trial 后来被替换；
- 精确生成时 commit、seed、temperature 和 token budget 没有记录；
- 只有聚合计数，缺少历史 trajectories；
- kit 条件既改变信息内容，也可能改变 instruction emphasis 与遵从度。

Table 7 进一步表明，42 个净新增接受来自 32 个更少的 pre-proof rejection、24 个更少的 proof timeout，同时又多了 14 个 proof error。它支持“kit 相关条件下结果更好”，但不能把差异唯一归因到某一条 procedure。

因此 Section 5.2 的冻结三臂实验比历史大数字更适合回答因果问题，而它给出的是混合结果。

## 九、智能合约案例说明了什么

DSToken transfer 的价值不在成功率，而在暴露规格边界：原始 runtime 执行失败时，状态里可能暂存此前日志；外层 message-call 失败又会回滚 storage 与 logs。只有明确“在哪一层观察状态”，两个看似矛盾的行为才能同时成立。

Optimism 案例保留 20 条有正向证明记录的 claims，覆盖六个 pause 操作和四个 pause dependency。人审确认它们在声明的范围内成立，但范围包含：London semantics、unbounded gas、直接 implementation bytecode、特定 authorized messenger、动态字节长度上限等假设。Malformed calldata、有限 gas 和 deployed proxy 不在结论范围内。

这些案例证明 kit 可以帮助组织复杂证明包与信任边界；因为没有 matched no-kit，它们不能估计 kit 的增量效果。作者还报告早期智能合约选择运行估计 AI 成本约 171.95 美元，但未覆盖 follow-up 与人工劳动，不能与手工验证做成本比较。

## 十、Figures 与 Tables 应该怎样读

### Figure 1：核心不是一条流水线，而是两个反馈环

横向链路负责单任务：意图→规格→证明→审计。下方反馈箭头把审计失败送回“责任阶段”，避免所有错误都靠在证明末端打补丁；上方链路把跨任务失败送入语义规则与 kit，形成长期记忆。

图没有证明知识一定会迁移，只定义了应该如何保存和复用。论文也明确说 `split_words` 新条目对后续任务的实际效果尚未测量。

### Figure 2：增益集中在困难层级，但只是历史描述

横轴是五个作者预设难度 tier，纵轴是 accepted attempts。Bare/Kit 在 Tier 1 为 58/60 与 60/60，在 Tier 4 为 22/72 与 40/72，在 Tier 5 为 21/36 与 33/36。视觉上确实显示难题增益更大。

然而这些 tier 后来的仓库版本会依据观察结果重新分配，论文保留的是原始作者标签；历史实验又缺少冻结轨迹与完整运行配置。因此这张图适合提出“指导可能对复杂控制流更有帮助”的异质性假设，不足以确认机制。

## 十一、证据审计：这篇论文最诚实也最值得学的地方

### 论文明确证明了什么

1. 失败经验可以被组织为带适用条件、证据要求和版本来源的 verification procedures，而不是散落的 prompt 技巧。
2. 在 12 个人工缺陷对中，形式化 proof success 与规格充分性可以明确分离；所有 defective package 都能证明，却仍可被审计识别。
3. frozen guidance 的效果会随模型和资源预算改变：Luna 正向、DeepSeek 负向，且不确定性很大。
4. 输入覆盖需要独立检查。只看 proof success 会接受通过缩窄 precondition 获得的空洞证明。
5. EVM 案例显示执行边界、存储 alias、日志回滚、gas/fork 与 ABI 范围必须显式进入规格作用域。

### 论文没有证明什么

1. 没有证明 kit 在 unseen task family 上稳定泛化；资源可能已被 HumanEval/KleverBench 的开发过程污染。
2. 没有证明 164/164 等于 164 个任务的意图被完全机器检查；最终指标包含 AI audit 判断和定向修复。
3. 没有证明哪个 procedure 贡献最大；历史实验没有组件消融，冻结实验也只比较整段 core。
4. 没有证明 audit 对自然缺陷同样可靠；审计挑战样本小、人工合成，并由一位作者专家给出标签。
5. 没有证明更完整的指导总是值得其 token/时间成本；DeepSeek 的 budget stops 恰好提示相反风险。

## 十二、作者与课题组背景

论文五位作者均列为 UIUC。公开可检索资料对第一作者 Yuqing Zhai 的研究履历很有限；可确认其与 UIUC、Pi Squared 有关联，但目前不能据此推断其长期独立研究方向。

团队的明确技术积累来自 Grigore Roșu 领导的 Formal Systems Laboratory。Roșu 长期研究程序语言语义、形式化方法、runtime verification、matching logic 与 K Framework；本文的可执行语义、reachability proof、KEVM/EVM 实例与 proof evidence 组织方式，都是这条研究路线向 coding agents 的直接延伸。Xiaohong Chen 也长期参与 matching logic 与 K 相关研究。

原文、arXiv 页面和可核验作者页面均未明确标注通讯作者，因此本文不按末位作者或 arXiv 提交者推断通讯作者。

## 十三、对当前“上下文干预—证据归因”研究的启发

### 1. evidence checklist 应当是待检验 treatment，而不是默认有效的 remedy

昨天 HiSentinel 提醒“干预质量比干预次数重要”，本文又进一步显示：固定 kit 在 Luna 上可能有帮助，在 DeepSeek 上却更容易耗尽预算。当前可以设计 `core-only / +equal-length generic checklist / +evidence-specific checklist` 三臂，而不能只比较有无 checklist 后就把差异归因于“更好验证”。

### 2. 把 outcome、mechanism、attribution、coverage 分层

本文把 proof success 与 specification adequacy 拆开，正对应当前不能只看 file F1。对 VLocBench 可分别记录：

- `O`：最终 file/patch localization；
- `M`：漏洞机制是否正确；
- `A`：引用的关键证据是否真正支持机制；
- `C`：决定性证据/必要输入域是否被覆盖。

`M=1, A=0` 类似“证明了一个命题，但证据或作用域没有对应真实意图”：最终结果偶然正确，不等于推理依据可靠。

### 3. token matching 仍不足以排除资源路径差异

论文把 Generic 与 Kit 做到 2,145 tokens 等长，但 DeepSeek 的 kit budget stops 从 14 增至 23。即使输入 token 相同，不同内容也可能诱发不同长度的探索、工具调用与 completion。当前实验除 prompt token 外，还应报告 completion token、turn 数、工具调用数、提前停止与 wall time。

### 4. 借鉴“责任阶段”而不是照搬形式验证

当前最可借鉴的不是把 VLocBench 全部形式化，而是给每类失败指定责任层：retrieval selection、node identity、context packaging、mechanism inference、evidence attribution 或 outcome reporting。这样 plausible node 导致的错误不会统统被记成“模型被噪声干扰”，而能定位究竟是哪一层发生偏移。

### 5. 用配对差异和负例保留反结论

本文保留 kit-only wins、control-only wins、capacity failures、budget stops 和方向相反的模型结果。当前五例 random/plausible 均为 0.5810，也应继续作为真实反例保留；后续扩样本时预注册 treatment、主要指标和失败计入规则，避免只挑出现 attribution shift 的 case。

## 最后真正应该记住什么

- checker 只能证明“你写下来的规格”，不能保证“你写的是用户真正要的规格”。
- 可复用经验最好带适用条件、来源、负控和检查程序，而不只是自然语言忠告。
- 164/164 的开发完成度很亮眼，但最有因果解释力的冻结实验给出的是不确定、跨模型不一致的效果。
- 等长 context 仍可能产生不同的推理成本与预算耗尽，context content 与 execution budget 必须同时审计。
- 对 coding agent 来说，可靠性不是在最后再加一个 judge；规格、证明、证据和审计需要形成可追责的闭环。
