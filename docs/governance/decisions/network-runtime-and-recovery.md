---
doc_id: DECISION-NETWORK-RUNTIME-RECOVERY
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 网络与在线服务负责人
canon_basis: "SRC-USER-2026-09-05-STEAM-ONLY-NETWORK-STACK-APPROVED；SRC-USER-2026-09-05-MATCHMAKING-AND-EVENT-BACKEND；当前网络技术证据"
depends_on: ["agent-first-modding-runtime.md", "host-authority-and-gameplay-commands.md", "fixed-tick-and-multirate-simulation.md", "state-replication.md", "lag-compensation-and-server-rewind.md"]
---

# 网络运行与恢复：Steam + FishNet + 小型协调器

## 决定

NETWORK-RUNTIME-001 · CANON/DIRECTION。

初始版本使用一套网络栈，不并行维护替代方案：

```text
Steam 身份 / 好友 / 邀请 / Lobby / 搜索
                  |
Steam Datagram Relay + ISteamNetworkingSockets
                  |
FishNet 连接、预测与网络对象基础设施
                  |
BREACH Command / Replication / Recovery Schema
                  |
BREACH 小型协调器：Run membership / lease / epoch / recovery certificate
```

对局 Authority 仍运行在玩家主机；协调器不模拟敌人、物理、任务或 60 Hz 世界，也不保存完整对局。它只解决 Steam Lobby 无法可靠解决的唯一新主、租约、分区与恢复证书问题，并可在未来复用为 Descent 公共活动结果的幂等汇总入口。

## 分层责任

| 层 | 唯一选择 | 拥有什么 | 不拥有什么 |
|---|---|---|---|
| 商业与公开平台 | Steam | 销售、身份、好友、邀请、Lobby、公开匹配入口 | Gameplay Entity、存档和奖励真相 |
| 公网传输 | SDR / ISteamNetworkingSockets | NAT/Relay、可靠与不可靠消息 | Command 语义、选主与状态格式 |
| Unity 网络框架 | FishNet；FishySteamworks 先做 Adapter Spike | 连接生命周期、预测基础、观察者与序列化设施 | 游戏规则、Package Lock 与恢复合同 |
| Gameplay 网络 | BREACH 自有 schema | Command、Snapshot/Delta/Event、Interest、Dormancy、稳定 ID | Steam 类型和 Unity Scene Instance ID |
| 在线协调 | 小型 TypeScript Worker + 每 Run 一个 Durable Object | Steam 身份绑定、成员、lease、epoch、恢复证书 | 60 Hz 模拟、完整世界、语音和 Mod 文件 |

NETWORK-RUNTIME-002 · CANON。

首发不接入 EOS、Unity Relay/Sessions/Auth、NGO、Photon 或第二公开 Mod 平台。若 FishySteamworks 无法满足 channel、队列、IL2CPP、Steam Deck 或断线要求，只替换薄 Adapter，不引入第二套 Gameplay 网络框架。离线 Solo 不启动 Steam 匹配或协调器。

## 会话与消息原则

NETWORK-RUNTIME-003 · CANON/DIRECTION。

Steam Lobby 保存可搜索的小型元数据；完整 RunManifest、Package Lock、世界状态和恢复流通过游戏连接交换。Steam Lobby Owner、Party Leader、Hub Owner 与 Simulation Host 是四个概念，任何一个都不自动取得世界写权限。

连续可覆盖状态使用 unreliable latest-state-wins；Spawn/Despawn、Inventory/Loot、Objective、Seat 与 epoch 使用 reliable idempotent event；Package/Join/Recovery baseline 使用限速可靠分块。Fire/Reload/Interact 等一次性 Command 允许有限冗余并由 Authority 按 ID 幂等消费。所有消息携带稳定 Run/Entity/sequence/epoch 语义，不把底层 SDK 枚举写进玩法协议。

## 主机迁移

NETWORK-RUNTIME-004 · CANON/DIRECTION。

当前 Host 向 Primary 与 Secondary Backup 发送可恢复状态。状态由低频自包含 Baseline、连续 Delta 和即时 Durable Journal 组成；关键资源、任务、重资产与结算事务必须由合格 Primary 确认后才成为可向玩家呈现的 durable commit。协调器只保存当前闭合状态的摘要证书、租约和 epoch，不接收完整世界。

首轮测试参数是 `10 秒 Baseline + 2 Hz Delta + 即时 Journal`；普通战斗瞬态目标回退不超过 500 ms，已确认 durable transaction 必须零重复、零遗漏。以上都是 TEST，不是宣传 SLA；数据表只在[主机迁移合同](../../technical/host-migration.md)和[测试配置](../../production/initial-test-parameters.md)维护。

正常换主先冻结事务并封闭最终恢复点，再由协调器撤销旧租约、增加 epoch、向新主发租约。突然失联时所有 Client 冻结 Simulation，等待旧租约失效；只有持有当前闭合证书且通过硬条件的候选能获得新 epoch。协调器不可用、没有合格备份、状态摘要不符或缺少精确 Mod hash 时进入 `RecoveryBlocked`，不能在网络分区两侧各自继续一条世界历史。

## 拒绝的方案

- 不把 Steam Lobby Owner 自动转移误称为 Host Migration。
- 不让客户端提交可信伤害、战利品、任务完成或公共活动进度数值。
- 不把整个对局搬到官方 60 Hz 专服，只为获得主机迁移。
- 不用 Unity Physics 输入重放假装完全确定；恢复当前认证状态。
- 不为 PVE 建竞技反作弊，但仍验证身份、schema、幂等事务和跨账号写入。
- 不在协调器故障时静默分叉，也不伪造补偿奖励或通关。

## Gate 与重审条件

必须在两台以上真实设备、独立 Steam 账号和不同公网条件下验证 Lobby、SDR、Package Lock、Join-in-progress、Host 硬退出、连续两次迁移、睡眠/唤醒、Steam/协调器单边分区、旧 Host 回归、缺旧 hash、100+ AI 与 Projectile 压力。`20 次至少 19 次在 8 秒内恢复`仍是早期功能目标，不是已通过结果。

若发生双主、durable transaction 重复/遗漏、关闭协调器后仍有旧 Host 写入，或真实成本超过所有者批准预算，该 Gate 失败。先修协议或缩减承诺，不以降低一致性标准宣布通过。
