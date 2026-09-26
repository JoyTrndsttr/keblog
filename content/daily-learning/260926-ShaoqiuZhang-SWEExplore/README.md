# SWE-Explore: Benchmarking How Coding Agents Explore Repositories

> 精读日期：2026-09-26  
> 第一作者：Shaoqiu Zhang  
> 论文：SWE-Explore: Benchmarking How Coding Agents Explore Repositories  
> arXiv：2606.07297  
> 项目：https://github.com/Qiushao-E/SWE-Explore-Bench  
> 主题：Coding Agent、Repository Exploration、Line-level Evidence、Context Retrieval、Trajectory、Restricted-context Repair

# 先把整篇论文装进脑子里

SWE-Explore 研究的不是“Agent 最后有没有修好 issue”，而是一个更靠前的问题：

> **给定一个 issue 和 repository，Coding Agent 在开始修改代码以前，到底有没有找到真正关键的代码证据？**

现有 SWE-bench 类评测把探索、推理、编辑、验证全部压缩成最终 Pass/Fail。一个 Agent 失败，我们很难知道它是根本没找到证据，还是已经找到证据却不会使用。SWE-Explore 因此把 repository exploration 单独拿出来，要求 Explorer 返回按重要性排序的代码区域，并在 line-level、rank-aware、budget-aware 的条件下评价。

这篇论文最有意思的地方不只是把 file-level localization 改成 line-level，而是 Gold Context 的构建方式：作者要求一个任务至少存在两条成功修复 trajectory，然后从这些成功 trajectory 实际读取过的代码中寻找共同 evidence，再对 optional reads 做 refinement 和人工审计，最后得到 trajectory-grounded core context。

整个逻辑可以概括为：

~~~text
SWE-bench Pass / Fail
        ↓
混合 exploration / reasoning / editing / validation
        ↓
单独抽出 Repository Exploration
        ↓
Successful Agent Trajectories
        ↓
实际读取过的代码 Region
        ↓
跨轨迹 Intersection
        +
Load-bearing Optional Evidence
        +
Human Audit
        ↓
Line-level Core Context
        ↓
Explorer 输出 Ranked Regions
        ↓
Exploration Metrics
        ↓
Restricted-context Repair
验证这些指标是否真的对应下游成功
~~~

如果只记住一件事，就是：

> **SWE-Explore 试图把“Agent 找到了什么 evidence”从最终 repair outcome 中拆出来，并用真正可执行的 restricted-context repair 检查这些中间指标是否有意义。**

---

# 1. 为什么 File-level Localization 已经不够用了？

假设真正重要的证据在 parser.py 第 620–670 行。

Explorer A 找到 parser.py，但把整个 2,000 行文件都暴露给模型；Explorer B 只给 600–690 行。

如果只看 File Recall，两者都是 1。

但实际上它们提供的 context 完全不同：

- A 的 evidence density 很低；
- B 的 evidence density 很高。

所以作者认为，仅仅问“有没有找到正确文件”已经不足以评价现代 Coding Agent。

真正应该继续问：

- 有没有找到正确 region？
- 暴露了哪些具体 line？
- 真正 evidence 排在多前？
- 有限 context budget 中，有多少是核心 evidence？
- 为了找到这些 evidence，是否暴露了大量外围代码？

因此 SWE-Explore 的基本输出单位是：

~~~text
(file path, start line, end line)
~~~

而不是文件。

这也是论文和 VLocBench 这类 file-level benchmark 最大的直接差异：file-level metric 可能把“同文件内部 attribution 已经漂移”完全隐藏掉。

---

# 2. Research Gap 到底是什么？

现有工作大致分两个极端。

一端是 end-to-end benchmark：

~~~text
Issue
 ↓
Agent
 ↓
Patch
 ↓
Tests
 ↓
Pass / Fail
~~~

它的优点是 outcome 真实。

问题是失败原因不可诊断：

- 没找到关键代码；
- 找到了但理解错；
- 理解对但 edit 错；
- edit 对但 validation / integration 错；

最后都是 0。

另一端是 localization benchmark：

