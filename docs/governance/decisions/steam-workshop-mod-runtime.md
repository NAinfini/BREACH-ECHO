---
doc_id: DECISION-STEAM-WORKSHOP-MOD-RUNTIME
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: Mod平台与运行时负责人
canon_basis: "SRC-USER-2026-09-05-HOST-MOD-AUTO-SYNC；SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY；SRC-USER-2026-09-05-STEAM-ONLY-NETWORK-STACK-APPROVED；SRC-USER-2026-09-05-NEXT-MOD-RUNTIME-BATCH；SRC-USER-2026-09-05-MOD-RUNTIME-APPROVED-SECURITY-FIRST；SRC-USER-2026-09-05-MOD-CONTENT-CAPABILITY-CLARIFICATION；Steamworks Workshop、Luau、MoonSharp、Microsoft与Unity官方资料；本轮系统设计评审"
depends_on: ["agent-first-modding-runtime.md", "network-runtime-and-recovery.md"]
---

# Steam Workshop 模组运行时、管理器与安全边界

## 裁决摘要

本批总体方案已由用户批准；脚本选择授权助手按安全、集成与作者体验作最终判断。现行结果如下：

1. Steam Workshop负责发现、社区页面、订阅、发布和下载；游戏内Mod Manager负责Profile、依赖、冲突、权限、精确版本、多人同步与诊断。不要在游戏里重做一个缩水版Steam商店。
2. `Profile`是玩家可编辑配置；`Package Lock`是一次编译出的不可变运行闭包；`Modpack`只是引用Workshop条目的可发布配方，不重新打包别人的文件。
3. 初始正式能力按`Data → Graph → Sandbox Script`开放；Sandbox Script确定为 **Luau Core Compiler + VM**。只嵌入Luau核心，不使用提供文件、网络和socket能力的Lute通用运行时。Unity 6/IL2CPP/Steam Deck安全与性能Spike仍是发货Gate；Gate失败就延后Script层，不能临时改用C#脚本或DLL。
4. 初始版本**不支持任何社区Managed Assembly或Native DLL**。PVE不做反作弊与“允许陌生代码读文件、起进程、偷凭据”完全是两回事。
5. Active/Suspended Run把已验证包按`content_hash`固定并本地缓存。Steam只能下载当前适用版本，不能被假定为任意旧hash仓库；新玩家拿不到精确hash时明确拒绝加入，不允许Host直传或非Steam公共CAS。
6. Gameplay Script只在Authority运行；Client只能运行无玩法写权限的Presentation Script。脚本超预算或崩溃不得静默删掉Mod继续结算。

些套方案并不“把所有API全部公开”。它开放稳定的玩法能力，不开放平台密钥、账号写入、任意文件、进程、网络套接字、反射、Unity对象图或Authority内部。否则所谓开放框架会变成一个更新就炸、联机就感染、作者互相踩覆盖顺序的垃圾场。

## 为什么不能把四个问题分开处理

Mod Manager决定玩家看见什么；Package Lock决定联机和存档复现什么；脚本Sandbox决定Workshop内容能安全做什么；旧版本策略决定长局是否还能恢复。只设计其中一项会制造假方案：

- 只有Workshop订阅，没有Package Lock：四个人“都装了同一个Mod”仍可能运行不同内容。
- 只有自动下载，没有安全分级：加入陌生Lobby等于同意执行任意本机代码。
- 只有hash，没有旧包缓存：作者更新一次，Suspended Run就永久死亡。
- 只有缓存，没有明确拒绝路径：新玩家会在下载、校验、重试之间无限循环。
- 只有任意load order：冲突不再是可诊断问题，而是玩家靠玄学拖排序。

## 候选决定

MODRUNTIME-DEC-A · CANON · 来源：SRC-USER-2026-09-05-MOD-RUNTIME-APPROVED-SECURITY-FIRST。游戏内Manager与Steam职责分离。

