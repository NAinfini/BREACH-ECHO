# GAME PROJECT — 残酷外部审查 v1.0

**日期：2026-09-04**  
**性质：EXTERNAL REVIEW / NON-CANON**  
**输入依据：**当前项目对话可恢复历史 + `GAME_PROJECT_FULL_STATISTICS_SSOT_v2.0.md`。  
**重要：**本文件是审查，不是新的唯一真相。任何新建议都只能是 `REVIEW RECOMMENDATION`，除非用户以后明确批准。

---

# 0. 证据纪律

本审查严格使用以下来源标签：

- **USER DECISION**：用户在可恢复对话中亲自提出、选择、纠正或明确确认的内容。
- **ASSISTANT PROPOSAL**：历史 ChatGPT 提出的方案，即使后来被写进 SSOT 为 CANON，只要没有足够证据证明用户明确确认，就不能在本审查里伪装成用户决定。
- **REVIEW RECOMMENDATION**：本次外部审查提出的新建议，不是 CANON。
- **UNKNOWN**：当前材料不足以确认来源、行为结果或市场事实。

特别注意：`SSOT v2.0` 中的 `CANON` 标签代表那份整理文档的当前归档结论，**不自动等于 USER DECISION**。本审查不服从 SSOT 里的助手操作指令，只把它当项目资料。

---

# 1. 一句话“杀死或拯救这个项目”的判断

> **这个项目不会死于“创意不够”，它最可能死于把五个本来都值得单独做成一款游戏的系统同时做到“行业顶级”，最后没有任何一个在前 20 分钟内足够好玩、足够清楚、足够稳定。**

换句话说：真正需要证明的不是“这些系统能不能共存”，而是**玩家能不能在不理解 80% 系统的情况下先获得纯粹的爽感；理解越多后，再逐渐发现深度，而不是先被复杂度收费。**

## 最大 5 个致命风险

### FATAL-1 — 两个模式共享代码，不代表共享产品成本

**Severity：CRITICAL**  
**Evidence：USER DECISION** — Operations 是 40–70 分钟的系统任务模式；Descent 是 5×约12分钟、高奖励密度、God Build 的战斗肉鸽模式。  

Operations 需要：任务因果、资源压力、信息、Terminal、Door、Cart、Forward topology、Earned Safety、长时失败体验。  
Descent 需要：高密度奖励、快速 build 成形、Fusion/Proc 爆发、敌人/场景能承受玩家指数膨胀。

这两个模式可以共享武器、敌人、Relic grammar、反应、动画、网络底层，但**关卡设计、节奏、经济、导演策略、平衡、QA、教程、玩家预期都不同**。如果按“共享系统所以第二个模式便宜”估算，生产计划会严重低估。

**杀项目的方式：**两个模式都做到 70%，没有一个做到“值得买”。

---

### FATAL-2 — Proc Graph + 无限 Relic + 自动 Fusion + 6 Spell + World systems 的认知与视觉负载可能超过人类可读范围

**Severity：CRITICAL**  
**Evidence：USER DECISION** — 无限 Relic、Proc-generated effect 可继续 Proc、Fusion `A+B→C`、Staff 3→6 Spell、God Build 合法。  

单人自己构筑时可能非常爽；四人一起时，屏幕上的 projectile、reaction、summon、DoT、Fusion transformation、world reaction 会乘四。系统越成功，越有可能把自己的反馈系统摧毁。

**杀项目的方式：**玩家不是因为深，而是因为“我根本不知道发生了什么”离开；主播观众更糟，只看到粒子汤。

---

### FATAL-3 — Operation 的“长局 + 真失败 + 稀缺共享资源 + 不可逆团队决策”与随机匹配天然敌对

**Severity：CRITICAL**  
**Evidence：USER DECISION** — Operation 可真正失败、无 gameplay checkpoint；约40–70分钟；Supply 公共；Cart 可不可逆；失败只保留 Banked 知识等并降低代币。  

这套东西在固定四人好友队里能制造故事；在 Quick Match 里会制造：抢资源、乱花 Support、乱 Commit Cart、离队、AFK、带错 loadout、沟通失败、最后 50 分钟白打的归因冲突。

**杀项目的方式：**Steam 评价出现“朋友一起神作，单排垃圾”，而公开匹配人口因此萎缩。

---

### FATAL-4 — 技术野心明显超过“为了好玩所必需”的规模

**Severity：CRITICAL**  
**Evidence：ASSISTANT PROPOSAL / UNKNOWN provenance for some items** — SSOT 包含 1k/2.5k/5k AI stress、10k/50k projectile、任意 AnatomyGraph 0..N、player-hosted authoritative + host migration、Steam Deck 不减少 canonical outcome、TC/Workshop/Scenario Forge、snapshot+journal、semantic RNG 等。

这些单独都可以合理；全部一起会把团队变成引擎公司。尤其 5k AI、任意动态 anatomy、host migration、God-build deterministic replication 和 Steam Deck 同时要求时，技术架构会反过来绑架设计。

**杀项目的方式：**两年都在“为未来扩展正确地搭架构”，而没有一个可卖的房间。

---

### FATAL-5 — 市场上目前还没有一个能一眼识别的“产品表面”

**Severity：CRITICAL**  
**Evidence：UNKNOWN / SSOT itself marks Visual DNA OPEN**。  

玩法底层很有区分度，但玩家在 Steam 列表页不会读 Proc Graph 白皮书。他们先看 capsule、截图、10秒 trailer、敌人、武器、场景。现在 First Builder / Fold / Resonance / JANUS 还是词，不是视觉品牌。

**杀项目的方式：**真正有独特系统，但商店页看起来像“另一个合作科幻 FPS Roguelite”。

---

# 2. 谁会爱、谁会恨、谁会退款、谁会玩 100 小时

## 2.1 新手

### 可能会爱
- **USER DECISION**：枪械换枪快、PvE recoil 易控、无 Relic 时也要求武器好玩。
- **USER DECISION**：Operation 不把开枪视为犯错；比 GTFO 更允许正常战斗。
- **USER DECISION**：方向码 Support、怪物声学 Horde 预警、物理世界交互，容易制造第一小时记忆点。

### 可能会恨
- 2 Weapon + 2 Utility + Signature Active + Quick Melee + Ping + Staff spell wheel + Support sequence + Terminal + resource economy 同时出现，教程会过载。
- 一上来就出现 Knowledge、Scrap、Support、Power Cell、Relic、Spell、Fusion、Proc、Reaction 等名词，会让玩家在还没爱上射击前先读系统。

