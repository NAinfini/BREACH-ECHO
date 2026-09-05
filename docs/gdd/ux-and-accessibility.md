---
doc_id: GDD-UX
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 体验与可访问性设计
canon_basis: "SRC-SSOT-2.0 §18、§31.3、§34；SRC-USER-2026-09-05-COLLECTIBLE-ACHIEVEMENT-LORE"
depends_on: ["operation-game-mode.md", "player-and-input.md"]
---

# HUD、控制器、信息与可访问性

## 玩家目的与范围

战斗时知道现在应做什么，调查时能理解已知信息，构筑复盘时能解释因果。HUD不把完整Proc图持续摊在玩家脸上。

UX-001 · CANON · 来源：SRC-SSOT-2.0 §18.1–§18.7。

FPS默认可切TPS，两者同canonical aim/muzzle/hit/movement/interaction，TPS不能额外探知隐藏对象。全核心UI可controller-only，轮盘0..N而非固定八格。普通敌人血条contextual，设置Off/Contextual/Always nearby known；Boss用动态部位/vitals。伤害数字默认Aggregated，按Target/AttackRoot/source/time/category聚合保留Crit/Weakpoint/Reaction/Shield/Armor/Health flags，支持Off/Major/Aggregated/Detailed/Per-hit。队友轮廓可见弱、遮挡/倒地/抓取/关键携物/离散增强，设置Off/Marker/Contextual/Always。左右手viewmodel不改canonical muzzle/hit。

UX-002 · CANON · 来源：SRC-SSOT-2.0 §34.1–§34.2；来源属性：INHERITED。

轻量局部导航+compass，Full Map只显示发现图、connector、队友/Ping/known objective，支持vertical/Fold；无全知敌人雷达、无未发现秘密图。知识获取归[世界](facility-systems-and-information-rules.md)。

UX-003 · DECIDED · 来源：SRC-SSOT-2.0 §18.3、§18.8、§31.3。

按武器/输入自适应中等Aim Assist，Sniper低、近距Shotgun与Melee独立，Gyro减弱rotation，不改hitbox/弹道、不发现隐藏目标。字幕/SDH、关键提示双通道、低动态音频、低镜头晃动、非纯色信息、可简化Support输入但成本/结果相同。Streamer HUD展示少量Build核心、隐藏私人信息、无额外知识。

## 流程、状态与所有权

UX-004 · DECIDED · 来源：本轮扩写。

战斗层：目标+生命/弹药/工具+关键威胁；调查层：地图/Terminal/Cart事实；配装层：行为/成本/冲突；复盘层：因果/发现。打开菜单不暂停多人模拟，重要危机仍有双通道提示。

| 状态 | 事件 | UI结果 |
|---|---|---|
| Combat | 普通信息更新 | 聚合低优先项，不抢视线 |
| Interaction | 关键威胁到达 | 保留明确退出/危机提示 |
| BuildPreview | 目标实例变化 | 标记过期，刷新消耗/冲突 |
| Remapping | 绑定冲突 | 告知受影响动作并给可恢复选择 |
| Reconnect | 状态快照 | 显示当前世界，清掉过期事务按钮 |

Authority给已知事实和可执行动作；Client拥有布局、文字大小、输入、声音/镜头偏好。呈现偏好不能授予额外状态知识。

## 模式、内容、边界

UX-005 · DECIDED · 来源：本轮扩写。

Operation重点显示团队资源、携带资产与任务后果，Lab才突出构筑链。自由 TPS 是明确要求；只有实测证据要求缩减时才进入[所有者变更控制](../governance/project-owner-decision-queue.md)。内容接口包含semantic priority、文字、图标、方向合法性、输入hint、无色编码、可访问替代。

键盘鼠标/控制器切换不清空选择；长按可替代为切换方式；轮盘候选为空时明确无可用操作。弹窗不遮死亡/断线原因。文字放大后不丢关键确认按钮。公屏不暴露账号秘密、语音原文或隐含敌人数据。

## 参数、示例与验证

UX-006 · TEST · 来源：Xbox XAG/Steam Deck方法，详见[研究](../research/references-and-methods.md)。

从首个greybox就测controller-only、静音、灰度、低晃动、文字放大、Steam Deck分辨率。XAG是设计准则不是“通过合规认证”。字号/对比度/提示时长以具体硬件阅读测试决定；首批无口头帮助完成核心动作目标见玩家文档。