Steam Workshop负责：发现、搜索、评分、评论、收藏、法律协议、作者页面、订阅、上传、文件分发与下载。BREACH负责：包验证、Profile/Modpack、依赖闭包、能力清单、冲突解释、Package Lock、hash校验、多人加入、缓存、故障与作者诊断。游戏内“浏览更多Mods”直接打开Steam Workshop；不复制评论、评分和社区审核UI。

MODRUNTIME-DEC-B · CANON · 来源：SRC-USER-2026-09-05-MOD-RUNTIME-APPROVED-SECURITY-FIRST。Profile、Modpack与Package Lock是三个不同对象。

| 对象 | 是否可编辑 | 内容 | 生命周期 |
|---|---:|---|---|
| Profile | 是 | 玩家想启用的顶层包、配置与本地显示名 | Hub/主菜单中编辑；每次应用产生新revision |
| Modpack | 作者发布配方，不在运行中编辑 | Workshop locator、稳定`package_id`、版本约束、推荐配置 | 作为小型Workshop item分发；应用后生成本地Profile |
| Package Lock | 否 | 完整传递依赖、精确hash、schema、编译器/runtime版本、能力与最终加载序 | Run创建时冻结；Active/Suspended Run全程不变 |

Modpack不得把依赖包重新压入自己的zip；那会绕过作者更新、许可和Workshop归属。Steam的dependency关系只能帮助发现/下载，真正能否运行仍由BREACH manifest与Validator决定。

MODRUNTIME-DEC-C · CANON · 来源：SRC-USER-2026-09-05-MOD-RUNTIME-APPROVED-SECURITY-FIRST。不提供“随便拖load order就能修好”的玄学按钮。

加载顺序为：解析依赖与版本→验证能力→依赖拓扑排序→显式Patch Layer→同层稳定`package_id`排序→交叉引用/冲突检查→编译Registry。两个包修改同一排他字段且未声明兼容时，Profile无法编译。玩家可以禁用其一、安装独立Compatibility Patch或切换Profile；公开匹配不提供“Force Load Anyway”。

MODRUNTIME-DEC-D · CANON/DIRECTION + TEST · 来源：SRC-USER-2026-09-05-MOD-RUNTIME-APPROVED-SECURITY-FIRST；用户授权助手选择。Sandbox Script使用Luau Core Compiler + VM，并以Spike为发布Gate。

选择Luau的理由不是“名字酷”，而是它原生面向嵌入和不可信代码，提供隔离环境、只读全局、interrupt和内存分类等宿主控制点，并带渐进类型、lint和分析工具。上游仍活跃、使用MIT许可证，Compiler与VM可作为库嵌入。代价是它是C++ VM，需要为Unity 6/IL2CPP构建和维护受支持平台绑定，崩溃隔离仍不等于形式化证明。

**只使用Luau Core，不使用Lute。** Lute是面向通用程序的Luau Runtime，主动提供文件、网络请求和socket等能力；些些能力不应先被引入再试图逐个封死。BREACH从Luau Compiler/VM空白宿主起步，只注册自己的白名单值类型和Capability API。

| 候选 | 决定 | 原因 |
|---|---|---|
| Luau Core Compiler + VM | SELECTED | 原生Sandbox设计、interrupt、内存分类、渐进类型、活跃上游；集成成本可通过单一受控Native Runtime承担 |
| MoonSharp | REJECTED AS PRIMARY | 纯C#接Unity更省事，但安全依赖正确挑选库、关闭自动Interop并约束宿主对象；当前稳定/测试路线不如Luau适合长期安全优先基线 |
| 标准Lua 5.x C VM | REJECTED AS PRIMARY | 可嵌入，但需要项目自行补更多Sandbox、类型与工具链能力；没有理由重复Luau已经提供的宿主控制面 |
| WebAssembly | REJECTED FOR INITIAL SCRIPT API | 隔离潜力强，但作者工具链、ABI、宿主对象映射和调试成本显著更高，不适合作为第一批大众Mod脚本语言 |
| C#脚本/Managed Assembly | REJECTED | 不能依赖现代.NET CAS或partial trust隔离未知代码 |