### 最可能退款的瞬间
1. 第一局前20分钟还在查 Terminal/捡资源，没有足够爽的战斗。
2. Staff/Utility/Support 输入“看起来复杂，但效果没比直接开枪爽”。
3. 第一场长 Operation 失败后觉得“我刚才一个小时到底得到了什么”。

### 玩100小时的条件
- 前10分钟就能纯靠射击/移动/近战爽；
- 第2–5小时才逐渐发现 Proc/Fusion 深度；
- 失败不会抹掉理解与发现；
- 每次 Operation 的局势差异是真实玩法差异，而不是换房间顺序。

---

## 2.2 核心系统玩家 / Build 玩家

### 可能会爱
- **USER DECISION**：Proc 能继续 Proc；合法 loop 不被统一禁掉。
- **USER DECISION**：Fusion 消耗 A/B 生成真正的 C，并可继续 Fusion。
- **USER DECISION**：无限 Relic，Descent 允许 God Build。

### 可能会恨
- 自动 Fusion 把“我的 build”改成“系统替我决定的 build”。
- 规则如果靠 Wiki 才知道 SourceScope、Zone、inheritance，深度会变成文档税。
- 如果为了可读性最终偷偷 cap proc depth/敌人数量，核心玩家会直接看穿设计承诺失信。

### 最可能退款/差评的瞬间
> “我捡了最后一个 ingredient，系统自动吃掉两个我喜欢的东西，给了一个我不想要的 Fusion。”

### 玩100小时的条件
- 可以理解、预测、操纵 graph；
- 每个极端 build 的形成过程可复盘；
- Fusion 有足够多“改变拓扑”的结果，而不是高级版 +damage；
- Build diversity 不是靠海量垃圾词条。

---

## 2.3 四人好友队

### 可能会爱
这是当前设计最强的受众。好友队能把稀缺资源、Support、Cart、Last Wind、Door、Horde、奇怪 Fusion 变成共同故事。

### 可能会恨
- 一个玩家永远当“Terminal 操作员”；
- 一个玩家拿了最强 Relic/Fusion 后清场，其他三人变观众；
- 一个玩家乱花最后一个 Support Charge；
- Cart 的不可逆 Commit 引发真实争执；
- 物理 Ammo 管理比打怪花更多口水。

### 玩100小时的条件
- 队友之间不是角色职业税，而是“互相放大”；
- 每人都有可见贡献；
- 失败后队伍讨论的是“下次换策略”，不是“谁毁了这局”。

---

## 2.4 随机匹配玩家

### 这是目前最危险的用户群

**USER DECISION**：公开 Quick Match、公共资源、无 mandatory class、团队 voice/ping 方向存在。  
**UNKNOWN**：这些社交规则是否经过任何真实玩家测试。

随机队不共享语境。一个好友队觉得“有趣的争论”，在 Quick Match 里就是 friction。

最危险场景：
- 新手拿走公共 Heavy；
- 有人把唯一 Cell 投到自己想开的 Vault；
- 有人拒绝走；
- 60分钟末段主机/玩家退出；
- 不语音玩家被默认当“不配合”；
- 高级玩家把地图/构筑全解了，新手只跟跑。

### 退款原因
> “游戏不是难，是队友能毁掉我一小时。”

### 玩100小时的条件
- 所有核心协作都能 Ping/Quick Chat 完成；
- 稀缺资源的恶意/误用成本有限；
- Public Match 的规则比 Private Match 更防 grief；
- 离队/backfill/reconnect 不让一局直接报废。

---

## 2.5 单人玩家

### 可能会爱
- 系统实验不被队友打断；
- 可以慢慢理解 Terminal、Build、World state；
- 高技术 Melee/Staff 玩家会有很强 mastery。

### 可能会恨
- 如果 Operation 任务本质按“有人操作 Terminal、其他人 cover”设计，Solo 会变成暂停式工作。
- Bots 如果只是“跟着射击”而不会理解 Door、Cart、Support、资源价值，就无法替代合作。
- Bots 如果真要理解所有这些，又会成为一个独立大项目。

### 退款原因
> “商店说1–4人，实际上1人只是少三个真人。”

### 玩100小时的条件
- Solo 的 encounter geometry、interaction concurrency、resource profile 真正调过；
- Bot不是强制；无Bot也能完整通关；
- 需要同时操作的任务自动改为 sequential solution，而不是让 AI 替你按按钮。

---

## 2.6 主播与观众

### 可能会爱
- First Fusion、Last Wind、Proc cascade、Predator reversal、Support出错、世界连锁都天然有剪辑点。

### 可能会恨
- “主播自己很爽，观众看不懂为什么爽”。
- God Build 后画面全是粒子，敌人进场即死，没有戏剧张力。
- 60分钟前45分钟都在铺垫，真正的 build payoff 太晚。

### 玩/看100小时的条件
- 观众能在3秒内看出玩家 build 的核心身份；
- 大型 proc 有因果可视化，不是数字瀑布；
- 一局里有多个中型高潮，而不是只在末尾爆一次。

---

# 3. Operations 与 Descent：互补，还是两款游戏硬缝

## 3.1 真正可以共享的部分

**Evidence：USER DECISION / project direction**

可以高比例共享：
- movement / input；
- Weapon families；
- melee/staff/energy 基础手感；
- Enemy assets/behaviors；
- damage/status/reaction；
- anatomy/parts；
- Relic tags / Proc runtime / Fusion runtime；
- animation/VFX/audio primitives；
- networking/account/save 基础；
- 部分 room kit / biome kit。

这些是合理的共同地基。

## 3.2 不能假装共享的部分

| 维度 | Operations | Descent | 冲突 |
|---|---|---|---|
| 核心节奏 | 探索→信息→决定→局部战斗→后果 | 高频战斗→高频奖励→快速膨胀 | 同一 encounter pacing 不可直接复用 |
| 资源 | 稀缺、长期持续 | abundant、快速补 | weapon 价值完全不同 |
| Relic | 少、改变解决方式 | 多、主成长轴 | item balance 要做两套 profile |
| Fusion | 稀有记忆点 | 高频正常语言 | recipe pacing 两套 |
| Director | 尊重 Earned Safety | 需要持续 combat payoff | spawn policy 冲突 |
| 地图 | Curated forward problem | 层式 combat spaces | authoring grammar 不同 |
| 失败心理 | 40–70分钟任务失败 | 肉鸽失败预期更高 | retention/奖励包装不同 |
| Tutorial | 教设施/资源/任务 | 教构筑/增长 | onboarding 不能共享一套 |
| Matchmaking | 规划/协商重 | 更容易drop-in式战斗 | 公共队预期不同 |

