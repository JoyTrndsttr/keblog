# 每日学习执行计划

> 生效版本：2026-09-25（恢复“教学式完整精读”协议，研究进度仅影响选题与最后的研究启发）  
> 执行时间：每天 08:30（Asia/Shanghai）  
> 内容仓库：`JoyTrndsttr/keblog` 的 `master` 分支
> 发布地址：`https://38-76-161-31.sslip.io`
> Paper Pool 页面：`https://38-76-161-31.sslip.io/daily-learning/?paper=pool`
> 来源：从 `dialog.md` 的历次调整中提取；此后以 GitHub 当前版本为唯一事实源。

## 目标

每天生成一份普通中文 Markdown 技术情报简报。前半部分只保留真正需要关注的邮件、校内通知和技术动态；最后一部分完整精读一篇论文，并把结果永久归档到 Daily Learning。

## 每日输出顺序

1. **今日最值得看**：不超过 5 行。
2. **Gmail 只读整理**：按“需行动 / 科研投稿与合作 / 技术资讯 / 可忽略”分组，明确截止日期、回复对象和动作；不得发送、归档、删除、移动或修改标签。
3. **中南大学通知**：检查研究生院、计算机学院公开通知；仅在已有合法登录会话时只读检查 OA。OA 无法访问时必须写明“OA 本次未覆盖（需要登录）”。
4. **过去 24–72 小时新论文雷达**：0–5 篇，宁缺毋滥。
5. **工程与计算机新闻**：0–4 条，优先 AI Coding、Coding Agent、工具链、模型、Benchmark 和 Agent Infrastructure。
6. **公众号与中文技术媒体**：只收录有技术或科研价值、来源可核验的内容。
7. **今日建议动作**：1–3 个低成本、明确、可执行的动作。
8. **每日论文精读**：每天一篇，必须放在全文最后，是篇幅最长、信息密度最高的主体；精读之后不再追加零碎栏目。

## 与博士阶段相关的校内通知

