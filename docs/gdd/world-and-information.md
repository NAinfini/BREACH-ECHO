---
doc_id: GDD-WORLD
doc_type: gdd
stage: DRAFT
updated: 2026-09-05
owner_role: 系统关卡设计
canon_basis: "SRC-SSOT-2.0 §4A.3、§4A.6、§4A.13–§4A.14、§14、§33.5、§34；本轮守门人交易候选"
depends_on: ["missions-and-spaces.md", "narrative-bible.md"]
---

# 设施、信息、Door、Cart 与 Earned Safety

## 玩家目的

先发现事实，再对设施做可观察的改变；做过的投入必须持续有效，玩家由此创造可呼吸的前线。

## 范围与术语

Terminal是设施自己的查询/控制节点；KnowledgeState是玩法确认的信息；Cart是小整数设施投资；SecurityDoor是战略基础设施，普通Door提供延迟。Supply属于[支援](economy-and-support.md)，图结构属于[任务空间](missions-and-spaces.md)。

## 已确认规则

WRD-001 · CANON · 来源：SRC-SSOT-2.0 §4A.3、§14.3、§34.2。

HUD总有清楚Primary Objective，未知物资/位置通常不免费全图显示。Terminal可Search/Query、查门/电力/通风/交通/本地网络/任务，再PING/TRACK已定位目标成团队waypoint；不要求记ID。Terminal不是Hub，不订Supply，不清全局Alarm。知识由合法观察、sense、terminal或system event生成；TPS/照片/画面技巧不获得额外知识。

WRD-002 · CANON · 来源：SRC-SSOT-2.0 §4A.6、§4A.14、§14.1、§14.4。

无固定Safe Room；清威胁、关门、Seal ingress、破坏Nest、接管Turret和控制威胁源可获得相对安全。普通Door免费开关、延迟/隔视线/部分声音，有Stable/Damaged/Breaching表现无传统HP条；敌人可砸/Hack/绕路。Security/Containment需投入Power/Terminal/Cart才长期Seal，只明确Breach能力、任务或Power failure能破坏。Director不得凭空刷怪绕过投资。Foam/Weld/Barrier/Ice/Breaker可按能力作用Door。

WRD-003 · CANON · 来源：SRC-SSOT-2.0 §4A.13、§37。

重大配置用小整数预算+Cart多选；同屏通常4–6项、成本主要1/2、极少3，每项一句话解释后果。任何合法操作者可直接Commit，不做多数票；极端不可逆终局动作可例外SharedDecision。提交后不免费反悔，重配需新的合法世界行动/Cell/下游节点。

WRD-004 · DIRECTION · 来源：SRC-SSOT-2.0 §14.2、§33.5。

设施候选系统包括Power、Ventilation/Fog、Security、Turrets、Transit、Fabricator/Storage、Containment、Network/Uplink、Cargo condition、Fold/Resonance。有限Transit需发现/激活节点与link，受电力/阵营/世界状态影响，高威胁/战斗不可用；不提供任意房间传送。

## 玩家流程

WRD-005 · PROPOSED · 来源：本轮系统扩写。

看见目标但未知位置→到Terminal查合法本地记录→结果自动分享→沿前向路线取Cell→Cart预览世界后果→操作者Commit→新灯光/通风/封门/炮台响应→队伍利用变化推进。Terminal让信息有地点和风险，不让另三人长期等菜单。

## 状态与数据所有权

WRD-006 · PROPOSED · 来源：本轮系统扩写。

Authority持有FacilityStateRevision、PowerLedger、DoorState、IngressGraph、ControlPermissions、TeamKnowledge；Terminal只是当前节点的视图与命令入口。Cart把预算扣减、设施改变、mission consequence和日志一起原子提交。

| 当前 | 条件 | 结果 |
|---|---|---|
| Unknown | 合法Query/观察 | Known，记录证据渠道与时间 |
| CartPreview | budget与revision仍有效 | Commit选项→扣Cell→世界变化 |
| CartPreview | 他人先改设施/耗Cell | StalePreview，重算并解释，不扣费 |
| OrdinaryDoorStable | 敌人明确破坏动作 | Damaged→Breaching→Open/Broken |
| SecuritySealed | 有合法Breach/Power failure | 可读失效过程，否则保持Seal |
| ThreatenedArea | 活威胁清除且Ingress受控 | RelativeSafety，由事实计算 |

