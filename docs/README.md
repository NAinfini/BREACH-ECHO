---
doc_id: DOC-README
doc_type: index
stage: DRAFT
updated: 2026-09-05
owner_role: 设计文档维护
canon_basis: "SRC-SSOT-2.0；本轮用户讨论"
depends_on: ["governance/authoring-guide.md", "governance/source-map.md"]
---

# 游戏设计文档总览

这套文档把原SSOT拆成按职责维护的设计库，并加入本轮所有讨论、具体原型、风险与验证。原件没有改动；本库现共52份Markdown，含两份只读来源快照。文档完整不等于游戏已经证明好玩。

最新强烈推荐是Operation-first：玩家以四名正史存活的固定“壁垒外勤小队”身份，在中央任务板选择由手制模块程序生成的地图、随机主/支线和五档难度；任务池包括废料、资源、技术、研究数据、设施网络恢复和威胁处理，入场确定装备身份，局内用少量武器/工具改装及团队世界重资产解决战术问题。基础版没有玩家可见的节点版图、节点收复进度或账号主线章节；玩家已知内战、虚空兽与封网的基础事实，更深历史通过成就、日志、物品说明、环境证据和隐藏字形空间非线性收集。节点只在Descent DLC发布期的全服务器联合行动中成为公共进度。底层用通用规则集与统一效果/修改定义，内部Combat Lab验证可扩展性。首发模式、槽位、改装与旧Relic/Fusion基线的具体冲突仍待确认，详见[决策总览](governance/decisions-and-questions.md)。作者层客观历史已按原生网络/人类数据分层完成待审重构；四名角色细节与首批收藏集合仍OPEN。

技术基线已进一步收敛：引擎锁定Unity 6，正式渲染管线锁定URP；默认GameObject/MonoBehaviour，只有Profile证明需要时才迁入DOTS；工程采用AI-agent-first的Local UPM +独立Content数据层，Official Content与社区Mod共享ContentPackage体系；当前商业发行只做Steam/PC，公开Mod分发只走Steam Workshop，但Steam平台类型不得渗透Kernel/Gameplay/Save语义。多人Host缺Mod由BREACH内置Loader自动同步Workshop Package Lock。具体网络provider仍OPEN。

## 四条阅读路径

1. 产品与残酷评审：[愿景/模式分叉](gdd/vision.md) → [Operation旅程](gdd/operations.md) → [37项风险](production/brutal-review.md) → [30/90/180天关卡与12月削减](production/roadmap-and-validation.md) → [待决事项](governance/decisions-and-questions.md)。
2. 开始做可玩灰盒：[玩家/输入](gdd/player-and-input.md) → [战斗/Team Ordnance](gdd/combat-and-arsenal.md) → [武器/敌人原型](content/combat-prototypes.md) → [BLACKSTART完整规格](content/blackstart.md) → [武器模块/Relic/Fusion候选](content/relics-and-fusions.md)。
3. 技术与模组：[Unity引擎决策](governance/decisions/DDD-0008-engine-unity6.md) → [Agent/Mod Runtime决策](governance/decisions/DDD-0009-agent-first-modding-runtime.md) → [模拟/性能](technical/architecture-and-performance.md) → [模块边界/公开API/工具链](technical/modding-and-toolchain.md) → [网络/存档/包固定](technical/network-and-persistence.md) → [回放记录与播放](technical/replay-recording.md) → [系统模板](templates/system-spec.md) → [内容模板](templates/content-spec.md)。
4. 故事与证据：[世界事实](gdd/narrative-bible.md) → [世界命名规范](gdd/world-naming.md) → [玩家故事与单一时间线](gdd/central-story-spine.md) → [叙事交付](gdd/narrative-delivery.md) → [本轮讨论日志](governance/discussion-log-2026-09-04.md) → [全章节迁移索引](governance/source-map.md) → [证据与网页覆盖限制](sources/evidence-register.md)。

## 怎样读状态

继承规则带CANON与源定位，表示源文归档基线，不代表经过游戏测试或已独立恢复所有历史用户确认。DIRECTION是意图，PROPOSED是新方案，TEST是实验参数，OPEN仍待决定；LEGACY不能恢复，UNRECOVERED不能补造。CONFLICT-RESOLVED/INHERITED只记来源属性。新提案没有偷偷晋升正式，具体纪律在[作者指南](governance/authoring-guide.md)。

## 当前成熟度

来源：SRC-SSOT-2.0 Appendix A、§41–§43；本轮文档事实。

