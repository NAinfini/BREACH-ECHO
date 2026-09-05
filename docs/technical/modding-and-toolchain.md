---
doc_id: TECH-MODDING
doc_type: technical
stage: DRAFT
updated: 2026-09-05
owner_role: 工具与扩展架构负责人
canon_basis: "SRC-SSOT-2.0 §27、§30、§36；最新模块化用户意图；SRC-USER-2026-09-05-UNITY-ENGINE-LOCK；SRC-USER-2026-09-05-AGENT-FIRST-STRUCTURE-A；SRC-USER-2026-09-05-OFFICIAL-CONTENT-PACKAGES；SRC-USER-2026-09-05-HOST-MOD-AUTO-SYNC；SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED"
depends_on: ["network-and-persistence.md", "../governance/decisions/DDD-0008-engine-unity6.md", "../governance/decisions/DDD-0009-agent-first-modding-runtime.md"]
---

# 模块化产品、公开能力与工具链

## 目的与诚实边界

让官方内容与社区内容能以同一套可验证结构生产。模块化减少设计过的扩展成本，不等于任意整块热替换或另一款游戏免费；“所有API全部公开”不能作为字面工程承诺。

MOD-001 · CANON · 来源：SRC-SSOT-2.0 §27.1、§27.5、§36.4。

扩展层级Data→Graph→Sandbox Script，native明确unsandboxed；官方内容尽量走public extension points；包声明namespace/manifest/dependencies/version/hash/permission，支持profile/modpack/rollback/staging与性能归因/quota/fault isolation。Gameplay包固定active/suspended run，presentation更灵活。TC可替换player-facing game/menu/progression，官方内容entitlement与free runtime分开。

MOD-002 · DIRECTION · 来源：SRC-SSOT-2.0 §27.2–§27.4、§30。

Entity/Anatomy/Ability/Relic/Fusion/Mission尽量共享compiler/IR/runtime/debugger；SDK方向包括graph editor、capability inspector、room/biome/puzzle/mission editor、scenario test、profiler和CLI/headless build/cook/validate。先内部→slice→精选作者→公开polish，核心未验证不先造完整公开Editor。Agent工作流使用文本/语义真相、契约/ADR、任务范围、变更manifest、包所有权、独立review、可回滚检查点和deterministic validators；AI资产走同一provenance/import/cook并可人工接手。

MOD-010 · CANON · 来源：SRC-USER-2026-09-05-UNITY-ENGINE-LOCK。

本项目Modding与Agent工具链以 **Unity 6** 为实现宿主；不继续维护Unreal/Blueprint/uasset兼容设计。公开内容格式和Authoring API仍应尽量保持项目自有、语义稳定，不让Unity具体对象成为所有Mod数据的唯一真相。

MOD-011 · DIRECTION · 来源：SRC-USER-2026-09-05-UNITY-TECH-DIRECTION；具体格式尚未冻结。

AI-agent-first与Modding共用一套生产哲学：核心Gameplay代码优先C#文本；可批量生成的内容优先文本/结构化数据；validator、build、cook、package、test尽量提供CLI/headless入口。Mod作者的主路径优先是自定义SDK/ContentPackage，而不是必须拿完整Unity工程手工拖Prefab。Unity Editor可作为高级Authoring工具，但不应成为所有Data/Graph Mod的硬前提。

MOD-013 · CANON · 来源：SRC-USER-2026-09-05-AGENT-FIRST-STRUCTURE-A。

工程采用 **Local UPM Packages + 独立 Content 数据层 + Assets 主要负责 Unity 表现/第三方资源**。Runtime、官方内容、社区Mod、SDK与Agent工具都围绕稳定ID、Registry、Schema、Validator与Package contract工作；Gameplay语义不以场景内临时Instance ID或Inspector引用作为唯一真相。

MOD-014 · CANON · 来源：SRC-USER-2026-09-05-OFFICIAL-CONTENT-PACKAGES。

**Official Content 必须使用与社区Mod相同的 ContentPackage / Registry / Schema / dependency / version / hash 体系。** 官方包拥有官方namespace与受控能力，但不得另建与Mod平行的隐藏武器/敌人/任务定义模型。Official content dogfoods public extension path；仅平台密钥、账户写权限、网络authority内部、安全敏感能力等可保持不可公开实现。

MOD-015 · CANON · 来源：SRC-USER-2026-09-05-HOST-MOD-AUTO-SYNC；具体联网流程见[Network](network-and-persistence.md)。

