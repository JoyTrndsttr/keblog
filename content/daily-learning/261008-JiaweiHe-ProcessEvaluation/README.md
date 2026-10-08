# What Process Evaluation of Coding Agents Actually Measures: Action, Task, and Step Are Three Different Levels

> 精读日期：2026-10-08  
> 第一作者：Jiawei He（何佳伟）；共同一作：Mengyu Shi（原文标注 equal contribution）  
> 通讯作者：**Xikai Yang、Dong Sun**（论文首页明确标注 corresponding author）  
> 机构：Amap / Alibaba Group；Nanjing University, State Key Laboratory for Novel Software Technology  
> Venue：arXiv 预印本，2026-08-24，v1（尚不应称为已录用会议论文）  
> 原文：[arXiv](https://arxiv.org/abs/2608.22960) · [完整 HTML](https://arxiv.org/html/2608.22960) · [PDF](https://arxiv.org/pdf/2608.22960)  
> Tags：`2026` `arXiv` `Coding Agent` `Causal Inference` `Process Evaluation` `Step Attribution` `SWE-bench Verified` `Repository Graph` `Trajectory` `Collider Bias`

这篇论文非常值得认真读，但它的主要贡献**不是发明了一个更准确的步骤打分器**。作者把大家习惯混在一起的“过程评估”拆成三个根本不同的问题：下一步行动能否预测（action level）、一次任务执行究竟有多不确定（task level）、某一步对最终结果有多少因果贡献（step level）。然后用同一套可重放的 coding-agent 文件定位轨迹检验这三个问题。结果颇有反直觉性：**工具输出中刚出现过的路径，比代码依赖图更能预测下一步；执行不确定性主要随任务变化；把完整未来轨迹交给 LLM judge，会系统性地把“责任”归给更靠后的步骤。**

## 1. 从现实问题到可测对象：先建立整篇论文地图

**过去：** 软件工程 Agent 通常用 SWE-bench 最终是否成功来评价。近来研究者又开始打分工具调用、搜索动作、过程缺陷、关键步骤等。

**问题：** “这一步看起来不合理”“这一步很可能发生”“这一步真正改变了最终结果”并不是同一件事。如果评价器使用完整执行轨迹及结局去评价早期动作，还可能把未来信息当成早期动作的功劳或过错。

**作者的选择：** 用可以复原环境、可检查文件真值的 repository file localization 作为最小实验载体；把 agent 的状态—动作—工具观察建成结构因果模型（Structural Causal Model，SCM），通过固定历史前缀后重新执行后续过程，估计步骤影响；同时设计无需可信因果真值的 judge 信息集干预，检验“未来可见性”是否改变归因。

```text
Research Gap：过程分数的对象与因果含义混淆
  ↓
Research Object：issue + repository snapshot + agent action/observation trace + gold files
  ↓
Operationalization：
  action → next tool/object prediction
  task   → repeated continuation outcome variance
  step   → prefix-conditioned action substitution effect
  ↓
Method：SCM + prefix reconstruction + replay/real intervention
  ↓
Evidence：499 个定位任务；7616 个动作点；190 个重放估计点；
          图结构置换对照；70 个 judge 归因样本
  ↓
Claims：
  provenance 主导短期动作预测；
  graph 主要界定工作区域而非移动顺序；
  任务差异比步骤差异更能解释执行方差；
  full-trace judge 具有未来信息引起的系统性归因偏移
```

先区分五个概念。

**Execution provenance（执行来源信息）**：此前工具输出里出现过哪些文件路径、这些路径出现的位置与频率。它不是 Git provenance，也不是静态调用关系；例如 grep 刚输出 `pkg/a.py`，agent 下一步打开该文件，这种转移属于观察来源驱动。

**Causal estimand（因果目标量）**：在相同已发生历史下，把当前动作从 a 换成 a'，最终定位结果期望改变多少。先确定目标量，才能判断一个评分器是否真的测到了它。

**Positivity / overlap（正值性 / 重叠性）**：固定同一历史后，策略有非零概率产生需要比较的两个动作。如果 Agent 总是确定地执行同一个动作，单凭观察数据无法估计另一个动作的后果。

**Anytime value（任意时点价值）**：执行到某一步时，考虑剩余策略随机性后最终成功的期望值。它的相邻变化可作为过程贡献，但不是简单的“这一工具调用是否有用”。

**Collider / post-treatment bias（碰撞点 / 处理后偏差）**：早期动作会影响后续动作与结局；评价早期动作时再依据这些后代信息筛选或条件化，可能改变原本要估计的效应。本文用 judge 的信息集实验直接测其可见行为，不能把“归因往后移动”误称为已识别模型内部心理机制。

## 2. Research Gap：为什么过程评估的三个层级不能互相替代

设想一个 agent 先搜索 `headers`，再打开几个类定义，最后报告漏洞文件。你可以问：

- **Action：** 搜索之后它大概率会打开哪个文件？这关乎工具推荐与路径预测。
- **Task：** 固定同一个 issue，重复运行结果稳定吗？这关乎任务本身的难度和策略波动。
- **Step：** 若把那次搜索改为另一个搜索，保留之前真实历史，最终结果会怎样？这才是步骤因果贡献。

以前的过程奖励模型（Process Reward Model，PRM）、人工缺陷标注、full-trace judge、restart ablation，常被放在“过程质量”大框架下讨论。作者指出它们的条件信息集不同：PRM 的标签可能由完成后的轨迹回填，full-trace judge 看到了未来，restart ablation 连已发生的历史也重新采样，人工缺陷标签只需与评审者一致。即使这些指标有工程价值，也不能据此直接声称“识别了这一步的因果效应”。

这是一个**测量构念（construct validity）**问题，而不是“某个 judge 准确率不够”的普通 benchmark 问题。

## 3. 方法全流程：从一次真实运行到可估计的步骤影响

```text
issue + 固定 repository commit + gold files
  → 执行一次 Agent，保存 (action, tool output) 完整轨迹
  → 选取若干时间点，按 item 粒度重建真实 prefix
  → 重置 repository、环境与随机相关配置
  → 从同一 prefix 多次继续执行，收集终局结果
  → 测该点 next-action 的经验熵
       ├─ 有 overlap：使用 observational replay
       └─ 无 overlap：实际替换动作并执行工具，注入真实返回值
  → 估计 anytime value 与局部变化
  → 比较 action predictors、task variance 与 attribution judges
```

### 3.1 SCM：状态、动作、观察、结局

作者把 Agent 的一步拆成：状态 S_t 产生动作 A_t；环境/工具对动作返回观察 O_t；状态更新函数用 S_t、A_t、O_t 构造 S_{t+1}。动作采样采用 Gumbel-max 表示，即用策略 log-probability 加独立 Gumbel 噪声再取最大项。这个写法是为了把模型采样的随机性显式纳入因果模型，并不表示实际运行一定开放所有 token 的 log-probabilities。

终局输出是预测文件集 F_hat；初始形式的成功定义为 gold file set F* 被 F_hat 包含。作者不要求精确集合相等，因为报告额外测试文件并不一定意味着定位失败。**但正式估计步骤变化时又改用 gold-file recall，不能把形式定义与实际统计指标混为一谈。**

### 3.2 Prefix-conditioned treatment：保留什么，改变什么

核心目标（Eq.1）：

θ_t(a,a') = E[Y_{A_t=a'} − Y_{A_t=a} | τ_{1:t−1}]

