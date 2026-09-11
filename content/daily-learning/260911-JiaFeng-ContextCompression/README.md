# On the Effectiveness of Context Compression for Repository-Level Tasks: An Empirical Investigation

> 精读日期：2026-09-11  
> 作者：Jia Feng, Zhanyue Qin, Cuiyun Gao, Ruiqi Wang, Chaozheng Wang, Yingwei Ma, Xiaoyuan Xie  
> Venue：arXiv cs.SE, 2026（Work in progress）  
> arXiv：[2604.13725](https://arxiv.org/abs/2604.13725)

## 一句话价值

这篇论文系统研究 repository-level context 太长时，**“保留全部”是否真的最好**。作者比较 Text-to-Text、Text-to-Vector 和 Text-to-Image 三类压缩策略，发现连续 latent-vector 压缩在部分设置下不仅没有下降，反而比 Full Context 高出最高约 **28.3% BLEU**；另一方面，一些文本压缩条件甚至比 **No Context** 更差。对 repository context / call graph noise 研究来说，后一个现象尤其值得注意：它说明额外上下文可能不只是“没帮助”，还可能主动误导模型。

## 先建立论文地图

Repository-level code intelligence 与单文件任务最大的不同，是模型必须处理大量跨文件信息，例如 API definition、import、dependency、historical implementation、caller/callee 关系和类型/函数签名。这些信息当然可能有帮助，但也带来三个问题：

1. **Noise**：真正有用的信息可能被大量 repository boilerplate 淹没；
2. **Context window**：repository 太长时最终仍要 truncation；
3. **Cost**：context 越长，推理 latency、显存和 decoding cost 越高。

作者因此把问题从“怎样塞更多 context”改成：

> **能不能先把 repository context 压缩成更高信息密度的表示，再交给 LLM？**

整体流程是：

```text
Raw Repository Context
        ↓
Context Compressor
        ↓
┌────────────┬──────────────┬──────────────┐
│   T2T      │     T2V      │     T2I      │
│ shorter    │ latent       │ rendered     │
│ text       │ vectors      │ image        │
└────────────┴──────────────┴──────────────┘
        ↓
Downstream Code Model
        ↓
Completion / Generation
        ↓
Quality + Latency + GPU Memory
```

作者研究三个问题：

1. 三种压缩范式对任务性能的影响；
2. compression ratio 增加后性能如何变化；
3. latency 和资源占用能降低多少。

## 理解全文需要的四个概念

### 1. Full Context 不是严格意义上的性能上界

作者设置两个基础 baseline：

- **No Context / Plain**：只给任务描述，不给 repository context；
- **Full Context**：直接给未经压缩的 repository context。

传统直觉会把 Full Context 当成性能上界，但结果恰恰说明它只能算“未压缩基线”。多个 T2V setting 超过了 Full Context。

真正成立的条件应该是：

```text
更多信息
+
模型能够正确找到并利用 relevant evidence
→ 更好结果
```

缺少后半句时，多的信息也可能变成 distractor。

### 2. Compression Ratio 不等于 Information Loss Ratio

4× compression 大致意味着表示长度变成四分之一，但四分之一 token 并不等于只剩四分之一有效信息。如果优先删的是 boilerplate，有效信息可能保留很多；如果先删 import、identifier、函数签名，即使剩余 token 仍不少，任务真正需要的信息也可能已经没了。

### 3. 三种 Compression 的区别首先是表示空间

**T2T：Text → Text**  
代表方法包括 LLMLingua、LLMLingua-2、LongLLMLingua。优点是 model-agnostic、training-free，压缩后仍是人能阅读的代码文本。

**T2V：Text → Vector**  
把长 context 编码为少量连续 memory vectors。模型不是看到“删短后的代码”，而是看到 learned latent memory。

**T2I：Text → Image**  
将代码渲染成图片，再通过视觉语言模型读取，希望利用 visual token 的高信息密度。

### 4. Compression 与 Denoising 不是同一个 claim

假设 Full Context 是 32 分，而 Compressed Context 是 41 分，可以确定的是：

> 当前 compressed condition 表现更好。

但不能立即推出：

> “删除 noise 导致了 +9。”

至少还有三种解释：

```text
真正删除了无关噪声 ─────→ Performance ↑
压缩器学到了任务先验 ───→ Performance ↑
输入 representation 改变 ─→ Performance ↑
```

这一区分是读整篇论文最重要的一步。

## Research Gap：为什么 NLP Compression 到代码上可能失效

自然语言压缩常利用 token 的 predictability / perplexity：越容易预测的 token，越可能被认为信息增量较小。

但代码很特殊。例如：

```python
from some_module import ImportantAPI
```

这一行模式非常常见，语言模型可能很容易预测；但 `ImportantAPI` 恰好可能决定另一个文件能否正确调用接口。

Python 缩进更极端：

```python
if condition:
    do_something()
```

空格几乎没有 lexical information，却决定 `do_something()` 属于哪个 scope。

所以代码里出现一个关键不等式：

> **Low linguistic information ≠ Low program importance**

这也是为什么 NLP context compression 不能直接照搬到 repository code。

## T2I：为什么 Completion 还能用，Generation 却明显掉

T2I 的流程是：

```text
Source Code
↓
Rasterize
↓
缩小图片
↓
切成 patches
↓
Qwen2.5-VL
↓
Code output
```

它最大的特点是**没有 information selection**：一行注释、一段 boilerplate、一个关键 function signature、一个 import statement 得到近似同样的视觉空间，所以本质上是一种 non-selective information loss。

Python completion 的一个例子：

- Full Context BLEU：**24.91**
- T2I 4×：**24.11**

差距很小。

但 Python generation：

- Full Context：**9.19**
- T2I：**4.52**

几乎腰斩。

一种合理解释是：Completion 更依赖目标位置附近的 variable、indentation 和 syntactic pattern；Generation 更依赖 function signature、API relation、import 和 cross-file dependency，而这些细粒度符号在图片缩放后更容易损失。

注意证据层级：论文观察到了 performance difference；“因为丢失 cross-file structure”是基于表示机制和 recovery 实验给出的合理解释，不是独立操纵 cross-file structure 后得到的因果结论。

## T2V：为什么它会超过 Full Context

T2V 不是直接删代码，而是先把代码分 segment，再压成少量 memory tokens。

作者设计两个维度。

### Memory Organization

**SLMC**：每个 segment 独立处理，可并行，但 segment 之间没有持续 memory。

**CPMC**：上一段 memory 继续传给下一段，希望显式保存跨 segment 信息。

### Memory Extraction

**SAMA**：Memory token 与代码表示通过 self-attention 交互。

**QDME**：设置 learnable query，让少量 memory query 主动从代码中“提取值得记住的信息”。

形成四种组合：

- SAMA-SLMC；
- SAMA-CPMC；
- QDME-SLMC；
- QDME-CPMC。

## 一个非常重要但容易漏掉的事实：T2V 是训练过的

T2V 有两阶段训练：

1. recovery-oriented pretraining；
2. downstream task adaptation。

第二阶段使用 **ComplexCodeEval 的 10k+ training split**。测试的 200 个实例没有进入训练集，因此不是直接 data leakage；但它造成了一个关键公平性问题：

```text
Full Context
=
Base Qwen2.5-Coder
+ raw repository context
```

而：

```text
T2V
=
Base Qwen2.5-Coder
+ task-adapted learned compressor
+ compressed context
```

所以 Treatment 实际捆绑了：

```text
compression
+
learned representation
+
task-specific adaptation
```

因此后面看到 T2V > Full Context 时，不能只解释为“repository noise 被删除，所以模型变好了”。“去噪”目前更多是机制假设，而不是已经被单独识别的 causal effect。

## 实验设计

### Dataset

作者使用 **ComplexCodeEval**，包含两类任务：

- Code Completion：给部分代码，预测缺失部分；
- Code Generation：根据 function signature、docstring 和 repository context 生成完整 function body。

### 样本

作者随机抽取：

- Python：100；
- Java：100；

总计 **200 个 evaluation instances**。

T2V 另使用 10k+ ComplexCodeEval training split 做压缩器任务适配。

### Models

T2V / T2T：

- Qwen2.5-Coder-3B；
- Qwen2.5-Coder-7B。

T2I：

- Qwen2.5-VL-3B；
- Qwen2.5-VL-7B。

### Metrics

Completion：BLEU、Edit Similarity、Exact Match。  
Generation：BLEU、Edit Similarity。  
效率：compression latency、decoding latency、total latency、peak GPU memory。

## 一个明显的 Baseline Fairness 问题

作者希望 Instruction 保持一致，让 observed difference 主要来自 compression operator，但严格来说并不成立。

```text
T2I
→ Qwen2.5-VL
```

而：

```text
T2V / T2T
→ Qwen2.5-Coder
```

所以跨范式比较同时改变了 compression paradigm、downstream model 和 modality。

因此，`T2V > T2I` 不能解释成纯粹的“Vector representation 因果优于 Image representation”。更可靠的比较是每种范式内部相对 Full Context / Plain 的变化。

## RQ1：不同 Compression Paradigm 谁表现最好？

最醒目的数字出现在 Qwen2.5-Coder-7B 的 Python completion：

| Condition | BLEU |
|---|---:|
| Full Context | 32.21 |
| T2V SAMA-SLMC | **41.34** |
| T2V QDME-SLMC | 40.03 |

41.34 相比 32.21 高约 **28.3%**。

Generation 也有类似现象：QC-7B Python generation 中，Full Context 为 **10.49**，QDME-SLMC 为 **13.58**。

但 Java completion 并非所有 T2V 都更好：Full Context 32.60，SAMA-SLMC 28.87，QDME-SLMC 33.44，QDME-CPMC 35.12。

所以正确结论不是“T2V 一定优于 Full Context”，而是：

> **多个配置出现 supra-context performance，但效果高度依赖 compressor 和 programming language。**

### 真正与你研究最像的现象：有 Context 比 No Context 更差

QC-3B Python completion：

- No Context：**27.59 BLEU**
- LLMLingua：**25.69**
- LongLLMLingua：**25.78**

这比“低于 Full Context”更重要。

如果只是 Compressed Context < Full Context，可以解释为有用信息丢失；但现在出现：

```text
Compressed Context < No Context
```

意味着这些剩余上下文至少在当前模型条件下**不是单纯没帮助，而是在把模型往错误方向推**。

这正是 retrieval distraction、context noise、misleading context 最干净的一类 operational phenomenon。

### 为什么 Python 特别容易被 T2T 伤害

T2T 方法倾向删除 low-perplexity tokens，而 Python 的 indentation、scope markers、regular imports 往往非常 predictable。压缩器可能认为它们“不重要”，但程序语义却认为它们是结构。

Java 有明确 `{}`，对部分 token deletion 更 robust。

这说明：

> **NLP relevance metric 的 construct validity 到 Code 上必须重新验证。**

这与 Call Graph 实验高度相似：graph distance 小，并不自动意味着 review relevance 高。

### RQ1 Takeaway

Context 是否有用，不能简单用长度定义。更准确的链路是：

```text
Context
↓
是否保住 Task-Relevant Structure？
↓
模型是否能正确利用？
↓
Performance
```

Repository context 是 treatment carrier，不是 effect 本身。

## RQ2：Compression Ratio 越高会发生什么？

### T2V：几乎是一条平线

作者从 **4× → 128×** 持续增加压缩倍率，但 T2V 的表现意外稳定。

Python completion，QDME-SLMC：

**62.49%–63.94% Edit Similarity**，而 Full Context 为 **60.19%**。

Python generation，SAMA-SLMC：

**32.40%–33.27%**，Full Context 为 **28.75%**。

传统直觉应该是：

```text
压得更多
↓
丢得更多
↓
效果下降
```

这里并没有明显出现。作者解释 latent bottleneck 不是机械删除，而是在固定 memory capacity 下学习 task-relevant representation。

但因为 compressor 经过额外训练，目前还无法判断究竟是去噪、representation learning 还是 downstream adaptation 谁贡献最大。

### T2I：出现“甜点区”

Completion 在 4× 左右最好，继续降低分辨率会变差；Generation 在所有 compression ratio 上基本都低于 Full Context。

一种合理解释是：uniform visual rendering 没有能力选择性保护 cross-file relational structure。

### T2T：存在明显 Performance Cliff

Generation 中出现明显临界点：

- LLMLingua：约 **12×** 时已接近 No Context；
- LLMLingua-2：约 **8.1×** 已低于 Plain；
- LongLLMLingua：约 **7×** 跨过 No Context。

所以 nominal compression ratio 并不能反映 retained useful information。

### 对 Call Graph Depth 实验的直接启发

不要只做：

```text
No CG
vs
CG
```

更有解释力的是：

```text
0-hop
↓
caller only
↓
callee only
↓
1-hop
↓
2-hop
↓
3-hop
↓
Full Graph
```

画 `Context Dose → Performance` 曲线。

可能出现：

- 单调正向；
- 倒 U；
- Threshold Cliff；
- 强异质性：Need-CG group 向上、No-Need-CG group 向下。

最后一种尤其值得研究，因为平均 ATE 很可能把两个相反群体冲掉。

## RQ3：Context Compression 到底省多少？

T2I latency 一个代表性结果：

| Condition | Total latency |
|---|---:|
| Plain | 4.17 s |
| Full Context | 8.95 s |
| T2I 4× | 6.02 s |
| T2I 128× | 4.48 s |

4× 已比 Full Context 少约 **33%**。

T2V 中，Full Context 约 **9.13 s**；SAMA-SLMC 从 4× 的 **6.51 s** 降到 128× 的 **5.71 s**，压缩模块本身只增加约 0.2 s。

T2T 在高压缩比下 latency 也会接近 No Context，但问题是**Performance 往往比 latency 更早崩**。

所以真正应该看的不是单独 cost，而是 quality–cost frontier。

## Figure 4：作者真正去看“删掉了什么”

Figure 4 展示 LLMLingua 压缩 Java source file。低倍率主要删除 whitespace 等边缘内容；倍率升高后，import statements 和 intermediate assignments 开始消失。

这给出了一条很重要的 mechanism evidence：

> import 很 predictable，所以 perplexity 很低；但它恰恰编码 cross-file dependency。

这比只看 benchmark score 更接近“为什么会掉”。

## Table 5：T2V 究竟保留了多少原始信息？

4× compression：

| Method | BLEU | ES |
|---|---:|---:|
| T2V | **84.12** | **91.57** |
| T2I | 22.80 | 46.38 |

128×：

| Method | BLEU | ES |
|---|---:|---:|
| T2V | 16.51 | 41.09 |
| T2I | 0.18 | 7.45 |

T2V 显然能恢复更多原始 text information。

但要注意：

> **Text Recovery Fidelity ≠ Task-Relevant Information。**

如果重建了 100 行 boilerplate、丢了 1 行关键 API，BLEU 仍可能不错，但任务仍会失败。

## 主动审查：这篇论文最大的五个问题

### 1. T2V 的“去噪”Claim 被额外训练混杂

这是最大的问题。

论文 narrative 是：

```text
Full Context
↓
包含 Noise

T2V
↓
过滤 Noise

所以 Performance ↑
```

但实验实际是：

```text
Full Context
=
Base Model
```

而：

```text
T2V
=
Base Model
+
Pretrained Compressor
+
Task-Adapted Compressor
```

因此 Treatment bundle 至少包含 Compression Representation + Additional Training。

更严格的实验至少应加：

- 给 Full Context 一侧相同训练预算的 adapter；
- Random bottleneck；
- Structure-aware deterministic compression；
- Oracle Relevant Context。

这样才能逐步判断 latent compression 的优势到底来自哪里。

### 2. Compression Paradigm 与 Model Architecture 被捆绑

T2I 用 Qwen2.5-VL，而 T2V/T2T 用 Qwen2.5-Coder。跨范式差异同时混入 downstream model 和 modality，因此不能做纯因果解释。

### 3. Dataset 只有一个，Evaluation 只有 200 个实例

Python 100 + Java 100。作为探索研究可以接受，但 repository context 的价值高度依赖 benchmark construction。ComplexCodeEval 如果天然 context redundancy 高、retrieved context 宽、relevant evidence 稀疏，压缩就更容易显出优势；换到 AACRBench、SWE-bench、RepoPairBench 或真实 Code Review，分布可能完全不同。

### 4. BLEU 上升不代表 Functional Correctness 上升

论文最醒目的 +28.3% 指的是 BLEU，不是 Pass@1 或 test pass rate。代码 lexical similarity 与 executable correctness 并不等价，因此不能把“BLEU +28.3%”写成“代码正确率提升 28.3%”。

### 5. “Noise”没有被真正测量

论文反复用 noise、redundant context、task-relevant signal 解释结果，但没有直接测量：

- Relevant Evidence Recall；
- Irrelevant Token Ratio；
- Distractor Count；
- Misleading Evidence；
- Evidence Position；
- Attention Allocation。

因此现有证据是：

```text
Compression
↓
Performance ↑
```

然后推测：

```text
可能是 Noise ↓
```

而不是已经证明：

```text
Compression
↓
Noise ↓
↓
Performance ↑
```

这正是后续因果研究可以继续推进的地方。

## 对 Causality for Code Review 的直接启发

### 1. 把 Context Treatment 拆开，而不是只做 Diff vs Diff+CG

建议至少考虑：

```text
T0: Diff only
T1: Diff + Relevant Call-Graph Context
T2: Diff + Irrelevant-but-Benign Context
T3: Diff + Misleading Context
T4: Diff + Relevant + Irrelevant Mixed Context
```

这五组回答的是不同机制问题。

### 2. Relevant Context 不能只让 Retriever 自己定义

如果“Retriever 认为相关”就被当作 relevant，再研究 relevant context 是否有帮助，会形成循环定义。AACRBench 已有 diff / in-file / repository-level 的 expert context-need 标签，可以作为相对独立的 contextual requirement signal。

### 3. 把 Context Noise 做成 Mediator

```text
Context Treatment
        ↓
┌───────────────────────────────┐
│ Relevant Evidence Coverage    │
│ Irrelevant Token Ratio        │
│ Misleading Evidence Rate      │
│ Search / Attention Allocation │
└───────────────────────────────┘
        ↓
Review Quality
```

这样问题不再只是“CG 为什么平均掉 2%”，而是可以问：CG 是否增加 irrelevant evidence exposure，而这一变化是否进一步导致 false positives 或 defect recall 变化。

### 4. ContextNeed 应作为 Effect Modifier

真正的问题可能不是：

\[
ATE(CG)
\]

而是：

\[
CATE(CG \mid ContextNeed)
\]

即 Call Graph 对真正需要跨文件 reasoning 的 instance 有什么 effect，对不需要 CG 的 instance 又有什么 effect。

如果：

```text
Need-CG group → positive effect
No-Need-CG group → negative effect
```

聚合以后完全可能得到 `ATE ≈ 0`，于是平均分会掩盖真正机制。

### 5. 一定保留 No Context / Minimal Context Baseline

如果只有 Full Context vs Compressed Context，当 compressed 更差时只能说它丢失了有用信息。

但如果：

```text
Context condition < No Context
```

就意味着 context **主动改变了模型行为并产生负贡献**，这给 distraction、anchoring、misleading evidence 提供更强的现象证据。

## 作者证明了什么

1. 在 ComplexCodeEval + Qwen2.5 的当前设置下，**Full Context 并非始终最优**。
2. T2V 在多个配置中超过 Full Context，而且 4×–128× 范围表现 surprisingly stable。
3. Perplexity-based T2T pruning 会破坏 code-specific structure，Python 尤其敏感。
4. Context representation 对 completion 与 generation 的影响明显不同。
5. Compression 可以显著降低 latency 与 GPU memory。

## 作者没有证明什么

1. 没有证明 More Repository Context 本身 causally hurts performance。
2. 没有证明 T2V 超过 Full Context 的原因一定是 denoising。
3. 没有隔离 task-specific compressor training 的贡献。
4. 没有证明结果能迁移到真实 Coding Agent 或 Code Review。
5. 没有证明 BLEU 提高意味着 executable correctness 提高。
6. 没有直接测量 noise / relevance / misleadingness 这些所谓机制变量。

## 真正应该记住什么

- **Full Context 不是天然性能上界。**
- **Program relevance 与语言模型 token importance 不是一回事。**
- T2V 的 supra-context 结果很有意思，但“denoising 导致提升”尚未被严格识别。
- **Context < No Context** 是研究 misleading/noisy context 最值得关注的信号。
- Completion → Generation → Code Review 不能直接外推，因为它们依赖的结构信息不同。
- 对 repository context / call graph 研究，最值得推进的是把 **Relevance、Noise、Misleadingness、Context Need** 从 Discussion 中的解释词，升级成真正的 **Treatment、Mediator 和 Effect Modifier**。