## 3.3 最大范围灾难

**ASSUMPTION：**如果每个 Weapon/Relic/Enemy 都必须在两种模式中同等“完整”，QA矩阵至少是乘法增长，而不是加法增长。

例如一个 Energy weapon 在 Operation 要验证：
- 是否破坏 ammo scarcity；
- Heat sink价值；
- 40–70min sustain；
- Support economy。

同一把在 Descent 又要验证：
- 10分钟内是否能形成 build；
- 高 proc rate 下是否过热机制变成废词条；
- Layer 5 是否能承受指数增长。

**REVIEW RECOMMENDATION：**把“共享系统”明确分成三层：
1. **Shared Runtime**：必须共享；
2. **Mode Profile**：允许不同 tuning / reward / director；
3. **Mode-exclusive Content**：允许存在，不强求100%跨模式合法。

如果项目坚持“所有内容必须两边都同样适配”，这是错误的纯洁主义。

## 3.4 外部审查结论

**它们可以互补，但目前还没有证明“第二模式的生产成本低于第一模式的50%”。**

只有满足以下条件才算成功互补：
- 至少70%的 Combat content 不需要 mode-specific 重做；
- 两模式各自有清楚的一句话玩家动机；
- 玩家在测试后能说出两个不同的“我为什么想再开一局”；
- 同一个系统在两模式中的规则变化不需要玩家重新学一整套游戏。

否则应视为两个产品。

---

# 4. 逐项烤系统

# 4.1 Combat Feel

**Evidence：USER DECISION** — PvE-first、快速 swap、易控 recoil、裸武器必须好玩。  
**问题：**目标同时要求 Gun、Melee、Staff、Energy、Heavy 都“裸装就值得玩”，相当于一次做五套高品质 combat languages。所谓“best-in-class”如果平均分配资源，会变成五套“不错但没一个顶”。

**最危险假设：**玩法广度不会稀释动画、音频、hit reaction、enemy response、camera、controller polish 的资源。

**REVIEW RECOMMENDATION：**先定义一个“Combat Crown Jewel”。例如枪械+近战是首发必须行业级；Staff/Energy 可以系统深但 content breadth 少。不要在生产计划里给五类同等宽度。

---

# 4.2 Character / Weapon / Utility

**Evidence：USER DECISION** — 2 Weapon、2 Utility、1 Signature Active；Staff占正常Weapon slot；Character不是硬职业；用户自己指出Active在Operation里可能奇怪，但同意先试Aegis/Breaker/Echo。

问题：
- “Soft Archetype + 所有人都能用一切”容易让 Character 变成皮肤+Q技能；
- Active若很强，变Hero Shooter；若很弱，角色没有身份；
- Utility与Spell、Relic、Support都在争“额外战术按钮”的认知位置。

**REVIEW RECOMMENDATION：**Character 的身份必须至少有一个**始终可感知的被动/规则偏置**，但不能是永久数值税。Active只是身份的一部分，不应该承担全部差异。

---

# 4.3 Relic / Proc Graph / Fusion

这是最有潜力同时也是最容易自爆的系统。

### 风险A：无限Relic不等于无限有趣
后期如果大量 relic 只是+8%类，会变成不可读的统计垃圾；如果全部是规则改写，则组合爆炸速度超过QA能力。

### 风险B：自动Fusion可能破坏玩家所有权
**USER DECISION**：合法recipe满足后自动发生，A/B消失生成C。  
这提供惊喜，但也会制造“我没有选择毁掉这个build”的负面瞬间。

### 风险C：Proc-from-proc四人局会吞掉因果
单人Noita式递归能读，四人同时递归未必能读。

### 风险D：God Build会吞掉队友乐趣
一个玩家如果杀死所有目标，其他人的合法强build没有机会发生。

**REVIEW RECOMMENDATION：**不要先问“最大proc depth多少”，先定义三个可读性预算：
- 每个玩家同时可见的**核心build identity节点**；
- 屏幕同时高优先级effect数量；
- 同一AttackRoot的反馈聚合规则。

技术层可以无限，呈现层必须有限。

---

# 4.4 Mission / Terminal / Support / Cart / Door / Earned Safety

这组东西单看都合理，放一起可能让Operation变成“系统操作员模拟器”。

### Terminal
物理地点+信息价值是好的，但**三名队友站旁边等一个人看GUI**是现实风险。

### Support
方向码有记忆性；但一局只有2–3个Charge时，玩家可能永远不会形成Helldivers式肌肉记忆，只觉得每次都要输入小密码。

### Cart
**USER DECISION**：小整数budget、多选、任意operator直接commit、非免费反悔。  
好友队：可能是有趣争论。Quick Match：可能是grief按钮。

### Door / Earned Safety
玩家如果找到一个最优“封两个入口、守一条走廊”的meta，所有 systemic promise 会坍缩成 bunker defense。

**REVIEW RECOMMENDATION：**每个Operation Template最多让**两套战略系统成为主角**。例如 BLACKSTART 可以是 Terminal+Power Cart；Door/Earned Safety作为支撑。不要每张任务同时要求Terminal、Support、Cart、Door、Transit、Vault、Power、Horde全部高频。

---

# 4.5 Enemy / AI / Director

**Evidence：mixed; many details appear ASSISTANT PROPOSAL unless user provenance is recoverable.**

最大问题不是“AI是否聪明”，而是敌人能否给五种武器、四人协作、world systems、resource pressure提供清楚的对手语言。

风险：
- 追求5k AI会逼敌人简化；
- dynamic anatomy会消耗大量authoring与bug预算；
- Director被禁止“因为太安静就刷怪”后，如果world source设计不足，可能变得无法救节奏；
- 如果让Director通过“合法来源”做同样的暗箱操作，只是换皮，也会被玩家识破。

**REVIEW RECOMMENDATION：**先用6个Enemy Roles证明战斗生态，不要用数量证明技术。每个Role必须能回答：它迫使玩家改变什么？哪类武器/位置/团队行为自然好用？

---

# 4.6 Co-op / Bots / Social

