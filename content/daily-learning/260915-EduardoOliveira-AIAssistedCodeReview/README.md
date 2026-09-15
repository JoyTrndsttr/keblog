# AI-Assisted Code Review as a Scaffold for Code Quality and Self-Regulated Learning: An Experience Report

> **作者**：Eduardo Oliveira; Michael Fu; Patanamon Thongtanunam; Sonsoles López-Pernas; Mohammed Saqr  
> **Venue**：ICSE-SEET 2026  
> **DOI**：10.1145/3786580.3786956  
> **arXiv**：2604.23251

## 论文地图

这篇论文把 LLM 代码审查器直接嵌入 GitHub Pull Request 工作流，观察两个硕士软件工程 capstone cohort（2023、2024，合计超过 100 名学生）如何真正使用它。最重要的发现不是“AI 提高了代码质量”，而是：工具能稳定触发一部分后续开发行为——成功 AI review 后约三分之一 PR 出现新 commit——但跨 cohort 的工具、模型、教学和开发活动同时变化，因此这些行为证据**不能直接解释为 AI review 的因果效果**。

对 Causality for Code Review 最值得借鉴的是它的 trace-based outcome：把“AI 评论后是否发生后续 commit”定义为 Action Rate。这比问卷里的“你觉得 AI 有用吗”更接近真实行为，但仍然只是 proxy，不能证明 commit 是由 AI 评论造成，更不能证明修改正确。

## 1. 为什么要做这项研究？

课堂代码审查有三个现实问题：学生经验不足，peer feedback 容易浅；同伴批评存在社会压力；项目 deadline 下人工 review 很容易被跳过。作者因此没有把 LLM 设计成自动修复器，而是把它定位为 **Self-Regulated Learning（SRL）的 scaffold**：在学生已有 PR 流程中提供即时、结构化反馈，让学生自己判断、计划和修改。

这里需要理解三个概念：

- **SRL**：学生主动经历 planning → monitoring/evaluation → action/reflection 的循环。
- **Scaffold**：工具不是替学生完成任务，而是在关键环节提供支撑，之后仍由学生做决定。
- **Cognitive offloading**：如果 AI 直接给答案或修复，学生可能把本应自己完成的理解和判断外包给模型。

作者真正的 research gap 是：既有教育研究大量依赖 perceived usefulness/self-report，但很少把 AI feedback 与仓库中后续可观察行为连接起来，也较少报告真实部署中的 friction。

## 2. LLM-Reviewer 是怎么工作的？

整体流程是：

```text
学生创建 PR
↓
按需触发 repository-local GitHub Action
↓
LLM 按结构化 code-review checklist 检查 diff
↓
以普通 PR comment 形式发布反馈
↓
学生自己判断是否修改
↓
GitHub 中留下 comment / commit / timestamp 行为轨迹
```

Prompt 按文档、视觉表示、结构、新功能、资源、检查、接口和逻辑等类别组织 review。设计上刻意不给可直接复制的完整答案，目的是保留学生理解反馈、规划修改和实施的认知工作。

一个关键变化是：2023 使用 GPT-3.5 Turbo，2024 使用 GPT-4；同时 2024 还加入 pre-check、scope guardrail、更清晰的错误提示和更明确的 human-in-the-loop 教学。因此两个 cohort 不是“只改变年份”的干净重复实验。

## 3. 数据与 Outcome 怎么定义？

RQ1 使用 GitHub repository traces。作者把 PR 分成：

- Successful AI Review：出现符合工具模板的有效 bot review；
- Failed AI Attempt：触发了 AI，但技术上失败；
- No AI Attempt：没有有效触发。

核心指标 Action Rate 定义为：在成功 AI-reviewed PR 中，首次 AI comment 之后至少出现一个新 commit 的 PR 比例。

直觉上，它想捕捉：

```text
AI feedback
↓
学生看到/评估
↓
采取行动
```

但测量上实际只能确认：

```text
AI comment timestamp
先于
new commit timestamp
```

所以它证明的是 temporal ordering + association，不是 causation。新 commit 可能来自原计划开发、人工 reviewer、测试失败、CI、deadline 或其他并行反馈。

## 4. RQ1：学生真的会用吗？

### 设计

2023 有 29 个团队，2024 有 34 个团队。作者对 PR、commit、comment 和 AI review 状态做描述性统计，并比较两届的 adoption、failure 和 Action Rate。

