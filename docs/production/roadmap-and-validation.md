---
doc_id: PROD-ROADMAP
doc_type: production
stage: BASELINE
updated: 2026-09-05
owner_role: 制作与验证负责人
canon_basis: "SRC-SSOT-2.0 §31、§41–§43；外部评审与最新用户意图；SRC-USER-2026-09-05-UNITY-ENGINE-LOCK；SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED；SRC-USER-2026-09-05-HOST-AUTHORITY-GAMEPLAY-COMMANDS；SRC-USER-2026-09-05-TICK-ARCHITECTURE；SRC-USER-2026-09-05-REPLICATION-ARCHITECTURE；SRC-USER-2026-09-05-LAG-COMPENSATION-BASELINE-APPROVED；SRC-USER-2026-09-05-HUMAN-FILE-NAMES-AND-LARGER-BATCHES"
depends_on: ["risk-register.md", "../governance/decisions/unity-engine-and-rendering.md", "../governance/decisions/agent-first-modding-runtime.md", "../governance/decisions/host-authority-and-gameplay-commands.md", "../governance/decisions/fixed-tick-and-multirate-simulation.md", "../governance/decisions/state-replication.md", "../governance/decisions/lag-compensation-and-server-rewind.md", "asset-policy-and-provenance.md"]
---

# 制作路线、范围与验证

## 当前成熟度

PLAN-001 · DIRECTION · 来源：SRC-SSOT-2.0 Appendix A、§41–§43；按最新用户技术决定更新。
项目尚未production ready。战斗/Build/Operation未通过原型，Narrative连接因果仍需审阅，Visual DNA虽已锁定但未通过实机生产Gate；**Unity 6 + URP、分层壁垒与中等多边形几何档位、GameObject-first/DOTS-on-proof、AI-agent-first、Steam/Workshop边界、Host Authority、60 Hz Authority、Snapshot/Delta/Event/Interest/Dormancy、有限Server Rewind、Steam/SDR + FishNet + 自有恢复，以及Luau Core/无社区DLL/旧hash本地缓存原则已锁。** 150 ms Rewind和全部容量/性能值只是TEST；FishySteamworks、Host Migration、Luau绑定、Mod Manager UX、Asset Registry细节、视觉Style Target、Deck性能与SDK成熟度仍未证明。当前交付主要是设计文档，不是完成的游戏；所有试玩、性能、市场Gate均“未执行”。

PLAN-002 · LEGACY/SUPERSEDED + PROPOSED · 来源：SRC-SSOT-2.0 §42；SUPERSEDED BY DECISION-UNITY-ENGINE-RENDERING。
原流程中的“Phase5 Engine Lock”已被用户提前完成，不再等待Descent原型后才选引擎。保留“先验证再扩范围”的方法，不制作Unity/Unreal双引擎分支。网络顺序为：Authority→Tick→Replication→Lag Compensation→Steam-only网络运行与恢复（原则均已锁）→公网/断主机实测；具体时间、频率和adapter仍为TEST。制作顺序仍为Visual/资产规则→Unity项目骨架/Agent与Package基础→Combat Sandbox→Build/Combat Lab→micro-BLACKSTART→完整Operation切片→网络/Deck/Workshop与Modding spikes。Descent是否进入正式制作仍需独立产品裁决。

## 30 / 90 / 180 天关卡

PLAN-003 · PROPOSED · 来源：本轮Operation-first评审；SRC-CHATGPT-REVIEW-1.0 §9；按Unity/Steam锁定调整。

日数从有可用开发人力的试制开始算，是检查点而非发布日期。每Gate需build/hash、录像、事件log、样本/招募来源、观察及决定；数值阈值唯一归[风险矩阵](risk-register.md)，不得事后替换。至少包含新手、合作核心玩家、陌生无语音队与单人，作者/开发者数据单独标。

| 时间 | 只交付的证明对象 | 关键风险/判断 | 失败后动作 |
|---|---|---|---|
| Day0–30 | Unity 6+URP可重复Build；AI-agent-first目录/validator骨架；灰盒裸武器/移动、少量敌人、控制器、三视觉候选；一个Official ContentPackage与一个测试Mod走同一Registry | RK02/03/07/08/20/33；技术基础不能拖慢裸战斗 | 裸战斗不过，停Build与内容扩建；工具过重则删未被真实消费者使用的抽象 |
| Week8 | 少量Weapon/Tool Modules；10min内部Combat Lab；至少一条可读Proc链与拒绝非法环；GameObject真实Profile并只对已证瓶颈做DOTS spike | RK04/06/27/28；Operation未焊死Kernel；DOTS不得先验扩散 | 删无玩家价值的抽象/上位模块；无Profile收益则保持GameObject |
| Week12 / Day90 | 10–15min micro-BLACKSTART；一次Terminal/Cart/Support、前向Breach+重资产、无语音团队；同一事件流生成最小详细战报与潜行破坏事件 | RK11/12/13/26/29/30/31/36/37 | 任务层不提高复玩则重做/转向；战报无法对账则先修事实流，不扩简化回放 |
| Day91–180 | 完整固定BLACKSTART、实际视觉/音频、失败banking、solo/private/public、network/Deck spikes；Workshop Host缺包自动同步切片；简化本地战术回放性能切片 | RK15/17/22/23/25/32/35/36/37；Package exact-hash与恢复 | 选择Operation聚焦、转向或停止；网络/Mod同步不稳则不扩大公开匹配/SDK范围 |
| Day180决策 | 产品差异与增量成本证据 | 是否值得付费、再次组队、再开一局 | 只有两体验均强且成本被证明才考虑双模式；默认Descent延后 |

