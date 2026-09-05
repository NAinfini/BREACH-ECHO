---
doc_id: TECH-MIGRATION
doc_type: technical
stage: BASELINE
updated: 2026-09-05
owner_role: 网络可靠性负责人
canon_basis: "SRC-USER-2026-09-05-STEAM-ONLY-NETWORK-STACK-APPROVED；SRC-USER-2026-09-05-MATCHMAKING-AND-EVENT-BACKEND；当前网络恢复决定"
depends_on: ["network-and-persistence.md", "gameplay-data-command-and-save-contracts.md", "../governance/decisions/network-runtime-and-recovery.md"]
---

# 主机迁移：快照、选主、租约与恢复协议

## 明确保证与不保证

MIG-001 · DECIDED。Authority在玩家机器运行；在线协调器只串行管理Run成员、epoch、租约及恢复证书，不模拟世界。Steam Lobby owner自动转移不等于游戏状态恢复，也不单独证明分区下不会双主，因此不把Lobby metadata当分布式锁。

保证目标是：对**已认证恢复点**不重复、不遗漏已包含的资源/任务事务；新主不会从旧 epoch 继续写；无法证明一致时冻结/挂起而非伪成功。突然断电时，普通战斗瞬态允许回退到最近闭合 Delta，初始目标不超过 500 ms；已经向玩家确认的 Durable 资源/任务事务必须零重复、零遗漏。这不是所有状态零时间回退承诺。正式奖励/任务最终完成只能在最终恢复证书确认后结算。单机离线本地原子快照可恢复，但没有另一台机器保证硬盘故障不丢数据。

## 可恢复状态

MIG-002 · DECIDED。

恢复记录包含RunManifest和包锁、authority tick/epoch、完整实体generation、部位拓扑/生命/装甲、位置速度与游戏物理状态、AI黑板与当前动作、分层RNG状态、任务图与门/电力/Cart、物资实例/归属、玩家Seat/库存/动作阶段、世界重资产位置弹药、已飞弹丸、定时事件、Effect/Proc因果链、Interest重建所需标识、资源事务水位与统计归因水位。Camera、粒子、音频播放游标等非玩法表现可重建。

不能只存Transform，也不能假定PhysX跨CPU逐位确定：恢复使用快照加**已提交的状态变更记录**，不从输入重新模拟整局。每种状态组件提供WriteSnapshot/ReadSnapshot/Validate/ApplyCommittedPatch契约和故障测试；不支持恢复的Gameplay组件不得进公开会话。

## 快照和认证

MIG-003 · DECIDED；频率/预算见测试参数。

Authority 首轮每 10 秒制作一个 tick 边界的自包含 Recovery Baseline，并以 2 Hz 发送可验证 Delta；加入、完成、挂起和 graceful transfer 立即触发边界 Baseline。接收端必须能用 Baseline + 连续 Delta 重建独立完整状态，缺片或摘要不符就请求新 Baseline。两名及以上真人在线时至少一名非 Host 的合格备份持有闭合恢复链；有三名非 Host 时优先复制到两名。候选未持有闭合链就不可选主。

备份校验版本、chunk 长度/hash、状态 digest、Delta 连续性和单调 commit index 后，向协调器提交本人认证的 ACK。Host 提交相同的 `run, epoch, recovery_id, tick, commit_index, state_digest`。协调器只在当前有效租约、相同摘要且满足备份条件时原子前移恢复证书。普通 Delta 可批量覆盖战斗瞬态；Durable Journal 的资源/任务事务需 Primary ACK 后才向玩家发布最终 commit，但不为每发子弹请求云服务。传输/本机状态与认证恢复状态是两个明确水位，UI 不把前者叫做“已安全保存”。

认证后各端保留最近两个完整恢复点和其依赖块；旧块只在新点完全独立且ACK完成后回收。有单个玩家在线的Run只能本地恢复；它不能被宣传为跨机容灾。Host没有可用备份或同步持续滞后时，进入冻结恢复/挂起流程，不继续累积不可恢复的长局。

## 租约和选主

MIG-004 · DECIDED。

协调器以RunID路由到唯一Durable Object，以持久化事务更新`epoch, holder, lease_expiry, membership_revision, recovery_certificate`。所有请求需验证Steam身份绑定的短期会话票据、成员身份、nonce、单调序号、限流和最大payload。一个普通成员不能写另一个成员的备份ACK。备份摘要不是反作弊证明；恶意玩家主机作弊仍是非竞技产品接受的限制。

初始租约4秒、Host每1秒续约、客户端安全余量0.5秒。Host在发送续约前记录单调时钟起点，收到回应后仅使用该请求起点加保守TTL减余量的期限；不能用收到包的时间重新获得完整旧TTL。挂起/系统睡眠、时钟异常或响应过迟必须使本地租约失效。客户端拒绝epoch回退、过期状态和未经协调器确认的新主；网络断裂后不能仅凭“我还在Lobby里”继续提交。

正常换主：旧Host冻结tick→交付最终认证点→候选完成恢复校验→协调器原子关闭旧租约并增加epoch→新Host取得新租约→发布baseline→所有成员ACK后继续。旧Host先停止写，不能同时发新旧数据。

突然失联：客户端冻结表现和输入提交→查询协调器→等待旧租约过期→按候选排序收集可用性→只从持有当前认证恢复点的成员中选取→协调器用比较并交换原子发新epoch租约→恢复并重新建立FishNet会话→发送当前世界baseline与Seat重绑定→ACK后继续。候选排序先满足内容/证书/可达性硬条件，再比较实测CPU余量、持续上行、丢包/jitter、热稳定性；同分用稳定内部ParticipantID排序。Lobby owner或PartyLeader不享有强制Host优先级。

没有合格候选、状态digest不符、缺旧hash或协调器不可用：`RecoveryBlocked`，保存已有材料，明确失败原因和可采取的操作；不能回到满资源任务起点、伪造完成或自动创建另一条同Run历史。旧Host回来只能以Client身份加入新epoch。

## 分区安全和服务代价

MIG-005 · DECIDED。

不能同时承诺任意网络分区下每一侧都继续玩与唯一权威。选定一致性优先：拿不到有效租约的一侧停。服务端epoch检查、客户端保守到期及恢复证书检查必须一起实现；只有一个UUID字段不构成安全协议。TTL/时钟漂移/进程睡眠/超时的假设和故障注入结果要随实现文档记录，不宣称形式化证明已完成。

协调器无完整存档和语音；运行期间约每秒一次 Host 续约，并接收有界的恢复证书/备份 ACK，按真实消息量计费，不宣称免费无限服务。空闲会话释放连接，已结束会话删除短期租约和非必要成员数据；防重放最终 ResultID 保留于玩家进度声明记录。配置请求/创建 Run 限额、并发准入、账单告警和停服开关。预算不足时拒绝新在线 Run 并说明原因，不能继续收费后隐藏风险；已开局保持到合法挂起点的策略要做负载演练。

## 必跑故障矩阵

MIG-006 · TEST。

分别在拾取、扣Cell、融合实验、重资产换手、倒地、Projectile飞行、关门、结算和包激活时杀进程；测试20次功能样本与更长压力批次。覆盖0/80/150/250ms RTT、丢包0/2/5%、乱序、重复、网络分区、Host只断Steam/只断协调器、协调器重启、旧Host回归、备份磁盘满、全部玩家退出。检查认证点资源守恒、唯一epoch、一次ResultID、状态digest、统计去重和freeze期间SimulationTime不动。8秒内恢复19/20仍是早期目标，不是服务SLA；失败不得通过调低一致性要求“达标”。