~~~text
Issue
 ↓
File / Function Ranking
~~~

它比较容易诊断，但很多工作仍停留在 file-level 或 function-level，而且不一定证明这些 localization metric 真能预测 downstream repair。

SWE-Explore 真正想填的是这个空白：

> **建立一个 line-level、rank-aware、budget-aware 的 Repository Exploration benchmark，并验证这些 exploration metrics 是否真的和后续 repair outcome 相关。**

因此它必须同时解决两个难题：

1. 哪些 line 应该算 Core Evidence？
2. 评价这些 line-level prediction 的 metric 是否具有下游 construct validity？

---

# 3. Benchmark 数据从哪里来？

作者从多个 executable repository-level benchmark 中收集任务，包括 SWE-bench Verified、SWE-bench Pro 和 SWE-bench Multilingual。

但不是所有 task 都进入 SWE-Explore。

一个非常关键的筛选条件是：

> **同一个 issue 至少需要观察到两条成功修复 trajectory。**

成功 trajectory 来自多种强模型 / Agent 配置，并且必须真实通过原 benchmark harness。

最终 benchmark 包含：

- **848 个 issue**
- **203 个 repository**
- **10 种编程语言**

论文报告平均每个任务大约有：

- 4.3 个 Gold files
- 4.7 个 Gold regions
- 1,578 行 Gold lines
- 2.9 条 successful source trajectories
- 759 个非测试文件
- 约 179.6K non-test LOC

所以这并不是一个小搜索空间的 localization benchmark，而是真正 repository-scale 的 exploration setting。

---

# 4. 为什么非得要求至少两条成功轨迹？

假设只有一条成功 trajectory：

~~~text
A → B → C → D → 修复成功
~~~

你不知道：

- A 是关键 evidence；
- B 是无意的探索 detour；
- C 是真正 root evidence；
- D 只是最后确认。

单条成功路径无法区分“必要读取”和“偶然读取”。

如果有两条不同成功轨迹：

~~~text
T1: A → B → C → D
T2: A → C → E
~~~

那么 A 和 C 至少获得更强的行为证据：

> 两条独立成功路径都主动读取了它们。

作者把这种 **cross-trajectory agreement** 当成 Core Evidence 的起点。

但要非常谨慎：

> Cross-trajectory agreement 是 behavioral signal，不是 causal necessity。

多个 Agent 可能共享同一种搜索习惯，因此共同读取并不自动等于“修复必须依赖”。

---

# 5. Ground Truth 到底怎样构建？

这是全文最值得学习的方法部分。

## 5.1 第一步：从 trajectory 中抽取 Read Action

作者抽取可以明确映射到代码区间的读取行为，包括 editor view、cat、head/tail、sed -n、grep -n 等。

统一成：

~~~text
(path, start_line, end_line)
~~~

如果一个动作无法可靠映射到具体代码 interval，作者倾向于丢弃，而不是猜测 Agent 看到了哪些内容。

这是一种保守策略：

> 宁可少记录，也不要制造虚假的 context exposure。

## 5.2 第二步：对成功 trajectory 做 line-level intersection

例如：

~~~text
Trajectory 1:
parser.py:40–80

Trajectory 2:
parser.py:60–100
~~~

共同部分不是整个 parser.py，而是：

~~~text
parser.py:60–80
~~~

也就是说 intersection 真正发生在 line-level。

作者把它当成最保守的 Core Candidate。

## 5.3 第三步：为什么纯 Intersection 还不够？

假设存在两条正确 solution path：

~~~text
Path A:
查看 helper function 理解 invariant

Path B:
查看 regression test 理解同一个 invariant
~~~

helper 和 test 都可能是 load-bearing evidence。

但由于两条 trajectory 没有同时读取它们，纯 intersection 会把两者都删掉。

因此论文还保留各条 trajectory 中的 Optional Context，并从 optional reads 中提升少量真正 load-bearing 的区域。

## 5.4 第四步：Refinement + Human Audit

作者没有直接把所有 optional read 当作 Gold。

整体逻辑更接近：

