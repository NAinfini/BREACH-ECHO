---
doc_id: GOV-DISCUSSION-20260904
doc_type: discussion
stage: DRAFT
updated: 2026-09-05
owner_role: 设计记录维护
canon_basis: "本轮Codex用户消息与SRC-CHATGPT-REVIEW-1.0"
depends_on: ["decisions-and-questions.md"]
---

# 2026-09-04 讨论记录

这是本轮可恢复讨论的语义摘要，不冒充逐字聊天导出。用户意图与助手推荐分列；网页助手评审只是NON-CANON证据。具体规则在责任GDD，小DDD保存为什么这样选。

| 顺序/话题 | 用户表达摘要 | 评审结论/状态 | 追溯 |
|---|---|---|---|
| 01 文档制作 | 拆SSOT、补细节、访问原网页、搜方法、严厉评审 | 已授权文档工作；不改Downloads原件 | [证据](../sources/evidence-register.md) |
| 02 双模式冲突 | 想GTFO资源管理又想Roguelike，担心双倍资源 | 单纯全禁/全放都需对照；PROPOSED Operation先行 | [DDD-0001](decisions/DDD-0001-operation-vs-roguelike.md) |
| 03 偏好收敛 | 进一步偏好高紧张GTFO-like合作 | DIRECTION明确；Operation-only未最终确认 | [DDD-0001](decisions/DDD-0001-operation-vs-roguelike.md) |
| 04 解谜本体候选 | 先无Roguelike解谜，以后模块增加 | OPEN；建议系统战术问题而非固定谜底 | [DDD-0001](decisions/DDD-0001-operation-vs-roguelike.md) |
| 05 接口与重写 | 不预留Roguelike接口怕未来重写 | 通用Ruleset/Effect/Resource等真实接缝；10min Lab验第二消费者 | [DDD-0002](decisions/DDD-0002-modular-product-architecture.md) |
| 06 全游戏模块化 | 接受不留专用接口，仍希望整块换/复用简单 | DIRECTION；替换性分层、公开API slice后冻结为提案 | [DDD-0002](decisions/DDD-0002-modular-product-architecture.md) |
| 07 最终类型询问 | 要明确选GTFO-like还是Roguelike | 强烈推荐Operation-first，尚未变Canon | [DDD-0001](decisions/DDD-0001-operation-vs-roguelike.md) |
| 08 固定loadout | 两枪与工具进场，不频繁选换枪，要下挂/稳枪/增伤 | DIRECTION；次数/槽位冲突OPEN，优先tradeoff | [DDD-0003](decisions/DDD-0003-operation-field-modification.md) |
| 09 统一底层 | 配件底层当Relic方便rework | 统一ModificationDefinition，不统一玩家概念/平衡 | [DDD-0004](decisions/DDD-0004-unified-modification-model.md) |
| 10 Team Ordnance | 手持超强、切枪放下、固定资源、普通补给不补 | DIRECTION；多人持久与安全规则PROPOSED | [DDD-0005](decisions/DDD-0005-team-ordnance.md) |
| 11 Predator Reversal | 先躲/控，前向取得能力后反转 | DIRECTION；不做取枪长回跑 | [DDD-0006](decisions/DDD-0006-predator-and-breach-missions.md) |
| 12 Breach/ToolHunt/Rejoin | 找重工具破障与前向汇合 | DIRECTION；耗尽仍有慢险路线，防软锁 | [DDD-0006](decisions/DDD-0006-predator-and-breach-missions.md) |
| 13 公共匹配/范围 | 要全部列出不好玩与市场风险 | E3风险矩阵，不假装已经发生/解决 | [风险总览](../production/brutal-review.md) |
| 14 小文件防丢 | 本轮所有讨论落命名清楚文件 | 已授权新增DDD与讨论log | [决策总览](decisions-and-questions.md) |
| 15 中文命名 | 面向用户统一使用“总览” | LOG-NAME · CANON · 来源：SRC-USER-2026-09-04-NAMING | 本库导航与报告 |
| 16 唯一中央故事 | 中央故事曲线绝对唯一 | STORY-001用户CANON；五幕细节仍PROPOSED | [DDD-0007](decisions/DDD-0007-single-canonical-story.md) |
| 17 First Builder初始用途 | 相关门户/Resonance基础设施用于快速旅行与能源采集 | CANON只锁初始工程用途；机制、Breach起因、预见性与责任OPEN | [世界观NAR-010](../gdd/narrative-bible.md) |
| 18 Prototype技术谱系 | 一部分试验型武器基于First Builder技术制造 | CANON只锁“部分”；具体武器及原件/仿制/逆向/量产关系OPEN | [世界观NAR-010](../gdd/narrative-bible.md) |
| 19 外星起源与物种解释 | 提出First Builders经Bridge抵达地球，以及Voidborn、Demon、寄生物种的宇宙来源 | 用户明确只是想法且不确定合理性；整组PROPOSED，不把物种自动写成Faction | [世界观NAR-011](../gdd/narrative-bible.md) |
| 20 Machines隐藏目标 | 提出人类制造Machines，其真实目标是关闭Bridge；Bastion知道外部威胁与战争的可能，但不知完整命令和因果 | PROPOSED；与JANUS、Secession及具体执行因果仍OPEN | [世界观NAR-011](../gdd/narrative-bible.md) |
| 21 Bridge扩张与封网循环 | 以40K人类黄金时代作灵感类比，提出人类与First Builders可能重复“扩张→接触高侵略威胁→封网”；Builder强在空间网络而非武器 | 仅灵感与PROPOSED结构；原始威胁是Voidborn还是Demon、是一段还是两段黄金时代均OPEN | [世界观NAR-011](../gdd/narrative-bible.md) |
| 22 First Builder断网衰亡 | 提出外敌定位后隐匿/封Bridge；供能与跨世界物流中断使区域分别缺资源和工程能力，文明缓慢灭绝 | PROPOSED；正式正文不用外部作品术语，保留残存遗迹/节点以兼容人类逆向；执行者、破坏范围、绝灭程度、冗余与Folding关系OPEN | [世界观NAR-011](../gdd/narrative-bible.md) |
| 23 JANUS与人类内战 | 提出JANUS发现外部威胁并告知人类；探索派与隔离派内战，隔离派授权切外部/留内部，授权者最终死亡后JANUS延续命令 | PROPOSED；授权者死于内战还是Voidborn仍OPEN，其他授权、责任与网络因果也未锁 | [世界观NAR-011](../gdd/narrative-bible.md) |
| 24 JANUS缩网代价 | 探索派接触Voidborn侵染前沿并被消灭；趋能行为和节点自动响应形成沿网扩散，JANUS逐段切网且同步失去该区访问/控制；内层无密钥且早已断讯 | PROPOSED；JANUS不能自行授予最高权限，不新增玩家揭示顺序 | [世界观NAR-011](../gdd/narrative-bible.md) |
| 25 Bastion不完整认知 | Bastion知道外部可能有威胁且正在/曾在战争；不知道其中有人类内战、威胁身份/性质（含Voidborn）及JANUS命令完整来源；内部两种政策立场都要为资源探索 | PROPOSED；谨慎派限界恢复，发展派以维持/发展为由研究技术，不神话化为“挖真相”，不自动新增Faction | [世界观NAR-011](../gdd/narrative-bible.md) |
| 26 当前时代触发 | JANUS退至最后防线；Voidborn生理/场效应触发物理节点尚存的Bridge残网自动响应，宏观侵染前沿逼近Bastion附近 | PROPOSED；被彻底物理摧毁的Anchor不可绕过，JANUS位置与玩家任务仍OPEN | [世界观NAR-011](../gdd/narrative-bible.md) |
| 27 Anchor永久代价 | 用户只提出物理摧毁必须构成硬边界；助手建议永久阻断同时永久失去能源/交通 | 助手PROPOSED合理化，不是用户决定，是否采用OPEN | [证据登记](../sources/evidence-register.md) |
| 28 聊天知识落盘 | 当前可见的重要决定、设想、纠正、否决及OPEN须在本轮结束/可能压缩前保存为精简语义摘要，保留来源与状态 | GOV-006 · CANON；不承诺恢复未访问、未看见或已删除历史 | [作者指南](authoring-guide.md) |
| 29 故事总览与盲审 | 故事全部排完后才给完整总览，用户审阅后再让无故事上下文的全新只读agent严苛审查并原样交付批评 | GOV-007/STORY-006 · CANON；当前不触发、不建占位 | [作者指南](authoring-guide.md) |
| 30 三层世界命名 | 人类口语外名/机构科学名/原生自称；无证据则UNKNOWN，低智能Voidborn无自称，并列多组候选 | 全部PROPOSED，无最终选择；碰撞初筛不是法律清查 | [命名候选](../gdd/world-naming.md) |
| 31 外部威胁分类 | 外部危险不只Voidborn；Demon为高温种外名；寄生谱系使用其灭绝宿主尸体延续 | PROPOSED；智能、敌意、机制和宿主记忆OPEN，不自动叫Faction | [世界观NAR-011](../gdd/narrative-bible.md) |
| 32 Voidborn低智能 | 个体/局部智能近乎无、无蜂巢/群体心智，追随能量梯度并触发节点自动响应 | PROPOSED；客观写侵染/饱和，不写发现Bridge或战略推进 | [世界观NAR-011](../gdd/narrative-bible.md) |
| 33 JANUS覆盖子网 | JANUS仅管人类认证闭合子图；后撤是撤实例、凭证、传感器和资产并隔离外围 | PROPOSED；无First Builder全网根权限，授权与位置OPEN | [世界观NAR-011](../gdd/narrative-bible.md) |
| 34 Bastion与Sol | Bastion建于First Builder枢纽，断网后与Earth/Mars失联；太阳系其他人类仍存在并独立发展 | PROPOSED；Bastion不是全人类最后城市，所知与作者真相分层 | [世界观NAR-011](../gdd/narrative-bible.md) |
| 35 Bastion—JANUS交易 | 付代价建立结构化合同，以物资/冷却/计算等换白名单内维护、防御与生存技术 | PROPOSED；不是对话商店或废料换神器，拒绝状态必须区分 | [世界设施WRD-013](../gdd/world-and-information.md) |
| 36 Sol重联DLC | 基础本地弧完成后才可能受控重联Earth/Mars并联合外推 | PROPOSED且不承诺；不能补卖基础结局，Earth武器为有代价sidegrade | [世界观NAR-011](../gdd/narrative-bible.md) |
| 37 枪械-only条件 | 倾向GTFO-like非Roguelike首发；正式确认后才删Staff/Arcane，保留Melee | 高影响DIRECTION，前提未锁；当前Staff 3/6不删、不建双轨 | [产品VIS-008](../gdd/vision.md) |
| 38 Bridge无限枪取消 | 取消从空间网道汲能的低伤无限弹药枪 | 用户明确否决；LEGACY，只留历史，不回active候选 | [决策DEC-013](decisions-and-questions.md) |
| 39 三类枪械 | 传统动能、电磁、有限Energy Block；电磁非静音且须测过穿/材料/残能 | DIRECTION；资源、特征、友伤和补给无锁定数值 | [战斗CMB-012](../gdd/combat-and-arsenal.md) |
| 40 Energy Block三子型 | 单发高伤、连发低伤、强制蓄力是三把独立武器 | PROPOSED；蓄力阈值/消耗/Heat/中断/范围风险OPEN | [战斗CMB-013](../gdd/combat-and-arsenal.md) |
| 41 响应性操作窗口 | 真正装填完成后可取消收尾，切枪/ADS/Fire可预输入，蓄力可衔接下一轮 | PROPOSED/TEST；状态反馈一致，不破射速/资源/网络权威 | [战斗CMB-014](../gdd/combat-and-arsenal.md) |
| 42 移动技巧 | bunny hopping等只试测可学习收益 | TEST候选；不得成为动作税或摧毁潜行、噪声、队形、关卡 | [玩家PLY-013](../gdd/player-and-input.md) |
| 43 玩家掌握成长 | 玩得越久应因知识/技巧表现更强，而非局外数值碾压 | DIRECTION；技巧可教学/观察/复现，不依赖Bug、宏、超高FPS或外部攻略 | [进度PRG-009](../gdd/progression-and-bastion.md) |
| 44 英文生造词组否决 | Farweft、Nearmakers、NARROWGATE、Farcross、Linegraze、Incands、Claimants、Return Current、Common Vector过度追求搜索唯一性且读写生硬 | 用户明确REJECTED；只留历史，不能恢复为正式名 | [命名NAM-006](../gdd/world-naming.md) |
| 45 中文正式命名 | 确认界桥网络/界桥、筑路者、守门人系统/守门人、壁垒、虚空兽/网道趋能生物群、灼星种/恶魔、借尸者、太阳回声、重光行动 | CANON/SELECTED；旧英文仅作规定别名；全部LEGAL NOT CLEARED，不改变NAR-011与DLC状态 | [命名NAM-002–NAM-003](../gdd/world-naming.md) |
| 46 正史先于玩家剧情 | 先决定作者层真实历史，再决定玩家实际经历、揭密顺序与逐幕任务 | 工作顺序CANON；客观历史收束稿仍PROPOSED，不能偷偷升格 | [世界观NAR-011](../gdd/narrative-bible.md) |
| 47 客观历史v0.1 | 用共振硬规则、筑路者断网、初次破界、机器离网、大分裂、死城、折叠封网和壁垒主动重启构成单一因果链 | PROPOSED；苍白增生归入虚空兽生态，灼星种/借尸者/DLC不进入核心灾难；待用户批准 | [世界观NAR-011](../gdd/narrative-bible.md) |
| 48 两种探索路线纠正 | 两派不是探索与不探索，而是无限、无预设边界的持续探索，对必要、受控、可隔离且可撤回的探索 | NAR-013 · CANON；双方都探索，v0.1阵营定义错误 | [世界观NAR-013](../gdd/narrative-bible.md) |
| 49 内战解释历史断层 | 用户确认大分裂是后世历史断层的主要原因；壁垒在断联前知道两派公开主张，断联后只保留无法识别交战方的警告与片段战况 | 核心因果与认知边界为NAR-013 · CANON；跨区通信、档案信任与根权限继承怎样被破坏仍为NAR-011 · PROPOSED | [世界观NAR-013与NAR-011](../gdd/narrative-bible.md) |
| 50 内战先于外敌 | 人类内战在外敌被确认或进入人类网络以前已爆发；若当时已有共同外敌，人类不会因此继续开战 | NAR-013 · CANON；SUPERSEDES旧恢复顺序及v0.1 | [世界观NAR-013](../gdd/narrative-bible.md) |
| 51 无限探索派速败 | 该派把主防御部署在人类战争边界，外拓链路不设对外纵深防御，首次接触虚空兽后从无防线一侧快速溃败 | NAR-013 · CANON；不把速败解释成虚空兽战略智能 | [世界观NAR-013](../gdd/narrative-bible.md) |
| 52 守门人不能转授权限 | 曾提议根权限天生不可转让、壁垒无席位且守门人从设计上永远不能完成移交 | LEGACY/SUPERSEDED；用户恢复原讨论结论：不是不能转，而是没有时间完成；由NAR-017覆盖 | [世界观NAR-017](../gdd/narrative-bible.md) |
| 53 接敌后停战 | 无限探索派发现怪物后立即向限界探索派求和，双方停战并尝试联合补救，但外拓链已被突破 | LEGACY/SUPERSEDED；已由条目69的双重证据门槛补全并升为NAR-019 · CANON | [世界观NAR-019](../gdd/narrative-bible.md) |
| 54 三方最终失联 | 无限探索派、限界探索派与壁垒最终失去可用于及时对话、指挥、档案同步和授权的远程双向联系 | NAR-013 · CANON；不否定NAR-014允许本地通信或迟到信号，具体分阶段断联机制仍PROPOSED | [世界观NAR-013–NAR-014](../gdd/narrative-bible.md) |
| 55 壁垒认知精确边界 | 壁垒在消息畅通时知道外部两种探索路线，内部也据此分成两个政治阵营；不知道外部两派后来发展成人类内战，也不知道接敌后停战 | NAR-013 · CANON；不是完全不知道两派，也不是知道内战 | [世界观NAR-013](../gdd/narrative-bible.md) |
| 56 三方断联机制v0.4 | 壁垒在内战前先失去自由通信并成为事实上的受保护人居域；外部两派后来保留不经过壁垒的外交窄链并以此停战，折叠最终烧断该链 | PROPOSED；壁垒先行隔离的授权主体、方式和法律依据仍OPEN | [世界观NAR-011](../gdd/narrative-bible.md) |
| 57 壁垒内部两派 | 壁垒不是中立社会在事后才重建争论；通讯仍畅通时，城内已经围绕无限探索与限界探索分成两派，但没有收到外部争端升级为内战的可靠消息 | NAR-013 · CANON；内外同路线阵营是否有正式隶属、指挥或秘密联络仍OPEN | [世界观NAR-013](../gdd/narrative-bible.md) |
| 58 壁垒战前断联机制v0.5 | 曾把壁垒写成位于两派之间、可供一方侧击另一方的战线共享中继，并以中立枢纽保全协议解释断联 | LEGACY/SUPERSEDED；错误是两派中点与侧击位置，不是否定壁垒的多路基础设施枢纽属性；已由NAR-015与v0.7覆盖 | [世界观NAR-015与NAR-011](../gdd/narrative-bible.md) |
| 59 常规通信距离边界 | 界桥断开不会让本地电波消失；同一星球和足够近的节点仍可通信，同恒星系跨行星通信也可能可达，远程星际信号则因延迟与链路预算无法承担即时联系 | NAR-014 · CANON；“壁垒失联”只指远程界桥链，本地节点分布与链路预算OPEN | [世界观NAR-014](../gdd/narrative-bible.md) |
| 60 壁垒地球门关拓扑 | 壁垒位于人类纵深后方，是通往地球的战略门关，不是位于两派之间的战线中继；当时仍可联系地球，控制壁垒意味着可能取得地球后方支持；外敌必须按外拓区→无限派→限界派→壁垒→地球推进 | NAR-015 · CANON；“不是共享中枢”的过宽表述已被条目62纠正，精确星图与是否唯一门关OPEN | [世界观NAR-015](../gdd/narrative-bible.md) |
| 61 后方门关断联机制v0.6 | 战前保全协议只冻结一个前向接口并保留地球内向链；两派另有不通壁垒/地球的外交窄链；最终封网才切断地球内向链并把壁垒留作隔离缓冲 | LEGACY/SUPERSEDED；保留分阶段断联思路，但“一内一外两个接口”过度简化，已由v0.7替换 | [世界观NAR-011](../gdd/narrative-bible.md) |
| 62 壁垒多路后方中枢 | 壁垒是多条界桥汇聚的共享基础设施中枢，至少一支通地球、一支通限界探索区，限界之外才是无限探索区；多路交通与资源使其拥有储备、防御能力和驻军 | NAR-015 · CANON；共享中枢是基础设施属性，不表示壁垒位于两派之间；其他支路终点、资源量与驻军规模OPEN | [世界观NAR-015](../gdd/narrative-bible.md) |
| 63 多路门关断联机制v0.7 | 战前保全协议按路由冻结通往两派战区的前线干线组，暂时保留地球链、认证资源/设施支路、本地通信和守门人合同；最终封网才切断地球链 | PROPOSED；安全支路必须不能中继至战区，具体支路与最终牺牲名单OPEN | [世界观NAR-011与WRD-013](../gdd/narrative-bible.md) |
| 64 自动隔离、联合授权与壁垒误判 | 战前隔离由预置协议自动执行；最终折叠由最后一批两派联合授权者共同签署；壁垒只收到“地球链完整性失效”，不知道自己被主动留在封锁线外 | NAR-016 · CANON；协议起草/阈值、签署人数、执行实例与原始字段OPEN | [世界观NAR-016](../gdd/narrative-bible.md) |
| 65 权限移交来不及完成 | 最高权限原则上可以迁移给壁垒，但危机窗口内未完成 | 部分保留：无时间恢复后重试仍为NAR-017 · CANON；“最后授权者随即全部丧失”未锁定 | [世界观NAR-017](../gdd/narrative-bible.md) |
| 66 权限迁移联网确认失败 | 旧解释为壁垒无法回执且无限探索派也无法确认 | LEGACY/PARTIALLY SUPERSEDED；条目77纠正为无限探索派仍在，唯一失败点是壁垒离线 | [世界观NAR-017与NAR-023](../gdd/narrative-bible.md) |
| 67 最终折叠与权限迁移分流 | 最终折叠是本地破坏性事务；权限迁移是跨域接管事务 | 核心分流仍为NAR-017 · CANON；旧“还要求无限探索派在线确认”已由条目77覆盖 | [世界观NAR-017](../gdd/narrative-bible.md) |
| 68 内战点火事件 | 无限探索派准备启用已认定危险的外拓干线，限界探索派命令守门人隔离；无限探索派派员强闯并造成人类伤亡，冲突升级为内战 | NAR-018 · CANON；危险证据后来由条目75锁定，第一枪、死因和伤亡数仍OPEN | [世界观NAR-018与NAR-022](../gdd/narrative-bible.md) |
| 69 停战双重证据 | 无限探索派必须同时交出可验证锚点数据与虚空兽实体，限界探索派才接受共同威胁并停战 | NAR-019 · CANON；实体必须物理交接或联合检验，具体路径与检疫OPEN | [世界观NAR-019](../gdd/narrative-bible.md) |
| 70 围困与自我封锁 | 逐能虚空兽占据多个出口、锚点和外围据点，使两派残余无法全线撤离；为避免能量梯度继续通向壁垒，两派共同切断周边和壁垒方向线路 | NAR-019 · CANON；不是智能包围，具体节点和破坏方式OPEN | [世界观NAR-019](../gdd/narrative-bible.md) |
| 71 最后几小时暂存 | 区域断网→全线迁移失败→确认周边线路尽失→签署关闭命令，同时权限迁移未完成 | LEGACY/SUPERSEDED；条目77已锁定更新后的相对顺序并纠正迁移失败点 | [世界观NAR-023](../gdd/narrative-bible.md) |
| 72 当代能源压力 | 壁垒附近仍有连接节点和本地守门人合同，但人口与设施负荷增长已令稳定能源不足；维持蓝图/许可交易会增加消耗 | NAR-020 · CANON；单靠“想买蓝图”不能证明必须重开 | [世界观NAR-020](../gdd/narrative-bible.md) |
| 73 能源闭环候选 | 首选为本地供能/转换设施不可逆老化，关键材料或高容量采能设施只在封闭支路外；人口只缩短倒计时，守门人只能给蓝图不能给成品 | LEGACY/SUPERSEDED提案状态；随后由条目74明确批准并升为NAR-021 · CANON | [世界观NAR-021](../gdd/narrative-bible.md) |
| 74 能源闭环批准 | 采用“非自给中枢+关键转换设备老化”组合：壁垒所在有限人工空间没有自然资源或可拓疆域，本地不能造替换件；守门人提供修复蓝图，但材料和完整工业设备只在封锁线外 | NAR-021/DEC-026 · CANON；恢复的是目标明确、可隔离、可再次摧毁的一条旧路线，具体设备与材料OPEN | [世界观NAR-021](../gdd/narrative-bible.md) |
| 75 危险干线模糊证据 | 无人探针在目标区域失联，但已知电磁风暴足以解释损失，风险仍可被视为合理勘探成本 | NAR-022 · CANON；双方解释都合理，当时均不知道虚空兽，数量与风险阈值OPEN | [世界观NAR-022](../gdd/narrative-bible.md) |
| 76 冲突命令触发安全重启 | 两派提交相互冲突的隔离/恢复命令；无限探索派强制覆写守门人权限失败，触发安全重启并自动隔离壁垒 | NAR-016 · CANON；线路失效是外部活动会话失效，不等于锚点已经物理摧毁 | [世界观NAR-016](../gdd/narrative-bible.md) |
| 77 末期顺序与迁移纠正 | 发现虚空兽封锁→撤离失败→迁移权限给壁垒因壁垒离线失败→两派共同授权最终下线；无限探索派在迁移时仍存在 | NAR-017/NAR-023 · CANON；覆盖“无限派也无法确认”，准确小时数与地点OPEN | [世界观NAR-017与NAR-023](../gdd/narrative-bible.md) |
| 78 最终下线范围 | 受困区域节点全部下线；永久切断壁垒—地球支路与壁垒通向两派区域的支路，使早期失效会话不能自动恢复 | NAR-023 · CANON；逐节点硬件/权限手段和人员结局OPEN | [世界观NAR-023](../gdd/narrative-bible.md) |
| 79 筑路者和平与军备追赶失败 | 筑路者科研/网道工程强、长期和平且武器相对落后；虚空兽在其仍存在时进入网络，临时堆军备追不上扩散，最终主动封网 | NAR-024 · CANON；首次进入载体与全物种结局OPEN | [世界观NAR-024](../gdd/narrative-bible.md) |
| 80 壁垒能源转换设施 | 曾把危机写成独立通用能源转换设施；仍保留“界桥不造能、失能会使封闭生态崩溃”的边界 | LEGACY/PARTIALLY SUPERSEDED；具体危机对象由条目92的人造太阳取代 | [世界观NAR-025](../gdd/narrative-bible.md) |
| 81 客观历史v1.0完整候选 | 曾用卵囊、四避难区、四层人类权限、双监护撤销、秘密脉冲及精确数值补洞 | LEGACY/SUPERSEDED；用户认为多项机制不合理或只是为剧情服务，已由v1.1覆盖 | [世界观NAR-011](../gdd/narrative-bible.md) |
| 82 壁垒存在方式与网络技术分层 | 壁垒位于界桥生成的有限非现实节点空间，无法常规扩张或逃离；筑路者原生管理仍工作，人类数据/权限层可独立崩溃 | NAR-015/NAR-016/NAR-026 · CANON；否决双监护技术授权和秘密撤销脉冲 | [世界观NAR-015–NAR-017与NAR-026](../gdd/narrative-bible.md) |
| 83 客观历史分层重构 | 虚空兽在被识别前以活体进入分支枢纽；人类数据层因原生拓扑重配失去共识并陷入启动死锁；死城使用既有原生接口关网；壁垒闭合域没有隐藏逃生口 | LEGACY/PARTIALLY SUPERSEDED；基础技术分层保留，后继社会、虚空兽休眠和关网范围由条目84–87更新 | [世界观NAR-011](../gdd/narrative-bible.md) |
| 84 筑路者后继社会衰亡 | 封网后大多数孤立社会因资源和供应链崩溃而死亡；少数存续者也因社会破碎而严重技术退化 | NAR-024/DEC-027 · CANON | [世界观NAR-024](../gdd/narrative-bible.md) |
| 85 整片可控网络停摆 | 最后行动关闭死城权限能够触及的全部活动路线和非必要节点供能，不是只隔离壁垒；目标是让虚空兽失去跨节点能量梯度 | NAR-019/NAR-023/DEC-025 · CANON | [世界观NAR-023](../gdd/narrative-bible.md) |
| 86 虚空兽生态与其他入网阵营 | 虚空兽起源于宇宙空洞贫能天体，偏食高能目标；界桥供能支持迁徙和繁殖，断能后停止繁殖并休眠；灼星种和借尸者也能利用既有网络但控制能力低于人类 | NAR-027/DEC-030 · CANON | [世界观NAR-027](../gdd/narrative-bible.md) |
| 87 外勤旧制低权限 | 小队使用断网前身份体系衍生的凭证；设施能识别格式但无法验证最新授权链，同一身份在不同节点映射不同，机器只接受本地命令 | NAR-028/WRD-015/OPS-009/DEC-031 · CANON；具体玩家身份与权限恢复节奏OPEN | [世界观NAR-028](../gdd/narrative-bible.md) |
| 88 供电不等于立即唤醒 | 节点重新供能只恢复能量与迁徙信标，不会立刻唤醒所有本地休眠虚空兽；个体需局部刺激超过唤醒阈值才进入活动 | NAR-027/ENC-011/DEC-030 · CANON；具体刺激组合和阈值待原型 | [遭遇ENC-011](../gdd/encounters-and-difficulty.md) |
| 89 载波重置与物理恢复 | 安全重启改变节点载波和字形路由；近距节点可用常规通信恢复，远端必须携恢复盘到场读取新载波、写入译码/身份映射并重新确认字形路线 | NAR-016/NAR-029/WRD-016/DEC-032 · CANON；恢复盘不是通用钥匙 | [世界观NAR-029](../gdd/narrative-bible.md) |
| 90 限界派灾备与防御资产 | 限界派各节点保留备份、恢复盘、资源、独立供电、炮塔和机器人；节点重新入域后，仍受本地控制的完整资产可转为友军 | NAR-029/WRD-016/ENC-012/DEC-033 · CANON；不免费修复或补满资产 | [设施WRD-016](../gdd/world-and-information.md) |
| 91 虚空兽长期积累 | 虚空兽繁殖不快，入侵规模来自宇宙空洞天体上历经极长时间积累和休眠的既存种群；Operation不以快速繁殖解释刷新 | NAR-027/ENC-011/DEC-030 · CANON | [世界观NAR-027](../gdd/narrative-bible.md) |
| 92 人造太阳数月倒计时 | 聚变燃料、冷却介质和电磁约束组件因同一长期供应链断裂接近终点，人造太阳将在数月内停机 | NAR-020/NAR-021/NAR-025/DEC-036 · CANON；精确月份与先失效子系统OPEN | [世界观NAR-025](../gdd/narrative-bible.md) |
| 93 两类区域风险收益 | 无限区少战术补给、多虚空兽与高永久发现收益；限界区多弹药/医疗和旧防御，重写后可获友军资产，但永久发现收益较少 | OPS-010/ECO-015/DEC-034 · CANON/DIRECTION；不是简单倍率 | [Operation OPS-010](../gdd/operations.md) |
| 94 可选字形改道 | 玩家可从任务内证据推导字形，把路线改至既存秘密空间；额外资源、信用点、成就、外观或知识必须承担额外敌人、时间、供能或退路风险 | WRD-017/MIS-015/DEC-035 · DIRECTION；禁止盲猜与Wiki依赖 | [任务MIS-015](../gdd/missions-and-spaces.md) |
| 95 节点永久清场与行星Descent | 世界观允许节点逐个永久清理，并以真实敌对行星端点承载非时间循环Descent | NAR-030/DEC-037 · CANON（LORE ONLY）；基础版玩家可见节点进度已被条目98否决 | [世界观NAR-030](../gdd/narrative-bible.md) |
| 96 程序Operation任务板 | Operation使用壁垒中央Hub任务板；地图程序生成，主任务与兼容支线随机组合，玩家选择任务和难度 | OPS-011/MIS-016/PRG-012/DEC-038 · CANON/DIRECTION；后续条目105取消账号主线阶段 | [Operation OPS-011](../gdd/operations.md) |
| 97 Operation多任务族与非固定关卡 | 节点恢复不是默认骨架；至少包括废料、资源、技术、研究数据、设施网络恢复和威胁处理，正式地图每局程序组合 | OPS-012/MIS-017 · CANON/DIRECTION；“每局新体验”是需试玩验证的决策差异，不是Seed不同即成立 | [任务MIS-017](../gdd/missions-and-spaces.md) |
| 98 节点仅用于Descent发布行动 | 基础版不显示或累计节点；Descent DLC发布时才以全服务器联合行动统计节点恢复，完成后永久开放真实行星端点 | VIS-009/OPS-013/PRG-013/DES-010/DEC-039 · CANON/DIRECTION；不得永久扣留已购买内容 | [Operation OPS-013](../gdd/operations.md) |
| 99 匹配后端复用活动汇总 | 基础版本来需要匹配控制面；Descent联合行动复用它去重结果和累计公共进度，普通对局仍由玩家房主运行 | NET-001/NET-008/DEC-040 · CANON/DIRECTION；小型部署是待压测成本假设 | [网络NET-008](../technical/network-and-persistence.md) |
| 100 合作PVE不建设反作弊 | 接受房主可修改私人会话；活动服务只做格式、账号边界、ResultID去重和公共计数一致性，不做作弊检测或封禁 | NET-008/OPS-013/PRG-013/DEC-040 · CANON/DIRECTION | [网络NET-008](../technical/network-and-persistence.md) |
| 101 GTFOReplay式战报与回看 | 初始要求参考GTFOReplay：每局结束显示团队命中率、伤害、击杀、倒地/救援、资源、目标等统计及行动摘要，并允许之后重看 | 由102与103细化；保留“结算期战报+可回看”的方向，不再解释为完整3D录像或永久档案 | [战报与回放](../gdd/debrief-and-replay.md) |
| 102 详细统计与轻量本地回放 | 战报统计要细，回放本身不要细到吞噬磁盘；本地只录简化地图、低频位置、关键动作和事件。潜行破坏必须能看到谁在何时以什么方式惊动敌人并跳到对应片段 | RPL-001至RPL-008/TRP-001至TRP-006/UX-009/DEC-041 · CANON/DIRECTION；Authority证据不足时共同/无法归因，不瞎甩锅 | [战报与回放](../gdd/debrief-and-replay.md) |
| 103 结算确认后删除 | 详细统计和简化回放只需保留到本局结束后的复盘；玩家确认后不再需要 | RPL-001/RPL-006/TRP-001/TRP-004/UX-009/DEC-041 · CANON/DIRECTION；取消永久行动档案、保存、置顶、导出与跨Build兼容 | [战报与回放](../gdd/debrief-and-replay.md) |
| 104 玩家是谁 | 在客观历史之后开始设计玩家剧情，先确定玩家身份 | 助手候选部分接受后被条目105覆盖：“第一代重新出网”、组织来源和线性发现未确认；专业外勤小队名称保留 | [中央故事STORY-008](../gdd/central-story-spine.md) |
| 105 固定四人、正史存活、非递进 | 玩家是类似GTFO的固定四人“壁垒外勤小队”，四人正史存活；不必装作不知道内战和虚空兽，基础玩法像《深岩银河》而非递进战役 | STORY-008至STORY-010/DEC-042至DEC-043 · CANON/DIRECTION；姓名、关系、外观和上级机构OPEN | [玩家故事](../gdd/central-story-spine.md) |
| 106 成就与收藏碎片叙事 | 玩家故事主要作为类似《黑暗之魂》的成就和可收集碎片存在 | STORY-011/NDL-004/MIS-018/PRG-014/DEC-044 · CANON/DIRECTION；不锁任务/战力，具体首批集合与成就名OPEN | [玩家故事STORY-011](../gdd/central-story-spine.md) |
| 107 四名角色v1 | 用户要求开始设计四名固定外勤队员 | 助手提出四立场、六组关系、收藏链、对白与反刻板边界，并建议解绑Signature Active；最初真实姓名候选随后被用户否决 | [角色v1](../content/character-roster-v1.md) |
| 108 只做人格并改用代号 | 用户限定本轮只做人设，不做美术或长相，并要求用代号替代真实姓名 | 人格、价值观、缺陷、关系、说话逻辑、背景与收藏钩子保留；年龄、性别呈现、身体、面部、服装、配色、轮廓、动作外观和配音选角DEFERRED；真实姓名不显示且不设真名谜题 | [角色CHAR-001/008](../content/character-roster-v1.md) |
| 109 代号语气纠正 | 用户连续否决`界碑/游标/砝码/留白`与`老闩/译码/骡子/白手套`，要求真正有冲击力的中文代号 | 两组候选作废；助手提出事故型候选`断桥/回声/铁砧/寒蝉`，仍为PROPOSED FOR USER VERDICT | [角色CHAR-001](../content/character-roster-v1.md) |

最终规则不能仅凭此摘要改变；需要在对应DDD与责任GDD记录明确确认。原文里的原型数值和最新提案差异保留为显式OPEN，不悄悄删除。
