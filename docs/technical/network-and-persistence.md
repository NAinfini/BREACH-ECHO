---
doc_id: TECH-NETWORK
doc_type: technical
stage: BASELINE
updated: 2026-09-05
owner_role: 网络与数据负责人
canon_basis: "SRC-SSOT-2.0 §21、§36；SRC-USER-2026-09-05-HOST-MOD-AUTO-SYNC；SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED；SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS；SRC-USER-2026-09-05-TICK-ARCHITECTURE；SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE；SRC-USER-2026-09-05-LAG-COMPENSATION-BASELINE-APPROVED；SRC-USER-2026-09-05-HUMAN-FILE-NAMES-AND-LARGER-BATCHES；SRC-USER-2026-09-05-STEAM-ONLY-NETWORK-STACK-APPROVED；SRC-USER-2026-09-05-NEXT-MOD-RUNTIME-BATCH；SRC-USER-2026-09-05-MOD-RUNTIME-APPROVED-SECURITY-FIRST"
depends_on: ["architecture-and-performance.md", "gameplay-data-command-and-save-contracts.md", "unity-steam-and-modding-technology-stack.md", "../governance/decisions/host-authority-and-gameplay-commands.md", "../governance/decisions/fixed-tick-and-multirate-simulation.md", "../governance/decisions/state-replication.md", "../governance/decisions/lag-compensation-and-server-rewind.md", "../governance/decisions/network-runtime-and-recovery.md"]
---

# 网络权威、存档与版本固定

## 目的与范围

让长局对断线和主机退出有韧性，保持资源、任务和构筑结果一致。技术恢复不允许玩家用死亡回到更好资源状态。

NET-001 · CANON · 来源：SRC-SSOT-2.0 §21.1–§21.5；SRC-USER-2026-09-05-MATCHMAKING-AND-EVENT-BACKEND。

Server-authoritative、默认 player-hosted、可 Host Migration、dedicated-capable。Solo 本地运行 Authority 且支持 offline；好友/Private/Public 由选定 PC 运行 Server Runtime + Client，不依赖每局官方模拟服务器。首发的销售、身份、好友、邀请、Lobby、搜索与公网传输使用 Steam/Steam Datagram Relay；另有一个小型 BREACH 协调器只管理在线 Run 成员、lease、epoch 与恢复证书，不模拟世界。Community Dedicated 是支持方向，未来 Official Dedicated 不是成本前提。Host 不等于 Party Leader，按 CPU/uplink/jitter/loss/stability/thermal 评估，Deck 可 host 但优先稳定 PC；使用 SDR 时不把 NAT 类型当主要评分项。Host 不能直接写他人 Account。壁垒是 Personal/Party Hub，Hub Owner、Network Host、Party Leader 不同，无公共 50 人 MMO Hub 承诺。

NET-002 · CANON · 来源：SRC-SSOT-2.0 §21.3、§36.4。

Host loss冻结Simulation Time，选新host/new Authority Epoch、防split-brain；恢复AI/RNG/loot/director/body parts/mission/projectiles/actions，并支持graceful transfer。Gameplay mods/content version固定active/suspended run，恢复不得静默用新逻辑。

NET-003 · DIRECTION · 来源：SRC-SSOT-2.0 §36.1–§36.3。

Save/Network/HostMigration共享语义schema但不同profile；snapshot+journal与strong transaction boundaries使Fusion/Support/Cart/world原子可恢复。1.0进入更强save/API compatibility时代；早期可breaking但需明确迁移/通知。

## 会话流程与状态所有权

NET-004 · PROPOSED · 来源：本轮技术扩写。

创建run并锁ruleset/packages→对等端验证hash/schema/能力→Authority模拟→定期snapshot+journal→挂起/迁移/结束→结构化account claim。Client预测表现和局部输入，不拥有物资结果。Session记录不包含用户平台密钥或可任意执行的存档脚本。

| 状态 | 触发 | 结果 |
|---|---|---|
| Preparing | profile依赖和hash一致 | Active，记录runID+epoch |
| Active | graceful transfer | 关闭旧epoch写入，封journal边界 |
| Active | host失联 | Frozen；生命/热/敌人计时不前进 |
| Frozen | 合法候选有可证连续状态 | 新epoch恢复，旧host回归只能client |
| Frozen | 无一致状态/缺包 | RecoveryBlocked，说明原因保留可恢复材料 |
| Suspended | exact profile可用 | 按原版本续续 |
| Completed | 重复claim请求 | 返回原ResultID，无二次奖励 |

