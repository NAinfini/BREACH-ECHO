---
doc_id: GDD-PROGRESSION
doc_type: gdd
stage: DRAFT
updated: 2026-09-05
owner_role: 进度设计
canon_basis: "SRC-SSOT-2.0 §4A.16、§24；SRC-USER-2026-09-04-PLAYER-MASTERY-PROGRESSION；SRC-USER-2026-09-05-COLLECTIBLE-ACHIEVEMENT-LORE"
depends_on: ["economy-and-support.md"]
---

# 知识、永久进度与壁垒

## 玩家目的与范围

失败仍留下发现和理解，成功让世界承认任务完成；账号不会靠永久伤害数字逼新玩家先刷级。此文件拥有上传与账户结算，Support经济另见[资源](economy-and-support.md)。

PRG-001 · CANON · 来源：SRC-SSOT-2.0 §24.1、§24.3。

永久成长是横向：Character、Weapon/Utility/Relic/Spell池资格、cosmetic/title、Knowledge/Archive、Fusion与Operation发现、Test Chamber、challenge/history/mod内容。无必需永久战斗属性，无永久装备仓把局内强武器/Relic/Spell/Utility带入下一局；Build快照可保存和展示。

PRG-002 · CANON · 来源：SRC-SSOT-2.0 §4A.16。

失败保留已上传/Banked Knowledge/Data的100%、Cosmetic/Fusion Discovery；Run Weapon/Relic/Spell/Utility/Prototype不永久继承，Mission Completion Bonus失败无。代币失败比例是测试而非保证。成功与失败结果都须有可追踪凭据。

PRG-003 · DIRECTION · 来源：SRC-SSOT-2.0 §24.2、§24.4。

Archive Credits命名/结算待统一；壁垒是物理Hub+快捷菜单，服务不强迫反复跑NPC，Archive做知识调查，Test Chamber复用真实Scenario，战利品/历史/外观可展示。

## 玩家流程

PRG-004 · PROPOSED · 来源：本轮系统扩写。

取Data→团队获得当局Support价值→到明确上传节点→看上传到账→结束页分别列已永久存入、仅本局、任务完成奖励、失败损失→回壁垒读发现/解锁。上传知识不第二次增加Support；一份数据的两种用途使用关联凭据但不同账本。

## 状态与数据所有权

PRG-005 · PROPOSED · 来源：本轮系统扩写。

Session authority持有CollectedData/UploadTransaction/ResultID；Account处理StructuredClaim，Host不能写其他账号。知识ID与用户资格组合成幂等claim key。团队收集的上传知识候选按上传时在场seat及其此前参与凭据授予资格，后加入不追溯所有历史；该公平规则待实测。

| 起点 | 事件 | 结果 |
|---|---|---|
| WorldData | 唯一採集事务 | Collected，发一次Support贡献凭据 |
| Collected | 合法上传节点提交 | BankedClaim，保留内容与参与名单 |
| BankedClaim | 账号确认收到 | Acknowledged，持久可见 |
| RunActive | 成功/真正失败 | ResultClaim，分别计算完成与保留项 |
| ResultClaim | 重传/重新登录 | 幂等确认，不双倍代币 |
| NetworkUnavailable | 账号暂无法确认 | Pending显示未确认，不伪成功 |

## 模式、内容与边界

PRG-006 · PROPOSED · 来源：本轮系统扩写。

Operation在前线设施的合法上传点提交数据；Descent可按层bank但是否首发由模式决策控制。Account unlock可以只扩充可选池，不强迫永久把玩家偏好池稀释；具体pool策展OPEN。故事关键证据与普通资源ID分开，不能卖给商店或当耗材。

死亡前未提交上传仍未bank，迁移冻结不改变资格；上传与Wipe同帧按commit序，不能“界面点过就算”。Account拒绝claim时显示具体待处理状态。离队不复制Run实例，已banked资格不因后来换Host丢失。单人离线须有可验证本地结构化账，不依赖持续联网才能正常玩。

## 参数

| 参数 | 值/状态 | 来源 |
|---|---|---|
| 失败banked knowledge保留 | 100% · CANON | SRC-SSOT-2.0 §4A.16 |
| 失败Operation/Archive代币 | 约成功应得50% · TEST | SRC-SSOT-2.0 §4A.16、§40 |
| Upload节点频率/一次用时 | OPEN | 不以任意数字假装解决长局失败 |
| 永久战斗属性 | 不提供必需数值 · CANON | SRC-SSOT-2.0 §24.1 |

## 示例与验证

PRG-007 · PROPOSED · 来源：本轮系统扩写。

正常：中段上传关键记录，终局失败后仍能在Archive阅读。失败：上传进度未commit玩家倒地，UI不列为已保留。跨系统：同一Data已贡献Support，上传只生成Account claim，不再刷Charge。

PRG-008 · TEST · 来源：本轮实验建议。

验证重复结果、迁移中上传、断网后重试、部分玩家离队、成功后再次失败消息都不重复/丢失合法claim。10小时测试问玩家还想追哪两项横向目标，不能用代币数量替代复玩动机。

## 玩家掌握作为长期成长

PRG-009 · DIRECTION · 来源：SRC-USER-2026-09-04-PLAYER-MASTERY-PROGRESSION。