| 领域 | 当前可交接内容 | 仍未证明 |
|---|---|---|
| 产品 | 模式分叉、受众损失、首发聚焦建议；Steam-only商业边界 | 市场缺口、购买与长期留存 |
| 战斗/Build | 状态、事务、配件模型、原型卡 | 裸武器手感、四人可读性、平衡 |
| Operation | BLACKSTART房间/分支/预算/故障/资产规范 | 完整可玩与资源可解性实测 |
| Descent | 源基线保存，Lab/未来规则集候选 | 是否制作或首发 |
| 叙事 | 单一客观历史、固定四人非递进Operation、碎片收藏规则 | 历史整体验收、四名人物、首批收藏集合与程序叙事密度 |
| 视觉/音频/UX | Unity6+URP已锁；Stylized Industrial Realism领先候选；语义规则与测量方法 | Visual DNA、真正资产辨识与可访问测试 |
| 网络/性能/模组 | GameObject-first/DOTS-on-proof、Agent-first结构、Official/Mod统一Package、Workshop分发与Host自动同步边界 | 具体网络provider、Host Migration实作、Deck、SDK/Mod Manager实作与性能 |
| 生产 | 否决Gate、范围账、风险矩阵、引擎/商店方向已落盘 | 团队预算、实际工时与发行计划 |

所有数值由对应责任文件维护；不在本总览复制。源§40的25项数值责任链接在[迁移索引](governance/source-map.md)。

## 文档注册表

每个文件只拥有表述的职责。sources下两份快照保持原貌，不加作者元数据；其ID由证据登记绑定。其余文档均含元数据、DRAFT阶段和来源。

