---
doc_id: DECISION-FIXED-TICK-MULTIRATE
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 网络与Gameplay架构负责人
canon_basis: "SRC-USER-2026-09-05-TICK-ARCHITECTURE；DECISION-HOST-AUTHORITY-COMMANDS；DECISION-STATE-REPLICATION"
depends_on: ["host-authority-and-gameplay-commands.md"]
---

# Tick 架构：固定 60 Hz 权威模拟与多频率更新

## 背景与用户意图

在 DECISION-HOST-AUTHORITY-COMMANDS 已锁定 player-hosted authoritative listen server、Gameplay Command Replication、Client Prediction / Server Reconciliation 后，需要确定 Authority Simulation 的时间基线，以及 Network Replication、AI Brain、Physics、Presentation 是否与同一频率绑定。

目标不是追求一个越高越好的“全游戏 Tickrate”，而是让 BREACH ECHO 的 1–4 人 PvE FPS 在枪感、移动精度、大量敌人、Projectile / Proc / Status Effect 压力、Listen Server CPU 预算、网络带宽与 Mod 可预测性之间取得稳定基线。

用户确认本轮方案可接受并要求落档。

## 用户决定

SIMTICK-001 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE。

**Authoritative Simulation 使用固定 60 Hz。**

```text
Authoritative Simulation Rate = 60 Hz fixed
Fixed Step                 = 16.666... ms
```

该值是 Gameplay/Protocol 级基线，不随 Render FPS 改变，也不作为普通 Server/Host 用户可调参数。

原因：
- 30 Hz 的 33.33 ms 逻辑粒度对第一人称射击、移动、Dodge、Hitscan、Projectile、Ability timing 与复杂 Proc 偏粗；
- 120 Hz 会显著放大 Listen Server 的移动、碰撞、Physics、Command processing 与 Gameplay 热路径成本，而 BREACH ECHO 不是以竞技电竞级 tickrate 为核心价值；
- 60 Hz 为射击响应、模拟精度、Host CPU 与未来高实体数压力之间的默认折中。

这不是“所有系统都必须每秒执行60次”的承诺；只有权威模拟时间基线固定为60 Hz。

SIMTICK-002 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE。

**Simulation Tick、Network Replication Rate、AI Brain Rate、Physics Update、Render FPS 必须解耦。**

基础架构：

```text
Render / Presentation     = variable, frame-rate dependent
Authority Simulation      = 60 Hz fixed
Gameplay Physics          = authority simulation aligned unless a later system decision explicitly substeps
AI Brain / decision       = lower-rate scheduled work
Network Replication       = lower/adaptive rate by object importance
```

禁止用一个“Global Tickrate”同时决定渲染、AI思考、Snapshot发送、所有Actor更新和Gameplay物理。

## 命令频率

SIMTICK-003 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE；依赖 DECISION-HOST-AUTHORITY-COMMANDS Gameplay Command 模型。

Gameplay Command Layer 与 60 Hz Simulation 对齐，可按 simulation step 产生语义 Command Frame。Client → Authority 的逻辑 Command cadence **最高按60 Hz处理**，但 Gameplay 层不能假设“一帧Command = 一个网络Packet”。

Transport 层允许：
- 多个 Command Frames 合并为一个 packet；
- 附带前序 command redundancy / sequence 信息；
- idle 时降低发送；
- 使用 ack / batching / resend 策略。

这些 packetization 细节仍由后续复制或传输决策记录决定。

核心边界：Gameplay Command 语义与网络 packet 结构解耦。

## 复制频率基线

SIMTICK-004 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE。

Host → Client 不以 60 Hz 全量复制世界。当前基线方向：

| 类别 | 默认目标频率 / 行为 |
|---|---:|
| Player / Boss / critical combat state | 约30 Hz |
| 近距离高相关战斗 AI | 约15–20 Hz |
| 普通战斗 AI | 约10–15 Hz |
| 远距离低相关 AI | 约5–10 Hz |
| 静止 / Dormant entity | 0 Hz until dirty/wake |
| 静态门、箱子、Objective等离散状态 | event-driven / dirty-state driven |