其中 τ_{1:t−1} 是 t 之前已经发生的真实动作和观察。比较时固定它，仅改变 t 的动作，再让后续过程继续。这与“重新开始整个 Agent 并改变提示词”不是同一个 estimand：后者同时重新抽取早期轨迹和工具结果。

论文给出三条识别假设：①完整 prefix 足以确定当前 Agent state；②当前解码噪声相对任务难度、过去与未来外生；③给定动作、仓库和环境噪声后，工具输出可重放。若都成立，固定 prefix 后动作差异只来自当前外生采样噪声，可以得到局部顺序随机化（Proposition 1）。**注意：识别结论还要求比较动作有正概率；上下文压缩、隐式状态、不可重放环境都可能使它失效。**

一个直观例子：在固定 issue 与已读文件的前提下，若模型偶尔选择 `grep foo`、偶尔选择 `grep bar`，可以比较各自后续定位结果；若它永远选择 `grep foo`，不能把未出现的 `grep bar` 效应从原策略的观察数据里“算出来”。

### 3.3 Anytime value 与可加性

定义 v_t = E[Y | τ_{1:t}, q, G]，Δ_t = v_t − v_{t−1}（Eq.7–8）。这衡量的是：执行到这一步并得到观察后，最终预期结果相对上一步变化了多少。