~~~text
Cross-trajectory Intersection
        +
Potentially Load-bearing Optional Reads
        ↓
LLM-assisted Refinement
        ↓
Manual Audit
        ↓
Refined Core Context
~~~

所以最终 Gold 不是：

> 所有成功 Agent 看过的代码。

而是：

> 多条成功 trajectory 的共同 evidence，加上少量经 refinement 和人工确认的重要 optional evidence。

---

# 6. 这个 Gold Context 真的是“必要上下文”吗？

不能这么强地解释。

更准确的说法是：

> **trajectory-grounded, manually-audited core evidence**

而不是数学意义上的 causally necessary context。

为什么？

第一，共同读取不等于必要。

如果所有 Agent 都习惯先看 README、配置文件或某个入口模块，这种共同习惯也会出现在 intersection 中。

第二，benchmark 本身只保留有至少两条 successful trajectory 的 task。

也就是说它 condition on success。

那些：

- 所有 Agent 都找不到 evidence；
- exploration 最困难；
- 正好最能暴露 retrieval failure；

的任务反而不在数据集中。

因此 SWE-Explore 的 population 更准确是：

> **已知至少存在多条可成功探索路径的 repository issue。**

不是所有真实软件工程任务的无偏样本。

第三，Manual Audit 能去掉明显无关内容，却不能把 observational trajectory 转换成严格因果必要性证明。

这三个边界对解释论文非常重要。

---

# 7. Figure 2 应该怎么读？

Figure 2 实际上包含三条逻辑链。

第一条是 Gold construction：

~~~text
Successful Trajectories
        ↓
Read Actions
        ↓
Intersection
        ↓
Optional Evidence
        ↓
Refinement + Audit
        ↓
Core Context
~~~

第二条是标准 benchmark：

~~~text
Issue + Repository
        ↓
Explorer
        ↓
Ranked Regions
        ↓
Line-level Metrics
~~~

第三条是 downstream validation：

~~~text
Ranked Regions
        ↓
Restricted Repository View
        ↓
Fixed Patcher
        ↓
Patch
        ↓
Original Tests
~~~

第三条非常关键。

作者不想只说“我们定义了一个新的 F1，因此它有用”，而是进一步问：

> 如果 Explorer 的 metric 真高，把它选出的 context 交给一个固定 patcher，repair 是否真的更容易成功？

这就是这篇 benchmark paper 比较完整的一层 construct validation。

---

# 8. Metrics 到底测什么？

## 8.1 Line Precision / Recall

Recall：

> Core Evidence 有多少被 Explorer 覆盖？

Precision：

> Explorer 暴露的代码里，有多少属于 Core Evidence？

问题是：Optional Evidence 可能是合理的 solution-specific information。

所以作者并不只依赖严格 Precision。

## 8.2 HitFile

只问：

> 有没有到达正确文件？

这是最粗粒度。

## 8.3 HitRegion

问：

> 有没有碰到正确 region？

比 file-level 更细，但仍不要求完整覆盖。

## 8.4 nDCG@B

Normalized Discounted Cumulative Gain（nDCG）是一种 rank-aware metric。

这里的直觉是：

> 有用 evidence 越早出现越好。

例如两个 Explorer 最终都找到相同 Core：

~~~text
Explorer A:
第 1、2 个 region 就命中 Core

Explorer B:
先返回大量外围代码，最后才命中 Core
~~~

A 的 nDCG 更高。

论文主要关注有限 line budget 下的 nDCG，例如 nDCG@500。

所以它不仅问“有没有找到”，还问：

> 在固定 context budget 内，Evidence 排得够不够前？

## 8.5 First Useful Hit

First Useful Hit（FUH）问：

> 第一个真正有用 region 出现得多早？

它直接反映 Agent 多快第一次接触到 Core Evidence。

## 8.6 Context Efficiency

这是全文非常值得借鉴的指标。

它关注：

> Explorer 暴露的全部代码里，有多少属于 Core 或允许的 Optional Evidence？

直觉是：

~~~text
Useful / Permissible Evidence
-----------------------------
Total Exposed Context
~~~