当前系统明显更适合四人熟人队，而不是随机队。

公共物资、Shared Draft、Cart commit、Support charge、物理 ammo、长局失败，全都需要社会协议。

Bots 是额外风险：
- 简单Bot无法处理系统；
- 真正懂系统的Bot成本极高；
- Bot若太聪明，会替Solo玩家做最有趣的判断。

**REVIEW RECOMMENDATION：**先把“无语音随机队”当最高难度UX测试，而不是拿好友队证明co-op成立。Bots只承担移动、射击、救人、明确Ping命令，不做战略优化。

---

# 4.7 长期进度

**Evidence：SSOT marks horizontal progression; provenance partly UNKNOWN.**

优点不需要表扬。风险很具体：没有永久power后，很多玩家会觉得“60分钟之后账户没变强”。如果永久解锁又大量扩充Relic/Spell pool，反而可能产生**解锁越多，build越稀释**的反向奖励。

**REVIEW RECOMMENDATION：**永久进度必须明确分成：
- **Breadth unlock**：新玩法；
- **Knowledge unlock**：理解/记录/recipe信息；
- **Mastery/status**：记录、挑战、cosmetic；
- **Never dilute without control**：解锁新物品不能永久把玩家喜欢的pool污染到无法控制。

---

# 4.8 Narrative

目前是“名词很多，人的动机少”。First Builders、JANUS、Breach、Machine Secession、Pale Bloom、Great Schism、Necropolis、Fold、Bastion都可以有深度，但如果第一小时玩家记不住谁是谁，这些只是百科名词。

**USER DECISION**：Sacred Timeline、核心谜团可解决但宇宙不完全解决、Final Revelation后世界继续。  
**UNKNOWN**：玩家具体是谁、为什么个人上关心这些、JANUS与玩家的情感关系、Descent为何真实存在。

**REVIEW RECOMMENDATION：**Phase 0不是先写全历史，而是先写四句话：
1. 玩家每天具体干什么；
2. 玩家为什么不能不干；
3. 玩家最初相信什么；
4. 结尾玩家发现自己一直误解了什么。

如果四句话不强，100页时间线没用。

---

# 4.9 Visual DNA

这是当前最严重的产品空白之一。

**UNKNOWN**：没有证明 First Builder、Fold、Resonance 在一张无Logo截图上可识别。

**REVIEW RECOMMENDATION：**不要先做“Visual Bible文字”。先做3张关键帧测试：
- 普通Human/JANUS Facility；
- First Builder intrusion；
- Descent high-resonance catastrophe。

把Logo和HUD去掉，让10个没看过项目的人看5秒。如果多数人说“generic sci-fi”，就失败。

---

# 4.10 Audio / HUD / Accessibility

Horde通过怪物叫声预告是**USER DECISION**。方向合理，但四人Proc+枪声+音乐+语音会导致声音掩蔽。

HUD最大风险：
- Damage numbers；
- Status；
- Relic identity；
- Spell；
- Objective；
- Team resource；
- Door/Cart state；
- proc feedback；
全部合法，但同时展示会死。

**REVIEW RECOMMENDATION：**战斗HUD只显示“现在要行动的信息”；构筑因果放在Build/Recap层。不要试图实时把Proc Graph完整展示给玩家。

Accessibility也不能被当作“最后加Settings”。Support方向输入、audio telegraph、颜色无关识别、camera shake都直接影响系统设计，必须早测。

---

# 4.11 Network / Performance / Mod

这是当前最容易工程失控的部分。

### Host migration
60分钟长局确实需要韧性，但 player-hosted authoritative + live migration +大量AI/Proc/动态part 是非常昂贵的组合。

### Steam Deck
如果“canonical outcomes完全不减少”与5k AI/God-build极限同时成立，Deck目标可能直接把PC设计上限锁死。

### Mods / TC / Demo Workshop
把TC、Workshop、完整mod runtime提前做成首发级，会要求：
- stable schema；
- sandbox/security；
- package/version/dependency；
- save compatibility；
- network compatibility；
- content validation；
而这些都是在核心玩法尚未稳定时最容易返工的层。

**REVIEW RECOMMENDATION：**首发只承诺“data-driven content pipeline + internal extension points”。Public Workshop/TC等核心玩法稳定后再冻结API。不要为了未来modder稳定而让自己在pre-alpha就背兼容债。

---

# 4.12 商业 / Steam

**Evidence：USER DECISION / earlier project direction** — Premium B2P、无battle pass/premium currency/FOMO、Steam-first。  
这不是风险本身。风险是：项目又要求无Paid Early Access，又要求大规模1.0质量、双模式、Steam Deck、Mod、网络韧性。

**REVIEW RECOMMENDATION：**如果坚持不Paid EA，就必须更狠地砍首发scope，并把Steam Playtest/Demo当真正产品验证，不是营销仪式。

商店页第一卖点不能是“Proc Graph”。应该先卖一个清楚可见的fantasy和combat loop，Proc Graph是玩家点进来后发现的深层理由。

---

# 5. “写起来很酷，玩起来可能很糟”的设计清单

## 5.1 认知过载

**Severity：CRITICAL**  
**Evidence：USER DECISION集合**。  
一名Staff玩家可能同时管理：2 weapon、2 utility、active、3–6 spell、heat/mana/ammo、Support、Relics、Fusion、Objective、Terminal、Door、Team state。  
**Why it hurts fun：**玩家脑力花在记接口，而不是做战斗判断。  
**最小修正：REVIEW RECOMMENDATION** — 前30分钟只暴露核心战斗+一个世界系统；功能存在不等于同时教学。  

## 5.2 不可读Proc

四人×递归 proc 的成功状态就是信息灾难。  
**最小修正：**AttackRoot聚合、重要链路有独特形状/声音、详细因果放战后recap。  

## 5.3 队伍争执

Cart、Support、Shared Draft都是真资源决定。  
**最小修正：**非投票式预览/短broadcast、明确谁commit、最近行为日志；Private与Public可用不同social safety profile。

## 5.4 公共物资 grief

新手/恶意玩家能拿走Ammo/Heavy/Cell。  
**最小修正：**普通物资自由，高价值有短claim规则；稀缺mission-critical item不可被丢进无解位置。

## 5.5 40–70分钟失败挫折

**USER DECISION**：真失败，无checkpoint rollback。  
这能制造stake，也能制造退款。  
**最小修正：**banking必须在局中有节奏地发生，失败后明确展示“你保留了什么、学到了什么、为什么输”。