这里锁定的是 **关键状态约30 Hz、其余对象按重要性降低并支持Dormancy/事件驱动** 的架构方向；精确阈值、距离、优先级预算与动态升降算法仍待 Replication Architecture 裁决和实测。

Client 使用 interpolation / smoothing 呈现远端实体，因此远端网络 Snapshot 频率不等于玩家显示帧率。

## AI 调度

SIMTICK-005 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE。

AI 的真正 Gameplay Authority 继续由 Server 持有，但 **AI Brain / high-level decision 不在每个60 Hz Tick对每个敌人完整执行。**

默认方向：
- 高层 AI Brain / target selection / ability choice：约5–10 Hz；
- 低层已确定 Intent 的 movement / collision / attack timing：继续由60 Hz Authority Simulation 执行；
- AI Think 必须 stagger / time-slice，不允许大量AI在同一Simulation Tick集中Think造成CPU spike。

示意：

```text
Authority Simulation @ 60 Hz
    |
    +-- apply current movement/attack intent every tick
    |
    +-- AI Brain groups scheduled across ticks
         Tick N   -> cohort A
         Tick N+1 -> cohort B
         Tick N+2 -> cohort C
```

具体 AI cohort 大小、priority、LOD 与最大决策延迟仍需真实敌人数和Profiler数据确认。

## 物理边界

SIMTICK-006 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE；与 DECISION-HOST-AUTHORITY-COMMANDS Gameplay/Cosmetic Physics 划分一致。

Gameplay-relevant Physics 默认跟随 60 Hz Authority Simulation；Cosmetic Physics 继续允许 Client-local，且不要求权威复制。

60 Hz authority 不等于每个 Gameplay Physics Actor 以60 Hz发送Transform。Physics replication 可以降低到15–30 Hz或事件/纠错驱动，再由Client插值/预测。

高速 Projectile / fast collision 的精度问题优先通过 sweep、CCD、有限substep或专门Projectile算法解决，不通过把全局 Simulation Tickrate 提升到120 Hz解决。

## 投射物联网影响

SIMTICK-007 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE。

针对可能出现的大量 Projectile / Multishot / Ricochet / Fragment / Proc chain，禁止把“每个Projectile每秒复制30–60个完整Transform”作为默认网络模型。

方向是：Authority 负责真实 Projectile Simulation / collision；Client 获得稳定的 spawn metadata（例如 stable ID、SpawnTick、position、direction、velocity、definition/seed），本地进行 presentation/prediction；只有必要时进行 authoritative correction / hit result replication。

该条锁定的是“不要高频全量复制每颗Projectile Transform”的架构边界；Projectile Prediction、碰撞算法、纠错阈值及可靠性通道在后续Projectile/Replication设计中细化。

## 追帧与过载行为

SIMTICK-008 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE。

固定60 Hz Simulation 必须有 **bounded catch-up**，禁止无限补Tick。

Host发生短时hitch时允许有限数量的catch-up steps；严重落后时必须有最大catch-up budget，防止：

```text
lag -> calculate unlimited missed ticks -> CPU saturation -> more lag -> spiral of death
```

过载时优先削减/延迟：
- 低优先级 AI 思考；
- 后台模拟；
- 低优先级复制；
- 纯装饰与表现工作。

不得为了追帧静默丢掉已合法发生的：
- 玩家移动 / 动作语义；
- 伤害 / 生命值事务；
- 武器开火；
- Gameplay Physics结果；
- Gameplay-relevant Proc / resource / mission结果。

精确的最大catch-up tick数、hitch阈值与降级策略属于性能Spike / TEST参数，不在本DDD写死。

## 模组时间合同

SIMTICK-009 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE。

Mod API 不允许依赖 Render FPS 产生 Gameplay 结果。禁止把 `OnFrame()` 一类表现帧回调作为伤害、计时、Cooldown或资源规则的Gameplay时间基线。

