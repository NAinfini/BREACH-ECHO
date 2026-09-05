---
doc_id: GDD-COMBAT
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 战斗设计
canon_basis: "SRC-SSOT-2.0 §6、§10、§12、§23；NAR-010；本轮枪械与操作方向"
depends_on: ["player-and-input.md", "field-modifications-and-effect-system.md"]
---

# 战斗与武器家族

## 玩家目的

没有 Relic 时也愿意开枪、躲避和近战；武器提供不同的解题成本，后续 Build 放大选择，不拯救无聊底盘。

## 范围与术语

AttackRoot 追踪一次因果攻击；Hit 表示合法命中；DamageEvent/Status/Reaction 由[Build系统](field-modifications-and-effect-system.md)解释。视觉后坐、镜头抖动与真实弹道分离。武器成本见[经济](economy-and-support.md)。

## 已确认规则

CMB-001 · CANON · 来源：SRC-SSOT-2.0 §6.1–§6.2。

Weapon A/B 接受所有合法家族。后坐采用易控制的可学习图样与小 seeded variance，短点射稳定、持续增长饱和、水平随机克制。轻中武器 Hipfire 可用，ADS 提高精度而非补救废弃腰射；换枪快，重武器可慢但必须立即反馈输入。分阶段换弹可取消，完成阶段保留；Camera shake 可独立关闭。

CMB-002 · DECIDED · 来源：当前产品基线；历史见Git。

官方Operation采用有限实体弹动能、电磁实体弹和有限Energy Block枪械；Heat限制爆发但不产生新弹药。快速近战付距离、动作与暴露成本；独立Hammer/Knife/Spear/Sword及Staff/Spell完整谱系只作Lab/FUTURE试验，不进入基础版装备池。Heavy/Prototype使用稀缺资源，对部位/装甲/结构有真实作用，不用隐藏CanKillBoss钥匙。

CMB-003 · CANON · 来源：SRC-SSOT-2.0 §12.1–§12.4。

官方玩家间伤害默认 0%；SelfDamage、FriendlyImpulse、FriendlyDebuff、环境归属分开。敌方同阵营默认无互伤，普通单位不挡同阵营普通射击；明确屏障/大型体型/攻击可覆盖。普通 Horde 软占位，重型/盾兵/车辆等明确硬阻挡；抓住玩家必须是可读动作，不是碰撞漏洞。自定义友伤是 typed multiplier，不是布尔开关。

CMB-004 · CANON · 来源：SRC-SSOT-2.0 §23.1–§23.4。

AnatomyGraph 是可增删/替换/再生的部位拓扑，提供感知、移动、抓取、武器挂点等能力；敌人可以严重肢解，官方玩家不承受整局跛行/断臂惩罚。固定人体假设不得进入命中或装备真相。

CMB-011 · CANON · 来源：SRC-USER-2026-09-04-FIRST-BUILDER-PROTOTYPES；引用[世界观NAR-010](canonical-world-history-and-lore.md)。

Prototype weapon的筑路者技术谱系由NAR-010唯一维护。战斗系统不得把“部分”扩大成全部，也不得在未确认前给具体武器指定原件、仿制、逆向工程或量产身份；这些身份不改变CMB-002对真实资源与机制作用的要求。

## 玩家流程

CMB-005 · DECIDED · 来源：本轮系统扩写。

识别威胁与掩体→选武器家族→预备/瞄准→提交攻击与资源→命中部位→反馈装甲/姿态/生命变化→决定续攻、换枪、冷却、近战或撤位。一次命中反馈必须能区分“没击中”“护甲有效”“打断”“击杀”，不能只有更大粒子。

## 状态与所有权

CMB-006 · DECIDED · 来源：本轮系统扩写。

Authority 拥有装填阶段、热量、投射物、命中、DamageEvent、部位能力；Client 预测本地动作和表现，不产生权威掉落或命中。每次攻击绑定装备版本、根事件、种子、消耗事务和目标部位稳定 ID。

| 起点 | 事件 | 结果 |
|---|---|---|
| Ready | 验证攻击成本通过 | Commit；产生攻击与扣费 |
| Ready | 资源不足 | 不提交，明确空仓/热锁提示 |
| ReloadStage | 阶段完成 | 持久化该阶段，再允许取消 |
| HeatReady | 超过家族热阈值 | Overheated，按显式 profile冷却/消耗 |
| PartIntact | 部位完整度耗尽 | PartBroken，更新能力及合法后续动作 |
| ProjectileActive | 射手倒地 | 保留已提交飞行与归属 |

## 模式配置与内容接口