实施边界：

- 标准Package包含可读Luau源码；安装时由项目固定版本的Compiler编译并把源码、编译器版本、API schema和产物纳入hash。
- 每个Package使用独立environment与内存类别；共享标准库只读；不共享可变global。
- 不暴露`io`、`os`、文件、进程、socket、动态库、反射、CLR/Unity对象、真实墙钟、环境变量、剪贴板或平台账号。
- 只暴露项目拥有的不可伪造Capability Handle与值对象；Gameplay写入必须提交经过验证的Command，不返回可任意调用的内部对象引用。
- RNG由Authority提供带域分离的确定种子；Gameplay逻辑不得读取Render FPS或Client本地时间。
- Gameplay Script只在Authority执行。Client根据复制结果播放表现；允许Client Presentation Script，但它不能改命中、碰撞、AI、资源、任务、掉落或网络可见性。
- 持久状态只能写入有schema、版本和配额的Package Save Namespace；闭包、线程、coroutine、宿主对象引用不能直接序列化。
- Hot Reload只存在于SDK测试会话；Active/Suspended Run不热换Gameplay脚本。

Luau语言与Core VM选择已经锁定，但“已选”不代表“绑定已证明”。若它不能在Unity 6、IL2CPP、Windows/Proton目标上可靠提供构建、调用栈、调试符号、CPU中断、内存配额与故障报告，则首发只发布Data/Graph，Script层延期。不得为赶功能改用任意C#动态编译、Assembly加载、MoonSharp或Lute形成第二运行时。

MODRUNTIME-DEC-E · CANON · 来源：SRC-USER-2026-09-05-MOD-RUNTIME-APPROVED-SECURITY-FIRST。社区DLL在初始版本完全拒绝。

`*.dll`、原生库、可执行文件、动态Assembly和可加载二进制插件不能出现在标准Workshop ContentPackage中；Validator发现即拒绝staging。官方随游戏签名发布的Luau VM、Steam适配器或其他运行时依赖属于游戏二进制，不属于社区Mod能力。

本地`Mods/Dev`同样不以“开发模式”为借口自动执行社区DLL。真正需要调试Kernel扩展的贡献者使用源工程和正常构建链；它不是可加入公共Lobby的Mod Profile。未来若确需不可信本机扩展，必须另立威胁模型并采用进程/OS级隔离，不能靠一个红色警告框把风险甩给玩家。

MODRUNTIME-DEC-F · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-MOD-RUNTIME-APPROVED-SECURITY-FIRST。精确旧版本采用本地不可变缓存 + 明确拒绝，而非假设Steam能任意回滚。

Steam Workshop默认给订阅者当前适用版本。Steam的Game Branch Versioning能按游戏beta branch选择兼容的Mod版本，但它不是按任意`content_hash`取回任何历史上传的通用接口。因此：

1. 每个通过验证的Package被复制到游戏管理的不可变artifact cache，以`package_id + content_hash`索引；不直接从Workshop安装目录运行。
2. Active Run、Suspended Run及用户明确保存的Profile pin其完整闭包。被pin的artifact不得被LRU静默驱逐。
3. Workshop更新只进入新的staging revision；不能替换运行中或暂停中的锁定artifact。
4. Join时先查本地精确hash；没有则通过`ISteamUGC::DownloadItem`取得当前可用item，完成后再由BREACH计算hash。匹配才staging，不匹配就失败。
5. 作者删除、私有化或更新item后，已经拥有精确本地artifact的原队伍可继续；缺少artifact的新成员不能加入。游戏把Lobby标记为“仅现有缓存成员可恢复”，避免反复诱导下载。
6. 若作者重新发布同一精确内容，可提供新的Workshop locator；Runtime身份仍是原`package_id + content_hash`，不会因PublishedFileId变化改存档。
7. 不允许Host把包直接传给Client，不建设非Steam公共CAS，也不静默升级Run。

