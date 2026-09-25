
# ContextBench：A Benchmark for Context Retrieval in Coding Agents

> 精读日期：2026-09-25  
> 作者：Han Li, Letian Zhu, Bohan Zhang, Rili Feng, Jiaming Wang, Yue Pan, Earl T. Barr, Federica Sarro, Zhaoyang Chu, He Ye  
> 机构：南京大学、University College London（UCL）  
> 明确通讯作者：Zhaoyang Chu、He Ye  
> arXiv：2602.05892  
> 项目：https://github.com/EuniAI/ContextBench  
> 关键词：Coding Agent、Repository Context、Context Retrieval、Gold Context、Trajectory、Evidence Utilization

# 先把整篇论文装进脑子里

这篇论文研究的不是“Coding Agent 最后能不能修好 issue”，而是一个更靠前、也更容易被最终 Pass@1 掩盖的问题：

> **Agent 在修一个真实仓库问题时，到底有没有找到真正需要的代码上下文？找到了多少？又带进来了多少额外代码？最后真正用于生成补丁的上下文，和它探索过程中看过的上下文是不是一回事？**

作者的核心做法是建立 **ContextBench**：从四个已有 repository-level issue-resolution benchmark 中筛出 1,136 个任务，人工为每个任务标出“解决这个问题所需要的 gold context”，而且不只给文件级标签，还做到 definition-level block 和 line level。随后把 Coding Agent 的完整 trajectory 解析成“它每一步看了哪些代码”，从而把最终修复成败拆开，单独评价 context retrieval。

如果只记住本文一个思想，就是：

> **最终 patch 是否通过测试，和 Agent 是否正确获取、筛选、保留了解题证据，是两件不同的事。ContextBench 试图给后者建立可测的 ground truth。**

论文最重要的实证结果有四个：

1. 更复杂的 Agent scaffold 并不自动带来更好的 context retrieval；简单的 mini-SWE-agent 在不少 retrieval metric 上反而更强。
2. 即使是 GPT-5、Claude Sonnet 4.5、Gemini 2.5 Pro、Devstral 2，block/line 级的 context F1 仍不高；模型普遍存在 recall–precision trade-off。
3. 不同模型采取完全不同的 retrieval style：有的少量大块读，有的很多次小块读；“找得多”不等于“找得好”。
4. Agent 在探索途中明明见过正确 evidence，最后却可能没有把这些 evidence 保留进最终声明的 patch context。作者把这种现象量化为 Usage Drop。

这四点里，前两点讲“找什么”，第三点讲“怎么找”，第四点讲“找到了以后有没有留下来”。

---

# 1. 为什么还需要一个 ContextBench？

## 1.1 过去的 benchmark 主要看终点，不看过程

SWE-bench 一类 benchmark 的典型评价是：给 Agent 一个真实 GitHub issue 和对应 repository，让它修改代码，最后跑测试，看 patch 是否正确。

这种评价当然重要，因为最终目标就是把问题修好。但它有一个天然盲区：

~~~text
Agent A
找到正确文件 → 找到关键函数 → 理解依赖 → 正确修改 → PASS

Agent B
到处 grep / cat → 看了一堆额外文件 → 反复试错 → 碰巧改对 → PASS
~~~

如果只看 Pass@1，两者完全一样。

所以作者真正不满意的不是“现有 benchmark 不准确”，而是：

> **现有 benchmark 对 context acquisition 这个中间能力不可观测。**

Repository-level software engineering 又恰好非常依赖这一层：仓库很大，Agent 必须先决定去哪找、看哪些文件、看多少行、什么时候停止。

因此论文的 Research Gap 是：

~~~text
已有 benchmark
      ↓
能评价最终 issue resolution
      ↓
但不知道 Agent 是否找到了必要 evidence
      ↓
无法区分 retrieval failure 与 reasoning / editing failure
      ↓
ContextBench：
为必要代码上下文建立人工 Gold Context
并评价 Agent trajectory 与 Gold Context 的关系
~~~

这里有一个非常重要的边界：**“看到正确 context”不等于“真正理解代码”。**

ContextBench 测的是 observable retrieval / exposure，而不是模型内部 reasoning state。所以把它称为 process-oriented evaluation 是合理的；如果进一步说“它证明 Agent 真正理解了 repository”，就超过证据了。

---

# 2. 读懂全文前必须掌握的四个概念

## 2.1 Gold Context

Gold Context 是作者认为**解决某个 issue 所需要的关键代码区域**。

它不等于 patch。

Patch 告诉我们“最终改了哪里”；Gold Context 试图回答“为了知道该怎么改，你还必须看哪里”。

例如 patch 修改 foo.py 里的 save()，但为了知道如何修改，开发者可能还要看：

- Config 类如何定义字段；
- 谁调用 save()；
- 某个 helper 怎样约束同一字段；
- interface / inheritance contract。

这些位置不一定被修改，却可能是解题证据。

所以本文的逻辑是：

~~~text
Gold Patch
   ↓ dependency tracing
Gold Context
~~~

而不是 Gold Patch = Gold Context。

## 2.2 File / Block / Line 三种粒度

