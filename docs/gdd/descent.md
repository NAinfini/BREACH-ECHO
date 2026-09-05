---
doc_id: GDD-DESCENT
doc_type: gdd
stage: FUTURE
updated: 2026-09-05
owner_role: 候选模式设计
canon_basis: "SRC-SSOT-2.0 §4B、§37、§40、§42；最新Operation优先建议；SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY"
depends_on: ["modifications-and-effects.md", "narrative-bible.md"]
---

# Descent：保留基线与未来候选

## 玩家目的与范围

为希望快速形成组合、连续转化并突破战斗规模的玩家提供另一种节奏。本文件保留源基线，不构成首发承诺；已选择未来扩展，内部Combat Lab仅按实际契约测试需要使用。

DES-001 · CANON · 来源：SRC-SSOT-2.0 §4B.1–§4B.5、§37、§40。

源Descent为五层，单层平均约12分钟，标准约60分钟，可Go Deeper进入Endless；任务轻、战斗密、资源Abundant not infinite、Build快。Layer1 Assemble，Layer2 Specialize，Layer3 Transform，Layer4 Loop，Layer5 Break；不是同一层仅增加敌人数。首层有Hybrid Guarantee：Anchor+可连接选择+Boss/major transformer/pivot机会。Spell扩容、Fusion-on-Fusion、可持续loop和God Build是正常语法。

DES-002 · DIRECTION · 来源：SRC-SSOT-2.0 §4B.3、§42 Phase4。

轻目标可用Clear/Eliminate/Capture/Assault/Hunt/Horde/Destroy/Boss/Moving Front；首批不全做。先三层原型再扩五层。具体每层Boss必要性、奖励节拍、商店、Endless终止、叙事原因仍OPEN。

## REVIEW RECOMMENDATION 与模式流程

DES-003 · PROPOSED · 来源：本轮Operation优先评审。

Descent不进入当前1.0承诺。内部[Combat Lab](../technical/modding-and-toolchain.md)只有10分钟、无任务、高密度奖励的第二消费者，用来证明Kernel没有焊死Operation及测试Proc；它不是公开Descent、完整三层内容或免费第二游戏。

未来批准后流程为局前profile→Layer1保证构筑连接→层间选择/恢复→后续转化→终局/继续深潜→结果。共享数学、资源事务、融合、死亡规则只引用[Build](modifications-and-effects.md)、[经济](economy-and-support.md)、[生命](survival-and-recovery.md)。

## 状态、所有权与奖励保证

DES-004 · PROPOSED · 来源：本轮系统扩写。

Authority持有LayerIndex、RewardSequence、AnchorTags、Offered/Claimed账、连接性证明与profile/RNG版本。保证的是“给过合法可连接的选择机会”，不强迫玩家拿，不读未来随机结果补偿强度。

| 状态 | 条件 | 结果 |
|---|---|---|
| Unanchored | 首个合法奖励节点 | Offer含至少一个可用Anchor |
| AnchorOffered | 玩家拒绝/Pass | 记录机会，下一节点仍给可用备选，不强塞 |
| Anchored | 检查当前Build可连接标签 | 后续至少一项可消费其输出/输入 |
| LayerEndPending | 未给transformer/pivot机会 | 使用预先预留的固定奖励槽补足；不凭空改敌人 |
| LayerResolved | 单次完成事务 | 结算层奖励/恢复再推进 |
| Break/Endless | 玩家继续且profile合法 | 新的公开循环规则，版本固定 |

不可用奖励被剔除，例如没有Staff且无法合法获取时不以Spell当唯一保证。多人各有eligibility与机会账；共享物品也必须记录轮次，不让最快抢者把其他人保证全部吃掉。四名固定角色各自拥有Build保证状态；即使装备相同也不共用机会账。

## 模式配置与边界

DES-005 · PROPOSED · 来源：本轮系统扩写。

Ammo/Medical/Utility补给与Support成长更宽松，可按战斗/目标获得；Supply更偏Weapon/Relic/Prototype，但资源变量仍真实存在，否则Reload/Heat等词条会失去意义。不迁入Operation的多终端和Cart规划。推荐未来高阶效果按独立能力profile准入，不要求所有Operation配件两边同样平衡。

掉线/死亡不刷新offer RNG；领取与Fusion同事务关联，不能先发双份后清理。层间恢复不回滚物资与任务历史。玩家拒绝所有连接奖励时可形成弱Build，保证不等于强迫获胜。Boss被合法Build融化不临时生成抗性。

## 参数

| 项目 | 值/状态 | 来源 |
|---|---|---|
| 正式层数/节奏基线 | 5层、每层约12分钟、Run约60分钟 · CANON pacing target | SRC-SSOT-2.0 §4B.1、§40 |
| 先行层数 | 3 · TEST | SRC-SSOT-2.0 §42 Phase4 |
| 内部Lab时长 | 10分钟 · TEST候选 | 本轮架构契约实验，不是Descent层数 |
| 每层奖励数/恢复量/Endless曲线 | OPEN | SRC-SSOT-2.0 §41.5 |
| 是否首发/是否制作 | 不进入基础1.0；未来另过制作Gate | DDD-0013/0018 |

