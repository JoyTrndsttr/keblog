# GraphLocator：用仓库图上的结构化归因追踪软件问题

> **论文**：[GraphLocator: Graph-guided Causal Reasoning for Issue Localization](https://arxiv.org/abs/2512.22469)  
> **作者**：Wei Liu, Chao Peng, Pengfei Gao, Aofan Liu, Wei Zhang, Haiyan Zhao, Zhi Jin  
> **单位**：北京大学高可信软件技术教育部重点实验室与计算机学院、北京大学电子与计算机工程学院、字节跳动  
> **会议**：FSE 2026 Research Papers  
> **DOI**：[10.1145/3797079](https://doi.org/10.1145/3797079)  
> **版本**：[arXiv:2512.22469v1](https://arxiv.org/html/2512.22469v1)，2025-12-27

## 先用三句话建立论文地图

GraphLocator 研究的是：给定自然语言 issue 和代码仓库，怎样从“用户看到的症状”沿程序依赖追到更深的修改位置，并在一个 issue 涉及多个相互依赖实体时避免只找出一个入口。它先把仓库构造成 Repository Dependency Fractal Structure（RDFS），再用 SearchAgent 找症状节点，随后逐轮访问邻居、生成子问题和假设性的因果依赖，最终形成 Causal Issue Graph（CIG）。在 SWE-bench Lite、LocBench 和 Multi-SWE-bench Java 上，作者报告 GraphLocator 相比基线平均提高函数级 recall 19.49 个百分点、precision 11.89 个百分点；但论文也明确承认 CIG 不识别统计意义上的因果效应，边权是 LLM 对相对因果可能性的赋值。

全文的逻辑链是：

```text
issue 往往只描述症状，且一次修复可能涉及多个实体
                         ↓
把目录、文件、类、方法等统一表示为分层异构 RDFS
                         ↓
SearchAgent 用名称、类型和边查询定位症状节点
                         ↓
每轮只展开一个高优先级子问题
                         ↓
读取其 RDFS 邻居，用溯因推理提出新的子问题与依赖
                         ↓
持续更新 CIG，输出关联的文件 / 模块 / 函数
                         ↓
用补丁位置评价定位，并把 CIG 交给下游修复器
```

理解论文时必须先分清三个“图”：

1. **RDFS** 是从代码静态结构得到的仓库图，节点是目录、文件、类、字段、函数等，边是包含、导入、使用、继承和实现关系。
2. **CIG** 是针对一个 issue 动态生成的解释图，节点是自然语言子问题并关联 RDFS 实体，边表示模型假设的原因—结果关系。
3. **补丁真值** 是开发者最终修改过的位置集合。它用于评价，但不等于唯一根因，也不保证所有被改文件都是机制核心。

## 1. Research Gap：相关性检索为什么不够

论文把 issue localization 的语义鸿沟拆成两个具体错配。

第一是 **symptom-to-cause mismatch**。issue 常写“计算结果错误”“端点太慢”或“调用失败”，但没有直接说哪个内部函数或依赖是根因。单纯用文本相似度检索，最容易找到复述症状的入口，而不是多跳依赖后的实现缺陷。

第二是 **one-to-many mismatch**。一次修复可能需要多个文件、类或函数协同变化。固定的 file→class→function 漏斗一旦早期选错就难以回退；自由探索型 agent 又可能在大量相关节点中不断扩张，召回上升而精度崩溃。

GraphLocator 的核心主张不是“图比文本好”，而是把两类 workflow 拼接起来：Phase I 保留 agent 的灵活搜索，Phase II 改为一次只展开一个子问题的程序化队列，并用 CIG 保存跨轮归因状态。其新意主要在搜索过程的状态表示和调度，而不是发明一种新的静态程序分析关系。

## 2. RDFS：把不同粒度的代码实体放进同一张图

RDFS 被定义为七元组，包含节点、边、类型、代码片段，以及把节点类型映射到层级的函数。论文将常见面向对象仓库划成四层：

- 目录与包；
- 文件；
- 类、接口与枚举；
- 字段、方法、函数和全局变量。

边类型包括 `HasMember`、`ImportedBy`、`UsedBy`、`ExtendedBy` 和 `ImplementedBy`。Figure 3 的重要信息不是图长什么样，而是层间和层内关系被统一查询：agent 可以先按层级找到文件或类，也可以沿调用、使用、继承关系在同层追踪。

这种设计有两个直接收益。其一，搜索工具参数明确包含名称与类型，减少同名实体歧义；其二，RDFS 可以只预建层间骨架、按需加载层内依赖，避免先完整构造所有细粒度边。代价是它仍依赖静态解析质量：反射、动态调用、运行时注册和生成代码很可能不完整，论文没有把 RDFS 当作真实运行时调用图。

## 3. Phase I：先找症状节点，不急着猜根因

SearchAgent 只有三类操作：

- `search_vertex(name, type)`：按名称和类型查节点，允许通配符；精确匹配失败时使用字符串编辑距离做模糊搜索，再让 LLM 根据路径、行号和代码过滤 top-k。
- `search_edge(src, relation, dst)`：按端点、类型和关系查询结构，例如某函数被哪些实体使用。
- `finish`：结束本阶段，返回与 issue 症状最直接对应的节点集合。

这个阶段刻意只解决“issue 在仓库中落在哪些入口”而不要求一步猜中最终补丁。Table 3 的消融给出强证据：去掉 `search_vertex` 后，跨三个数据集平均的函数级 F1 从 30.91% 降到 14.23%；`search_edge` 的移除也会退化，只是幅度较小。

但这里存在一个值得注意的混合机制：模糊候选先由字符串相似度召回，再由同一个或同类 LLM 做语义过滤。因此 Phase I 的收益不能完全归功于图结构，模型的候选筛选、代码片段序列化方式和 top-k 范围都在共同起作用。

## 4. Phase II：CIG 怎样逐轮长出来

### 4.1 CIG 不是统计因果图

CIG 的节点是自然语言子问题，每个子问题映射到一组 RDFS 节点；有向边表示子问题间的假设性因果关系，边权位于 0 到 1。论文用结构因果模型作概念类比，但明确写明：CIG **不识别经统计验证的因果效应**，而是为 LLM 溯因推理提供结构化工作记忆。

因此边权不能解释成“干预该函数会以 0.85 的概率导致症状”，更不能直接用于 treatment-effect 估计。它只是模型在当前 prompt 和候选邻居下分配的相对优先级。

### 4.2 优先队列一次只展开一个子问题

对一个子问题 $x$，论文把其优先级写为：

$$
\Psi(x)=1-\prod_{(x,y)\in\mathcal{Y}}(1-\psi(x,y))
$$

直觉是：若 $x$ 对多个已知结果都有较高的模型赋权，它更值得先展开。每轮从队列取最高优先级子问题，收集与其关联代码节点相邻、但尚未访问的 RDFS 节点，再让 CausalAgent 更新 CIG。新发现的子问题入队，已覆盖代码节点加入 visited 集合。

这个过程把自由 agent 的“同时追很多线索”改成单分支扩展，目的是保持跨轮因果叙事一致。Figure 4 的 Astropy 例子显示，模型从 issue 明示的 `separability_matrix` 出发，经“嵌套 separability matrix 处理错误”等中间子问题，最终落到 `_cstack`。真正值得记住的是中间节点承担了可审计的解释桥，而不只是最终命中。

### 4.3 动态解耦 one-to-many

所谓 dynamic issue disentangling，不是先规定 issue 有几个子任务，而是在邻居展开中逐步产生子问题。多个分支可以共享或交叉，因此作者称其为 graph 而不是 tree。对多函数真值，Figure 7 显示所有方法随涉及函数数增加而更难完整覆盖，但 GraphLocator 的 recall/precision 平衡最好；LocAgent 在单函数时接近，函数数增加后退化更明显。

## 5. 实验设计：评价对象与口径

实验覆盖三套数据：

| 数据集 | 语言 | 规模 | 特点 |
|---|---|---:|---|
| SWE-bench Lite | Python | 300 | 11/12 个常用项目的真实 issue，主要为 bug fixing |
| LocBench | Python | 559 | 164 个仓库，包含功能、安全、性能和 bug 等多类维护任务 |
| Multi-SWE-bench Java | Java | 128 | 9 个可执行项目，带人工复核真值 |

作者从 human-written fix patch 在文件、模块和函数三级重提取真值：文件级记录所有修改路径，模块级取包含修改行的类/接口/枚举，函数级取直接包含修改行的函数或方法。指标包括：是否完全覆盖真值的 Success Location（SL）、Recall、Precision 和逐实例 F1。

对比方法包括 SWERank-Small/Large、Agentless、LocAgent 和 CoSIL；GraphLocator 分别使用 GPT-4o-2024-11-20 与 Claude-3.5-Sonnet-2024-10-22。四个 RQ 分别检查总体有效性、对症状距离和多函数任务的泛化、组件消融，以及图构造与 LLM token 成本。

这里最重要的口径限制是：补丁位置是可复核 outcome，但不一定是唯一合理定位。替代修复、辅助修改、测试文件和格式性变更都可能使“预测了机制核心但没覆盖所有 patch 文件”的系统被低估。作者在 validity threats 中承认这一点。

## 6. 主结果：最大的收益在精度，而不是无边界扩大召回

Table 2 显示 GraphLocator 在三数据集、两模型和三级粒度上整体领先 LLM 基线。论文汇总称，函数级 recall 平均提升 19.49 个百分点，precision 提升 11.89 个百分点。以 SWE-bench Lite + Claude-3.5 为例，GraphLocator 的函数级 SL/REC/PRE/F1 为 70.76/73.23/20.51/27.73；LocAgent 为 58.48/61.94/5.01/8.60。

这个结果支持的不是“CIG 已找到了真实因果”，而是“显式结构状态和受控扩展能减少自由图搜索的过预测”。论文指出 GraphLocator 的函数级优势比文件级更明显：粒度越细，候选越多，相关但非修改实体越难区分，结构化展开的精度收益才更突出。

Figure 6 按 RDFS 上症状节点到全部真值函数的最短路径汇总难度。距离增大时所有方法表现都下降，GraphLocator 仍最好。但距离的构造本身依赖 Claude-3.5 从 issue 抽关键词、精确映射节点，并排除无法映射的实例；因此它是一个经过筛选的图距离 proxy，不是任务固有、与模型无关的真实因果距离。

## 7. 消融：哪些部件真的在贡献

Table 3 分别移除 Phase I 的 `search_vertex`、`search_edge`，以及 Phase II 的优先队列和 CIG prompt guidance。四项移除都会使性能下降：

- `search_vertex` 是从自然语言进入仓库图的主桥，移除后退化最大；
- `search_edge` 提供结构约束，防止只有名称相关性；
- CIG guidance 让后续轮次保留已经提出的依赖与子问题；
- priority queue 主要改善 recall，使扩展更集中于高潜力分支。

这组消融说明“搜索工具 + 跨轮结构状态 + 调度”整体有效，却仍不是严格析因。组件之间存在交互，移除某一项会改变 prompt、访问轨迹、token 和候选集合；单项下降不能被解释为该组件独立的平均因果效应。

## 8. 成本：比 LocAgent 省，但远非最便宜

Table 4 报告每实例平均 LLM 交互量。GPT-4o 下 GraphLocator 输入/输出约 99.44k/7.56k token，估算 0.61 美元；LocAgent 为 211.23k/1.74k、1.08 美元；CoSIL 只需 12.93k/0.86k、0.08 美元。Claude-3.5 下 GraphLocator 约 156.80k/6.71k、0.57 美元。

所以正确结论是：GraphLocator 相对自由探索的 LocAgent 显著减少输入和成本，但相对程序化的 Agentless、CoSIL 仍更贵。它用更多输出 token 换取显式子问题与 CIG，适合把“可审计的中间结构”视作产品价值的场景，不适合只追求最低单次成本的批量筛选。

## 9. 下游修复：知道在哪里，并不等于知道怎么修

作者将不同定位结果接入 Agentless 和 Trae Agent，并比较只按拓扑顺序提供代码实体与额外序列化 Mermaid CIG 两种设置。SWE-bench Lite 上，Trae Agent 的 resolved rate 从 25.00% 提升到 GraphLocator+CIG 的 30.67%；Agentless 从 25.33% 到 28.67%。Multi-SWE-bench Java 也总体改善。

Table 5 最值得看的不是“最高提升 28.74%”，而是同一定位结果在保留结构后通常优于只给扁平代码列表。这暗示下游修复器不仅需要候选位置，还可能受益于“这些位置为什么相关”的关系表示。

但实验是 single-sample greedy 的 proof of concept，且不同定位器输出的数量、顺序和文本量未必严格匹配。论文也承认绝对 resolved rate 仍低：定位改进不能替代补丁生成、编译、测试和验证。

## 10. 作者与课题组背景

第一作者 **Wei Liu** 的论文署名为北京大学高可信软件技术教育部重点实验室与计算机学院。公开原文没有提供足以独立确认其职称、完整履历或长期个人研究方向的主页，因此这里不作超出论文与可核验成果的推断；就本文而言，他承担的研究对象集中在基于 LLM 的软件 issue 定位、仓库结构建模和可审计推理。

论文明确把 **Chao Peng** 标注为通讯作者，不能因作者顺序把末位作者默认视为通讯作者。原文署名显示其来自字节跳动；其公开合作成果还包括 repository-level issue resolution 系统 Trae Agent，说明本工作与团队在真实仓库 agent、定位—修复流水线和下游验证方面的积累直接相连。

其余团队横跨北京大学的软件工程与高可信软件研究单位以及产业研究者。共同作者 Haiyan Zhao、Zhi Jin 等所在团队长期关注软件工程、需求与智能化软件开发；本文把这类“结构化软件知识”积累具体化为 RDFS，把产业侧 repository agent 经验落实为搜索、队列和修复器集成。这个背景能解释方法为何同时强调静态结构、agent workflow 和下游修复，但不能被当成实验有效性的替代证据。

## 11. 重要图表怎样读

- **Figure 1** 用两个例子区分症状—原因错配与一对多错配，是整篇论文的任务定义，而不只是动机插图。
- **Figure 3** 展示 RDFS 的四层结构；阅读时要看边类型和粒度，不要把所有边都叫 call graph。
- **Figure 4** 展示 Astropy issue 的 CIG。它证明系统能生成中间归因链，但不证明链上的每条边是可干预、可统计识别的真实因果关系。
- **Figure 6/7** 显示随着图距离或真值函数数增加，所有系统都会退化；GraphLocator 的相对优势支持其复杂任务鲁棒性，但分桶变量由补丁和模型辅助构造，存在选择与测量依赖。
- **Table 2** 是定位主结果，重点看 precision 与 function level；只看 SL 会忽略大量过预测。
- **Table 3** 支持各模块有用，但不能独立估计每个模块的 treatment effect。
- **Table 4** 说明效率结论是“相对 LocAgent”，不是“普遍低成本”。
- **Table 5** 提供下游价值证据，也同时提醒定位指标与最终修复并非一一对应。

## 12. 论文证明了什么，没有证明什么

### 有证据支持的结论

1. 在三个 Python/Java benchmark 的补丁位置口径下，GraphLocator 的定位表现总体优于所选 embedding、程序化和 agentic 基线。
2. 优势在函数级尤其明显，主要来自降低过预测并保持较高 recall。
3. 搜索节点/边、CIG guidance 和优先队列都与性能相关，移除任一组件都会退化。
4. 相比 LocAgent，GraphLocator 使用更少输入 token 和更低费用；相比 CoSIL 则成本更高。
5. 把 CIG 结构提供给下游修复器，比只提供扁平候选列表更有希望提升单样本 resolved rate。

### 尚未被证明的结论

1. CIG 没有识别统计因果效应，边权也没有经过概率校准；“causal”主要指结构化溯因语义。
2. 没有证明 RDFS 捕获了完整运行时依赖，尤其未覆盖反射、动态注册和输入相关调用。
3. 没有证明 human patch 是唯一正确真值，也没有把机制核心、必要修改和辅助改动分开评分。
4. 没有在严格等 token、等候选、等调用次数下单独识别“加入 CIG”的净效应。
5. 下游修复实验规模和采样设置不足以说明定位提升必然转化为可部署的修复收益。
6. Python/Java 开源仓库结果不能直接外推到 C/C++、多语言 monorepo、闭源系统或安全漏洞定位。

## 13. 真正应该记住什么

- GraphLocator 的实用创新是把仓库图搜索拆成“找症状入口”和“逐轮追归因”两阶段。
- RDFS 是代码结构图，CIG 是 LLM 生成的 issue 解释图；两者不能混称为 call graph。
- CIG 边权是模型分配的调度信号，不是概率校准后的因果效应。
- 论文最强结果来自函数级 precision，说明受控扩展主要在抑制相关但不必要的候选。
- 补丁位置适合做可复核 benchmark outcome，却会把替代修复和机制命中压成单一集合匹配问题。
- 显式结构对下游修复可能有价值，但“哪里改”与“怎么改”仍是两个不同任务。

## 14. 对当前研究的启发

当前研究已经直接使用 GraphLocator 的冻结 trace、RDFS 和 CIG，因此这篇论文不是一般 related work，而是 treatment 构造与解释边界的原始依据。

第一，现有实验页面中每轮变化的 0.80→0.85 应继续称为 **model-assigned edge weight**。论文自己明确否认 CIG 在识别统计因果效应；研究报告不能把该权重写成真实概率、效应大小或模型信心的校准值。冻结 trace 中队列弹出、邻居暴露、CIG 重写的时间顺序应完整保留。

第二，RDFS treatment 必须按关系类型报告。GraphLocator 的图包含 `HasMember`、`ImportedBy`、`UsedBy`、继承和实现，不是只有 caller/callee。当前 `disturb@1/@2` 的 sibling、semantic transition 和 path bridge 应记录具体边类型；否则“调用图上下文”会夸大实际干预的语义纯度。

第三，论文的 symptom-to-cause distance 很适合做异质效应候选，但不能原样当作预处理难度变量。其距离依赖 Claude 抽关键词、精确映射、补丁函数真值，并剔除不可映射样本。当前 VLocBench 应优先使用冻结输入可观察的 seed、静态路径长度、候选分支宽度，并把 patch-derived distance 标为 answer-aware diagnostic。

第四，论文再次暴露 patch GT 与机制正确性不等价。当前 `fObS7tW2` 中模型命中 `function.py` 和 lock primitive 相关 `utils.py`，却未覆盖所有 patch 文件，这与 GraphLocator validity threat 完全一致。正式 outcome 应同时报告 official file F1、vulnerable-snapshot observable F1、机制命中和归因偏移，而不能用单一 patch F1 判断是否“理解漏洞”。

第五，GraphLocator 自身就是一个多轮、动态暴露上下文的系统。若研究“repository context expansion 是否帮助”，应冻结其 Phase I seed、RDFS snapshot、CIG trace、prompt 和预算，只在最终可见 context bundle 上干预；若同时让 agent 重新搜索，treatment 会混入路径选择、调用次数和边权更新。

最后，论文的消融不是当前因果主张的替代物。它表明组件移除会改变系统表现，但没有控制 token、候选集合与轨迹。当前 tokenizer-aware、同文件数、固定核心、多个噪声 seed 的设计，正是在把“GraphLocator 有效”推进为更细的问题：**哪类仓库证据、在何种真实上下文需求下，改变了模型的机制判断与文件归因。**
