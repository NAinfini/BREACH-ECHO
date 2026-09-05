---
doc_id: GOV-DECISIONS
doc_type: governance
stage: DRAFT
updated: 2026-09-05
owner_role: 设计决策维护
canon_basis: "SRC-SSOT-2.0 §37、§39、§41、Appendix B；本轮用户讨论"
depends_on: ["authoring-guide.md", "../gdd/vision.md"]
---

# 决策、冲突与未决问题总览

## 最新决策入口

DEC-001 · OPEN · 来源：SRC-SSOT-2.0 §1.1、§4；SRC-USER-2026-09-04-OPERATION-FOCUS。
源双模式基线与最新Operation优先建议必须显式裁决；强烈推荐不等于用户已批准。详见[DDD-0001](decisions/DDD-0001-operation-vs-roguelike.md)。

DEC-002 · OPEN · 来源：SRC-SSOT-2.0 §4A.15、§5、§9；本轮武器改装讨论。
Operation固定loadout、Weapon/Tool Modules、排除自动Fusion与原Relic/自动合成基线冲突；同时两枪一工具与两Weapon/两Utility/一Active尚未统一。[配装决定](decisions/DDD-0003-operation-field-modification.md)、[统一模型](decisions/DDD-0004-unified-modification-model.md)。

DEC-003 · DIRECTION · 来源：SRC-USER-2026-09-04-MODULAR-REFINEMENT。
模块化偏好明确，具体替换边界/通用接缝/权限/API冻结仍PROPOSED；[DDD-0002](decisions/DDD-0002-modular-product-architecture.md)。

DEC-004 · DIRECTION · 来源：SRC-USER-2026-09-04-ORDNANCE-MISSIONS。
团队重资产与前向Predator/Breach意图归[DDD-0005](decisions/DDD-0005-team-ordnance.md)、[DDD-0006](decisions/DDD-0006-predator-and-breach-missions.md)。具体卡/权威/旁路候选尚未实测。

DEC-005 · OPEN · 来源：SRC-SSOT-2.0 §18.1、§21、§27–§28；本轮12月范围评审。
延后TPS、完整TC/Forge/Workshop或调整托管/发行范围会影响原基线，未经批准不能直接删除。理由与替代见[制作计划](../production/roadmap-and-validation.md)。

DEC-006 · CANON/PARTIALLY SUPERSEDED · 来源：SRC-USER-2026-09-04-SINGLE-STORY；SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY。
唯一客观历史继续有效；旧“逐账号中央主线、Final Truth与唯一主结局”作为基础版产品结构已被非递进程序合同方向覆盖。现行规则见[STORY-001](../gdd/central-story-spine.md)，理由见[DDD-0007](decisions/DDD-0007-single-canonical-story.md)。

DEC-009 · CANON · 来源：SRC-USER-2026-09-04-FIRST-BUILDER-UTILITY；SRC-USER-2026-09-04-FIRST-BUILDER-PROTOTYPES。
用户确认筑路者基础设施的初始用途及部分Prototype技术谱系；作者层客观事实唯一责任为[世界观NAR-010](../gdd/narrative-bible.md)。中央故事和战斗文档只引用该条，不得补定具体机制、Breach责任、具体武器或制造关系。

DEC-010 · CANON · 来源：SRC-USER-2026-09-04-FINAL-STORY-OVERVIEW-BLIND-REVIEW；按SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY调整对象。
客观历史、公开知识、四名固定队员、当前Operation时代和公共事件边界排完后，才生成完整总览供用户审阅，之后按[GOV-007](authoring-guide.md)与[STORY-006](../gdd/central-story-spine.md)启动全新只读agent盲审；不再等待五幕、最终揭示或Post-story状态。当前人物仍未完成，不触发盲审。

DEC-011 · OPEN（READY FOR USER VERDICT） · 来源：SRC-USER-2026-09-04-OBJECTIVE-HISTORY-FIRST；SRC-USER-2026-09-05-NATIVE-MANAGEMENT-HUMAN-DATA-LAYER；SRC-CODEX-2026-09-05-OBJECTIVE-HISTORY-CURRENT-CANDIDATE。
用户已锁定“先裁决作者层客观历史，再设计玩家经历”的工作顺序。NAR-011当前以一套技术分层连接完整历史：筑路者原生空间与管理层继续工作，人类数据与权限层可以独立崩溃；安全重启改变载波和字形路由，人类只能靠近距链路或携盘逐节点恢复；限界派灾备优势加剧无限派扩张压力；虚空兽规模来自宇宙空洞天体上的长期休眠积累；最后关闭权限范围内的整张活动网络；当代壁垒受人造太阳数月倒计时逼迫，按节点恢复并永久清场，抵达真实敌对行星后才具备Descent的世界观入口。整条连接因果仍待用户批准；客观历史只在[NAR-011](../gdd/narrative-bible.md)，玩家五幕不得反向决定历史。

DEC-012 · DIRECTION · 来源：SRC-USER-2026-09-04-GUN-ONLY-CONDITIONAL。
用户倾向GTFO-like非Roguelike首发；“正式确认后删Staff/Arcane、远程只留枪”的条件尚未满足。现在保留CMB-002及Staff 3/6，不建立永久双轨。

DEC-013 · LEGACY · 来源：SRC-USER-2026-09-04-BRIDGE-GUN-CANCELLED。
从界桥持续汲能的低伤无限弹药枪已被用户取消：Heat/等待不构成永久资源成本，会奖励安全磨怪并击穿资源管理。它不得回到active候选。

DEC-014 · DIRECTION · 来源：SRC-USER-2026-09-04-ENERGY-EM-GUN-FAMILIES；SRC-USER-2026-09-04-RESPONSIVE-GUNPLAY-CANCEL-WINDOWS。
当前active枪械方向为传统动能、电磁、有限Energy Block；Energy Block三子型是三把枪。该重做方向与CMB-002现有Energy热量基线的覆盖关系尚未裁决；响应性窗口与全部资源/声音/穿透/友伤/补给参数均须测试，详见[CMB-012–CMB-015](../gdd/combat-and-arsenal.md)。

DEC-015 · DIRECTION · 来源：SRC-USER-2026-09-04-PLAYER-MASTERY-PROGRESSION。
长期成长优先来自可教学、可观察、可复现的player knowledge/skill，不来自局外数值碾压；守门与测试见[PRG-009–PRG-010](../gdd/progression-and-bastion.md)。