### File level

只看文件路径。

如果 Gold Context 包含 src/parser.py，Agent 只要打开这个文件，就会获得 file-level hit。

优点是稳定；缺点是非常粗。一个 2,000 行文件里只需要一个函数，整文件访问仍然算命中文件。

### Block level

这里的 block 不是任意 AST 节点，而主要是 definition-level semantic unit，例如 function、method、class、interface、trait 等。

作者用 Tree-sitter 统一解析多语言代码，再把 Agent 访问的代码范围映射到这些 definition block。

这比 file level 更接近“Agent 到底看到了哪个程序实体”。

### Line level

直接比较具体行范围，是最细粒度。

这三个粒度一起用的意义是：

> Agent 可能 File Recall 很高，因为它打开了正确文件；但 Line Precision 很低，因为它把整个文件乃至周边大量代码都读了。

所以单纯 file-level localization 很容易高估 retrieval quality。

## 2.3 Recall 和 Precision

Recall 问：

> **该看的东西，我看到了多少？**

Precision 问：

> **我看的东西里，有多少属于 Gold Context？**

如果 Agent 为了不漏 evidence，把大量 repository 内容都读进来：

- Recall 可能提高；
- Precision 会下降。

这就是全文反复出现的 Recall–Precision Trade-off。

## 2.4 Trajectory Context 和 Final Context

Agent 执行时会不断 grep、cat、sed、跳转函数、回访文件。

这些构成 **trajectory / explored context**。

但作者还要求 Agent 在最终 submit 前声明自己认为关键的代码范围，形成 **final context**。

于是可以问：

> Agent 曾经看到的 Gold Evidence，有多少最后还留在它提交 patch 前声明的重要 context 中？

这就是后面 Usage Drop 的基础。

---

# 3. ContextBench 是怎么构建出来的？

整个 pipeline 是：

~~~text
四个已有 benchmark，共 4,497 tasks
        ↓
Step 1 任务去重
        ↓
约 3,100 unique tasks
        ↓
Step 2 难度 / context-demand 筛选
        ↓
约 1,500 candidate tasks
        ↓
人工过滤语义简单或不适合的任务
        ↓
1,136 tasks
        ↓
Step 3 专家 annotation
        ↓
file / block / line Gold Context
        ↓
LLM patch-generation verification
        ↓
compactness / consistency 检查
        ↓
ContextBench
~~~

这部分是理解整篇论文的核心，因为后面的 Precision / Recall 是否有意义，完全依赖 Gold Context 是否可信。

---

# 4. Step 1：从 4,497 个任务开始去重

原始任务来自四个 benchmark：

- SWE-bench Verified：500
- Multi-SWE-bench：1,632
- SWE-PolyBench PB500：500
- SWE-bench Pro：1,865

合计 **4,497**。

作者没有直接选一个 benchmark，是因为希望覆盖更多语言、更多 repository、更多复杂 issue。

但不同 benchmark 之间会重叠，因此需要两层去重。

## 4.1 Exact Deduplication

先用 repository、issue、metadata 等信息去掉明确重复。

它解决“完全同一个任务被多个 benchmark 收录”的问题。

## 4.2 Semantic Near-Duplicate

然后再用 embedding similarity 识别语义近重复。论文报告大约使用 **0.90 cosine similarity threshold**，对边界 case 再人工检查。

为什么还需要这一层？

因为同一个 issue 在不同 benchmark 中可能经过：

- title 清洗；
- description 重排；
- 格式转换；
- metadata 变化。

字符串不同，但本质仍是一个任务。

经过这一阶段，4,497 个任务约剩 **3.1k**。

### 这一阶段的证据边界

Embedding 去重仍依赖 threshold：

- threshold 太高，可能漏掉近重复；
- 太低，可能错误合并相似但不同的问题。

人工检查能缓解，但不是绝对客观。它主要影响 benchmark diversity，而不是后面单个 task 的 Gold Context 正确性。

---

# 5. Step 2：为什么主动筛“难任务”？

因为 ContextBench 要测的是 **repository context retrieval**。

如果一个 task 只需要打开一个明显的小文件、改一行常量，Context Retrieval 几乎没有挑战。

所以作者不随机抽样，而是主动富集更需要 repository exploration 的任务。

## 5.1 Agent Solvability

如果绝大多数 Agent 都轻易解决，任务区分度有限。

作者因此降低过于容易任务的比重。

## 5.2 Edit Scope

修改范围大，通常意味着更可能涉及多处代码。

但这是 proxy，不是真理。

一次机械 rename 可以改很多文件，却并不需要复杂 reasoning。

## 5.3 Edit Dispersion

作者还看修改是否分散在不同区域或模块。

集中在一个局部和跨模块修改，对 repository navigation 的要求不同。

Appendix 还提到 limited-scope task：例如 Gold Context 中少于四个 distinct code hunks 的任务，可能不足以有效考查多步 retrieval。

筛选后约剩 **1.5k tasks**。

随后再人工排除一些“patch 看起来很大，语义却很简单”的任务，例如 bulk formatting、机械 rename 等。

最终得到 **1,136 个任务**。

