---
doc_id: DDD-0012
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 网络与Gameplay架构负责人
canon_basis: "SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE；DDD-0010；DDD-0011"
depends_on: ["DDD-0010-host-authority-gameplay-commands.md", "DDD-0011-tick-architecture.md", "../../technical/network-and-persistence.md", "../../technical/architecture-and-performance.md"]
---

# Replication Architecture：Snapshot + Delta State + Reliable Gameplay Events

## Context / User intent

DDD-0010 已锁定 player-hosted authoritative listen server、Gameplay Command Replication 与 Client Prediction / Server Reconciliation；DDD-0011 已锁定 60 Hz fixed authoritative simulation 与 multi-rate replication。下一项高返工风险问题是：Authority 已经算出的世界状态究竟如何高效、可恢复地投影给每个 Client。

BREACH ECHO 是 1–4 人 PvE FPS，并计划支持大量敌人、Projectile、Proc、Status Effect、可交互设施、Modded Content 与 Host Migration。因此不能把“每个 NetworkObject 自己发 RPC / 每个 Tick 全量发 Transform”作为默认方案；需要统一的状态复制合同，让带宽、CPU、可靠性、Replay、Host Migration 与 Mod schema 都围绕同一语义工作。

用户确认本轮方案可接受并要求继续按既定流程落档。

## USER DECISIONS

DDD-0012-DEC-A · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE。

BREACH ECHO 的默认 Host → Client 复制模型采用：

> **Snapshot + Delta State Replication + Reliable Gameplay Events + Interest Management + Dormancy**

这五项是同一套系统的组成部分，而不是五个互相独立、任意混用的网络风格。

总体数据流：

```text
Committed Authority State
        |
        +--> Snapshot / Delta State
        |
        +--> Reliable Gameplay Events
        |
        +--> Interest / Priority Filter
        |
        +--> Dormancy / Wake Rules
        v
Per-client Replication Frame
        v
Client State Projection
        +--> prediction reconciliation
        +--> interpolation / smoothing
        +--> presentation
```

Client 接收的是 Authority 已经 Commit 的状态/事实投影；Replication 不重新执行 Gameplay 语义，也不让 Client 获得结果权威。

## State replication：Snapshot 与 Delta

DDD-0012-DEC-B · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE。

连续或可覆盖的 Gameplay State 默认通过 **Snapshot / Delta State Replication** 表达，不通过可靠 RPC 流逐项驱动。

典型状态：
- Player / Enemy transform、velocity、stance、movement mode；
- HP / armor / ammo 的当前权威值；
- AI locomotion/combat state；
- Door / interactable 当前状态；
- Objective 当前阶段；
- 可复制 Status / Effect 的当前集合或版本；
- Gameplay Physics Actor 的权威状态；
- 可恢复 Projectile 的必要权威纠错状态。

Server 维护可供每个 Client 使用的 acknowledged baseline。Client 已确认某个 baseline 后，后续 frame 优先发送“相对该已确认状态发生了什么变化”，而不是重复发送整个对象。

概念模型：

```text
Snapshot 120 -> Client ACKs baseline 120

Authority advances...

Replication Frame 121
- Entity 42: Transform changed
- Entity 90: HP changed
- Door 7: unchanged -> omitted
- Objective 2: unchanged -> omitted
```

若某个 Delta 所依赖的 baseline 已不可用、丢失或超出保留窗口，Server 必须能够回退到可解码的较新完整/重基准状态；不能让 Client 永久卡在“缺一个旧Delta所以后面全部无法解释”的状态。

具体 baseline history 深度、full-state cadence、编码与压缩仍由实现/压测决定。

## Dirty state / component granularity

DDD-0012-DEC-C · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE。

Replication 必须支持 **dirty-state / dirty-mask** 或语义等价机制。默认不允许为了判断变化而在每个网络发送周期对每个对象做昂贵的完整序列化与全字段比较。

示意：

```text
Enemy 581
- Transform     DIRTY
- Health        clean
- StatusSet     clean
- CombatState   DIRTY
- Inventory     clean
```

只有需要投影给该 Client 的 dirty component / field 才进入本次 state frame。

Dirty flag 代表“相对可用 baseline 的权威状态需要更新”，不代表“必须可靠发送每一个中间变化”。对于位置等 latest-state-wins 数据，旧中间状态丢失通常可以被更新状态覆盖。

## Reliable Gameplay Events

DDD-0012-DEC-D · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE。

**离散、不可仅靠未来连续状态安全推断、且漏掉会造成语义错误的 Gameplay 事实** 使用 Reliable Gameplay Event 或具备等价可靠语义的事务/消息通道。