DEC-016 · CANON · 来源：SRC-USER-2026-09-04-WORLD-NAMING-CHINESE-SELECTION；SUPERSEDES：SRC-USER-2026-09-04-WORLD-NAMING-SELECTION与SRC-USER-2026-09-04-WORLD-NAMING-NATURAL-WORKING。
用户已选定中文正式命名；具体主名称、口语称呼、机构分类、旧称及法律状态只见[世界命名NAM-002–NAM-003](../gdd/world-naming.md)。本决策只记录“选择已经发生”，不复制第二份名称表；对应世界事实和未来内容状态不随命名升格。

DEC-017 · CANON · 来源：SRC-USER-2026-09-04-TWO-EXPLORATION-DOCTRINES；SRC-USER-2026-09-04-CIVIL-WAR-HISTORY-GAP；SRC-USER-2026-09-04-WAR-BEFORE-EXTERNAL-CONTACT；SRC-USER-2026-09-04-EXPLORER-DEFENSE-ORIENTATION；SRC-USER-2026-09-05-THREE-WAY-DISCONNECTION；SRC-USER-2026-09-05-BASTION-KNEW-DOCTRINES-NOT-WAR；SRC-USER-2026-09-05-BASTION-TWO-INTERNAL-CAMPS。
人类内战的两种探索路线、内战先于外敌、无限探索派防御朝向人类边界、三方最终失去实用远程双向联系、壁垒在最后具名公共消息仍畅通时知道外部两派且内部也分成两个政治阵营、但不知道外部两派后来发展成内战，以及内战造成历史断层均已由用户确认；“失联”不否定NAR-014允许本地与迟到的常规信号。NAR-016–NAR-030已经锁定冲突命令与载波重置、近距/远端恢复差异、内战导火索、停战双重证据、围困、撤离失败、权限迁移失败、最终全网停摆、虚空兽生态、外勤旧制身份、节点永久清场及行星Descent边界。壁垒内外同路线阵营之间的组织隶属、实体交接、外部战区距离、准确时长及其余NAR-011历史仍为PROPOSED/OPEN。

DEC-018 · CANON · 来源：SRC-USER-2026-09-05-CONVENTIONAL-COMMS-DISTANCE。
界桥断开不关闭物理上可达的常规通信：同一星球及其他附近节点仍可用无线电/激光通信；跨行星可达性由距离和链路预算决定，不能一概写成收不到；遥远星际信号虽可传播，但不构成即时战略链路。唯一物理边界见[世界观NAR-014](../gdd/narrative-bible.md)。

DEC-019 · CANON · 来源：SRC-USER-2026-09-05-BASTION-EARTH-GATEWAY；SRC-USER-2026-09-05-BASTION-MULTIROUTE-REAR-HUB；SRC-USER-2026-09-05-BASTION-NETWORK-SPACE。
壁垒在基础设施上是拥有多条通道的共享中枢，至少一支通地球、一支通限界探索区，并因交通与资源汇聚而具备储备、防御设施和驻军；在存在方式上，它位于筑路者生成的有限人工节点空间，不在普通天体上，无法靠常规航行、开采或扩建逃离；在战略纵深上，它又是限界探索区后方、地球前方的门关。外敌逻辑纵深为外拓区→无限探索派→限界探索派→壁垒→地球；唯一事实正文见[世界观NAR-015](../gdd/narrative-bible.md)。

DEC-020 · CANON · 来源：SRC-USER-2026-09-05-BASTION-ISOLATION-AUTHORITY；SRC-USER-2026-09-05-CONFLICTING-ORDERS-SAFETY-RESTART；SRC-USER-2026-09-05-NATIVE-MANAGEMENT-HUMAN-DATA-LAYER。
限界探索派提交隔离命令，无限探索派提交冲突的恢复命令并强制覆写；覆写失败触发筑路者原生管理层安全重启和路线重配。重启改变节点载波与字形路由状态，人类建立在其上的译码、地址、同步、身份和远程控制层因此失去共同状态，壁垒在战前隔离。人类数据层失效不等于原生管理失效，也不等于节点已物理摧毁；近距与远端恢复边界由DEC-032锁定。最终封网由死城操作人员调用既有原生隔离功能；地球支路关闭时，壁垒只得到“地球链完整性失效”的原生状态翻译。唯一事实正文见[世界观NAR-016、NAR-026与NAR-029](../gdd/narrative-bible.md)。

DEC-021 · CANON · 来源：SRC-USER-2026-09-05-AUTHORITY-TRANSFER-NO-TIME；SRC-USER-2026-09-05-EMERGENCY-FOLD-LOCAL-COMMIT；SRC-USER-2026-09-05-FINAL-SEQUENCE-AUTHORITY-CORRECTION。
最高权限迁移属于人类数据与控制层；迁移包包含最后共同认可的拓扑目录、根身份状态和重新签发跨域身份的权力，必须由壁垒在线接收和确认。迁移尝试时无限探索派仍存在并参与决定；壁垒无法在线回执，而物理方案必须重新解出连续字形路线、携盘逐节点重写并穿过虚空兽封锁区，已经没有完成这条链的时间。最终关网由死城本地操作人员直接调用仍工作的筑路者原生管理接口，不是同一事务，也不需要把人类解释发送给壁垒。唯一事实正文见[世界观NAR-017与NAR-029](../gdd/narrative-bible.md)。

DEC-022 · CANON · 来源：SRC-USER-2026-09-05-CIVIL-WAR-SPARK。
人类内战的直接导火索为：无限探索派试图启用因无人探针异常失联而被限界探索派判为危险的外拓干线；该区域的已知电磁风暴又足以把损失解释为正常勘探风险，因此证据真实但模糊。限界探索派命令守门人隔离，无限探索派派员强闯，造成人类伤亡并使冲突升级为战争。具体第一枪、伤亡机制与规模仍OPEN。唯一事实正文见[世界观NAR-018与NAR-022](../gdd/narrative-bible.md)。

DEC-023 · CANON · 来源：SRC-USER-2026-09-05-CEASEFIRE-DUAL-PROOF；SRC-USER-2026-09-05-FINAL-CONTAINMENT-SACRIFICE；SRC-USER-2026-09-05-VOID-ECOLOGY-AND-EXTERNAL-USERS。
无限探索派在初次接敌后必须同时向限界探索派提供可验证锚点数据与虚空兽实体样本，才足以促成停战。此后逐能虚空兽占据多个供能出口和外围据点。相对顺序已锁定为“发现封锁→尝试撤离→确认全线迁移失败→尝试迁移权限给壁垒但因壁垒离线失败→两派共同授权最终下线”。实体样本物理交接、具体节点和各阶段时长仍OPEN。唯一事实正文见[世界观NAR-019与NAR-023](../gdd/narrative-bible.md)。

