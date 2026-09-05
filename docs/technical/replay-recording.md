---
doc_id: TECH-REPLAY
doc_type: technical
stage: DRAFT
updated: 2026-09-05
owner_role: 回放与记录负责人
canon_basis: "SRC-USER-2026-09-05-DEBRIEF-AND-REPLAY；SRC-USER-2026-09-05-SIMPLIFIED-REPLAY-AND-STATS；SRC-USER-2026-09-05-DETAILED-STATS-LIGHTWEIGHT-LOCAL-REPLAY；SRC-USER-2026-09-05-POST-DEBRIEF-DISCARD；REF-GTFO-REPLAY"
depends_on: ["architecture-and-performance.md", "network-and-persistence.md", "../gdd/debrief-and-replay.md"]
---

# 行动回放记录、存储与播放

## 唯一事实流

TRP-001 · DIRECTION · 来源：SRC-USER-2026-09-05-DEBRIEF-AND-REPLAY；SRC-USER-2026-09-05-SIMPLIFIED-REPLAY-AND-STATS；SRC-USER-2026-09-05-DETAILED-STATS-LIGHTWEIGHT-LOCAL-REPLAY；SRC-USER-2026-09-05-POST-DEBRIEF-DISCARD；REF-GTFO-REPLAY。

回放不是MP4录屏，也不依赖跨版本完全确定的输入重演。Authority提交的同一语义事件流生成两份本地临时产物：`DebriefSnapshot`保存详细聚合统计与关键事件，`SimplifiedReplayRecord`只保存关键语义事件、低频空间采样和简化地图。两者共享事件ID和定义，只保留到玩家完成本局复盘并确认离开；禁止战斗系统、结算页和回放各维护口径不同的击杀、伤害或资源计数器。

`ReplayManifest`至少记录ReplayID、RunID、ReplaySchemaRevision、build、ruleset与content package graph/hash、地图Seed与已实例化Cluster Graph、难度、开始/结束时间、参与Seat、Authority Epoch序列、结局和索引校验值。回放只能读取事实，不拥有奖励、成就、任务推进或账号写权限。

## 记录内容

TRP-002 · PROPOSED · 来源：本轮技术扩写。

记录分成三类：

| 轨道 | 记录 | 不记录 |
|---|---|---|
| Semantic Events | 射击/命中/伤害、潜行刺激/唤醒/警戒扩散、倒地/救援、资源事务、目标、门/电力/炮塔/机器人、重资产、Ping、发现与撤离 | 未提交候选、内部调试猜测 |
| Tactical Samples | 玩家及重要实体的低频位置、朝向、生命/活动状态、装备与当前动作 | 原始相机、逐帧动画、每颗普通弹体、AI黑板 |
| Map Proxy | 已发现房间/连接轮廓、门、目标、重资产与关键资源位置 | 原始网格、材质、灯光、粒子、布料、ragdoll与音频 |

`DetailedStatAccumulator`在任务中消费已提交事件，按Seat、武器、敌人、命中部位、任务阶段和资源类别累计；结束时写入`DebriefSnapshot`，无需为详细统计永久保存每发弹体轨迹。`StealthBreakEvent`必须携带EventID、时间、区域、StimulusType、SourceActionID、CauseEventID、FirstAlertedEntityIDs、CascadeRootEventID、AttributionStatus（Single/Shared/Unknown）和CausalSeatIDs。客户端到达顺序不能决定责任人。

周期关键帧提供随机拖动入口，关键帧之间应用有序事件与空间采样。伤害、资源、目标和实体生死必须完全一致；标记在两个采样点之间只做可视插值，不允许由插值反推新的命中或统计。查看器不调用战斗模拟，也不尝试还原当时画质。空间轨道只需达到“看懂队伍如何移动、谁在何处触发关键事件”的清晰度；首轮候选为玩家4Hz、已警觉关键敌人2Hz、其余相关实体0.5–1Hz，最终以体积和可读性原型裁决。