数学上 Σ_t Δ_t = v_T − v_0 = Y − E[Y|q,G]（Eq.9），因为相邻项首尾抵消（telescoping）。**可加性来自定义，不代表每个估计的 Δ 都准确，也不代表五个稀疏采样点的估计值能精确相加。**作者在 Appendix D 明确承认正式实验只选离散 segment，未做连续窗口的可加性实证验证。

更细地说，一个 Δ 可拆成两部分（Eq.24–25）：选择某个动作相对策略平均动作的变化，以及执行动作后看到特定工具输出造成的变化。前者更接近决策/规划，后者更接近搜索工具或环境证据；两者不应混成“工具调用好坏”。

### 3.4 为什么要混合 observational replay 与真实 intervention

每个选定 prefix 多次 fork continuation，平均最终 Y 得到 v_hat。对下一动作按 (tool, target object) 分桶并计算经验熵 H_hat。

- 若 H_hat > 0，观察到至少两个动作桶，有局部 overlap，可以使用相邻 prefix 的 replay value 差；
- 若 H_hat = 0，原策略在采样中近乎确定，作者换成实际替代动作（如图上邻近文件或 oracle gold-file inspection），**真的执行这个工具动作，获取真实工具输出**，再继续跑。

为什么不能自己编一个“看起来合理的 grep 返回值”？因为那会同时改变 observation 生成机制，测的是“注入某条观察”而非“改变某个动作”。二者都是可能的实验，但目标量不同。

替代动作属于一个适度扰动的策略支持集，而非原确定性策略的自然随机化。论文为此明确增加 **perturbation transferability** 假设（Assumption 4），并区分原策略与扰动策略的估计结果。这一分支不能再冒称纯观察识别。

Appendix B 的 Algorithm 1 强调两个工程不变量：continuation prompt **字节级相同**，以及替代动作返回值必须来自真实执行；否则比较组发生未声明的二次 treatment。

### 3.5 Outcome 的选择不是无关紧要的细节

作者比较了多种结果定义。严格二元成功在这批数据里有很高天花板，许多步骤变化根本无法让 0/1 改变；精确文件集相等又会惩罚合理辅助文件。gold-file recall 的 paired sensitivity/std 达 **2.505**，高于 F1 的 **2.165** 和 binary success 的 **1.643**；98.6% 的任务在 recall 指标上保留可变化空间，而 binary 只有 73.2%。

这是很好的测量设计：**指标必须对你想研究的干预足够敏感**。但这也意味着“定位成功率”与“步骤因果估计使用的 Y”不是同一个数，后文不可偷换。

## 4. 实验坐标系：谁在什么数据上跑了多少次

主数据是 **SWE-bench Verified 派生的 499 个文件定位 episode，覆盖 12 个仓库**。每个 episode 包括 issue、修复前仓库快照、真实 Agent 轨迹和参考 patch 的 gold file set。

- Agent：Codex CLI，JSON-RPC app-server，底层模型 **gpt-5.5-0424-global**；只读沙箱、approval policy=never、每轮超时 900 秒。
- 环境：固定 base commit、locale、timezone、terminal width、hash seeds、工具输出顺序和截断点；100 个动作各重放 3 次，报告字节级一致率 1.00；所有 rollout 中未发生 context compaction。
- 数据分层：499 个任务不等于 499 个 attribution experiment。完整 next-action 表为 **488 个 episode / 7616 个决策点**；first-visit 子集为 **341 个决策点**；重放分析为 **38 个任务 / 190 个估计前缀**，每点 8 次，合计 **1901 次 continuation / 12.7 小时**；judge 主实验为 **70 个 episode**，三 judge 复验仅 **23 个共同 episode**。
- 统计：按 episode/instance bootstrap 置信区间；同轨迹内置换检验；Benjamini–Hochberg 假发现率控制（BH-FDR，q=0.10）；涉及拟合预测器时采用 leave-one-repository-out，避免同仓库泄漏。
- 主要比较：静态仓库频率、访问历史、加强版多源图邻近排序、先前工具输出路径的频率/新近性/位置、按 tool 路由的 candidate model；任务不确定性使用 replay variance；步骤归因使用 prefix/full-trace judge、零 LLM 结构规则与 noisy intervention reference。