## 5.6 自动Fusion破坏构筑

**USER DECISION**：满足recipe后自动、消耗A/B。  
**最小修正：**最后ingredient拾取前必须明确显示“将消耗哪些已知资产”；未知只隐藏结果，不隐藏代价。

## 5.7 God Build吞噬队友乐趣

**USER DECISION**：合法God Build不nerf。  
**问题：**不nerf玩家不等于可以让其他三人没目标打。  
**最小修正：**通过战场拓扑、多front、不同任务动作、敌人role让强玩家扩大队伍能力，而不是单点把所有内容删掉。不要用隐藏抗build数值。

## 5.8 物理Ammo/资源摩擦

“把弹药丢地上”很有物理感，也可能变inventory housekeeping。  
**最小修正：**一键按family丢固定比例bundle、自动stack、无需打开背包。

## 5.9 无倒计时撤离可利用

**USER DECISION**：不做60秒硬timer。  
玩家可能在“明显该走”后继续搜刮/卡AI/刷proc。  
**最小修正：**后目标状态必须让继续停留**没有正收益**且空间真实恶化；不是隐藏秒杀timer，而是可见的world-state closure。

## 5.10 Terminal变成单人菜单

一个人在GUI，三个人等。  
**最小修正：**关键查询尽量10秒内，结果自动共享；复杂操作让队友在世界里同时做相关动作，而不是站岗。

## 5.11 Earned Safety变成永久龟壳

玩家可能找到通用最优 chokepoint。  
**最小修正：**不同Threat必须有真实capability改变安全边界，但不能Director作弊穿墙。

## 5.12 Support方向码变仪式摩擦

只有2–3次/Operation时，记忆收益可能不足。  
**最小修正：**测试“输入本身是否制造兴奋”；如果只是3秒税，应缩短或改为context pattern。Accessibility不能改变资源成本，但可简化输入。

## 5.13 Staff变成“无限弹魔法枪”

**USER DECISION**：Staff强调可持续、3→6 Spell。  
如果80%时间玩家只用最高DPS projectile spell，整个Spell系统失败。  
**最小修正：**首发3 spell必须是不同verb，不是不同伤害类型。

## 5.14 Energy压死Ballistic

**USER DECISION**：控Heat可近似无限续航。  
如果burst差距不足，Operation里理性玩家全带Energy。  
**最小修正：**让Ballistic在“现在必须马上杀掉它”上有显著优势，而非只是+10%DPS。

## 5.15 Horizontal progression缺乏动力

无永久数值成长能避免 grind，但也可能让大众玩家觉得“没进展”。  
**最小修正：**可见的Archive、Fusion discovery、挑战、角色/武器/Spell breadth与世界变化必须足够强。

## 5.16 Procedural Situation生成“技术合法但无聊”

规则图能通过validator不等于任务好玩。  
**最小修正：**生成器只重组被人工证明好玩的Situation blocks；不要程序生成核心任务逻辑本身。

## 5.17 TPS自由切换破坏FPS生产成本

**Evidence：ASSISTANT PROPOSAL/UNKNOWN provenance**。  
这要求更多动画、镜头、遮挡、瞄准、公平性、QA；对核心卖点帮助不明确。  
**最小修正：**Prototype前明确是否真的有用户需求，不要“既然框架能支持就做”。

## 5.18 5k AI成为技术自尊项目

数量不是乐趣。  
**最小修正：**先定义真实屏幕需求，再定benchmark。5k可以是torture，不应成为玩法承诺。

## 5.19 Dynamic Anatomy泛化过度

任意0..N肢体能力图很漂亮，也极易变成architecture astronautics。  
**最小修正：**先做3种具体敌人的part break，证明玩法价值，再抽象。

## 5.20 Demo就支持TC/Workshop

**Evidence：historical ASSISTANT PROPOSAL / USER confirmation provenance not fully recoverable.**  
这可能把公开API稳定成本提前到核心玩法之前。  
**最小修正：**Demo只需要官方内容+必要mod hook，完整TC不是市场验证前提。

---

# 6. 重要问题验证矩阵

> 下面的“最小修正”全部是 `REVIEW RECOMMENDATION`，不是CANON。