缓存容量不在文档里拍脑袋写死。管理器必须显示总量、每个pin来源与清理后果；如果配额不足且只剩被Run/Profile引用的内容，阻止新下载并让玩家选择删除旧Run/Profile或扩大本地预算。具体默认GB数经真实Mod资产体积与Steam Deck存储测试后确定。

MODRUNTIME-DEC-G · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-MOD-RUNTIME-APPROVED-SECURITY-FIRST。Mod故障必须按权威影响分级。

| 故障 | 处理 |
|---|---|
| 加载前schema/hash/dependency/capability错误 | 阻止Profile激活，定位Package、文件、字段和修复建议 |
| Authority Gameplay Script异常、超时或越权 | 停止接受新的canonical gameplay commit，进入`Mod Fault`；保存诊断，队伍返回Hub或放弃Run，不静默禁用后继续结算 |
| Client Presentation Script异常 | 隔离该本地表现模块；若不影响信息公平可继续，并显示可追踪报告 |
| 内存/CPU预算超限 | 同一Package计数与归因；测试会话可暂停调试，正式Authority按Gameplay故障处理 |
| Save migration缺失 | 阻止恢复，不猜字段、不丢弃未知状态后伪装成功 |

“错误后继续玩”听起来友好，但一个负责掉落、任务或敌人逻辑的脚本消失后，后续世界已不是锁定规则集。继续结算只是在制造无法复现的坏档。

MODRUNTIME-DEC-H · PROPOSED · 性能配额按总预算和单包归因，不靠固定Sleep或无限重试。

首轮Spike使用以下TEST，不是发行承诺：

- 全部Gameplay Mod Script在Authority稳定帧中的总CPU预算不超过Simulation CPU预算的10%；每包另有burst与rolling-window配额。
- 无限循环必须在当前simulation tick内被interrupt，不能冻结主线程或跳过整个Authority watchdog。
- 初始内存实验为每VM 32 MiB、全体Script 256 MiB；以大型任务Mod实测后调整。
- Event订阅、Command提交、Spawn请求、Timer数量、Save字节和日志速率均必须有配额；不能只限制Lua指令数，却允许一次宿主调用生成十万个对象。
- 超限诊断必须显示Package、入口、事件、源码行、耗时/内存和最近Command；正式游戏不向玩家倾倒完整堆栈，但可导出作者报告。

## 玩家界面信息架构

### 入口

主菜单和Hub提供`模组`入口。它不是一块挤满Workshop卡片的商城，而是本机运行状态控制面。

### 总览

- 当前Profile名称、`Official / Modded`标记、顶层包数、完整依赖数与总磁盘占用。
- `继续使用`、`新建Profile`、`复制Profile`、`恢复纯净版`、`浏览Steam Workshop`。
- Active/Suspended Run使用的锁显示为只读；编辑会创建新Profile revision，不改变旧Run。

### 已安装

- 按启用、未启用、更新待应用、孤儿/不可下载、冲突、故障筛选。
- 每项显示作者、来源、版本、hash短码、内容类型、依赖、能力、存储占用和被哪些Run/Profile pin。
- “更新可用”与“此Run仍固定旧版”同时显示，避免把更新误解成已经生效。

### 配置档编辑

- 玩家只选择顶层意图；传递依赖自动展开。
- 编译结果显示新增/移除、冲突、Compatibility Patch建议、权限变化和Package Lock摘要。
- Apply只在Hub/主菜单完成；若包更新要求重启Runtime则明确提示并安全重启，不在Operation中途套用。

### 加入Modded Host

1. 展示Host Profile名称、Official/Community分类、缺失数量、总下载量和安全等级。
2. Data/Graph/获支持Luau包自动从Steam Workshop下载，无逐包许可弹窗；系统能力本来就不可用，因此不制造警告疲劳。
3. 显示下载、校验、编译、staging四段进度；Steam下载完成不等于Runtime验证成功。
4. 失败必须给出唯一主因和可执行下一步，例如`Workshop条目已删除`、`只找到不同hash`、`依赖冲突`、`磁盘缓存不足`、`Host只允许现有缓存成员`。
5. 成功后创建临时Join Profile revision；离开Lobby不自动污染玩家常用Profile。

