---
doc_id: DDD-0010
doc_type: decision
stage: DRAFT
updated: 2026-09-05
owner_role: 网络与Gameplay架构负责人
canon_basis: "SRC-SSOT-2.0 §21、§36；SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS"
depends_on: ["../decisions-and-questions.md", "../../technical/network-and-persistence.md", "DDD-0009-agent-first-modding-runtime.md"]
---

# Host Authority 与 Gameplay Command Replication

## Context / User intent

在 Steam-only 商业发行/Workshop Mod 分发、平台服务与运行时解耦、玩家房主 Operation 会话以及匹配控制面已经讨论后，下一项高返工风险问题是实际 Gameplay Simulation 的权威模型。目标是让 BREACH ECHO 的 1–4 人合作射击既保持即时枪感，又不把生命、伤害、AI、战利品、任务或资源结果交给各 Client 自行决定；同时架构必须继续适配 Mod、Replay、Host Migration、未来 Community Dedicated 与可能的 Headless Server Runtime。

用户在比较原始 Input Replication 与语义 Gameplay Command Replication 后明确选择 **方案 B：Gameplay Command Replication**，并确认本轮其余权威模型建议均可接受。

## USER DECISIONS

DDD-0010-DEC-A · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS。

BREACH ECHO 的默认多人模拟采用 **player-hosted authoritative listen server**。Gameplay-Relevant State 的最终真相由 Server Simulation 持有；Client 拥有自己的输入意图和本地表现，但不拥有 Gameplay Result。Solo 仍可在本地运行同一 Authority Runtime；该权威合同不得绑死为只能 Listen Server，未来 Community Dedicated / Headless Dedicated 应复用同一 Server Simulation 接口，而不是重写第二套 Gameplay 逻辑。

核心原则：

> Client sends intent; Authority decides result.

Client 可以请求“移动、开火、换弹、使用技能、交互”，但不能宣告“我现在在这里、我已经命中、敌人掉了多少血、我获得了什么物资”。

DDD-0010-DEC-B · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS。

网络 Gameplay 输入采用 **Gameplay Command Replication**，不把键盘、鼠标、手柄或 Steam Input 的原始设备事件作为 Gameplay 网络协议。

标准层级为：

```text
Input Device
  -> Input Mapping
  -> Gameplay Command Layer
  -> Local Prediction where allowed
  -> Network Command Transport
  -> Authoritative Simulation
  -> Replication / Reconciliation
  -> Presentation
```

典型 Command 是 `MoveCommand`、`FireWeaponCommand`、`ReloadCommand`、`ActivateAbilityCommand`、`InteractCommand`、`JumpCommand`、`DodgeCommand` 等语义动作，而不是 `KeyW=true`、`LeftMouse=true`。

这一层必须与输入设备解耦，使键鼠、手柄、Steam Input、可访问性重绑、Bot、Replay、Debug Harness 等来源可以产生同类 Gameplay Command，而无需让 Authority 认识具体硬件输入。

DDD-0010-DEC-C · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS。

**Host 本地玩家与远程 Client 必须经过同一 Gameplay Command / Authority Pipeline。** Listen Server 可以在进程内绕过实际网络序列化/传输开销，但不得绕过 Authority 规则直接改世界状态。禁止把 Host 玩家发展为长期的 `if (IsHost) { mutate gameplay directly; }` 特例路径。

这条规则的目的不是制造额外延迟，而是保证：
- Host 与 Client 使用相同 Gameplay 语义；
- Replay、Bot、测试和 Dedicated Server 可复用同一路径；
- Host Migration 不需要把一套 Host-only Gameplay 状态翻译成另一套 Client 状态；
- Mod API 不需要区分“房主专用玩法调用”和“正常玩法调用”。

DDD-0010-DEC-D · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS。

玩家移动和其他高响应本地动作允许 **Client-Side Prediction + Server Reconciliation**。Client 可以在收到 Authority 回包前根据已提交 Command 立即进行可预测的本地模拟和表现；Authority 随后返回已确认状态/Command cursor。预测出现差异时 Client 以 Authority 为最终真相进行 reconciliation，必要时 replay 尚未确认的本地 Commands。