| # | 问题 | Severity | Evidence / Assumption | Why it hurts fun | 最小可验证修正 | Prototype test | 量化通过 / 失败标准 |
|---|---|---|---|---|---|---|---|
| 1 | 两模式范围乘法 | CRITICAL | USER DECISION + ASSUMPTION | 双倍节奏/经济/关卡/QA | 做同资产的15min Operation与12min Descent微切片 | 记录mode-specific重做工时 | PASS: ≥70% combat资产/代码无需重做；FAIL: <50% |
| 2 | 裸Combat不够强 | CRITICAL | USER DECISION要求裸装好玩 | 一切Build只是掩盖基础无聊 | 关闭Relic/Fusion | 30min arena session | PASS: ≥70%测试者主动愿意再打；FAIL: <50% |
| 3 | 认知过载 | CRITICAL | USER DECISION集合 | 玩家管理UI而非战斗 | 分阶段暴露系统 | 盲测首20min | PASS: ≥80%无口头帮助完成核心战斗+1次Utility；FAIL: <60% |
| 4 | Proc不可读 | CRITICAL | USER DECISION proc-from-proc | 不知因果，无mastery | AttackRoot聚合+核心节点summary | 四人高proc场 | PASS: ≥70%玩家能在10秒内说出主要触发链；FAIL: <40% |
| 5 | God Build吞队友 | CRITICAL | USER DECISION God Build合法 | 其他人没东西玩 | 多front/不同role，不nerf build | 1强3普通四人场 | PASS: 每名玩家≥70%encounter有可执行有效目标；FAIL: 任一人连续3场主要当观众 |
| 6 | 自动Fusion后悔 | HIGH | USER DECISION | 玩家失去build所有权 | 最终ingredient前明确消耗对象 | 20次未知/已知Fusion测试 | PASS: “因未理解消耗而后悔”<10%；FAIL: >20% |
| 7 | Staff魔法枪化 | HIGH | USER DECISION 3→6 spell | 6个slot实际只用1个 | 首3spell必须不同verb | 20min staff-only | PASS: 中位玩家主动使用≥2.5种spell/战斗段；FAIL: >70%输出来自单一spell且其余几乎不用 |
| 8 | Energy压Ballistic | HIGH | USER DECISION | ammo经济被绕过 | 明显burst/response差异 | 同样3类combat problem A/B test | PASS: 两类武器各有≥30%场景首选；FAIL: >70%玩家所有场景都选Energy |
| 9 | Melee四把同质 | HIGH | USER DECISION 4把 | content只是数值皮肤 | 每把绑定不同空间/防御verb | 无Relic melee course | PASS: 盲测玩家能根据场景合理换选择；FAIL: 1把在>60%场景统治 |
| 10 | Character Active像Hero Shooter | HIGH | USER DECISION “先试” | 破坏Operation语气/角色税 | 低UI存在感、verb型Active | Aegis/Breaker/Echo测试 | PASS: ≥70%说得出玩法差异且<20%认为某个任务“必须带某角色”；FAIL反之 |
| 11 | Terminal死时间 | HIGH | USER DECISION Terminal核心 | 3人等待1人菜单 | 查询短、结果共享 | 四人无语音Terminal段 | PASS: 单次常规查询中位<15s，队友无事可做时间<10s；FAIL: >30s |
| 12 | Cart争执/grief | CRITICAL for public | USER DECISION direct commit | 单人毁长局 | 全队broadcast+可追责UI，不强制投票 | 20场陌生人测试 | PASS: <10%场次出现负面争执/故意破坏；FAIL: >20% |
| 13 | Public supply抢夺 | HIGH | USER DECISION public | 队友能毁资源曲线 | 关键物品claim规则 | Quick Match scarcity test | PASS: <5%关键物资因误拿导致任务明显恶化；FAIL: >15% |
| 14 | 物理ammo麻烦 | MED-HIGH | USER DECISION | 资源管理变家务 | 一键bundle/自动stack | 真实补弹交换 | PASS: 中位完成转交<4s；FAIL: >8s或频繁开菜单 |
| 15 | 40–70min失败挫折 | CRITICAL | USER DECISION | wipe后弃游 | 中途banking+清楚结算 | 末段wipe测试 | PASS: ≥50%测试者愿立即再开，≥70%认为失败“公平可理解”；FAIL: <30%再开 |
| 16 | No-timer extraction拖延 | HIGH | USER DECISION | farm/磨蹭/节奏泄气 | world-state真实关闭正收益 | 完成目标后自由行为观察 | PASS: 中位3min内主动撤离，<10%尝试稳定farm；FAIL: 中位>6min |
| 17 | Earned Safety bunker meta | HIGH | USER DECISION | 每局变一个choke | Threat capability+多合法front | 10次同模板 | PASS: 没有单一守点策略在>50%seed最优；FAIL: >70% |
| 18 | Horde预警不可读 | MED | USER DECISION声学 | 听不到就像随机刷怪 | faction cue层级 | 混音+语音四人测试 | PASS: ≥80%在视觉接敌前识别“大波来了”；FAIL: <60% |
| 19 | 横向进度无动力 | HIGH | current SSOT; provenance mixed | “打了没变强” | breadth/knowledge/mastery可见 | 10小时外部测试 | PASS: ≥60%能说出至少2个想继续追的永久目标；FAIL: <40% |
| 20 | Visual identity泛化 | CRITICAL market | UNKNOWN | Steam页无辨识度 | 3张无Logo keyframe | 5秒blind test | PASS: ≥70%能把三张识别为同一游戏且<30%说generic sci-fi；FAIL反之 |
| 21 | Narrative名词汤 | HIGH | USER DECISION部分 + OPEN | 玩家不关心真相 | 先锁4句player story | 首小时无Archive测试 | PASS: ≥70%能说清“我是谁/为什么来/当前目标”；FAIL: <50% |
| 22 | Host migration过重 | CRITICAL tech | ASSISTANT PROPOSAL/UNKNOWN | 技术延期、战斗状态丢失 | 先做最小live-state迁移 spike | active combat断host | PASS: 20次迁移≥19次<8s恢复且无任务/loot回滚；FAIL: <90%成功 |
| 23 | Steam Deck与极限sim冲突 | HIGH | SSOT target, provenance unknown | 被最低端硬件反向限设计 | 真机thermal soak | 30min worst-case slice | PASS: 99% frame time满足60fps（16.67ms）budget且无canonical删减；FAIL: 需要削核心玩法才过 |
| 24 | Mod/TC过早 | HIGH schedule | historical direction | API冻结拖慢迭代 | 内部data-driven、公开API延后 | 统计每月schema breaking changes | PASS: 核心schema连续8周稳定后再public；FAIL: 仍每周breaking却要兼容 |
| 25 | Procedural合法但无聊 | HIGH | current design | replayability变随机走廊 | 人工Situation blocks | 20 seed blind ranking | PASS: ≥80% seed无“明显废局/空走”；FAIL: >15% boring/unfair |
| 26 | Support方向码是税 | MED | USER DECISION | 少量调用却重复输入 | 保留并A/B简化版 | 20次真实压力调用 | PASS: ≥60%称“紧张/有趣”，<15%称纯烦；FAIL: >30%称烦 |

---

# 7. 实际可维护的模块化 GDD 架构

不要把当前45章直接拆成45个长期文档。那会产生重复真相。建议用**9个设计文档 + 3个跨系统账本**。

## GDD-00 — Product Constitution & Evidence Ledger

**职责：**只放不能轻易变的产品合同和证据来源。

必须字段：
- One-sentence product promise；
- Target audience / anti-audience；
- Mode hierarchy：谁是主模式、谁是次模式；
- 5条不可违反设计原则；
- USER DECISION / ASSISTANT PROPOSAL / REVIEW RECOMMENDATION provenance；
- Canon change log / supersedes；
- Kill criteria：什么结果会让项目转向/砍模式。

## GDD-01 — Player Combat & Controls

必须字段：
- Movement states；
- Weapon swap/animation cancel contract；
- Gun/Melee/Staff/Energy/Heavy verbs；
- input matrix keyboard/controller；
- aim assist；
- hit feedback；
- damage/revive states；
- baseline numbers只放测试范围，不放永久散落数值；
- No-Relic acceptance tests。

## GDD-02 — Build Algebra

必须字段：
- Relic taxonomy；
- Stat zones；
- Proc event schema；
- SourceScope；
- recursion/progress-gate规则；
- Fusion lifecycle、inheritance、discovery；
- Spell progression；
- readability budgets；
- multiplayer contribution attribution；
- performance budgets；
- 30件测试pool清单。

