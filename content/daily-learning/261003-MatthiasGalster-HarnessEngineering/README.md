# Harness Engineering：编码智能体的“上下文工程”之外，人们实际配置了什么？

> 精读日期：2026-10-03  
> 论文：**Harness Engineering for Agentic AI Coding Tools: An Exploratory Study**  
> 作者：Matthias Galster, Seyedmoein Mohsenimofidi, Jai Lal Lulla, Muhammad Auwal Abubakar, Christoph Treude, Sebastian Baltes  
> 机构：University of Bamberg、Heidelberg University、Singapore Management University  
> 通讯作者：原文未明确标注；不按作者顺序推定  
> Venue / 年份：AIware 2026 扩展版 / arXiv v5，2026  
> 原文：[arXiv:2602.14690](https://arxiv.org/abs/2602.14690) · [HTML 全文](https://arxiv.org/html/2602.14690v5) · [PDF](https://arxiv.org/pdf/2602.14690) · [会议版 DOI](https://doi.org/10.1145/3805760.3814887) · [补充材料](https://doi.org/10.5281/zenodo.18625980)  
> Tags：Agentic Coding · Harness Engineering · Context Files · AGENTS.md · Skills · Subagents · Repository Mining

这篇论文做的不是“哪一种配置能提高编码智能体成功率”的因果实验，而是先回答一个更基础的问题：在真实开源仓库里，开发者究竟留下了哪些可版本化的智能体配置，哪些已经成为常规实践，哪些还只是工具文档中的能力。

作者分析了 2,853 个采用 Claude Code、GitHub Copilot、Cursor、Gemini 或 Codex 配置的 GitHub 仓库，识别出八类机制。最醒目的结果是：90.6% 的样本仓库有 Context Files，而 Skills 只出现在 158 个仓库、Subagents 只出现在 131 个仓库；即便已经使用 Skill，85.5% 也没有 scripts、references 或 assets 等附加资源。换言之，当前开源实践中的 “harness engineering” 大多仍是静态指令文件工程。

这与昨日精读的上下文文件消融研究形成互补：昨日论文问“给 agent 上下文文件有没有可测收益”；今天这篇论文说明“上下文文件为何值得单独研究——它确实是目前最普遍的配置形态”。但采用率不能替代效果证据，二者必须严格分开。

## 一、先把三个层次分清

论文的核心概念链条是：

```text
模型（model）
  ↓ 被软件层包裹
智能体 harness：组装每轮输入、暴露工具、维护状态、驱动 agent loop
  ↓ 可由仓库内制品定制
Context Files / Skills / Subagents / Hooks / Rules / MCP ...
```

作者把 **context** 定义为一次模型调用的完整输入；**context engineering** 是设计 harness 在运行时组装什么输入；**harness engineering** 则更宽，包含对模型外围软件层的定制，不只改变文本上下文，也能改变工具连接、生命周期脚本、并行代理和执行规则。

这一区分有用，因为 `AGENTS.md`、一个带脚本的 Skill 和一个 MCP 连接并不是同一种干预：前者主要改变模型看到的指令，Skill 可能增加可调用工作流，MCP 则改变智能体能访问的外部能力。如果把它们都叫“context”，实验会混淆信息、行动空间与执行控制。

论文进一步区分：

- **配置机制（mechanism）**：定制工具或 agent 行为的方式，例如 Context Files、Hooks；
- **配置制品（artifact）**：机制在仓库中的具体文件或目录，例如 `CLAUDE.md`、`.claude/agents/reviewer.md`；
- **智能体工具（agentic AI coding tool）**：Claude Code、Codex 这类承载完整 agent loop 的产品；
- **细粒度工具（tool）**：由 agent 调用的 Bash、搜索或测试等有界能力。

## 二、研究问题与方法链路

论文有三个研究问题：

1. 五类 agentic coding tools 提供哪些仓库级配置机制？
2. 开发者如何采用这些机制，它们怎样共现、随时间怎样增长？
3. 跨工具都存在的 Context Files、Skills，以及格式相近的 Subagents，实际被怎样组织？

整体流程是：

```text
SEART GitHub 初始样本
    ↓ 许可证、非 fork、至少两位贡献者、创建和活跃时间等过滤
36,184 个候选仓库
    ↓ GPT-5.2 根据 README 判断是否为 engineered software project
32,564 个仓库
    ↓ clone 后按文件名与路径启发式检测配置制品
2,926 个初始命中仓库
    ↓ 去除 vendored、空文件、误收集目录等
2,853 个最终仓库
    ↓ 分析采用率、共现、创建顺序、引用网络与资源结构
```

采样要求仓库非 fork、有许可证、至少两位贡献者、在 2024-01-01 前创建，并在 2025-06-01 后仍有提交。创建时间门槛用于降低“仓库本来就是围绕新工具搭建”的影响；活动门槛用于去掉休眠项目。语言限定为 GitHub 常见的十种语言。

“engineered project” 分类依赖 README 中的项目目的以及构建、测试、维护等工程实践。GPT-5.2 将 32,564 个判为 engineered，1,416 个判为非工程项目，2,204 个标为 unsure 并排除。这里的 LLM 不是研究对象，而是样本筛选器；因此它的误差会直接改变后续总体。

## 三、八类配置机制：不要把所有文件都当成上下文文件

作者系统审查五种工具的文档，再由另外两位作者交叉核对，得到八类机制：

| 机制 | 作用 | 典型仓库制品 |
|---|---|---|
| Context Files | 每次会话加载的项目级 Markdown 指令 | `CLAUDE.md`、`AGENTS.md`、`GEMINI.md`、Copilot instructions |
| Settings | 项目级 JSON/TOML/YAML 行为配置 | `.claude/settings.json`、`.codex/config.toml` |
| Skills | 可按需调用的知识与工作流 | `*/skills/<name>/SKILL.md` |
| Subagents | 在独立上下文中工作的专门代理 | `.claude/agents/*.md`、`.cursor/agents/*.md` |
| Commands | 用户触发的预定义 prompt 快捷方式 | `.claude/commands/`、`.cursor/commands/` |
| Hooks | agent 生命周期特定节点执行的脚本 | settings 中的 hook 或 hooks JSON |
| Rules | 约束 agent 行为的系统级规则 | `.codex/rules/`、`.cursor/rules/` |
| MCP | 通过 Model Context Protocol 连接外部工具或数据 | `.mcp.json`、工具设置文件 |

只有 Context Files 与 Skills 在论文检查时被五种工具全部支持，没有任何工具同时覆盖八类机制。这个结果说明生态正在趋同，但还没有统一的“完整配置栈”。它也提醒基准研究：若只保存最终 prompt，可能漏掉 Hooks、Rules、MCP 和 Subagents 对轨迹的影响。

## 四、样本长什么样

最终 2,853 个仓库中：

- Claude Code 配置出现在 1,297 个仓库；
- GitHub Copilot 为 957；
- Cursor 为 327；
- Gemini 为 175；
- Codex 的工具专属配置仅 4 个；
- 另有 493 个仓库只使用工具无关的 `AGENTS.md`，没有其他工具专属制品。

70.6% 的仓库只配置一种工具，10.3% 配置两种，1.8% 配置三种或更多；17.3% 属于上述 “仅 AGENTS.md” 类别。最常见的多工具组合是 Claude + Copilot（167），其次为 Claude + Cursor（144）。Cursor 仓库中有 44.0% 同时配置 Claude。

语言分布也不是总体 GitHub 样本的缩影。初始 36,184 个仓库以 Python 为首，而采用 agentic 配置的 2,853 个仓库中 TypeScript 占 25.8%，Python 16.8%，Go 14.7%，C# 8.0%，Java 7.8%。这意味着采用模式与语言生态、工具偏好和项目类型缠绕，不能把工具之间的原始比例直接解释为工具自身吸引力。

## 五、RQ2：静态 Context Files 占据绝对主导

Figure 3 显示，每种工具中 Context Files 的采用率都在 61.5% 至 100% 之间。除两个工具特有模式外——72.8% 的 Cursor 仓库采用 Rules，62.3% 的 Gemini 仓库使用 Settings——Claude、Copilot、Cursor 与 Gemini 的其他任何机制采用率都没有超过 20%。Codex 只有 4 个专属样本，不足以稳定描述。

从整体看，2,853 个仓库中有 2,586 个包含 Context Files，占 90.6%；共检测到 4,768 份 Context Files：

| 文件类别 | 文件数 | 占全部 Context Files | 覆盖仓库数（在 2,586 中） |
|---|---:|---:|---:|
| `CLAUDE.md` | 1,640 | 34.4% | 1,187（45.9%） |
| `AGENTS.md` | 1,508 | 31.6% | 1,021（39.5%） |
| Copilot instructions | 1,393 | 29.2% | 930（36.0%） |
| `GEMINI.md` | 154 | 3.2% | — |
| `.cursorrules` | 73 | 1.5% | — |

不同语言中的 Context File 覆盖率都很高（88.5%–96.2%）。多数仓库只有一两个文件。`.cursorrules` 已被 Cursor 弃用并建议迁移到 `AGENTS.md`，所以横截面中的低数量也包含规范迁移因素。

### 共现不是独立选择

作者用卡方检验和 Cramér's V 分析 28 对机制，并做 Benjamini–Hochberg 校正。Settings 与 Hooks 的关联最强之一（V=0.36），很大程度是因为 Hooks 常写在 Settings 文件中；Subagents 与 Commands、Skills、Hooks 也呈正关联。Context Files 与 Rules 的共现反而低于独立期望：观察到 122 个，期望为 216 个，V=0.41。

这不能解释成“二者互相排斥”。机制是否共现首先受工具支持矩阵影响，例如 Claude 并不支持 Rules。这里的 V 混合了开发者偏好与产品架构。

### 时间趋势

Figure 4 的累计曲线显示，Context Files 持续快速增长，而 Skills 和 Subagents 增长缓慢。它描述的是截至 2026 年 2 月的制品出现史，不是活跃使用量，更不是带来的生产力收益。

## 六、RQ3：AGENTS.md 正在成为互操作入口

在包含多类 Context Files 的仓库里，作者分析了创建顺序和文件间引用。`CLAUDE.md` 通常先出现，随后加入 `AGENTS.md`。在 594 个多文件仓库中，最常见序列是两者同日创建（142），其次是 `CLAUDE.md → AGENTS.md`（102）。

作者识别了三种“引用而不复制全文”的方式：只有一行直接指针、带 2–5 行解释的短引用、以及简短摘要后再指向主文件。全文描述中报告了 497 个引用关系；Figure 7 在扩展后的网络统计为 514 对，读者应注意两个数字对应的统计口径或版本表述并不完全一致。

最稳定的结构是：`CLAUDE.md` 有 344 个外向引用，其中 301 次指向 `AGENTS.md`；`AGENTS.md` 收到 353 个入向引用。再结合 493 个只用 `AGENTS.md` 的仓库，作者将其解释为一种由开发实践推动、而不是由单个厂商强制的跨工具标准化。

这个解释有支持，但仍是观察性推断。文件创建顺序不能证明开发者的主观动机；迁移工具、模板生成和 monorepo 合并都可能产生相同序列。

## 七、Skills：名义上的可执行工作流，现实中的静态说明居多

论文找到 158 个含 Skills 的仓库，共 601 个 Skill。每仓库平均 3.8 个，中位数 2，最大 28；分布明显右偏。只有 29 个 Skill（4.8%）超过规范建议的 500 行。

Skills 可以带三类附加资源：

- `scripts/`：Python、Bash、JavaScript 等可执行代码；
- `references/`：按需读取的技术资料、模板或结构化数据；
- `assets/`：文档模板、图片、schema、查找表等静态资源。

但 601 个 Skill 中，514 个（85.5%）没有任何附加资源；单独带 `references/` 和单独带 `scripts/` 的各 35 个（各 5.8%）；同时有 scripts 与 references 的只有 11 个（1.8%）；assets 仅见于 4 个（0.7%）。

因此，把“使用 Skill”直接等价为“采用了可执行、渐进披露的工作流”会高估实践成熟度。绝大多数 Skill 更接近有触发条件的静态指令包。论文的目录扫描能证明资源是否存在，却没有审查脚本是否真正被调用、成功运行或产生收益。

## 八、Subagents：存在配置，但尚未观察到持久记忆

作者在 131 个仓库中找到 450 个 Subagent。每仓库平均 3.44 个，中位数 2，最大 17，同样呈右偏分布。Subagent 与 Skill 都使用 Markdown/YAML 描述，但关键区别是：Skill 在调用者的上下文中执行，Subagent 在自己的上下文窗口中工作，再把结果返回父代理。

Claude Code 的 Subagent 支持持久目录，用于跨交互积累调试知识等记忆；样本中没有仓库提交这种 memory 文件。这只能说明“仓库中未观察到版本化的持久记忆”，不能排除本地未提交、运行时生成或私有环境中的使用。

## 九、Figure 与 Table 应怎样读

### Table 1：配置机制矩阵

它是全文的构念基础。先看“机制作用”，再看“什么路径代表采用”。表格证明不同工具对相似概念使用不同文件约定，也暴露检测的边界：基于文件系统的研究看不见只在 Web UI 中配置的能力。

### Figure 3：各工具机制采用率

这张图最适合生成假设，而不是排工具名次。工具的发布时间、支持机制和用户群均不同；Codex n=4 尤其不能与 Claude n=1,297 横向比较。

### Figure 4：累计采用曲线

它支持“静态文件扩散快于 Skills/Subagents”，但右端只是 2026-02 的快照。新规范推出时间不同，曲线斜率不能直接当作开发者偏好。

### Figure 5：每仓库制品数量

Context Files、Skills、Subagents 都以一两个制品为主。这里证明的是配置广度较浅，不是文件内容浅；一个单独文件可能很复杂。

### Figure 6 与 Figure 7：创建顺序和引用网络

两图共同支持 `AGENTS.md` 成为共享入口。但更强的结论需要分析 commit message、PR 讨论或开发者访谈，确认是为了互操作，而非模板、复制或重构。

### Table 3：仓库元数据

Cursor 仓库更年轻、更大；Gemini 仓库贡献者和提交数更多；仅 `AGENTS.md` 仓库更小。作者报告 Mann–Whitney U、BH 校正与 Cliff's delta，这是规范做法。但大多效应很小，统计显著不等于实际差异巨大；Codex 的四仓库结果必须忽略为描述性异常。

## 十、有效性威胁：论文自己指出了什么

### 构念效度

路径存在不等于工具在活跃使用，`AGENTS.md` 也可能服务于非编码代理。作者用三组检查缓解：限制为工程软件仓库；扫描 AI 署名 commit，在 2,853 个仓库中有 2,058 个（72.1%）发现可归因于相关工具的 AI-authored commit；并清理 vendored、空文件和误匹配。

不过 72.1% 是保守下界，也是样本级佐证，不是每个具体配置文件都被执行的证明。Copilot、Cursor、Gemini 的部分文件还同时服务聊天和 agent 模式，研究无法隔离是哪种模式在使用。

### 内部效度

“engineered project” 只运行一次 GPT-5.2 分类，2,204 个 unsure 被排除。作者测试过 GPT-5-mini、GPT-5-nano 与 GPT-5.2，并做 spot check，但没有正式报告随机样本上的人工一致率、precision/recall 或第二模型复核。

短文件审查更扎实：作者用 Claude Code Opus 4.6 high effort 检查全部 451 个不超过十行的文件，396 个有实质配置内容，51 个只是引用，4 个处于边界。可复现材料公开，但这仍是单模型辅助审查。

### 外部效度

样本只来自 GitHub 开源项目，排除了单人项目、无许可证项目、休眠项目和不在十种语言范围内的项目，也看不见企业私有仓库。所有结论是 2026 年 2 月快照；对高速演化的工具生态而言，不能把比例当成长期常数。

## 十一、论文证明了什么，没有证明什么

### 较充分证明

1. 截至采样时点，五种编码工具可以映射到八类仓库级配置机制，Context Files 与 Skills 是唯一跨五工具均有的机制。
2. 在严格筛选后的 2,853 个开源仓库中，Context Files 极其普遍，Skills 与 Subagents 的仓库覆盖明显更低。
3. `AGENTS.md` 既大量单独出现，又在跨文件引用中成为主要目标，构成跨工具入口的有力观察证据。
4. 大多数 Skills 没有附加资源，多数 Skills/Subagents 仓库只定义一两个制品。
5. 不同工具生态形成不同配置组合，机制共现受到产品支持矩阵约束。

### 没有证明

1. 没有证明 Context Files、Skills、Subagents 或更多配置会提高任务成功率、效率或代码质量。
2. 没有证明 `AGENTS.md` 是因果意义上的最佳起点；“natural starting point”是基于普及度与互操作性的实践建议。
3. 没有证明路径存在等于制品被加载、遵循或执行。
4. 没有证明复杂 harness 优于简单 harness，也没有评价配置冲突、陈旧或安全风险的实际后果。
5. 没有代表企业、闭源、个人试验仓库，且无法把 2026-02 的比例外推到快速变化的未来。
6. 没有分离工具选择、语言、仓库规模与配置采用之间的因果方向。

## 十二、作者与研究团队背景

第一作者 **Matthias Galster** 是 University of Bamberg 实验软件工程讲席负责人。其官方主页列出的长期方向包括需求工程、软件架构以及软件开发过程与实践。这篇论文延续的是“把新开发实践变成可观察、可比较的软件工程现象”的路线：先定义构件，再从仓库制品建立经验基线。

合作者分布在 Heidelberg University 与 Singapore Management University。Sebastian Baltes 领导 Heidelberg 的 Software Engineering Group，长期聚焦 empirical software engineering 与 software analytics；Christoph Treude 的研究聚焦经验与自动化软件工程、软件开发中的人机协作、AI 辅助工作流和可复现性。团队此前还完成了开源软件中的 Context Engineering 研究、AGENTS.md 效率研究，以及本文配套的配置制品数据集；因此本文并非一次孤立文件计数，而是一个围绕“可版本化 agent 配置”持续扩展的研究程序。

原文没有以星号、脚注或 correspondence 字段明确标注通讯作者。虽然末位作者具有相关课题组背景，也不能据此推定通讯身份。

## 十三、与当前研究主线的关系

当前主线关心 repository context 是否为任务提供决定性机制证据、模型为何会被 plausible-but-non-decisive context 误导。本文提供的是上游“处理变量清单”与现实采用分布，而不是下游效果估计。

它带来四点直接启发：

1. **把 treatment 从“有/无上下文文件”扩展为机制向量。** `Context Files`、`Rules`、`Skills`、`Hooks`、`Subagents` 与 `MCP` 会分别改变信息、约束、行动和状态。若只用一个 binary context 指标，会发生处理定义过粗的问题。
2. **优先研究现实高频 treatment，但不要把高频当有效。** Context Files 覆盖 90.6%，适合先做外部效度高的干预；昨天的两代理消融却显示它们未稳定提高隐藏测试通过率。组合起来的结论应是“重要且未证实”，不是“普及所以有用”。
3. **显式建模重叠和冲突。** 497/514 个引用关系与多文件创建序列说明，仓库上下文常是图而非单文件。实验需要记录主文件、转发文件、重复段落、作用域与优先级，否则会把同一信息重复注入或引入冲突。
4. **把存在性、可达性、实际使用与效果拆开。** 本文测量 artifact presence；Skill Following 类研究测 actual use；上下文消融测 outcome effect；当前因果研究还需测 evidence attribution。四层不能相互替代。

可将后续数据表扩为：

| 层 | 推荐变量 | 作用 |
|---|---|---|
| Presence | 是否存在八类机制、文件数 | 描述 harness 供给 |
| Reachability | agent 是否会加载/触发该制品 | 排除“存在但不可见” |
| Usage | 轨迹是否引用、调用、执行 | 区分 exposure 与 uptake |
| Attribution | 输出是否真正依赖其中证据 | 识别 plausible 干扰 |
| Outcome | 成功、成本、回归、安全 | 估计净效果 |

对最近 VLocBench 的 FIELD seed 审计尤其重要：一个 seed 或配置文件存在，只说明搜索起点或潜在上下文可用；它不等于任务真值可达，更不等于模型的最终判断由它决定。本文的 presence study 恰好提供了一个反例，提醒我们不要把仓库里“有某种制品”升级成“制品发挥了作用”。

## 十四、真正应该记住什么

1. Harness engineering 比 context engineering 更宽：它还包括工具连接、生命周期脚本、规则、技能和子代理。
2. 真实开源采用仍高度集中在静态 Context Files；90.6% 与 5.5%（Skills 仓库占 2,853 的比例）之间存在数量级差异。
3. `AGENTS.md` 的价值首先是互操作入口：493 个仓库只用它，且它是跨文件引用的主要汇点。
4. “有 Skill”通常不意味着“有可执行工作流”：85.5% 的 Skill 没有附加资源。
5. 这是一项采用与制品结构研究，不是效果研究。任何“配置提升 agent 能力”的表述都超出证据。
6. 下一步最重要的问题不是再数文件，而是连接 presence → reachability → usage → attribution → outcome，并用受控实验识别每种机制的真实增益与副作用。