典型候选：
- authoritative spawn / despawn identity；
- Inventory / Loot ownership transaction；
- Objective completed / mission phase committed；
- Player joined / left / seat ownership change；
- 需要保证一次性消费语义的交互/事务结果；
- Authority Epoch / Host Migration 关键控制事件；
- 不能只靠瞬时表现重建的关键 Gameplay lifecycle transition。

Reliable Event 仍必须使用稳定 event/transaction ID、sequence 或幂等语义，避免网络重试导致重复执行奖励、资源扣除、Objective complete 等结果。

“Reliable”不代表所有Gameplay都使用可靠消息，也不代表把状态同步变成逐条可靠RPC日志。

## Unreliable / sequenced latest-state data

DDD-0012-DEC-E · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE。

**连续、频繁、旧数据在新数据到达后已经没有价值的状态默认不得依赖可靠有序传输。**

典型：
- Player / Enemy transform snapshots；
- velocity / look / locomotion state；
- 高频 Physics correction；
- 临时 aim / movement projection；
- 其他 latest-state-wins 的高频网络状态。

例如 Player Position 的旧包晚到，不应阻塞更新位置等待旧状态补齐。具体底层 unreliable / unreliable-sequenced / channel API 由未来 Transport Provider 适配，但 Gameplay Replication 层必须表达这种语义，而不能被某个 provider 的 API 名称绑死。

## Interest Management / Relevance

DDD-0012-DEC-F · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE。

Server 为 **每个 Client 单独计算 Replication Interest Set / Relevance**；不存在“只要世界里有对象，就持续复制给所有玩家”的默认规则。

Relevance 不能只用欧氏距离。至少允许考虑：
- 与 owning Player 的距离/空间区域；
- 是否与该玩家处于同一战斗空间/房间/可达区；
- 是否正在攻击、锁定或即将直接影响该玩家；
- 是否属于 Team-critical / Objective-critical 状态；
- 是否会产生玩家应当感知的重要世界事件；
- 对象的重要度类别（Player、Boss、Elite、普通AI、背景对象）；
- 可见性/声学/任务关系等后续系统提供的 relevance hints。

关键原则：**Interest Management 是带宽/CPU优化，不得改变权威世界是否真实存在。** 不在某Client interest set中的敌人仍由Authority存在和模拟；Client只是暂时不需要其高精度投影。

精确 AOI 分区、空间索引、房间图、距离阈值和priority公式仍OPEN，必须由真实关卡与Profiler/带宽测试决定。

## Dormancy / Wake

DDD-0012-DEC-G · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE。

长期不变化、当前不需要连续网络更新的 replicated object 可以进入 **Dormant** 状态。

典型：
- 长时间关闭且无人交互的Door；
- 静止箱体/设施；
- 远处未激活或不相关的实体；
- 已稳定且没有dirty state的世界对象。

Dormant 期间目标网络更新率可以为 0 Hz。对象发生权威状态改变、进入Client relevance、收到会影响Gameplay的交互或系统显式请求时必须 Wake，标记必要状态 dirty，并使Client获得足够的新baseline/state恢复正确投影。

Dormancy 不能造成“Server已经改变但Client永远不知道”的永久分叉；Wake/dirty 规则属于Replication合同的一部分。

## Spawn / despawn 与实体身份

DDD-0012-DEC-H · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE；依赖 DDD-0009 stable package identity 与 DDD-0010 Authority ownership。

Network entity 必须使用 BREACH 自己的稳定运行时 identity / generation 或等价防复用机制。SteamID、Lobby ID、Workshop PublishedFileId、Unity instance ID 或底层transport connection handle不得直接成为Gameplay Entity identity。

Spawn 必须给Client足够信息构造正确的presentation/proxy：stable entity identity、definition/content reference、initial authoritative state、spawn tick/time reference及必要ownership/relevance信息。

Despawn / destruction 必须明确结束该identity epoch，防止迟到packet错误应用到之后复用同一slot的新实体。

## Projectile consequence

DDD-0012-DEC-I · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE；与 DDD-0011-DEC-G 一致。

高数量 Projectile 默认采用 **spawn metadata + local presentation/prediction + authoritative correction/result**，而不是每颗Projectile高频可靠Transform流。

概念信息可以包括：

```text
ProjectileSpawn
- stable projectile/entity ID
- definition ID
- spawn simulation tick
- origin
- direction
- initial velocity
- deterministic/presentation seed where valid
```

Authority 继续负责真实碰撞/伤害结果。具体哪些Projectile需要中途correction、哪些可只同步spawn + hit/despawn、哪些必须持续state replication，由后续Projectile与Lag Compensation设计决定。

## State + Event consistency

DDD-0012-DEC-J · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE。