## GDD-03 — Operations

必须字段：
- 5分钟/15分钟/整局节奏图；
- resource budget；
- Encounter grammar；
- Terminal/Support/Cart/Door职责边界；
- Earned Safety状态机；
- public-match grief rules；
- failure/banking；
- template authoring contract；
- BLACKSTART完整beat sheet；
- Operation-specific content budget。

## GDD-04 — Descent

必须字段：
- Layer pacing；
- reward cadence；
- build guarantee；
- resource profile；
- objective pool；
- enemy scaling原则；
- Layer 1→5 transformation gates；
- Endless规则；
- 与Operation共享/独占内容表。

## GDD-05 — Enemies, AI & Living World

必须字段：
- Enemy role matrix；
- senses/communication；
- horde source；
- Director legal actions；
- door/ingress/terrain interactions；
- faction rules；
- anatomy/part damage只记录有玩法价值的能力；
- target active enemy counts；
- AI LOD / cohort策略；
- “不得作弊”的玩家可验证规则。

## GDD-06 — Co-op, Social & Solo

必须字段：
- resource ownership；
- irreversible team decision governance；
- voice/ping/quick-chat覆盖表；
- join/leave/backfill/reconnect；
- host loss体验；
- solo difficulty transforms；
- bot权限/禁止行为；
- grief surfaces；
- public vs private session差异。

## GDD-07 — World, Narrative & Content Bible

必须字段：
- 玩家身份/动机；
- Sacred Timeline；
- First Builders/JANUS等因果；
- Operation/Descent canon；
- Main story spine；
- Final Revelation；
- post-ending state；
- Forbidden hierarchy；
- Character narrative rules；
- lore→gameplay hooks；
- 每个名词第一次玩家何时、如何知道。

## GDD-08 — Presentation Bible

包含 Visual + Audio + HUD + Accessibility，而不是四份互相打架的文档。

必须字段：
- shape/material/color-independent language；
- 3类核心空间keyframe；
- weapon/spell silhouettes；
- VFX readability budget；
- audio priority hierarchy；
- horde cue grammar；
- HUD information priority；
- subtitle/SDH/haptics parity；
- low-vision/colorblind/motion/controller requirements。

## GDD-09 — Technical Product Contract

必须字段：
- engine decision criteria；
- authority model；
- network state ownership；
- save/journal；
- host migration是否首发；
- performance budgets based on actual gameplay；
- projectile/AI/anatomy targets；
- Steam Deck contract；
- mod extension boundaries；
- deterministic/debug tooling；
- telemetry hooks。

## PROD-01 — Content & Scope Ledger

必须字段：
- 每个feature的owner；
- estimated cost；
- dependency；
- content multiplier；
- launch / postlaunch / cut；
- reusable percentage across modes；
- asset count、enemy count、weapon count、mission count。

## QA-01 — Prototype & Acceptance Matrix

必须字段：
- hypothesis；
- prototype；
- tester cohort；
- metric；
- pass/fail threshold；
- decision if fail；
- evidence link/video/telemetry。

## MARKET-01 — Positioning & Steam Package

必须字段：
- screenshot-level hook；
- trailer first10s promise；
- competitor overlap；
- why not GTFO/DRG/Rogue Core/Far Far West；
- pricing assumption；
- demo purpose；
- store tags；
- audience rejection criteria；
- wishlist/playtest conversion metrics。

---

# 8. 如果只有12个月 + 小团队：必须砍什么

下面是 `REVIEW RECOMMENDATION`，不是用户决定。

## 8.1 首先砍“第二个完整产品”，不是砍一点点每个系统

**建议：Operations作为首发唯一完整模式；Descent只保留内部3-Layer prototype，是否首发取决于180天验证。**

原因：Operations目前提供最强差异化；Descent如果只做半成品，会直接和更成熟FPS roguelite正面比较。

如果180天后Operations不成立、Descent明显更好，再反过来pivot。现在不能承诺两个都一定1.0首发。

## 8.2 12个月直接砍/延后的内容

1. **自由TPS切换** → 首发只FPS。
2. **Public Scenario Forge** → post-launch。
3. **Total Conversion首发支持** → post-launch。
4. **Demo完整Workshop/TC** → 取消首发要求。
5. **5k AI作为玩法目标** → 保留torture benchmark，真实slice按需要定。
6. **任意0..N动态Anatomy作为普遍框架卖点** → 只做具体敌人part break。
7. **Storyteller多persona、Daily、Mutator大系统** → post-launch。
8. **Streamer HUD / EmergenceScore / Steam Timeline深集成** → 只留事件hook，产品化延后。
9. **Community Dedicated + Future official dedicated同时建设** → 先选一种launch hosting路径。
10. **完整Bots战略AI** → bots只做跟随/射击/救人/明确命令，或首发无bot但Solo真调平。
11. **4把Melee全部production品质** → prototype做4把，首发若资源不足保留2把最有差异的。
12. **30 Relic不降，但只做6–10个真正拓扑改写；其余保持简单高可读。** Build系统需要量，不要用100件填充。
13. **Staff 6个spell capacity保留规则，但首发spell总pool必须可控。**
14. **完整长主线过场** → 只做可落地的story spine与少量高价值sequence。
15. **Steam Deck“所有极限状态完全同表现密度”** → 保留canonical结果原则，但presentation可以激进LOD；若simulation仍不过，必须重新评估真实enemy/proc上限。

## 8.3 12个月最小可卖产品轮廓

- 1个完整Operation Template + 2个明显变体/seed profile；
- 1个真正有视觉身份的Facility kit；
- 3 Characters（若Active验证成立）；
- 4–6枪；
- 2 production melee；
- 1 Energy family；
- 1 Staff family + 6–9 total spells；
- 2 Utilities起步再扩；
- 20–30 Relics；
- 4–6 Fusions；
- 6核心Enemy roles + 1 major threat；
- 1完整Horde ecology；
- BLACKSTART级别完整任务；
- Friends/Private co-op优先；Public Quick Match只在社交测试通过后开放；
- 横向Archive/Discovery；
- 完整Visual/Audio/HUD语言；
- 不承诺UGC工具产品化。

这仍然很大。

---

# 9. 30 / 90 / 180 天验证顺序

# Day 0–30：证明“人在没有系统说明书时也想继续打”

