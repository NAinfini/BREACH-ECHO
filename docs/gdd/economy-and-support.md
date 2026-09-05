---
doc_id: GDD-ECONOMY
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 资源与合作经济设计
canon_basis: "SRC-SSOT-2.0 §4A.9–§4A.12、§8.3、§33、§40"
depends_on: ["world-and-information.md"]
---

# 资源、Support 与公共物资

## 玩家目的

让资源约束产生“现在怎么打、去哪里、给谁、买什么”的讨论。玩家仍有行动手段，但糟糕决策确实可能把局势耗到无法恢复。

## 范围与术语

Support Meter/Charge 是团队请求支援预算；Knowledge/Data与Scrap/Salvage是不同世界对象；Mission Cell 是任务资源，不是通用货币。知识永久结算见[进度](progression-and-bastion.md)，设施配置见[世界](world-and-information.md)。

## 已确认规则

ECO-001 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

Operation所有远程主枪均使用有限资源。Ballistic和EM扣实体弹，Energy Block扣有限能量单位，热量只限制节奏而非生成补给；Quick Melee付距离/时间/暴露风险，Heavy扣独立固定弹药/燃料。Staff等续航家族不进入Operation。生成器必须保证初始合法配置存在数学上可行的主任务解法；玩家后续错误仍可能耗到真实失败。

ECO-002 · CANON · 来源：SRC-SSOT-2.0 §4A.11。

Knowledge与Scrap均可贡献团队Meter，Knowledge另有研究价值。普通击杀不稳定形成Kill→Support→Ammo正循环。Meter满变离散Charge，溢出保留；标准Drop通常一Charge，高级/Prototype可两Charge或Authorization。按固定方向序列授权，错误不扣费，真实Beacon提交后才扣Charge；设施Terminal不负责Hub补给。

ECO-003 · CANON · 来源：SRC-SSOT-2.0 §4A.11–§4A.12、§20.5。

Pod内容公共所有：Ammo/Med/Tactical/允许的Power可拿、放、再分，关键任务Cell不能被随机补给生成。Operation高价值Modification用Shared Draft，首轮每Seat最多claim一件或Pass，余物之后自由。固定入场枪身份不由Pod随机替换；模块按挂点安装，拆出实例可留世界，Prototype是可转交重资产。Host/Leader无特权。reserve可拆为按弹族/容量拾取的实体bundle并放回合法locker；Lab吸收型Relic不进入此Operation流程。

## 玩家流程

ECO-004 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

发现物资/数据→交互确认归属→Meter增加并提示获得Charge→查看团队状态与支援候选→输入授权→投Beacon→权威提交扣费→胶囊到达→draft或自由分配→剩余缓存。Knowledge上传与Support获得不是同一账，具体分离见进度文档。

## 状态与所有权

ECO-005 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

Authority 拥有 TeamMeter、ChargeBalance、spendRevision、worldSupplyID、ClaimLedger、PodDeliveryState；每个世界物件的採集凭据最多消费一次。玩家个人reserve仍由权威持有，世界drop是reserve减少与bundle生成的原子转换。

| 当前 | 事件/条件 | 结果 |
|---|---|---|
| MeterPartial | 新收集凭据 | 加值，整除生成Charge，余数保留 |
| Selecting | 方向序列正确 | Authorized；不锁费、不扣费 |
| Authorized | 合法Beacon投掷提交且余额足 | 扣费+DeliveryID同事务提交 |
| Authorized | 他人先用完余额 | 拒绝提交并显示差额，不吞Beacon |
| Committed | 有效投递完成 | PodOpen，物资实例只生成一次 |
| PodDraft | 首轮资格用完/Pass/明确超时 | PublicRemainder |
| Committed | 无合法落点/投递路径失效 | 显式失败状态按既定合同处理 |

## 并发花费与投递失败

ECO-006 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

两个玩家可同时输入同一余额，但输入不保留Charge；Beacon提交以spendRevision和权威序列比较扣款，首个合法提交成功。请求带幂等ID，重传只返回同一DeliveryID。UI持续显示最近谁请求了哪种支援，降低误花；不以多数投票阻塞普通行为。

Beacon投掷前验证合法投递面和任务允许区。提交后因世界变化无法落地时，寻找预先声明的邻近合法delivery anchor；若不存在，进入DeliveryFailed，返回原Charge且不生成物资并记录失败原因。不得无限重试、吞费或偷偷送双份。此为故障事务候选，不补偿玩家自己合法使用后的战术损失。

## Shared Draft 加入/离开

ECO-007 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

Pod开启时快照本次在场真人/被替代Bot slot的eligible seats；每seat最多一个claim。新加入者不追溯首轮资格，首轮后可拿余物；若继承离开者同一seat，则继承该seat已claim/pass状态，不新造额度。短暂断线保留资格至公开的等待期限；明确离队视为Pass并释放未提交claim。机器人只有明确授权才消费scarce物资。首轮超时参数在局前social profile可读，不能让AFK永久锁物资。

## 模式配置与经济能力边界

ECO-008 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：SRC-USER-2026-09-04-OPERATION-FOCUS；本轮评审 E3。

Operation-safe pool允许方向改变、局部控制、环境导流、有成本的效率交换与团队窗口。内容验证追踪 ResourceMint、ResourceTransform、MissionAdvance、DoorOverride、Spawn、Revive 等能力及来源；普通Operation奖励不得正和复制弹药/医疗/任务Cells、免成本跨过必要Objective或形成指数经济。公开规则在内容准入时决定，不在玩家变强后暗削。