PLAN-004 · TEST · 来源：本轮对照试验设计。
任务价值实验：同一套战斗内容，A为轻目标战斗，B为Terminal/Cart/路线后果，C为B+少量武器改装；顺序随机/交叉平衡，保持时长和敌人资源条件可比较。观察自发再开选择与原因，而非只给1–10满意度。候选Gate：B相对A至少多20个百分点参与者选择自发再玩，且至少70%能复述设施选择后果；C不得显著增加等待或误解。小样本用于否决/方向判断，不宣称统计显著或销量推断；不达时先诊断等待、谜底背熟或资源失衡。

## 若只有12个月与小团队

PLAN-005 · PROPOSED · 来源：SRC-CHATGPT-REVIEW-1.0 §8；最新用户方向。
团队/预算未知，因此这是假设下的削减建议，需要实际工时校准。先砍完整第二产品和工具产品化，不平均把每一系统都做到七成。

| 范围 | 候选处理 | 保留的必要东西/冲突 |
|---|---|---|
| 对等完整Descent首发 | 延后 | 内部Lab验接缝；与源双模式基线冲突待批准 |
| Public Forge/完整TC/复杂Editor | 延后公开冻结 | Mod Loader、ContentPackage、Steam Workshop运输层与基础SDK接口已成为当前技术基线；完整作者工具仍需按真实需求成长 |
| 自由TPS完整生产品质 | 候选延后 | 源Camera Canon未被自动删除，需独立批准 |
| 5kAI/50k弹体 | 仅torture工具 | 真玩法规模按需求；不营销承诺 |
| 任意anatomy内容广度 | 先具体部位破坏 | 内核不硬编码人形，不先造万能编辑器 |
| 多Storyteller/Daily/大Mutator系统 | 延后 | 单一可复现Director与profile边界 |
| Streamer专用HUD/复杂EmergenceScore | 延后产品化 | 玩家战报与基础回放时间线保留，直播专用分析不混入首发 |
| 高策略Bots/公共50人Hub | 不作为当前范围 | Solo无Bot成立，Bot有限明确命令 |
| 所有家族大量武器 | 先一个明确战斗强项 | 四近战可试制，生产数量由差异与成本定 |
| 完整长主线过场 | 延后大演出 | 唯一中央因果、任务动作、少量关键序列 |
| 同时建设多种商店/UGC/托管产品 | 不做 | 当前只卖Steam、公开Mods只走Workshop；代码边界保持Provider解耦即可，不实现未来平台 |

一个模板和少数变体可以当强切片，不能未经内容消费测试就称最小可卖产品。枪、敌人、房间数量由实测制作速度和复玩数据决定；原30Relic池作为Lab验证集合，不强塞Operation首发。免费持续更新与无Paid EA需要更保守范围，不从原则推出“总能做完”。

## 遥测、研究与工具

PLAN-006 · DIRECTION · 来源：SRC-SSOT-2.0 §31。
Build Evolution Timeline记录Anchor/Connector/Fusion/Loop/Pivot/GodBuild；Steam Timeline/clip可标FirstFusion/cascade/world chain/reversal/LastChance/team combo并回溯root cause。EmergenceScore为TEST工具，按topology/loop/cascade/multikill/world/cross-player筛选，不能只按DPS。

PLAN-007 · PROPOSED · 来源：本轮研究方法。
最小事件：session_started/ended、mode+packagehash、room_enter/exit、objective_commit、cart_commit、support_commit、resource_transfer、modification_install、fusion_commit、ordnance_pick/drop/deplete、downed/revive/wipe、knowledge_upload、disconnect/migration。只收伪名session/seat、操作类型、耗时、版本和结果原因；不默认raw voice、聊天全文、平台秘密。保留期候选30天，外测告知/同意/删除机制在上线前确定；当前没有采集真实用户数据。

研究提问固定：“刚才发生什么”“你为什么做这一步”“下次会怎么变”“愿意自己再开吗”；不先向玩家讲设计的正确答案。记录正反证据，招募来源与熟练度分层。文档/系统数量不得写成体验进度百分比。

## 本轮文档 Validation / Testing Policy

PLAN-008 · PROPOSED · 来源：实施包验收合同。
文档任务不运行代码/游戏测试。实际检查一次：核原件SHA；将源所有顶层标题与source-map逐项比对；检查相对链接、文档ID/规则ID/状态与无来源CANON；人工走读无通用Alarm/无gameplay checkpoint/无强制回跑/无硬撤离表/Staff占武器槽/源自动消费Fusion/合法Proc loop/默认0友伤/公共物资/单一时间线。新增“总览”命名，禁用旧称。

本轮结构检查结果由交接报告提供，独立verifier尚待完成。任何失败只做一次针对性修复后重跑失败检查，不反复扩展整套验收。后续游戏Gate均不在本轮运行。

## 决策和停止条件

PLAN-009 · PROPOSED · 来源：本轮制作治理。
若三个月仍需要解释很多系统才能让玩家理解为何重开，先减少认知/菜单，而非加剧情和奖励。若六个月还没有可读、稳定、可复玩的单一体验，停止首发承诺并做明确转向决定。需要用户决定的事项由[决策总览](../governance/decision-register.md)拥有；只将已确认唯一主线升级Canon，其他评审推荐不替用户做最终选择。