### 关键结果

| 指标 | 2023 | 2024 |
|---|---:|---:|
| Participating Teams | 29 | 34 |
| Teams Using AI Tool | 27 | 17 |
| Total PRs | 581 | 1176 |
| Successful AI Review PRs | 75 | 100 |
| Failed AI Attempts | 227 | 0 |
| Actioned PRs | 24 | 33 |
| Action Rate | 32% | 33% |
| Commits in PRs | 8699 | 9436 |
| Comments in PRs | 1698 | 2872 |

最显眼的是三个现象。

第一，2024 总 PR 数几乎翻倍，但使用 AI 的团队比例反而从约 93% 降到 50%。作者推测 2023 有 novelty effect，而 2024 学生已经更熟悉 Copilot 等 AI 工具，可能更选择性地调用 reviewer。**这只是合理解释，论文没有识别这一机制。**

第二，Failed AI Attempts 从 227 降到 0。这个结果很强地说明工程 guardrail 和教学 onboarding 能消除部署 friction，但因为多项改动同时发生，不能判断究竟是哪一个组件贡献最大。

第三，两个 cohort 的 Action Rate 几乎相同：32% vs 33%。这说明成功 AI review 后，大约三分之一 PR 会继续产生 commit，而且这种比例跨两届相对稳定。但它不等于“32% 的 AI 评论被采纳”，因为作者没有把具体 comment 与具体 code change 做语义级匹配。

**RQ1 Takeaway：** AI reviewer 能在真实 PR workflow 中形成稳定可观察的 engagement，但 adoption 和 friction 强烈受工具设计、教学和 cohort 环境影响。

## 5. Figure 2 应该怎么读？

Figure 2 按周展示 PR engagement composition。两个 cohort 都随着课程 sprint 推进在 Weeks 8–12 进入 PR 高峰，而 AI reviewer 从 Week 7 的教学介绍后才正式进入工作流。

这里最值得注意的不是某一周柱子的绝对高度，而是**时间与 treatment 暴露高度捆绑**：课程阶段、deadline、开发强度、AI 可用性同时随周次变化。因此如果直接比较“使用 AI 的周”和“未使用 AI 的周”，会有严重 time-varying confounding。

对你做真实 Code Review 因果分析很有启发：review tool rollout、PR maturity、sprint stage、developer workload 都可能同时影响 Treatment assignment 和 Outcome。

## 6. RQ2：学生觉得 AI reviewer 有用吗？

RQ2 主要来自 2023 cohort 的 reflection reports 和 survey；2024 因课程调整取消了相同反思任务，因此 perception 不能做对称的跨 cohort 比较。

学生报告的正面价值主要包括：

- 帮助理解语言、代码和安全问题；
- 对 naming、formatting、documentation 等质量问题给出结构化反馈；
- 加快 debugging 和理解错误行为；
- 提供 alternative solution 和讨论起点。

调查中约 73% 认可易用性，64% 认为反馈有意义，67% 认为有帮助，80% 认为改善 coding skills，73% 认为帮助理解 good coding practices；但只有约 53% 认为改善 logical skills。

负面反馈同样重要：学生指出 system-level context 不足、response/size limit、反馈偶尔矛盾，以及过度依赖、隐私和成本风险。

**RQ2 Takeaway：** 学生总体认可即时结构化反馈，但对深层逻辑和系统上下文的信任明显弱于 style/documentation 层面。

## 7. 论文最容易被误读的地方：Action Rate 不是“采纳率”

Action Rate 的 construct validity 是全文最值得审查的地方。

如果 AI comment 后出现 commit：

```text
AI comment → commit
```

并不能自动推出：

```text
AI comment → 学生接受建议 → 正确修改
```

至少缺三层验证：

1. commit 是否真的修改了 AI 指出的代码；
2. 修改方向是否与 AI suggestion 一致；
3. 修改后质量是否提高。

因此 Action Rate 更准确的名字是 **post-feedback activity rate**。它是很好的低成本 behavioral proxy，但不能替代 semantic adoption 或 quality outcome。

## 8. 因果视角下的主要混杂

如果把 AI Review 视为 Treatment，至少有这些变量同时影响是否调用 AI 和后续 commit：

```text
PR complexity ─┬→ AI usage
               └→ later commits

Developer experience ─┬→ AI usage
                      └→ response behaviour

Sprint stage / deadline ─┬→ AI usage
                         └→ commit activity

Human review / CI failures ─→ later commits
```