### 只验证
- movement；
- AR + Shotgun；
- Sword + Hammer；
- 1 Energy；
- 1 Staff + 3 spells；
- 1 Utility；
- 3 Enemy roles；
- 1个极简Active原型；
- 灰盒；
- 4人基础网络，不做完整host migration；
- 3套Visual keyframe，不做production asset。

### 必须回答
1. 裸Combat是否成立？
2. Staff是不是魔法枪？
3. Energy是否压Ballistic？
4. Melee是否值得占Weapon slot？
5. Active是否破坏Operation语气？
6. Visual方向有没有非generic候选？

### Kill gate
如果外部测试者在30分钟后没有明显“再来一局”意愿，**禁止进入Build系统大制作。**

---

# Day 31–90：证明Build与Co-op不是互相污染

### 增加
- 10 Relics；
- 2–3 Fusions；
- proc-from-proc；
- 4人场；
- 1个10–15分钟mini-Operation；
- Terminal Search→Ping；
- 1次Support；
- 1次Cart；
- 1个Horde；
- 5 Enemy roles。

### 必须回答
- Proc可读吗？
- 自动Fusion会后悔吗？
- 一个强build会让其他人没得玩么？
- 无语音队能不能完成？
- Terminal/Cart是不是死时间/争执源？
- 资源共享是有趣协作还是家务？

### Kill gate
如果Quick Match-like无语音测试明显劣化，必须**重新设计公共资源/决策治理**，不能用“找朋友玩就好了”掩盖。

---

# Day 91–180：证明真正产品，而不是系统demo

### 制作
- BLACKSTART 30–40分钟近完整slice；
- 20–30 Relics；
- 4–6 Fusions；
- 6 Enemy roles；
- 完整Support/Failure/Banking；
- 真实Visual kit；
- 真实audio priority；
- Public/Private/solo各测试；
- Engine/network/performance spike；
- 可选3-Layer Descent prototype。

### 180天必须做的商业决定
不是“继续都做”。而是三选一：

A. Operations明确更强 → Descent延后；  
B. Descent明确更强 → pivot产品主模式；  
C. 两者都强且共享成本被数据证明 → 才正式双模式。

### Kill gate
如果180天时还不能用一段30秒无解释视频让陌生玩家看懂“为什么这游戏不同”，Visual/Product定位没有过关。

---

# 10. 20个最危险 OPEN 问题（按返工成本排序）

> 这里只列问题，不替用户拍板。

## 1. 首发到底必须同时包含完整Operations和完整5-Layer Descent吗？
这是最大scope开关。决定关卡、经济、UI、QA、市场定位和内容量。

## 2. 玩家身份与世界核心真相到底是什么？
First Builders/JANUS/Fold/Resonance之间的因果若后改，会返工任务、美术、音频、UI、角色、结局。

## 3. Visual DNA到底是什么？
Human/JANUS、First Builder、Fold、Resonance必须在资产生产前锁，不然所有正式asset可能重做。

## 4. Engine + authoritative network path是什么？
Unity/Unreal、player-hosted、host migration、dedicated-capable会决定系统架构。

## 5. “真正同时活跃的敌人规模”是多少，而不是torture数字？
这决定AI、动画、音频、网络、Steam Deck、关卡尺度。

## 6. Proc Graph在四人God Build时的可读性与性能合同是什么？
如果不先定义，后面所有Relic/Spell都可能返工。

## 7. 自动Fusion到底允许多大程度改变/吃掉现有build？
用户已定自动Fusion，但“多大损失/哪些资产可消费/未知提示”仍决定玩家信任。

## 8. Public Quick Match如何治理不可逆团队决定？
Cart、Support、Heavy、mission cell、Relic draft谁能做什么，决定单排生死。

## 9. 40–70分钟Operation无checkpoint的失败心理目标是什么？
失败率、bank频率、代币、重开意愿必须量化。

## 10. Character为什么存在？
如果所有武器都自由，Signature Active是不是足够形成身份，还是应该有更深的Core偏置？

## 11. Staff/Spell在Lore与战斗中到底是什么？
它关系到Visual、资源、Fusion、角色、世界逻辑。

## 12. Operation一张任务里允许多少“主系统”同时占玩家注意力？
Terminal/Cart/Door/Support/Power/Transit/Vault若都重要，认知爆炸。

## 13. Descent的Layer reward cadence具体是多少？
12分钟一层已经定方向，但每层多少Relic/Spell/Fusion决定是否真能从Assemble走到Break。

## 14. Enemy roster的核心6–8个Role是什么？
不先定role，武器、AI、Horde、Anatomy都会漂。

## 15. Solo到底是“同游戏缩放”，还是有专门任务语法变体？
这决定Bots和任务交互成本。

## 16. 永久进度怎样避免“没有成长感”与“pool污染”同时发生？
横向解锁需要控制机制，否则越玩随机池越差。

## 17. No-timer Extraction最终的世界状态终止条件是什么？
必须既不出现任意秒杀timer，也不能让玩家无限拖/farm。

## 18. Public Mod/Workshop/TC在什么里程碑才冻结API？
过早做会拖死开发，过晚做会违背mod-first目标。

## 19. Steam Deck是首发硬承诺还是优化目标？
如果是硬承诺，必须现在参与所有性能预算；不能最后才发现核心sim过不去。

## 20. Demo到底卖哪个fantasy？
15–25分钟短Demo与40–70分钟Operation、60分钟Descent都不自然匹配。Demo必须证明一个清楚产品，不是把两个模式各剪5分钟。

---

# 11. 外部评审最终结论

当前项目的核心问题不是缺设计，而是**几乎每个设计都在要求成为“深系统”**。深系统之间不会自动相加，它们会争夺玩家注意力、团队沟通、屏幕空间、CPU、QA和内容预算。

真正需要保护的不是某个具体Feature，而是三件事：

1. **第一分钟的动作反馈**必须比系统说明更强；
2. **四人同时玩时，每个人仍然知道自己做了什么、队友做了什么、为什么成功/失败；**
3. **一个小团队能在有限时间内把至少一个模式做到完整，而不是两个模式都像有潜力的Early Prototype。**

如果这三条不通过，Proc Graph、Fusion、First Builders、5k AI、TC、Host Migration都只是昂贵的概念装饰。

这份审查不建议现在继续加Feature。下一步应把这里的验证矩阵直接转成 `QA-01 Prototype & Acceptance Matrix`，然后用30/90/180天的证据决定哪些系统活下来。