同一Gameplay结果同时投影为State与Event时必须有一致的版本/sequence边界，避免出现：
- Event先到但State仍旧，Client重复表现/执行；
- State已经包含结果，迟到Event再次产生Gameplay副作用；
- 重连/Join-in-progress依赖历史Event重放才能知道当前世界。

原则：
- **State回答“现在是什么”；**
- **Event回答“发生了哪个不可丢的离散事实/生命周期转换”；**
- Client Gameplay proxy不得通过重复播放Event来重新创造Authority结果；
- Join-in-progress优先从当前权威State / baseline恢复，而不是要求从Run开始重放全部网络事件。

Replay / Audit可以保存更丰富的权威事件流，但不等于网络Client需要长期保留全部历史事件。

## Presentation events are not automatically reliable gameplay events

DDD-0012-DEC-K · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE。

枪口火焰、普通枪声、Camera Shake、局部粒子、轻微Impact VFX等Presentation不能因为“看起来是事件”就自动升级为Reliable Gameplay Event。

Client可以根据本地Prediction、authoritative state变化或低成本presentation signal即时表现。偶尔漏掉一粒火花不能阻塞Gameplay网络；真正改变Gameplay结果的Damage、HP、Ammo、Loot、Objective等仍以Authority state/transaction为准。

## Explicitly rejected / not selected

DDD-0012-DEC-L · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE。

本轮明确不采用以下默认架构：
- **60 Hz全世界全字段Snapshot广播**；
- **每个NetworkObject自行用大量RPC驱动全部Gameplay状态（RPC soup）**；
- **所有网络消息都Reliable**；
- **Player/Enemy位置使用可靠有序队列等待旧包补齐**；
- **只靠距离、不考虑Gameplay关系的单一Relevance规则**；
- **Dormant对象持续发送“我没变”心跳式完整状态**；
- **Join-in-progress必须重放整局RPC/Event历史才能获得当前世界**；
- **每颗Projectile持续高频可靠Transform复制**；
- **底层Steam/EOS/某Unity transport类型渗透为Gameplay replication schema真相**。

## Architectural consequences

推荐职责分层：

```text
Gameplay.AuthoritySimulation
        |
        v
Committed State / Transactions / Facts
        |
        +-----------------------------+
        |                             |
        v                             v
Replication State Builder       Gameplay Event Builder
(dirty/baseline/delta)          (reliable/idempotent)
        |                             |
        +--------------+--------------+
                       v
             Interest / Priority
                       |
                 Dormancy / Wake
                       |
                       v
             Per-client Frames
                       |
                       v
             Transport Adapter
        Steam / EOS / other future provider
                       |
                       v
                    Client
```

Gameplay/Content代码应声明需要复制的语义状态与事件，不自行决定底层packet、socket、provider channel或重发算法。

## Required validation

首个Replication Spike至少应覆盖：
- 4名玩家、不同ping/loss/jitter环境；
- Player transform 30 Hz级别复制 + interpolation；
- 100+ AI 分层relevance与dormancy；
- Door/Objective离散状态；
- reliable spawn/despawn/transaction event；
- 丢失若干delta后能通过后续state/baseline恢复；
- Join-in-progress不重放整局事件即可得到正确当前状态；
- Projectile压力下网络成本不随“每颗弹丸 × 高频Transform”线性爆炸；
- 测量 per-client kbps、packets/s、serialization CPU、replication scheduler CPU、baseline memory 与丢包恢复时间。

任何数值预算在真实Spike前都属于TEST，不在此DDD伪装为已达成SLA。

## OPEN / next gates

本轮仍未锁：
1. Replication frame的具体二进制schema、bit packing、compression；
2. baseline history深度、full/rebase cadence、ACK布局；
3. reliable event channel的具体window/resend/ordering实现；
4. exact per-class replication rate与priority公式；
5. AOI空间结构、room graph和interest阈值；
6. interpolation buffer、extrapolation和correction smoothing参数；
7. Command channel batching / redundancy / ack / resend；
8. Server Rewind / Lag Compensation history window与判定算法；
9. Projectile correction与Physics correction算法；
10. Host Migration snapshot cadence / Authority Epoch恢复协议；
11. 带宽预算、CPU预算和最大活动实体压力；
12. Networking Provider / Transport最终选择。

**下一正式网络 Gate：Lag Compensation / Server Rewind Architecture。**

先确定Hitscan、Projectile与移动目标在延迟下如何使用Command时间和Authority历史做公平命中验证，再继续Host Migration具体协议与Transport Provider选择。

## 2026-09-05 implementation closure

本文件已确认的引擎/内容/命令/60Hz/复制合同继续有效；当时列出的provider、回溯、迁移算法、脚本、旧hash和UI未决项现在由DDD-0015–0017与其责任文档关闭。历史段落用于追溯，不要求重复询问所有者；具体TEST尚未执行。
