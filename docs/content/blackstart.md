---
doc_id: CONTENT-BLACKSTART
doc_type: content
stage: DRAFT
updated: 2026-09-04
owner_role: 任务内容设计
canon_basis: "SRC-SSOT-2.0 §16、§40、§42；SRC-USER-2026-09-04-ORDNANCE-MISSIONS"
depends_on: ["../gdd/operations.md"]
---

# BLACKSTART：可搭建灰盒规格

## 身份、用途与范围

BST-001 · TEST · 来源：SRC-SSOT-2.0 §16、§40、§42 Phase3。

模板是Restart+Containment Allocation，验证裸战斗→物理Terminal→信息→资源压力→Support→Cart→贪探索→Objective Pressure→先前选择改变Finale。第一切片无Boss，不验证完整剧情、Predator或复杂阵营战争。固定拓扑后才程序变化，源切片目标35–45分钟；源详细时间表如下保留，实际试玩未做。

| 源节拍 | 时间 | 玩家问题 |
|---|---|---|
| Insertion/Gunfeel | 0–5分钟 | 裸武器是否值得用 |
| Terminal查Coupler并Ping | 5–10 | 信息从哪里来 |
| Security/Maintenance前向路线 | 10–18 | 打、绕或改系统 |
| Emergency Grid Cart | 18–24 | 怎样花有限Cells |
| Optional/Knowledge/Support | 24–32 | 弹药还是贪构筑 |
| Moving BLACKSTART Finale | 32–42 | 先前选择带来什么 |
| Resolve+新撤离路线 | 42–45 | 何时离开 |

BST-002 · TEST · 来源：SRC-SSOT-2.0 §16.3–§16.4。

Cart总3 Cells；Ventilation=1、Security Shutters=1、Defense Network=1、Transit=1、Research Vault=2。Vault前向loop/rejoin，增加Knowledge/Relic/Support并产生后续ingress/route代价。Finale通过local/forward Fault推进空间，不站圈；Cart改变Fog/Turret/Ingress/Transit。源Relic奖励在最新武器改装提案下需作A/B版本，不自行抹掉旧测试。

## 几何与对象清单

BST-003 · PROPOSED · 来源：本轮Greybox扩写；所有尺寸/敌人数/数值为TEST。

固定主序：B00→B01→{B02S或B02M}→B03→{B04直接或B04V Vault}→B05→B06→B07→B08。另在B02M分出B02O Team Ordnance工具支路，向B03障碍后重接。所有连接连续真3D，不用传送省去可读路径。

| ID/空间 | 建议内部尺寸m | 必需对象/状态 | 玩法与可达 |
|---|---:|---|---|
| B00插入舱 | 12×10×4 | 任务牌、合法loadout、出口 | 安全只因无威胁源，非永久SafeRoom |
| B01接入大厅 | 26×18×6 | T01 Terminal、普通Door、3处掩体 | 一次短战斗后查Coupler；两方向离开 |
| B02S安保通道 | 30×12×5 | GuardedValue、装甲Role、侧掩体 | 路短弹耗高，前接B03 |
| B02M维护层 | 38×16×6 | 手动风阀、低威胁通路、Coupler备选socket | 较长、可避战，前接B03 |
| B02O工具检修支路 | 20×12×5 | 一件Team Ordnance、对手可读威胁 | 位于障碍侧后，出口到B03前方；不要求原路返回 |
| B03紧急配电厅 | 24×20×7 | Cart01、3 Cells保证可得、反结构障碍 | 全组短预览；慢维护旁路始终可达 |
| B04决策前厅 | 18×18×5 | Upload01、Support投递点、可见前向标识 | 自愿补给和一处改装候选 |
| B04V研究库 | 24×18×7 | VaultData、奖励、明确来源门 | 花2Cells可开；前接B05并开启代价源 |
| B05低层继电廊 | 35×20×8 | Fault01、Fog、可控Turret | 首段移动战斗，通风选择改变低处路线 |
| B06换流台 | 28×22×8 | Fault02、侧Ingress、普通Door | Shutter改变侧压；不强制站圈 |
| B07出口联接器 | 24×18×6 | Fault03、Transit接点、主任务完成 | 推进任务后新撤离路线可见 |
| B08撤离端 | 18×12×5 | Exit01、世界恶化边界 | 不回插入点，不硬秒杀计时 |

通行主门净宽候选≥2.4m、重武器/搬人路线≥3m、主战场至少两条可读移动线；最终尺寸按移动/相机/碰撞实测。层高和mantle高度不能猜测为引擎默认。所有入口标typed port和允许Role，不从玩家当前视野凭空spawn。

## 任务状态机与制作步骤

BST-004 · PROPOSED · 来源：本轮Greybox扩写。

| 状态 | 进入前置 | 玩家动作/输出 | 失败/降级 |
|---|---|---|---|
| Inserted | 玩家入场 | HUD:定位Sync Coupler | 无通用Alarm |
| CouplerLocated | T01合法查询或直接发现 | Team waypoint | T01失效可在维护侧读实体标牌，不隐藏必要信息 |
| CouplerAcquired | 唯一pickup凭据 | 带到前方接入座 | 越界回收至已知合法点，不复制 |
| GridConfigurable | Coupler接入+Cells可达 | Cart选择并提交设施后果 | 旧revision拒绝，无免费撤销 |
| RelayStarting | 前进到B05且开始目标 | Fault01激活+合法Horde预兆 | 无站圈要求 |
| FaultChainActive | 上一Fault处理 | 沿B05→B06→B07交互/战斗推进 | Optional功能失败走较险前向路线 |
| RelayStable | Fault03完成 | Primary完成，打开B08 | 无Boss来补节奏 |
| Evacuating | 世界后向失效可见 | 沿新出口离开 | 留下不能重复获得任务奖励 |
| Finished | Exit01结算或真正Wipe | 一次ResultID | 保留已Banked知识 |