DEC-024 · CANON · 来源：SRC-USER-2026-09-05-BASTION-ENERGY-PRESSURE。
当代壁垒闭合域仍包含若干仓储、农业、维护和防御设施，并与本地守门人保持合同链；这些设施全部位于同一个有限人工空间内，不构成新的领土或逃生出口。人口和设施负荷增长已使可稳定供应的能源不足，继续换取本地托管蓝图与技术许可还会占用额外资源。该事实单独不能推出“必须重开”；完整原因已由后续DEC-026锁定。唯一事实正文见[世界观NAR-020–NAR-021](../gdd/narrative-bible.md)。

DEC-025 · CANON · 来源：SRC-USER-2026-09-05-FINAL-SEQUENCE-AUTHORITY-CORRECTION；SRC-USER-2026-09-05-FINAL-SHUTDOWN-SCOPE；SRC-USER-2026-09-05-FULL-ACCESSIBLE-NETWORK-SHUTDOWN。
灾难末期相对顺序及封线范围已经确定：安全重启使壁垒外部会话失效；停战后两派发现虚空兽封锁出口，撤离失败；随后迁移权限给壁垒因壁垒无法回执而失败；两派最后共同授权关闭本地原生接口能够触及的全部活动路线和非必要节点供能，其中包括外拓区、两派区域、壁垒对外路线、壁垒—地球支路及其他在线节点。整张可达网络中的能量梯度由此消失。精确小时数、逐节点执行方式、根设施位置与人员结局仍OPEN。唯一事实正文见[世界观NAR-023](../gdd/narrative-bible.md)。

DEC-026 · CANON · 来源：SRC-USER-2026-09-05-BASTION-ENERGY-CLOSURE-APPROVAL。
当代重开动机采用两项组合：第一，壁垒是依赖多路输入的中枢，不是为长期独立、自给自足设计的殖民地，所在人工空间没有自然矿脉、生态圈或可开拓疆域；第二，维持文明的人造太阳受同一条长期维护与供应链断裂影响，聚变燃料、冷却介质和电磁约束组件均接近终点，本地不能完成补给或制造替换件。守门人能提供修复蓝图，却没有材料或完整工业设备可交付。配给只能延迟，不能消除数月倒计时，因此壁垒以工程方式重建一条目标明确、可隔离、可再次摧毁的旧路线；目标节点、库存数值和先失效子系统仍OPEN。唯一事实正文见[世界观NAR-020、NAR-021与NAR-025](../gdd/narrative-bible.md)。

DEC-027 · CANON · 来源：SRC-USER-2026-09-05-FIRST-BUILDER-PEACEFUL-COLLAPSE；SRC-USER-2026-09-05-BUILDER-SUCCESSOR-DECLINE。
筑路者是长期和平、科研与网络工程强而武器和军事组织相对薄弱的文明；虚空兽在其仍存续时进入界桥网络。筑路者随后急速发展军备，但速度追不上网络内扩散，只能主动关闭界桥网络。封网摧毁统一供应链后，大多数隔离聚落因资源与工业能力不足而消亡；少数存续社会也因人口、知识链和专业分工断裂而严重技术退化，不再具备全盛时期的网络建造能力。唯一事实正文见[世界观NAR-024](../gdd/narrative-bible.md)。

DEC-028 · LEGACY/PARTIALLY SUPERSEDED · 来源：SRC-USER-2026-09-05-BASTION-POWER-CONVERSION-FAILURE；SUPERSEDED BY：DEC-036。
旧稿把危机对象写成一台独立的通用能源转换设施；该对象已被人造太阳的燃料、冷却与电磁约束系统取代，不得作为并行故障复活。仍有效的边界只有界桥不凭空造能、传能接口不是人口交通门，以及稳定能源丧失会让农业与生命支持连锁崩溃。

DEC-029 · CANON · 来源：SRC-USER-2026-09-05-BASTION-NETWORK-SPACE；SRC-USER-2026-09-05-NATIVE-MANAGEMENT-HUMAN-DATA-LAYER。
壁垒位于筑路者技术生成的有限人工节点空间，不在普通天体上，不能通过常规工程向外扩张、开采或逃离。界桥空间与路线管理是筑路者原生技术；人类只掌握部分操作，并在其上建立数据、身份、档案和远程控制层。人类数据层失效不等于原生管理层失效，最终关网由现存本地控制站调用原生管理功能。唯一事实正文见[世界观NAR-015、NAR-016与NAR-026](../gdd/narrative-bible.md)。

DEC-030 · CANON · 来源：SRC-USER-2026-09-05-VOID-ECOLOGY-AND-EXTERNAL-USERS；SRC-USER-2026-09-05-POWER-DOES-NOT-INSTANT-WAKE；SRC-USER-2026-09-05-VOIDBEAST-ACCUMULATED-POPULATION。
宇宙空洞是正常宇宙中的极端低密度区域，只有零散恒星、暗弱天体和行星系；黑暗、贫能与资源匮乏孕育了虚空兽。它们会吞食几乎任何可利用物质，尤其追逐高能目标。其入侵规模来自真实天体上历经极长时期积累并长期休眠的大量既存个体，不来自单局快速繁殖。活动界桥泄出的运输与转换能量支持其苏醒、迁徙和较长周期的繁殖；断能会移除食物与迁徙梯度，使活体重新休眠。恢复供能不会立刻唤醒所有个体，仍需局部刺激超过阈值。灼星种与借尸者也分别取得既有网络入口，但网络控制能力低于人类。唯一事实正文见[世界观NAR-027](../gdd/narrative-bible.md)。

DEC-031 · CANON · 来源：SRC-USER-2026-09-05-LEGACY-ID-LOW-CLEARANCE。
壁垒外勤小队使用从断网前身份体系继承并在本地重新签发的旧制凭证。远端设施通常能识别其格式，却无法验证最新授权链，所以只提供低级、局部或过期权限；同一身份在不同节点可能映射成不同记录，机器只接受本地可验证命令。这是小队必须亲自进入设施并现场恢复权限的直接原因之一。唯一事实正文见[世界观NAR-028](../gdd/narrative-bible.md)与[设施规则WRD-015](../gdd/world-and-information.md)。