### 诊断

普通玩家看到一行原因和建议；作者模式可展开依赖图、Patch冲突、Validator路径、源码行、能力调用、CPU/内存、日志限流和导出报告。所有状态必须有文字/图标，不只靠红绿颜色；键鼠与控制器焦点顺序一致。

## 作者工作流

推荐CLI闭环：

```text
breach-mod new
→ edit Data / Graph / Luau source
→ breach-mod validate
→ breach-mod test --scenario <id>
→ breach-mod cook
→ breach-mod pack
→ breach-mod publish --steam
```

发布工具调用Steam `CreateItem` / `SubmitItemUpdate`，检查Workshop法律协议，并把PublishedFileId写进distribution metadata，不写进Gameplay ID。标准包必须包含manifest与可验证的Data/Graph/Luau文本；Cook后的mesh、texture、audio等二进制资产不要求可读。源文件可见不自动授予复用权，`license`与第三方provenance仍必须声明。

## 模组实际可以增加什么

MODRUNTIME-DEC-I · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-MOD-RUNTIME-APPROVED-SECURITY-FIRST；SRC-USER-2026-09-05-MOD-CONTENT-CAPABILITY-CLARIFICATION；项目既有公开Mod与可替换官方内容意图。

Luau是安全逻辑层，不是模型格式、地图编辑器或Unity替代品。真正的内容Mod由Data、Graph、Cooked Assets和Luau按需组合；每类内容必须有稳定Schema、Cooker、Validator和运行时Capability，不能只发布一个“万能Lua API”后让作者猜内部对象。

| 内容 | 作者提供 | Luau负责 | 必须由SDK/Runtime提供 | 发行范围 |
|---|---|---|---|---|
| 新武器/工具 | 定义、模型、动画、音效、VFX、图标 | 特殊开火、蓄力、命中后反应、状态与自定义资源逻辑 | Weapon schema、挂点、动画事件、Damage/Effect Command、网络与性能验证 | 初始公开SDK核心目标 |
| 新敌人 | Anatomy/Stat/感知数据、模型、动画、音频 | 特殊技能、阶段与受限决策扩展 | 行为Graph、Nav/Spawn合同、Authority AI接口、Hitbox/LOD预算 | 初始公开SDK核心目标 |
| 新任务与地图模块 | 房间/走廊/机关资产、连接器、碰撞、Nav、灯光、音频、Spawn/Interaction anchors、任务Graph | 特殊机关、事件、任务状态与局部规则 | Space cooker、连接/可达性/可解性/Nav/预算Validator、程序生成注册表 | 初始公开SDK核心目标；先支持模块化空间，不先承诺任意Unity Scene直接加载 |
| 新玩家角色 | Character定义、第一/第三人称资产、Rig/动画、语音/字幕、能力引用 | 自定义能力、被动与状态逻辑 | Seat/输入/动画/复制/UI/本地化合同 | 支持Modded Profile；工具优先级低于武器/敌人/任务，不改变官方四人正史 |
| 新规则集/游戏模式 | Ruleset、任务池、资源政策、菜单配置、内容依赖 | Run生命周期、模式专用事件与规则 | Kernel Capability、Save/Network schema、Profile/Lock与自定义匹配标签 | 架构支持；完整TC工具不是初始SDK发货Gate |
| Total Conversion | 上述多种Package组合 | 受限逻辑组合 | 可替换player-facing菜单/进度/规则接口，但仍服从安全和平台边界 | 后续能力，不以首发宣传承诺 |

地图Mod不是把作者的Unity项目整个塞进玩家进程。SDK把受支持的Prefab、mesh、material、texture、audio、动画和空间元数据Cook成受控包；运行时只实例化白名单组件描述，行为通过Graph/Luau连接。自定义`MonoBehaviour`、Editor脚本、DLL和未知序列化Unity对象一律不能混入Cooked Package。