**重要样本结构限制：** django 230/499（约 46%）；总体按 gold containment 的成功率 **93.99%**，容易出现 ceiling effect。附录显示 exact set equality 仅 15.23%，主要是额外测试文件造成，不应直接解读为“定位几乎全错”。这些细节会实质影响所有 RQ 的解释。

## 5. RQ1：到底什么最能预测 Agent 下一步？

**问题。** 看到 Agent 下一步打开一个文件，我们能否用 repository dependency graph 解释它为什么去那里？还是 Agent 主要沿着上一次工具输出列出的路径行动？

**设计。** 先对 7616 个决策点预测 (tool, object) 联合动作；再特别抽取 **341 个首次访问对象的步骤**，排除“已经去过该文件所以再去一次”的捷径。所有候选方法采用同一分母：真实动作不在候选集合里算 miss，不能靠缩小覆盖范围美化 top-k。

**Table 1：** factorized 的 P(tool)P(object) 与 routed joint candidate model 对比，后者 top-1 **0.109 → 0.150**，top-10 **0.432 → 0.484**，effective candidates **39.9 → 12.8**。tool 类型与 object 类型并非独立，互信息 0.159 nats，置换 p=5×10^-4；例如 read 更常接 path，search 更常接 free-text query。把这两种对象混成一个词表会浪费预测能力。

**Table 3 / Figure 3：** 在 first-visit 子集，强化后的 dependency graph top-3 只有 **0.058**；仅按最后一次工具输出中的路径位置排序，top-3 达 **0.326**；按整个历史新近性加权为 **0.308**。这里的图 baseline 不是弱版“只看上一个节点”：作者用**所有已访问节点**作多源邻近排序，仍明显落后。首次访问目标中 **68.9%** 曾在先前工具输出中被提及，支持 provenance 的解释。

**异质性（Figure 3b）：** handler 型动作 top-3 **0.582**，路径动作 **0.185**，新的自由文本查询仅 **0.029**。不能从总 top-k 推出所有动作都好预测；最难的其实是模型下一步要构造什么搜索 query。

**Table 2 的反直觉点：** 刚执行 search 后预测较准（top-3 **0.469**），刚 read 后仅 **0.160**；“候选集很小、熵很低”不代表可信，effective candidates ≤5 的组反而校准最差（ECE 0.0762），可能只是候选覆盖不足。

**证据强度。** 这是固定日志上不同 predictor 的关联/预测对照，不是把工具输出删除后重新运行 Agent 的因果实验。因此可以说“provenance 比 graph 更能预测下一步”，不能说“删除 graph 不影响 agent 行为”。附录 C.4 还报告 query parser 缺陷：修复后 query top-3 从 0.067 降到 0.031；增强 issue identifiers 后最好到 0.076。作者主动披露缺陷方向，增强了负结果可信度。

## 6. RQ2：图没有预测下一步，那图到底有什么用？

**问题。** Agent 访问过的文件看起来在依赖图上很集中，是否意味着它是沿图上的边一步步走过去的？

**关键 null model。** 把**同一条 episode 已访问的文件多重集保留**，仅随机打乱访问顺序。这样保持工作区域不变，单独检验时间顺序是否比随机排列更贴近图。若拿全仓库随机文件对照，会把“Agent 选了同一个模块”错当“Agent 按图边导航”。

**Figure 4a：** 去掉同节点重复后，连续步骤的 one-hop graph proximity lift **0.94**，three-hop **1.02**，same-community **1.01**，基本和同轨迹置换一样。原始相邻 one-hop 比例其实有 **0.284**，但置换预期就有 **0.301**：**0.284 不小，却没有超过正确的 null**。只有立即自重复 lift 1.47，但那是时间复用，不是图驱动。

**Figure 4b：** Agent 访问文件集合的内部边密度 **0.269**，全仓库同大小随机集合仅 **0.0087**，高出 **30.9 倍**。所以图能刻画“Agent 工作在什么代码区域”，却不能据此断言“下一步会沿哪条边走”。

另一个泄漏控制：用 graph 排名尚未访问的 gold files 时，unvisited-gold rank quantile **0.049**；从早期 prefix seed 时 **0.103**。如果把已经访问的 gold 也算进排名，会把 Agent 已知信息当成预测力。这个结果样本较小：未访问 gold 的有效实例 n=39，早期 seed n=54。