## 并发 Cart 与安全承诺

WRD-007 · PROPOSED · 来源：本轮系统扩写。

同节点多个玩家可看Cart；命令带observedRevision与option set，权威串行验证。首个成功者扣预算；第二个收到“配置已由某人改变”与新成本，必须重新预览再提交。无需投票，也不能用陈旧预算超买。

候选社交保护：选择时全队出现简短预览广播；按住确认关键提交，说明谁将改什么，不锁权给Host。这降低误触，无法根治恶意；公共匹配风险归[风险登记](../production/brutal-review.md)。若实测仍可轻易毁局，需要用户批准改变权限，不把UI日志当完整解决方案。

安全由可达威胁路径与其能力推导。封口后不因“节奏需要”生成免疫封门的单位。新威胁必须已由任务/世界来源允许且可感知；关闭一处入口不自动平移等量敌人到玩家背后。

## 模式配置与内容接口

WRD-008 · PROPOSED · 来源：本轮系统扩写。

Operation调用完整设施配置；Descent可复用门/材质/世界反应，不自动带入Terminal与Cart流程。设施系统卡声明可查询信息、控制范围、权限、Power dependency、故障输入、可达port、UI短句与结果表现。关卡不得依赖“查到一次后记住秘密ID”。

## 边界

WRD-009 · PROPOSED · 来源：本轮系统扩写。

操作者死亡/离线取消未提交Cart，已提交世界状态保留。关键电源丢失时展示实际失效系统，不回滚已花资源。封门不能切断唯一必需目标可达路径；设计允许自毁路线时须有提前可读替代/失败条件并经验证。已知目标移动时更新“最后确认位置”，不提供无授权追踪雷达。Host迁移保持Knowledge来源、门状态与剩余物资。

## 参数

| 参数 | 值/状态 | 来源 |
|---|---|---|
| Cart展示项数与成本 | 通常4–6项；1/2/极少3 · CANON | SRC-SSOT-2.0 §4A.13 |
| BLACKSTART电池与选项 | 只在[实例](../content/blackstart.md)拥有数值 | SRC-SSOT-2.0 §16.3 |
| 安全确认延迟/门耐受/Query耗时 | OPEN | 原文未给定 |
| 常规Query用时 | 中位≤15秒 · TEST | SRC-CHATGPT-REVIEW-1.0 §6；候选阈值 |

## 示例

WRD-010 · PROPOSED · 来源：本轮系统扩写。

正常：队伍选择Ventilation，finale低处视野恢复，之前有毒区变成合法移动路径。失败：另一人先花Cell，后提交者不被允许用旧预算开Vault。跨系统：Spear玩家在普通Door将被砸开前拉开距离；SecuritySeal仍阻隔无Breach能力的Horde，没有“玩家太安全所以门突然坏了”。

## 验证与 OPEN

WRD-011 · TEST · 来源：本轮实验建议。

枚举所有Cart合法组合检查预算和可达性；对比有无Seal、关门前后AI路线；多人同时操作、断线、Power failure都只提交一次。记录队友等待、后果理解与实际策略变化。设施系统完整列表是方向，不意味着每个模板都实现全部系统。
## Team Ordnance 与设施互作

WRD-012 · PROPOSED · 来源：SRC-USER-2026-09-04-ORDNANCE-MISSIONS。
结构卡声明可接受的Structure/Armor/Heat/Sonic等能力、需消耗量、破坏输出及替代前向路线。Security战略Seal与任务关键门不能仅因“Heavy”标签被全体通杀。Terminal可合法查团队重资产位置/状态，未知资产不自动全图显示；发现后按共享Ping呈现。重资产失联不删除，世界持久由[战斗合同](combat-and-arsenal.md)与存档共同承担。

## 壁垒—守门人结构化联系