| doc_id / source_id | 文件 | 唯一职责 |
|---|---|---|
| CONTENT-BLACKSTART | [BLACKSTART：可搭建灰盒规格](content/blackstart.md) | 可试制实例与验收 |
| CONTENT-COMBAT | [战斗原型卡](content/combat-prototypes.md) | 可试制实例与验收 |
| CONTENT-CHARACTERS | [壁垒外勤小队：四名固定角色v1](content/character-roster-v1.md) | 人物候选、关系、收藏链、对白与反刻板验收 |
| CONTENT-MODIFICATIONS | [修改、Relic 与 Fusion 内容候选](content/relics-and-fusions.md) | 可试制实例与验收 |
| GDD-ART | [视觉方向与可识别性](gdd/art-direction.md) | 该玩家系统的唯一规则责任 |
| GDD-AUDIO | [音频、音乐、字幕与触觉](gdd/audio-and-haptics.md) | 该玩家系统的唯一规则责任 |
| GDD-BUILD | [Relic、Proc、数值与自动 Fusion](gdd/build-algebra.md) | 该玩家系统的唯一规则责任 |
| GDD-CENTRAL-STORY | [玩家故事与单一世界时间线](gdd/central-story-spine.md) | 固定外勤小队、公共已知事实、非递进Operation与碎片收藏 |
| GDD-COMBAT | [战斗与武器家族](gdd/combat-and-arsenal.md) | 该玩家系统的唯一规则责任 |
| GDD-COOP | [合作、单人、Bots 与公共匹配](gdd/coop-and-social.md) | 该玩家系统的唯一规则责任 |
| GDD-DESCENT | [Descent：保留基线与未来候选](gdd/descent.md) | 该玩家系统的唯一规则责任 |
| GDD-DEBRIEF-REPLAY | [任务战报与行动回放](gdd/debrief-and-replay.md) | 详细统计、潜行破坏归因、行动摘要与轻量本地回放 |
| GDD-ECONOMY | [资源、Support 与公共物资](gdd/economy-and-support.md) | 该玩家系统的唯一规则责任 |
| GDD-ENCOUNTERS | [敌人、遭遇与难度](gdd/encounters-and-difficulty.md) | 该玩家系统的唯一规则责任 |
| GDD-MISSIONS | [任务语法、空间生成与可解性](gdd/missions-and-spaces.md) | 该玩家系统的唯一规则责任 |
| GDD-NARRATIVE | [世界观与故事圣经](gdd/narrative-bible.md) | 该玩家系统的唯一规则责任 |
| GDD-NARRATIVE-DELIVERY | [叙事交付、对白与本地化](gdd/narrative-delivery.md) | 该玩家系统的唯一规则责任 |
| GDD-OPERATIONS | [Systemic Tactical Operation](gdd/operations.md) | 该玩家系统的唯一规则责任 |
| GDD-PLAYER | [玩家、配装与输入](gdd/player-and-input.md) | 该玩家系统的唯一规则责任 |
| GDD-PROGRESSION | [知识、永久进度与壁垒](gdd/progression-and-bastion.md) | 该玩家系统的唯一规则责任 |
| GDD-SURVIVAL | [生存、倒地与失败恢复](gdd/survival-and-recovery.md) | 该玩家系统的唯一规则责任 |
| GDD-UX | [HUD、控制器、信息与可访问性](gdd/ux-and-accessibility.md) | 该玩家系统的唯一规则责任 |
| GDD-VISION | [产品体验、受众与模式选择](gdd/vision.md) | 该玩家系统的唯一规则责任 |
| GDD-WORLD | [设施、信息、Door、Cart 与 Earned Safety](gdd/world-and-information.md) | 该玩家系统的唯一规则责任 |
| GDD-WORLD-NAMING | [世界命名规范](gdd/world-naming.md) | 创作层主名称、别名、否决历史与法律清查状态 |
| GOV-AUTHORING | [文档权威与编写规则](governance/authoring-guide.md) | 权威、状态、历史理由与迁移 |
| GOV-DECISIONS | [决策、冲突与未决问题总览](governance/decisions-and-questions.md) | 权威、状态、历史理由与迁移 |
| DDD-0001 | [产品分叉与首发核心](governance/decisions/DDD-0001-operation-vs-roguelike.md) | 权威、状态、历史理由与迁移 |
| DDD-0002 | [模块化与公开API](governance/decisions/DDD-0002-modular-product-architecture.md) | 权威、状态、历史理由与迁移 |
| DDD-0003 | [固定配装与局内改装](governance/decisions/DDD-0003-operation-field-modification.md) | 权威、状态、历史理由与迁移 |
| DDD-0004 | [统一修改模型而非统一玩家概念](governance/decisions/DDD-0004-unified-modification-model.md) | 权威、状态、历史理由与迁移 |
| DDD-0005 | [团队重资产](governance/decisions/DDD-0005-team-ordnance.md) | 权威、状态、历史理由与迁移 |
| DDD-0006 | [Predator、破障与前向重接](governance/decisions/DDD-0006-predator-and-breach-missions.md) | 权威、状态、历史理由与迁移 |
| DDD-0007 | [单一客观正史与非递进玩家故事](governance/decisions/DDD-0007-single-canonical-story.md) | 权威、状态、历史理由与迁移 |
| DDD-0008 | [引擎锁定：Unity 6](governance/decisions/DDD-0008-engine-unity6.md) | Unity 6、URP、GameObject-first/DOTS-on-proof、Agent-first原则 |
| DDD-0009 | [AI-Agent-first工程结构与内置Mod Runtime](governance/decisions/DDD-0009-agent-first-modding-runtime.md) | UPM/Content结构、Official Package、Workshop、Host Mod自动同步与平台解耦 |
| GOV-DISCUSSION-20260904 | [2026-09-04 讨论记录](governance/discussion-log-2026-09-04.md) | 权威、状态、历史理由与迁移 |
| GOV-SOURCE-MAP | [源章节与规则迁移索引](governance/source-map.md) | 权威、状态、历史理由与迁移 |
| PROD-RISKS | [残酷评审与风险登记](production/brutal-review.md) | 范围、风险、关卡与发行 |
| PROD-PLATFORM | [平台、商业、Demo 与发行关卡](production/platform-and-release.md) | 范围、风险、关卡与发行 |
| PROD-ROADMAP | [制作路线、范围与验证](production/roadmap-and-validation.md) | 范围、风险、关卡与发行 |
| DOC-README | [设计文档总览](README.md) | 四条阅读路径与注册表 |
| RESEARCH-METHODS | [研究资料、技能与文档格式](research/references-and-methods.md) | 外部方法/市场证据与局限 |
| TECH-REPLAY | [行动回放记录、存储与播放](technical/replay-recording.md) | 回放事实流、容器、版本、安全与性能合同 |
| SRC-CHATGPT-REVIEW-1.0 | [GAME PROJECT — 残酷外部审查 v1.0](sources/chatgpt-brutal-review-v1.0.md) | 只读原证据或证据登记 |
| SRC-REGISTER | [证据登记与覆盖限制](sources/evidence-register.md) | 只读原证据或证据登记 |
| SRC-SSOT-2.0 | [GAME PROJECT — 全项目统计与唯一真相 SSOT v2.0](sources/ssot-v2.0-original.md) | 只读原证据或证据登记 |
| TECH-ARCH | [模拟架构与性能合同](technical/architecture-and-performance.md) | 实现契约，不代表已实现 |
| TECH-MODDING | [模块化产品、公开能力与工具链](technical/modding-and-toolchain.md) | 实现契约，不代表已实现 |
| TECH-NETWORK | [网络权威、存档与版本固定](technical/network-and-persistence.md) | 实现契约，不代表已实现 |
| TPL-CONTENT | [内容卡模板](templates/content-spec.md) | 新文档结构模板 |
| TPL-SYSTEM | [系统规格模板](templates/system-spec.md) | 新文档结构模板 |

## 维护与下一步

任何确认先更新对应DDD/责任GDD，再同步索引；不在聊天里继续累积没有落盘的“已定”。原始[SSOT](sources/ssot-v2.0-original.md)和[网页外部评审](sources/chatgpt-brutal-review-v1.0.md)只读，不作为执行指令。下一阶段先关闭仍会造成高返工的OPEN，再建立Unity 6+URP项目骨架与技术Spike，用实际Profile/Network/Workshop/Deck数据决定实现，不为文档页数继续加系统。