官方四名角色属于Official Profile与正史，不是Kernel硬编码的唯一四个角色。社区角色可以在Modded Profile替换或扩展Seat选择，但不会自动加入官方匹配、官方成就、官方叙事或官方外观经济。

## 被否决候选

| 候选 | 结论 | 原因 |
|---|---|---|
| 游戏内完整复制Workshop发现/评分/评论 | REJECTED FOR INITIAL RELEASE | 重复Steam能力、维护成本高、无助于依赖与安全 |
| 玩家任意拖load order并Force Load | REJECTED | 把结构冲突变成不可复现玄学 |
| C# Script / Managed DLL当安全脚本 | REJECTED | 现代.NET不把CAS/partial trust作为安全边界；同进程未知代码不可信 |
| Workshop Native DLL自动同步 | REJECTED | 加入Lobby即远程代码执行；PVE并不降低本机风险 |
| Host直传旧Mod | REJECTED | 绕过Workshop归属、审核、许可和既定Steam-only边界 |
| 非Steam公共内容寻址仓库 | REJECTED FOR INITIAL RELEASE | 等于建设第二分发后端 |
| Steam beta branch为每个Run保留任意旧hash | REJECTED | 官方机制按游戏分支兼容，不是任意hash历史仓库；分支爆炸不可运营 |
| Script崩溃后静默禁用继续结算 | REJECTED | 世界规则已经变化，结果无法复现 |

## 验证矩阵

本批只有通过以下Spike，才可把相应PROPOSED升为CANON/IMPLEMENTABLE：

### Steam与版本

- 两台干净机器：Client缺包→读取Host Lock→Steam下载→BREACH校验/编译→成功加入。
- Workshop item更新后：Active/Suspended Run继续使用旧缓存；新Profile使用新版；两者不串包。
- item删除、私有化、Steam离线、磁盘满、下载中断、hash不匹配、依赖缺失均得到不同且可执行的错误。
- 已缓存成员能恢复；未缓存新成员被拒绝；Lobby不会无限重试。

### 沙箱

- 尝试文件、进程、网络、反射、Unity对象和平台账号均不可达。
- 无限循环、深递归、日志洪水、事件洪水、大表内存和一次宿主批量Spawn均能被预算截断并归因。
- Authority与Client运行不同帧率时，Gameplay结果只由Authority脚本决定。
- Save/Resume、Host Migration与Replay使用同一Package Lock；脚本状态schema不靠序列化VM内部对象。
- Unity 6 IL2CPP发布构建与Steam Deck/Proton目标通过稳定性、崩溃符号和性能压力测试。

### 用户体验与作者体验

- 新玩家两步内恢复纯净Profile；加入Host时无需手工订阅清单或排序。
- 玩家能在错误页十秒内指出阻塞Package与原因；些是TEST目标，需可用性测试。
- 两名未参与系统开发的作者分别完成武器Data Mod、任务Graph Mod和一个受限脚本Mod；记录首次成功时间、文档缺口和需要修改Kernel的次数。
- 50个Package、复杂传递依赖、Compatibility Patch、多个Profile及大资产缓存下，Manager仍可使用且不会阻塞主线程。

## 当前仍OPEN

本批已获批，但以下实现值仍不能伪装成已定：

- Luau Unity绑定的具体封装、上游升级节奏、调试器与崩溃符号策略；
- Graph IR与Luau API的具体schema；
- 精确CPU、内存、Save、日志、事件和缓存GB预算；
- Workshop Modpack是否使用独立item type、tag或collection辅助展示；
- Compatibility Patch的作者归属、发现与弃用流程；
- 游戏更新导致Mod API破坏时的Steam beta branch保留周期；
- 最终Manager视觉设计、文本、本地化与可访问性实测。

些些OPEN需要Spike或制作数据，不需要现在靠想象填一个数字。Luau Core、无社区DLL、Manager职责和旧hash原则已经锁定；容量和交互指标必须后测。
