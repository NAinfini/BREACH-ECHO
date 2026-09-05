---
doc_id: CONTENT-COMBAT
doc_type: content
stage: BASELINE
updated: 2026-09-05
owner_role: 战斗内容设计
canon_basis: "SRC-SSOT-2.0 §6–§8、§42；Team Ordnance用户意图；NAR-010"
depends_on: ["../gdd/combat-and-arsenal.md"]
---

# 战斗原型卡

## 范围与状态

PRT-001 · TEST · 来源：当前产品基线；历史见Git。

首发试制先AR/Shotgun+工具/自由战术模块，再EM与三把独立Energy Block枪。独立四近战、Staff和Spell卡完整保留为Lab/FUTURE资料，不进入Operation奖励、教程或必需工作量；全部数值未测。

PRT-002 · PROPOSED · 来源：本轮内容扩写。
以下行为、代价与反馈全为可执行候选；通用输入/伤害/资源语义归系统。每张卡先用简模、基础碰撞、可辨动作和一个音效实现，用相同对手比较。基础试测目标Health=100只作为沙盒单位，正式平衡未测，首个可执行数值采用战斗试制参数。

PRT-005 · DECIDED · 来源：当前产品基线；历史见Git。

首批生产使用人类来源的通用枪械与维修重资产，不将任何具体卡擅自宣布为筑路者原件。NAR-010“部分Prototype源于筑路者技术”的明确事实保留；哪一把正式命名武器属于哪条历史谱系随OWNER-01的内容审阅再批准，不阻塞灰盒。

PRT-006 · DECIDED · 来源：当前产品基线；历史见Git。

三枪械家族和三把Energy子型已选定，全部扣有限资源。初始HP、弹仓、射速、成本、蓄力、敌人和工具数值见[战斗试制参数](combat-balance.md)，均TEST不是已完成平衡。Staff/Spell表只是未来实验保存。

## 武器卡（首发与Lab逐行标注）

| ID/身份 · 状态 | 触发/动作 | 成本/输出Tags | 交互、模式与反馈 | 验收问题 |
|---|---|---|---|---|
| W-AR · DECIDED / 数值TEST | 持Fire连射，点射首发稳定 | Ballistic/Direct/Piercing；真实弹仓/分段换弹 | Operation即时处理暴露目标；清楚击中/护甲音 | 不靠配件愿意用；ADS不把hipfire救活才可用 |
| W-SHOTGUN · DECIDED / 数值TEST | 单发近距扇束，分段装弹 | Ballistic/Pellet/Stagger，距离散布 | 每pellet真实、反馈聚合；近距breakthrough | 拥挤走廊比AR有不同选择 |
| W-HAMMER · Lab/FUTURE TEST | 轻击/蓄重；右键稳身格挡 | Melee/Impact/Posture/Structure | 慢承诺、高姿态与部位作用；无弹耗 | 正面破阵与timing，不是最高通用DPS |
| W-KNIFE · Lab/FUTURE TEST | 快轻击/精准重刺；右键短偏转 | Melee/Piercing/Weakpoint | 短reach短恢复，依位置 | 与Sword盲测能区分 |
| W-SPEAR · Lab/FUTURE TEST | 长直刺/蓄刺；右键spacing counter | Melee/Line/Piercing | 单线穿刺，贴脸侧压差 | 远距控场与拥挤代价均可见 |
| W-SWORD · Lab/FUTURE TEST | cleave/重斩；右键guard/parry | Melee/Cleave/Parry | 中庸覆盖、最完整防御节奏 | 技术能减少换血，不设固定体力税 |
| W-EM · DECIDED / 数值TEST | 发射小口径实体弹丸 | Electromagnetic/Projectile/Penetration；有限弹药 | 较低发射特征但非静音；显示材料层与残余能量 | 穿透有选择价值且不成免费墙后扫描 |
| W-EB-SINGLE · DECIDED / 数值TEST | 单次提交一发 | EnergyBlock/Direct；有限能量块 | 高单发伤害倾向，真实换块/补给 | 与动能高伤枪有不同资源和特征代价 |
| W-EB-AUTO · DECIDED / 数值TEST | 持Fire连续提交 | EnergyBlock/Automatic；有限能量块 | 较低单发伤害，持续消耗和反馈可读 | 不靠免费续航淘汰传统动能 |
| W-EB-CHARGE · DECIDED / 数值TEST | 按住蓄力、松开合法发射 | EnergyBlock/Charge/Area候选；按蓄力扣有限资源 | 低蓄力低伤；高蓄力高伤并可范围爆炸 | 蓄力回报明确且下一轮缓冲不破射速 |
| W-STAFF · Lab/FUTURE候选 | Fire施法、轮盘换三个verb | Casting/Resonance，家族资源 | 只限Lab/FUTURE，Operation不加载 | 控制/防御也被主动使用 |
| S-BOLT · Lab/FUTURE候选 | 短前摇定向投射 | Projectile/Arcane，消耗charge | 中等爆发；需瞄准 | 不是其他两Spell的全面上位 |
| S-FIELD · Lab/FUTURE候选 | 放一处短时导流区域 | Area/Control/World，持续耗资源 | 导流合法Medium/减慢小敌，不能免费开关键门 | 队友能利用改变路线 |
| S-WARD · Lab/FUTURE候选 | 定向短防御通道 | Defense/Channel，持引导占手 | 掩护Revive/过射线，停止施法失效 | 确实牺牲本人输出换团队机会 |

