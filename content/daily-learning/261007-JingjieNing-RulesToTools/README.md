# Rules to Tools：把书面科学规则变成可执行检查，真的能让 Coding Agent 修得更好吗？

> **论文**：Rules to Tools: Executable Checks for LLM Agents in Scientific Computing  
> **作者**：Jingjie Ning, Guojiang Zhao, Chen Xu, Shanshan Zhong, Xiaochuan Li, Ji Zeng, Guolin Ke  
> **机构**：Carnegie Mellon University School of Computer Science；DP Technology  
> **版本**：arXiv:2610.00313v1，2026-09-29  
> **原文**：[arXiv](https://arxiv.org/abs/2610.00313) · [PDF](https://arxiv.org/pdf/2610.00313)  
> **Tags**：`Coding Agent` `Scientific Computing` `Executable Check` `Tool Use` `SciCode` `PDEAgentBench` `Verification` `Controlled Experiment`

## 先给结论

这篇论文问了一个很具体、也很适合迁移到仓库级 Coding Agent 的问题：如果同一条科学要求已经用文字完整告诉 Agent，再额外给它一个随时可调用的、预先实现好的检查器，修复会不会更成功？

答案是“有时会，但不能只看总平均”。两个未参与早期 checker 绑定的 SciCode task-ID 队列合计从文字组的 **26/30** 提升到工具组的 **29/30**；然而原始 8 个任务中，优势几乎由 task 77 一项驱动，去掉它后其余 7 个任务的任务均值差为 0。更大的 shared-definition 队列又是 **13/24 对 13/24**。因此，论文最有价值的不是证明“工具胜过规则”，而是把“书面规则—可执行实现—运行观测—最终修复”拆开，并暴露出任务异质性、检查覆盖范围和资源成本。

对当前研究最重要的启发是：**evidence checklist 不必停在文字层；可以把其中可观测的证据条件编译为 executable probe，但必须把“工具可用”“工具被调用”“检查是否命中真实缺陷”“最终归因是否正确”分开测量。**

## 1. 论文试图解决什么问题？

科学计算程序可能成功运行，却仍违反边界条件、守恒关系、公开方程或输出契约。Agent 若只读到自然语言要求，需要自己完成三件事：把规则翻译为探针、实现探针、解释运行结果。R2T（Rules to Tools）把前两步预先完成，使 Agent 可以直接对当前候选程序调用检查器，再根据结构化测量继续修改。

论文的核心干预不是“有没有规则”，因为文字组与工具组共享：

- 完整公开任务与起始程序；
- 检查关系、探针输入、容差、适用条件和报告规则；
- 相同模型、响应数、输出 token、CPU、内存与修订预算；
- 普通 Python 执行能力。

唯一主要差异是：工具组还拿到一份已经实现的 callable checker。最终得分由独立 benchmark evaluator 给出，公开检查器本身不贡献最终分数。

这使研究问题变得清楚：当规则内容相同、Agent 本来就能自己写检查代码时，**“现成实现”这一交付形式**还能否改变修复结果和成本？

## 2. R2T 的技术对象：规则、检查器与运行观测

作者把第 \(t\) 个任务的公开规范记为 \(P_t\)，当前候选程序记为 \(c\)。一个诊断写成：

\[
d_j(c;P_t)=(\text{relation},\text{probe},\text{observation},\text{status}).
\]

其中：

- `relation`：被检查的公开要求，例如边界导数应为负、某个离散递推式成立；
- `probe`：具体输入、网格和参数；
- `observation`：在当前候选程序上计算出的残差、误差位置或异常；
- `status`：通过/失败、连续测量或不可用。

关键区别是：书面规则 \(W_t\) 与可执行工具 \(T_t\) 可以描述同一个检查规格 \(S_t\)，但真正反馈 \(y_t=T_t(c)\) 只有运行当前候选程序后才产生。论文称前者在“声明的关系与探针层面”具有 specification equivalence；它没有声称文字和工具在认知负担、调用便利性或计算成本上等价。

一个典型 PDE 残差是：

\[
r_h(u)=\frac{\lVert L_hu-f\rVert_2}{\lVert L_hu\rVert_2+\lVert f\rVert_2+10^{-12}}.
\]

这类检查返回连续测量，而不是简单二值标签。论文还覆盖径向方程的 Numerov 递推、球谐旋转与场重建、Dyson 方程残差、数值积分响应、倒易晶胞几何，以及流体方程的边界、散度和动量旋度残差。

## 3. 从 Figure 1 看完整工作流

Figure 1 把流程画成四段：公开规则 → 支持形式 → 检查并修订 → 独立终评。

文字组读规则后自行构造并运行检查；工具组直接调用 `check(c)` 取得测量。两组都继续编辑并保存程序，最终都交给独立隐藏测试。这个图强调了两个容易混淆的层次：

1. **检查器是修订期支持，不是最终裁判。** 它只暴露公开要求的测量；
2. **最终成功要求完整任务通过。** 即使公开检查全部通过，程序仍可能在未覆盖逻辑上失败。

这一点随后在 task 77 和 task 11 上成为论文最重要的反例：二者起始程序的公开检查均未报告违规，但工具组仍出现额外成功；成功轨迹后来修的是检查覆盖之外或并非起始命中的代码。因此不能把组间差异机械归因于“checker 找到了 bug”。

## 4. 实验设计：哪些比较最可信？

### 4.1 两个 task-ID 队列

主分析使用 DeepSeek-V4.1-Flash，每条轨迹最多保存 3 次修订，最多 196,608 个报告输出 token、360 CPU-budget 秒、单次公开执行 120 秒和 3 GB 内存，主要响应上限为 24。

- **8-task held-out 队列**：8 个此前没有 checker binding 的失败起始模块，每个任务、每组各 2 次续写，共 32 条轨迹。检查器在看到历史失败起点之后由作者构造，但在配对修复前冻结。
- **7-task independent extension**：使用所有剩余的 7 个、此前没有 checker binding 的失败 test-split task ID。先由一次 public-only 请求为每个任务生成候选检查，再经公开定律审查、已接受程序和定向注入缺陷验证后冻结；每组同样 2 次续写。

第二个队列的 checker 资格验证更完整：21 个草案筛成 14 个检查，14 个检查在 28/28 个用于选择的 accepted-program 运行和 8/8 个留出 accepted-program 运行中通过，并检测到 7/7 个针对性 seeded fault。但 7 个真实失败起点里只有 1 个被选中检查命中，说明这些 probe 的自然缺陷召回范围很窄。

### 4.2 其他队列不是同一种证据

论文还报告：

- 12 个任务的 shared-definition SciCode 队列；
- 5 个 development-exposed task ID 上的另一批失败起始程序；
- 12 个 PDE 任务的详细文字与工具配对；
- 经过文字 probe 失败筛选的 7 个 flow 任务；
- 历史 MDArena 与 AInsteinBench 面板。

不能把这些行直接合并为一个总体效果。尤其 flow 队列不仅交付形式不同，文字卡和工具实现的 field-capture gate 也不同；而且样本以“文字 probe 修复失败”为条件进入，对工具组有选择偏置。development-exposed 队列的任务 ID 又参与过 checker 开发，只是换了起始程序。论文在表注和附录中明确保留了这些边界。

## 5. 主结果：总数正向，逐任务却高度集中

### 5.1 两个未绑定 task-ID 队列

| 队列 | 文字组 | 工具组 | 关键不确定性 |
|---|---:|---:|---|
| 8 个 held-out task ID | 13/16 | 15/16 | 任务聚类 bootstrap 95% CI：−12.5 到 43.75 个百分点 |
| 7 个 independent task ID | 13/14 | 14/14 | 95% CI：0 到 21.43 个百分点 |
| 合计 | 26/30 | 29/30 | 3 个任务偏工具、1 个偏文字、11 个持平 |

8-task 队列里：task 17 从 1/2 到 2/2，task 37 反向从 2/2 到 1/2，task 77 从 0/2 到 2/2。Figure 2 直观显示，去掉 task 77 后其余 7 个任务的任务均值差为 0。两队列合并后，对非平局任务的双侧精确符号检验是 \(p=0.625\)。样本支持“存在任务级收益”，不支持稳定的总体优势。

还有一个很关键的指标分歧：8-task 队列中文字组和工具组的 native-step completion 都是 **95.83%**，但完整修复是 13/16 与 15/16。完整任务成败与平均子步骤进展并不等价；只报告局部检查通过率会掩盖系统级差异。

### 5.2 起始检查没有报错，为什么工具组还能多成功？

所有 16 条 held-out 工具轨迹都调用了 checker，共 34 次。task 17 的正向差异伴随起始违规；但 task 77 和 extension 中的 task 11 起始检查都没有报错。task 77 的成功工具轨迹后来用普通 Python 修复周期 wrapping 与 pressure 计算；development-exposed task 22 也是所有检查均无违规，却在工具组修复了检查覆盖之外的 translation coefficients。

因此有三种可能解释，论文数据无法完全拆开：

1. checker 的后续调用在修订过程中提供了稳定反馈；
2. checker 作为一个现成制品改变了 Agent 的搜索路径或注意分配；
3. 小样本随机性或同族任务关联造成了差异。

这些结果测到的是“完整可执行支持包”的效果，不是被命中诊断的纯中介效应。

### 5.3 交付形式消融

在原始 8 个 ID 上，作者又比较四种访问方式：

| 访问形式 | 完整修复 | Native steps | 模型 token | Public CPU |
|---|---:|---:|---:|---:|
| 书面规则 | 13/16 | 95.83% | 7.25M | 456.90s |
| 只给起始报告 | 14/16 | 98.96% | 8.68M | 521.24s |
| checker 源码，通过 Python 运行 | 15/16 | 99.48% | 8.51M | 509.39s |
| 专用命令 | 15/16 | 95.83% | 7.88M | 633.15s |

源码形式与专用命令都到 15/16，却不是逐任务完全一致；每个 cell 只有两次重复，不能据此给交付形式排名。它更可靠地说明：增益未必依赖一个特殊 tool-call API，Agent 用普通 Python 执行同一检查源码也能达到相同总成功数。

## 6. 成本不是单向下降

Figure 3 和各队列成本记录揭示：模型生成与公开执行是两类不同成本。

- 8-task SciCode：工具组输出 token **+6.8%**，public CPU **+38.6%**；
- 7-task extension：工具组总模型 token 更少，但 public CPU 从 322.53s 增至 826.73s；
- 两个 task-ID 队列合计：工具组报告输出至少低 **4.9%**，public CPU 却高 **87.3%**；
- development-exposed SciCode：报告输出降低 **22.9%**，考虑一次缺失 usage 的最保守界仍至少降低 **17.9%**；
- matched detailed PDE：23/24 对 24/24，工具组报告输出少 **31.2%**，最保守界至少少 **25.0%**，CPU 几乎相同；
- 24-response flow：工具组成功更多，但输出和 CPU 都更高。

所以“把规则变成工具更省成本”并不是普遍结论。更精确的表述是：预制检查可能减少模型自己写和解释检查代码的输出负担，却通常增加真实执行；净收益取决于任务、检查调用频率和测量成本。

## 7. 其他结果应怎样解读？

### Shared-definition 与 development-exposed SciCode

12-task shared-definition 队列是 **13/24 对 13/24**，直接说明同内容的现成实现并不保证提升。5 个 development-exposed 任务换用另一批失败起点后是 **3/10 对 7/10**，native subtask completion 从 61.27% 升至 90.48%；但这些 task ID 已参与 checker 开发，且只有 5 个任务，探索性 bootstrap 区间为 10 到 70 个百分点，不能作为独立泛化证据。

### PDE 与 flow

详细文字 PDE 几乎天花板：23/24 对 24/24，工具的主要价值是降低模型输出。Figure 6 每条轨迹约从 44.3k 降到 30.4k 输出 token，完成率基本不变。

flow 的 24-response 结果是 16/28 对 21/28，25-response 敏感性是 20/28 对 24/28。Figure 5 显示 7 个任务里 5 个偏工具、1 个偏文字、1 个持平；但该队列按文字 probe 失败筛选，且两组 field-capture gate 不同，所以它更像“不同支持包在特定筛选样本上的比较”，不能当作纯工具效应。

### 历史面板

MDArena 的文字、checker-only、文字加 checker 分别为 5/18、8/18、7/18；AInsteinBench 为 4/15、7/15、7/15。它们的支持设计、时间限制和单位定义与主 SciCode 队列不同，适合作为现象补充，不适合汇总显著性。

## 8. 重要图表给出的真正信息

- **Figure 1**：把静态规则、交付形式、运行反馈和独立终评分开，避免把 checker 当 grader。
- **Figure 2**：总体 13/16→15/16 很醒目，但逐任务图显示增益集中在 task 77；这是全文最重要的异质性证据。
- **Figure 3**：成功、模型输出和 CPU 不共用同一个方向；效率必须多指标报告。
- **Figure 4**：task 12 中 checker 报告边界斜率 +0.6455，Agent 改为从外半径向内积分，复检为 −0.01394 并通过 14/14 子步骤；它证明 checker 能嵌入修复链，但文字组两次也都成功，不能单独证明因果优势。
- **Figure 5**：flow 的任务级方向大多偏工具，但选择机制与 capture gate 混入了处理差异。
- **Figure 6**：PDE 的成功率接近天花板，收益主要体现在输出 token，而非完成率。

## 9. 作者与课题背景

论文脚注明确标注 **Jingjie Ning 与 Guolin Ke 为共同通讯作者**，不能按末位作者惯例猜测。

- **Jingjie Ning**：论文署名机构为 Carnegie Mellon University School of Computer Science。其近期连续工作包括 *Auto Research with Specialist Agents Develops Effective and Non-Trivial Training Recipes*、*Closed-loop Auto Research for Molecular Property Prediction* 与 *Auto Research for Materials*，共同主线是让 Agent 在可执行环境中提出、实施、评估并复用研究改进。R2T 把这条“闭环研究 Agent”路线收缩到一个更可辨识的干预：只增加准备好的公开检查实现。
- **Guolin Ke**：论文署名 DP Technology，个人主页称其为该公司 AI 高级副总裁，长期方向从高性能机器学习和大规模预训练扩展到 AI for Science，覆盖分子表征、三维几何/生成和蛋白结构；其早期代表性系统包括 LightGBM。R2T 与这条路线的关系，不是再提出一个科学基础模型，而是研究科学 Agent 的验证基础设施与计算权衡。

这支团队已有 Auto Research、材料研究闭环和 agent skill 相关积累，因此能同时访问科学计算任务、agent harness 和可执行评测。但也正因为 checker 由研究团队构造，作者诚实指出：原始 8-task 队列没有保留 blinded authoring log，checker authoring time 也没有记录。部署成本不能只算推理期 token 与 CPU。

## 10. 证据边界与潜在威胁

1. **任务数小，重复数少。** 主队列只有 8+7 个 task ID，每个组每任务 2 次；区间宽，符号检验不支持强总体结论。
2. **效果由少数任务驱动。** task 77 单独决定原始队列的净优势；同族 task 80 曾参与 checker 开发，存在家族层面的间接暴露可能。
3. **检查覆盖有限。** extension 中只有 1/7 个真实失败起点触发选中检查；no-violation 仍可能出现组间差异。
4. **构造并非完全盲化。** 8-task checker 在历史失败起点与上下文已经存在后编写，虽在配对修复前冻结，但没有盲化日志。
5. **部分比较混合了处理。** flow 同时改变支持形式和 capture gate，又有基于文字 probe 的选择。
6. **模型与环境有限。** 控制实验主要使用一个 DeepSeek Flash 变体；SciCode 的双环境 OR endpoint 也不同于 canonical stepwise leaderboard。
7. **未计人工开发成本。** checker 编写、审查与绑定时间未记录；真实部署中的维护成本可能超过推理节省。
8. **公开 checker 可能改变搜索而非直接定位。** 论文轨迹能证明调用发生，却不能证明最终成功经由哪一个测量中介产生。

## 11. 对当前研究的直接启发

当前研究正在区分 mechanism、attribution 与 observation，并关注“机制正确但归因错位”的 \(P(M=1,A=0)\)。R2T 提供了一个很自然的下一步实验框架。

### 11.1 把 evidence checklist 拆成三臂

对同一条 evidence requirement，可以比较：

1. **Text-only**：给出证据规则和定位要求；
2. **Source-available**：给出可执行 probe 源码，由 Agent 自行运行；
3. **Dedicated-tool**：给出固定工具接口和结构化输出。

三组共享仓库快照、任务、模型、预算、规则语义和隐藏终评。这样能区分“语义提醒”“现成实现”和“低摩擦调用接口”的贡献。

### 11.2 不只测最终 review 是否正确

建议至少记录：

- \(M\)：是否找到正确机制路径；
- \(A\)：是否把责任归到正确实体/作用域；
- \(O\)：是否执行了相关观察或 probe；
- \(C\)：检查是否覆盖真实缺陷；
- 最终评论/修复是否通过独立 oracle；
- token、工具调用次数、CPU/墙钟时间与失败重试。

尤其应报告 \(P(M=1,A=0)\)、\(P(O=1,C=0)\) 和“检查无违规但最终成功”的比例。这样才能识别工具是修正了归因，还是只改变了搜索路径。

### 11.3 用 `self.headers` 案例做最小可执行 probe

当前研究记录已确认 `self.headers` 是真实解析出的 FIELD 节点，但 unscoped identity 把 8 个父类合并。一个可执行 probe 可以固定：

- 接收 candidate review 或证据路径；
- 输出字段的声明类、访问路径、跨类碰撞集合；
- 标记“机制证据存在，但实体作用域不唯一”；
- 最终判定仍由独立、带 scoped identity 的 oracle 完成。

这与 R2T 的原则一致：probe 只测公开、可观察的中间关系，不直接充当最终 grader。最重要的对照是检查是否降低 \(M=1,A=0\)，而不只是提高某个宽松的“提到相关字段”指标。

### 11.4 冻结 checker，保留开发暴露账本

R2T 最值得复用的实验纪律是：先冻结规则、探针、容差、适用条件、pair manifest 和终评，再运行对照；同时把参与 checker 开发的任务与真正 held-out task ID 分层报告。还应补上它缺失的一项：记录 checker 的人工设计、审查和维护时间。

## 12. 最终评价

R2T 是一篇方法上克制的论文。它没有用 29/30 对 26/30 宣称普遍胜利，而是给出逐任务符号、宽区间、交付形式消融、no-violation 轨迹和 CPU 账本。最坚实的结论是：**把公开规则实现成可重复调用的检查，可以在某些科学编程任务中改变完整修复并减少模型输出，但收益不稳定、覆盖并不等于定位、执行成本会上升。**

对仓库级代码评审研究，它提供的不是现成答案，而是一种更强的干预设计：把 checklist 从提示词变成可运行的观测装置，同时用独立 oracle 守住最终归因与正确性。下一步真正该问的，不是“工具有没有用”，而是“哪类证据条件值得编译成工具、它通过什么中介改善机制与归因、又在哪些任务上只增加了计算而没有增加证据”。