多人加入时，Client不手工寻找或修改Host所需Mods。Host在正式Gameplay连接前提供本局精确Package Lock；Client自动比对本地包，对缺失或不匹配的可自动获取包执行下载、安装、验证、staging和profile激活，全部hash一致后才进入Run。Data/Graph/受支持Sandbox Script可走标准同步；未来若开放Native/unsafe code则必须独立标记并要求显式授权，不得静默执行。

MOD-016 · CANON · 来源：SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED。

**当前正式公开Mod生态只使用 Steam Workshop。** Workshop负责发布、发现、存储、订阅、安装和Host缺包自动下载；当前不实现mod.io、Epic/GOG Mod平台或另一套公开Mod Marketplace。游戏自带BREACH Mod Loader/同步协调层，第三方Loader/Manager不是正常玩家使用官方支持Mods的前提。

Workshop `PublishedFileId` 只是distribution locator，必须映射到项目自己的 `package_id`、manifest和content hash；Steam负责把文件送到本机，BREACH Loader仍负责schema、dependency、permission、conflict、hash和save/network compatibility。Local/dev Mod保留给开发、测试、SDK示例和诊断，不作为与Workshop并列的公开Mod分发渠道。

MOD-017 · CANON · 来源：SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED。

**Distribution Provider与Runtime Package Model必须解耦。** `Steamworks/ISteamUGC`只能存在于平台/分发适配层；Kernel、Gameplay、Content Registry、SaveSchema、Package dependency graph和Network semantic state不得依赖Steam类型或把Workshop ID当业务主键。未来若新增商店或Mod分发源，只增加Provider/locator映射，不修改ContentPackage格式或Gameplay API。该扩展能力是防锁死边界，不代表承诺非Steam发行。

MOD-018 · DIRECTION · 来源：本轮Mod UX讨论。

游戏内需要最少的Mod状态与同步UI：启用/禁用Profile、Host所需包列表、下载进度、依赖/权限/冲突和失败原因。完整Mod浏览、排序、评分、收藏等可以直接利用Steam Workshop UI或后续增加游戏内界面；最终Mod Manager的信息架构和功能密度尚未冻结。

## 模块分层及替换难度

MOD-003 · PROPOSED · 来源：SRC-USER-2026-09-04-MODULAR-REFINEMENT；本轮评审。

| 层 | 可替换性 | 实际边界与代价 |
|---|---|---|
| Official ContentPackage | 高 | 武器、工具、修改、敌人、房间、任务定义；仍需资产/规则验证 |
| Resource/Reward/Director policy与ruleset | 中高 | 契约可换，资源/节奏/教程/QA同步改变 |
| 完整ModePackage | 中 | 可复用内核，仍要地图、内容、平衡、UI和玩家预期 |
| authority/physics/serialization/entity lifecycle/rendering | 低 | 明确服务边界，不承诺插拔后save/network仍可用 |
| combat feel/accessibility/performance/co-op readability | 很低 | 横跨资产与系统，不能打包成插件就省掉整体调试 |

目标为stable kernel+capability interfaces+composable rulesets+official packages。官方Operation不得直接写Kernel私有状态；Kernel不得引用BLACKSTART/Operation专属类型。不要把每个小对象插件化、靠全局event bus藏依赖、把Economy替换说成只换文件或在原型期冻结所有public API。

## 当前就建立的真实接缝

MOD-004 · PROPOSED · 来源：本轮架构评审。

| 合同 | 负责 | 当前消费者 |
|---|---|---|
| Simulation primitives | Action/Entity/Damage/Effect/Tag/Stat/Reaction/order | Operation武器/世界、Lab |
| Ruleset | Run生命周期、legal pool、resource policy、reward cadence、map grammar、failure | Operation；内部Lab |
| Effect/Modification | 统一效果图、scope、冲突与权限 | 武器/工具改装、TeamProtocol、Lab Relic |
| RewardSource | 明确来源、eligibility、offer与claim | 设施/支援/改装站；Lab奖励 |
| ResourcePolicy | 供给/消耗/转换的许可与成本 | Operation budget；Lab高密度 |
| ContentPackage/SaveSchema | namespace/版本/加载/保存与pin | 全部内容 |

不设计IRoguelike等未来专用接口。内部Combat Lab是廉价第二消费者：10分钟固定空间、无任务、高密度奖励、可重放效果组合，验证更换Ruleset不用改Kernel。不制作5层流程、商店、正式叙事或发布Descent。

## 统一修改定义

MOD-005 · PROPOSED · 来源：本轮用户武器配件底层统一意图；规则责任见[Build](../gdd/build-algebra.md)。

同一个ModificationDefinition/Effect schema供WeaponModule、ToolModule、TeamProtocol、Relic使用。区别在target_scope/presentation/eligibility，不建立RelicBase继承或两套近似效果引擎。公共schema并不使跨模式平衡自动共享；Operation配件不因此触发自动Fusion。

