---
doc_id: DECISION-LAG-COMPENSATION
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 网络与Gameplay架构负责人
canon_basis: "SRC-USER-2026-09-05-LAG-COMPENSATION-BASELINE-APPROVED；SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS；SRC-USER-2026-09-05-TICK-ARCHITECTURE；SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE"
depends_on: ["host-authority-and-gameplay-commands.md", "fixed-tick-and-multirate-simulation.md", "state-replication.md"]
---

# 延迟补偿与服务器历史判定

## 决策目标

让80至120 ms RTT下的玩家射击移动敌人时仍得到可信反馈，同时不让高延迟命令倒转已经提交的世界状态。BREACH: ECHO是合作PvE，可以适度偏向“玩家射中AI时感觉公平”，但不能以穿过已关闭掩体、重复伤害或撤销队友行为为代价。

## 已确认规则

LAG-001 · CANON · 来源：SRC-USER-2026-09-05-LAG-COMPENSATION-BASELINE-APPROVED。

所有命中与伤害仍由Authority决定。Lag Compensation只允许Authority查询受限历史以验证一次Command，不把整个Simulation、AI、Physics或世界状态真正倒带。历史查询产生的合法结果只在当前Authority Tick提交一次。

LAG-002 · CANON/DIRECTION · 来源：同上。

Hitscan使用射手的可信Command时间参考，由Server映射到自身时间轴，再查询当时相关敌人的历史Hitbox/Pose。Client不能直接指定目标、命中点、Damage或任意回看时间；过旧、未来、重复或无法映射的Command由Authority拒绝或夹断到允许范围。

LAG-003 · CANON · 来源：同上。

静态世界几何始终参与Authority射线。门、可破坏墙、移动平台等动态掩体采用保守的双重否决：历史状态或当前已提交状态任一能够挡住射线，该次Hitscan就不能穿过。代价是极端竞态下会牺牲少量射手宽容，但不会出现队友已经关门后，旧高延迟子弹仍穿门改变当前世界的结果。

LAG-004 · CANON · 来源：同上。

具有可感知飞行时间的Projectile不做整段Server Rewind，也不沿历史世界补跑。Authority收到并验证开火Command后，在当前世界生成并模拟Projectile；Client可以立即播放枪口、后坐力与预测弹道表现，但碰撞/伤害以Authority为准。功能上近乎瞬时、无法靠玩家观察飞行来瞄准的弹体，应按Hitscan家族设计，而不是伪装成Projectile绕开规则。

LAG-005 · CANON/DIRECTION · 来源：同上。

Melee允许比Hitscan更短的目标Hitbox历史查询，以补偿近身移动造成的视图差；具体窗口和swept-volume算法属于TEST。Explosion、范围伤害、交互、门、拾取、资源、Objective和AI攻击默认只按当前Authority状态结算。未来若某一动作确需例外，必须在该动作家族规则中显式登记，不能继承一个全局“全部回滚”开关。

LAG-006 · CANON · 来源：同上。

高延迟玩家超过允许历史窗口时，Server夹断可回看的时间，不为了Lag Compensation直接踢出玩家，也不让旧Command修改已提交的敌人攻击、玩家伤害、Ammo、门、拾取、资源或Objective。一次Fire只能生成一条幂等命中/伤害结果，历史态与当前态不得各结算一次。

LAG-007 · CANON · 来源：同上。

Host本地玩家与远端Client使用同一Hit Query接口和验证路径。Host的有效历史偏移通常接近0，但不得维护绕过Command、射速、Ammo、Hit Query或Damage pipeline的Host专用命中代码。

## 历史数据边界

LAG-008 · DIRECTION · 来源：本轮技术收敛。

历史缓冲只保存命中验证所需的紧凑数据：相关目标的Hitbox/Pose、稳定实体身份/代次、Simulation Tick，以及会影响射线的动态掩体状态。HP、Inventory、Loot、资源、Objective、AI Brain、完整Physics世界和Presentation不进入可被Lag Compensation恢复的历史真相。Interest Management不能导致一个当时能被射手合法命中的目标完全没有历史记录；具体记录集合与内存预算需在Spike中证明。

## 首轮测试参数

LAG-009 · TEST · 来源：SRC-USER-2026-09-05-LAG-COMPENSATION-BASELINE-APPROVED。

首轮Hitscan `Max Rewind = 150 ms`。这是用于80至120 ms RTT场景的原型起点，不是永久CANON，也不是直接等于Ping上限。测试必须把Authority Tick、Replication Rate、Client Interpolation Buffer、历史采样/保留和Max Rewind分开记录。

网络模拟至少覆盖RTT 0/40/80/120/180/250 ms、jitter 0/20/50 ms、loss 0/1/3%。记录预测命中与Authority结果分歧、实际history age、clamp率、掩体竞态拒绝、输入到确认延迟、历史内存和查询CPU。若150 ms导致大量穿掩体观感、对120 ms玩家仍频繁误拒或历史成本过高，调整数值或动作分型，不修改CANON的“有限历史查询、当前态提交、世界不倒带”边界。

## 明确未锁

历史采样频率与压缩格式、保存余量、Client时间同步/Command tick映射算法、Melee窗口、异常jitter过滤、每种Hitscan武器是否共用窗口、Projectile表现校正和最终Ping/Join UX仍需原型证据。Networking Provider、Transport、Session和Host Migration原则已经由[网络运行与恢复](network-runtime-and-recovery.md)确认，具体参数与adapter仍须Spike。