WRD-013 · PROPOSED · 来源：SRC-USER-2026-09-04-BASTION-JANUS-CONTACT；SRC-USER-2026-09-04-BASTION-JANUS-TRANSACTION；SRC-USER-2026-09-04-BASTION-ORIGIN-JANUS-TRADE；SRC-USER-2026-09-05-BASTION-MULTIROUTE-REAR-HUB；SRC-USER-2026-09-05-EMERGENCY-FOLD-LOCAL-COMMIT；SRC-USER-2026-09-05-FINAL-SEQUENCE-AUTHORITY-CORRECTION；SRC-USER-2026-09-05-BASTION-ENERGY-CLOSURE-APPROVAL；SRC-USER-2026-09-05-BASTION-ARTIFICIAL-SUN-DEADLINE；SRC-USER-2026-09-05-BASTION-NETWORK-SPACE；SRC-USER-2026-09-05-NATIVE-MANAGEMENT-HUMAN-DATA-LAYER；SRC-CODEX-2026-09-05-OBJECTIVE-HISTORY-CURRENT-CANDIDATE。

壁垒位于筑路者技术生成的有限人工节点空间，不存在可供常规航行、开采或扩张的外部宇宙。无线电、有线与激光只在同一节点空间内部有效，不能跨越关闭的界桥路线。闭合域保留少数筑路者预设的传能接口和封闭设施空间：前者不是交通门，后者的有限体积已经属于壁垒边界；它们不能通往正常宇宙，也不能中继外部战区的人类数据，因此既不是逃生口，也不能绕过历史断层。

守门人必须按两层处理：筑路者原生层维持节点空间、路线和基础能量，人类只会调用部分操作；人类上层负责身份、档案、消息、远程控制和本地技术托管。壁垒可以维护本地人类上层并从托管库取得制造图、校准、固件和许可，却不能因此访问外部数据或理解筑路者底层。该结构不是与AI自由聊天的商店，也不证明外部人类在线。

交易API可处理合同状态、材料规格、安装/兼容信息与安全约束。对Archive、History、Global topology、Command等自由提问返回`AUTHORITY_INSUFFICIENT`；该状态只表示当前会话/主体无权限，不证明守门人持有答案。系统还必须区分`DATA_UNAVAILABLE`、`NETWORK_ISOLATED`、`OUT_OF_CONTRACT`与`INTEGRITY_UNKNOWN`，不能统一显示“权限不足”，更不能借错误状态暗示守门人掌握当前地球情报。

壁垒今天仍能建立本地合同会话，不表示历史上的最高权限迁移也能在同一链路完成。前者只需要壁垒闭合域内的本地守门人实例；后者按NAR-017需要壁垒作为接收方在线并返回确认，而迁移尝试时壁垒外部会话已经失效。无限探索派当时仍存在并参与共同授权，不能再把迁移失败归因于它无法确认。合同权限与最高管理权限必须保持不同作用域，不能因为系统会交换维护技术，就推断它也能把全网控制权交给壁垒。

当代闭合域能源不足与合同仍在线已经由NAR-020锁定，NAR-021进一步确认壁垒原本是依赖多路输入、而非按长期自给设计的中枢；有限人工空间没有自然资源和新增疆域。NAR-025把危机主体锁定为人类建造的人造太阳：聚变燃料和补充冷却介质将在数月内耗尽，电磁约束与控制部件也接近强制停机阈值。守门人可以交付维修蓝图、校准与许可，却不能凭空制造燃料、冷却介质、备件或完整工业设备。停止购买非必要技术和继续配给只能延迟，不能完成替换，因此合同必须明确目标旧维护节点、现有余量与再次隔离条件。精确月份和路线仍为OPEN，不能用无名万能材料跳过可验证因果。

| 合同阶段 | 输入 | 合法结果 |
|---|---|---|
| ContactUnavailable | 尝试建立联系 | 返回可解释原因，不伪造在线守门人 |
| ContactEstablished | 提交材料/劳务能力声明 | 返回规格接受、缺口或合同外，不直接生成技术 |
| ContractOffered | 验证材料、兼容与白名单 | 接受后记录义务、交付和安装条件 |
| FulfilmentPending | 现场劳务/材料尚未完成 | 保持待履约，不预发完整战斗能力 |
| Fulfilled | 双方义务均满足 | 交付已批准技术/能力并记录来源版本 |
| QuerySubmitted | 请求Archive/History/Topology/Command | 按权限、数据、隔离、合同与完整性分别返回状态 |

