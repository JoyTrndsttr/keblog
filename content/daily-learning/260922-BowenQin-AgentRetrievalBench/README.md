# Agent Retrieval Bench：Evaluating Repository Context Retrieval for Coding Agents

> 精读日期：2026-09-22  
> 简称：ARB / Agent Retrieval Bench  
> arXiv：2607.24882  
> 作者：Bowen Qin; Yi Xie  
> 主题：Repository Context Retrieval、Coding Agent、Context Acquisition、Trajectory、Evidence Localization

## 一句话结论

ARB 真正研究的不是“哪个 retriever 排名最高”，而是把 Coding Agent 完整工作流最前面的 **Repository Context Acquisition** 单独拆出来测：**Agent 在进入 reasoning / editing 之前，能否先找到真正需要的仓库证据？** 作者先把这一抽象问题 operationalize 成四类真实 workflow context-need，再比较不同 retrieval inductive bias，并进一步用 seed intervention 验证初始 context 是否会改变后续 Agent trajectory、证据命中与成本。

## 1. 先看整篇论文的顶层设计

传统 Coding Agent benchmark 通常只看最终 patch 是否成功：

```
Issue / Review / Failure Signal
        ↓
Repository Exploration
        ↓
找到相关代码
        ↓
Reasoning
        ↓
Editing
        ↓
Validation
        ↓
Patch Success
```

问题是：如果最终失败，我们并不知道失败发生在哪一层。

可能是：

- 一开始就没找到关键文件；
- 找到了文件，但没找到真正 evidence span；
- evidence 已经到场，但模型不会利用；
- reasoning 对了，但 edit 错了；
- patch 基本正确，但 validation/环境失败。

ARB 的 Research Gap 就是：

> **现有端到端 benchmark 把 context acquisition failure 与后续 reasoning/editing failure 混在最终 outcome 里，缺少一个专门测“仓库证据是否被正确找到”的 evaluation layer。**

所以它把完整 Agent pipeline 拆成：

```
Issue / Workflow Signal
        ↓
[ Repository Context Acquisition ]   ← ARB 专门研究这一层
        ↓
Reasoning
        ↓
Editing
        ↓
Patch / Task Outcome
```

这就是整篇论文真正的研究对象。

后面出现的四类 task、retriever、BCY、line-level evidence、interactive agent 和 seed intervention，都服务于同一个顶层问题：

> **什么样的 context need，应该由什么样的 retrieval mechanism 处理；retrieved context 是否真的改变 Agent 后续行为？**

---

## 2. 作者如何把“Context Acquisition”变成可测的 Benchmark

“找 repository context”本身太抽象，因此作者必须先回答：

> **Agent 在真实软件工程 workflow 中，到底为什么要搜索仓库？**

不同阶段，Agent 手里拥有的 query signal 不一样：

- 有时知道某段 implementation 改了，要找相关 test；
- 有时拿到 code review comment，要找理解该 comment 所需的其他文件；
- 有时只有 failure command / stack trace，要找 root-cause implementation；
- 有时已经知道一个 edit，要找 ripple effect。

因此作者把 Repository Context Acquisition operationalize 成四类 workflow task：

```
Repository Context Acquisition
            │
     Agent 为什么要搜仓库？
            │
 ┌──────────┼────────────┬───────────┐
 ↓          ↓            ↓           ↓
code2test   comment2context   trace2code   edit2ripple
```

这四类 task 不是随意罗列出来的 benchmark 子任务，而是四种典型的 **workflow state → needed repository evidence** 映射。

### code2test

已知 implementation change，目标是找相关测试。

这里的 relevance 往往来自：

```
implementation
   ↓
test convention / dependency / structure
   ↓
relevant tests
```

不一定靠文本语义相似度。

### comment2context

已知 review comment 和被评论文件，目标是找理解或处理该评论需要的额外文件。

这里 reviewed file 已经是 given context，所以 gold 不是“评论发生在哪个文件”，而是：

> **还缺哪些 repository evidence？**

这与 repository-level code review 特别接近。

### trace2code