### 这里必须记住的 selection effect

ContextBench 不是现实 GitHub issue 的随机样本，而是一个**主动富集 context-demanding task 的 challenge benchmark**。

所以不能拿它的平均 context 数量去声称：

> “真实软件工程问题平均就需要这么多 repository context。”

它描述的是筛选后的 population。

---

# 6. Step 3：Gold Context 到底怎样人工标出来？

这是整篇论文最关键的一步。

## 6.1 Annotator 不是从 issue 盲搜，而是从 Gold Patch 反向追

Annotator 已知官方 patch。

这是 **answer-aware annotation**。

他们从被修改的位置出发，追问：

> 为了知道这一处为什么要这样改，一个开发者还需要理解哪些代码？

然后沿程序关系向外 trace。

论文明确提到：

- function invocation
- class invocation
- inheritance relation
- control-flow path
- data-flow path
- 同文件 / 同模块中语义相关代码。

直觉上就是：

~~~text
Patch location
  ↓
这里依赖哪些函数 / 类 / 变量？
  ↓
定义在哪里？
  ↓
caller / contract / state 在哪里？
  ↓
继续追真正与修复有关的依赖
  ↓
删掉明显冗余区域
~~~

这和“把 patch 文件全部当 Gold”完全不同。

## 6.2 Annotation Frontend

作者做了专门的轻量 IDE 式标注界面。

Annotator 可以：

- 浏览 repository；
- 跳转 function / variable reference；
- 查 class definition；
- 选择精确代码范围。

所以它不是简单在 PDF 旁边手抄 line number，而是提供 repository navigation 支持。

## 6.3 谁在标？成本多高？

论文报告：

- 六位作者及 expert developers 协作；
- 标注持续约四个月；
- annotator 有三年以上大型代码库开发经验；
- 单个 issue 约 **20 分钟到 1.5 小时**；
- 平均约 **40 分钟 / issue**。

这也是为什么 ContextBench 的人工成本很高。

---

# 7. “必要上下文”这么主观，作者怎么验证？

只说“专家觉得必要”还不够。

作者增加了 **Context Verification**。

直觉是：

> 如果这份 Gold Context 真包含解决 issue 所需的主要证据，那么一个足够强的模型在只拿到这些 context 时，至少应该有机会生成正确 patch。

因此作者使用强模型做 patch-generation verification：

~~~text
Issue Description
      +
Annotated Gold Context
      ↓
GPT-5 尝试生成 patch
      ↓
运行官方测试
      ↓
如果无法解决
→ Gold Context 可能缺 evidence
→ 返回人工 annotation 修订
~~~

这主要验证 **sufficiency**。

同时 annotator 被要求遵循 **compactness principle**，尽量删掉 redundant / irrelevant code。

## 7.1 它验证了什么，没验证什么？

它比较有力地支持：

> 这套 context 对解决任务是足够的。

但它没有严格证明：

> Gold Context 中每一行都是不可删除的必要条件。

“足够”与“逐元素必要”不是一回事。

因此更准确的叫法是：

> **expert-curated, compact-and-verified sufficient context**

而不是数学意义上的 globally minimal necessary context。

这会直接影响后面 Precision 的解释：

**non-gold 不自动等于 useless。**

---

# 8. 最终 Benchmark 的规模

最终包含：

- **1,136 tasks**
- **66 repositories**
- **8 programming languages**
- **4,548 gold files**
- **23,116 gold blocks**
- **522,115 gold lines**

按语言：

| Language | Repos | Tasks |
|---|---:|---:|
| Python | 20 | 512 |
| Java | 6 | 57 |
| JavaScript | 9 | 153 |
| TypeScript | 8 | 119 |
| Go | 7 | 104 |
| Rust | 9 | 63 |
| C | 3 | 68 |
| C++ | 4 | 60 |

虽然已经明显比 SWE-bench 更 multilingual，但 Python 仍然占 512 / 1,136，约 45%，语言分布并不均衡。

---

# 9. 不同 Agent 的日志格式不同，怎么统一评价？

不同 Agent 的工具完全不同：

- mini-SWE-agent 常用 bash、cat、sed、grep；
- SWE-agent 使用自己的 editor / view interface；
- OpenHands 有不同的文件导航工具；
- Agentless 是 pipeline-style retrieval；
- Prometheus 还包含 graph-based repository retrieval。

ContextBench 因此做 trajectory extractor，把不同格式统一成：

~~~text
Step 1:
  file A, lines 10–80

Step 2:
  file B, lines 120–170

Step 3:
  file A, lines 60–110
~~~

再用 Tree-sitter 映射到 definition blocks。

## 9.1 为什么额外要求 Final Context Declaration？

“Agent 看过什么”可以从 trajectory 抽取。

但“最终生成 patch 前它认为哪些 evidence 重要”并不容易知道。

作者因此对多个 Agent 加入 pre-submission constraint：

> 最终 submit 前先明确声明 precise code context。

于是获得：

~~~text
Trajectory Context
= 整个探索过程中访问过的代码

Final Context
= 最终提交前显式声明的重要代码
~~~