NET-009 · CANON · 来源：SRC-USER-2026-09-05-HOST-MOD-AUTO-SYNC；SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY；Mod runtime见[Agent-first Mod Runtime](../governance/decisions/agent-first-modding-runtime.md)。

**Client加入Modded Host时自动同步Host的Gameplay Package Lock。** 玩家不需要手工查找、编辑或逐项安装Host要求的Mods。连接流程在进入Gameplay Authority前完成：Host公布package_id/version/content hash/dependencies/distribution locator/permission class；Client比较本地状态；缺失或不匹配且可自动获取的包由内置Mod系统下载、验证、staging并激活；全部exact hash一致后才进入Run。

当前正式公开分发/下载层为 **Steam Workshop / ISteamUGC**：Steam负责Workshop文件传输与安装目录，BREACH Loader负责Package语义、hash、schema、依赖、权限和冲突。Data/Graph/受支持Luau Sandbox内容可进入标准自动同步；社区Managed/Native DLL、可执行文件与动态库在初始版本由Validator直接拒绝，不进入警告后放行路径。Host不得把未知代码以临时网络文件方式直接推送给Client并绕过Loader。

NET-010 · CANON · 来源：SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED。

**Steam平台集成与网络/玩法语义解耦。** Steam AppID、SteamID、Lobby ID、Workshop PublishedFileId、好友邀请token等只能存在于平台/服务适配层；RunManifest、SaveSchema、Package Lock、Entity/Account内部ID和Simulation事件使用BREACH自己的稳定语义。当前只发行Steam不等于允许Steam类型渗透Kernel；未来若新增平台，应通过Provider/Adapter增加实现，不重写Gameplay或ContentPackage。

NET-011 · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS；详见[Host Authority与Gameplay Command](../governance/decisions/host-authority-and-gameplay-commands.md)。

**Gameplay网络权威采用Host-authoritative Simulation + Gameplay Command Replication。** Client发送Move/Fire/Reload/Ability/Interact等语义意图，Authority验证并产生最终transform、命中、Damage、HP、Ammo、Loot、AI、Objective、Gameplay Physics等结果。Host本地玩家与远程Client必须走同一Command/Authority pipeline；Listen Server仅允许绕过实际网络传输开销，不允许Host-local gameplay直接写世界状态形成第二套逻辑。高响应动作允许Client Prediction + Server Reconciliation，本地VFX/SFX/recoil/UI等Presentation可立即播放，但本地预测永远不升级为Gameplay真相。

Gameplay Command必须与具体输入设备、Steam Input和底层Transport解耦；Replay、Bot、测试Harness可产生同类Command。Server Rewind的动作家族与公平边界已由[延迟补偿决定](../governance/decisions/lag-compensation-and-server-rewind.md)锁定；历史采样、时间映射和具体测试数值仍需Spike。

NET-012 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE；详见[固定Tick与多频模拟](../governance/decisions/fixed-tick-and-multirate-simulation.md)。

**Authority Simulation固定60 Hz，网络复制、AI Brain与Render解耦。** 关键玩家/Boss状态以约30 Hz复制为当前基线方向；近距/普通/远距AI按重要性降到约15–20 / 10–15 / 5–10 Hz并支持Dormancy/Event-driven更新；AI高层决策约5–10 Hz且必须stagger/time-slice，低层已确定Intent续续在60 Hz Authority Simulation执行。Gameplay Physics默认与60 Hz authority对齐，但Physics transform不要求60 Hz全量复制；高速Projectile优先使用sweep/CCD/substep或专门算法，不把全局tickrate提升到120 Hz。

60 Hz是Gameplay/Protocol时间合同，不作为普通Server配置项。Command逻辑cadence可最高60 Hz，但多个Command可packet batching；禁止假设一Command等于一Packet。固定步进必须有bounded catch-up，严重hitch时优先削减低优先AI Think、background simulation、低优先replication与cosmetic work，不得静默丢合法Damage、资源、任务、Gameplay Physics或Proc结果。Mod gameplay计时基于SimulationTime/seconds/events，不得用Render FPS改变结果。