Prediction 只获得“临时表现权”，永远不会因为本地先显示结果就升级为 Gameplay Authority。

## Authority ownership matrix

DDD-0010-DEC-E · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS。

以下默认属于 Authority，除非未来某个系统 DDD 明确改变：

| 状态/决定 | 默认权威 |
|---|---|
| Player input intent / command ownership | owning Client 产生；Authority 验证与执行 |
| Player authoritative transform / movement result | Authority |
| HP / armor / downed / death state | Authority |
| Ammo / magazine / reload completion | Authority |
| Fire-rate legality / weapon state | Authority |
| Hit validation / damage / crit / reaction | Authority |
| Buff / debuff / status effect gameplay state | Authority |
| AI brain / target / attack decision | Authority |
| Enemy spawn / despawn / death | Authority |
| Loot spawn / roll / pickup ownership | Authority |
| Objective / mission / director state | Authority |
| Door / trigger / gameplay interactable state | Authority |
| Procedural-generation seed and authoritative generation state | Authority |
| Gameplay-relevant physics | Authority |
| Cosmetic VFX / SFX / camera / HUD / screen shake | local Client |
| Cosmetic animation and non-gameplay physics | local Client |

Client 可以提前播放本地枪口火焰、枪声、后坐力、相机反馈等 presentation，以避免等待 RTT；这些表现不能自行提交命中、伤害、资源或任务结果。

## Command contract and validation

DDD-0010-DEC-F · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS。

Gameplay Command 应表达“玩家想做什么”，并携带足够的时间/顺序信息供 Prediction、去重、Replay 与 Lag Compensation 使用。具体二进制 schema 仍待实现，但概念上至少支持：

```text
CommandHeader
- player / seat identity
- sequence
- simulation tick or equivalent authoritative time reference
- command type

FireWeaponCommand
- weapon slot / stable weapon instance reference
- aim direction or equivalent aiming intent
- relevant command-time metadata
```

Client **不得**把以下字段当作可接受的权威结果上传：任意最终 Damage、Enemy HP、Loot Result、Mission Result、最终 Player Transform，或“目标一定被我命中”的未经 Authority 验证声明。

Authority 必须验证命令所有权、Actor 当前状态、资源、武器状态、射速/冷却、生命状态、Command 顺序以及相关规则后才产生 Gameplay Result。

## Shooting and lag compensation boundary

DDD-0010-DEC-G · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS。

射击采用 Authority 命中/伤害判定，同时保留 **Server Rewind / Lag Compensation** 作为正式网络方向，避免移动目标在合理 RTT 下因 Authority 当前时刻已经移动而把 Client 当时真实瞄准的命中全部判空。

已锁的是“命中结果由 Authority 决定”和“需要基于 Command 时间参考设计 Lag Compensation”；以下仍 OPEN：rewind history 时长、最大可接受 RTT、不同武器类别是否使用不同 rewind、hitscan 与 projectile 的精确算法、碰撞历史压缩、Host 本地玩家是否也统一进入历史查询接口、异常高延迟/旧 Command 的拒绝规则。

客户端不能借 Lag Compensation 自行指定 Damage 或最终 Target；Authority 只使用受限 Command 时间和历史状态重新验证。

## AI and physics boundary

DDD-0010-DEC-H · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS。

AI 的真正决策只运行在 Authority：AI Brain、Target Selection、Attack Decision、Ability Decision、Gameplay path/steering result 与造成 Gameplay 影响的行为均由 Authority 决定。Client 负责复制后的插值、动画、音频和视觉表现，不各自独立运行可改变结果的 AI Brain。

物理明确分成：
- **Gameplay Physics**：能造成伤害、阻挡、资源变化、目标变化、推动重要实体或影响任务结果，由 Authority 持有；
- **Cosmetic Physics**：纯装饰、不会改变 Gameplay 结果的碎片/小物体等，可以 Client-side，不要求全量复制。