这为 RQ4 的 Usage Drop 提供了可观测数据。

但要非常谨慎：

> Final Context 是 Agent 的显式声明，不是内部 attention 或 latent reasoning 的直接观测。

模型可能实际利用过某段代码却没声明，也可能声明了但并没有真正依赖。

所以 Usage Drop 更准确叫：

**retrieved gold evidence → declared-final gold evidence 的下降**。

---

# 10. 整体实验设计：五个 RQ 怎样分工？

论文的五个 RQ 可以分成三层：

~~~text
RQ1：固定 GPT-5
     改变 Agent scaffold
     → Agent architecture 影响 retrieval 吗？

RQ2：固定 mini-SWE-agent
     改变 LLM backbone
     → Model 本身影响 retrieval 吗？

RQ3–RQ4：
     看 retrieval pattern 与 trajectory dynamics
     → 模型怎么找？找到后保留了吗？

RQ5：
     检查 measurement instrument 本身
     → Gold Context 会不会依赖某个特定 patch？
~~~

这个结构是论文实验设计做得比较漂亮的地方：尽量把 **Model Effect** 和 **Agent Scaffold Effect** 分开。

---

# 11. RQ1：复杂 Agent scaffold 更会找 Context 吗？

## 11.1 设计

固定 backbone 为 **GPT-5**，改变 agent framework：

- mini-SWE-agent：简单 bash-based iterative agent；
- Agentless：pipeline-style / semantic retrieval；
- SWE-agent：专用 agent-computer interface；
- OpenHands：更完整的开发 runtime / navigation；
- Prometheus：graph-based repository retrieval。

真正问的是：

> 模型一样，只换 scaffold，context retrieval quality 会不会变好？

## 11.2 Table 2 怎么读？

每个 Agent 都报告：

- File Recall / Precision / F1
- Block Recall / Precision / F1
- Line Recall / Precision / F1
- Pass@1

### mini-SWE-agent

File：
- Recall 0.682
- Precision 0.709
- F1 0.634

Line：
- Recall 0.606
- Precision 0.301
- F1 0.312

Pass@1 = 0.472。

最明显的是：**从 File 到 Line，Precision 掉得很厉害。**

说明它经常能找到正确文件，但在文件内读取范围较宽。

### OpenHands

File Recall = **0.733**，比 mini-SWE-agent 高。

但：
- File Precision = 0.400
- File F1 = 0.463

这是典型的 broad exploration：

> 宁可打开更多文件，也尽量不漏 evidence。

Recall 上去了，但 Precision 大幅下降。

### Prometheus

- File Recall = 0.717
- Block Recall = 0.646
- Block Precision = 0.258
- Line Recall = 0.584
- Line Precision = 0.195
- Pass@1 = **0.512**

它的 Pass@1 是这五个系统里最高，但 context precision 并不好。

这非常重要：

> **最终修复成功率最高的 Agent，不一定拥有最“干净”的 Gold-relative context。**

因此 Context Retrieval 和 End-to-End Success 有关系，但绝不是一一对应。

### Agentless

Agentless：
- File Recall 0.609
- File F1 0.390
- Line Recall 0.461
- Line Precision 0.318
- Line F1 **0.376**

它在 file-level 看起来不强，但 line-level F1 很有竞争力。

这说明不同 Agent 的 trade-off 可能只在细粒度指标里暴露出来。

## 11.3 作者的结论

作者把结果概括成类似 “Bitter Lesson”：

> sophisticated scaffold 不一定带来更好的 context retrieval，当前 Agent architecture 可能存在 over-engineering。

在本文实验里，“复杂度不保证 retrieval 更好”是有数据支持的。

## 11.4 但这不能证明“复杂 Agent 没用”

原因有三层。

第一，Agent 的目标不是只优化 compact Gold Context F1。它还要跑测试、排除错误 hypothesis、理解环境等。

第二，Gold Context 是 compact reference。Agent 访问一个合理但不在 reference 中的 helper，会降低 Precision，但这不等于那次访问毫无价值。

第三，为了统一评价，论文对不同 Agent 加入了 context declaration / extraction adaptation；这不是每个 Agent 原封不动的生产配置。

### RQ1 Takeaway

**更复杂的 Agent scaffold 没有稳定改善 Gold Context retrieval；不同 scaffold 更像是在选择不同的 recall–precision trade-off，而不是复杂度越高，证据定位越准。**

---

# 12. RQ2：固定 Agent 后，不同 LLM 自己会不会找 Context？

固定 mini-SWE-agent，只替换 backbone：

- GPT-5
- Claude Sonnet 4.5
- Gemini 2.5 Pro
- Devstral 2

这样就把问题从“Agent 设计好不好”变成：

> 同一个最小 scaffold 下，不同模型自身怎样搜索 repository？

## 12.1 GPT-5

File：
- Recall 0.682
- Precision 0.709
- F1 0.634

Block：
- Recall 0.645
- Precision 0.369
- F1 0.375

Line：
- Recall 0.606
- Precision 0.301
- F1 0.312

Pass@1 = **0.472**

特征非常明确：**Recall 强，但粒度越细，Precision 越低。**