“双倍资源”不是必然破坏所有游戏，但它会把计划的稀缺曲线推到另一种体验。在本候选中禁止“所有拾取×2”；可测试“选一个已存在补给，将更大份额转换成指定ammo family，同时损失另一份”或“短暂更省弹，牺牲射速/暴露/任务时间”。物资总量、来源和成本可解释；不能把+100%资源改名为“效率”就蒙混过关。

Operation有限Energy和Quick Melee按各自真实成本合法，资源压力同时来自时间、空间、医疗、安全、热锁、任务消耗；仅靠弹药稀缺设计会被无限续航家族击穿。Descent/Lab可开放不同ResourcePolicy，但仍声明资源事件和推进，不删弹药/热量系统。该边界会影响原文合法God Build在Operation的内容范围，由DDD-0014在授权下确认。

ECO-014 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：SRC-USER-2026-09-04-ENERGY-EM-GUN-FAMILIES。

Operation Energy枪已选择可掉落、可补给的有限Energy Block；Heat只限制节奏，不生成弹块。DDD-0014已经覆盖旧广义Energy续航的Operation解释；Staff/Arcane只保留Lab/FUTURE，不加载到当前奖励池或配装。具体三枪数值见战斗试制参数。

## 内容接口与边界

ECO-009 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

Resource definition声明family、单位、容量、可drop/storage、收集凭据、支持值、永久账关联。关键物品被丢出合法导航域时移动到最近可达的已知回收点，记录原因；不复制任务Cell。不能从被消耗bundle重复取出。受伤/死亡打断未提交拾取，已提交物资按death规则留世界。断线不复制背包或Charge，迁移恢复同ledger。

ECO-010 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

Operation不设置通用商店、Gamble、免费Respec或重掷RNG服务。任务Cart是一次真实设施预算，不是可退款购物车；支援通过Charge与Beacon，改装通过合法维护点和原子替换。Lab/FUTURE的商店与Respec不进入基础产品。

## 参数

| 参数 | 当前值/状态 | 来源 |
|---|---|---|
| 正常Operation Charge产出 | 约2–3，可贪探索更多 · TEST | SRC-SSOT-2.0 §4A.11、§40 |
| 支援输入 | 3–5步固定序列 · CANON | SRC-SSOT-2.0 §4A.11 |
| Meter threshold/value | 100 · TEST；包内容见测试参数 | SRC-SSOT-2.0 §41.4 |
| Draft断线等待 | 20秒 · TEST候选，不暂停模拟 | 本轮边界提案 |
| 击杀稳定补足Ammo | 不允许作为Operation正常经济 · CANON | SRC-SSOT-2.0 §4A.11 |

## 示例

ECO-011 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

正常：队伍缺Ammo但想要枪械模块，主动去Vault取得额外知识后再决定。失败：两人同投最后一Charge，第二人收到余额变化提示且没有扣任何费。跨系统：合法模块把团队标记窗口转成节省装填时间，不生成Ammo；它改变战术，不免费解除整个资源约束。

## 验收与尚未实测项

ECO-012 · TEST · 来源：本轮实验建议。

覆盖并发Beacon、重复拾取、丢包重传、Pod出现前迁移、draft加入/离队/重连、关键Cell越界。预算实验记录供给、实际支出、末段可行选择和是否出现所有人永远选Energy/Modification Pod。阈值、设施覆盖率、授权成本及资源池准入尚未实测。
## 最新 Operation 奖励与重资产边界

ECO-013 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮用户武器配件与Team Ordnance讨论。
Operation奖励确定为WeaponModule/ToolModule/TeamProtocol，数量由[测试参数](../production/test-profile.md)拥有，原Relic目标只属Lab。普通Supply不补充Team Ordnance固定弹药；它是独立世界资产，不接通用reserve拾取/复制路径。经济准入同时检查效果真正写的ResourceKind与权限，不能仅凭“它叫配件”就认为安全。传统Relic/自动Fusion仅留Lab/FUTURE；当前Operation选择由DDD-0014记录，不存在两套并行官方经济。

## 区域回报与外观信用点

ECO-015 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：SRC-USER-2026-09-05-REGION-RISK-REWARD-PROFILES；SRC-USER-2026-09-05-OPTIONAL-GLYPH-REROUTES。

无限探索区的较高风险对应较高毛回报：可撤离废料、稀有材料、字形知识与筑路者资料密度更高；限界探索区则把更多价值放在当局弹药、医疗、封闭储备及可转友军的固定防御上。区域标签只调整内容预算和来源组合，不直接乘算所有掉落。高风险区可以单局给更多外观信用点价值，但不保证比安全区拥有更高每小时期望值，避免一种区域成为唯一刷取答案。

可撤离废料在任务中必须选择用于当前Support贡献，或在成功撤离后转换为外观信用点；同一凭据不能两边重复结算。任务关键材料、人造太阳燃料、冷却介质和控制部件不得出售换外观。外观信用点只购买外观、展示和不影响战力的自定义内容；无付费战力、无过期商店和无FOMO。团队拾取生成共享任务凭据，结算时向符合参与条件的账号分别提交，不能让抢拾取速度决定谁得到永久外观进度。

字形知识、筑路者资料与成就条件不是可出售货币。它们分别进入Archive/路线知识与成就系统；秘密字形支路的奖励必须在进入前通过风险类型和可见价值做合理提示，不能承诺具体物品后暗换。


## 当前边界闭合

ECO-016 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0014。

Operation文中的旧Weapon/Relic draft实例现为允许的Modification/供给实例，传统Relic只在Lab。包的实际弹量、Med量、首轮等待采用测试参数；高价值各Seat资格一次，后进者继承Seat状态不重置。非法投递的返费事务必须与“不生成物资”一起提交，合法Pod落地后的战术损失不返费。废料同凭据用于Support或成功撤离外观收益二选一，不双算；未撤离部分收益0，已Banked知识100%保留。
