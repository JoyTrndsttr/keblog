# PhantomCall：如何在不改变恶意行为的情况下，主动扰动 Function Call Graph？

> **论文**：Md Ajwad Akil, Adrian Shuai Li, Imtiaz Karim, Arun Iyengar, Ashish Kundu, Elisa Bertino. *PhantomCall: Evading ML Malware Detectors via Function Call Graph Perturbation*  
> **版本**：arXiv:2609.00705v1 [cs.CR], 2026-09-01  
> **原文**：[arXiv:2609.00705](https://arxiv.org/abs/2609.00705)  
> **阅读依据**：完整 PDF 原文  
> **代码状态**：论文写明实验代码与 dataset hashes “will be released soon”；本次未把尚未公开的代码仓库当作可用复现资源。

## 一句话先记住

PhantomCall 的直接目标是攻击 Windows PE 恶意软件检测器：它把原来的直接调用改道到 trampoline，**先照常执行原始 callee，再额外调用一批可执行但语义惰性的 dummy functions，最后回到原控制流**，于是程序恶意行为尽量保持不变，而 FCG 的节点和边被主动改变。最关键的消融是：对纯 FCG 的 SAFE+GNN，去掉 FCG 注入后 ASR 从 97.4%/85.0% 几乎塌到 0.9%/0.1%，说明模型确实高度依赖可被结构扰动的图表示。

对当前 VLocBench 主线，它的价值不是“拿攻击代码直接改 call graph”，而是提供一个很清楚的实验设计范式：**固定任务语义，显式操纵图结构的 dose / topology / location，再检查 Outcome 是否变化。** 但 PhantomCall 改的是“真实可执行程序的 FCG”，而当前研究第一阶段要改的是“最终 localizer 能看到的 graph context”；这两个 Treatment 必须分开。

## 作者与团队背景

第一作者 **Md Ajwad Akil** 是 Purdue Computer Science 的研究生。就公开学术轨迹看，他目前还不适合被描述成已经形成独立学术地位的安全或软件工程学者；这篇论文更应该从团队背景理解。

末位作者 **Elisa Bertino** 是 Purdue Computer Science 的 Samuel D. Conte Distinguished Professor，也是长期的信息安全与数据库安全学者，研究覆盖 access control、data security/privacy、软件与网络安全以及 AI for cybersecurity，并长期参与 CERIAS / Cyberspace Security Lab。论文没有在首页明确标出“通讯作者”，因此这里不把末位作者自动称为通讯作者。

团队构成也说明这篇工作的学术位置：Purdue、UT Dallas、Cisco Research 与安全研究者合作，主线属于 **adversarial malware / ML security / program binary analysis**，而不是传统 ICSE/FSE repository-level SE。对我们的意义主要来自“语义保持结构干预”方法，而不是领域任务本身。

## 1. 论文到底在解决什么？

ML malware detector 不只看原始 bytes。有些模型会把 binary 恢复成 CFG / FCG，再用 GNN 学结构表示。如果模型把某种 FCG 拓扑当成恶意性证据，就产生一个问题：

> 能不能保持 malware 原来的执行行为，却改变它的 FCG，让 detector 的判断翻转？

已有 Windows PE 攻击更多改 raw bytes、PE header 或 function 内部 CFG。作者认为 Windows PE 上“真正加入可执行、可到达的新函数，从而改变 FCG”的 problem-space attack 还没有被系统研究。

因此目标可写成：

```text
原 malware m
   │
   ├── 保留原 malicious behavior
   │
   └── 施加 semantics-preserving transformation Φσ
             ↓
        adversarial m*
             ↓
     P(m*) < classifier threshold
```

这里的关键约束不是“feature vector 看起来合理”，而是最终必须仍然是一个可执行 PE binary。

## 2. 必须先分清 CFG、FCG 和作者真正操纵的变量

**CFG（Control-Flow Graph）** 描述单个函数内部 basic block 如何跳转；**FCG（Function Call Graph）** 描述函数之间谁调用谁。PhantomCall 的核心不是仅在一个函数里塞 NOP，而是给 FCG 增加新的 function nodes 和 call edges。

每次 call-site perturbation 的结构是：

```text
原来：
caller ──call──> real_callee ──return──> next

PhantomCall：
caller ──jmp──> trampoline
                  │
                  ├─ call real_callee
                  ├─ call dummy_1
                  ├─ call dummy_2
                  ├─ ...
                  └─ jmp next
```

因此原始调用仍执行，但 graph extractor 会额外看到 dummy functions 和新的 call edges。

### 为什么必须“先调用 real callee，再调用 dummy”？

x86 的调用约定使得进入原 call 前，参数可能已经在 stack 上。原来的 `call` 被 `jmp` 替换后，trampoline 接管执行；如果先乱动 stack，再执行真实 callee，就可能破坏原语义。作者因此先完成原 call，再执行 parameterless、register/memory-neutral 的 dummy leaf functions，最后 `jmp` 回原 call 后的下一条指令。

这其实就是论文最重要的 **treatment-fidelity constraint**：结构必须变化，但原行为不能因为实现错误一起变化。

## 3. PhantomCall 的 Treatment 不是一个开关，而是一组可控维度

论文真正值得我们借鉴的是它把图扰动拆成了多个可调变量：

- **Injection location**：选哪个 call site；
- **Injection volume**：一个 site 加多少 dummy functions，即 (k)；
- **Coverage**：修改多少个 call sites；
- **Function-body content**：dummy body 里使用什么 semantic NOP；
- **Topology**：dummy functions 是互相独立的 leaf，还是再加边形成 DAG；
- **Search budget**：每个 call site 尝试多少种 NOP / configuration。

MalConv / MalGraph 默认每个 site 注入 (k=1sim3)；SAFE+GNN 则需要极端得多的 (k=2500sim3500)。这不是一个可忽略的实现细节：它直接说明**不同模型架构对同一个 structural intervention 的响应机制不同**。

## 4. 为什么还需要 Greedy / Simulated Annealing？

攻击者只有 black-box query：输入 binary，看到 predicted label 和 maliciousness probability (P(m))，没有梯度。

作者的优化目标直觉上就是：

[
min_{sigma} P(m^*)
]

同时满足：

[
P(m^*) < 	au,qquad m^*=Phi_sigma(m),qquad m^*sim m
]

最后一个 (m^*sim m) 表示语义/恶意行为尽量保持。

因此作者设计 Greedy、SA 和 Adaptive SA，在 call sites 与 semantic NOP configuration 上搜索。SA 的意义是：即使某一步没有立即降低 maliciousness score，也可以按温度概率暂时接受，从而避免纯 Greedy 卡在局部配置。

不过一个很有意思的结果是：**call-site 选择本身并没有显示出“聪明排序一定更好”**。作者比较 raw degree、betweenness、eigenvector centrality、局部 instruction density，均没有跨 classifier 稳定超过 random，因此默认仍采用随机 call-site selection。

这对我们的 `disturb@k` 很有启发：不要先验认为 centrality 高、离 GT 近或 graph distance 小就一定是更强干预；这些都应该成为可测的 treatment dimension / effect modifier。

## 5. 实验设计

作者测试三个结构明显不同的 detector：

| Detector | 主要输入 | 为什么重要 |
|---|---|---|
| MalConv | raw bytes | 不直接看 FCG，用来观察结构修改是否通过 bytes 间接影响分类 |
| MalGraph | CFG + FCG hierarchical GNN | 同时依赖局部 CFG 与函数级结构 |
| SAFE+GNN | pure FCG GraphSAGE | 最直接检验 FCG topology 是否是攻击面 |

数据来自 2025 MalwareBazaar Windows x86 PE；SAFE+GNN 另用 2024 corpus 从头训练。作者在 0.1% 与 1% FPR 两个 operating point 测试。最终 attack pools 分别为 MalConv 559/3662、MalGraph 2605/3234、SAFE+GNN 1000/1000。

核心指标有三个：

- **ASR**：原本检测为 malware 的样本中，有多少被改到 detector 判成 benign；
- **SPR**：成功 evasion 中，有多少仍通过 sandbox 行为相似性检查；
- **Throughput Θ**：每小时能生成多少个成功 bypass。

## 6. RQ1：PhantomCall 到底能不能攻击成功？

最直接的结果如下：

| 方法 | MalConv 0.1/1% | MalGraph 0.1/1% | SAFE+GNN 0.1/1% |
|---|---:|---:|---:|
| MalGuise | 100.0 / 97.05 | 91.09 / 82.16 | 1.90 / 0.90 |
| PhantomCall Greedy | 100.0 / 98.31 | 96.81 / 96.94 | **97.40 / 85.00** |
| PhantomCall SA | 100.0 / 99.45 | 95.28 / 94.53 | 88.70 / 64.50 |
| PhantomCall Adaptive SA | 100.0 / 99.40 | 96.01 / 94.28 | 88.60 / 64.50 |

最值得看的不是 MalConv 的 100%，而是 SAFE+GNN：原 CFG-oriented baseline MalGuise 基本打不动 pure-FCG classifier，而显式 FCG node/edge injection 后 ASR 跳到 85–97.4%。

因此这不是“随便多加 bytes 都能骗模型”的证据；至少对 pure-FCG 模型，**真正改变 FCG topology 是关键因素**。

## 7. RQ2：到底是哪一部分起作用？

### 7.1 去掉 FCG injection

作者保留 trampoline / displacement，只拿掉 dummy function nodes：

| 模型 | With FCG | Without FCG | 差异 |
|---|---:|---:|---:|
| MalConv 0.1% | 100.0 | 99.46 | +0.54 pp |
| MalGraph 0.1% | 96.01 | 88.64 | +7.37 pp |
| MalGraph 1% | 94.28 | 84.13 | +10.15 pp |
| SAFE+GNN 0.1% | 97.40 | 0.90 | **+96.50 pp** |
| SAFE+GNN 1% | 85.00 | 0.10 | **+84.90 pp** |

这个 ablation 很干净地展示了 **Treatment × Architecture** 的异质性：对 byte model 几乎没额外价值，对 mixed graph model 中等，对 pure-FCG model 是决定性的。

### 7.2 Search 是否必要？

对 MalConv / MalGraph，Adaptive SA 与“一次随机 NOP 后就走”的 1-Pass 相比，ASR 可高约 26–62 pp；代价是 throughput 下降。也就是说，**结构扰动本身与如何寻找有效内容配置是两个独立贡献来源**。

### 7.3 SAFE+GNN 更依赖“数量”而不是 NOP 内容

SAFE+GNN 使用 global mean pooling。大量 dummy function embeddings 被平均进去后，会稀释原 malware representation。作者的附录分析中，SAFE+GNN graph-level embedding 的 mean L2 norm 从约 4.4 降到 0.4。

因此这里有一个非常清楚的机制：

```text
大量新增 dummy nodes
        ↓
global mean pooling 等权聚合
        ↓
原 malware nodes 的 representation 权重被稀释
        ↓
graph embedding 改变
        ↓
classification 翻转
```

这和 LLM 的 “attention dilution” 只能做**类比**，不能直接等同。GNN mean pooling 的 dilution 是明确的数学聚合机制；LLM context dilution 是否通过 attention、retrieval、reasoning trajectory 或 evidence competition 发生，需要另行实验。

## 8. RQ3：Topology 和扰动强度有什么关系？

作者把默认的独立 leaf dummy functions 改成彼此带边的 DAG。结果反而统一变差：MalConv 下降较小；MalGraph 最多约 -5.5 pp；SAFE+GNN 最多约 -34.3 pp。

作者的解释是，互相连接的 dummy functions 会形成更明显的结构 cluster，反而更容易被 graph model 识别。换句话说：

> **不是“图越乱越有效”，而是 perturbation topology 与模型 aggregation mechanism 的交互决定效果。**

超参数实验也显示，SA 初始温度影响很小；MalGraph 对 NOP diversity 很敏感；把 (k) 固定为 1 会使 MalGraph ASR 下降 11.5 pp，而 (kge3) 后变化趋于饱和。

这已经非常接近我们想做的 **dose-response** 思路：不是只比较 Context / No Context，而是画出 intervention strength 增加后 Outcome 如何变化，以及何时进入 plateau / tipping point。

## 9. RQ4：“语义保持”到底验证到什么程度？

作者没有只说“dummy function 理论上是 NOP”，而是做 sandbox validation。

对 original malware 跑两次，先测 malware 自己的非确定性；再把 adversarial variant 的 Windows API-call sequence 与 original 比较。距离使用 normalized Levenshtein distance，并以 original-vs-original 距离分布的 99.5 percentile 作为每个配置的 equivalence threshold。

SPR 结果：

| MalConv | MalGraph | SAFE+GNN |
|---|---|---|
| 86.26–87.00% | 90.00–93.00% | 93.67–96.95% |

所以“semantics-preserving”不能理解成实验上 100% 等价。更准确的说法是：

> transformation 按构造意图保持语义，但实际 sandbox proxy 只有 86–97% 的成功 evasions 被判定为保留原行为。

而且 sandbox 的 API trace similarity 仍只是 behavioral proxy，不是形式化语义等价证明。

这个边界对我们的 repository-topology intervention 尤其重要：未来如果真的重写 Python call graph，不能只说“wrapper 理论上等价”，还要跑原测试、漏洞测试、输出/trace comparison，最好再独立提取 graph 验证“结构真的按预期变了”。

## 10. RQ5：防御有效吗？

作者测试 adversarial finetuning 与结构 heuristic。

Adversarial finetuning 后，1% FPR 下 ASR 大致变为 MalConv 81.0%、MalGraph 82.7%、SAFE+GNN 26.3%。它明显增强 robustness，但没有消灭攻击。

简单结构 heuristic 可以做到很高 TPR，但存在明显 trade-off。例如只检查新 section 可达到 100% TPR，但 benign FPR 为 9.5%；组合 OR heuristic 达到 100% TPR 时 FPR 为 17.4%。而专门检测 leaf injection 的 heuristic 虽然 FPR 很低，攻击者把 dummy functions 连成 DAG 后就能明显削弱它。

因此论文证明的是“这些简单 defense 不足以完全解决问题”，不是“PhantomCall 可以普遍绕过现实 AV”。附录对商业 AV 的测试恰好提醒了这个边界：Bitdefender、Microsoft Defender、Norton 上 ASR 只有约 14–18%，因为真实产品还有 signatures、API sequence、behavioral analysis 等正交信号。

## 11. 和当前研究的真正连接：它比 RepoMirage 更接近哪一步？

结合最新研究记录，现在主线已经明确区分：

```text
A. Context-selection intervention
固定 vulnerable repository
只改变 localizer 看见的 graph/code context

B. Repository-topology intervention
真正重写 repository / call structure
保持任务语义与 vulnerability 不变
```

当前 `oracle-matched / disturb@2 / disturb@3` 属于 **A**。PhantomCall 属于 **B**，而且它比 RepoMirage 更直接地操纵 Function Call Graph。

所以最有价值的不是把 PhantomCall 原样搬过来，而是抽象出它的 intervention schema：

| PhantomCall | VLocBench 可迁移设计 |
|---|---|
| call site | 已验证的 caller/callee edge / mechanism anchor |
| dummy function count (k) | 每层增加的 distractor node / branch width |
| leaf vs DAG topology | distractor 的连接结构 |
| random / centrality site | random / graph-distance / centrality-based context selection |
| size budget | source-token / file-count envelope |
| malware behavior preservation | vulnerability/test/behavior preservation |
| FCG extraction | 独立 call-graph extraction 验证 treatment fidelity |
| ASR | localization F1 / Recall / false positives |
| architecture sensitivity | model × treatment heterogeneous effect |

尤其值得注意的是，你刚提出的 `disturb@2/@3` 与 PhantomCall 的思想高度一致：**保留主干，同时控制额外分支的数量和结构。** 但第一阶段仍应在“模型可见 Context”上做，因为这样可以完全固定 repository snapshot，不引入真实代码重写造成的新混杂。

## 12. 可以直接借到实验里的四个设计原则

### 原则一：Treatment 要拆成 dose × topology × location

不要只有 `Local vs Graph`。至少记录：

[
T=(	ext{dose},	ext{distance},	ext{topology},	ext{relevance},	ext{token budget})
]

这比“加 call graph 后下降了”更能回答机制问题。

### 原则二：必须做 matched control

PhantomCall 的消融会尽量固定 search strategy / displacement，只去掉 FCG injection。对应到当前实验，就是 `oracle-matched` 与 `disturb@k` 必须匹配 files / source tokens，避免把规模差异当成 graph effect。

### 原则三：Treatment fidelity 与 semantic fidelity 分开检查

两个问题必须分别回答：

1. **图真的变了吗？**——节点、边、hop、branch width、edge type 是否达到预注册条件；
2. **任务真的没变吗？**——GT、vulnerability、tests、observable behavior 是否保持。

### 原则四：预期 Heterogeneous Treatment Effect，而不是寻找单一结论

PhantomCall 同一个 perturbation 在 MalConv、MalGraph、SAFE+GNN 上机制完全不同。对应到 LLM：

[
	au(x)=E[Y(1)-Y(0)mid X=x]
]

这里 (X) 可以包括模型、context requirement、seed quality、graph distance、repository size 等。目标不是证明“context hurts”，而是找出 **何时、对谁、通过什么结构会 hurt**。

## 13. 这篇论文证明了什么，没有证明什么？

**它比较有力地证明了：** Windows PE 上可以构造真实可执行的 FCG structural perturbation；FCG injection 对 graph-based detector，尤其 pure-FCG SAFE+GNN，是强攻击面；扰动量、拓扑、body content 与模型架构存在明显交互；语义保持不能只靠代码构造声明，需要额外 behavioral validation。

**它没有证明：** 任意程序都能无副作用地改写 call graph；FCG 越大越坏；所有 graph model 都存在同样机制；商业 AV 会被同等程度攻破；更没有证明 LLM repository context 的性能下降来自同一种 pooling / dilution 机制。

## 14. 对当前研究最值得留下的一句话

**RepoMirage 教我们“保持任务、改变 repository evidence structure”；PhantomCall 则进一步展示“保持程序行为、把 FCG 的 location / dose / topology 做成可控干预变量”。当前 VLocBench 最合理的顺序仍是先做 context-selection counterfactual，等 matched treatment 和机制证据稳定后，再把 PhantomCall 式真实 call-graph rewrite 作为第二层实验。**