## Public API Surface 与权限

MOD-006 · PROPOSED · 来源：本轮技术扩写。

公开可支持的内容注册、只读查询、验证过Command提交、受限效果节点、场景测试、状态观测和版本化schema。CapabilityPolicy对资源铸造/转换、门控制、MissionAdvance、实体生成、复活、网络可见性等逐项授权。官方Operation普通改装不能免费复制资源或越过关键任务；TC可在明确自定义ruleset中另设规则，不混入官方匹配。

内核内存、平台密钥、账户写权限、网络authority内部、任意文件/进程/系统网络不能因“全部开放”暴露给普通mod。Native包显式未沙盒化，用户需看见权限/信任风险且不能混同安全Data包；具体允许渠道待决定。不承诺从不受信任包中获得安全的任意本地执行。

官方Gameplay baseline应尽可能对SDK可inspect，并允许通过稳定ID执行inherit/patch/override/replace；但官方安装源文件保持只读语义。Mod通过显式Patch Layer改变最终Registry，而不是直接写坏`Official/...`文件。这样更新、卸载、多人hash、冲突诊断和存档恢复均可重现。

## 包结构与确定加载

MOD-007 · PROPOSED · 来源：本轮技术扩写。

Manifest至少：package_id、version、content_hash、schema_version、dependencies及版本范围、capability_permissions、entrypoints、mode_allowlist、conflict_groups、entitlements、author/license/provenance；Steam分发包可另带`workshop_item_id`等locator，但分发ID不能替代package identity。先解析依赖→验证版本与能力→依赖拓扑排序→同层按稳定package_id排序→注册→交叉引用/冲突/循环验证→compile→生成精确lock manifest。循环依赖拒绝，重复ID拒绝；不靠文件系统顺序或“后加载覆盖一切”决定结果。显式覆盖要声明目标/兼容范围与授权。

Save/network固定完整依赖图、加载序和hash；细节归[持久化](network-and-persistence.md)。进行中的Run不热换gameplay包；presentation变更须证明不改碰撞、信息可见性和规则。

MOD-012 · DIRECTION · 来源：SRC-USER-2026-09-05-UNITY-TECH-DIRECTION。

Unity实现时，官方包与社区包应优先指向项目自己的稳定ID/Registry/Schema，而不是直接序列化场景内临时Instance ID或依赖Inspector手工引用。需要Unity资产的内容可以由构建阶段把受支持的Prefab/mesh/material/audio等Cook成包，但Data/Graph定义本身保持可diff、可验证、可由Agent生成。购买的Asset Store/Fab/CGTrader等资源必须按各自许可处理；不得为了SDK/Workshop把不允许再分发的raw source assets打包给Mod作者。

## 生命周期、边界与工具反馈

MOD-008 · PROPOSED · 来源：本轮技术扩写。

Authored→Validated→Compiled→Staged→Loaded/Pinned→Suspended/Completed。每阶段可报告包ID、文件路径、规则ID、失败前置与修复建议；不静默忽略坏字段。代码/资产工具只修改所属包，产物与源码分开，手工takeover不丢provenance。

加载不支持schema则阻止会话开始；运行脚本超预算按已公布fault policy报告并终止不可信执行，不能删一半canonical outcomes继续假装正常。多人加入先检查精确package graph，缺包时按MOD-015自动同步；下载/安装完成仍需显式验证，不把“Steam已下载”当成“Runtime已批准”。

## 开放时机与验收

MOD-009 · PROPOSED · 来源：本轮评审；方法见[研究](../research/references-and-methods.md)。

当前内部API允许破坏性修订并同步所有调用方；Vertical Slice稳定后，至少两名外部作者用文档各改一个武器/任务小包，记录需要改Kernel的次数和制作时间，再冻结有真实需求的公共面。版本兼容承诺从已发布边界开始，不为从未发布的草案留compat wrapper。

验收：Operation全部官方内容走相同注册路径；Lab切ruleset不改Kernel；两个包的加载在两机一致；版本缺失明确阻止恢复；无权限Mod不能改Mission/账户；错误能定位作者文件。Unity项目还需验证Agent可通过文本变更+batch/headless流程完成至少一个武器和一个任务内容修改，而无需人工逐字段修Inspector引用；多人测试还需验证Client加入缺一个安全Workshop测试Mod的Host时可自动获取、验证、启用并成功join，Vanilla profile可一键恢复；平台解耦测试要求移除/Mock Steam分发适配器后，Kernel/Gameplay/Content验证仍可独立运行。团队人数、公开API日期、脚本语言、license、完整Mod Manager UI与TC计划仍有OPEN部分。