NET-013 · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE；详见[状态复制](../governance/decisions/state-replication.md)。

**Host→Client复制采用Snapshot + Delta State Replication + Reliable Gameplay Events + per-client Interest Management + Dormancy。** 连续/可覆盖状态（Transform、Velocity、HP当前值、AI locomotion、Physics correction等）以Snapshot/Delta为主；Server围绕Client已确认baseline发送dirty component/field，而不是每次全字段序列化。丢失Delta不得导致永久不可解码，baseline失效时必须能rebase/发送足够的新状态恢复Client。

离散且漏失会改变语义的Spawn/Despawn、Inventory/Loot transaction、Objective commit、Seat/ownership change、Authority Epoch等使用Reliable Gameplay Event或等价可靠事务，并携带稳定ID/sequence/幂等语义，防止重试重复扣资源或重复奖励。Player/Enemy位置等latest-state-wins高频状态不使用可靠有序队列等待旧包补齐。

Server为每个Client单独计算Interest/Relevance；距离只是一个输入，还可考虑房间/战斗关系、是否正在影响该玩家、Team/Objective criticality和对象类别。长期无变化对象可Dormant到0 Hz，权威变化或重新进入relevance时Wake并补足dirty/baseline。Interest/Dormancy只改变投影成本，不改变Authority世界是否真实存在。

Entity网络身份使用BREACH自己的稳定runtime identity/generation；SteamID、Lobby ID、Workshop ID、Unity instance ID与transport handle不得成为Gameplay Entity identity。Join-in-progress优先从当前Authority State/baseline恢复，不要求从Run起点重放整局RPC/Event历史。高数量Projectile默认使用spawn metadata + Client presentation/prediction + Authority correction/result，而不是每颗弹丸持续高频可靠Transform流。

明确拒绝：60 Hz全世界全字段Snapshot、RPC soup、所有消息Reliable、只按距离做Relevance、Dormant对象持续心跳式完整状态、以及底层Steam/EOS/某Unity transport类型渗透为Gameplay replication schema真相。

NET-014 · CANON/DIRECTION + TEST · 来源：SRC-USER-2026-09-05-LAG-COMPENSATION-BASELINE-APPROVED；完整责任见[延迟补偿决定](../governance/decisions/lag-compensation-and-server-rewind.md)。

**Lag Compensation不是一个全局开关，按动作家族分别处理。**

| 动作家族 | 已确认基线 | 仍需测试 |
|---|---|---|
| Hitscan | Authority按可信Command时间查询有限历史Hitbox；历史态或当前态掩体任一挡住即否决；当前Tick提交一次 | 历史采样/压缩、散弹、穿透与顺序 |
| Projectile | Authority在当前世界生成并模拟，不回滚整段飞行 | 弹体分类、追踪/反弹与Client表现纠错 |
| Melee | 允许短于Hitscan的历史Hitbox/swept-volume查询 | 窗口、攻击者/目标位姿与多目标顺序 |
| Explosion / World Interaction | 默认只以Authority当前状态结算 | 是否存在需要单独登记的极少数例外 |

只查询命中所需历史，不把整个世界倒带。不得因高延迟射手的旧Command撤销已经提交的敌人攻击、伤害、弹药、门、拾取、资源或Objective结果；不得让一次Fire因当前态与历史态各结算一次。Host本地玩家通过同一Hit Query接口，接近零回溯只属于时间参数差异。

首轮`Max Rewind = 150 ms`为TEST，不是Ping上限或永久CANON。验证矩阵覆盖RTT 0/40/80/120/180/250 ms、jitter 0/20/50 ms、loss 0/1/3%，记录Client预测命中与Authority判定分歧、实际history age与clamp率、掩体竞态拒绝、输入到确认延迟、CPU与内存。历史采样/压缩、时间映射、Melee窗口和最终高延迟UX续续OPEN。

NET-015 · CANON/DIRECTION + TEST · 来源：SRC-USER-2026-09-05-TECH-OPEN-BATCH-AND-LAG-COMP-GATE；SRC-USER-2026-09-05-HUMAN-FILE-NAMES-AND-LARGER-BATCHES；SRC-USER-2026-09-05-STEAM-ONLY-NETWORK-STACK-APPROVED；完整方案见[网络运行与恢复](../governance/decisions/network-runtime-and-recovery.md)。