**证据边界。** 只有 **46.2%** 的 agent objects 能可靠映射到依赖图节点；free-text query 尤其不适合图化。结论是“在可映射子集和所用 graph 上，图更像 scope prior 而非局部 transition model”，不是“call graph 对所有 Agent 无用”。

## 7. RQ3：Agent 真的有重复访问偏好，还是统计假象？

**问题。** 看到工具复用率 79.1%、对象复用率 41.6%，能否据此说 Agent 有强烈回访倾向？

**设计。** 仍用保留访问多重集、只打乱顺序的 within-episode permutation。复用过的对象总数由“总步数和 distinct 数量”算术决定，因此**总体复用率本身对排列不敏感**。真正有行为意义的是重复发生在什么时间位置。

**结果。** 对象连续重复 lift **1.83**，相邻回访间隔比随机短（ratio **0.90**）；过去出现频次偏好 lift **1.70**，近期访问偏好 lift **1.74**。这些与同轨迹随机重排不同，支持局部时间聚集。

但工具连续重复 lift 只有 **1.02**，p=0.51；工具之间的转换模式却有显著结构（互信息 lift 1.13）。因此“对象会粘着访问”和“工具会机械重复”不是一回事。

**Takeaway：** 研究 trajectory 时要区分“multiset 必然导致的复用率”和“真实时间组织”。不做正确 null 的复用图表很容易制造机制故事。

## 8. RQ4：执行不确定性究竟在任务层还是步骤层？

**问题。** 如果某一步 action distribution 的熵很高，它是否就是导致最终失败的不确定步骤？能否低成本定位这样的步骤？

**设计。** 固定真实 prefix 后重复执行后续轨迹，用最终 gold-file recall 的方差测 execution uncertainty；再看它与下一动作 entropy、step position、tool type、instance identity 的关系。由于 Y 被限制在 [0,1]，靠近 0 或 1 时方差天然变小，必须先对 mean–variance 机械关系 residualize。

**Figure 5a：** action entropy 与 replay variance 的步骤级相关 **ρ=-0.088**（CI [-0.244,+0.062]），instance 聚合后 **ρ=-0.219**（CI [-0.518,+0.126]），都不能充当可靠 proxy。作者提供一个会响应的正对照（ρ=-0.425），避免把“测量器完全没灵敏度”误报为无关联。

**Figure 5b：** 消除机械 mean–variance 关系后，instance identity 的 ICC **0.640**，置换 null **0.196**，p=5×10^-4；step position 的 ρ=-0.131，tool type p=0.65。说明可观察方差主要由“是哪一个任务”解释，而非“当前走到第几步或用了什么工具”。

**对 causal step effect 的影响：** 190 个估计的步骤效应中，仅 **5.3%** 达未校正 p<0.05，**0 个**通过 BH-FDR q=0.10；投入了 **1901 次 continuation、12.7 小时**。在每点 m=8 下，中位 replay variance 为零，50.5% 的 segment 方差为零，22.9% 的 episode 所有估计增量都为零。作者因此承认：**理论上可识别 ≠ 实际预算下能定位。**

**额外负结果：** v_0 的 leave-one-repository-out AUROC **0.481**，虽然 ECE **0.015**，但只是高成功基率下近似常数预测，risk–coverage 曲线基本平坦。论文提出的 task/policy/model 三分不确定性分解仅在**已知生成过程的 synthetic test** 上验证（参数恢复相关 0.994），没有在真实轨迹中全部识别。不能把公式当成已完成的真实 Agent uncertainty decomposition。

## 9. RQ5：Full-trace LLM judge 究竟在归因什么？

这是全文最强的受控实验，也是最需要防止误读的部分。

**问题。** 让 judge 看完整轨迹并挑“最该负责的步骤”，它是否会利用未来动作/结局，系统性地把责任往后归？如果没有可信 causal-step ground truth，如何独立检验？

**设计（Figure 2 与 Figure 6a）。** 对**同一条已记录轨迹**、同一个 judge、同一 rubric，仅改变 judge 能看到的后续信息：prefix-only vs full-trace。现实世界、真实动作与终局 outcome 都不变；被随机/受控改变的是**评价器的信息集**，而不是 Agent 过去的执行。于是即使 SCAE 的 step reference 很噪，也能独立测“信息集是否导致归因偏移”。