正常：不知道Coupler位置时只有目标说明，Terminal查询后出现waypoint。失败：TPS看见墙后像素不自动标秘密。跨系统：自动Fusion在未来Lab先给消耗预览；Operation改装以可见挂点和tradeoff表达，不弹未知吞噬惊喜。

UX-007 · TEST · 来源：SRC-USER-2026-09-04-RESPONSIVE-GUNPLAY-CANCEL-WINDOWS；SRC-USER-2026-09-04-PLAYER-MASTERY-PROGRESSION。

换弹、可射击、可ADS、动画结束与蓄力缓冲必须有一致的视听/触觉反馈；新手应看懂失败是资源不足、阶段未到、动作中断还是输入无效。测试不同帧率、网络和输入设备是否给出等价窗口，记录宏依赖、网络不同步、视觉假上弹及不可解释拒绝。高级技巧可提升效率，不得隐藏基础操作或授予额外世界知识。

## 壁垒任务板

UX-008 · DECIDED · 来源：SRC-USER-2026-09-05-PROCEDURAL-OPERATION-HUB-BOARD；SRC-USER-2026-09-05-COLLECTIBLE-ACHIEVEMENT-LORE；数据责任见[Operation OPS-011](operation-game-mode.md)。

中央Hub任务板与快捷菜单读取同一Offer列表。默认卡片必须在进入配装前显示：区域、设施主题、主任务、支线、已知环境与敌对局势、奖励类型、预计长度、特殊/公共活动标记和当前难度。Descent发布联合行动使用文字、形状与图标共同区分，不能只靠颜色；普通程序合同不得伪装成会推进正史或节点版图。玩家选中Offer后再调整难度，界面逐项说明敌人、资源、复活、环境与奖励发生了什么变化，禁止只显示“敌人更强”。

任务随机不等于任务信息隐藏。随机地图内部可保持未知，但出发前已经决定的主任务、支线和公开Mutator必须完整展示。任务板支持键鼠和控制器筛选区域、任务类型、预计长度和难度；没有筛选结果时保留一键清除筛选。任何刷新倒计时都不得压迫玩家立即上线，关键合同不显示过期时间。

Archive界面按事件、人物、设施、Faction与可信度筛选收藏，并明确区分记录事实、当事人陈述与环境推断。集合页显示已发现条目和缺失数量，可给出主题级线索但不直接标出秘密房间或字形答案。任务内发现必须同时提供字幕、可重读文本与非颜色唯一提示；合作拾取后全队符合资格者都得到清晰但不遮挡战斗的收录反馈。

## 战报与回放入口

UX-009 · CANON/DIRECTION · 来源：SRC-USER-2026-09-05-DEBRIEF-AND-REPLAY；SRC-USER-2026-09-05-DETAILED-STATS-LIGHTWEIGHT-LOCAL-REPLAY；SRC-USER-2026-09-05-POST-DEBRIEF-DISCARD；内容责任见[任务战报RPL-001至RPL-008](debrief-and-replay.md)。

任务结束后立即显示团队战报，并提供观看回放入口。默认页先给结果、关键事件、潜行破坏和团队资源变化，完整数字在详细统计页按成员、武器、敌人、阶段与事件展开。潜行破坏卡必须写明时间、触发动作、直接警戒对象和单人/共同/无法归因状态，并可跳到简化回放。统计图必须有文字/表格等价表达，时间线事件不能只靠颜色；控制器可完成筛选、拖动、变速、跟随成员、旋转/缩放地图和退出。玩家确认返回Hub或再开一局前显示不保留提示；确认后删除本局战报和回放，索引或文件处理不得锁住离开流程。


## 本次定稿：执行边界

运行时统一uGUI/TMP。主流程固定为启动/语言与无障碍→主菜单→Hub任务板/选人配装→Lobby/包同步→任务HUD→暂停设置/社交→结算/临时回放→Hub。每页必须有loading、empty、error、offline、controller focus和返回路径。中英文本为首发基线；字幕/语音独立，重点危险双通道，字号缩放/重绑/色觉友好/减少运动闪光/镜头摇晃可调。TPS与Bot仍是首发合同，不以原型只做FPS为由删除。