给 failure command / failure excerpt，目标是找真正的 root-cause implementation。

stack trace 显式出现的 test/file 可能只是 symptom evidence：

```
Failure Trace
   ↓
stack frame / test
   ↓
dependency / call relation
   ↓
root-cause implementation
```

因此这是最能暴露“semantic similarity 不等于 task utility”的任务。

### edit2ripple

已知一个 anchor edit，目标是找其他受影响 source/test file。

本质上是：

> **从局部修改推断 repository-wide dependency consequences。**

所以四类 task 的作用，是把一个抽象的“repository retrieval”问题拆成不同 workflow 下不同类型的 context need。

---

## 3. 四类 Task 之后，论文真正研究的核心变量是什么？

一旦定义了四类 context need，下一步自然变成：

> **什么叫“relevant repository context”？**

作者的核心判断是：repository relevance 不只是 semantic similarity。

一个文件可能因为以下原因有用：

- **semantic-direct**：内容直接和 query 语义相关；
- **structural-indirect**：通过调用、依赖、项目结构间接相关；
- **workflow-conventional**：通过测试命名、目录约定、开发流程相关；
- **causal-indirect**：query 表面指向 symptom，但真正需要的是根因实现。

所以不同 retrieval 方法实际上代表不同 **inductive bias**：

```
Lexical Retriever
→ 偏关键词/表面匹配

Embedding Retriever
→ 偏语义相似

RepoMap / Structural Retriever
→ 偏 repository relation

Hybrid / RRF
→ 尝试融合多种相关性
```

因此论文比较 retriever，不只是想做 leaderboard，而是在问：

> **不同 workflow context need 是否需要不同的 retrieval inductive bias？**

这也是为什么 trace2code 很关键：它最容易出现“query 里提到的是测试/trace，但真正答案是另一个 implementation file”的情况。

---

## 4. 为什么普通 Recall@k 还不够？

到这里作者已经能测：

> Retriever 有没有把 gold file 排到前面。

但 Coding Agent 真正接收的不是“Top-20 文件名列表”，而是受 token budget 限制的代码内容。

所以作者继续指出第二个 gap：

> **File ranking quality 不等于 model-facing evidence exposure。**

例如：

```
Top-5 小文件
```

和：

```
Top-5 巨型文件
```

即使 Recall@5 一样，真正塞进 8k/16k context window 的 evidence 可能完全不同。

因此他们引入 **Budgeted Context Yield（BCY）**。

BCY 的顶层意义是：

```
Repository Retrieval Quality
        │
        ├─ Ranking quality
        │    ├─ Recall@k
        │    └─ MRR
        │
        └─ Model-facing context exposure
             └─ BCY under token budget
```

也就是说：

- Recall / MRR：正确文件排得靠不靠前；
- BCY：在真实 token budget 下，真正有多少 gold context 能进入模型。

所以 BCY 不是一个孤立的新 metric，而是为了把 retrieval evaluation 从“IR ranking”推进到“LLM context exposure”。

需要注意：BCY 仍不是“充分 evidence 已经进入 prompt”的完美测量，因为只要 gold file 有部分内容进入 budget，就可能得到 exposure credit。

---

## 5. 为什么作者还要做 Span / Line-Level Evidence？

因为即使正确文件进入 prompt，文件内部真正有用的代码可能只占很小一部分。

在带 span annotation 的样本中，gold evidence 中位只占所在文件约 4.7%；很多 gold file 里真正 evidence 不超过文件内容的 10%。

所以：

```
File Hit
   ≠
Evidence Hit
```

进一步可以拆成：

```
找到正确文件
    ↓
真正相关 span 是否进入 context
    ↓
模型是否注意并利用
    ↓
任务是否成功
```

这一步把论文从“文件级 retrieval benchmark”推进成了“evidence acquisition benchmark”。

对当前 VLocBench 的启发也非常直接：official file-level GT 很可能不足以判断模型有没有拿到真正漏洞机制证据，因此 patch/function/span-level evidence annotation 是有价值的。

---

## 6. 离线 Retrieval 实验到底在回答什么？

