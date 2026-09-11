# Antares: Foundation Models for Agentic Vulnerability Localization

> 精读日期：2026-09-06  
> 作者：Supriti Vijay, Aman Priyanshu, Didier Chapoteau, Arthur Goldblatt, Jianliang He, Kimia Majd, Fraser Burch, Baturay Saglam, Takahiro Matsumoto, Zhuoran Yang, Amin Karbasi  
> 机构：Foundation AI, Cisco Systems；部分作者来自 Yale University  
> 年份：2026  
> 技术报告：[Cisco Foundation AI Technical Report](https://cisco-foundation-ai.github.io/vulnerability-localization-benchmark/technical-report.pdf)  
> Benchmark：[Vulnerability Localization Benchmark (VLoc Bench)](https://cisco-foundation-ai.github.io/vulnerability-localization-benchmark/)

## 一句话价值

这篇报告同时做了两件事：一是提出 **VLoc Bench**，把漏洞定位从“给一段代码判断有没有漏洞”改成“只给 CWE 描述，让 Agent 在真实仓库里自己搜索并找出漏洞文件”；二是训练了 Antares 350M/1B/3B 三个小模型去学习这种搜索策略。对后续 repository-level / call graph / context causality 研究最有价值的并不是“小模型接近 GPT-5.5”，而是论文非常清楚地暴露了：**任务难度主要由仓库结构、搜索空间、漏洞证据分散程度和交互预算决定，而不是 CVSS 严重性；大仓库中的核心失败模式是 signal dilution。**

## 先建立论文地图

作者真正想解决的是一个很实际的问题：一个漏洞已经知道属于哪类 CWE，但在一个陌生仓库里，**到底是哪几个文件真正实现了这个漏洞？**

传统漏洞检测常把任务简化为：

```text
给定代码片段
↓
判断 vulnerable / benign
```

但真实修复流程更像：

```text
给定 CWE 类别描述 + 完整仓库
↓
先理解仓库结构
↓
搜索可能相关的符号 / API / 路径
↓
打开候选文件
↓
沿调用链、配置边界、校验逻辑继续追踪
↓
不断修正假设
↓
提交真正相关的漏洞文件
```

作者认为，后者不是静态分类任务，而是 **agentic repository exploration**。因此，他们既需要一个能测这种能力的 benchmark，也需要一个专门学会“搜索—验证—收缩”的模型。

理解全文最需要四个概念：

1. **Vulnerability Localization**：目标不是直接修复漏洞，而是找到包含漏洞实现的文件集合。它是修复、triage、回归测试和后续安全审查之前的一步。
2. **Agentic Localization**：模型不能一次性看到整理好的上下文，而要自己用 terminal 搜索、读文件、看目录、修正搜索策略。
3. **File F1**：每个任务比较“提交的文件集合”和“ground-truth 漏洞文件集合”，分别算 precision / recall / F1，再对 500 个任务 macro-average。
4. **Signal Dilution**：大仓库中，同类危险 API、缺失校验模式或数据流线索可能在很多 benign 文件中出现。问题不再是“有没有信号”，而是“真正安全关键的那一个实例被大量相似信号淹没”。

## 为什么现有漏洞检测不够

作者把现有方法分成几类。

第一类是 CodeQL、Semgrep、SonarQube 等静态分析工具。优势是可扩展、确定性强，但依赖已有规则、data-flow query 或前端覆盖，面对陌生漏洞模式时能力受限。

第二类是 security-specialized LLM。这些模型学了很多 CWE/CVE、安全问答和漏洞知识，但通常还是在固定输入上做分类或推理，**不会自己在仓库中导航**。

第三类是已有 repository-level / agentic 方法。它们虽然能搜仓库，但不少系统依赖静态分析先生成候选位置，或者把 frontier model 套在搜索 scaffold 上；作者认为，这样并没有真正训练出一个端到端 repository-search policy。

所以本文的 gap 不是“LLM 不懂安全知识”，而是：

> **现有系统没有充分回答：模型能不能只拿到一个很粗的 CWE 描述，就在陌生真实仓库中学会一套高效、可迁移的定位策略？**

## VLoc Bench 到底在测什么

VLoc Bench 包含：

- **500 个任务**；
- 来自 **290 个真实仓库**；
- 覆盖 **6 个 package ecosystems**；
- **147 个不同 CWE 类别**；
- 78% 的任务带 CVE；
- ground truth 来自真实安全修复对应的 implementation files。

### Phase A：Localization

模型拿到：

```text
CWE ID + CWE 的通用类别描述
+ 一个含已知漏洞的仓库快照
```

模型**不会拿到 advisory 原文、漏洞文件提示或 severity 信息**，需要自己搜索仓库，并最终提交漏洞文件列表。

主要评价：**File F1**。

### Phase B：Verification

给模型同一个仓库的已修复版本，要求模型正确判断漏洞已经不存在，避免 false alarm。

这里有一个非常重要的细节：

> **这份 Antares 技术报告的主实验实际只评了 Phase A；Phase B 虽然属于 VLoc Bench 规范，但没有在主报告中完成系统评测。**

所以不能因为 benchmark 页面写了“两阶段”，就把报告结论说成同时证明了定位能力和修复验证能力。

## Agent 的实验环境控制得很干净

每个任务都在全新 Docker 中运行：

```text
Ubuntu 24.04
2 CPU
4 GB RAM
无网络
仓库只读
单条 command 最多 10 秒
```

模型有三类工具：

```text
terminal
submit_vulnerable_files
submit_no_vulnerability_found
```

并且每个任务只有：

**15 次 terminal commands + 1 次最终 submission**。

这个设计很重要，因为它让 VLoc Bench 测的不只是“模型知道多少安全知识”，还测：

> 在一个固定行动预算下，模型会如何分配搜索、读文件和结构探索。

换句话说，**interaction budget 本身就是 task difficulty 的组成部分。**

## Antares 的整体方法：不是把更多代码塞进 Context，而是训练搜索策略

Antares 有三个尺度：

- 350M；
- 1B；
- 3B。

分别从 IBM Granite 4.0 对应 checkpoint 初始化。

整体训练流程可以写成：

```text
Granite Base Model
↓
SFT：学安全知识 + 深度研究 + terminal/code-search trajectory
↓
学会“怎么像一个 terminal agent 一样行动”
↓
GRPO：在真实 repository localization 环境中 rollout
↓
用可验证 file-level reward 优化整条多轮 trajectory
↓
形成 Antares search policy
```

这里最大的思想区别是：

> 作者不要求模型一次性拥有完整 repository context，而是让模型学习“下一步该看哪里”。

这和 repository-level context research 的关系很直接：**Context 不一定要一次性喂给模型，也可以被视为 Agent 主动获取的信息。**

## SFT 到底教了什么

SFT 数据大约由三部分组成：

- 71.5% Cybersecurity Reasoning；
- 13.1% Deep Research & General；
- 15.4% Code Search Trajectories。

前两类主要教漏洞、安全知识和长程 reasoning；第三类才真正教模型如何使用 terminal 找代码。

这里作者还用了一个叫 semantic conditioning 的辅助目标。它的作用可以直觉理解为：

> 不只让模型模仿下一个 token，还更明确地把 terminal observation 和后续行动联系起来。

Table 7 的 ablation 很关键：350M 模型如果没有辅助目标，SFT File F1 只有 0.021；ECHO 是 0.076，而 semantic conditioning 到 0.108。3B 上差距缩小，分别约 0.164、0.177、0.198。

这说明：**小模型尤其需要显式学“怎么把环境反馈变成下一步动作”。**

但不能进一步说 semantic conditioning 是唯一原因，因为这只是 SFT initialization 的对比，不是对整个最终系统所有模块贡献的完全分解。

## GRPO 真正优化什么

GRPO reward 不是简单的 0/1 成功信号，而是多个可程序验证的组成：

- localization quality；
- 正确 submission 行为；
- tool-use compliance；
- exploration behavior；
- malformed output penalty。

早期训练时，工具调用和提交格式这些“先学会把游戏玩对”的 reward 很重要；模型能稳定完成流程后，真正的 File F1 / localization quality 才成为主要区分信号。

这里有一个很值得借鉴的设计：

> **Reward 不直接规定“必须先 ls、再 grep、再 cat”，而是奖励最终定位效果和合规交互。**

所以后面出现的 search-heavy / verify-refine 行为，至少不是被硬编码成固定动作序列。

## 结果一：Specialization 比单纯 Scale 更重要

Table 4 最醒目的几个数字：

| Model | File F1 | Precision | Recall |
|---|---:|---:|---:|
| GPT-5.5 (xhigh) | 0.229 | 0.310 | 0.221 |
| Antares-3B | **0.223** | 0.303 | 0.221 |
| GPT-5.5 default | 0.221 | 0.305 | 0.211 |
| Antares-1B | 0.209 | 0.262 | **0.224** |
| GLM-5.2 | 0.186 | 0.226 | 0.186 |
| Antares-350M | 0.135 | 0.136 | 0.178 |

最值得注意的不是“3B 打赢 753B”这个宣传点，而是模型表现并没有随 parameter count 平滑上升。

作者把这称为 **capability cliff**：一批模型落在 0.186–0.229 的高层，另一大批模型直接掉到 0.152 以下。

这说明当前 benchmark 测到的不是一个单纯随 scale 平滑增长的能力，而是某种更依赖：

```text
security specialization
+
repository navigation policy
+
agent harness adaptation
```

的组合能力。

### 证据边界

这个结果能证明：

> **在当前 VLoc Bench + 当前统一 harness 下，task-specific post-training 的小模型可以显著超过很多更大的 general-purpose 模型。**

但不能把它泛化成：

> “任何软件工程 Agent 上，小模型 specialization 都比模型规模重要。”

因为 Antares 正是在 VLoc 类任务上直接训练的，而很多 baseline 没有经历相同目标的训练。

## 结果二：Task Difficulty 不是 Severity，而是 Structure

这是整篇报告与你之前 VLocBench 思路最相关的一段。

作者原本可以猜：Critical 漏洞也许更明显、更容易定位。

结果 Figure 5 显示 Critical / High / Medium / Low 的 F1 差异其实不大。

相反，Figure 4 按 ecosystem 分组时差异巨大：pip、npm 等目录结构相对扁平、约定明显的生态显著更容易，而 Maven 对几乎所有模型都很难。作者报告 pip / npm 的得分相对 Maven 可以高 **7–14 倍**。

因此作者认为真正重要的是：

> **Structural Locality：漏洞相关证据能否集中在一个小、可预测、容易搜索的局部区域。**

这比 CVSS severity 更能解释定位难度。

但这里仍然要谨慎：ecosystem、language、repository layout、平均仓库大小、framework usage、漏洞类型分布彼此相关。这个结果是强烈的 **association / dimensional analysis**，并没有因果识别“repository structure 独立造成了多少性能下降”。

## 结果三：Repository Size 是最强烈的 Difficulty Signal

Figure 6 是全文最重要的图之一。

作者按代码库大小分成：

```text
<100 KB
100–500 KB
0.5–2 MB
2–10 MB
10+ MB
```

结果所有模型都随 repository size 增长明显下降。

尤其：

- `<100 KB` 时 Antares-1B File F1 = **0.843**；
- Antares-3B = **0.828**；
- 到 `10+ MB` 时所有模型都已经非常低，GPT-5.5 反而开始超过 Antares。

这里作者提出一个很合理的解释：

### 小仓库

```text
grep broadly
↓
read candidate
↓
verify
```

15 次 command 基本能够覆盖相关搜索空间。

### 大仓库

同样 15 次 command 已经不足以形成可靠 repository model，单纯 grep elimination 开始失效，需要更强 architectural reasoning。

这说明：

> **Repository Size 并不是一个普通背景变量，它会改变“哪种 Agent Strategy 最有效”。**

从因果研究角度，它更像一个 **effect modifier**。

## 结果四：Multi-file Vulnerability 是另一个核心瓶颈

作者发现 single-file 漏洞明显更容易。

当 ground-truth 涉及 5 个甚至更多文件时，各模型表现急剧下降。

这个现象非常关键，因为它说明当前 Agent 很擅长：

> 找到一个“vulnerable foothold”。

却不擅长：

> 找回构成漏洞的完整 implementation slice。

比如它可能找到入口文件，却漏掉：

- call path 上的 supporting files；
- validation chain；
- config boundary；
- downstream implementation。

这也是为什么单纯把 file-level F1 当成“漏洞理解能力”要小心：它同时混合了“找到第一个关键点”和“完整恢复跨文件实现链”两个能力。

## 结果五：作者把失败模式明确叫做 Signal Dilution

Discussion 中作者给出了一个对你特别重要的表述：

> 在大仓库里，unsafe call、missing validation、attacker-controlled data flow 这些相关模式，会同时出现在很多 benign context 中。

模型的问题不是找不到可疑 pattern，而是：

```text
找到很多 plausible signals
↓
无法区分哪个实例真正参与 vulnerable implementation
↓
提交了相似但 benign 的候选文件
```

作者称之为 **signal dilution**。

这个概念和你现在研究的 repository context / call graph noise 非常接近，但又有一点区别：

- 你的问题更偏 **输入侧：额外 context 是否稀释 / 误导模型**；
- 这里更偏 **搜索空间侧：仓库中大量相似 benign signals 是否让 Agent 难以识别真正证据**。

二者可能是同一个更一般机制的两个表现：

> **Relevant evidence density 下降。**

## 结果六：GRPO 学出的不是“多探索”，而是 Search–Verify–Refine

Figure 7 分析了 Agent 的 terminal 行为。

作者把命令粗分成：

- grep/search；
- cat/read；
- list/explore。

Antares-3B 相比 GPT-5.5：

- 更偏 search；
- 更少做结构性目录探索；
- 总 command 更少。

但它的 command bigram entropy 仍然不低，说明它不是死板地重复 `grep → grep → grep`，而是在一个较窄的动作集合里动态切换。

作者总结成：

```text
Search broadly
↓
Read candidate
↓
Verify evidence
↓
Refine search
```

这就是所谓 **Search–Verify–Refine policy**。

### 这里真正有意思的是

Agent 并没有先构建完整 repository mental model。

它更像一种 elimination strategy：

> “先找到可能的，再逐步排除。”

这对 context research 有很直接的启发：**全局理解并不总是必要，尤其在预算受限时，主动局部获取可能比预先提供 Full Repository Context 更高效。**

## Figure 8：SFT 和 GRPO 分别贡献了什么

Base Granite 几乎不能做这个任务：

- 350M：0.001；
- 1B / 3B：接近 0。

SFT 后：

- 350M：0.108；
- 1B：0.188；
- 3B：0.198。

GRPO 后：

- 350M：0.135；
- 1B：0.209；
- 3B：0.223。

所以最先带来“从不会到会”的其实是 SFT。

GRPO 的作用更像：

> **在一个已经会使用 terminal 的 Agent 上，进一步把策略收缩到高回报轨迹。**

Table 6 还有一个很容易被只看平均分的人忽略的结果：GRPO 把不同 run 之间的 File F1 标准差降低 **42–65%**。

这说明 RL 的贡献不只是平均 F1 + 几个点，还包括：

> 行为更稳定、更少 run-to-run variance。

## 不同尺寸模型学到的 Strategy 还不一样

GRPO 后：

### 350M / 1B

变得非常 search-heavy，作者报告大约 87–89% command 都是 search 类型，并提交更多候选文件。

这是一种：

> **高 Recall / 弱 Verification** 的补偿策略。

### 3B

保持更平衡：大约 52% search、37% read，提交文件更少，但 precision 更高。

这说明 RL 没有学出一个固定“最佳算法”，而是：

> **不同 capacity 的模型根据自己的验证能力形成不同 operating point。**

这其实是很好的 HTE 类思路：Treatment = RL，但其行为机制随 Model Capacity 改变。

## 一个特别重要的额外实验：只改 Prompt，就能改变 Strategy 和 Score

Appendix C.2 是我认为全文最值得你额外关注的实验之一。

作者发现 GPT-5.5 比 Antares 更喜欢先 `ls` / map repository，再搜索。于是他们只修改 Antares-3B system prompt，要求：

```text
1. Explore first：3–4 calls
2. Targeted search：4–6 calls
3. Verify and read：3–5 calls
```

其他全部保持不变：

- model checkpoint；
- inference parameters；
- tool definitions；
- sandbox；
- evaluation instances；
- scoring function。

结果：

- Baseline Antares-3B：**0.223**；
- Explore-First Prompt：**0.2313**；
- GPT-5.5 xhigh：约 **0.2292**。

同时 structural exploration 从约 10.2% 上升到 17.3%，search command 从 52.3% 下降到 46.2%。

这几乎是一个非常干净的 intervention：

> **只改变 Strategy Instruction，就同时改变了 Agent Behavior 和最终 Outcome。**

当然它还不能说明 explore-first 对所有任务都好，因为作者没有进一步分层看哪些 repository size / structure 最受益。

这正好可以做成后续异质效应分析。

## Harness 也是 Benchmark 的一部分，而不是中性管道

Appendix C.3 进一步提醒：不同 Agent harness 会改变性能。

作者明确总结：

> Harness 是 meaningful source of performance variation。

也就是说，Benchmark 最终测到的是：

```text
Base Model
×
Prompt
×
Tool Set
×
Command Budget
×
Harness Orchestration
×
Repository Task
```

而不是一个纯粹的“LLM capability”。

这一点和明天你指定的那篇 *What Does an Agentic Software Engineering Benchmark Measure?* 会非常连贯。

## Transfer：到底学到了安全知识，还是通用 Repository Search？

作者用 SWE-Bench file localization 做 zero-shot transfer。

Antares 没有使用 SWE-Bench repository、issue description 或 issue-resolution localization 数据训练，但：

- Antares-3B 在 SWE-Bench Verified File F1：**66.54**；
- CodeScout-14B：68.57；
- CodeScout-4B：68.52；
- Antares-1B：64.24。

这说明 Antares 的训练并不只是记了“某个 CWE 应该 grep 什么关键词”。

比较合理的结论是：

> **它确实学到了部分可迁移的 repository navigation / candidate verification policy。**

但仍然不能说已经完全隔离出“通用 Agent 能力”，因为 SFT 中本来就包含 general code-search trajectories。

## 认真审查 VLoc Bench：它到底测的是什么？

### 1. 它测的不只是 Vulnerability Knowledge

输入 CWE 描述非常粗，但成功还需要：

- repository exploration；
- lexical search；
- architecture inference；
- call-path reasoning；
- candidate verification；
- budget allocation。

所以 File F1 是多个 latent abilities 的混合 outcome。

### 2. Repository Size 可能和很多变量捆绑

大仓库通常同时意味着：

```text
更多文件
更多重复 symbol
更深目录
更复杂 framework
更多 call paths
更高 context heterogeneity
```

因此“size 导致 performance drop”在严格因果意义上还没有识别。

更准确说：

> repository size 是一个很强的 difficulty proxy。

### 3. Ecosystem Difference 也不是纯语言效应

Maven 难，pip/npm 易，并不能直接写成：

> Java 导致 Agent 表现差。

因为 ecosystem 同时携带：

- directory convention；
- build structure；
- framework style；
- vulnerability composition；
- repository scale。

### 4. 15-command budget 是非常强的 Task Constraint

如果给 30、50、100 个 commands，模型排序可能改变。

论文自己也通过更大 harness / prompt 实验说明 inference configuration 会影响结果。

所以：

> VLoc Bench 的性能是 **Capability under Budget**，不是无约束下的“最终定位能力”。

### 5. File F1 对 distributed vulnerability 特别严格

这既是优点，也是一个 construct choice。

它奖励完整恢复所有漏洞实现文件，但会把：

- 找到 root vulnerable entry；
- 找到全部 supporting files；

融合成同一个分数。

后续如果想研究机制，最好拆成：

- First-hit / foothold recall；
- complete-slice recall；
- path completeness；
- false candidate rate。

## 对你之前“先控制 Task Difficulty 再证明 Call Graph 重要”的直接启发

这篇报告其实进一步说明了，你后来放弃“只证明 call graph 有用”是对的。

因为 VLoc Bench 自己已经得到一个很清楚的现象：

> **Task difficulty 和 repository structure 强相关。**

如果你的实验只是：

```text
控制 repository size / difficulty
↓
比较 +CG vs -CG
↓
证明 CG 对跨文件任务更有用
```

即使做得很严谨，结论也容易停留在一个大家已经预期的层面。

更值得做的是把本文的 **signal dilution** 往前推进：

> 当 call graph / repository context 中存在大量可有可无的结构信息时，为什么 Agent 会被带偏？

## 可以直接借鉴的变量设计

### Treatment

```text
Context Type
= Diff only / In-file / Call-Graph / Full Repo
```

或：

```text
Search Strategy
= Search-first / Explore-first / Call-graph-first
```

### Effect Modifiers

- repository size；
- file count；
- number of relevant files；
- call-path depth；
- fan-out；
- structural locality；
- context-need label。

### Mediators

- relevant evidence density；
- number of benign candidate hits；
- search entropy；
- number of inspected irrelevant files；
- complete path coverage；
- context token ratio；
- attention / trajectory allocation。

### Outcomes

不要只用最终 F1，可以拆成：

- First Relevant File Hit；
- Complete Relevant File Recall；
- False Candidate Count；
- Commands to First Hit；
- Commands to Verification；
- Token Cost；
- Final Review / Localization Quality。

## 一个特别值得做的析因实验

可以直接从本文的 Appendix C.2 延伸：

```text
Factor A：Context
No CG / CG

Factor B：Search Strategy
Search-first / Explore-first

Factor C：Task Structure
Local / Distributed
```

得到一个：

```text
2 × 2 × 2 factorial design
```

你真正想看的不是三个 main effects，而是：

> **CG 是否只有在 distributed task + explore-first strategy 下有正效应，而在 local task 中反而造成 signal dilution？**

这个 interaction 比“平均 +CG 提高 x%”有价值得多。

## 作者证明了什么

1. 在统一的 15-command agent harness 下，VLoc Bench 上的 repository-scale vulnerability localization 仍然非常困难，当前最佳 File F1 只有约 0.23。
2. Task-specific post-training 可以让 1B/3B 小模型在这个任务上匹配或超过大量更大的 general-purpose 模型。
3. Repository structure、repository scale、ground-truth file count 与定位难度存在非常强的关联，而 CVSS severity 的区分力较弱。
4. GRPO 不只提高平均 File F1，还显著降低 run-to-run variance，并使不同模型尺度形成不同 search / verify operating regimes。
5. Strategy-level prompt intervention 可以改变 Agent command distribution 和最终定位表现，说明 Agent behavior 并非完全固定在 checkpoint 中。
6. Antares 在 SWE-Bench file localization 上具有明显 zero-shot transfer，表明训练出的部分能力可以迁移到更一般的 repository navigation。

## 作者没有证明什么

1. 没有证明 repository size 本身是性能下降的独立因果原因；size 与大量结构变量共变。
2. 没有证明 call graph 或 architectural reasoning 是大仓库中的唯一缺失能力。
3. 没有证明 signal dilution 已经被直接测量或介导分析；它主要是基于失败模式和结构分层结果提出的机制解释。
4. 没有在主报告中系统评估 VLoc Bench Phase B，因此不能把结果扩展到“已修复漏洞验证能力”。
5. 没有证明 Antares 的优势全部来自 GRPO；SFT、security corpus、code-search trajectories、semantic conditioning 和 RL 是连续训练链路。
6. 没有证明当前模型排序在不同 command budget、prompt 或 agent harness 下保持不变；附录反而说明这些 evaluation choices 会显著改变结果。

## 真正应该记住什么

- **VLoc Bench 测的不是单纯漏洞知识，而是“安全知识 × repository navigation × budgeted agent behavior”。**
- **Repository structure 比漏洞 severity 更能预测任务难度，但这目前首先是关联证据，不应直接写成因果结论。**
- 大仓库里最值得关注的失败模式不是“没有 relevant signal”，而是 **relevant evidence 被大量 benign look-alikes 稀释**。
- 15 次 terminal command 使 benchmark 本质上测的是 **有限预算下的搜索策略质量**。
- Agent benchmark 的结果高度依赖 prompt 和 harness，因此不能只把最终分数归因于 base model。
- 对后续 Causality for Code Review，最值得继续的是：把 **signal dilution / context noise** 从解释性语言真正变成可操纵 Treatment、Mediator 和 Effect Modifier。

## 对后续研究最直接的一个问题

如果把这篇论文与你现在的方向真正接起来，我会把下一步研究问题改成：

> **在固定模型、工具预算和任务条件下，repository-level structural context 的增加，是否通过降低 relevant-evidence density、扩大 benign candidate search space，从而改变 Agent 的搜索轨迹和最终代码审查/漏洞定位质量？**

这比“Call Graph 是否重要”多了一层真正可以验证的机制，也正好解释为什么：

> 对需要跨文件信息的任务，结构 context 可能帮助；而对不需要它的任务，同一份 context 反而可能成为 signal dilution 的来源。