为何及由谁授予联系权限、一次联系的实际成本、守门人位置、技术来自旧档案还是新研发、白名单审批主体和断线后的合同恢复均OPEN。

WRD-014 · TEST · 来源：本轮守门人交易验收建议。

验证同一合同重试不重复扣料或发技术；五种拒绝/未知状态能被玩家区分；安装不兼容不会吞物资；断线和Host迁移保持合同阶段。测试观察玩家是否误以为这是通用问答AI、是否把`AUTHORITY_INSUFFICIENT`理解成守门人“知道但不说”，以及技术是否形成无代价纵向战力跳跃。

## 旧制身份与设施权限

WRD-015 · CANON · 来源：SRC-USER-2026-09-05-LEGACY-ID-LOW-CLEARANCE；事实边界见[世界观NAR-028](narrative-bible.md)。

壁垒外勤凭证继承断网前的人类身份格式，因此旧设施通常不会把小队当成完全未知的外星入侵者。但设施无法从已经分裂的人类身份目录验证最新授权链：同一个人在不同节点可能被解析为不同旧记录、过期岗位或只有基础访问权的主体。默认结果是“身份格式有效，当前授权无法证明”，而不是全权通过或彻底拒绝。

这项规则解释Operation为什么必须派人进入设施。壁垒可以让小队通过最外层身份识别并使用少数低权限接口，却不能在出发前远程取得整座设施控制权。更高权限必须依靠该设施内部仍可验证的记录、设备和现场行为逐步恢复；具体升级方式由任务规格拥有。自动机器只执行本节点能够验证的权限状态，因此可以允许小队通过公共区域、拒绝受限操作，并在小队强闯高权限区域时转为敌对。

权限反馈必须区分“旧身份存在但权限低”“当前目录没有该身份”“身份完整性损坏”“数据域不可达”和“设施拒绝本次操作”。不得把所有情况压成同一句`权限不足`，否则玩家无法判断应寻找凭证、恢复节点、改走路线还是准备战斗。

## 载波、协议恢复与节点入网

WRD-016 · CANON · 来源：SRC-USER-2026-09-05-CARRIER-REBOOT-PHYSICAL-RECOVERY；SRC-USER-2026-09-05-DOCTRINE-RECOVERY-ASYMMETRY；SRC-USER-2026-09-05-LIMITED-NODE-DEFENSE-ASSETS；世界事实见[世界观NAR-016、NAR-026与NAR-029](narrative-bible.md)。

人类数据层使用节点产生的共振载波。原生安全重启改变载波特征和路由状态后，人类设备可以检测到信号，却无法用旧配置解码消息、地址或权限。常规通信距离内的节点可直接交换载波样本与恢复软件；没有此类链路的节点必须由小队携带协议恢复盘进入现场。恢复流程固定为：确认目标字形路由证据→开启合法交通路线→抵达节点→读取当前载波→生成并写入本地译码配置→校验身份与地址→提交节点入域。

恢复盘只提供受信根、恢复工具和可携带状态，不预装所有节点的最终配置。写入成功也只接管仍属于该节点、结构完整且未被其他阵营改写的资产。限界探索区的炮塔、机器人、备用电源和封闭资源库在节点入域前可能保持锁定、中立或敌对；入域后按当前权限转为友军设施。必须通过灯光、识别色以外的形状/声音、炮口姿态、终端状态和友军目标选择清楚表现转换，不能只改UI阵营标签。

WRD-017 · DIRECTION · 来源：SRC-USER-2026-09-05-OPTIONAL-GLYPH-REROUTES。

部分节点允许玩家把当前字形路由序列改为已存在的备用地址，进入隐藏仓库、检修空间或被遗忘的支路。它不生成新空间，也不允许任意输入通往任意节点。有效序列必须由日志、环境符号、扫描或其他合法证据取得；错误序列通常不给答案，主线和可访问性内容不得要求盲猜或穷举。

改线前必须预告至少一项代价：占用路线、消耗电力或任务时间、暂时失去退路、提高节点暴露，或接通额外合法敌人来源。隐藏区域可提供额外物资、废料、外观信用点、成就条件、外观物品、字形知识或筑路者资料；不得放置主线唯一必需能力，也不得让奖励无风险获得。进入后必须存在可理解的返回或重新设路方式。