DEC-032 · CANON · 来源：SRC-USER-2026-09-05-CARRIER-REBOOT-PHYSICAL-RECOVERY。
安全重启改变节点共振载波与当前字形路由状态；旧人类协议仍能探测信号，却无法译码内容，旧目的地目录也不能直接寻址。近距节点可借无线电、有线或激光交换新样本并恢复；远端节点必须由人员携恢复盘现场读取载波、写入本地译码/身份映射并重建字形路线。恢复盘只提供受信工具和根材料，不是全网通用钥匙。唯一事实正文见[世界观NAR-016与NAR-029](../gdd/narrative-bible.md)、[设施规则WRD-016](../gdd/world-and-information.md)。

DEC-033 · CANON · 来源：SRC-USER-2026-09-05-DOCTRINE-RECOVERY-ASYMMETRY；SRC-USER-2026-09-05-LIMITED-NODE-DEFENSE-ASSETS。
限界探索派在各节点保存协议副本、恢复盘、字形记录、备用资源、独立供电、炮塔和机器人，因此断网后恢复更快；节点正确重写并重新入域后，仍完整且由该节点控制的防御资产可重新识别己方。无限探索派偏重集中调度与吞吐，独立恢复能力较差，这一劣势加剧其重开外拓路线的压力。唯一事实正文见[世界观NAR-029](../gdd/narrative-bible.md)。

DEC-034 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-REGION-RISK-REWARD-PROFILES。
无限探索派区域以低战术补给、高虚空兽压力和高永久发现收益为身份；限界探索派区域以较多弹药/医疗、密集旧防御及重写后的友军资产为身份，但废料、信用点、字形和筑路者知识较少。这是内容预算倾向，不是粗暴倍率，也不保证无限区永远拥有更高每小时收益。具体掉落和兑换由[Operation OPS-010](../gdd/operations.md)与[经济ECO-015](../gdd/economy-and-support.md)负责。

DEC-035 · DIRECTION · 来源：SRC-USER-2026-09-05-OPTIONAL-GLYPH-REROUTES。
玩家可依据关卡内证据改写字形，把节点暂时路由到既存秘密房间或隐藏支路。额外资源、信用点、成就、外观和知识必须由额外敌人、供能、时间、退路或路线暴露承担成本；不采用盲猜字形或Wiki依赖。正式责任见[设施规则WRD-017](../gdd/world-and-information.md)与[任务MIS-015](../gdd/missions-and-spaces.md)。

DEC-036 · CANON · 来源：SRC-USER-2026-09-05-BASTION-ARTIFICIAL-SUN-DEADLINE；SUPERSEDES：DEC-028的通用转换设施对象。
壁垒人造太阳将在数月内被迫停机；聚变燃料、冷却介质和电磁约束/控制组件同时接近终点，是长期隔离造成的同一维护供应链故障。停止交易或配给只能延缓，无法补充关键材料和制造能力。先失效子系统、精确月份和目标维护节点仍OPEN。唯一事实正文见[世界观NAR-020、NAR-021与NAR-025](../gdd/narrative-bible.md)。

DEC-037 · CANON（LORE ONLY）/PARTIALLY SUPERSEDED · 来源：SRC-USER-2026-09-05-NODE-CLEARANCE-AND-PLANETARY-DESCENT；SUPERSEDED BY：DEC-039的玩家进度边界。
作者层世界观仍允许网络按节点重建、有限节点在封闭入口后永久清场，并以真实行星端点承载非时间循环Descent。旧稿把这一结构直接做成基础Operation的玩家可见战略进度，已被DEC-039否决；基础游戏不显示、累计或逐局提交节点状态。

DEC-038 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-PROCEDURAL-OPERATION-HUB-BOARD；SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY。
Operation采用中央Hub任务板与程序任务实例：地图由手制模块程序组合，主任务与兼容支线随机配置，玩家从任务板查看Offer后选择任务和五档难度。所有任务都产生本局内真实系统反应，但基础游戏不提交节点、路线所有权、清场版图或账号剧情阶段。基础版没有必须按顺序完成的主线合同；特殊合同和公共事件可以使用手制内容，但不得建立个人剧情世界。正式责任见[Operation OPS-011](../gdd/operations.md)、[任务MIS-016](../gdd/missions-and-spaces.md)与[进度PRG-012](../gdd/progression-and-bastion.md)。

DEC-039 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-NODES-LORE-ONLY-DESCENT-COMMUNITY-EVENT。
节点在基础游戏中只属于世界观和后台网络结构，不是玩家可见地图、任务类型或常驻进度。只有准备发布Descent DLC时，才开启一次全服务器联合行动并累计指定Operation贡献的节点恢复进度；完成后在唯一正史中永久开放一个敌对真实行星端点。活动后节点计数冻结为历史记录，晚加入或活动后购买DLC的玩家继承端点已开放状态；不得以社区活跃度永久扣留已购买内容。正式责任见[产品VIS-009](../gdd/vision.md)、[Operation OPS-013](../gdd/operations.md)、[进度PRG-013](../gdd/progression-and-bastion.md)与[Descent DES-010](../gdd/descent.md)。

DEC-040 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-MATCHMAKING-AND-EVENT-BACKEND；SRC-USER-2026-09-05-PVE-NO-ANTI-CHEAT。
基础版保留玩家房主权威的Operation会话，同时必须具备账号/身份、Lobby、匹配和服务发现控制面。Descent发布联合行动复用该控制面，增加结果幂等去重与公共进度汇总，不因此改成每局官方专服。轻量部署是成本方向，不是已验证容量。本作是合作PVE，房主作弊是接受的非目标；服务只保护数据格式、跨账号边界、重复结算和公共计数一致性，不建设玩法反作弊。正式责任见[网络NET-001、NET-008](../technical/network-and-persistence.md)。

DEC-041 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-DEBRIEF-AND-REPLAY；SRC-USER-2026-09-05-SIMPLIFIED-REPLAY-AND-STATS；SRC-USER-2026-09-05-DETAILED-STATS-LIGHTWEIGHT-LOCAL-REPLAY；SRC-USER-2026-09-05-POST-DEBRIEF-DISCARD。
每次Operation结算生成详细团队/个人战报和轻量本地行动回放；团队命中率、伤害、击杀、倒地/救援、潜行破坏、资源与目标统计可展开到成员、武器、敌人、阶段和关键事件。回放只保存简化地图、低频位置、关键动作与事件，不保存原始画面、音频、逐帧动画或完整弹道。玩家可从潜行破坏统计跳到对应时刻，查看谁以什么动作惊动了哪些敌人；只有Authority因果链充分时才指名，多人同时触发记共同，证据不足记无法归因。战报与回放由同一权威事件流生成，只保留到该玩家完成本局复盘并确认返回Hub或再开一局，随后删除；首发不建设永久行动档案、导出或跨Build兼容。合作PVE不设唯一MVP、总分或K/D排名。正式责任见[战报RPL-001至RPL-008](../gdd/debrief-and-replay.md)与[技术TRP-001至TRP-006](../technical/replay-recording.md)。