Fault01候选：将可搬导流件装入前向槽，需短时暴露但可中断保留已提交阶段。Fault02候选：切换两个局部断路开关，单人顺序可做，四人可分工；没有必须同时按。Fault03候选：搬开卡住出口的可破结构或走侧维修架操作释放。互动候选单阶段≤3秒，模拟持续，离开不重置已完成合法动作。精确耗时属TEST。

## Cart 后果矩阵

BST-005 · PROPOSED · 来源：本轮Greybox扩写。

| 选项 | 可观察收益 | 明确机会成本/代价 | Finale验收 |
|---|---|---|---|
| Ventilation | B05低层雾消、射线更清楚 | 占Cell，未封侧门/未开Vault | 实际出现可用下层路线 |
| Shutters | 关闭B06明确侧Ingress | 占Cell，不能封所有已存在威胁 | 无Breach敌人不能绕封门作弊 |
| Defense Network | 接管B05 Turret | 固定射界，不能覆盖所有前线 | 队友可利用但仍需移动 |
| Transit | B06→B07短移动段可用 | 暴露上层出口且耗Cell | 真连接可读，无任意teleport |
| Research Vault | 增加Data与一项奖励 | 用2Cells且开启已展示的后续侧来源 | 奖励与新增压力都能指出因果 |

三项一费方案与Vault+一费方案全部走读；不默认某一组合永远最优。安全与资源对照必须用相同初始seed/武器，区别来自选择本身。

## Team Ordnance / Breach 分支

BST-006 · PROPOSED · 来源：SRC-USER-2026-09-04-ORDNANCE-MISSIONS。

B03前出现非关键结构堵塞，队伍先看到“可直接突破/维护旁路”的空间关系。B02O检修支路可取得一具Thermal Cutter候选；需持双手，切普通结构速度快，但切换主武器会放下。向前通过小货运出口在障碍后重接，不返回B01；队友可在侧路掩护携带者。

固定测试燃料100单位，破该结构需40，战斗切割每次耗10；普通Supply不可补充。若玩家提前用空，仍可走B02M→维修架→B03侧门，额外约90–150秒且有可预告GuardedValue对手。重武器是爽/快/耗资产的捷径，不是唯一mandatory key。空壳留场并明确标“已耗尽”；不在背后凭空补一把。

验证包括开局耗尽、多人抢取、持有者断线、切主武器、丢出导航、倒地搬人、离开B02O再回来；按[Team Ordnance共享规则](../gdd/combat-and-arsenal.md)保留Instance和剩余资源。此切片不加入完整Predator；Predator语法在任务文档保留供下一模板。

## 资源、敌人与奖励账

BST-007 · TEST · 来源：本轮Greybox预算候选，不是最终平衡。

把一份“个人标准主武器reserve容量”定义为1 Ammunition Unit仅作观察计量，不新增玩家货币。初始团队正常reserve总量按实际4人loadout记录，沿保证主线放相当于约0.75倍团队初始reserve的本地Ammo；各弹族实际单位必须由配装表换算。医疗初始每人一份候选，主线补给两份团队医疗，不能以这个数字宣布所有场景可解。

测试Support Meter threshold=100，保证主线总贡献240，Vault再100；因此主线2Charges+40余量，Vault可多1，符合源约2–3的试制范围。分布：B01知识40、两路之一保证Scrap60、Coupler目标40、B04知识50、Fault02目标50。每份凭据唯一，敌人常规击杀不给稳定Support。Supply包内实际弹量/医疗量OPEN，先按试测记录，不给假精确经济。

Role只用Runner、Ranged Suppressor、Armored Holder、Scout/Source与Flanker；战斗原型详见[内容卡](combat-prototypes.md)。第一10分钟不发Relic/配件，隔离裸战斗测试。最新profile在B04/B06给少量Weapon/Tool Modification机会；对照profile沿源规则测试Relic，二者不能混在同一数据组声称某方案更好。

## 多人、边界与反馈

BST-008 · PROPOSED · 来源：本轮Greybox扩写。

单人无Bot能完成所有Fault与运输，双人以上可分工但不强制职业。查询结果自动分享；Cart只任一合法操作者提交但全队预览。Support/draft/上传走共享事务，不在关卡脚本另建账。所有任务目标最多一次完成，Host migration保存door/power/coupler/cell/ordnance/fault/upload状态。

最终世界恶化候选是后方供电相继失效与既有威胁源向前推进，音画明确；不设置隐藏撤离秒数或无限奖励敌人。可选Vault没开仍可通关；所有Cart组合、空重武器、资源损失都应给可读的可行路径或已批准明确失败，不能陷入没有目标也没有结束的局。

## Greybox验收清单

BST-009 · TEST · 来源：SRC-SSOT-2.0 §16.5；本轮扩写。

完整单人和四人走读；第一10分钟零改装；查询产生合法Ping；至少一次玩家主动绕战；Support的Ammo与成长选择都在合理状态下有价值；Cart组合实际改变Finale；低压安全不被无来源spawn破坏；无强制回跑/站圈/Boss/硬撤离表/checkpoint；空Ordnance仍可完成任务；无重复资源事务。

记录每房进入/离开、等待、伤害/资源来源、Cart选择、改装、退出/Wipe原因；询问玩家能否指出自己造成的终局后果。此文件只达到可搭建规格，所有实验结果尚未产生。