**已确认组合为Steam控制面与SDR传输 + FishNet Gameplay框架 + BREACH自有Host Migration。** 初始版本的商业发行、身份、好友、邀请、Lobby、匹配搜索、P2P/Relay与公开Mod分发全部使用Steam/Steam Workshop。四层职责不得混淆：Steamworks.NET/Steam Lobby负责身份、好友、邀请与搜索；Steam Datagram Relay经ISteamNetworkingSockets承担公网P2P与relay；FishNet承担Unity内连接、预测和网络对象基础设施；BREACH自己的Command、Snapshot、Recovery Schema、Journal和Authority Epoch持有玩法与恢复真相。

首发不并行接入Unity Relay/Sessions/Auth、EOS、NGO或Distributed Authority。FishySteamworks只作为首个Transport Adapter Spike候选；若其channel、队列、断线或目标平台表现不合格，只替换adapter，不重写Gameplay语义。

Host Migration 使用两名热备、Recovery Baseline + Delta + Durable Journal；存在 Primary Backup 时，关键事务由其 ACK 后才向玩家发布 Commit。小型协调器签发当前 lease、Migration Record 与 Authority Epoch，Gameplay Host 按已发布候选表选择；协调器不可用时不另起无租约的第二世界。10 秒 Baseline、2 Hz Delta、90 秒 Seat 保留、8 秒恢复目标、15 秒 RecoveryBlocked 和普通战斗最多 500 ms 瞬态回退均是首轮 TEST。有合格 Primary 时 Durable 事务必须零重复零丢失；single-authority degraded 状态明确不作此保证。

## 存档与包固定

NET-005 · PROPOSED · 来源：本轮技术扩写。

RunManifest至少含runID、ruleset ID/version/hash、所有content/module版本hash、确定加载序、依赖图、capability policy、schema revision、seed hierarchy、authority epoch、参与seat与事务cursor。Save按定义保存实例/挂点/Modification/Team Ordnance弹药和位置、任务图、已知信息、draft资格、LastChance候选、delayed event和RNG。

引擎已锁Unity 6，初始商业与在线平台已锁Steam/PC/Steamworks/Steam Workshop；网络组合与选主原则已确认，具体adapter、迁移频率和指标仍须Spike。本作为合作PVE，不建设或承诺竞技级反作弊，也不以高风险公共排行榜驱动架构；玩家房主修改私人会话是接受的非目标。服务器仍需验证结果schema、账号归属和事务唯一性，目的是防止损坏存档、跨账号写入及网络重试重复结算，不是判定玩家是否按官方方式完成战斗。

Gameplay package在Active/Suspended Run期间必须按exact hash冻结。分发源的“最新版本”不自动替换Run锁定版本；Client若只能取得不匹配的新版本，则不得伪装兼容。已确认把本局验证通过的artifact复制进BREACH本地不可变缓存并由Run/Profile pin；新Client先查本地精确hash，再尝试通过Steam取得当前item并重新校验。仍无法取得时明确拒绝加入，不允许Host直传、非Steam公共CAS或静默升级。缓存容量与失败UX仍须Spike；完整决定见[Steam Workshop Mod Runtime](../governance/decisions/steam-workshop-mod-runtime.md)。

## 模式、模块与边界

NET-006 · PROPOSED · 来源：本轮技术扩写。

Operation与Lab用不同ruleset但相同保存接口；恢复需要exact gameplay package graph。缺版本明确要求恢复相应版本/选择合法显式迁移，不静默降级或变强。Presentation-only mod是否可变由内容声明验证，不能给Gameplay功能贴presentation标签绕pin。

两个host同时声称authority只接受当前epoch授权；旧epoch命令不再次消费。断线中的pickup/Fusion/Support以最后已提交事务为准。离队玩家Team Ordnance物化保留。迁移期间语音不因gameplay freeze必然中断，但provider能力必须实测。不可恢复技术故障应显示未完成而非“通关”，不得伪造补偿奖励。

## 参数、示例与验证

NET-007 · TEST · 来源：SRC-CHATGPT-REVIEW-1.0 §6；本轮适配。