此外跨 cohort 比较还有 model、guardrail、instruction、AI familiarity、PR volume 和 cohort composition 同时变化的问题。

因此论文自己称 repeated cross-sectional comparison 是合适的；把 2023→2024 的变化解释成某个单一 intervention effect 就过头了。

## 9. 这篇论文真正有价值的方法论贡献

它最大的价值不是证明“LLM reviewer 提高学习”，而是展示了一种**低侵入、可观测的真实工作流实验基础设施**：工具就在 GitHub PR 里，Treatment 暴露、评论、后续 commit 都自然留下 timestamped trace。

这比实验室里给受试者一段孤立代码更接近真实 review process，也为后续更严格的因果设计提供了基础。

如果进一步做随机化，可以把团队或 PR 随机分配为：

```text
No AI Review
vs
AI Review
```

再随机化：

```text
Diff-only Context
vs
In-file Context
vs
Repository Context
```

并记录 comment-level adoption、后续修改、人工 reviewer judgement、测试结果和 review latency，就能从 experience report 升级为真正的 causal experiment。

## 10. 对 Causality for Code Review 的直接启发

### 10.1 Outcome 不应只有 Precision / Recall

这篇给出了一个重要提醒：真实 review 的 Outcome 是链式的。

```text
Review Comment
↓
Developer Attention
↓
Developer Action
↓
Code Change
↓
Quality / Defect Outcome
```

你的研究可以把 Outcome 拆成：comment correctness、comment adoption、time-to-action、patch correctness、review burden，而不是只看模型是否命中 ground truth。

### 10.2 Context Treatment 很可能存在自选择

真实系统中开发者可能只在“觉得复杂”或“觉得风险高”的 PR 上主动请求 repository context / AI review。于是观察数据里：

```text
More Context ↔ Worse Outcome
```

可能只是因为难 PR 更容易触发 More Context。

这正是你现在一直担心的 task difficulty confounding 的真实版本。解决办法不是简单控制一个 LOC 指标，而是优先随机化 Context；不能随机时，则需要更完整的 treatment assignment model。

### 10.3 可以把 Action Rate 升级为 comment-level mediator

比论文更进一步，可以追踪：

```text
Context Treatment
↓
Review Comment Type / Evidence Grounding
↓
Developer Acceptance
↓
Code Change
↓
Final Quality
```

这会让“为什么加 Call Graph 反而下降”从单纯 benchmark performance 问题变成可解释的机制问题。

## 11. 作者证明了什么？

1. LLM reviewer 可以低摩擦地嵌入真实 GitHub PR workflow，并留下可分析的行为轨迹。
2. 两个 cohort 中，成功 AI review 后出现后续 commit 的 PR 比例稳定在约三分之一。
3. 2024 的工程与教学改进与 failed AI attempts 从 227 降至 0 同时出现。
4. 学生普遍认可 AI feedback 对 code quality、documentation 和技能学习的帮助，同时明确指出 system context、矛盾反馈和 over-reliance 风险。

## 12. 作者没有证明什么？

1. 没有证明 AI review 导致了后续 commit；只有时间顺序和关联。
2. 没有证明后续 commit 采纳了 AI comment，更没有证明修改正确。
3. 没有证明 2024 的改进由 GPT-4、guardrail、教学或任何单一因素造成。
4. 没有证明 AI reviewer 提升最终项目代码质量或长期学习成绩。
5. 没有证明教育场景的结果可直接推广到职业开发者。

## 13. 真正应该记住什么

- **真实工作流中的行为 trace 比“我觉得 AI 有用”的问卷更有价值，但 proxy 仍然不是因果证据。**
- **AI comment 后有 commit，不等于 comment 被采纳。** Outcome construct 必须逐层验证。
- **工具是否被调用本身是一个 treatment-selection 问题**；复杂 PR、开发者经验和 sprint stage 都可能是 confounder。
- 对你的研究，最值得借的是 `Context → Comment/Evidence → Developer Action → Quality` 这条机制链，而不是 32%/33% 这个绝对数字。
- 如果能在真实 PR 中随机化 Diff / In-file / Repository Context，再记录 comment-level adoption，这会比单纯在 benchmark 上比较 CG / No-CG 更接近真正的 Causality for Code Review。