DEC-042 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY；SUPERSEDES：SRC-CODEX-2026-09-05-BASTION-FIELD-TEAM-CANDIDATE的匿名可变编制。
玩家是固定四人编制的“壁垒外勤小队”，四名固定角色在官方世界观中持续存活。每局支持一至四名真人并占用不同角色Seat，少人局不强制Bot；角色身份不锁武器或主任务能力。Wipe不写成正史死亡，也不另造复活机制。四名角色不使用真实姓名；代号、性格、关系和上级机构仍OPEN，美术与身体设定明确延后；完整规则见[STORY-008](../gdd/central-story-spine.md)。

DEC-043 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY。
基础游戏采用非递进玩家故事。开局时外勤小队已经知道人类内战与虚空兽等基础行动事实，不通过五幕、账号阶段或强制主线逐步解锁世界设定。普通Operation是可重复程序合同；可选档案补充局部信息，公共世界变化只通过对所有玩家一致的更新或联合行动发生。现行规则见[STORY-009至STORY-010](../gdd/central-story-spine.md)。

DEC-044 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-COLLECTIBLE-ACHIEVEMENT-LORE。
深层玩家故事采用类似《黑暗之魂》的非线性碎片叙事：日志、物品说明、环境证据、隐藏字形空间与成就集合让玩家主动拼接局部历史。Archive收藏是永久知识进度，不是战役章节；不得锁普通任务或数值战力。碎片可偏颇但须标明事实、证词或推断，程序地图只在语义兼容Cluster中放置；重要集合不能因Seed或限时活动永久错过，合作发现不制造队友争抢。正式规则见[STORY-011](../gdd/central-story-spine.md)、[NDL-004](../gdd/narrative-delivery.md)、[MIS-018](../gdd/missions-and-spaces.md)与[PRG-014](../gdd/progression-and-bastion.md)。

DEC-045 · OPEN（READY FOR USER VERDICT） · 来源：SRC-USER-2026-09-05-FOUR-CHARACTER-DESIGN-REQUEST；SRC-USER-2026-09-05-CHARACTER-PERSONALITY-ONLY；SRC-USER-2026-09-05-CHARACTER-CODENAMES；SRC-USER-2026-09-05-COOL-CODENAME-DIRECTION；SRC-CODEX-2026-09-05-FOUR-CHARACTER-ROSTER-V1。
当前事故型代号候选为`断桥 / 回声 / 铁砧 / 寒蝉`，分别以安全规程、技术求知、生存账本和污染边界审视同一Operation代价；每人都有会帮助也会伤害队伍的优点、明确道德边界、个人收藏链和与另外三人的关系。真实姓名不设计、不显示，也不作为收藏谜底；年龄、性别呈现、外貌、服装、动作外观和配音选角延后。助手强烈建议角色只提供叙事身份，把现有Signature Active改为所有角色可选的配装战术模块；否则Seat会变成职业/强度选择。代号、人物内容与Active解绑均未获用户批准，完整候选见[角色v1](../content/character-roster-v1.md)。

DEC-046 · DIRECTION · 来源：SRC-USER-2026-09-05-GAME-WORKING-TITLE。
当前游戏工作标题为中文《裂界残响》、英文BREACH: ECHO。用户明确保留以后更改的可能，因此不升格为冻结的最终发行名；商店、搜索、商标、域名与社交账号均未完成清查。唯一标题状态见[世界命名NAM-008](../gdd/world-naming.md)。

DEC-047 · CANON · 来源：SRC-USER-2026-09-05-UNITY-ENGINE-LOCK；SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST；详见[DDD-0008](decisions/DDD-0008-engine-unity6.md)。
技术基线已锁定：Unity 6 + URP；GameObject/MonoBehaviour为默认实现，DOTS/Entities/Burst/Jobs只在Profiler证明具体热路径需要时采用；项目采用AI-agent-first工程原则。旧“引擎未锁”“URP/HDRP并行候选”和“默认Hybrid GameObject+DOTS分工”不得继续作为OPEN基线。具体Networking Provider仍未锁。

DEC-048 · CANON · 来源：SRC-USER-2026-09-05-AGENT-FIRST-STRUCTURE-A；SRC-USER-2026-09-05-OFFICIAL-CONTENT-PACKAGES；SRC-USER-2026-09-05-HOST-MOD-AUTO-SYNC；SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY；详见[DDD-0009](decisions/DDD-0009-agent-first-modding-runtime.md)。
Modding基线已锁定：Local UPM Packages + 独立Content数据层；官方内容dogfood同一ContentPackage/Registry/Schema/dependency/version/hash体系；Host Package Lock驱动多人自动同步；Steam Workshop是当前唯一正式公开Mod分发渠道，但PublishedFileId只属于Distribution Adapter，不进入Gameplay/Save身份真相；BREACH自带Loader与同步协调层，不依赖第三方Mod Manager。完整游戏内Mod Manager UI、Sandbox脚本语言/技术、Native DLL政策以及Workshop旧hash无法取得时的恢复方案仍OPEN。

DEC-049 · CANON · 来源：SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS；详见[DDD-0010](decisions/DDD-0010-host-authority-gameplay-commands.md)。
Gameplay网络采用player-hosted authoritative listen server + Gameplay Command Replication。Client发送语义意图，Authority决定transform、命中、Damage、HP、Ammo、Loot、AI、Objective与Gameplay Physics结果；Host本地玩家与远端Client走同一Command/Authority pipeline。移动等高响应系统允许Client Prediction + Server Reconciliation；Presentation可本地立即反馈但不能成为权威结果。Raw Input Replication、Client-authoritative Gameplay Result和Host-only直接写世界路径均明确未选。