TRP-003 · DIRECTION · 来源：本轮技术扩写；网络模型见[NET-001至NET-008](network-and-persistence.md)。

每台参与设备记录自己收到的权威事实、空间采样与地图轮廓，因此每位玩家都能回看队伍实际获知的行动。它不增加全知实体复制，也不记录本机相机。Host迁移时关闭旧Authority Epoch、写入迁移关键帧，由新Authority续写新Epoch；播放器按授权Epoch拒绝旧Host的重复事件。

正常任务结束后，Authority发送同一份`DebriefSnapshot`给所有成员。详细统计与回放仅暂存在本地结算区，不上传匹配或Descent活动服务器。迟加入玩家的本地回放从其获得合法状态快照时开始，界面必须明确显示缺失的前半段；其战报可以显示全队最终聚合，但不能声称本地文件含有加入前的可播放轨迹。

## 文件、索引与版本

TRP-004 · PROPOSED · 来源：本轮技术扩写。

回放文件采用分块、压缩、逐块校验的只读临时容器：Manifest→简化世界描述→Keyframe/Event/State chunks→时间与实体索引。独立的小型`DebriefSnapshot`保存详细统计与关键事件引用。记录过程中先写临时尾部；任务结束时只承认校验通过的完整块。播放器先读Manifest与索引，不得为显示结算页扫描整个40至50分钟文件。

每台设备维护明确生命周期：`Recording → DebriefReady → Viewing → ConfirmedForDeletion → Deleted`。`确认并返回壁垒`与`再来一局`都进入`ConfirmedForDeletion`；关闭文件句柄后删除快照、回放块、索引和未完成尾部。异常退出不构成“用户选择保存”：下次启动清理遗留块。奖励、成就和正常进度属于其他持久化系统，不得被一并删除。

简化播放不加载Manifest引用的Gameplay包，而使用记录内的Map Proxy、稳定Type ID、显示名称、类别、形状和状态。由于数据不会跨本局结算永久保留，首发不建设跨Build回放迁移或旧schema兼容层；播放器只读取当前进程支持的ReplaySchemaRevision，解析失败时仍显示能够校验的当局战报，不伪装成可播放。

TRP-005 · DIRECTION · 来源：SRC-USER-2026-09-04-MODULAR-REFINEMENT；本轮回放扩写。

公开模组API的实际消费者包括回放：新增可见实体、武器、状态或任务事件的Gameplay包必须提供稳定Type ID、统计类别和简化显示描述；图标/形状等必要描述随记录暂存。没有注册的私有内存或任意脚本不能写入回放容器。模组产生的名称、图标和事件仍按不可信输入解析，长度、实体数、chunk大小和引用均有边界，禁止容器携带或执行脚本。自定义查看器扩展只能读取已经验证的schema数据。

## 性能、体积与验证

TRP-006 · TEST · 来源：本轮技术扩写。

在代表性40至50分钟四人Operation中同时测记录CPU、磁盘写入、内存、文件体积、首次打开和随机拖动。首轮候选预算为记录线程P95低于0.25ms、额外常驻内存低于64MB、单局`DebriefSnapshot`低于1MB、50分钟`SimplifiedReplayRecord`中位数低于25MB且P95低于60MB、普通SSD持续写入低于0.25MB/s、已建索引后90%的随机拖动在0.5秒内显示可读战术状态；这些都是待原型否决的预算，不是已实现承诺。

验证必须覆盖高密度敌人/投射物、程序地图、秘密未发现、单人/共同/环境潜行破坏、Host硬退出与迁移、客户端断线重连、Mod实体、文件截断、重复chunk、异常退出残留清理和恶意超大字段。统计聚合与Authority Event Journal逐项相等；潜行归因必须由Authority因果链重建一致；记录开关开/关不得改变模拟结果或网络权威顺序。确认离开后不得残留快照、回放块或索引。若简化回放仍超预算，先降低非玩家实体空间采样或只保留关键事件轨迹；不得先删详细战报，也不能暗降战斗模拟。