CMB-007 · DECIDED · 来源：本轮系统扩写。

共用命中、伤害、装填和能力语义；模式只改资源供应与公开内容参数。武器卡声明射击方式、节奏、弹道、手感反馈、成本、范围、Tags、部位作用与可取消点。禁止靠不同模式悄悄改变同一攻击对同一材质的定义。

## 边界

CMB-008 · DECIDED · 来源：本轮系统扩写。

同帧死亡和已提交攻击按权威提交序执行；先已成立的攻击不会因死亡消失。断线不能复制装弹；换弹物资在唯一事务内转移。多玩家同破一个部位只发一次 sever/state change，可分别记录贡献。无法访问的穿墙目标不得被相机、Aim Assist 或 UI赋予合法命中知识。高密度呈现聚合不删实际命中，性能做不到应缩小公开目标并重新批准，不能偷 cap。

## 参数

| 参数 | 值与状态 | 来源 |
|---|---|---|
| Lab/FUTURE Staff 初始 Spell | 3 · 历史实验profile | SRC-SSOT-2.0 §6.4、§40 |
| Lab/FUTURE Staff 局内目标上限 | 6 · TEST；不是Operation或内核上限 | SRC-SSOT-2.0 §6.4、§40 |
| Melee试制集合 | Hammer/Knife/Spear/Sword，共4把 · TEST | SRC-SSOT-2.0 §6.3、§40 |
| 玩家友伤默认 | 0% · CANON；自定义示例10/25/50/100% | SRC-SSOT-2.0 §12.1、§40 |
| DPS/护甲/姿态/热初值 | TEST | 见战斗试制参数；实际平衡待裸武器对照 |

## 示例

CMB-009 · DECIDED · 来源：本轮系统扩写。

正常：Hammer 打断护甲目标的动作并开放队友射击窗口；Knife 利用短恢复打传感器。失败：Energy 贪输出热锁，玩家仍可换近战撤位，系统不补一份免费弹药。跨系统：切断带枪部位移除 WeaponMount，敌人切换合法行为而非原动画继续空手开枪。

## 验收与尚未实测项

CMB-010 · TEST · 来源：SRC-SSOT-2.0 §42 Phase 1、§43.1；本轮测量补充。

原 Gate 是零 Relic 愿意连续玩 30 分钟；本轮建议记录主动继续游玩的比例、家族选择理由、误判反馈，而不是只问“爽不爽”。不能为了让一把枪过线把另外家族做成资源上位替代；具体实验见[战斗原型](../content/combat-prototypes.md)。

## 当前枪械方向

CMB-012 · DECIDED · 来源：SRC-USER-2026-09-04-ENERGY-EM-GUN-FAMILIES。

当前活跃远程枪械候选只有三类，均无已锁数值：

| 家族 | 倾向 | 必须支付/验证的代价 |
|---|---|---|
| 传统动能 | 高即时伤害与高射速倾向 | 消耗较多实体弹药；枪声与枪口特征高 |
| 电磁 | 小口径实体弹丸、较低发射特征、强材料穿透 | 较低停止力/基础伤害；过穿、友伤profile和未知墙后反馈风险 |
| 有限Energy Block | 能量块作为可掉落、可补给的有限弹匣资源 | 不能把Heat或等待当免费补给；弹块、Heat和输出都需测试 |

电磁武器不等于静音：机械动作、空气扰动、超音速、撞击与命中仍可产生声音。穿透计算必须区分肉体、护甲与结构，追踪出射后的残余能量和多目标效率；墙后hit marker只能反馈合法已知结果，不能变成免费扫描器。默认玩家伤害仍遵守CMB-003，但电磁过穿对队友遮挡、冲量及启用友伤的profile必须测试。

CMB-013 · DECIDED · 来源：当前产品基线；历史见Git。

Energy Block固定为三把独立枪：单发、连发、强制蓄力，全部扣有限能量单位。蓄力从最低合法阈值到满蓄力提高伤害/资源成本，只有声明的高蓄力段产生范围效果；中断未发射时取消未提交弹药，但已经发生的暴露/时间不退。行为与初值由[战斗试制参数](../content/combat-balance.md)拥有。旧“等冷却即可无限续航”退出Operation，不保留两套长期实现。未来DLC标准Operation武器也必须是有成本的sidegrade。

## 响应性、取消窗口与玩家技巧

CMB-014 · DECIDED · 来源：SRC-USER-2026-09-04-RESPONSIVE-GUNPLAY-CANCEL-WINDOWS。