DEC-050 · CANON · 来源：SRC-USER-2026-09-05-TICK-ARCHITECTURE；详见[DDD-0011](decisions/DDD-0011-tick-architecture.md)。
Authority Simulation固定60 Hz；Render、Network Replication、AI Brain与Dormant/background对象采用multi-rate架构。关键玩家/Boss约30 Hz复制为当前基线方向，AI按相关性降频并支持Dormancy/Event-driven，AI Brain约5–10 Hz且stagger/time-slice。Gameplay Physics默认跟随60 Hz Authority但不要求60 Hz发送Transform；Projectile不采用每颗弹丸高频全量Transform复制。固定步进必须bounded catch-up；60 Hz不是普通玩家可调Server选项；Mod Gameplay计时不得依赖Render FPS。Replication Architecture已由DDD-0012完成，下一正式网络Gate为Lag Compensation / Server Rewind。

DEC-051 · CANON · 来源：SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE；详见[DDD-0012](decisions/DDD-0012-replication-architecture.md)。
Host→Client正式采用Snapshot + Delta State Replication + Reliable Gameplay Events + per-client Interest Management + Dormancy。连续/latest-state-wins数据不进入可靠有序队列；离散Spawn/Despawn、Inventory/Loot transaction、Objective commit、Seat/Authority Epoch等关键事实使用可靠且幂等的事件/事务语义。Server围绕acknowledged baseline与dirty state发送Delta，丢失Delta必须可通过rebase/较新状态恢复；Relevance不只看距离，也看战斗/房间/Team/Objective关系；Dormant对象可0 Hz直到dirty/wake。Join-in-progress从当前Authority State恢复，不重放整局RPC历史；高数量Projectile不采用持续高频可靠Transform流。RPC soup、所有消息Reliable、全世界60 Hz全字段Snapshot均明确未选。

## 历史A/B/C/D账：源§37完整迁移

下表保持源文的选择与当时状态，未把网页助手再次归因当作独立证据；当前新提案不回写历史列。CONFLICT-RESOLVED/INHERITED只为来源属性。本文不提供第二份运行规则，以责任文件为准。

| 历史ID/主题 | 源选择 | 源状态及定位 | 当前唯一责任 |
|---|---|---|---|
| H37-01 Public Team Voice topology | A — Global Team Voice | CANON；SRC-SSOT-2.0 §37 第1项 | [责任规则](../gdd/coop-and-social.md) |
| H37-02 旧 Layer Transition Recovery | D — Baseline floor, not reset | Operation: LEGACY；Descent: 可作为 profile TEST；SRC-SSOT-2.0 §37 第2项 | [责任规则](../gdd/descent.md) |
| H37-03 Enemy same-faction damage | A — 默认不互伤 | CANON；SRC-SSOT-2.0 §37 第3项 | [责任规则](../gdd/combat-and-arsenal.md) |
| H37-04 Same-faction普通攻击拦截 | A — 不拦普通攻击 | CANON；SRC-SSOT-2.0 §37 第4项 | [责任规则](../gdd/combat-and-arsenal.md) |
| H37-05 Enemy blocking | C — Soft Horde + explicit Hard blockers | CANON；SRC-SSOT-2.0 §37 第5项 | [责任规则](../gdd/combat-and-arsenal.md) |
| H37-06 Basic flashlight | A — 人人基础手电 | CANON；SRC-SSOT-2.0 §37 第6项 | [责任规则](../gdd/player-and-input.md) |
| H37-07 旧 Advanced Sensor baseline | A，但后改“Scan是战斗标记”，再经Reset改为Utility | LEGACY→当前 Scan Utility；SRC-SSOT-2.0 §37 第7项 | [责任规则](../gdd/player-and-input.md) |
| H37-08 Recoil style | C — Hybrid learnable, easy-control PvE | CANON；SRC-SSOT-2.0 §37 第8项 | [责任规则](../gdd/combat-and-arsenal.md) |
| H37-09 Utility baseline concept | C — Quick Utility/Throwable | 发展为2 Utility slots，CANON；SRC-SSOT-2.0 §37 第9项 | [责任规则](../gdd/player-and-input.md) |
| H37-10 旧 Utility Recharge | C — Rechargeable Charges | Operation默认快速Recharge：LEGACY；Descent可用；SRC-SSOT-2.0 §37 第10项 | [责任规则](../gdd/economy-and-support.md) |
| H37-11 Utility shared cooldown | A — 无Global cooldown | CANON（具体Operation资源另算）；SRC-SSOT-2.0 §37 第11项 | [责任规则](../gdd/player-and-input.md) |
| H37-12 Revive Utility | B — 专门Utility/Build可Revive | CANON；SRC-SSOT-2.0 §37 第12项 | [责任规则](../gdd/survival-and-recovery.md) |
| H37-13 Revive recovery | B — 中等Health + 短Grace | CANON；SRC-SSOT-2.0 §37 第13项 | [责任规则](../gdd/survival-and-recovery.md) |
| H37-14 旧 Character Active slots | B — 2个 | LEGACY；Reset后1个 Signature Active；SRC-SSOT-2.0 §37 第14项 | [责任规则](../gdd/player-and-input.md) |
| H37-15 Separate Ultimate slot | B — 不设通用Ultimate | CANON；SRC-SSOT-2.0 §37 第15项 | [责任规则](../gdd/player-and-input.md) |
| H37-16 Duplicate Character | A — 允许 | LEGACY/SUPERSEDED；DEC-042已改为四名固定角色Seat不可重复 | [责任规则](../gdd/player-and-input.md) |
| H37-17 Mid-run Character swap | A — 不允许 | CANON；SRC-SSOT-2.0 §37 第17项 | [责任规则](../gdd/player-and-input.md) |
| H37-18 Layer1 Build guarantee | C — Hybrid guarantee | Descent CANON；SRC-SSOT-2.0 §37 第18项 | [责任规则](../gdd/descent.md) |
| H37-19 Fusion discovery | C — Hybrid：知道强互动，不知道首次结果 | CANON；SRC-SSOT-2.0 §37 第19项 | [责任规则](../gdd/build-algebra.md) |
| H37-20 Fusion determinism | A — 条件满足结果确定 | CANON；SRC-SSOT-2.0 §37 第20项 | [责任规则](../gdd/build-algebra.md) |
| H37-21 Fusion consumption model | 用户纠正：A+B消失生成C | CANON；SRC-SSOT-2.0 §37 第21项 | [责任规则](../gdd/build-algebra.md) |
| H37-22 Fusion commit | A — 自动发生，Isaac-like | CANON；SRC-SSOT-2.0 §37 第22项 | [责任规则](../gdd/build-algebra.md) |
| H37-23 Fusion inheritance | C — Compatible preserve + recipe convert | CANON；SRC-SSOT-2.0 §37 第23项 | [责任规则](../gdd/build-algebra.md) |
| H37-24 Operation/Descent双模式 | 用户提出并批准 | CANON；SRC-SSOT-2.0 §37 第24项 | [责任规则](../gdd/vision.md) |
| H37-25 Operation Earned Safety | C | CANON；SRC-SSOT-2.0 §37 第25项 | [责任规则](../gdd/world-and-information.md) |
| H37-26 Door system | C — 普通Delay，Security战略Seal | CANON；SRC-SSOT-2.0 §37 第26项 | [责任规则](../gdd/world-and-information.md) |
| H37-27 Alert decay | C曾选，但随后用户指出Alarm不适合并改DRG式Horde | LEGACY；SRC-SSOT-2.0 §37 第27项 | [责任规则](../gdd/encounters-and-difficulty.md) |
| H37-28 Operation generation | C — Curated Template + Procedural Situation | CANON；SRC-SSOT-2.0 §37 第28项 | [责任规则](../gdd/missions-and-spaces.md) |
| H37-29 Operation Wipe Recovery Anchor | 助手建议B，被用户否决 | LEGACY：无Gameplay checkpoint；SRC-SSOT-2.0 §37 第29项 | [责任规则](../gdd/survival-and-recovery.md) |
| H37-30 Support pricing | B — Meter→discrete Support Charges | CANON；SRC-SSOT-2.0 §37 第30项 | [责任规则](../gdd/economy-and-support.md) |
| H37-31 Supply ownership | Team/Public contents | CANON；SRC-SSOT-2.0 §37 第31项 | [责任规则](../gdd/economy-and-support.md) |
| H37-32 Equipment/Accessory | 删除，只留Relic | CANON；SRC-SSOT-2.0 §37 第32项 | [责任规则](../gdd/player-and-input.md) |
| H37-33 Relic slots | Isaac式无限累计 | CANON；SRC-SSOT-2.0 §37 第33项 | [责任规则](../gdd/build-algebra.md) |
| H37-34 Staff spell count | 默认3，上限6，局内扩容 | CANON profile；SRC-SSOT-2.0 §37 第34项 | [责任规则](../gdd/combat-and-arsenal.md) |
| H37-35 Descent layer length | 约12 min ×5 | CANON pacing target；SRC-SSOT-2.0 §37 第35项 | [责任规则](../gdd/descent.md) |
| H37-36 Facility Cart commit | A — 任意操作者直接Commit | CANON；SRC-SSOT-2.0 §37 第36项 | [责任规则](../gdd/world-and-information.md) |