论文还定义 Noise Rate：prediction 与 Core 和 Optional 都不重叠的比例。

但这里必须强调：

> Benchmark 里的 Noise Rate 只是“相对于当前 evidence definition 的 off-target context”。

它并不自动等于：

> “这些代码一定会伤害 LLM”。

---

# 9. 为什么统一 Top-5？

Refined Core 平均大约有 4.7 个 region，因此作者统一设置 Top-5。

这样 BM25、RAG、Agentic Explorer、specialized localizer 可以在同一输出接口下比较。

优点是公平。

缺点是它切掉了真实 Agent 很重要的一项能力：

> adaptive stopping。

真实 Agent 可能判断：

~~~text
这个问题只需要 2 个 region
~~~

也可能需要：

~~~text
这个问题至少 20 个 region
~~~

统一 Top-5 因此更准确地测的是：

> **固定 region budget 下，谁能把关键 evidence 排得更好。**

而不是完整 search policy。

---

# 10. Baseline 为什么要横跨四类方法？

论文比较了多种 Explorer，大体可分为：

1. Oracle / Random；
2. Classical lexical retrieval，如 BM25 / TF-IDF；
3. Dense RAG；
4. Agentic / specialized repository localization。

Agentic 方法包括 Claude Code、Codex、OpenHands、Mini-SWE-Agent、AweAgent 等；specialized localizer 包括 AutoCodeRover、LocAgent、OrcaLoca、CoSIL 等。

这组 baseline 真正想回答：

> Repository Exploration 是否只需要更好的 one-shot similarity retrieval？

结果显然不是。

Agentic Explorer 整体形成了更强的一层。

原因从机制上很好理解：

~~~text
One-shot Retriever:
Issue → similarity → code

Agent:
Issue
 ↓
搜索 symbol
 ↓
读 definition
 ↓
根据新 evidence 改 query
 ↓
找 caller / tests
 ↓
继续探索
~~~

Interactive exploration 本身就是 sequential decision process。

但要注意：这组实验无法告诉我们 Agent 到底哪个具体模块产生优势，因为模型、prompt、tool、search policy 往往一起变化。

---

# 11. Restricted-context Repair：全文最漂亮的一组验证

只做 exploration metric 很容易遭到质疑：

> 你定义的 metric 真的和修复有关吗？

作者因此做 restricted-context repair：

~~~text
Explorer Top-5 Regions
        ↓
隐藏 Repository 其他代码
        ↓
固定 GPT-5.4 + Mini-SWE-Agent
        ↓
生成 Patch
        ↓
运行原 Benchmark Tests
~~~

主要结果：

| Explorer | Resolve Rate |
|---|---:|
| Oracle | **59.7%** |
| CoSIL | **59.3%** |
| Codex | **50.3%** |
| Mini-SWE-Agent | 50.0% |
| Claude Code | 48.0% |
| OpenHands | 47.7% |
| OrcaLoca | 45.3% |
| AutoCodeRover | 44.7% |
| LocAgent | 44.7% |
| AweAgent | 41.3% |
| TF-IDF | 26.0% |
| RAG | 23.3% |
| BM25 | 12.7% |
| Random | **4.7%** |

第一眼最容易关注 CoSIL 几乎追平 Oracle。

但真正值得注意的是：

> **Oracle 也只有 59.7%。**

这说明：

~~~text
Evidence Availability
≠
Patch Success
~~~

即使 evidence 质量很好，Agent 仍然可能：

- reasoning 错；
- edit 错；
- integration 错；
- 对 tests / API 理解错。

因此 repository exploration 和 patch synthesis 确实是两个不同瓶颈。

---

# 12. Oracle 只有 59.7%，是不是说明 Gold Context 不充分？

不能直接这么说。

至少有三种解释：

1. Gold Context 漏掉某些 solution-specific evidence；
2. Gold Context 足够，但固定 patcher 没能力正确使用；
3. restricted-context environment 比真实 Agent 工作方式更苛刻。

所以这组实验真正支持的是：

> **正确 context 本身并不会自动产生正确 patch。**