## 示例与验证

DES-006 · PROPOSED · 来源：本轮系统扩写。

正常：首层选ReloadAnchor，后续出现与ReloadCompleted连接的选择，第三层转换武器行为。失败：玩家拒绝全部连接，系统显示可连接标识但不自动改装；不能事后“为保底”改掉落。跨系统：高频资源回路在Lab规则集授权，Operation池没有该能力，差异在入场profile可查。

DES-007 · TEST · 来源：本轮实验建议。

重放奖励序列、多人各自连接机会、拒绝/断线/迁移、已有合成导致offer失效等，要求无死奖励和重复结算。外部试玩需要玩家复述“行为如何变了”而非只说伤害更高；正式双模式必须证明额外关卡、教程、平衡和QA成本可承担。

## 行星端点与正史位置

DES-008 · DIRECTION · 来源：SRC-USER-2026-09-05-NODE-CLEARANCE-AND-PLANETARY-DESCENT；SRC-USER-2026-09-05-NODES-LORE-ONLY-DESCENT-COMMUNITY-EVENT；世界边界见[世界观NAR-030](narrative-bible.md)。

Descent不从基础游戏任务板无条件出现，平时也不让单个玩家积攒隐藏节点进度。准备发布DLC时，全服务器联合行动才在玩家层面重新引入节点恢复：社区完成指定程序Operation，逐阶段恢复通往一个真实行星的路线；端点通信、防御、撤退路线和入场条件成立后，它在唯一正史中永久开放为Descent前进基地。候选端点包括虚空兽原生贫能天体、灼星种世界和借尸者占领行星，不要求三类同时制作。

每次Descent Run代表同一正史中的一次新地表、地下或设施纵深远征。程序图选择尚未探索的行动区域、入口条件和局势，不让同一房间的死亡敌人复活，也不回滚已经开放的公共端点。Run内快速构筑解释为本次远征收集和装配的临时模块、异星器材与现场协议；结算后不把指数战力带回Operation，只带出被奖励合同允许的知识、外观进度和战略资源。

## 必须正面解决的产品风险

DES-009 · RISK · 来源：game-design评审；SRC-USER-2026-09-05-NODE-CLEARANCE-AND-PLANETARY-DESCENT。

这条设定只解决“Descent为什么存在”，没有自动证明它好玩或做得完。最大风险有四项：第一，全服务器节点恢复行动如果只是重复普通任务刷一条数字，会成为上线劳动而不是战争；每个阶段必须改变Hub、任务池或路线局势。第二，基础Operation的程序生成如果只换房间朝向和目标名称，所谓“每局新体验”就是营销谎话。第三，一个敌对行星已经足以形成整套生态、地貌、关卡池、Boss和奖励池；三种阵营各做一颗行星接近制作三款扩展，首批不得同时承诺。第四，如果Descent奖励反过来碾压Operation，资源管理核心就被自己毁掉；若完全不回流，它又会像孤立小游戏。因此只允许知识、外观和经过上限控制的战略资源跨模式，指数战力永久隔离。

进入三层公开原型前必须证明：联合行动的阶段变化不只是数字；程序任务板能持续生成合法且可辨识的普通Operation；一个行星主题能用有限资产组合出足够多的可辨识区域；Descent回流奖励既值得追求又不能让Operation补给失去意义。任一项失败，保留端点世界观，但不制作公开Descent。

DES-010 · DIRECTION · 来源：SRC-USER-2026-09-05-NODES-LORE-ONLY-DESCENT-COMMUNITY-EVENT；活动与进度责任见[Operation OPS-013](operations.md)和[进度PRG-013](progression-and-bastion.md)。

全服务器联合行动是Descent发布事件，不是基础游戏常驻系统。活动期间，指定Operation贡献节点恢复进度；达到阶段阈值后，Hub与任务板依次显示路线识别、通信恢复、前沿防御建立和端点稳定，最终开放第一个Descent目的地。节点名称与进度只在该活动叙事中出现，活动结束后不保留为日常地图清单或赛季刷条。

活动进度可以影响开放仪式与纪念记录，不能决定已购买内容是否永远可玩。即使社区活跃度低，也必须按预先公开的确定方案完成路线；活动结束后的玩家直接继承“端点已开放”的公共历史。否则这不是宏大世界事件，只是开发商拿服务器人数绑架DLC入口。


## FUTURE状态如何解释

本文件的奖励、层Boss、Endless、活动阈值等OPEN均是未来产品实验，不是当前基础版待所有者选择的技术问题。基础游戏不需要实现这些系统才能通过文档或M0。未来启动时先用单一行星、三层原型证明内容/节奏，再按五层历史目标扩展；未通过不对外承诺日期或销量。