## 12.2 Claude Sonnet 4.5

- File Recall 0.720
- File Precision 0.665
- File F1 0.624
- Block Recall 0.631
- Block Precision 0.449
- Block F1 0.420
- Line Recall 0.588
- Line Precision 0.374
- Line F1 **0.344**
- Pass@1 **0.530**

Claude 的关键不是“找最多”，而是更平衡。

GPT-5 的 Line Recall 0.606 > Claude 0.588；

但 Claude 的 Line Precision 0.374 > GPT-5 0.301。

最后 Claude 的 Line F1 和 Pass@1 都更高。

## 12.3 Gemini 2.5 Pro

它更偏 precision：

- File Precision 0.752
- Block Precision **0.632**
- Line Precision **0.529**

但：
- Block Recall 0.393
- Line Recall 0.313
- Pass@1 0.364

这说明另一端也有问题：太保守会漏掉关键 evidence。

## 12.4 Devstral 2

- File Recall 0.660
- Precision 0.693
- F1 0.615
- Block F1 0.422
- Line F1 0.332
- Pass@1 0.402

整体处于另一种折中位置。

## 12.5 Recall–Precision Trade-off 到底说明什么？

四个模型中，表现较好的不是单纯 Recall 最大，也不是 Precision 最大。

Claude 的行为更 balanced。

所以作者认为 retrieval 不应该只追求“覆盖越多越好”。

但注意：

### 论文没有证明“额外 Context 导致 GPT-5 变差”

这里比较的是不同模型。

GPT-5 和 Claude 的差异还包括：

- reasoning ability；
- instruction following；
- code generation；
- tool choice；
- patch synthesis。

因此不能从 Table 3 得出因果结论：

> GPT-5 因为读取更多 extra context，所以 Pass@1 比 Claude 低。

这最多是一个可能解释。

### RQ2 Takeaway

**Frontier LLM 仍难同时做到高覆盖和高精度；ContextBench 能把不同模型的 retrieval style 从最终 Pass@1 中拆出来，但跨模型相关性不能直接证明 context noise 导致 repair failure。**

---

# 13. RQ3：模型是“怎么找”的？

RQ3 不再只看最终 aggregated context，而看 retrieval pattern。

Table 4：

| Model | Avg Steps | Avg Lines / Step | Avg Cost |
|---|---:|---:|---:|
| GPT-5 | **5.87** | **119.29** | $0.45 |
| Claude Sonnet 4.5 | 14.38 | 29.74 | $0.76 |
| Gemini 2.5 Pro | 7.57 | 26.29 | **$0.38** |
| Devstral 2 | **22.16** | **11.98** | **$0.91** |

## 13.1 GPT-5：少次、大块

5.87 steps，但每步约 119 行。

它像：

> 不一点点试，一次直接读较大的代码块。

这和它高 Recall、低 Line Precision 的结果是相容的。

## 13.2 Devstral 2：多次、小块

22.16 steps，每次约 11.98 行。

它像：

> 一点点探，每次只看小范围。

看起来更精细，但交互次数多，成本反而最高 $0.91。

所以“小块 retrieval”不自动等于低成本。

## 13.3 Claude：中间路线

14.38 steps，29.74 lines / step。

作者认为这种更 balanced 的 style 与它更好的 Line F1 和 Pass@1 相吻合。

这里必须说“相关”，不能说“导致”，因为作者没有把同一个模型强制改成不同 lines/step 做随机 intervention。

## 13.4 这张表真正教我们什么？

“Context Quantity”至少有两个维度：

~~~text
Retrieval Breadth
= 每一步看多少

Exploration Frequency / Depth
= 一共查多少次
~~~

两个 Agent 最后总共看相似数量的 token，也可能采用完全不同的过程。

### RQ3 Takeaway

**Repository retrieval 不能只用总 token 数描述；retrieval frequency 与 per-step granularity 是两个不同的行为维度。**

---

# 14. RQ4：找到 Evidence 以后，最后还在吗？

Table 5：

| Model | Efficiency ↑ | Redundancy ↓ | Usage Drop ↓ |
|---|---:|---:|---:|
| GPT-5 | 0.591 | **0.487** | **0.179** |
| Claude Sonnet 4.5 | **0.658** | 0.708 | 0.196 |
| Gemini 2.5 Pro | 0.529 | 0.558 | 0.431 |
| Devstral 2 | 0.616 | 0.672 | **0.435** |

## 14.1 Efficiency

作者用类似 Area Under Coverage Curve（AUC-Cov）的思想衡量：

> Agent 多早覆盖 Gold Context？

如果最终 Recall 一样，但 A 在前几步就找到大部分 Gold，而 B 到最后才找到，A 更高效。

Claude = 0.658，为四者最高。

## 14.2 Redundancy

Redundancy 衡量重复访问 / 重叠 context。

Claude 虽然 Efficiency 最好，但 Redundancy = 0.708 很高。

所以它可能很早找到 evidence，但之后不断 revisit。

作者提出一种可能解释：Claude 会反复查看已访问区域来维持对重要 code 的覆盖。

