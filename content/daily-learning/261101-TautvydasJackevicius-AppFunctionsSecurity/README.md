# The Agent in the Middle: A Security and Privacy Analysis of Android AppFunctions

> 计划外精读｜2026-11-01｜**Proceedings on Privacy Enhancing Technologies（PETS）2027(1)**  
> 作者：Tautvydas Jackevičius、Aniketh Girish、Vinuri Bandara、Guillermo Suarez-Tangil、Juan Tapiador、Narseo Vallina-Rodriguez  
> 机构：IMDEA Networks、Universidad Carlos III de Madrid；论文没有明确标注通讯作者，不根据作者位置推断。  
> 原文：[IMDEA 机构论文页面](https://dspace.networks.imdea.org/handle/20.500.12761/2072)｜[官方研究工件](https://github.com/appfunc/app-functions-security-analysis)  
> Tags：Android / AppFunctions / Agent Security / Permissions / Confused Deputy / Prompt Injection / Cross-App Collusion  
> 本文根据完整 20 页论文整理；明确区分作者验证结果、教学比喻、后续研究假设。

## 一、从一个 AI 秘书的故事理解研究问题

把 Android 想象成一栋办公楼，每个 App 都有自己的房间和门禁。普通天气 App 没有位置权限，按理不能直接请求系统提供精确坐标。现在公司请来一个能够进入多个房间的 AI 秘书：用户问“今天天气如何”，秘书用自己的能力得到位置，再将坐标传给天气 App 的 `getWeather(location)`。天气 App 没破解位置权限，却最终收到了位置。

AppFunctions 让 Android 原本孤立的应用通过一个具有特殊权限的 AI Executor 协作。**核心研究问题是：如果每一次单独调用都符合 Android UID 和权限规则，是否就能保证 Agent 编排的整体数据流符合用户意图？** 这篇论文的答案是：未必。作者提出系统级的攻击模型，验证七种攻击，并调查真实 App 的部署与防护情况。

## 二、论文为何值得读

PETS 是隐私与系统安全研究的发表渠道。本研究由 IMDEA Networks 及 UC3M 团队完成，第一作者为 Tautvydas Jackevičius。团队的 Android 应用安全、权限与生态测量背景与该问题契合。但场所和团队背景只是判断研究主题的线索，论文结论仍需要实验支持。文章没有明确通讯作者。

从 Agent 安全角度，作者把已有 Prompt Injection 和 confused-deputy 问题放入 **Android 系统级执行权限、Binder、应用身份、函数参数和数据来源**的具体机制中。对于探索跨 App 共谋尤其重要：作者明确没有研究“多个恶意工具共谋”；这是后续工作可探究的空白，还不是已证明的攻击。

## 三、先补 Android 基础：Sandbox、Permission、IPC

传统 Android 应用通常各自运行在独立 Linux UID 和进程里，彼此的私有文件不能直接访问。权限模型控制位置、相机、联系人等敏感接口。允许合法通信的 Intent、Binder、Content Provider 等 IPC 机制依然需要经过身份、权限和接口约束，后台执行还有独立限制。

**图 1（论文第 3 页）的 AppFunctions 工作流：**

```text
用户提出自然语言请求
   ↓
AI Agent / Executor（具有 EXECUTE_APP_FUNCTIONS 的特权调用者）
   ↓ 查询 AppSearch 维护的函数元数据
选择 Function，生成调用参数
   ↓
AppFunctionManager → Android system_server → Binder
   ↓ 系统验证调用者身份及函数状态
Provider 的 AppFunctionService（在 Provider 自己的 UID 下执行）
   ↓
结构化结果返回 Executor，可能触发下一次工具调用
```

Provider 可以用 Jetpack 的 `@AppFunction` 注解或 XML + Service 暴露功能，注册的函数签名、参数、返回类型及开发者描述被系统索引。**提供 Function 的普通 App 不必拥有 `EXECUTE_APP_FUNCTIONS`，能跨 App 调用它的 Executor 则需获得特权授权。**

关键的不对称性：Provider 函数体仍在自身 UID 下运行，但 Executor 能把用自己权限取得的敏感数据填进参数，间接交给无此权限的 Provider。这种传递未必违反单次调用的内核权限检查，却可能违反端到端用户授权。

与 MCP 比较：MCP 是平台无关的本地或远端 client-server 协议；AppFunctions 则是 Android 设备内的系统发现/调用机制，直接受到 Binder、UID、Android 沙箱影响。MCP 有 sampling 机制，AppFunctions 本身没有供 Provider 在一次活跃调用中递归请求 Agent 推理的等价机制。

## 四、威胁模型：攻击者有多大权限

攻击者控制一个普通低权限 Provider，可以决定 Function 的 Schema/描述、返回文本及自己进程内允许的操作；通常只需要 INTERNET 等少量权限。用户正常使用未被攻击者控制的 Executor；攻击者不能修改 Agent 系统提示词、Android 系统或其他正常 App，也不能绕过普通权限检查。论文把风险分成隐私泄露、访问控制/进程隔离假设失效、LLM 决策完整性攻击。

研究中的“权限突破”很多是**借助有权限的中介把数据转交给无权限 App**，并不意味着恶意 App 获得系统 UID、Root 或真正破解了 Android 内核。

## 五、七种攻击的机制与证据：第 7 页 Table 1

### A1 Permission Re-delegation（权限再委托）

实验室天气 Provider 没有定位权限，却注册 `getWeather(location: String)`；用户问天气，Executor 用自己的定位能力取坐标并传给函数。真实三星 S26 的 Figure 3 展示了 Gemini 帮用户创建带精确当前位置的日历事件，即使 Calendar 本身没有位置权限。这里用户明确要求使用位置，故真实案例主要证明权限相关数据经 Agent 转交的**可能性**，不应直接称为恶意窃取。

### A2 Confused Deputy（提供者选择混淆）

正常 App 与恶意 App 分别暴露同名 `getFunFact()`，恶意方用相近的包名及元数据竞争 Agent 的选择。实验室 Executor 有时选择恶意实现，证明工具发现与选择存在歧义；没有在商业 Gemini 上验证任意恶意 Provider 冒充正常 Provider。

### A3 Information Overdisclosure（过量信息披露）

恶意天气函数通过参数描述索取邮箱、电话号码、设备信息等完成天气任务并不必要的数据。实验室 Agent 可能额外提供这些信息。与 A1 任务可能需要的位置不同，A3 更强调违反最小数据披露原则；未在生产设备完整验证。

### A4 Installed-App Fingerprinting（已安装应用指纹采集）

恶意 Function 返回正常结果的同时，秘密枚举其权限及包可见性范围内的 App，再向受控端传输列表和设备标识。作者修改 Samsung Notes 的 `findNotes`，在真实设备复现了正常调用伴随的隐蔽副作用。注意，AppFunctions 本身并不会赋予任意 Provider 查看全部安装包的能力，它仍受到 QUERY_ALL_PACKAGES 或 `<queries>` 等规则约束。问题在于 **Function 内部的实际副作用可能超出其 Schema 宣称的业务目的**。

### A5 Prompt Injection via Result（结果注入）

实验室的 `getEvents()` 附带伪造系统指令，诱使 Agent 启用蓝牙。商用环境则将攻击文本嵌入修改后 Samsung Notes 的返回结果，使 Gemini 额外调用搜索/定位相关能力并创建包含笔记摘要及大致位置的新笔记（Figure 4）。这是把低可信工具输出误提升为行动指令。实验室“开启蓝牙”和真实设备“创建额外笔记”不能混写成一个结果。

### A6 Context Poisoning（上下文污染）

恶意 `getReminders()` 返回提醒，同时要求 Agent 在以后用户每次发言时再次调用 Function，并填充 `verifyMessage`。实验室中该要求污染了后续会话状态。它与 A5 的区别在于跨轮次的持久影响；没有在生产环境验证。

### A7 Schema Injection（Schema 元数据注入）

`setTimer()` 的恶意函数描述在**调用之前**被放进 Agent 工具发现上下文，可能影响其选择和执行行为。A5/A6 需要先调用函数再读到恶意返回值，A7 注册阶段即可形成入口。只在实验室成功，不能据此认为商用 Gemini 会接受任意恶意工具 Schema。

| 攻击 | 自建实验室 | 商用 S26 / Pixel 10 Pro |
|---|---|---|
| A1 权限再委托 | ✓ | ✓ |
| A2 提供者选择混淆 | ✓ | 未验证 |
| A3 过量披露 | ✓ | 未验证 |
| A4 应用指纹采集 | ✓ | ✓ |
| A5 结果注入 | ✓ | ✓ |
| A6 上下文污染 | ✓ | 未验证 |
| A7 Schema 注入 | ✓ | 未验证 |

**7/7 与 3/7 是“验证了几类案例”，不是随机多次运行得到的成功率。**

## 六、实验系统为什么分成两部分（§4）

**生产环境**：Samsung Galaxy S26 与 Pixel 10 Pro。当时商用 Gemini 仅索引 Samsung Notes、Calendar、Clock、Reminders 等少量受信任 Provider，并实施内部 Schema-gating，不能轻易接入随意开发的第三方 App。作者通过提取、反编译、修改、重新签名安装 Samsung Notes，保留既有 AppFunction 入口研究 Gemini 的实际行为。成功调用不代表远程攻击者能无条件替换用户手机中的 Samsung Notes；替换 App 是重要实验前提。

**实验室环境**：作者自建 Provider 和可迭代调用 Function 的 Executor，后者以 **Gemini 3.1 Flash Lite（Google API）**作为推理引擎，读取 AppSearch 元数据，并模拟位置、网络、蓝牙等特权工具。设备为 Root 的 Pixel 10 Pro；Root 主要为了让自建 Executor 获得 `EXECUTE_APP_FUNCTIONS` 保护权限。七类攻击都能在这个受控环境开展，但其安全策略不等于商用 Gemini 的完整策略。

**证据边界**：真实 Framework + 自建 Executor 可以验证某个安全机制与攻击原语的存在；不能自动外推到所有 OEM AI 助手及其白名单、确认和过滤逻辑。

## 七、25 万 APK 生态调查：为什么要做（§5）

攻击案例说明“机制上可能”，生态测量才帮助回答“现实中暴露了哪些条件”。

论文从 AndroZoo 获取 **248,557 个 Google Play APK**，结合 S26 / Pixel 10 Pro 的预装应用，利用权限声明、XML 文件、DEX 字符串等特征筛选出 **34 个候选（17 个预装）**；再通过 jadx 反编译、人工确认与动态实验，最终确认 **17 个实现 AppFunctions 的预装 App**。该样本中没有确认完全实现 AppFunctions 的普通 Google Play 候选，不等于全商店任何时候都不存在这样的 App。

作者以 Google 六条开发建议为审计参照（第 9 页 Table 2）：函数应用于自然语言交互有优势的动作、仅暴露任务必需数据、隐私需用户同意、破坏性操作需确认、默认禁用并显式启用、长耗时函数用 suspend 等。Table 3 对 17 个 Provider 逐项记录违背情况。

主要结果：**16/17 至少违背一条建议；67% 的被检查权限存在 Schema-Permission Gap**。这个 gap 是 Provider 持有的权限能力与 Function Schema 描述所暗示能力之间的差异，是潜在风险条件，并不能等同于“67% 的权限已经存在可利用漏洞”。

### 第 5.5 节三个真实 App 案例

- **Samsung Notes**：读取笔记的 `findNotes/getNotes` 会检查 `KeyguardManager.isKeyguardLocked()`，锁屏时阻断读取；`createNote` 不做同样检查，可在锁屏状态创建新笔记（Figure 5）。这提示安全决策主要由开发者逐个 Function 实现。
- **Samsung Browser**：提供可能返回最长 **90 天浏览历史**的接口，但论文测试中缺少同等的锁屏保护；作者通过 ADB 调试调用读到历史。它当时**没有被商用 Executor 索引**，故不能断言商业 Gemini 可直接读到锁屏浏览历史。
- **Samsung Gallery**：部分 Function 描述包含引导 Agent 选择另一搜索功能的自然语言。正常引导本身不等于恶意注入，但表明元数据可能影响 Agent 决策。

## 八、Discussion 与 Limitation：结论的强度

作者认为现有 Android 的 UID、沙箱与单次权限检查无法自动表达“用户让 Agent 做什么、敏感数据能不能再交给另一 App”的**端到端授权策略**。他们建议更细粒度的 Function 级授权、敏感操作确认、锁屏验证、调用日志、Provider 审核和 Agent 侧安全策略。论文并未交付一个经充分评估的平台级防御系统。

重要限制：研究时 AppFunctions/API 与商用准入快速演进；生产环境仍主要只有受信任 App；实验室 Executor 不等同于商用代理；论文缺乏大规模跨模型成功率测量；**只考虑单一恶意 Provider，没有研究多个恶意工具共谋**。作者也没有证明 Root 或内核权限突破。

## 九、延伸研究：与 MCP-UPD 及 Android 权限共谋的联系

《Parasites in the Toolchain》将 MCP 风险工具按 EIT（外部内容摄入）、PAT（隐私读取）、NAT（网络发送）构造多步骤攻击链；本论文则提出 Android 原生函数编排的权限、Schema、UID 和数据流问题。两者可以结合，但不能只把三类工具换个 Android 名字。

一个更严格的新研究问题是：**在同样的总工具能力、相同用户任务与相同 Agent 权限下，两个恶意 Provider 是否能通过不同 App 身份获得单个恶意 Provider 无法获得的攻击能力？**

可用小型受控实验逐步探索：一恶意 A、单恶意 B、A+B 共谋、单 Provider 合并同等工具能力的对照；固定模型、Prompt、预算、系统版本，记录 Function 调用顺序、每一步 UID、权限与实际数据来源，并分开判定“Agent 未遵循用户意图”“数据不当披露”“真正 OS 权限绕过”。全部敏感数据使用合成 Canary。

如果 A 单独就可泄露隐私，B 仅作接收端，则还称不上新的组合攻击。需要证明独立能力不足、组合后可达的特有机制，最好再提出可复现的检测或防御方法。

## 十、一句话总结

Android 原本依靠独立 App 身份和门禁保护资源；AppFunctions 增加了一个能够以自身权限处理用户请求、并替不同 App 调用 Function 的 AI 秘书。**论文证明：每一步 Android 调用表面合法，并不自动保证由 Agent 编排的完整流程符合用户的隐私和安全意图。** 它给多 Provider 共谋留下了研究空间，但下一步必须通过严格的单方/多方对照去证明真正的组合效应。