操作优先响应性、可掌握输入技巧和可读窗口，不为强行拟真牺牲手感。换弹在弹匣实际就位且武器已具备发射条件后，可以取消非功能性收尾动画；客户端表现、权威弹药状态和反馈必须指向同一完成点，不得“看似上弹实际未上”或通过取消复制弹药。可发射时点、可ADS时点与完整动画结束是三个显式阶段。

切枪或换弹后，ADS与Fire可通过input buffering和合法cancel window尽早衔接，不要求所有恢复帧锁死。蓄力武器必须用高伤、高穿透或高蓄力范围效果等明确回报支付蓄力承诺，不能只是延迟普通一枪；当前射击结算前后可在合法窗口预输入下一轮蓄力，不强迫等待完整发射收尾。缓冲时点和移动/受击/换弹中断采用测试参数的阶段优先级，且不得突破已声明射速、资源扣除与权威提交顺序。

移动技巧包括bunny hopping只进入TEST候选：可提供可学习机动收益，但不得摧毁潜行、敌人威胁、体力/噪声、队形或关卡边界，也不得成为每名玩家必须重复的动作税。只学习同类游戏的响应性原则，不复制其专有表现或数值。长期技巧成长的总原则见[进度PRG-009](progression-and-bastion.md)，输入交付见[玩家PLY-013](player-and-input.md)，失败反馈见[UX-007](ux-and-accessibility.md)。

CMB-015 · TEST · 来源：本轮操作与枪械验收建议。

同时观察资深玩家是否因掌握取消/缓冲窗口而提高资源效率和安全裕度，新手是否看懂失败原因；是否出现宏、特定超高FPS、设备或延迟优势；动画取消是否导致网络不同步或弹药复制；bunny hopping是否成为唯一最优移动。三类枪须比较资源消耗、声音/发射特征、穿透、友伤profile与补给压力；Energy Block三子型分别测试，不用一把全能原型代替。

CMB-016 · DECIDED · 来源：当前产品基线；历史见Git。

Operation枪械核心已裁决。Staff 3/6法术和四主武器近战试验仅归Lab/FUTURE；Quick Melee、有限资源和已有动作纪律继续有效。该选择见Operation装备与改装决策，后续不再作为等待所有者选技术的OPEN。

## Team Ordnance：世界团队重资产

ORD-001 · DECIDED · 来源：SRC-USER-2026-09-04-ORDNANCE-MISSIONS。
用户提出团队世界重武器：不占常规loadout，必须手持，切主武器即物理放下；固定Ammo/燃料，普通Supply不可refill，用尽作废。火力应明显超常，代价来自双手、移动/攀爬/交互、噪声和队友掩护；放下持久、全队可Ping、倒地/断线不消失。候选HMG、Grenade Launcher、Anti-armor Cannon、Thermal Cutter、Sonic Driver。

ORD-002 · DECIDED · 来源：本轮系统扩写。
Authority独占OrdnanceInstanceID、definition/version、ammoRemaining、holderSeatID、worldTransform、pickupRevision、actionStage、noiseProfile、depleted状态。Available→ClaimPending→Carried→Firing/Using→Dropped或Depleted；拾取/放下/消耗同权威序裁决。两个玩家同拾，首个合法commit获持有；失败者仍保留普通武器状态。

Carried期间普通武器收起但未离开loadout；切主武器在最近合法支撑面Drop，再恢复主武器。攀爬/Revive/搬人若需双手，先预览放下；不让资产消失进无限背包。射击消耗提交后不可用取消换枪退还。持有者倒地/离线在合法位置物化，记录剩余Ammo和已提交弹体，重连不生成一把新枪。零Ammo变Depleted，不再开火、不受普通补给恢复，可保留空壳直到明确场景卸载。

ORD-003 · DECIDED · 来源：本轮系统扩写。
全部真人可Ping资产及可知剩余资源，无Host特权。丢出世界/不可达地形时移到最近可达已知回收点，记录物件移动而非复制。恶意早耗仍是公共匹配风险：关键障碍不得仅靠这件可提前耗尽资产完成，必须有更慢/更险的前向旁路或只让重资产控制shortcut/optional。不能把恢复弹药作为掩盖任务软锁的fallback。

ORD-004 · TEST · 来源：本轮内容验收。
覆盖双拾取、切枪、攀爬、Revive、倒地、离队、迁移、耗尽、越界、重新加载；要求唯一Instance、弹量守恒、无消失、无必经任务软锁。移动惩罚、噪声量、携带尺寸、固定Ammo由具体卡测试；不在系统里统一“全部减速30%”。共享修改模型只提供明确允许的接口，普通Relic/AmmoMultiplier不能给它无限弹。