玩家玩得越久、学得越多，实际表现应越强；长期成长优先来自player knowledge与skill，不来自局外数值碾压。可教学、可观察、可复现的技巧包括取消窗口、预输入、蓄力衔接、路线/敌人/资源知识、噪声管理和队伍协同。新手应能完成基本动作，高级技巧提高效率与安全裕度，不取消弹药、噪声、遭遇或合作规则；具体操作合同见[战斗CMB-014](combat-and-arsenal.md)。

技巧不能依赖隐藏Bug、特定超高FPS、宏或外部攻略。单一技巧包括bunny hopping不得成为强制动作税，也不得摧毁潜行、资源、队形与遭遇设计；失败反馈应说明规则与原因，而不是只让玩家猜输入时机。

PRG-010 · TEST · 来源：本轮玩家掌握验证建议。

按可控经验组记录完成率/胜率、任务耗时、弹药与医疗效率、受伤和队友救援，并检查技巧能否通过游戏内观察与练习学会。跨不同帧率、网络条件、键鼠/控制器测试相同窗口的公平性；若某项技巧成为mandatory tech、宏显著上位或新手无法完成基本动作，则该技巧设计失败而非“玩家不够硬核”。

## 字形知识与外观进度

PRG-011 · DIRECTION · 来源：SRC-USER-2026-09-05-REGION-RISK-REWARD-PROFILES；SRC-USER-2026-09-05-OPTIONAL-GLYPH-REROUTES；SRC-USER-2026-09-05-NODES-LORE-ONLY-DESCENT-COMMUNITY-EVENT。

基础游戏不记录或显示战略节点、节点所有权、清场率、恢复百分比或账号剧情阶段。永久进度只拥有横向账号解锁、故事收藏、知识、成就/挑战和外观；普通程序合同不需要声明自己在唯一时间线中永久改变了哪个地点。字形知识解锁可验证的秘密路线、Archive解释和新的可选支路，不直接增加伤害。筑路者资料只推进世界理解与允许的横向内容。

外观信用点来自成功撤离并结算的合法废料凭据，只用于外观与展示。无限探索区单次成功可提供更高毛回报，但失败概率、耗时和资源成本必须进入测试；不得用隐藏衰减、每日任务或限时奖励强迫重复刷取。秘密字形路线可授予一次性成就、外观或知识发现，重复游玩只按公开规则提供普通回报。

Descent入口不靠单个账号平时积攒隐藏节点进度。它只在PRG-013的全服务器联合行动完成后，作为唯一正史中的公共端点开放；Descent失败不会回滚该公共历史状态。

## 壁垒任务板与非递进叙事

PRG-012 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-PROCEDURAL-OPERATION-HUB-BOARD；SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY；模式合同见[Operation OPS-011](operations.md)。

壁垒中央Hub的任务板是Operation Offer的权威入口；为尊重玩家时间，物理任务板与快捷菜单只显示同一份数据，不得形成两套任务池。每张卡至少展示区域、设施主题、主任务、支线、已知局势、奖励、预计长度和当前选择的难度。所有基础合同完成后只结算资源、故事收藏、知识、挑战和外观资格；没有合同提交账号剧情阶段、节点或路线版图。

程序任务板与唯一正史不互相冒充。普通Offer的数量、刷新方式和周期仍OPEN；禁止用现实时间轮换让玩家永久错过故事收藏、必要装备或唯一知识。联机时所有玩家共享本局任务状态，故事收藏与一次性成就按各账号既有资格幂等结算；队长的Archive完成度不改变其他人的任务池，也没有需要同步的个人剧情世界。

PRG-014 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-COLLECTIBLE-ACHIEVEMENT-LORE；内容规则见[中央故事STORY-011](central-story-spine.md)。

碎片叙事形成个人Archive收藏进度，但不是战役进度。玩家可按事件、人物、设施、Faction与可信度重组日志、物品说明、环境推断和成就记录；完成单条发现、主题集合或隐藏字形挑战可授予档案完成标记、成就、称号、外观或Hub展示物，不授予主任务所需能力或数值战力。游戏内Archive拥有完整条目与关联，平台成就只镜像里程碑，离线或未连接平台服务也不能丢失故事内容。

一名玩家在任务内确认收藏时，为所有当局在场且符合资格的玩家生成同一发现凭据；重复拾取只提示已收录，不重复发放唯一奖励。核心公共事实不要求收集，收藏负责解释局部事故、人物立场、技术来源和历史细节。重要集合不得依赖限时活动或单一随机Seed，缺失条目可提示所属主题和仍缺数量，但不直接剧透具体房间答案。

PRG-013 · DIRECTION · 来源：SRC-USER-2026-09-05-NODES-LORE-ONLY-DESCENT-COMMUNITY-EVENT；活动模式见[Operation OPS-013](operations.md)。

节点恢复进度只在Descent DLC发布联合行动期间存在，且为全服务器共享活动账。符合公开条件的Operation完成后提交一次防重复贡献；服务器汇总阶段进度并驱动Hub广播、路线图和端点状态变化。活动结束并开放端点后，节点计数冻结为历史记录，不转成日常赛季等级、个人战力或永久重复刷条。

该活动不能成为付费内容的永久门锁。晚加入者、未参加活动者和活动后购买DLC的玩家看到的是已经完成的公共历史，并可正常进入Descent；参与者奖励只允许纪念外观、称号或Archive记录，不授予影响Operation平衡的独占战力。本作是合作PVE，不为该公共进度建设作弊检测；服务只负责合法格式、账号归属和ResultID去重。离线贡献、服务器分区、目标阈值和活动失败语义仍OPEN。