这只是作者对行为的解释，论文没有进一步验证“为什么”。

## 14.3 Usage Drop

这是全文最有价值的中间指标之一。

直觉：

~~~text
Trajectory 中曾覆盖的 Gold Evidence
                ↓
Final Context 中仍声明的 Gold Evidence
                ↓
中间丢掉了多少？
~~~

- GPT-5 0.179
- Claude 0.196
- Gemini 0.431
- Devstral 0.435

Gemini 和 Devstral 明显更高。

作者因此指出：

> 有些 Agent 不是“没找到”，而是“找到以后没有把 evidence consolidation 到最终 context”。

于是过程可以拆成：

~~~text
Evidence Acquisition
       ↓
Evidence Consolidation / Retention
       ↓
Patch Generation
~~~

## 14.4 “Usage” 不能解释得太实

它真正观测到的是：

> 是否出现在 final declared context。

它不是内部 causal attribution。

模型可能看过某段 code，已经把信息吸收到 conversation state，最后却没有显式声明。

因此更准确理解为：

**Declared Evidence Retention / Consolidation**

而不是“模型脑内是否使用”。

### RQ4 Takeaway

**Retrieval failure 不只发生在“没找到”，还发生在“找到后没有保留到最终声明的 context”；ContextBench 因此把 acquisition 和 consolidation 分成了两个阶段。**

---

# 15. RQ5：Gold Context 会不会只是绑定某一个官方 Patch？

因为 Gold Context 是从 Gold Patch 反向 trace 出来的，自然会有一个强质疑：

> 同一个 issue 可能有两个完全不同但都通过测试的修法。换一个 patch，会不会得到另一套完全不同的 Gold Context？

如果会，那么 Agent 走另一条合法路径也可能被错误判成 retrieval failure。

## 15.1 作者怎么测？

找了 **82 个 task**。

每个 task 有两份：

> 语义等价、都 test-passing，但语法实现不同的 patch。

对两个 patch 分别按同样流程构建 patch-conditioned Gold Context。

然后用 **Jaccard Similarity** 比较两份 context。

Jaccard 的直觉：

- 完全一样 → 1
- 完全不重叠 → 0

## 15.2 结果

平均 Jaccard similarity：

**0.9518**

对应 distance 约 0.0482。

这说明在这 82 个 case 中，即使 patch 写法不同，主要 repository evidence 高度稳定。

## 15.3 证明到哪里？

它很好地缓解了：

> Gold Context 只是某一个 official patch artifact

这个担忧。

但不能无限外推。

第一，只测了 82 / 1,136 个 task。

第二，两份 known passing patch 也不代表穷尽所有可能 solution path。

所以它支持 robustness，但不证明 Gold Context 是所有合法解法的唯一 evidence set。

### RQ5 Takeaway

**Gold Context 在 82 个 alternative-solution case 上对 patch choice 很稳定，但这仍然是 robustness case study，不是“唯一正确上下文”的证明。**

---

# 16. Figure 1 应该怎么看？

Figure 1 用 radar plot 分别比较：

- 不同 Coding Agent；
- 不同 LLM；

在 File / Block / Line 三个粒度上的 Precision / Recall / F1。

它最重要的视觉信息不是“谁面积最大”，而是：

> 很多系统 Recall 轴伸得更远，Precision 轴明显缩进去。

也就是作者所谓 recall-biased retrieval。

但 radar chart 不适合精确数字比较，所以真正判断谁更好仍要回 Table 2 / Table 3。

Figure 1 主要让你一眼看到：

> **覆盖得广 ≠ 上下文干净。**

---

# 17. Figure 2 / Figure 4：真正要看的是 Funnel

Construction Figure 不是只告诉你“有三个步骤”。

真正应该看：

~~~text
4497 raw tasks
  ↓ dedup
3100
  ↓ difficulty / context-demand filtering
1500
  ↓ annotation-quality / semantic filtering
1136
  ↓ expert tracing + verification
human-verified Gold Context
~~~

这个 funnel 暴露了 ContextBench 的 population：

> 它不是自然分布的所有 issue，而是经过去重、难度筛选、context-demand 筛选、annotation-quality 筛选后的 challenge set。

这直接决定外部有效性。

---

# 18. Baseline 设计是否公平？

论文做得比较好的地方是 RQ1 / RQ2 分离。

## RQ1 固定 GPT-5

尽量把 backbone ability 控住，只比较 scaffold。

## RQ2 固定 mini-SWE-agent

尽量把 agent interface 控住，只比较 LLM。

这比“拿各家最佳 Agent 直接比 Pass@1”有解释力得多。

但仍有几个问题。

## 18.1 Tool Affordance 本身是复合 Treatment

不同 Agent 可以用不同 search / navigation abstraction。

因此 RQ1 测到的是：

> interface + prompt + control policy + retrieval mechanism 的合成效果。

不能把差异归因到某个单独模块。

## 18.2 Final Context Declaration 是额外 Protocol

为了获得 Final Context，作者加入 pre-submission declaration。

这是 measurement 所需，但可能轻微改变系统原始行为。

## 18.3 Gold-relative Precision 对探索型 Agent 未必完全公平