而不是：

> “Gold Context 只有 59.7% 是充分的。”

---

# 13. 哪个 Metric 最能预测 Repair？

作者比较不同 Explorer 的 exploration metric 和 downstream restricted-context resolve rate。

最醒目的结果是：

> **Context Efficiency：Pearson r = +0.950，Spearman ρ = +0.739。**

这说明在 Explorer 这一聚合层面，Context Efficiency 与下游修复表现高度相关。

这支持：

> “不仅要找到 evidence，还要尽量减少暴露的外围 context。”

但仍然只能写成 correlation。

不能写成：

> “提高 Context Efficiency 会因果提升 repair performance。”

因为更强 Explorer 可能同时在其他维度更强。

---

# 14. Ground Truth Ablation 到底在验证什么？

作者没有只相信一种 Gold construction，而是比较不同聚合策略，例如：

- Pure Intersection；
- Refined Core；
- 更宽的 Union / Optional。

它检验的不是传统神经网络模块，而是：

> **主实验结论会不会只是某一种 trajectory aggregation rule 的 artifact？**

三种思路的 trade-off 很直观：

### Pure Intersection

优点：

> 干净、保守。

缺点：

> 容易漏掉 solution-specific evidence。

### Union

优点：

> Coverage 高。

缺点：

> 容易把 exploratory detour 也当 Gold。

### Refined Core

折中：

> intersection + 少量 load-bearing optional + refinement / audit。

所以这个 ablation 更像 measurement validity check，而不是“去掉模块 A 性能掉多少”。

---

# 15. 最大的 Selection Bias：Conditioning on Success

这是读这篇论文最不能忽略的一点。

一个 task 要进入 SWE-Explore，至少存在两条 successful trajectory。

所以它研究的其实是：

> **在强 Agent 已经证明存在多条成功 solution path 的任务中，其他 Explorer 能否找到类似核心 evidence？**

它不是：

> 所有真实 repository task 的探索难度。

这会系统性排除：

- 所有强 Agent 都迷路的 task；
- evidence acquisition 极难的 task；
- 恰恰最需要研究的 retrieval failure case。

因此不能拿 SWE-Explore 的平均表现去代表整个软件工程任务分布。

---

# 16. “多个成功 Agent 都看过”是不是 Necessary Evidence？

仍然不是。

这是本文最重要的 construct-validity 边界。

例如所有 Agent 都习惯：

~~~text
Issue
 ↓
README
 ↓
config
 ↓
source
~~~

README 即使不是 necessary evidence，也可能反复出现在 successful trajectory intersection。

所以：

> Cross-trajectory agreement 提升了“这段 context 很可能重要”的可信度。

但它没有完成：

> “必要性”的因果识别。

Manual Audit 可以缓解明显冗余，却不能把 observational trajectory 变成严格 causal proof。

---

# 17. 作者证明了什么？

可以较有把握地记住五点。

1. **Repository Exploration 可以独立 formalize 成 ranked line-region selection task。**
2. **多个 successful Agent trajectory 的 observable reads 可以作为大规模 line-level evidence supervision 的来源。**
3. **Agentic Explorer 整体明显强于 classical one-shot retrieval；现代方法在 file-level 已经不差时，line-level ranking 更能拉开差距。**
4. **Restricted-context repair 与 exploration quality 高度相关，特别是 Context Efficiency。**
5. **Correct evidence availability 并不自动等于 repair success，exploration 与 patch synthesis 是两个不同瓶颈。**

---

# 18. 作者没有证明什么？

同样重要的是它没有证明：

1. successful trajectories 共同读取的每一行都是 causally necessary；
2. Optional 之外的代码都是 useless noise；
3. Context Efficiency 的提高会因果提升 repair；
4. 848 个 task 能代表所有真实 repository issue；
5. extra context 本身一定伤害模型；
6. line-level Core 是唯一正确的 evidence path。

尤其是第五点。

这篇论文更强地说明的是：

> **Missing decisive evidence 很危险。**

它并没有直接证明：

> **Extra non-decisive evidence 一定危险。**