在至少一名合格 Backup 持续持有闭合恢复状态的前提下，原型迁移 20 次，目标至少 19 次在 8 秒内恢复，且 Durable 资源/任务/实例零重复零丢失；成功率低于 90% 为失败区。没有合格 Backup 或协调器无法签发 Migration Record 时，验收对象是准确进入 RecoveryBlocked，而不是伪造成功。该目标非已实现 SLA，剩余小样本需追加证据。网络模拟至少覆盖延迟、丢包、抖动、主机硬退出与 Steam/协调器单边分区；借用[Unreal 网络模拟方法](../research/references-and-methods.md)不代表选择 Unreal。

正常：炮弹已发后Host退出，新host续续同一炮弹。失败：内容包hash不一致明确拒绝进入，不按最新版本硬读。跨系统：同一Cart journal只扣一次Cell，迁移恢复不提供游戏checkpoint。Modded Join测试必须覆盖：Client缺一个安全Workshop测试包→游戏自动获取→显示进度→验证hash→进入Run；另测Workshop item不存在/私有化、下载失败、依赖缺失、hash变化与用户拒绝unsafe权限时的清晰失败路径。平台解耦测试要求Mock/移除Steam平台适配器后，Save/Package/Simulation单元测试仍能运行。

Tick/Replication原型还必须验证：60 Hz Authority在目标Host硬件与代表性战斗负载下可持续；高负载时AI Think分片没有周期性尖峰；关键实体约30 Hz、普通/远距AI低频复制后远端表现通过interpolation仍可接受；Dormant对象不持续占带宽；Projectile压力不能退化成每颗弹丸高频Transform洪泛；Render FPS变化不得改变Gameplay结果。精确带宽、CPU与频率阈值属于TEST数据，不因本文件基线而视为已证明。

Replication Spike还必须覆盖：4人不同ping/loss/jitter；baseline ACK后仅发送dirty delta；主动丢弃若干delta后Client可通过后续rebase/state恢复；Reliable transaction重发不产生重复奖励/扣除；Interest Set变化能正确spawn/wake/despawn proxy；Dormant对象权威变化会立即wake；Join-in-progress不重放整局历史即可得到正确当前世界；100+ AI和Projectile压力下测量per-client kbps、packets/s、serialization/replication scheduler CPU、baseline memory与恢复时间。上述均为验证要求，不是已达到的性能承诺。

## Descent发布联合行动

NET-008 · DIRECTION · 来源：SRC-USER-2026-09-05-NODES-LORE-ONLY-DESCENT-COMMUNITY-EVENT；SRC-USER-2026-09-05-MATCHMAKING-AND-EVENT-BACKEND；SRC-USER-2026-09-05-PVE-NO-ANTI-CHEAT；产品规则见[Operation OPS-013](../gdd/operation-game-mode.md)。

全服务器节点恢复进度要求逻辑上独立于玩家房主的官方聚合权威，但不要求为活动新建整套官方对局服务器。基础版既有的匹配/身份控制面在Descent发布时只增加两个职责：接收活动任务结果、以幂等方式累加阶段进度。普通Operation仍由player-hosted Authority运行；完成声明复用匹配会话ID并携带活动任务ID、参与账号和唯一ResultID。同一ResultID因重试再次上传时不重复贡献，客户端提交的是任务结果而不是任意进度数值。

联合行动是合作PVE叙事事件，不做玩法遥测证明、作弊检测、封禁或贡献速率审判。房主可以修改本局甚至伪造完成，这项风险明确接受；公共进度阈值本来也必须由运营保证最终完成，不能把一条没有竞争价值的剧情进度做成警察与小偷。活动专用官方任务列表只是贡献资格边界；Modded/自定义规则局是否计入由活动规则决定，不以反作弊名义限制玩家私人玩法。

该服务只在匹配控制面上增加活动计数与历史查询，不升级为每局官方专服依赖。早期目标可按单个小型服务部署估算，但容量、峰值并发、区域故障与运维成本必须以压测和真实匹配规模确认，当前不能写死为一台机器。活动上线前还必须定义服务停运和活动结束后的静态状态：端点开放结果随版本或轻量配置长期保存，即使聚合服务退役，玩家仍可访问已经开放的内容。离线结果何时提交、区域分片与总量合并仍OPEN；这些问题未解决前，活动只能作为发布方向，不能承诺具体日期或阈值。