真实 debugging 需要排除错误 hypothesis。

如果 Agent 查看一个最终证明“不需要”的文件，ContextBench 会降低它的 Precision。

这对“compact evidence retrieval”是合理的，但不能自动把这次 exploration 叫浪费。

所以更准确的 interpretation 是：

**Gold-relative evidence compactness**

而不是：

**所有 non-gold retrieval 都是坏行为。**

---

# 19. 这篇论文没有传统 Module Ablation，但有三类 Benchmark Validation

它不是一个带神经模块 A/B/C 的 method paper，因此没有典型的 “w/o module” ablation。

但如果把 ContextBench 看成 measurement instrument，它做了三类 validation。

## 19.1 Sufficiency Verification

给强模型 annotated Gold Context，看能否生成 test-passing patch。

验证：

> Gold Context 是否够用。

## 19.2 Compactness Principle

标注时要求尽量删 redundant / irrelevant region，并周期性 audit。

验证目标：

> Gold 不要膨胀成半个 repository。

不过这不是严格 deletion test，因此 compactness 仍主要依赖专家流程。

## 19.3 Alternative-Patch Robustness

RQ5 的 Jaccard 0.9518。

验证：

> Gold Context 是否会因为换一个等价 patch 就大幅变化。

三者分别对应：

~~~text
Sufficiency：够不够解题？
Compactness：是不是过宽？
Robustness：是不是绑定某个答案写法？
~~~

---

# 20. 作者最强的 Claim，哪些站得住？

## 20.1 “End-to-end benchmark 看不到 retrieval process”

站得住。

这是 measurement design 层面的直接事实。

## 20.2 “复杂 scaffold 不一定改善 context retrieval”

在本文配置下站得住。

Table 2 明确显示复杂系统没有在主要 context metric 上一致超过 mini-SWE-agent。

但不能推广成“复杂 Agent architecture 普遍无价值”。

## 20.3 “Frontier LLM 仍然 struggle with precise retrieval”

基本站得住。

Block-level F1 都低于 0.45，Line-level F1 都低于 0.35。

不过“多低才叫 struggle”仍带有评价色彩。

## 20.4 “模型整体更偏 Recall”

本文结果支持这个整体趋势。

但 Gemini 明显更 precision-oriented，所以不能理解成所有模型在所有粒度上 Recall 都高于 Precision。

## 20.5 “Balanced retrieval 导致更高成功率”

这句话需要降级。

Claude 的 balanced behavior 与更高 Line F1 / Pass@1 同时出现。

论文没有随机操纵 retrieval granularity，因此更准确是：

> balanced strategy 与更好 outcome **相关**。

不是因果。

## 20.6 “Usage Drop hinders resolution”

数据明确支持 Usage Drop 存在。

但 Usage Drop → Repair Failure 没有被 controlled intervention 识别，而且 Usage Drop 本身依赖 final declaration proxy。

因此这是有依据的机制解释，不是已证明的因果链。

---

# 21. 真正的 Limitation

## 21.1 Gold Context 不是数学意义上的最小必要集合

它是 expert-curated + compact + verified sufficient context。

因此 **non-gold ≠ useless**。

这是最重要的限制。

## 21.2 Ground Truth 是 Answer-Aware 构造

Annotator 从 Gold Patch 出发。

这适合构建 evaluation reference，但和真实开发者从 issue 开始、不知道答案的探索过程不同。

Gold Context 更像 hindsight evidence set。

## 21.3 Task Selection 改变了现实分布

作者主动富集高 context-demand task。

所以不能直接把 ContextBench 统计量当作自然 GitHub issue 分布。

## 21.4 Usage 只是 Proxy

Final declared context 不是模型内部真正使用 evidence 的直接观测。

## 21.5 Cross-Model 对比不是 Context 的因果实验

GPT-5 看得多、Pass@1 低于 Claude，并不证明 extra context 导致 GPT-5 失败。

## 21.6 Annotation 成本很高

平均约 40 分钟 / issue。

这限制了 benchmark 的快速扩展与持续维护。

---

# 22. 作者与团队背景

论文明确标注：

- Han Li：第一作者，南京大学。
- Zhaoyang Chu、He Ye：通讯作者，UCL。

公开项目属于 EuniAI 团队，其工作集中在 Coding Agent、SWE benchmark、repository context、agent runtime / environment 与 process evaluation。

这和 ContextBench 的问题意识是一致的：他们不只关心 leaderboard，而是关心 Agent 在真实仓库里怎样探索和解决任务。

作者背景在这里的意义不是“名气”，而是帮助理解这篇论文为什么会把 Pass@1 拆成 process-level signals。

---

# 23. 作者证明了什么？

1. **ContextBench 把 repository context retrieval 建成了一个可单独评价的中间能力。**  
   它提供 1,136 个任务和 file / block / line 三级 human-verified Gold Context。

2. **复杂 Agent scaffold 不保证更好的 Gold Context retrieval。**  
   固定 GPT-5 后，复杂系统没有在主要 retrieval metric 上稳定超过 mini-SWE-agent。