这两者必须分开。

---

# 19. 真正应该记住什么？

如果几天后导师突然问这篇论文，可以直接讲这六句：

1. **SWE-Explore 的核心不是提出一个新 localizer，而是把 repository exploration 建成 ranked line-level evidence task。**
2. **Gold 不是 patch lines，而是多个成功 Agent trajectory 的共同 read regions，再加 optional evidence refinement 和人工 audit。**
3. **数据规模是 848 issue / 203 repo / 10 languages，每个 task 至少有两条 successful trajectory。**
4. **Restricted-context validation 很关键：只给固定 patcher Explorer 选出的 context，再真正跑原 benchmark tests。**
5. **Oracle 59.7% vs Random 4.7% 说明 context selection 非常重要，但 evidence availability 和 patch synthesis 是两个不同瓶颈。**
6. **最大的理论边界是：trajectory-grounded evidence 不等于 causally necessary evidence。**

---

# 20. 对当前研究的启发

到这里才应该把论文接回当前 VLocBench / plausible-context 主线。

## 20.1 File F1 很可能太粗

假设两个 condition 最终都定位到：

~~~text
vyper/semantics/types/function.py
~~~

File F1 完全相同。

但内部可能是：

~~~text
Condition A:
关注真正 patch-associated function

Condition B:
被同文件 sibling function 吸引
最后仍报同一个 file
~~~

这正是当前实验最可能漏掉的 attribution shift。

因此 outcome 最好拆成：

~~~text
Core Evidence Coverage
        ↓
Core Evidence Rank
        ↓
Context Efficiency
        ↓
Mechanism Correctness M
        ↓
Attribution Correctness A
        ↓
File / Patch Outcome
~~~

尤其值得继续观察：

~~~text
P(M = 1, A = 0)
~~~

也就是：

> 机制理解仍然正确，但 evidence attribution 已经发生偏移。

## 20.2 Core / Optional 的思想可以直接借鉴

当前最危险的标签仍然是：

~~~text
non-GT = distractor
~~~

更稳妥的分类应该是：

- Core / Necessary Candidate
- Potentially Useful / Optional
- Audited Non-decisive
- Conflicting
- Unknown

只有经过独立 evidence audit 的 non-decisive context，才适合作为 plausible distractor treatment。

## 20.3 Restricted-context protocol 可以改造成 Sufficiency Gate

正式比较 plausible vs random 之前，可以先做：

~~~text
只给 Core Evidence
        ↓
固定模型
        ↓
Mechanism / Localization 是否稳定正确？
~~~

如果 Core-only 本身无法稳定解题，那么：

~~~text
Core + plausible
vs
Core + random
~~~

的差异会同时混合：

- 补充缺失 evidence；
- 引入 interference。

这样 causal interpretation 会很弱。

## 20.4 SWE-Explore 还提供了一个重要反方向证据

当前 Coding Agent 的主要瓶颈可能首先是：

> **missing decisive evidence**

而不是：

> “多一点 noise 就会崩”。

所以论文故事不应该预设 More Context Hurts。

更值得检验的是一个更窄、更有辨识度的问题：

> **When sufficient evidence is already present, does plausible-but-non-decisive repository context cause a larger attribution shift than matched random context?**

如果结果是 plausible ≈ random，也应该接受。

那会说明模型对这种 plausible interference 其实比较 robust，主要问题仍然是 evidence acquisition。

如果出现：

~~~text
Mechanism Correctness 基本不变
Attribution Accuracy 明显下降
plausible > random
~~~

这才是当前研究真正有意思的机制发现。

---

# 最后一句

**SWE-Explore 最值得带走的不是“又一个 repository localization benchmark”，而是它把“模型看了什么”从模糊的文件命中或 token 数，推进到可审计的 line-level evidence exposure，并用 restricted-context repair 验证这个中间变量确实和最终任务有关。对当前研究最自然的升级，是固定 sufficient core 后操纵 extra context，再用 node/line-level exposure、retention 与 attribution 做 mediator，而不是继续只盯 file-level F1。**