前面的 benchmark construction 完成后，作者先做 offline retrieval comparison。

真正的问题不是：

> 谁是全局最强 retriever？

而是：

> **不同 workflow context need 下，哪种 inductive bias 更合适？**

结果说明没有一个方法通吃所有任务。

例如 trace2code 更依赖从 failure symptom 跳到真正 implementation，结构化方法表现相对更强；某些 task 下 embedding 又更有优势。

所以核心结论是：

> **Repository retrieval 的最优策略具有 task heterogeneity。**

这和论文前面对四类 task 的设计是直接对应的：

```
Workflow type
    ↓
Relevant relation type
    ↓
Retriever inductive bias
    ↓
Retrieval quality
```

而不是“四个 task 分别跑一遍排行榜”。

---

## 7. 到这里还只是 Offline Retrieval：和真实 Coding Agent 有关系吗？

这是论文第二个宏观问题。

即使某种 retriever：

- Recall 更高；
- MRR 更高；
- BCY 更高；

也不能自动推出：

> Agent 最后会更好。

因为 Agent 拿到 initial context 后还会自己继续搜索 repository。

所以作者必须回答：

> **更好的 initial retrieval 是否真的会改变 Agent 的后续 exploration？**

这就是 Seed Intervention 存在的原因。

它不是附加实验，而是连接：

```
Offline Retrieval Benchmark
        ↓
Actual Coding Agent Behavior
```

的桥。

---

## 8. Seed Intervention：整篇论文最接近因果干预的部分

作者固定：

- Agent；
- tool set；
- Docker environment；
- task；
- 后续搜索 budget；
- tool-call / model-turn 限制。

只改变 initial context seed：

- No seed；
- Random non-gold；
- Lexical；
- embedding-based retrieval；
- hybrid retrieval；
- Oracle。

因此 treatment 可以写成：

```
T = Initial Repository Context
```

然后观察：

```
Initial Context
      ↓
First Evidence Hit
      ↓
Further Search / Read
      ↓
Tool Calls / Read Tokens
      ↓
Final Localization
```

这一步特别重要，因为它开始研究：

> **context 如何改变 Agent trajectory。**

---

## 9. Seed Intervention 真正揭示的不是“Retrieval 提升 F1”这么简单

最值得注意的是 Random non-gold context。

它并不是一个完全 inert 的 placebo。

Random context 即使不包含 gold，也可能让 Agent：

- 多搜更多文件；
- 触发不同 search path；
- 花更多 read tokens；
- 最终偶尔碰到 gold。

因此：

> **Random context 本身就是 active treatment。**

这意味着在 context intervention 研究里：

```
No Context
```

与

```
Random Non-relevant Context
```

必须分开。

它们测的不是同一个东西。

对当前实验来说：

- no-expansion / no-extra-context 才是“无额外干预”；
- random-noise 是“加入非相关 context”；
- plausible-noise 是“加入语义上看似合理但非决定性的 context”。

这个区分比把 random-noise 当 placebo 更严格。

---

## 10. 这篇论文最终提出的机制链

把 benchmark 与 agent experiment 合起来，ARB 实际上构造的是：

```
Workflow Signal
      ↓
Repository Context Need
      ↓
Retrieval Strategy
      ↓
Evidence Exposure
      ↓
Agent Exploration
      ↓
Evidence Acquisition
      ↓
Final Localization
```

这就是整篇论文的顶层方法论贡献。

所以它不是单纯：

> 建一个 retrieval benchmark + 比几个 retriever。

而是：

> **把 Coding Agent 中原本埋在最终成功率里的 Context Acquisition 单独建模、测量，并验证 initial context 会改变后续 agent trajectory。**

---

## 11. Selective Retrieval 为什么又出现？

在前面已经建立“不是所有 context 都值得 retrieve”之后，作者进一步问：

> 如果 repository 里本来就没有答案，能不能检测出来然后不检索？

他们加入两类 no-gold：

1. natural no-gold；
2. wrong-repository counterfactual。

结果出现一个重要反例：