**主结果（70 episodes）：** full-trace 相比 prefix-only，选中步骤的平均标准化位置向后移动 **+0.537**，95% CI **[+0.459,+0.610]**；**59/70** 个 episode 向后、10 个持平，sign test p≈1.1×10^-16。附录给出绝对位置：prefix-only 平均 **0.214**，full-trace **0.751**。不是两个选择都挤在中间，而是从轨迹前四分之一移到后四分之一。

**Figure 6b：judge 也不是乱猜。** full-trace judge 选中的步骤有 **90.0%** 曾操作或揭示 gold file；这类步骤在全轨迹中的基率仅 **41.3%**，富集 +48.7 percentage points。可见 judge 能识别“语义上相关的证据”。但在这类步骤内部，它又偏向更晚的位置（0.746 vs uniform 0.5）。

**Table 4：** 不用 LLM、只选“最后一次 gold-provenance 步骤”的规则，和 judge 的精确同一步一致率 **0.243**，随机基线 **0.053**；只选最后一步也有 0.171。说明 judge 有晚期/真值关联偏好，但不能简化成单一 lookup rule。

**Table 5：跨 judge 复验。** 三个模型在 **23 个共同 episode** 上的位移分别约 **+0.533、+0.434、+0.394**，每个 CI 都排除 0；位移异质性检验 p=0.181（不是证明三者等价）。但 gold-provenance enrichment 只有 2/3 显著，模型间异质性 p=0.044：**未来可见性引起的位移较稳健，judge 究竟偏爱哪类内容则有模型差异。**

**为什么不能把 judge vs SCAE 不一致当成 judge 错误率？** SCAE 在 RQ4 已证明其 190 个 step reference 没有一个经 FDR 后可信。judge 选择点与估计窗口只有 **32.9%** 可直接比较；若硬算 top-1 disagreement，97.1% 的差异几乎就是两种不同粒度随机选择器的 null。作者在 Appendix C.10 **主动撤回 D1 disagreement 作为证据**，这是非常重要的研究纪律。

**严格结论。** 论文强有力地识别了“给 judge 更多后续信息会改变它归责位置”的**评价机制层因果效应**；它并没有用可靠 ground truth 证明 full-trace judge 每次归因都是错的，也没有证明其内部一定按某个特定 collider 路径计算。论文把现象解释为 post-treatment / collider bias 有明确理论基础，但经验实验直接识别的是信息集操纵引起的位移。

## 10. 图表与附录里不该漏掉的关键负结果

**Figure 1（完整流程图）**：重点是先生成 factual trajectory，随后在相同 prefix 上 fork，而不是把多个从零开始的 run 当成同一历史的 counterfactual；图中的 entropy probe 决定采用观察还是实际干预。

**Figure 2（因果结构）**：潜在 task difficulty、当前动作、后续动作与结果之间有方向关系。比较 prefix-only 与 full-trace 的信息集，恰好在这里改变了 conditioning set。阅读时要问“谁是 treatment，谁是 post-treatment descendant”，而不是只看 judge 的文字解释。

**Figure 3 / Table 1–3**：固定动作预测任务，变的是候选构造/结构来源；最关键是 first-visit 0.326 vs 0.058、joint routing 0.150 vs 0.109、query channel 0.029。三者分别回答 provenance、联合建模和困难子类，不能互相替代。

**Figure 4**：同一个图既可在 visited-set density 上得到 30.9×，又在相邻转移 one-hop 上只有 0.94×。这不是自相矛盾，是 null 保留变量不同。

**Figure 5**：一定先看 mean–variance 约束，再看 residualized ICC；否则“成功率接近 1 导致方差接近 0”会伪装成步骤规律。

**Figure 6 / Table 4–5**：最强的是固定 judge/rubric 的信息集对照，次强是 gold-provenance 富集；最弱的是拿 noisy SCAE top-1 做正确性参考。

**Figure 7 / Table 9**：仅 3 个 episode、10 个决策点探测 positivity，其中 50% 有非零 entropy，说明 overlap **可以在同一 episode 内变化**；样本太小，不能据此估计全体动作的随机性分布，也不能把位置相关 0.072 解读成“位置绝对无影响”。

**Figure 8 / Table 11**：真实任务 v0 预测失败、synthetic 三分不确定性恢复成功，恰好是“理论工具能跑”与“真实数据可用”之间的证据断层。