3. **Frontier LLM 仍存在显著 fine-grained retrieval 问题。**  
   四个模型的 block F1 < 0.45，line F1 < 0.35。

4. **模型 retrieval style 差异很大。**  
   GPT-5 少次大块，Devstral 多次小块，Claude 更居中；“Context 多少”不能只用总 token 表示。

5. **探索过程中找到 evidence，不代表最终 evidence 被保留下来。**  
   Usage Drop 揭示 acquisition 和 final consolidation 是不同阶段。

---

# 24. 作者没有证明什么？

1. **没有证明所有 non-gold context 都是噪声。**
2. **没有证明 extra context 因果地降低 repair performance。**
3. **没有证明 Claude 更好的 Pass@1 是由 balanced retrieval 导致。**
4. **没有证明 Usage Drop 等于模型内部真正丢失 causal evidence。**
5. **没有证明 Gold Context 是唯一、全局最小、逐行必要的 solution evidence。**
6. **没有证明复杂 Agent 整体无价值；只说明复杂 scaffold 没稳定转化成更好的 Gold-relative retrieval。**

---

# 25. 真正应该记住什么？

如果过几天导师突然问这篇论文，可以直接讲这六句：

1. **ContextBench 不是再做一个 repair leaderboard，而是给 Coding Agent 的 repository context acquisition 建 Gold Standard。**
2. **Gold Context 不是 patch file：作者从 patch 出发沿调用、继承、控制流和数据流追踪解题 evidence，再做 sufficiency verification。**
3. **它同时评价 file / definition block / line，能揭示“找到正确文件但在文件里看了大量额外代码”的问题。**
4. **它把 Model 和 Agent Scaffold 分开实验：固定 GPT-5 比 Agent，固定 mini-SWE-agent 比模型。**
5. **真正有新意的不只是 Recall / Precision，而是 trajectory dynamics 和 Usage Drop——找到 evidence 和最终保留 evidence 是两个阶段。**
6. **它仍然是 observational diagnosis，不是 context intervention，所以不能直接证明 plausible extra context 为什么伤害模型。**

---

# 26. 对我们当前研究的启发

到这里才应该把 ContextBench 接回我们自己的问题。

## 26.1 它提供了“现实 Agent 会自然获取 Gold 外 Context”的证据

ContextBench 的 Precision 普遍不高，说明正常 Agent 在正确 repository snapshot 上运行时，本来就会访问大量 compact Gold Context 之外的代码。

这比人为把旧 commit API 注入当前任务更贴近我们的现实性问题。

但必须保持边界：

**Gold 外 ≠ non-decisive。**

所以不能直接把 ContextBench 的 false-positive context 全部叫 plausible noise。

## 26.2 Outcome 不应该只剩 File F1

ContextBench 提醒我们把：

~~~text
Treatment → File F1
~~~

升级为：

~~~text
Context Treatment
      ↓
GT Evidence Acquisition
      ↓
Evidence Retention
      ↓
Attribution / Final Localization
      ↓
File / Patch Outcome
~~~

尤其可以测：

- GT evidence 是否出现；
- GT block 是否被保留；
- final explanation / localization 归因到哪个 node；
- 在 GT 已经存在的条件下，最终 attribution 是否被 plausible distractor 拉走。

## 26.3 我们真正可以补 ContextBench 没回答的因果问题

ContextBench 是自然行为观察：

> 模型 A 找了这些，模型 B 找了那些。

我们的实验如果要更进一步，应该固定：

- 同一个 task；
- 同一个 model；
- 同一个 prompt；
- 同一个 current repository snapshot；
- 同一个 sufficient evidence C*；
- 同一个 node / token budget；

只改变额外 context：

~~~text
C* only
C* + matched random
C* + structurally plausible but non-decisive
C* + semantically plausible but non-decisive
~~~

再看：

- Evidence Retention
- Attribution Shift
- False Localization
- Final F1

这才可能回答 ContextBench 没有识别的因果问题：

> **当正确 evidence 已经固定存在时，额外 plausible-but-non-decisive repository context 是否比 random context 更容易改变模型最终的 evidence weighting 与 attribution？**

即使最终 F1 没明显下降，只要 attribution / retention 发生系统性漂移，也仍然可能是有意义的机制发现。

## 26.4 ContextBench 也提醒我们不要把 non-GT 直接叫 distractor

我们的 plausible candidate 最好做额外 audit：

- Necessary
- Potentially useful
- Non-decisive
- Conflicting
- Unknown

真正 treatment 尽量使用有依据判断为 non-decisive 的 context。

否则审稿人完全可以质疑：

> 你所谓的 plausible noise，其实是另一条合理 solution path。

---

# 最后一句

**ContextBench 最重要的贡献，是把“Agent 最后有没有修对”打开成了一条可测的 evidence pipeline；我们真正可以继续往前补的，是用 controlled intervention 识别额外 repository context 如何改变 evidence retention 与 attribution。**

但顺序必须保持：先忠实承认 ContextBench 只观察 retrieval / retention，再把我们的 intervention 放到它没有识别的因果缺口上，而不是把它包装成已经证明 plausible context 有害。