如果把明显 wrong-repository 的 easy control 算进去，selective retrieval 看起来有收益；

但去掉这些明显 mismatch，只保留真正困难的 natural no-gold case 后，优势明显减弱。

因此这里真正说明的是：

```
Detect obvious repository mismatch
        ≠
Detect absence of local evidence
```

这对 benchmark design 很重要：如果 negative control 太容易，可能会人为抬高 calibration / selective retrieval 的效果。

---

## 12. 与当前 VLocBench 研究如何一一对应

ARB 最有价值的地方，是给当前 VLocBench 的 context intervention 补上了一层 process measurement。

目前你的设计主要是：

```
Context Treatment
      ↓
Final File F1
```

但 ARB 提醒我们，中间至少还有：

```
Context Treatment
      ↓
Evidence Exposure
      ↓
Evidence Acquisition
      ↓
Agent Exploration / Re-read
      ↓
Evidence Utilization
      ↓
Mechanism Judgment
      ↓
File Reporting
      ↓
Official F1
```

因此下一轮实验，不应只记录最终 F1。

建议同时记录：

- first patch/mechanism evidence hit；
- 是否访问 patch-associated / GT file；
- search/read 次数；
- post-seed read tokens；
- mechanism-level hit；
- 最终 file-level output。

这样才能区分：

> context 是真的让模型“理解错了”，

还是：

> context 只是改变了它搜索和报告 evidence 的路径。

---

## 13. 对 patch-aware sibling disturbance 的直接启发

当前 `disturb@1/@2` 已经从 hop depth 改成“每条合格 semantic transition 添加多少 sibling”。

ARB 进一步提示：仅操纵 sibling 数还不够。

可以给每个 sibling 增加 role annotation，例如：

- semantic-direct-like；
- structural-indirect；
- path-support；
- plausible-but-non-decisive。

然后固定：

- sibling count；
- tokenizer-aware token budget；
- model；
- prompt；
- initial seed。

只改变：

> **context role composition**

这样就能研究：

```
Same amount of context
        +
Different evidence role
        ↓
Different exploration trajectory?
        ↓
Different mechanism hit?
        ↓
Different final localization?
```

这个比继续增加 `disturb@3/@4` 更接近机制研究。

---

## 14. 论文证明了什么

ARB 比较有力地证明了三件事。

第一，Repository Context Acquisition 可以作为 Coding Agent pipeline 中一个独立 failure surface 被评测。

第二，不同 workflow context need 对 retrieval inductive bias 的需求明显不同，不能默认 semantic similarity 是统一 relevance definition。

第三，initial repository context 会改变后续 Agent exploration、evidence hit 与成本，因此 context 不只是静态 prompt 内容，也是 trajectory intervention。

---

## 15. 论文没有证明什么

它没有证明：

> retrieval 更好一定导致最终 patch success 更高。

它没有证明：

> File F1 可以替代 mechanism/span-level evidence acquisition。

它也没有证明：

> semantic-direct / structural-indirect 等关系本身是因果机制。

Seed intervention 每个 sample × arm 只有一次 trajectory，policy sampling variance 没有通过 repeated runs 系统消除，因此更适合作为 descriptive mechanism evidence，而不是稳定识别后的 causal effect。

---

## 16. 真正应该记住什么

ARB 的核心不是“四类 task”“BCY”或“某个 retriever 最强”。

真正应该记住的是这条研究链：

```
Final Agent Failure
      ↓ 拆解
Context Acquisition Failure
      ↓ operationalize
Four Workflow Context Needs
      ↓
Different Relevance Relations
      ↓
Different Retrieval Inductive Bias
      ↓
Evidence Exposure under Token Budget
      ↓
Agent Exploration
      ↓
Final Localization
```

它最值得当前研究借鉴的思想是：

> **不要把 repository context 当成一个静态输入变量；它首先决定模型能看到什么 evidence，其次还会改变 Agent 接下来如何探索仓库。**

因此下一阶段更值得问的是：

> **同样预算下，不同 repository context composition 如何改变 evidence acquisition 与 exploration trajectory，并最终影响 vulnerability localization？**