**Table 12（预注册审计）**：预期 entropy 随轨迹后移下降却未出现；预期 v0 AUROC≥0.60 却只有 0.481；预期 degenerate 30–40% 实际 22.9%；D1 指标发现 null 有问题后主动退役。作者还披露早期 prefix-only judge 的截断点若依赖因果估计点，会机械制造“往后偏移”；后来改为与估计无关的固定截断比例。这个修正直接决定 RQ5 是否可信。

## 11. Baseline、公平性与效度：审稿人会追问什么？

**（1）强化图 baseline 是优点，但图覆盖有限。** 多源 graph predictor 已比简单一步邻接强；不过只有 46.2% 的 object 能落到图上。图结构对“下一步路径”弱，可能是 parser、图粒度、动作类型和信息来源共同作用，不能宣称所有 call-graph retrieval 都无效。

**（2）499 并不意味着因果估计样本也有 499。** 实际 attribution 只有 38 个 replay task、190 个估计前缀；70 个 judge episode 又是另一子样本。统计时必须按 episode 聚类，不能把同一 episode 的数千 action 当独立样本。

**（3）任务极易与 gold 定义有关。** 93.99% containment success 可能反映定位任务易、输出集合宽松；作者通过 recall outcome 缓解天花板，但如果目标换成 patch-level 精确归因，难度、方差和可测效应都会变化。

**（4）Replay 不是免费反事实。** Fork 的 Agent 内部状态是否完全由可见 log 决定？作者验证无 compaction 与字节一致的工具输出，但解码外生性不能由日志证明。替代动作的 oracle-gold 方案又引入了“答案引导的处理”，不能直接外推到自然探索策略。

**（5）信息集操纵是本文最干净的实验，但归因语义有限。** 它识别了评价器输出对未来信息的敏感性，而不是每一步对任务结局的真实 causal effect；更不能直接证明“模型受 repository plausible context 误导”。

**（6）论文主动承认的缺口。** 未实际比较训练好的 PRM 与 restart-ablation 的偏差；未在真实轨迹完成三分 uncertainty identification；未给出可检验的准确 step-local causal reference；部分实验依赖单个 Agent/model；跨 judge 仅 23 个共同任务。附录把这些缺口说清楚，比只写笼统 threats 更可信。

**（7）非因果的证据使用仍可能合理。** full-trace judge 可能很好地回答“哪一步最像相关证据”，这与“哪一步改掉后 outcome 会改善”是两个目标。不能因为后者未识别，就否定前者的产品价值。

## 12. 作者与课题组：为什么会做这种测量论文

**第一作者 Jiawei He** 的公开个人主页说明其为阿里巴巴 AI Development Engineer，曾在南京大学软件学院 Intelligent Software Engineering Laboratory 攻读硕士，研究兴趣包括 CodeSearch、AI-native 能力建设、机器学习与自然语言处理在软件工程中的结合；他参与 ACoder 项目。这与本文强调“Agent 真实工具输出、路径搜索、可重放日志”而非只做离线问答很一致。

**明确通讯作者 Xikai Yang、Dong Sun** 均在论文首页标注；本文合作单位为 Amap/Alibaba Group 与南京大学。与本文团队相邻的公开工作 **ProcCtrlBench（arXiv:2605.20251）** 由 Jiawei He、Jie Jia、Xikai Yang、Dong Sun 等参与，先把 coding-agent 过程缺陷划分为可标注的质量维度；另一项 **From Fragments to Paths** 研究工业代码库的任务级上下文恢复。可以看出团队有一条从代码搜索/工业 Agent → 过程观测 → 因果测量边界的连续研究路线。

需要注意：公开来源没有充分披露两位通讯作者各自长期独立研究履历；这里依据共同论文说明**团队层面的相关积累**，不凭空为个人添加头衔或研究成就。

作者主页：https://ehhhhjw.github.io/  
相关工作：https://arxiv.org/abs/2605.20251

## 13. 最终证据审计：证明了什么，没证明什么

**论文较有力支持：**

1. 在这批 coding-agent file-localization 日志中，先前工具输出的路径来源比静态依赖图更能预测 next object；first-visit top-3 0.326 vs 0.058。
2. 图结构对工作文件集合有很强的区域聚集信号（30.9×），但访问顺序没有显著超出保留 visited multiset 的 permutation null（one-hop lift 0.94）。
3. 真实时间复用主要体现在 object recency/frequency，而不是“工具不断重复同一个 tool”。
4. replay execution variance 在这批任务里主要呈 instance-level 结构（ICC 0.640），步骤因果贡献在 m=8、190 点预算下无法可靠定位（FDR 后 0 个）。
5. 控制 judge 的信息集后，full-trace 归因明显后移（+0.537），同时优先选择语义上与 gold 有关的步骤；这说明 semantic relevance 与 certified causal contribution 不能等同。