Mod Gameplay接口优先提供：
- 模拟时间（SimulationTime）/ 固定玩法时间；
- `OnSimulationTick(dt)`（仅在确实需要时）；
- `ScheduleAfter(seconds)`；
- `ScheduleEvery(seconds)`；
- `OnDamage` / `OnProjectileHit` / `OnStatusApplied` 等事件驱动回调。

Mod应优先event-driven，避免所有Mod在每个60 Hz Tick轮询全部状态。时间API使用秒/Simulation Time，而不是鼓励“每60 tick做一次”的硬编码。

## Tickrate 可配置性

SIMTICK-010 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE。

**60 Hz authoritative simulation tickrate 不作为普通玩家/房主Server配置项。**

不提供类似：

```ini
ServerTickRate=30
ServerTickRate=120
```

作为正式兼容表面。原因是Gameplay timers、Physics、Prediction、Replay、Lag Compensation、Mod行为和协议时间参考都需要一个稳定Simulation时基。

未来若研发分支为benchmark临时改变tickrate，只能作为开发实验，不产生对Mod/Save/Network兼容的产品承诺。

## 明确淘汰与未选择

SIMTICK-011 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE。

本轮明确未选：
- **30 Hz global authoritative baseline**：成本低但对本项目FPS核心模拟粒度偏粗；
- **120 Hz global authoritative baseline**：收益不足以抵消Listen Server CPU与高实体压力；
- **所有系统统一60 Hz**：AI Brain、远端Replication、Dormant对象不应被迫每tick完整处理；
- **60 Hz全世界全量Snapshot**：带宽和序列化成本过高；
- **每颗Projectile高频Transform复制**：高弹幕/Proc构筑下不可扩展；
- **Render FPS驱动Gameplay/Mod时间**：会导致不同帧率产生不同Gameplay结果；
- **用户可自由修改Simulation Tickrate**：会破坏稳定时间合同与Mod/Replay/Prediction基线。

## 架构影响

标准时间/数据流：

```text
Input / Gameplay Commands
          |
          v
Authority Simulation @ fixed 60 Hz
          |
     +----+-------------------+
     |                        |
Gameplay Physics        AI intent execution
@ simulation rate       @ simulation rate
                              |
                      AI Brain scheduler
                         ~5-10 Hz / staggered
          |
          v
Committed Authority State
          |
          v
Replication Scheduler
  +-------+---------+----------------+
  |                 |                |
Critical ~30 Hz   AI 5-20 Hz     Dormant/Event-driven
  |                 |                |
  +-----------------+----------------+
                    |
                    v
                 Client
        prediction / reconciliation /
        interpolation / presentation
                    |
                    v
             variable Render FPS
```

该架构要求后续系统显式声明自己的：
- 模拟责任；
- 决策 / 更新频率；
- 复制频率 / 事件政策；
- 优先级 / 相关性；
- 过载降级行为。

禁止默认继承“60 Hz就全部执行60次”。

## Replication 交接与待实测参数

DECISION-STATE-REPLICATION 已完成本DDD原先的下一Gate，正式锁定 Snapshot + Delta State Replication + Reliable Gameplay Events + per-client Interest Management + Dormancy；baseline/dirty-state、latest-state-wins 与 reliable transaction 的语义边界，以及 Join-in-progress / Projectile 的复制方向均见[状态复制架构](state-replication.md)。

因此以下不再是架构选择，只是必须通过 Spike 和性能测试固定的实现参数：
1. Replication frame具体二进制格式、compression/bit packing；
2. baseline history深度、rebase cadence、ACK布局；
3. Interest/AOI算法、priority公式与精确动态频率；
4. Client interpolation buffer、extrapolation和correction smoothing；
5. Command batching、ack、redundancy与底层可靠/不可靠channel映射；
6. Projectile prediction/correction实现；
7. Physics correction/smoothing策略；
8. 目标带宽预算与Host CPU预算。

Lag Compensation / Server Rewind已由[延迟补偿决定](lag-compensation-and-server-rewind.md)完成；150 ms Max Rewind仍只是TEST参数。Session/Lobby、SDR/Transport、FishNet与Host Migration原则已由[网络运行与恢复](network-runtime-and-recovery.md)确认，具体频率和性能仍须Spike。