W-HAMMER至W-SWORD身份来源为SRC-SSOT-2.0 §6.3；具体动作实现仍PROPOSED。首发射速、距离、热量、弹仓采用战斗试制参数，后续裸武器实测调整，不称为最终DPS。

## 工具与自由战术模块卡

| ID/状态 | 动作与成本 | 输出/Tags与互动 | 模式差异/反馈 | 验收 |
|---|---|---|---|---|
| U-SCAN · DECIDED / 数值TEST | 指向合法已知hostile，消耗战术charge | Mark/TeamWindow；不穿墙不叠乘 | Operation有限、Lab可快；目标轮廓与计时 | 不成为所有队伍必带税 |
| U-FOAM · DECIDED / 数值TEST | 投部署体，消耗战术charge | Barrier/Control/DoorInteraction | 可延缓普通门/小敌，不顶替战略Seal | 队友看得懂延迟而非永固 |
| A-AEGIS · TEST | 定向可移动barrier | Defense/Advance/ReviveCover，移动/输出承诺 | Operation不能免全伤过所有目标 | 新verb+战场解法成立 |
| A-BREAKER · TEST | 近距冲击cleave | Posture/Part/Armor/Breach，暴露与动作成本 | 不能当唯一任务钥匙 | 新verb+多hook，非纯加伤 |
| A-ECHO · TEST | Operation仅对合法已付费枪械攻击延迟Echo | Echo/Triggered，明确时间和追加成本 | Operation不复制资源/任务；Lab可强连接 | 可解释什么可echo、什么不可 |

三个战术模块的历史候选来源SRC-SSOT-2.0 §7.2；回声额外成本等采用战斗试制参数的TEST初值，不能仅因“Echo”名字就复制一整个Support Pod。

## 敌人角色卡

| ID/状态 | 感知/行为 | 迫使玩家改变什么 | 反制/可见反馈 | 测试点 |
|---|---|---|---|---|
| E-RUNNER · DECIDED / 数值TEST | 看/听后逼近，近身明确前摇 | spacing和移动路线 | 软占位、姿态打断、门延迟 | 不靠碰撞永久锁人 |
| E-SUPPRESSOR · DECIDED / 数值TEST | 可见射线/掩体换位 | 压住一直站桩的远程 | 开火前定位cue，侧翼/屏障 | 不墙透追踪输入 |
| E-HOLDER · DECIDED / 数值TEST | 护住资源/系统，慢硬体积 | 弱点/部位/重火力 | 装甲部位和武器挂点可破 | 不是仅更多HP |
| E-SCOUT · DECIDED / 数值TEST | 感知后短通信动作 | 打断来源或接受后果 | 通信失败不召来援军 | 不是全局Alarm开关 |
| E-FLANKER · DECIDED / 数值TEST | 使用合法维护侧port | 关注战场侧线与队友掩护 | 声音/路径线索，Seal可阻断 | 不凭空teleport背后 |

## 团队重装备（首发三件与未来候选）

PRT-003 · DIRECTION · 来源：SRC-USER-2026-09-04-ORDNANCE-MISSIONS。
团队世界重资产不占普通loadout，手持、切主武器放下、固定资源、普通Supply不能补、用尽作废；详细权威/持久规则归[战斗系统](../gdd/combat-and-arsenal.md)。

| ID/状态 | 动作/成本 | Tags与解决问题 | 代价/反馈 | 验收 |
|---|---|---|---|---|
| O-HMG · DECIDED / 数值TEST | 架肩高密度射击，固定弹带 | Heavy/Ballistic/Suppress | 双手、慢转向、强声源 | 火力显著超常枪，仍需掩护移动 |
| O-GL · Lab/FUTURE候选 | 弧线榴弹，固定弹数 | Explosive/Area/Structure | 自伤/视线/小空间风险按profile公开 | 能清复杂阵地，不开全部任务门 |
| O-CANNON · DECIDED / 数值TEST | 长前摇反装甲发射 | Heavy/Armor/Part/Structure | 搬运、瞄准、稀缺弹 | 真实破部位，不CanKillBoss标志 |
| O-CUTTER · DECIDED / 数值TEST | 近距持续热切 | Heat/Structure/Channel | 燃料、近身、持续双手 | 可突破障碍，耗空仍有旁路 |
| O-SONIC · Lab/FUTURE候选 | 定向声波脉冲 | Sonic/Posture/Resonance | 巨声暴露、有限电容 | 能断控/抑制，非万能钥匙 |

## 验证与失败样例

PRT-004 · TEST · 来源：本轮实验建议。
同一沙盒测所有家族的紧急杀敌、资源持续、跨线、近身拥挤、部位破坏、队友救援。失败例：Staff90%行为都是Bolt、Energy Block所有场合上位、Knife只是短Sword、Aegis成为任务必需，均返回具体卡改动作，不靠加更多武器掩盖。

Ordnance提前耗尽、丢越界、断线、两个玩家同pickup、切主武器与倒地必须保持唯一资产。跨系统每种输出至少接入真实伤害/姿态/世界接口，不能只播演出。


## 首发工具与重资产裁决

PRT-007 · DECIDED · 来源：当前产品基线；Operation装备与改装决策。

三工具为Scan、Foam、Decoy；Decoy投掷有限物理声源，引导能听见且路径可达的敌人，不改写已确认视野或任务来源预算。三自由战术模块沿Aegis/Breaker/Echo原型，资源与冷却详见战斗试制参数；没有人物专属。首发三件Team Ordnance选择Cutter、HMG、Anti-armor Cannon；GL/Sonic保留未来候选，不能因为目录有五行就承诺全部首发。