不是“所有物理都联网”，也不是“所有视觉对象都必须服务器模拟”。

## Threat model / host cheating

DDD-0010-DEC-I · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS；与 SRC-USER-2026-09-05-PVE-NO-ANTI-CHEAT 一致。

本作为 Mod-friendly 合作 PVE，**不以阻止房主修改自己的 Listen Server 为架构目标**。Server Authority 主要用于一致性、Client 结果边界、存档/事务正确性、同步和良好网络体验，而不是把本地 Host 变成不可作弊的竞技服务器。

Client 侧仍不能因为“PVE 不做反作弊”就获得任意写 Damage/HP/Loot/Objective 的协议权限；这是数据所有权和一致性边界，不是竞技封禁系统。

## Explicitly rejected / not selected

DDD-0010-DEC-J · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS。

本轮明确未选：
- **Raw Input Replication 作为主要 Gameplay 网络协议**：不直接把键鼠/手柄事件作为网络 Gameplay 真相；
- **Client-authoritative Gameplay Result**：不接受 Client 直接写命中、伤害、生命、战利品、任务结果；
- **Host-only gameplay bypass path**：Host 本地玩家不维护第二套直接变更世界的代码；
- **完全等待 Server 回包才响应移动/枪口表现**：高响应动作允许预测与本地 presentation；
- **所有物理/动画/VFX 都由 Server 全量驱动**：只有 Gameplay-relevant state 需要 Authority。

## Architectural consequences

该决定要求 Networking 与 Gameplay 的依赖方向保持清晰：输入设备层不渗透到网络协议；Gameplay Command 类型应位于可由 Runtime、Bot、Replay 和测试共享的模块；Transport Provider 不应决定 Gameplay Command 语义；Authority Simulation 产生的事件/状态应可被 Replication、Persistence、Host Migration、Debrief/Replay 消费。

推荐模块边界方向：

```text
Input / Accessibility
        |
        v
Gameplay.Commands <---- Bot / Replay / Test Harness
        |
        +---- Prediction (Client)
        |
        v
Networking.CommandTransport
        |
        v
Gameplay.AuthoritySimulation
        |
        +---- Replication
        +---- Persistence / Snapshot / Journal
        +---- Debrief / Replay Events
        +---- Host Migration State
```

Transport 可以是 Steam/EOS/其他 provider adapter 的实现细节，但不得让 `SteamInput`、Workshop ID、Lobby provider 类型或底层 socket 类型成为 Gameplay Command schema 的身份真相。

## Resolved follow-up: Tick Architecture

本文件最初把 Simulation Tick、Network/Replication rate 与系统分频列为下一设计Gate。用户随后已确认 [DDD-0011 Tick Architecture](DDD-0011-tick-architecture.md)：固定60 Hz Authority Simulation、约30 Hz关键状态复制方向、AI/远端对象低频自适应更新、AI Brain约5–10 Hz staggered、Render解耦、Gameplay tickrate不作为普通用户配置。以后不得继续把这些基础原则写成OPEN。

## OPEN / next gates

当前仍未锁以下实现参数：
1. Snapshot / delta / event replication 的最终组合；
2. Interest management / relevance / dormancy 的具体规则；
3. Command batching、ack、resend、可靠/不可靠通道划分；
4. 具体 Transport Provider 与 socket API；
5. Server Rewind history window 与 hitscan/projectile 细节；
6. 移动 prediction/reconciliation 的误差阈值与 smoothing；
7. Host Migration 的选主、快照频率和恢复时限实现；
8. 带宽预算、最大敌人数与 CPU budget；
9. Dedicated Server 的包装、部署和管理体验。

**下一正式设计 Gate：Replication Architecture。** 先裁决 Snapshot + Delta + Event、state baseline / dirty mask、interest set / dormancy 与可靠性语义，再继续细化 Rewind、Host Migration 和 Transport Provider。