## 被覆盖规则账：源§39完整迁移

这些旧路径不进入新的实现；历史箭头仅保存为何改变，不能从旧聊天复活。最新尚未批准的Operation提案不得假借“LEGACY”提前抹掉现行基线。

| 历史ID | 旧路径→源当前结论 | 来源状态 |
|---|---|---|
| H39-01 | **Hard Classes / mandatory Warrior-Healer-Tank-Mage composition** → Soft Archetype + 1 Signature Active。 | LEGACY；SRC-SSOT-2.0 §39 第1项 |
| H39-02 | **2 Character Active Abilities** → 1 Signature Active。 | LEGACY；SRC-SSOT-2.0 §39 第2项 |
| H39-03 | **Universal Weapon Active button** → 删除；weapon behavior使用Fire/ADS/R/hold/context。 | LEGACY；SRC-SSOT-2.0 §39 第3项 |
| H39-04 | **Scan as baseline universal ability / Scan merged with Ping** → 删除；Scan 是 Utility，Ping纯Ping。 | LEGACY；SRC-SSOT-2.0 §39 第4项 |
| H39-05 | **Equipment + Accessory + Relic** → Equipment/Accessory删除，只留Relic。 | LEGACY；SRC-SSOT-2.0 §39 第5项 |
| H39-06 | **Fixed Relic slots** → Isaac式无限累计。 | LEGACY；SRC-SSOT-2.0 §39 第6项 |
| H39-07 | **全游戏固定5 Layers** → 只有 Descent 5 Layers；Operation单Mission。 | LEGACY；SRC-SSOT-2.0 §39 第7项 |
| H39-08 | **Operation Layer baseline recovery/reset** → Operation持续资源，无阶段Reset。 | LEGACY；SRC-SSOT-2.0 §39 第8项 |
| H39-09 | **Operation所有Utility快速免费Recharge** → Operation有限/technical resource；Descent宽松。 | LEGACY；SRC-SSOT-2.0 §39 第9项 |
| H39-10 | **传统Extraction shooter/搜打撤核心** → 明确不做：无bring-in gear/stash-loss主循环。 | LEGACY；SRC-SSOT-2.0 §39 第10项 |
| H39-11 | **Persistent Facility Alarm / Alarm levels** → 删除通用系统；改 Horde/Objectives/System responses。 | LEGACY；SRC-SSOT-2.0 §39 第11项 |
| H39-12 | **Combat=被发现后的错误状态** → 删除；Operation更像mission-driven co-op PvE。 | LEGACY；SRC-SSOT-2.0 §39 第12项 |
| H39-13 | **Gameplay Recovery Anchor/Checkpoint rollback** → 删除；Operation可真实失败。 | LEGACY；SRC-SSOT-2.0 §39 第13项 |
| H39-14 | **Mandatory backtracking** → 禁止作为主线时长填充。 | LEGACY；SRC-SSOT-2.0 §39 第14项 |
| H39-15 | **Extraction hard countdown** → 删除；用世界恶化表达“现在走”。 | LEGACY；SRC-SSOT-2.0 §39 第15项 |
| H39-16 | **Retro dark sci-fi =唯一品牌** → 删除；需要独立Visual DNA。 | LEGACY；SRC-SSOT-2.0 §39 第16项 |
| H39-17 | **每个人永久自带完整Staff当无Ammo保底** → 删除；Staff占正常Weapon slot。 | LEGACY；SRC-SSOT-2.0 §39 第17项 |
| H39-18 | **Melee“几乎必然换血”作为平衡** → 删除；Skill应显著降低Health cost。 | LEGACY；SRC-SSOT-2.0 §39 第18项 |
| H39-19 | **复杂连续Power allocation/Excel** → 删除；小整数Cart。 | LEGACY；SRC-SSOT-2.0 §39 第19项 |
| H39-20 | **所有重大Team决定投票** → 普通Facility Cart由任意合法操作者直接Commit；仅极端终局动作可SharedDecision。 | LEGACY；SRC-SSOT-2.0 §39 第20项 |
| H39-21 | **Supply通过Facility Terminal订购** → 删除；Hub Support Beacon独立。 | LEGACY；SRC-SSOT-2.0 §39 第21项 |
| H39-22 | **Knowledge直接当Ammo货币** → 删除；Knowledge/Scrap贡献Support，同时Knowledge有永久研究价值。 | LEGACY；SRC-SSOT-2.0 §39 第22项 |
| H39-23 | **Fusion是可逆A+B active state** → 删除；Fusion是真正consume→C。 | LEGACY；SRC-SSOT-2.0 §39 第23项 |
| H39-24 | **Fusion需要Forge/手动确认** → 删除；满足合法Recipe后自动。 | LEGACY；SRC-SSOT-2.0 §39 第24项 |
| H39-25 | **公开Scenario Editor先做** → 延后；先内部工具。 | LEGACY；SRC-SSOT-2.0 §39 第25项 |