- [中南大学研究生院通知](https://gra.csu.edu.cn/yjsytz.htm)
- [中南大学计算机学院通知公告](https://cse.csu.edu.cn/index/tzgg.htm)
- [中南大学 OA 公告](https://oa.csu.edu.cn/con/ggtz)：仅在已有合法登录会话时检查。

只保留与 2026 级计算机学院博士生直接相关的报到、账号、校园卡、宿舍、体检、档案、培养计划、选课、学籍、奖助、公派、联合培养、科研项目、学术规范、数据安全和研究生事务。近 7 天同一通知不重复，除非内容或待办发生变化。

## 每日选论文前：同步当前研究进度

在进入“新论文雷达 / 当日精读选题”之前，必须先读取 GitHub 仓库 `JoyTrndsttr/causal-review` 的 `documents/研究记录.md`。该文件可能很长，**无需每天从头通读**：优先读取文件末尾/最近新增的研究记录（必要时向前补读足够上下文），掌握用户最近的实验进展、研究问题变化、已确认/否定的假设、当前瓶颈和下一步计划。

读取后先在内部做一次简短研究诊断：当前研究主线是什么、最近发生了什么变化、目前最缺哪类证据/方法/实验。这个诊断主要用于驱动选题，默认不必在简报里单独写成长篇栏目；只有确有价值时用 1–3 句话点出。

随后再结合该进度选择“新论文雷达”和“每日精读”。推荐论文不能只按长期兴趣关键词匹配，而应优先补当前研究记录里最新暴露出的缺口，例如需要某种因果设计、context intervention、trajectory mediator、异质效应、benchmark/metric、相关 baseline 或反例证据时，优先寻找能直接帮助下一步实验或论文叙事的工作。仍需同时遵守 Paper Pool / Daily Learning 的永久去重规则和完整原文要求。


## 论文选择优先级

### 第一优先级

- Causality for Code Review。
- 因果推断、因果发现、因果效应估计与反事实分析。
- 代码审查决策、审查者或工具干预效应。
- 混杂、选择偏差、测量偏差与可信实证软件工程。
- 实验设计、构念效度和证据边界。

### 第二优先级

- 仓库级代码理解、Repository Context 与 Call Graph。
- 自动化代码审查、Agentic SE 与人机协作。
- 测试、定位、修复、代码生成与代码精炼。

### Venue 范围

优先最近一届 ICSE、FSE、ASE、ISSTA、MSR、SANER、ICSME、AIware，以及 TOSEM、TSE、EMSE 中的相关论文。用户明确指定的下一篇论文始终优先于自动选择。

## Paper Pool Markdown 结构

Paper Pool 改为“轻量入口 + 永久去重索引 + 月度详细记录”：

- `content/documents/paperpool.md`：轻量入口与维护说明，不再保存全部论文详情。
- `content/documents/paperpool_short.md`：只保存所有**已精读论文标题**，作为永久去重的首选事实源。
- `content/documents/paperpool_YYYYMM.md`：按月份保存完整精读条目；日常只读取**当前月份**文件，例如 2026-09 读取 `paperpool_202609.md`。
- 跨月时新建新的 `paperpool_YYYYMM.md`；历史月份无需日常读取。
- 当前月份的待精读候选也维护在当前月份文件的 `## 待精读论文` 中。
- 完整条目仍按 `### YYYY-MM-DD` 分组，每篇论文一个无序列表项，字段保持：简称（链接）→ Tags → 作者 → Venue/年份 → DOI/arXiv/原文 → 主题 → 一句话价值。
- 每完成一篇精读，必须同时：①向 `paperpool_short.md` 追加标题；②向当前月份文件追加完整条目；③更新 Daily Learning 索引。
- 去重顺序：先用 `paperpool_short.md` 做规范化标题快速去重；存在标题变体/疑似同文时，再读取相关月度文件核对 DOI/arXiv ID。
- 每次执行仍需重新读取 GitHub 当前版本，先取得最新完整内容，再在内存中插入/更新当日记录，然后把**完整的新文件内容覆盖写回同一路径**。这是正常的 Git 文件更新，不是危险操作；Git commit 会保留旧版本。若返回内容被截断就分段读取并拼接完整，随后直接重写。**不得再以“可能覆盖既有月度记录”“文件较长”“增量编辑不方便”为理由跳过 GitHub 发布。**
- 不得依赖 Zotero、本地 Paper Pool、自动化 memory、电脑路径或本地附件完成状态查询与去重。
- 若无法获得完整可读论文原文，不登记完整精读或永久去重。

## GitHub 单次原子提交

每日精读完成后，正文 `content/daily-learning/<slug>/README.md`、精读索引 `content/daily-learning/README.md`、`paperpool_short.md` 和当前月份 `paperpool_YYYYMM.md` 应组成**一个原子 commit**。月度 Paper Pool 的标准写法就是：读取最新完整文件 → 插入当日条目 → 用新的完整内容创建 blob 覆盖同一路径。Git commit 本身保留旧版本，因此无需担心“覆盖历史”。通常不需要修改轻量入口 `paperpool.md`。流程：重新读取最新 master/目标文件 → 创建 4 个 blobs → 基于最新 master tree 创建包含 4 处修改的新 tree → 创建一个 commit → 一次性推进 master ref。提交消息固定为 `content(daily-learning): add YYYY-MM-DD paper reading`。只有 GitHub API/权限明确报错时才能报告未更新；文本较长、需要整文件重写、返回截断但可分段读取，都不属于失败理由。临时网络/API断连时至少重试一次，并在重试前重新读取 master head。


## 每日论文精读协议（高优先级）

> **核心目标不是压缩论文，而是把论文重新讲明白。** 精读应像一位真正理解该方向的老师坐在研究生旁边，顺着作者的研究逻辑一步一步解释：为什么做、以前为什么不行、作者怎样把问题 operationalize、方法或 benchmark 如何从输入走到输出、实验为什么这样设计、每个 RQ 到底验证什么、重要图表和公式说明什么、证据能支持多强的结论、哪些地方仍然没有被证明。

### 0. 研究进度的作用边界：只能影响选题和最后的研究启发

每日运行仍需在选论文前同步 JoyTrndsttr/causal-review 的最新研究记录，但**研究进度只用于：①决定今天最值得读哪篇论文；②精读最后一节“对当前研究的启发”**。

不得让用户当前 hypothesis 反过来主导论文主体讲解。论文主体必须先忠实重建作者自己的问题、设计和完整证据链。即使某个重要 Method、RQ、Figure、Table、Ablation、Negative Result 或 Limitation 与用户当前研究没有直接关系，也不得因此省略。

尤其禁止把一篇论文写成“它对 plausible context / call graph / 当前实验有什么用”的 research note，而没有把论文本身讲完整。

### 1. 写作定位与完整性

- 每日论文精读必须是整份简报篇幅最长、信息密度最高的主体部分；资讯栏目保持简洁。
- 不设置硬性字数上限。简单论文可以较短，复杂论文必须充分展开；不得为了控制篇幅压缩重要 Method、RQ、Figure/Table、Baseline、Ablation、Failure Case 或证据边界。
- 不做普通摘要，不做逐节翻译，也不机械按 Abstract / Introduction / Related Work / Method / Experiment / Conclusion 顺序复述。应围绕“问题如何被提出、设计如何被推导、证据如何支持结论”重新组织。
- 不能只写“作者做了 A / B / C”。必须解释：为什么要做 A、A 解决什么、为什么不能直接用 B、A 的输出怎样进入后续步骤、如果没有 A 会发生什么。
- 通俗、适度口语化，但专业准确；不堆术语、不写论文腔、不像机器翻译。
- 不假设用户已经理解论文，也不把用户当完全没有基础的初学者。目标是让第一次读这篇论文、但有软件工程/LLM基础的研究生真正学会它。
- 不再输出速读导航表、最短阅读路径或“哪些章节可以跳过”。

### 2. 开头先建立完整论文地图

开头先完成三件事：

1. 用 1–3 句话说明研究问题、核心方法或设计、最重要发现。
2. 用“过去是什么情况 → 存在什么具体问题 → 作者为什么这样解决”讲清核心矛盾。
3. 列出理解全文真正必要的 3–5 个概念。概念第一次出现时，用 2–5 句话解释到足够理解本文即可，不扩写成百科。

在展开任何 Dataset、Task、Module、Metric、RQ 或表格之前，必须先讲清论文的顶层证据链：

~~~text
Research Gap
    ↓
Research Object
    ↓
Operationalization
    ↓
Method / Experiment
    ↓
Evidence
    ↓
Claim
~~~

对于 benchmark / empirical paper，尤其先说明：作者把哪个现实问题抽象成什么可测对象，再解释 dataset、task、gold label、metric 为什么是该抽象的 operationalization。对于 method paper，则先说明核心 design choice 如何从 research gap 推导出来，再进入模块细节。

### 3. 把研究动机和 Research Gap 讲透

至少回答：

- 作者观察到什么现象或现实痛点？
- 现有工作已经能做什么？
- 具体哪一步解决不了？
- 真正的 research gap 是什么？
- 这个 gap 是已有实证证据支持的事实，还是作者提出的假设或担忧？
- 不解决它会带来什么实际后果？
- 作者从 A 推到 B 是否依赖尚未验证的前提？如果有，明确指出，不替作者补圆。

Related Work 只在帮助理解 gap、baseline 或方法来源时讲，不做无意义文献罗列。

### 4. 方法或 Benchmark 构建必须做到“读者能复述它怎么跑”

先给整体文本流程图，再逐步展开。Method paper 通常按 Input → Step → Intermediate State → Output；Benchmark / Dataset paper 通常按 Raw Tasks → Filtering / Deduplication → Task Selection → Annotation / Ground Truth Construction → Validation / Quality Control → Evaluation Protocol → Metrics → Final Benchmark。

每一个重要步骤都必须回答：

- 输入是什么？
- 具体做了什么？
- 为什么必要？
- 最好用一个小例子说明它如何运行。
- 输出是什么？
- 下游哪一步使用它？
- 如果删掉或改变这一步，会影响什么？

不能把“提出三个模块”或“经过三步构建 benchmark”当成方法讲解完成。

### 5. 公式先讲直觉，再讲数学

对于核心公式：

1. 先说它想衡量或优化什么。
2. 再解释每个变量。
3. 解释变量增大或减小时结果如何变化。
4. 最后说明数学意义以及它和实验结论之间的关系。

非核心推导可以简化并明确说明，但不得歪曲。不要一上来堆公式。

### 6. 实验设置必须先整体交代，再进入 RQ

进入 RQ 前，先建立整个实验的“坐标系”，至少说明与解释结果有关的 Dataset / Split、实验单位和样本数、Models / Agent scaffolds、Baselines、Treatment / Control、Metrics，以及 prompt、token/context budget、工具权限、运行次数、温度、统计检验等会影响公平解释的关键配置。

与结论无关的超参数可以省略，但任何影响 baseline 公平性、可复现性或结果解释的设置不能略。

### 7. 每个重要 RQ 必须按“问题 → 设计 → 结果 → 含义”完整讲

对每个 RQ：

1. 问题：作者真正想问什么？为什么值得单独问？
2. 设计：实验单位、Dataset、Models、Baselines、Treatment、Metrics、控制变量和关键配置是什么？
3. 结果：给出可核验的关键数字；不要堆整表数字，但必须保留决定结论的比较。
4. 图表阅读：告诉读者表或图的行列、横纵轴、颜色或线条分别是什么，应该先看哪里。
5. 解释：作者怎样解释结果？还有没有其他合理解释？
6. 证据强度：这组实验到底能支持“相关”“有帮助”“必要”“贡献最大”还是“因果导致”？不要越级。
7. 最后给一句真正的 Takeaway。

不得因为某个 RQ 与用户当前研究关系较弱就两句话带过；不得因为某个 RQ 恰好支持用户的 hypothesis 就给它不成比例的篇幅。

### 8. 重要 Figure / Table 必须真正阅读

对重要 Figure 说明横轴、纵轴、线、颜色、柱子、区域或节点的含义和阅读顺序；指出 2–4 个最有解释力的比较、趋势或异常；解释作者想证明什么、图本身是否足以支持这个 claim、是否存在其他解释。

对重要 Table 先说明“这张表固定了什么、改变了什么”；不逐行念数字，但挑 2–4 个决定性比较；关注差距是否随模型、任务、数据集、难度、budget 或粒度变化。

默认不截图或嵌入 Figure，但必须真正读图并用文字讲明白；用户明确要求某张图时再展示。

### 9. Baseline、Ablation、Negative Result 和 Failure Case 要单独认真解释

Baseline 要说明其代表什么方法范式、为什么是合理对照，以及模型、prompt、budget、工具权限和数据是否公平。

Ablation 要说明到底删除或改变了什么变量、有没有同时改变别的东西、性能下降能够说明什么和不能说明什么。必须区分“必要”“有帮助”“贡献最大”“仅在特定场景有效”和“存在模块交互”。两个模块一起移除后的下降不能写成两个模块分别独立有效。

Negative Result / Failure Case 不得只挑支持当前故事的案例。如果作者系统报告了失败类型、反例或异常，需要说明这些结果如何限制主结论。

### 10. 主动审查证据，而不是只复述作者 Threats

在原文证据允许时主动检查实验是否真正回答 RQ、baseline 公平性、confounding / omitted variables、selection / aggregation / measurement bias、task difficulty、treatment 是否与 token 数或 representation 等变量捆绑、metric construct validity、data leakage、benchmark contamination、judge 可靠性、模型规模、prompt、token/context budget、工具权限、correlation 与 causation 边界、external validity 和 heterogeneous effects。

不要为了批判而批判；没有证据的问题不要硬凑。

### 11. 严格区分三层证据

全文必须区分：

1. 论文明确报告的事实：直接陈述，并尽可能给关键数字以及 Figure / Table / Section 来源。
2. 基于证据的合理解释：使用“从结果看可以推测……”“一种可能解释是……”。
3. 论文没有验证的内容：明确写“论文没有进一步验证这一点”。

不得替作者补实验，不得用常识把缺失证据自动补成已证明结论。

### 12. 概念教学和缩写规则

- 用户当前研究领域之外、或不应默认熟悉的专业缩写，第一次出现必须写成“全称（缩写）”，并用一句短解释其在本文中的作用。
- 容易混淆的概念可以使用紧凑对比表解释，但不滥用表格。
- 新概念教学以“足够理解当前论文”为度，不扩写成百科。

### 13. 结尾必须给真正的 Takeaway

在联系用户当前研究之前，先单独回答：

- 作者证明了什么？列 3–5 点，有证据支撑。
- 作者没有证明什么？明确结论边界，尤其区分相关性、机制解释和因果结论。
- 读完真正应该记住什么？用 3–6 条简洁但有信息量的话总结，不能只是改写 Abstract。

### 14. 最后才讨论“对当前研究的启发”

只有完成论文本体精读之后，才允许联系最新 causal-review 研究记录。重点讨论哪些变量、指标、实验单位或设计可以直接借鉴；哪些问题仍未解决；哪些观察可以转成随机、配对、析因或因果实验；哪些结论可能只在当前 benchmark / model / agent 下成立；如何扩展到 repository-level / call graph / coding agent / code review；哪些论文只能作为 mechanism precedent，不能作为现实性证据。

不强行制造创新点。只有真正相关时才联系当前研究，不再让当前 hypothesis 主导整篇论文。

### 15. 禁止选择性精读

不得因为某个重要 Method、RQ、Figure、Table、Baseline、Ablation、Negative Result、Failure Case 或 Limitation 与用户当前研究关系较弱而省略。

“与当前研究的相关性”只能决定最后“研究启发”一节的篇幅，不能决定论文本体的覆盖范围。

### 16. 发布前九问自检

精读发布前必须自检：如果用户没有打开 PDF，只阅读这份笔记，能否较完整回答：

1. 这篇论文为什么做？
2. 以前的方法或 benchmark 具体为什么不够？
3. 方法或 benchmark 从输入到输出怎样运行？
4. 每个重要 RQ 是怎样设计和验证的？
5. 主要 Figure / Table 应该怎样读？
6. Baseline 为什么这样选，比较是否公平？
7. Ablation 到底证明了什么、没有证明什么？
8. 哪些结论证据充分，哪些只是解释或推测？
9. 最重要的 limitation / failure mode 是什么？

任一核心问题仍无法从笔记中回答，则认为精读未完成，不得发布。


每篇完整精读使用目录 `YYMMDD-FirstAuthor-ShortName`，正文统一为 `README.md`。

网站直接读取这些 Markdown；计划任务同时维护论文池、索引和正文，经 GitHub commit/push 后由 Webhook 自动部署。

## 今日任务状态

| 时间 | 任务 | 状态 | 产物 |
|---|---|---|---|
| 08:30 | 技术情报简报 | 规则已同步 | 本计划定义栏目和去重流程 |