**论文没有证明：**

1. 没有证明任意 coding agent 的行动都不受代码图影响；也没有测试把图移除后的真正 Agent 因果效应。
2. 没有证明 step causal effects 不存在，只证明在该任务、指标与预算下**未能可靠测出**。
3. 没有证明 full-trace judge 的每个归因都错误；没有可信 causal step ground truth 可用于这样的错误率。
4. 没有在真实轨迹上完整识别 task/policy/model 三种不确定性。
5. 没有证明任意 plausible repository context 比 random context 更危险。
6. 没有直接解决 patch-level 归因、跨文件根因验证或非重放式 Agent 的外部有效性。

**读完最该记住：** 过程评估先问“在测什么”，再问“分数是多少”；graph 的 region effect 与 transition effect 必须用不同 null 分开；可重放与理论可识别不等于有限预算下可估；未来信息会改变 judge 归因，即使 judge 找到的是语义相关步骤；一个有价值的 negative result 应保留其统计功效、失败条件和被废弃的指标。

## 14. 最后才联系当前研究：对 repository-context 干预的具体启发

已同步 `JoyTrndsttr/causal-review` 的最新 `documents/研究记录.md`：截至 2026-10-02 第 73 节，五实例 random/plausible 的官方 F1 均为 0.5810；当前优先考虑“机制保持、归因偏移”，并已发现 unscoped `self.headers` FIELD 合并多个父类，不能把可达路径直接等同于决定性证据。

**启发 A：把 attribution 的两种含义彻底拆开。** 我们目前的 A（Attribution Correctness）最好明确定义为“模型最终声明的支持代码节点是否正确”，这是 **evidence attribution / semantic grounding**。它不是本文的 **step causal attribution**（替换某个 Agent 动作对最终 Y 的效应）。前者可人工核验，后者需要 prefix replay/intervention；不能因为名字相同就借用本文的因果识别结论。

**启发 B：加一个只改变 judge 信息集的低成本对照。** 同一份 response，比较“只看任务 + 当前代码证据”与“再看完整模型理由/后续工具轨迹”时 judge 给出的 A 是否偏移。这样先测评分器自身是否受未来信息影响，再谈模型是否被 plausible context 带偏。该实验测的是 evaluator information-set effect，不是原 Agent 的 context treatment effect。

**启发 C：图上同一区域不等于逐边探索。** 对 `self.headers` 的 8 父类合并问题，至少要把“节点/边是否真实有作用域”“该路径是否在可见证据中”“Agent 是否真的沿它行动”分开。GraphLocator CIG 边权本来就是 model-assigned signal，不能因图连通就当成因果作用。

**启发 D：优先 outcome sensitivity 与 common support。** 现有五例 F1 经常不变，先看 core evidence coverage、M、A、O 的可变空间。对于难以重放的 Agent trace，不应冒充估计 step causal effect；可以继续做**固定模型/任务/核心证据，只随机改变最终 context**的 treatment effect，这比从已有 Agent trace 反推内部因果更容易识别。

**启发 E：设置匹配 null。** 如果比较 graph 路径，采用固定 visited region、只打乱顺序的对照；如果比较 plausible/random snippets，则匹配 token、位置、文件数、可读性与 representation。两者回答不同问题，不能用一种 null 偷换另一种。

**最值得立刻执行的一个小实验：** 在现有 5 个 VLocBench case 上，不重跑 Agent，人工标注 M/A/O 与决定性证据覆盖 C；对同一 response 的 A 做 prefix-only/full-evidence 两种 judge 评分并计算位移/一致率。只有在评估器稳定后，再扩大 context intervention 的样本数。这样即使最后 plausible 与 random 仍然相同，也能清楚报告“treatment 没影响”还是“评价器根本测不准”。

---
*核对来源：arXiv:2608.22960v1 的完整 HTML 正文、Figure 1–8 的说明与 Table 1–12、Appendix A–D；作者主页及 ProcCtrlBench 论文首页。所有数值均按原文对应实验子样本与统计口径报告；研究启发为独立推导，不冒充作者结论。*