## 按返工风险排列的OPEN

DEC-007 · OPEN · 来源：SRC-SSOT-2.0 §41；本轮评审。
以下不是让用户一次回答所有问题的问卷；先完成不依赖答案的greybox，到了相关Gate再要求具体决定。

| 事项 | 责任/证据需要 | 最迟关卡 |
|---|---|---|
| 首发核心/Operation时长/成长形式/槽位 | [模式](../gdd/operations.md)、A/B体验 | Week12前形成候选、Day180定范围 |
| 中央其余因果与唯一终局代价（NAR-010已锁内容除外） | [中央故事](../gdd/central-story-spine.md) | 大规模任务/资产制作前 |
| NAR-011客观历史、威胁分类、守门人子网、壁垒/太阳系与DLC | [世界观](../gdd/narrative-bible.md) | 故事总览及正式叙事资产前 |
| 中文正式名称的法律清查、母语歧义与配音可读性 | [命名规范](../gdd/world-naming.md) | 对外公布或录音前 |
| 枪械-only条件是否正式确认 | [产品方向](../gdd/vision.md) | 删除Staff/Arcane或锁首发战斗范围前 |
| 三枪族资源/特征/穿透/友伤/补给与Energy Block三子型 | [战斗](../gdd/combat-and-arsenal.md) | 武器正式资产前 |
| 取消/缓冲/蓄力/移动技巧公平性与mandatory tech | [掌握成长](../gdd/progression-and-bastion.md) | 动画与网络窗口冻结前 |
| 玩家公开称呼、Staff/Active/Fusion世界解释 | [世界观](../gdd/narrative-bible.md) | Phase0 |
| Stylized Industrial Realism是否升格最终CANON Visual DNA / renderer表现细则 | [美术](../gdd/art-direction.md) | 正式asset前 |
| Demo时长/模板/进度/TC范围 | [发行](../production/platform-and-release.md) | 公布Demo前 |
| 裸武器换枪、四近战、初始Spell、热/资源、Active、Controller | [原型卡](../content/combat-prototypes.md) | Day30/Week8 |
| 30Relic/6–10Fusion、继承、循环、可读性、Spell互作 | [Build](../gdd/build-algebra.md) | Lab验证后再扩大 |
| Support价值、本地覆盖、Ammo vs成长、Cart meta、Horde、安全、失败比例 | [BLACKSTART](../content/blackstart.md) | Week12/Day180 |
| Descent奖励、层时长、Boss、L3转化/L5质变、供给密度 | [Descent](../gdd/descent.md) | 仅批准该模式后 |
| Networking Provider / Transport组合（Steamworks、EOS、FishNet/Unity Netcode等） | [网络](../technical/network-and-persistence.md)、4人公网/relay/NAT/延迟实测 | Replication合同后、网络技术Spike前 |
| Host Migration具体协议：选主、snapshot cadence、Authority Epoch、恢复时限 | [网络](../technical/network-and-persistence.md)、Host loss压力测试 | Snapshot/Replication模型锁定后 |
| Lag Compensation / Server Rewind：history window、Hitscan/Projectile、异常高延迟与公平边界 | [DDD-0010](decisions/DDD-0010-host-authority-gameplay-commands.md)、[DDD-0012](decisions/DDD-0012-replication-architecture.md)、[网络](../technical/network-and-persistence.md) | 当前下一设计Gate |
| 完整游戏内Mod Manager UI：浏览、排序、冲突、Profile/Modpack体验 | [Modding](../technical/modding-and-toolchain.md) | Public Mod UX冻结前 |
| Mod脚本层：Graph→Sandbox Script的语言、Sandbox技术、Native DLL政策 | [DDD-0009](decisions/DDD-0009-agent-first-modding-runtime.md)、安全Spike | SDK/API冻结前 |
| Workshop旧版本/exact hash不可取得：缓存、安全直传、官方CAS或拒绝Join | [DDD-0009](decisions/DDD-0009-agent-first-modding-runtime.md)、[网络](../technical/network-and-persistence.md) | Suspended Run与Modded Join实现前 |
| Asset采购、provenance、许可证登记与可再分发边界 | [资产/发行](../production/platform-and-release.md)、待建ASSET-POLICY/license registry | 批量购买第三方资产前 |
| 真实规模、public Forge、dedicated扩展 | [架构](../technical/architecture-and-performance.md) | 技术spike后 |
| Carry四格、Shop/个人offer、Run货币、Respec、Transit | [经济](../gdd/economy-and-support.md)、[世界](../gdd/world-and-information.md) | 不默认进入当前模板 |
| Public grief/长局离队/Bots/单人 | [合作](../gdd/coop-and-social.md) | 公共匹配公布前 |
| 已删除对话/旧技能精确数值/完整旧Narrative | [证据](../sources/evidence-register.md) | UNRECOVERED，找到原件再审 |

## 附录B变更历史与后续纪律

DEC-008 · DIRECTION · 来源：SRC-SSOT-2.0 Appendix B。
v2.0将Project Archaeology改为全项目统计，扩学习库，补音频/语音/社交/网络/模组/商业/agent/QA，加入决策账与未确认叙事，模式化重审旧Difficulty/Shop/Carry等；合并Operation无Alarm/无checkpoint/前向路线/公共Support和新输入/Staff/Descent/数值，集中旧规则防复活。完整字句只保留[原快照](../sources/ssot-v2.0-original.md)。

本轮逐项讨论记录在[讨论日志](discussion-log-2026-09-04.md)。任何新增重大决定按[作者规则](authoring-guide.md)写SUPERSEDES、影响、证据和状态；不以继续写文档代替试玩或用户确认。