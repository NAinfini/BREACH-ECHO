# GAME PROJECT — 全项目统计与唯一真相 SSOT v2.0

**状态：CURRENT CANON + OPEN/TEST 显式标记**  
**日期：2026-09-04**  
**用途：这是当前项目的全项目统计（Full-Project Audit）与唯一设计真相（Single Source of Truth）。从本版本起，旧聊天、旧 Architecture Bible、旧 SSOT v1.0、旧“锁定项”、草案和助手建议若与本文件冲突，以本文件为准。**

---

# 0. 权威规则、范围与证据等级

## 0.1 本文件到底统合什么

本文件不是单纯 Gameplay Design Doc，而是整个项目的 Preproduction Canon：

- 产品定位与为什么玩家会买/留下；
- 竞品/参考游戏，以及**具体学什么、明确不学什么**；
- Systemic Operations 与 Descent 两个核心模式；
- Input、Loadout、Character、Weapon、Melee、Staff/Spell、Energy、Heavy、Utility；
- Relic、Proc Graph、Fusion、Crit、Status、Reaction、God Build；
- Mission、Terminal、Support、Knowledge/Scrap、Cart、Door、Earned Safety、Horde、地图生成；
- Enemy、AI、Director、Faction、Anatomy、Physics；
- Downed、Last Wind、Revive、Wipe、Operation 失败与永久收益；
- Bastion/Hub、Knowledge、Archive、永久进度；
- 世界观、历史、Sacred Timeline、主线、Final Revelation、Forbidden、Glyph；
- Visual DNA、Audio、Music、Subtitle、Haptic、HUD、Accessibility；
- Co-op、Bots、Voice/Text/Ping、Social safety；
- Networking、P2P、Host Migration、Dedicated；
- Mods、SDK、Scenario Forge、Total Conversion；
- Steam、Workshop、Demo、Steam Deck、商业模式；
- Engine、Performance、ECS、Benchmark；
- AI-agent-first 开发、CLI/headless、QA/Telemetry/Streamer tooling；
- Prototype / Vertical Slice / Release Gate；
- Legacy、冲突、仍需确认、无法恢复的项目。

## 0.2 已纳入的历史来源

当前可恢复来源包括：

1. 当前超长项目对话中仍可见内容；
2. 系统保留的长对话压缩摘要/近期对话上下文；
3. 已保存到长期 Memory 的项目决定；
4. 当前会话中明确重新确认的 Reset 后规则；
5. 当前存在的 SSOT v1.0；
6. 用户上传的 GTFO 社区建议 Markdown，以及我们已经实际采纳/改造的建议；
7. 可恢复的更早项目讨论中的网络、模组、Demo、Lore、Class/Trigger 等信息。

**限制：**真正已经被删除、且系统没有留下任何摘要/Memory/文件/可检索痕迹的历史消息，不能被伪造为“已恢复”。任何这种内容只能标记为 `UNRECOVERED`，以后用户若找到旧材料再并入。

## 0.3 状态标签

- **CANON**：当前正式规则。
- **TEST**：Prototype/Vertical Slice 测试参数；可调，但不能无意改变其背后的产品原则。
- **OPEN**：尚未拍板。
- **LEGACY**：过去曾确认，但已经被新版明确覆盖。
- **CONFLICT-RESOLVED**：发现过历史冲突，本文给出当前唯一答案。
- **UNRECOVERED**：历史上可能讨论过，但当前没有足够证据恢复。

## 0.4 冲突裁决顺序

1. 最新用户明确决定/纠正；
2. 2026-09 Game Design Reset 后用户批准的新基线；
3. Reset 后未被推翻的旧明确决定；
4. 与新设计不冲突的旧已锁基础架构；
5. 助手单方面建议只能是 `TEST/OPEN`，不能偷偷晋升 Canon。

## 0.5 变更规则

未来重大修改必须写：

> **SUPERSEDES: SSOT v2.0 §X.Y**

而不是继续用“我记得我们以前锁过”。每次大批修改形成 v2.1 / v2.2；Preproduction Freeze 后再进入 v3 Production Canon。

---

# 1. 项目定义与最高设计哲学

## 1.1 一句话定义 — CANON

**1–4 人 PvE Systemic First/Third-Person Combat Game：同一套高表现战斗、Build Algebra 与 Living World，承载两个核心模式——Systemic Operations 与 Descent。**

它不是“另一个 FPS Roguelite”，也不是“GTFO + Roguelike”。

## 1.2 核心内部语句 — CANON

> **Good combat first. Broken build second. Living battlefield always.**

> **Player builds their character. Player also builds the situation.**

> **Other roguelites have procs. Ours has proc graphs.**

> **Build the weapon. Shape the disaster.**

> **Start with a great weapon. End the run as a controlled catastrophe.**

## 1.3 PvE Fun First — CANON / 最高优先级

这是 PvE 游戏。任何 Enemy、Boss、Difficulty、Resource pressure、Mission、UI、Active、Horde、Failure rule，都必须先回答：

> **它让玩家更好玩吗？**

不是：

> **它会不会更难、更折磨人、更容易死？**

难度是有趣决策和局势复杂度的副产品，而不是目的。

具体含义：

- 玩家可以变得非常强；
- 合法 God Build 不偷偷 nerf；
- Melee 高手可以凭技术省大量资源；
- Staff/Energy 可以形成高续航；
- 团队规划优秀可以让 Operation 明显更轻松；
- Boss 被一个惊人的 Build 融掉是合法故事，不是系统错误；
- 任何“纯粹多受罪但没有新增玩法”的机制优先删除。

## 1.4 简单输入，复杂结果 — CANON

复杂度放在：

- Relic interaction；
- Proc Graph；
- Fusion；
- Spell repertoire；
- Resource tradeoffs；
- World state；
- Mission consequence；
- Co-op interaction。

而不是不断增加 Q/E/F/G/Ultimate/Skill hotbar。

## 1.5 Cardinality / Hardcoding Law — CANON

> **Cardinality is data. Topology is data. Capability is data.**

任何固定数量都要问：

> **Is this a Game Rule or an Engine Assumption?**

Official 可以默认 2 Weapon / 2 Utility / 3 Staff Spells，但 Framework 必须支持 0..N。固定槽数不能渗透 Save/Network/UI/Entity architecture。

---

# 2. 为什么玩家会买、为什么会继续玩

## 2.1 五个产品支柱 — CANON

### 2.1.1 Best-in-class PvE Combat Feel

- Gunfeel 目标不是“indie 里不错”，而是真正拿 Roboquest / Returnal / Witchfire 当 benchmark；
- Recoil 清楚、有重量、**非常容易控制**，不做 PvP 压枪考试；
- Gun、Melee、Staff、Energy、Heavy 全部必须在 0 Relic 情况下就值得玩；
- Weapon swap 快、输入立即、Hit feedback 强、Camera shake 不冒充 recoil。

### 2.1.2 Compositional / Emergent Build Algebra

存在 `+8% Damage`，而且它必须有清楚的 Tag / Stat / Zone / SourceScope。

深度来自：

- Proc 产生的结果仍是完整 Gameplay event；
- Proc 可以继续 Proc；
- 简单效果可以成为另一个效果的输入；
- A+B 真正 Fusion 成 C；
- C+D 可继续 Fusion 成 E；
- 合法循环可以自持续。

### 2.1.3 Systemic / Living Battlefields

Enemy anatomy、Door、Power、Fog/Medium、Turret、Transit、Faction、Structure、Physics、Reaction、AI communication 都是 Gameplay system，不是背景。

### 2.1.4 Co-op Emergence

四名玩家不是四个独立 DPS 表。Weapon、Utility、Spell、Relic、Reaction、Revive、World manipulation、Mission decision 应不断互相创造机会。

### 2.1.5 Streamable Emergence

游戏应自然制造值得直播/剪 Clip 的事件：

- First Fusion；
- Fusion-on-Fusion；
- Proc cascade；
- Self-sustaining loop；
- Last Wind comeback；
- Posthumous kill/revive；
- Multi-player combo；
- World chain reaction；
- Predator reversal；
- bizarre Staff/Weapon transformation。

## 2.2 长期护城河

长期 retention 依靠：

- 多种 Operation Template；
- Descent + Endless；
- Relic/Fusion/Spell interaction graph；
- Storyteller/Director；
- Secrets / Forbidden；
- Mods / TC / Scenario Forge；
- 免费内容更新。

**Mods 是 retention reason，不是首发购买理由。**

---

# 3. 对标/学习库：每款游戏到底学什么

> 这不是“我们像谁”，而是“每个系统找最强参考”。同样重要的是明确**不抄什么**。

## 3.1 Binding of Isaac — 核心 Build 参考

**我们选：**
- Isaac 式 Relic/Item run 内无限累计；
- 简单 Item 也能通过组合形成复杂 Build；
- Item interaction 与玩家发现感；
- 特定组合可以彻底改变攻击形态；
- 新组合第一次发现前不把结果全告诉玩家；
- Build 越到后期越能“坏掉”。

**我们进一步做：**
- Curated Fusion 明确定义为 `A+B→C`，A/B 消失、C 是真实新 Instance；
- C 可继续参与 Fusion；
- 所有 inherited stats/procs 有 provenance；
- Proc-from-proc 是一等规则。

**不抄：**
- 把大量关键 Item 功能完全藏到必须查 Wiki 才能正常玩的程度；
- 2D/单人限制。

## 3.2 Noita — 规则语言/递归参考

**我们选：**
- Spell/Modifier 像一套可组合语法；
- Trigger/Modifier/Emitter 可以继续生成新的 event；
- 大量 Build 深度来自系统规则，而不是预写 combo 表；
- 允许玩家“编程”出奇怪 weapon behavior。

**我们进一步做：**
- Build compiler 检测 zero-time non-terminating cycle；
- 合法有 Progress Gate 的 sustainable loop 不限 Proc depth；
- 高密度 loop 做 batching/analytical representation，不删 canonical outcomes。

## 3.3 Deep Rock Galactic — Operation 高层节奏/资源参考

**我们选：**
- 任务目标清楚；
- Combat 是正常乐趣，不是“潜行失败”；
- 探索资源支撑 Supply；
- Horde/Swarm 是高低节奏中的高压窗口；
- Mission 类型有明确核心 fantasy；
- Deep Dive 启发多层长 Run 结构，但我们的正式模式命名为 Descent。

**我们改造：**
- Knowledge + Scrap 像 Nitra 一样填团队 Support Meter；
- Support Meter 满后转化成离散 Support Charge；
- Operation 资源来自 Facility 探索，Descent Support 可更多来自战斗表现。

**不抄：**
- 固定 Nitra/Resupply 的唯一经济；
- 每种 Mission 只是一套固定 Objective checklist。

## 3.4 GTFO — 局部 Operation 机制参考

**我们选：**
- Information is not free HUD；
- Terminal 是一个真实物理地点；
- Terminal Query/Search 后可 PING/Track 已知目标；
- 长期资源规划和物理资源分享；
- Terminal/Uplink、Door、Zone/Facility thinking；
- 资源可以放进 Locker/Storage；
- Bot Stay / On Me / Take / Use Tool；
- Predator/不可永久击杀 Threat 的任务灵感；
- 目标开始后敌人更多的高压感。

**我们降低门槛：**
- 默认 GUI，不强迫 CLI；
- 找到东西后可直接 PING waypoint，不要求记 Zone/Item ID；
- Mission decision UI 必须简洁。

**明确不抄：**
- “被发现=你犯错”的长期 Alarm 惩罚；
- 全局 Persistent Alarm；
- 所有关键任务都站圈；
- Standard Operation wipe 后强制重做相同 40–60 分钟内容作为“难度价值”；
- 过度潜行导致玩家不敢用我们最强的 Gunfeel。

## 3.5 Helldivers 2 — Support 输入/Heat 参考

**我们选：**
- Hold Support modifier + 方向序列；
- 熟练玩家形成肌肉记忆、新玩家永远可看提示；
- 输入成功后投掷真实 Beacon，支援物资真实到达世界；
- Heat weapon 的核心：正常控热可长期持续，贪爆发会烧掉有限 emergency sink/resource。

**我们自己的版本：**
- Hub 用 Fold/Resonance 投送 Supply Capsule；
- Operation Support Charge 来源是 Knowledge/Scrap；
- Relic/Weapon/Prototype 也可成为 Supply 选择。

## 3.6 Borderlands — Last Wind / Second Wind 参考

**我们选：**
- Downed 后仍有有限 Combat agency；
- 有效击杀/贡献可以把自己拉起来；
- Team assist 不应该“抢人头导致你无法复活”。

**我们改造：**
- 使用正式 Revive Transaction；
- 可由自己已 commit 的 DoT/Summon/Turret/Reaction 完成；
- 防止故意留 1 HP 小怪当无限保险。

## 3.7 Risk of Rain 2 — God Build escalation 参考

**我们选：**
- 后期 power scaling 必须真正戏剧化；
- proc cascade；
- Endless 中继续推极限。

**我们进一步做：**
- Descent 的 5 层就是 Build escalation；
- Operation 不追求同样的高速膨胀。

## 3.8 Roboquest / Returnal / Witchfire — Combat Feel 参考

- **Roboquest**：高速 movement + readable, responsive gunplay；
- **Returnal**：高规格 PvE mobility/combat presentation；
- **Witchfire**：武器重量、声音、命中、整体质感。

**不抄：**
- 为了“硬核”做高 recoil / sluggish input；
- 用屏幕 shake 代替真正 weapon feel。

## 3.9 Gunfire Reborn — FPS Roguelite breadth 参考

**学：**英雄/武器/Build breadth 与多人重复游玩。  
**警告：**不能只停在“更多升级”；我们的优势必须是 Fusion + Proc Graph + Systemic world。

## 3.10 Abyssus — Co-op FPS Roguelite 内容量参考/警告

**学：**co-op build content packaging。  
**警告：**大量 mods/charms/blessings 不等于 interaction depth；不能靠 Item count 做卖点。

## 3.11 Deep Rock Galactic: Rogue Core — 直接竞争警告

**学：**4p FPS Roguelite 市场需求。  
**警告：**与我们表面重叠很高，尤其此前 Player 名称 `Reclaimer` 与其碰撞；公开命名必须改。Build escalation 若不够质变，会被视为“又一个 Rogue Core”。

## 3.12 Moros Protocol /《毁灭协议》 — 表面同质化红线

**警告：**Retro/Pixellated dark sci-fi FPS + procedural rooms + gore + roguelite 已经有产品占位。  
**结论：**Retro 不能是我们的品牌身份；我们必须靠 Fusion/Proc/Living Battlefield/visual DNA 拉开。

## 3.13 HELLBREAK — “又一个 Roguelite”警告

**警告：**fast FPS + many blessings/upgrades 并不足以形成长期差异。  
**我们必须避免：**“shoot → upgrade → shoot harder”成为全部循环。

## 3.14 Holy Shoot — Dead-End Proc 反面教材

**我们观察到的风险：**`roll→reload`、`roll→shock`、`every N hits→effect` 如果 effect 到此结束，Build 仍是 perk list。  
**我们的规则：**重要 proc 输出必须成为可继续被消费的 first-class event。

## 3.15 ANVIL — Gameplay/Art 拼装感反面教材

**警告：**走、射、拿升级、重复；Relic/upgrade 行为变化不够；visual identity 弱会产生 asset-pack 感。  
**我们的回答：**Mission 本身也要提供不同问题；Visual DNA 必须早锁。

## 3.16 Far Far West /《遥遥西土》 — Gun + Spell + Mission + Visual Identity

**我们选：**
- 1–4p mission-driven PvE；
- 枪与 Spell 共存；
- Hub→Mission→Reward 的清楚组织；
- 强 Theme/Art identity 的价值。

**竞争提醒：**如果 Staff 只是魔法枪、Operation 只是“进去做任务”，表面会撞。我们的差异必须是 Systemic Operation + Build Algebra/Fusion + Living Battlefield + Descent。

## 3.17 Iron's Spells 'n Spellbooks — Staff Spell repertoire 参考

**我们选：**Staff 是施法平台，一根 Staff 里可以切不同 Spell。  
**我们的输入：**Hold R 打开 Spell radial，Fire 施放当前 Spell。  
**不抄：**RPG hotbar/大量独立 spell button。

## 3.18 Darktide — Staff/Peril 与 PvE weapon loop 参考

**我们选：**caster/energy resource 可以通过 heat/peril/cooling 形成持续但有压力的循环。  
**不要求：**所有 Staff 都使用同一 Mana+Peril 双条；每种 Staff family 可以有自己的 resource identity。

## 3.19 Mario Maker / StarCraft Editor — UGC 参考

**我们选：**开发团队内部任务也使用同一套 Scenario/Graph primitives；成熟后开放给社区。  
**不做：**核心玩法未验证前先造完整公开 Editor。

---

# 4. 两个核心模式

# 4A. SYSTEMIC OPERATIONS — 默认/主模式

## 4A.1 定义 — CANON

- 一个 Run = 一个连续 Operation / Facility / Mission；
- **没有玩家可见 Layers**；
- 资源、Door、World state、Cart、Knowledge、Support、Optional consequences 从 Insertion 持续到结束；
- 典型时长目标约 40–70 分钟，具体 Template 可变化；
- Mission 比 Build 更核心；
- Combat 正常且应当爽，但不是所有 Encounter 都值得打。

### Fantasy

> **进入一座你不控制的设施，用有限资源解决一个不断变化的问题，并承担自己造成的后果。**

## 4A.2 核心循环 — CANON

Briefing → Insertion → Explore/Fight/Avoid → 获取信息 → 获取 Knowledge/Scrap/资源 → 任务步骤 → Facility/Route/Cart 决策 → Support/Build/补给选择 → Objective Pressure/Horde → Consequence → Resolution → Exit。

Operation 不是 Roguelike progression 主循环；Roguelike 元素是 **Field Adaptation / Run Mutation**：少量 Relic/Spell/Fusion 改变“这次怎么解决任务”。

## 4A.3 信息不是免费 HUD — CANON

- HUD 始终保留一个清楚 Primary Objective；
- 关键未知位置/物资/系统状态通常不自动全图显示；
- Physical Terminal 是 Facility 自身的信息/控制节点；
- Terminal Search 找到目标后可以 **PING/TRACK → 生成正常 Team waypoint**；
- 难点在主动获取信息，不在背 Item ID/Zone code。

### Terminal 能做

- Search/Query；
- Security/door state；
- Power / ventilation / transit / local network；
- objective systems；
- ping 已定位对象。

### Terminal 不能做

- 不能代表我们的 Hub；
- 不能从 hostile/abandoned facility 直接下单 Supply；
- 不能一键“清全局 Alarm”。

## 4A.4 没有通用 Alarm 系统 — CONFLICT-RESOLVED / CANON

早期曾设计 Local→Persistent Facility Alert；**现已删除作为游戏系统。**

当前只有：

- Ambient/local threats；
- Horde/Threat Surge；
- Objective Pressure；
- 具体 System Response（Scout叫援军、Camera触发Security response、Nest激活等）。

开枪不是“犯错”。

## 4A.5 Horde / Objective Pressure — CANON

- 普通探索阶段允许零散 combat 与偶发 Horde；
- Objective 开始时通常比平时有更高 enemy pressure；
- Horde 不是无限刷，结束后要真的回到较低压力；
- 不使用通用地面震动提示；
- 主要用怪物叫声、远处回应、抓挠、脚步、Faction-specific acoustics、环境反馈提示“有东西来了”；
- 不用全局红色 Alarm meter / countdown。

## 4A.6 Earned Safety — CANON

没有固定 Safe Room。

玩家通过：

- 清理局部威胁；
- 关普通 Door；
- Seal Security/Containment route；
- 破坏 Spawner/Nest；
- 接管 Turret；
- 控制 ingress；
- 处理当前 Threat source；

在**当前前线**创造相对安全空间。

Director 不得因为“太久没打怪”就在安全区凭空刷敌人。

## 4A.7 No Mandatory Backtracking — CANON

- 主线总体向新空间推进；
- 玩家可自愿回去拿漏资源/Optional；
- Mission 不应要求回 5–10 分钟前的 Terminal/Control Room 做重复劳动；
- 新获得 Power Cell 可在下游 Control Relay继续配置；
- Branch 采用 Forward-Branch-Rejoin；
- Optional 尽量有第二出口，并在前方重接；
- Extraction 尽量打开新路线。

## 4A.8 Extraction — CANON

**不使用“60秒撤离否则死”的硬倒计时。**

完成 Primary Objective 后，通过世界状态明确告诉玩家：

> **现在继续留在这里会越来越危险，应该走。**

例如 Fold collapse、Containment失效、Threat从后方推进、系统逐步失效。没有任意秒数到点处决；留下风险升高且没有稳定 farm 收益。

## 4A.9 Operation 资源哲学 — CANON

资源压力的目标是：

> **改变打法，而不是取消玩法。**

玩家可以真的把局势搞到不可恢复，但 Generator/RNG 不得生成数学上无解的资源局。

### Ballistic

- 有限 Ammo；
- 即时、精准、高 burst；
- 最依赖 Ammo Supply。

### Energy

- Heat 可自然冷却；
- 正常控热可近似无限续航；
- 贪爆发导致 Overheat、downtime，或消耗有限 Heat Sink/Cooling resource；
- 参考 Helldivers 2 的“可持续但过度使用会烧应急资源”哲学。

### Staff/Casting

- 可恢复 Mana/Instability/Heat/Health/Charge 等 family-specific resource；
- Spell 有 cast/channel commitment；
- 可持续、多功能、control/reaction 强；
- 不能同时成为无成本最高远程 DPS。

### Melee

- 不耗 Ammo；
- 成本是 Proximity + Time + Safety；
- 高技术玩家应能通过 Parry/Footwork/Stagger/Part break 把 Health cost 降得很低；
- 不把“必然换血”当平衡手段。

### Heavy/Prototype

- 稀有/昂贵 resource；
- 用来解决大问题，不做日常小怪武器。

## 4A.10 Facility 本地资源 — CANON

Facility 中可以直接找到少量：

- Ammo；
- Medical；
- Tactical/technical resources；
- Mission resource。

但通常**不足以覆盖整个 Operation 的正常消耗**；它们用于缓冲、探索奖励和救急。

## 4A.11 Knowledge + Scrap → Support — CANON

- Knowledge/Data 与 Scrap/Salvage 是不同世界对象；
- 即时玩法上都可为团队 Support Meter 提供价值；
- Knowledge 同时拥有 Archive/Research/剧情价值；
- 普通 Enemy kill 不应稳定产出足够 Support 形成 Kill→Ammo 正反馈。

### Support Meter / Charge

- Meter 满后生成一个离散 Support Charge；
- 溢出进度保留；
- Operation 正常探索/主线目标测试目标约 2–3 Charges；贪探索可更多；
- 标准 Drop 通常 1 Charge；Prototype/高级支援可 2 Charges/Authorization。

### Support 输入

- Hold Support key（默认可为 Ctrl，可重绑）+ 3–5 步方向序列；
- Controller：modifier + D-pad；
- Pattern 固定/稳定，新手看提示，老手记肌肉记忆；
- 输错不扣 Charge；
- 成功授权后投真实 Fold/Resonance Beacon；
- Beacon commit 后才扣 Charge。

### Supply 类型 — CANON

- Ammo；
- Medical；
- Tactical；
- Power/Mission Cell；
- Weapon；
- Relic；
- Prototype/Heavy。

Descent 也共享这个系统，但 Earn policy 与用途不同。

### Supply 公共所有权 — CANON

所有 Pod 物资都是 Team/Public world contents。

- Ammo/Med/Tactical/Power：自由拿、Drop、再分；
- Weapon Pod：Shared Draft 第一轮每人最多 claim 1 或 Pass，之后剩余自由；
- Relic Pod：Shared Draft；claim 后 Relic 吸收进 Build，不能再 drop；
- Prototype：少量/单个 Team Asset，可以传递。

Host/Party Leader 没有特权。

## 4A.12 Physical Ammo / Storage — CANON

- 玩家可以从自己的 reserve 拆出 ammo bundle 丢到地上；
- 队友按 ammo family/capacity 拾取；
- 可将 supplies 放回合法 Locker/Storage，创建团队临时 cache；
- 资源物理化优先于抽象“Give Ammo”菜单。

## 4A.13 Facility Cart / Power — CANON

重大系统配置使用**小整数 Budget + Cart 多选**，不是 1-of-2，也不是工程模拟器。

例如有 3 Cells：

- Turrets — 1；
- Ventilation — 1；
- Security Shutters — 1/2；
- Transit — 1；
- Research Vault — 2。

规则：

- 同屏通常 4–6 项；
- Cost 主要 1/2/极少3；
- 每项一句话能理解后果；
- 复杂性来自世界后果，不来自 UI 数学。

**任何合法 Terminal/Control operator 都可直接 Commit。** 不做多数投票，避免 2v2/AFK/恶意 stall。重大不可逆终局动作可例外用 Shared Decision。

Commit 后不免费反悔返资源；后续重配置必须通过新的合法 World action/Cell/下游节点。

## 4A.14 Door System — CANON

### 普通 Door

- 免费开关；
- Delay、LOS、部分声音隔离；
- Enemy 可砸/Hack/绕；
- 状态用 Stable/Damaged/Breaching 世界表现，不显示传统 HP 条。

### Security/Containment Door

- 战略 Infrastructure；
- Power/Terminal/Cart 投入后可真正长期 Seal 一个 ingress；
- 只有明确 Breach-capable Threat/Mission/Power failure 可以破坏；
- 不允许 Director 偷偷绕过玩家投入。

Door 可被 Foam/Weld/Barrier/Ice/Breaker 等公共系统互动。

## 4A.15 Operation Build / Roguelike 强度 — CANON DIRECTION

Operation 不是 Descent-lite。

- Relic 获取少；
- Fusion 是稀有大事件；
- Build 主要帮助改变解决任务的方法、资源效率、战术选择；
- 不要求每几分钟三选一；
- 如果删掉 Relic 后 Operation 本身不好玩，说明 Mission 设计失败。

测试目标（非最终）：自然约 2–4 个有意义 Relic/Player；主动贪 Build/花 Support 可更多。具体数量以 Prototype 为准。

## 4A.16 Operation 失败 — CANON

**没有 Gameplay Recovery Anchor / checkpoint rollback。**

恢复梯子：

Alive improvisation → Downed/Last Wind → teammate revive/carry → Revive Utility/support effects → committed Last Chance effects → 真正不可恢复 Wipe。

真正失败意味着 Operation Failed；不能用死亡洗掉坏资源状态/Cart/贪心后果。

### Last Wind

- Downed 后保留有限战斗；
- 有效 kill/contribution 可自救；
- Team assist 不抢恢复；
- 自己已 commit DoT/Summon/Turret/Reaction 也可触发；
- 防 farm。

### Last Chance

全员 Downed 后，已 commit 的 projectile、DoT、Summon、Turret、Revive Drone 等先跑完；若能制造恢复，就取消 wipe。

### 失败永久收益

- 已上传/Banked Knowledge/Data：100% 保留；
- Cosmetic Discovery：保留；
- Fusion Discovery：保留；
- Run Weapon/Relic/Spell/Utility/Prototype：不永久继承；
- Operation/Archive 类代币失败时测试目标约成功应得的 50%；
- Mission Completion Bonus：失败无。

---

# 4B. DESCENT — Build/Combat Power Fantasy 模式

## 4B.1 定义 — CANON

- 5 Layers；
- 每 Layer 目标平均约 12 分钟；
- 标准 Run 约 60 分钟上下；
- 完成后可 Go Deeper → Endless；
- Mission 轻、Combat 密度高、资源宽松、Build 快。

### Fantasy

> **Forget restraint. Kill, build, fuse, loop, break the game.**

## 4B.2 五层成长曲线 — CANON

1. **Layer 1 — Assemble**：第一层结束前 Build 已“上线”；Hybrid Guarantee 保证 Anchor + connectable choices + Boss/major transformer/pivot opportunity。
2. **Layer 2 — Specialize**：乘区、Crit、Status、Reaction、Utility/Spell方向明确。
3. **Layer 3 — Transform**：Fusion / topology rewrite 明显增加。
4. **Layer 4 — Loop**：Proc Graph 开始闭环、自持续。
5. **Layer 5 — Break**：God Build / controlled catastrophe；大量 combat payoff。

不是同样的 12 分钟 ×5，只提高敌人数量。

## 4B.3 Mission / Objectives — CANON DIRECTION

故意简单，负责改变“怎么杀”，不把 Operation 的 Terminal/Cart/resource planning 搬进来。

候选：

- Clear；
- Eliminate；
- Capture；
- Assault；
- Hunt；
- Horde；
- Destroy；
- Boss / Moving Front。

Vertical Slice 不需要全做。

## 4B.4 Resource Profile — CANON

**Abundant, not infinite.**

- Ammo/Medical较多；
- Utility 更快 Recharge/更多补给；
- Support Meter 增长快，可由 combat/objective performance 填；
- Supply 更常用于 Weapon/Relic/Prototype；
- Layer transition 可以使用更宽松 Recovery profile；
- 资源系统仍存在，否则 Ammo/Reload/Heat/Recharge Build 会变死词条。

## 4B.5 Relic / Spell / Fusion — CANON

- Relic 高密度；
- Staff Spell 获取/扩容更明显；
- Fusion-on-Fusion 正常；
- Proc loop 正常；
- God Build 合法；
- Streamer moment 高密度。

---

# 5. Player Loadout 与 Input

## 5.1 当前 Loadout — CANON

- Character；
- 2 Weapon slots；
- 2 Utility slots；
- 1 Signature Active；
- Quick Melee；
- Ping；
- Relics（无限累计）；
- 若持 Staff：Staff 自己的 Spell repertoire。

**已删除：**Equipment、Accessory、Universal Weapon Active、2 Character Active、独立 baseline Scan button、通用 Ultimate slot。

## 5.2 Keyboard — CANON DIRECTION

- `1 / 2`：两把 Weapon；
- `3 / 4`：两个 Utility 的快速选择/直接入口；
- Weapon swap：非常快，PvE-first；
- Ping：纯 Ping；
- Signature Active：一个独立输入；
- Utility：正式语义仍支持一个 Tactical Use + select；Keyboard 可提供 direct bind；
- Controller 只做语义等价，不强迫模拟数字键。

## 5.3 R / Weapon Context — CANON

### Gun

- Tap R = Reload/Cycle；
- Hold R = 仅在该枪确实有 Fire mode/Ammo mode/Context 时打开 radial；
- 没功能就不硬塞。

### Staff

- Hold R = Spell radial；
- mouse/stick 选择，松开确认；
- Fire = cast 当前 Spell。

### Melee

- R 没有通用强制行为；
- 若有 stance/technique 才 Hold R 打开相关 radial；
- Right Click 是即时 defensive action，更合适。

---

# 6. Weapon / Combat Arsenal

## 6.1 Weapon slots — CANON

不叫 Primary Gun / Secondary Gun；就是 Weapon Slot A/B。

合法组合：

- Rifle + Shotgun；
- Rifle + Sword；
- Rifle + Staff；
- Staff + Sword；
- Energy + Staff；
- 双 Melee 等。

## 6.2 Gunfeel — CANON

- Recoil：Hybrid learnable pattern + 很小 seeded variance；
- 常规枪必须非常容易控制；
- First shots / short burst 稳定；
- Recoil growth 有 saturation，不无限抬枪；
- Horizontal random recoil 克制；
- Camera shake 独立、可关；
- Hipfire 对 Light/Medium 真正可用；
- ADS 提高 precision/stability，不把 Hipfire 故意做废；
- Light/Medium 倾向快速 sprint→fire/ADS；
- Heavy 可以更慢但输入必须立即反馈；
- Reload staged、可取消，已完成 stage 保留；
- Weapon swap 快；
- No-Proc Test：裸枪就好玩。

## 6.3 Melee — CANON

输入：

- Tap Left Click = Light；
- Hold Left Click = Heavy/Charged；
- Right Click = Defensive Action；
- 无通用 stamina attack tax。

### Vertical Slice 四把 — CANON TEST SET

1. **Hammer**：Posture/Stagger、Armor/Part/轻 Structure break；
2. **Knife**：最快、短 reach、高机动、精准 Weakpoint/Part、短 recovery；必须不是“小号 Sword”；
3. **Spear**：最长 reach、spacing/counter、单线穿刺，贴身拥挤较弱；
4. **Sword**：balanced、cleave、最完整 guard/parry。

Melee 省 Ammo，但不是免费：危险来自空间、远程敌人、Area denial、失误 Health cost。

## 6.4 Staff / Spell — CANON

**Staff 是 Casting Platform，不是魔法枪。**

- 默认 3 Spells；
- Run 内通过合法 progression 扩容；
- Official 测试上限 6；
- 3/6 是 profile，不是 engine hardcode；
- Staff 在 Operation 里必须开局就完整好用；
- Staff 是 Descent 的重要深 Build 轴。

### Spell reward

Spell 与 Relic 分开。Spell 可来自：

- Spell Archive；
- Resonance shrine；
- Spell cache；
- 专门 Run reward；
- Staff/Spell Fusion 系统。

Relic 强化 Spell，但不等于“Relic 随机送 Spell”。

### Spell 类型应真正不同

Projectile、Channel、Area、World manipulation、Defense、Summon、Mobility、Control 等，不做“100个不同颜色火球”。

## 6.5 Energy — CANON

- Heat 上升、停火自然冷却；
- 技术好可近似无限续航；
- 贪 burst → Overheat / lockout / consume Heat Sink；
- Tactical Supply 可补 emergency technical resource；
- Energy 的强项是 sustain/稳定，不应同时永远拥有最高 burst。

## 6.6 Heavy / Prototype — CANON

- Rare ammo/cell；
- 大型 problem-solving weapon；
- 对 Heavy armor、Boss parts、Structure 等有真实作用；
- Mission Prototype 不能只带一个隐藏 `CanKillBoss=true`。

---

# 7. Character System

## 7.1 Character ≠ Hard Class — CANON

不做必须的 Warrior/Tank/Healer/Mage composition。

所有合法 Character 都拥有：

- 完整 movement；
- gun use；
- Quick Melee；
- Staff/Melee/Energy 的合法使用能力；
- 2 Utility；
- Interact/Ping。

Character 是 Soft Archetype：改变起点与 synergy，不决定终点。

### 历史 Legacy

更早曾讨论 Warrior/Healer/Tank/Gunner/Wizard 等 Class/trigger 思路；当前其真正有价值的部分已经吸收到 **Proc Graph + Soft Archetype**，硬职业依赖废弃。

## 7.2 1 Signature Active — CANON / TEST CONTENT

没有通用 Ultimate。

Active 必须：

- 至少满足“新增 Verb / 改变战场解法 / 大量 Build hooks”三项中的两项；
- 不接受纯 `+50% damage for 8s`；
- Operation 中不能成为必选经济/Objective工具；
- Descent 可通过 Build 推到极端。

### Prototype candidates — TEST

- **Aegis**：Directional/mobile barrier；推进/Revive/Crossfire；
- **Breaker**：Cleave/Posture/Part/Armor/Breach；
- **Echo/Conduit**：让合法 Attack/Spell/Utility 产生延迟 Echo/规则变化。

**风险：**如果在 Operation 里像 Hero Shooter CD 按钮，应重做，不强留。

## 7.3 Duplicate Character — CANON

Official 允许重复 Character；4人同一个也合法。Matchmaking 不做角色多样性税。

## 7.4 Mid-run Character swap — CANON

Run 开始后 Character 锁定到 Run 结束；特殊 Artifact/TC 可以 rule-break。

---

# 8. Utilities

## 8.1 Slots — CANON

Official 默认 2 Utility slots，Framework 0..N。

一个 Utility 可以是：

- Frag/Smoke/EMP/Healing/Gravity/Decoy；
- Scan；
- Sensor beacon；
- Deployable；
- Trap；
- support device 等。

## 8.2 Scan — CANON

Scan 现在是 Utility，不是 baseline ability，也不是 Ping。

- 对合法 hostile target 施加 Scanned/Marked；
- Team-wide DamageTaken amplification / focus-fire window；
- 不穿墙、不揭 Secret；
- 默认不多玩家线性叠加；
- 可被 Relic/Fusion 改成 multi-mark/chain/transfer 等；
- 不能强到成为“团队税”。

## 8.3 Resource profile — CANON

### Operation

- limited charges/technical resource；
- Facility tactical supplies + Tactical Drop + Build recovery；
- 不默认快速免费 auto recharge。

### Descent

- more charges / fast recharge / more tactical drops；
- 支持 Utility spam/God Build。

## 8.4 Revive Utility — CANON

只有明确 ReviveEffect 的专用 Utility/Build 能复活；普通 Healing 不自动 revive。

---

# 9. Relic / Build Algebra / Proc / Fusion

## 9.1 Relic — CANON

- 唯一通用被动 Build item domain；
- Isaac 式无限累计；
- 无固定 6-slot；
- Run 结束不永久带出。

### Vertical Slice pool — TEST

第一批目标 30：

- 约8 Scalar/Amplifier；
- 8 Connector；
- 6 Rule Modifier；
- 4 Transformer/Keystone；
- 4 高交互/Fusion ingredient；

类别可重叠；Interaction density 优先。

## 9.2 Numeric modifier — CANON

`+8% Damage` 完全合法。

必须清楚：

- 什么 Tag；
- 哪个乘区；
- 哪些 SourceScope；
- 当前 Build 有哪些 effect 真正受益。

## 9.3 Proc Graph — CANON

重要 Proc 输出默认是 first-class Gameplay primitive，而不是 terminal callback。

例如：

Dodge → ReloadCompleted → Overcharge → Crit → Electric Attack → Shock → Reaction → Projectile → Crit → Utility Recharge。

**Proc-generated effect 默认可以继续 Proc。**

Trigger 自己决定接受 Direct/Triggered/Utility/Reaction/Summon/Team/World 等来源；不是 engine 全局 ban。

## 9.4 Sustainable Loop vs 技术死循环 — CANON

合法无限：

- 有时间推进；
- projectile travel；
- resource/charge/cooldown；
- target/state change；
- action cadence 等 progress gate。

非法：同一个 commit 内 A→B→A，零时间、零资源、零状态推进的 non-terminating cycle。

Compiler 必须提前检测；可以显式重写成 periodic/sustained process，但不偷偷 cap 结果。

## 9.5 Fusion — CANON

**Fusion = Consuming synthesis，不是临时 synergy buff。**

> `A + B (+...) → C`

- A/B 独立 Instance 消失；
- C 是新 Item/Weapon/Relic/Spell Provider Instance；
- C 可继续 `C + D → E`；
- Recipe 满足后自动 Fusion；
- deterministic，额外不掷“是否成功”；
- 第一次拿最后 ingredient 前只提示 Unknown Strong Interaction / 消耗成本，不泄露结果；
- 已发现后可明确显示 Known Fusion。

### Fusion inheritance — CANON

C 最大程度继承/转换 A/B 的投入：

- Preserve；
- Merge；
- Convert；
- RebindScope；
- Promote；
- 明确 Discard。

例如 Reload Speed → Return Speed、Magazine → Orbit count 等。重大损失必须提前可读。

### Fusion 不是 Synergy

- **Synergy**：A/B 都还存在，互相增强；
- **Fusion**：A/B 被消费，生成 C；
- **Loop**：现有 Providers 因果闭环。

---

# 10. Combat Math / Crit / Reaction

## 10.1 Stat/Zone pipeline — CANON

多区乘法结构：Base → Weapon/Utility/Ability modifiers → Character/Core → Relic → Team/Conditional → Crit → Target DamageTaken → Element/Reaction → Defense。

同 Zone additive，跨 Zone multiplicative；最终实现由统一 Stat Engine 编译。

## 10.2 Crit >100% — CANON

超过100%进入 Crit Tiers，不浪费。Utility/Ability direct damage 默认也能 Crit，除非 effect 自己明确禁用。

## 10.3 Reaction — CANON

ReactionEvent 是 first-class：Fire+Toxic 等通过 Tag/Registry 定义，不硬编码 switch。

环境 Medium/Material/World Network 也能参与；跨玩家/Utility/Spell/Weapon 都可触发。

## 10.4 God Build — CANON

不做隐藏 anti-player scaling、boss global damage cap、proc depth cap。优化 representation，不删 outcome。

---

# 11. Player Movement / Damage / Life State

## 11.1 Movement — CANON

所有 Official Character 基础拥有：

- 高速移动；
- 无限 Sprint / 无全局 Stamina；
- Jump；
- Crouch；
- Slide；
- Mantle；
- 有用的 Air Control；
- Quick Melee lunge；
- Rocket jump / impulse 等系统可以合法存在。

Light/Medium Weapon 通常可在 Sprint 中快速进入 firing；Heavy 可以更慢，但不做普遍输入迟滞。

## 11.2 Player injury — CANON

Official Standard 不做长期四肢残废/跛行/断臂影响玩家几十分钟。Enemy 可有严重 dismemberment，Player 伤害主要影响 Health/Downed/Death/短暂明确状态。

## 11.3 Health recovery — CANON

Operation：

- 不自动回满；
- 低于很低 Emergency Recovery Floor 时，真正安全/脱战后可缓慢恢复到最低生存线；
- 测试概念约 20–25% 当前合法 HealthCap；
- 不恢复 MaxHP sacrifice / sealed HealthCap；
- Medical 仍是重要资源。

Descent：可以使用更宽松 recovery/Layer profile。

## 11.4 Downed / Revive — CANON

- 0HP/FatalEvent → Downed（Mode允许）；
- Downed 可 crawl/look/ping/使用允许的武器；
- Primary Interact = Revive；Secondary = Carry；
- Carry 暂停/影响 bleedout，具体数值后测；
- Revive 后恢复中等 Health，约 35–50% HealthCap 测试区间；
- 极短 Revive Grace 只防动画/控制恢复时秒倒，主动攻击会提前解除。

## 11.5 Team wipe / Last Chance — CANON

- 全员倒地时不立即判死；
- 已 commit DoT、Projectile、Turret、Summon、Reaction、Revive Utility 继续运行；
- 若其触发合法 Last Wind/Revive，则恢复；
- Operation 真正无恢复路径才失败；
- Descent 可按模式继续使用 Reinforcement/Recovery profile，但不通过 checkpoint 洗资源。

---

# 12. Friendly Fire / Faction / Collision

## 12.1 Player Friendly Fire — CANON

Official Standard 默认 Player-to-Player damage = 0%。Framework 用 typed multiplier/profile，不是 boolean；Custom/Community 可设 10/25/50/100% 等。

SelfDamage、FriendlyImpulse、FriendlyDebuff、environment ownership 分开。

## 12.2 Same-faction Enemy damage — CANON

- 同 Faction Enemy 默认不互相造成 gameplay damage；
- 尽量在 candidate filtering 阶段就排除，减少 Horde/AoE 无意义计算；
- 不进入完整 armor/status/reaction pipeline。

## 12.3 Same-faction projectile interception — CANON

普通同 Faction infantry 默认不阻挡彼此普通 projectile/hitscan；Movement/Crowd occupancy 仍存在。Security barrier/large body/特殊 attack 可以显式 override。

## 12.4 Crowd blocking — CANON

Hybrid Size/Role-based：

- 普通小/中 Horde：soft occupancy/pressure，不能靠碰撞意外把玩家永久锁死；
- Heavy/Brute/Shield/Boss/Vehicle/Blocking Role：可真实 hard block；
- 真正抓住玩家必须通过 Grab/Pin/Restraint action，不靠 physics bug。

---

# 13. Enemy / AI / Director

## 13.1 AI原则 — CANON

Pipeline：Perception → Belief → Group/Cohort → Role Intent → Action → Motor。

- AI 不全知；
- 感知基于 Vision/Hearing/其它 Sense providers；
- Group 可以共享信息，但必须有 communication scope；
- 不 input-read；
- 高难度提高协同/决策，不通过作弊 wallhack。

## 13.2 AI scale / representation — CANON DIRECTION

- 目标支持高密度 Horde / 5k AI 级压力测试；
- ECS/SoA、Group Brain、Cohort、Flow field、LOD；
- 只有当前 Combat fronts 高精度运行 individual behavior。

## 13.3 Operation Encounter Grammar — CANON

1. Pass-through Threat；
2. Guarded Value；
3. System Holder；
4. Escalation Source；
5. Mobile Pressure；
6. Pursuit/Displacement；
7. Combat Payoff；
8. Forced Breakthrough。

每个 Encounter 必须回答：

- Why fight?；
- Can we avoid/reshape it?；
- What changes if we engage?。

## 13.4 Combat vs Avoidance — CANON

- Avoid：省 Ammo/Medical/Tactical、少占时间；
- Fight：清空间、Earned Safety、Guarded Value、夺 System、阻止 escalation、享受 Gunfeel；
- 不设统一 stealth bonus，也不设 kill quota；
- 目标是经常出现“值得打 / 绕了更赚 / 先改系统再打”。

## 13.5 Predator Reversal / Unkillable-but-interactable Threat — CANON

Mission Grammar：

Threat → Manipulation/Trap → Capability Acquisition → Reversal。

前期普通 build 不能永久杀，但所有 attack 都有意义：Part damage、Stagger、Slow、Burn suppression、Door/Trap/Lure 等。

后续沿前向路线拿 Prototype/Anti-predator capability；Predator 通过真实 Transit/Vent/Maintenance/Fold/破坏结构绕到前方，不凭空 teleport；最后从猎物变猎人。

## 13.6 Spawner / Construct capability — CANON DIRECTION

不做几十个“Mom spawns baby X”换皮。Spawner/Constructor 是公共 capability：Brood、Drone fabricator、Corpse architect、Parasite host 等通过不同 world/economy/target behavior 形成差异。

## 13.7 Hordes — CANON

Operation：Ambient/local → Horde/Surge → Objective Pressure。高压结束后必须给真正低压窗口。Descent 则允许更高密度持续 payoff。

---

# 14. World Systems / Door / Facility

## 14.1 Door — CANON

Hybrid Door System，详见 §4A.14。

## 14.2 Facility Systems — CANON DIRECTION

可用系统包括：

- Power；
- Ventilation/Fog；
- Security/Doors；
- Turrets/Defense；
- Transit；
- Fabricator/Storage；
- Containment；
- Network/Uplink；
- Cargo/Condition systems；
- Fold/Resonance structures。

重要原则：UI 选择简单，World consequences 深。

## 14.3 Terminal / local network — CANON

Terminal 只管 Facility 自己的 Network/Information/Control，不负责 Hub Supply。

## 14.4 Earned Safety — CANON

玩家创建安全，不靠固定 Safe Room。

## 14.5 No mandatory backtracking — CANON

主线持续揭开新空间；旧区域只可自愿返回。

---

# 15. Operation Mission Architecture

## 15.1 Mission = Stateful Problem, not Objective Checklist — CANON

Major Mission 至少包含一个会变化的 World/System state 与一个真正改变后续玩法的玩家选择。

## 15.2 Mission Grammar v1 — CANON WORKING SET

1. Restart / Reconfigure；
2. Predator Reversal；
3. Capability Acquisition；
4. Infrastructure Reclamation；
5. Condition-sensitive Transport；
6. Network / Uplink Operation；
7. Containment Allocation；
8. Ecological / System State Collapse。

普通 Operation 通常只用 1 Primary + 0–1 Secondary；极少数复杂 Operation 才加第三个。禁止“Restart+Cargo+Predator+Uplink+Collapse 全塞”。

## 15.3 Curated Template + Procedural Situation/Room Graph — CANON

- 设计师定义 Operation Template 的核心玩法故事；
- Generator 只在允许范围内重混：Cluster、Terminal/Resource/Optional 位置、World state、Cart、Enemy、Ingress、Finale fault、Extraction route；
- Hand-authored Cluster，procedural graph/state；
- 目标：**熟悉问题，不熟悉答案。**

## 15.4 Template examples — CANON / TEST

### BLACKSTART

Restart + Containment Allocation：重启 Relay，同时配置 Facility systems，前面选择改变 Finale。

### HUNTING GROUND

Predator Reversal + Capability Acquisition：先控制 Predator，再获得真正能杀它的 Prototype。

### COLD STORAGE

Condition Transport + Infrastructure Reclamation：运输条件敏感 cargo，并抢回 Facility infrastructure。

### DEAD NETWORK

Network/Uplink + System State Collapse：恢复 network，同时每个恢复步骤改变环境/生态状态。

## 15.5 Failure path — CANON

子目标失败优先进入 Degraded Success Path：改变局势/增加步骤/损失功能，而不是“一次按错就 Mission Failed”。真正不可逆 failure 要少、提前可读、Generator 可验证。

---

# 16. BLACKSTART Vertical Slice — TEST SPEC

## 16.1 Purpose

验证：

> Great combat → Physical Terminal → Information → Resource pressure → Support choice → Cart configuration → Greed → Objective Pressure → earlier decisions reshape finale。

不验证完整剧情、Boss、Predator、复杂 Faction war。

## 16.2 结构

- 0–5 min：Insertion / Gunfeel proof；
- 5–10：Terminal Search→PING Sync Coupler；
- 10–18：Security/Maintenance forward routes；
- 18–24：Emergency Grid Cart / 3 Cells；
- 24–32：Optional/Knowledge/Support decision；
- 32–42：Moving BLACKSTART Finale；
- 42–45：Resolve + 新 Extraction route。

## 16.3 Prototype Cart

- Ventilation — 1；
- Security Shutters — 1；
- Defense Network — 1；
- Transit — 1；
- Research Vault — 2；
- 3 Cells total。

Research Vault 必须 forward-loop/rejoin，不做原路走回去；它增加 Knowledge/Relic/Support，同时新增后续 ingress/route consequence。

## 16.4 Finale

不是站圈；Relay 启动后通过 local/forward Faults 推进新空间。前面 Cart 决定 Fog、Turrets、Ingress、Transit 等实际状态。

**No Boss in first slice.** 如果没有 Boss Finale 就不爽，优先怀疑 Mission core，而不是塞 Boss 修补。

## 16.5 BLACKSTART QA questions

1. 0 Relic 的前10分钟好不好玩？
2. Terminal 是有用还是手续？
3. 玩家会不会主动说“这群别打”？
4. Support 会不会产生 Ammo vs Relic 的真实讨论？
5. Melee/Staff/Energy 是否改变资源策略而不是上位替代？
6. Cart 是否秒懂、后果长期可感？
7. Finale 是否真被早期决策改变？
8. 失败时玩家能否说出“我们哪里做错了”，而不是“RNG没给资源”？

---

# 17. Map / Room / Spatial Generation

## 17.1 Operation

Hand-authored Cluster + procedural graph/state。Forward-Branch-Rejoin，typed semantic ports：Security/Maintenance/Transit/Vent/Fold/Cargo/Power/Optional/ThreatIngress 等。

## 17.2 Descent

Isaac-like macro Room Graph + hand-authored true-3D Room/Cluster templates；main path + branches + Treasure/Shop/Gamble/Sacrifice/Elite/Event/Secret/Boss 等旧方向仍可作为 Descent 的 non-conflicting inspiration，但正式 room taxonomy 需要在 Descent prototype 后重新审定。

## 17.3 Spatial fairness — CANON

- 必需物品/Terminal/Power cell 每局可换位置，但必须合法可达；
- Resource Safety Budget；
- 不生成 technical legal but boring/unfair graph；
- 不靠空走廊增加时长。

---

# 18. Camera / HUD / Controller / Accessibility

## 18.1 Camera — CANON

Official FPS default + 可自由切 TPS；两者共享 canonical aim/muzzle/hit/movement/interaction。TPS camera 不得通过墙角窥视给 Gameplay Knowledge/Lock-on/Secret discovery。

## 18.2 Controller first — CANON

核心 UI 必须 controller-only 可完成；Radial 是动态 0..N selection surface，不固定 8 格。

## 18.3 Aim Assist — CANON DIRECTION

Adaptive medium baseline：不同 Weapon/Input 使用不同 friction/rotation；Sniper低、Shotgun近距、Melee独立辅助、Gyro 减弱 rotation assist。Aim Assist 不改 hitbox/projectile truth，不发现隐藏目标。

## 18.4 Enemy Health UI — CANON

普通 Enemy 不常驻 overhead bar；Aim/Hit/Scan/Ping/focus 时 contextual，Boss 用专用动态 vitals/parts UI。Settings 可 Off/Contextual/Always nearby known。

## 18.5 Damage Numbers — CANON

默认 Aggregated。Projectile/Pellet/DoT/Reaction/Summon 按 Target/AttackRoot/source/time/category 聚合，保留 Crit/Weakpoint/Reaction/Shield/Armor/Health flags。Settings 支持 Off/Major/Aggregated/Detailed/Per-hit。

## 18.6 Teammate Outline — CANON

Contextual：可见时弱；遮挡/Downed/Grabbed/Critical carrier/Separated 时增强。Settings Off/Marker/Contextual/Always。

## 18.7 Left-handed viewmodel — CANON

左右手 viewmodel 可选，不改变 canonical muzzle/hit。

## 18.8 Accessibility — CANON DIRECTION

- Subtitle/SDH；
- critical cue 至少双通道；
- low dynamic range/night audio；
- reduced camera shake/motion；
- color 不是唯一信息；
- Support direction input 可简化 accessibility mode，但成本/结果相同。

---

# 19. Audio / Music / Voice / Subtitle / Haptics

## 19.1 Semantic Audio Event — CANON

Gameplay 发语义事件，Audio backend 决定 clip/layer/spatialization。WeaponFire、ArmorBreak、PartSever、BossTelegraph、ObjectiveState、Footstep、EnvironmentReaction 等都不由音频资产本身驱动 gameplay。

## 19.2 Audio Bus / Critical Cue — CANON DIRECTION

Bus 0..N data-driven；Official 常用 Master/Music/SFX/Weapons/Dialogue/VoiceChat/UI/Ambience/CriticalCue。Critical cue（Boss lethal、Downed、Objective critical）不能被普通 gunfire/music/voice 完全掩盖。

## 19.3 Audio virtualization / Horde audio — CANON

- 不为5000 AI保持5000独立 audio voice；
- individual → cluster → virtualized；
- Horde 通过 crowd beds + 少量高价值 individual cues；
- Operation Horde 重点使用 Faction-specific 叫声/脚步/抓挠/机械启动声作为预兆。

## 19.4 Dynamic Music — CANON DIRECTION

Music 读取高层 CombatIntensity/Momentum/Boss/Faction/Biome/Quiet/Objective/LastChance/Victory 等 semantic state，不驱动 gameplay。Boss/Last Chance music 不假定固定三阶段。

## 19.5 Subtitle / SDH — CANON

- Gameplay-critical spoken info 必须字幕；
- Speaker/priority/direction/location semantic metadata；
- Critical subtitle 优先；
- directional subtitle 不泄露非法隐藏信息；
- SDH 可显示 `[sniper charging]`、`[door grinding]` 等，但不默认把所有 ambience 变文字噪声。

## 19.6 Voice Chat — CANON

Public Quick Match：

- Voice available；
- 默认 Push-to-Talk；
- Team Voice 是全队 global，不因距离/不同Room失声；
- 不采用 proximity-only 作为 Official 默认；
- Party/Team membership 相同可合并 channel；
- Voice 与 gameplay authority 解耦，Host migration 不应切断语音；
- Ping/Quick Chat/Text 必须形成完整 non-voice alternative；
- 不做默认长期 raw voice recording。

## 19.7 Haptics / Cue parity — CANON DIRECTION

Critical gameplay cue 由 semantic definition 同时映射 Audio/Visual/Haptic/Subtitle；presentation 变化不改 canonical timing。

---

# 20. Co-op / Bots / Communication / Social

## 20.1 Bots — CANON

- Optional Bots，默认 OFF；
- Solo 真正可独立玩；
- 可加0–3 AI teammates；
- Bot 使用同样 Character/Weapon/Downed/Ammo rules，不给隐藏永久资源优势；
- Human join 可替换 Bot slot；
- Bots 不做重大 Glyph/Forbidden/Gamble/Fusion/唯一团队资源等最终战略决定。

## 20.2 Bot commands — CANON

基础语义：

- Stay Here；
- On Me；
- Defend Here；
- Take this；
- Use Tool / handle pinged object。

Bot 默认不自主拿走珍贵 scarce resources；Ping/Context command 可授权。Human 全倒时 Bot 可打破 Stay 去救人。

## 20.3 Ping / Quick Chat / Text — CANON

- Ping 纯 Ping/communication，不再内置 Scan；
- Quick Chat 用 semantic intent IDs（Need Ammo/Healing/Group Up/Wait/Ready/Thanks/Sorry/Enemy/Go Here 等）；
- Text 默认 Team/Party；Official 不把 global strangers chat 作为核心；
- spam aggregation/cooldown；
- Chat/Quick Chat 不暂停 online simulation。

## 20.4 Social safety — CANON DIRECTION

- granular mute/block；
- Recent Players；
- Public Quick Match Vote Kick，NetworkHost 无单方面 owner kick；
- Private owner 可移除 private session 玩家；
- AFK warning→可能 Bot takeover/protection→vote/admin removal，不做轻微AFK永久惩罚；
- minimal data retention；
- Host reliability 与“社会信用”分开。

## 20.5 Duplicate character / public loot — CANON

Duplicate characters 允许；Team supply 是公共 world content。高价值 Weapon/Relic Shared Draft 防抢；普通 resource 保持自由分配。

---

# 21. Network / Hosting / Authority

## 21.1 Authority model — CANON

> **Server-authoritative, player-hosted by default, host-migratable, dedicated-capable.**

- Solo：本机运行 Authority Server Runtime；offline-capable；
- Friends/Private/Public Quick Match：选择的一名 Player PC 运行 authoritative Server Runtime + Client；
- Steam/relay/identity/lobby 提供连接层，不做每局官方服务器强依赖；
- Community Dedicated 支持；
- Future Official Dedicated 可以同一 Runtime 部署，但不是核心成本前提。

## 21.2 Host selection — CANON

Host 不等于 Party Leader。评估：CPU headroom、uplink、jitter/loss、NAT/relay、stability/thermal。Steam Deck 可 host，但有更强稳定 PC 时降低优先级。

## 21.3 Host Migration — CANON

- recovery checkpoint/journal/standby candidates；
- Host loss 时 freeze Simulation Time；
- elect new host；
- new Authority Epoch；
- 防 split-brain；
- AI/RNG/loot/director/body parts/mission/projectiles/actions 保持；
- graceful transfer 支持。

## 21.4 Account authority — CANON

Host 不能直接写其他玩家 Account；Session 只产出 structured claims/result，由各账号/backend/validation 层处理。

## 21.5 Bastion hosting — CANON

当前 Bastion = Personal/Party Hub，player-hosted；HubOwner ≠ NetworkHost ≠ PartyLeader。当前不做公共50人MMO Bastion；底层保留未来 AOI/capacity profile 扩展。

---

# 22. Performance / Technical Architecture

## 22.1 最高工程优先级 — CANON

**Gameplay/Simulation performance 是第一工程优先级。** 尤其：AI、projectiles、hit detection、networking、ECS/memory/jobs、physics/nav/spatial/serialization、host migration。

God Build 合法结果不能因为性能被偷偷删掉。

## 22.2 Entity / Memory — CANON DIRECTION

- ECS/archetype/chunk/SoA；
- hot/cold split；
- stable handle = index + generation；
- steady-state hot path 目标接近0 general heap allocation；
- systems query capability/tags，不查 giant inheritance tree。

## 22.3 Jobs / Events — CANON DIRECTION

- TaskGraph/DAG；
- worker-local buffers；
- deterministic commit；
- Event/Command/Transaction 分开；
- Dirty dependency incremental compile；
- high-frequency trigger/event fanout 编译/聚合。

## 22.4 Projectiles / Physics / Spatial — CANON DIRECTION

- Projectile SoA/batched queries；
- gameplay physics 与 presentation physics 分离；
- hierarchical spatial partition/regions/cells/local coords/origin rebasing；
- hierarchical nav/flow/cohort route sharing；
- same-faction candidate early filtering。

## 22.5 Network replication — CANON DIRECTION

- AOI/deltas/dirty masks/semantic relevance；
- 不复制整个世界；
- unified serialization schema/codegen；
- snapshot+journal；
- deterministic semantic RNG hierarchy。

## 22.6 QoS / Budget — CANON

性能系统可以降低：

- presentation density；
- VFX；
- audio voices；
- distant representation；
- animation fidelity。

不能偷偷减少：

- canonical damage；
- canonical enemy count（在模式承诺范围内）；
- legitimate projectile/proc/summon outcomes。

## 22.7 Benchmark targets — TEST

- 1k / 2.5k / 5k AI；
- 10k projectiles；
- 50k projectile torture test（极限工具目标）；
- dynamic anatomy / many tentacles；
- 4p baseline + future large mod stress；
- 4p high-utility/proc God Build；
- Steam Deck thermal soak；
- host migration under active combat。

---

# 23. Dynamic Anatomy / Entity Composition

## 23.1 Composition — CANON

Player/Enemy/Boss/Vehicle/Summon 都是 components/profiles/tags 的组合，不是 giant class inheritance。

## 23.2 Anatomy Graph — CANON

BodyPartGraph / AnatomyGraph 支持0..N parts：stable IDs、topology、tags、hit volume、integrity/armor、functions、sever/regrow/add/remove/replace/transform。

Human 只是 Official anatomy profile；支持 Blob/Hydra/Centipede/Tentacle horror/Drone/Vehicle/Machine/Boss modules。

## 23.3 Capabilities — CANON

Part 提供 Manipulator/Locomotor/Sensor/WeaponMount/Flight/Grab 等 capabilities；hot path 读取 CompiledCapabilityProfile，不每 tick 解释 graph。

## 23.4 Player vs Enemy dismemberment — CANON

Enemy 可严重肢解；Player Official Standard 不做长期断肢惩罚/跛行系统。

---

# 24. Hub / Bastion / Permanent Progression

## 24.1 Horizontal progression — CANON

永久 Account progression 不提供必须的永久 Combat stats。

可解锁/记录：

- Character；
- Weapon/Utility/Relic/Spell pool eligibility；
- cosmetics / titles；
- Knowledge/Archive；
- Fusion discovery；
- Operation discovery；
- Test Chamber；
- challenge/record/history；
- mod/scenario content。

不做“账号等级低所以伤害少30%”。

## 24.2 Archive Credits / Knowledge — CANON DIRECTION

过去已定的 Archive Credits 作为横向 account currency/knowledge progression 仍未与新版 Support economy 冲突，但具体命名/结算需要 Phase 0 再统一。Layer-banked/Uploaded Knowledge 可在 Operation 失败后保留。

## 24.3 No permanent gear vault — CANON

Run-grown Weapon/Relic/Spell/Utility 不作为下局永久 combat power。可以保存 Build snapshot/history/showcase，不带战斗实例回下一 Run。

## 24.4 Bastion — CANON DIRECTION

- Physical hub + quick menu；
- Services 可有物理表现，但重复交互可 shortcut；
- Archive 是知识/调查，不是 +damage tech tree；
- Test Chamber 使用真实 Scenario system；
- trophies/history/cosmetics 可以永久展示。

---

# 25. Lore / Narrative Canon Audit

> 本节把“已确认世界规则”和“仍需 Phase 0 确认的 Story Spine”分开，避免把助手建议误当已拍板故事。

## 25.1 已确认世界核心 — CANON

- Resonance；
- Arcane / Holy / Void 作为世界中已讨论的 Resonance/超常领域概念；
- First Builders；
- JANUS；
- Breach；
- Machine Secession；
- Pale Bloom；
- Great Schism / Schism；
- Necropolis；
- Folding / Fold；
- Bastion；
- 当前 Expedition/Operation 时代。

## 25.2 Sacred Timeline — CANON

> **Fold changes space, not history.**

- 不用时间循环解释重复 Run；
- 世界只有一个 Sacred Timeline；
- Operation/Descent 必须找到与此兼容的 canon 表达。

## 25.3 First Builder Glyph — CANON

- 固定 conceptual glyph language；
- symbols/sequences 跨 Run/语言固定；
- 通常不普通本地化；
- 错误序列一般不给反馈；
- Deep/Forbidden sequence 是最深秘密，不是普通 Main Quest password。

## 25.4 Main narrative outcome — CANON

用户已选择“Hybrid”主线结果：

- Core Narrative/Revelation Arc 可以真正完成；
- 玩家能理解 First Builders/JANUS/Folding/Bastion/Containment 的核心真相；
- 存在 Final Revelation Expedition；
- 它解决/改变的是核心局部 containment/state，不是“拯救整个宇宙”；
- Post-Revelation Bastion/NPC/Archive 必须承认玩家已经完成；
- Operations/Descent/Endless/Secrets/Forbidden 继续存在。

核心原则：

> **Core Mystery can be solved. The universe cannot be solved.**

## 25.5 Recovered working historical sequence — NEEDS CANON CONFIRMATION

当前可恢复的历史排序为：

> First Builders → Resonance era → JANUS → First Breach → Machine Secession → Pale Bloom → Great Schism → Necropolis → Folding → Bastion → Current Expeditions。

**状态：**顺序来自可恢复历史讨论，但每个事件之间的具体因果、谁创造 JANUS、各事件相隔多久、Pale Bloom/Schism/Necropolis 的精确定义仍需要 Phase 0 Narrative Audit 正式确认。

## 25.6 Operation canon — CANON DIRECTION / 需补写

Operation 是实际发生的 field missions：Bastion/Hub 派出玩家进入失控/未知/敌对 Facility，执行任务、回收 Knowledge/Scrap/Data、改变局部世界状态。

## 25.7 Descent canon — OPEN HIGH PRIORITY

当前最佳工作方向：Descent 是真实进入高度不稳定的 Fold/Resonance-depth 区域，空间不断重组，因此比普通 Operation 更疯狂、更高 Relic/Fusion density；不是“时间循环模拟器”。

但这一解释**尚未被用户正式拍板**，必须在 Phase 0 Canon Freeze 解决。

## 25.8 Failure canon — OPEN / DIRECTION

Gameplay failure 不要求每一次都写入主线历史为“主角真的死一次又复活”。成功/Banked Knowledge 可以成为 Canon record；失败 Run 属于 aborted attempt/gameplay possibility。具体叙事包装待 Phase 0。

## 25.9 Main Story curve — OPEN / WORKING

尚未用户正式批准的工作结构：

1. The Assignment — 玩家建立世界工作模型；
2. The Contradictions — Facility/JANUS/历史证据开始不一致；
3. The First Truth — 第一个无法继续用“事故”解释的重大真相；
4. The Cost of Containment — 理解现有残酷系统为何存在；
5. Final Revelation — 解开核心谜团但留下宇宙更深层未知。

**这五幕不是 Canon，必须在 Phase 0 讨论。**

## 25.10 Public player name — OPEN / RENAME REQUIRED

`Reclaimer` 历史上作为玩家称呼，但 Rogue Core 已有强烈同名/相似用法；市场/SEO/品牌层建议重新命名。新名称尚未定。

---

# 26. Visual DNA / Art Direction

## 26.1 当前结论 — CANON DIRECTION

“Low-res retro dark sci-fi FPS”不能是项目唯一品牌身份。Moros/HELLBREAK 等已经覆盖这个表面空间；Generic sci-fi asset-pack look 是明确失败状态。

Canonical gameplay 是真3D；Presentation 可以支持 Retro / stylized / Full3D backend，但品牌必须拥有自己的视觉语法。

## 26.2 Visual DNA Bible — OPEN HIGH PRIORITY

必须在大量正式 asset production 前确认：

- Human/JANUS architecture grammar；
- First Builder shape language；
- Fold spatial grammar；
- Resonance VFX geometry；
- materials/lighting；
- faction motifs；
- Character silhouettes；
- Weapon silhouettes；
- Staff/Spell visual language；
- UI typography/iconography；
- animation cadence；
- color-independent identification。

目标：只看一张截图也知道是我们的游戏。

## 26.3 Visual lore consistency — CANON DIRECTION

美术不是“看起来酷”的独立部门。Lore reason → shape/material → gameplay readability 必须一致。

---

# 27. Mods / SDK / UGC

## 27.1 Mod philosophy — CANON

- Data → Graph → Sandbox Script；native 明确 unsandboxed；
- Official content 尽量走 public extension points；
- package namespaces/manifests/dependencies/versions/hashes/permissions；
- gameplay mods 固定在 active/suspended run，presentation mods 更灵活；
- mod profile/modpack/version rollback/staging；
- mod performance attribution/quota/fault isolation。

## 27.2 Unified Graph / IR — CANON DIRECTION

Entity/Anatomy/Ability/Relic/Fusion/Mission 等尽量共享 node compiler/IR/runtime/debugger，而不是每个系统一套脚本架构。

## 27.3 SDK — CANON DIRECTION

目标：Entity/Anatomy Graph editor、Capability inspector、Room/Biome/Puzzle/Mission editor、Scenario test、Profiler、CLI/headless build/cook/validate。

## 27.4 Scenario Forge — CANON DIRECTION

公开版延后，但内部从第一天使用数据/图工具制作 Official missions。顺序：内部→Vertical Slice→精选 modders→公开 polish。

## 27.5 Total Conversion — CANON

TC 可替换 player-facing game/menu/progression；Official Base Game content entitlement 与 free runtime 分离。

## 27.6 Demo mod runtime — CANON DIRECTION

Demo 目标拥有完整 mod runtime/Workshop/TC；Premium 价值主要来自 Official content/progression/free updates，不通过人工锁 runtime 阻止社区。

---

# 28. Commercial / Platform / Distribution

## 28.1 Platform — CANON

Steam/PC first；Steam Deck 官方支持；future console/crossplay 可扩展但不承诺。

## 28.2 Business model — CANON

- Premium buy-to-play Base Game；
- 持续免费内容更新；
- Paid Cosmetic DLC；
- Supporter Packs；
- Community Mods 全免费。

明确不做：

- premium currency；
- loot box；
- battle pass；
- rotating FOMO store；
- daily login rewards；
- paid combat power；
- official paid mods marketplace。

## 28.3 Early access / testing — CANON DIRECTION

- 不做 Paid Early Access；
- internal/closed/Steam Playtests；
- benchmark/public tests；
- Demo → Premium 1.0；
- 1.0 开始更强 save/API compatibility era。

## 28.4 Demo — CANON DIRECTION / NEEDS RECONCILIATION

早期可恢复设计曾要求 Demo：

- 15–25分钟；
- 有完整开中结；
- 下载小；
- 从一开始是真3D；
- 支持 Workshop/Custom Scenario/TC。

当前 Operation 正式时长更长，因此 **Demo 是专门缩短 Template 还是 Descent/Operation 混合体验仍 OPEN**。

Demo progression 早期已定为 Limited Carryover：cosmetics/title/badge/安全horizontal claims可带；Run saves/Archive Credits/Glyph/Forbidden/Main Evidence等不完整继承。需要 Phase 0 再和新版 Knowledge/Operation economy 对齐。

## 28.5 Steam Deck — CANON

- Official support；
- stable 60 FPS（16.67ms frame budget）hard target；
- 降低 rendering/presentation，不减少 canonical gameplay outcomes；
- sustained thermal soak test；
- full controller support。

---

# 29. Engine / Licensing / Selection

## 29.1 Engine — OPEN

用户偏 Unity，但未正式锁。

Unity 重点：DOTS/大量 simulation、agent/code workflow、无销售版税的当前 license economics。  
Unreal 重点：高端 rendering/presentation、成熟 AAA art/animation/lighting tooling。

## 29.2 Engine evaluation — CANON PROCESS

必须使用同一代表性 Prototype 比较：

- 1k/2.5k/5k AI；
- 10k projectiles；
- dynamic anatomy/tentacles；
- 4p network + host migration；
- Retro/Full3D presentation；
- Steam Deck；
- mods/TC；
- Codex/Claude/GPT agent workflow；
- compile/cook/iteration latency；
- license projected cost。

**不因为价格/DOTS/画质单一因素提前锁。**

---

# 30. AI-agent-first Development

## 30.1 Agent as first-class developer — CANON DIRECTION

未来 Codex/Claude/GPT agent 是正式开发工作流的一部分。

要求：

- CLI/API/headless build/test/cook/validate/profile/content pipelines；
- text/semantic source of truth；
- machine-readable Architecture contracts + ADR；
- Agent TaskContext/plans/change manifests/package ownership；
- drift detection；
- independent review；
- rollback/checkpoints；
- screenshot/depth/semantic-mask visual inspection；
- deterministic validators 是 blocking truth。

## 30.2 AI-generated assets — CANON DIRECTION

可用于 voice/image/sprite/placeholder/production aid，但全部走同一 source/import/validate/cook/provenance pipeline；manual takeover 永远可用。

---

# 31. QA / Telemetry / Streamer Tooling

## 31.1 Build Evolution Timeline — CANON DIRECTION

记录 Anchor、Connector、Fusion、Loop closed、Pivot、God-build threshold 等重大 Build changes。

## 31.2 Steam Timeline / Clip suggestion — CANON DIRECTION

使用 Steam Game Recording/Timeline integration 标记：First Fusion、proc cascade、mass chain reaction、Boss/Threat reversal、Last Chance、team combo 等；重要事件回溯 root cause→payoff，而不是只标最终爆炸一帧。

## 31.3 Streamer HUD — CANON DIRECTION

显示少量 Build core nodes/Fusions/Loop、隐藏私人信息、保持 gameplay readability；不能提供额外 gameplay knowledge。

## 31.4 EmergenceScore — TEST TOOL

内部可按 topology rewrite、loop depth、proc cascade、multikill、world destruction、cross-player contribution 等筛选真正值得 QA/Marketing review 的 run，不以纯 DPS 作为唯一标准。

---

# 32. Difficulty / Storyteller / Mutator / Challenge

## 32.1 Difficulty — INHERITED CANON, 需双模式调参

所有 Official Difficulties 从第一次启动就开放：

- Relaxed；
- Standard（推荐）；
- Veteran；
- Nightmare；
- Cataclysm。

原则：

- 高难度优先提高 threat fronts、AI coordination、mutation、hazard、resource/revive pressure；
- 不优先用纯 HP sponge；
- 不 input-read / wallhack / hidden anti-build；
- PlayerCount / Storyteller / Difficulty 分开；
- Higher difficulty 可以提高 Archive/cosmetic/record efficiency，但不锁核心内容。

**需要后续做：**分别定义 Operation 与 Descent 的 Difficulty dimension，避免同一个“+资源稀缺”套两种模式。

## 32.2 Storyteller / Meta-Director — INHERITED CANON DIRECTION

Storyteller 是规则化 policy，不使用 LLM 在 gameplay runtime 做不可复现的决策。

历史候选：Commander、Butcher、Sadist、Madman、Architect、Survivor、CHAOS 等。

- Storyteller 影响 encounter pacing/combination/world events；
- 不偷偷改玩家 stats；
- Difficulty 不秘密改变 Storyteller identity。

`Black Swan`：极低概率、独立 RNG 的超稀有事件，不进入 completion checklist；可恢复，不应因没遇到而“100%无法完成”。

**状态：**Storyteller 如何分别服务 Operation/Descent 需要 Reset 后重新整合，当前保留为技术/内容方向。

## 32.3 Mutators / Daily / Challenges — INHERITED CANON DIRECTION

- Mutator 与 Difficulty/Storyteller 分开；
- Daily/Challenge 可以固定 seed/rules/content profile；
- Leaderboards/records 只对明确可比较 rulesets 有意义；
- 不通过日常奖励/FOMO强迫登录；
- Challenge reward 优先 cosmetic/title/history。

---

# 33. Inventory / Shop / Economy / Respec / Transit — Reset后待模式化整合

## 33.1 General Carry — INHERITED TEST

过去已确认 `Small Carry`：active/equipped 之外有小型 General Carry，早期目标约4 item slots；Ammo/material/relic/quick consumable/strategic items 分开，不占这些槽；Dormant carry 不运行 passive/listeners。

**当前状态：OPEN-REVIEW。** 新版 Operation 强调 world-physical resources、Relic 无限吸收、Weapon/Utility直接装备，General Carry 是否仍需要4格、哪些东西可进入，必须在 BLACKSTART inventory prototype 重审，不能直接沿用旧UI。

## 33.2 Shop — INHERITED / MODE-SPECIFIC OPEN

旧方案曾锁 `Mixed Shop`：shared world stock + personal offers。新版 Operation 的核心补给已经由 Support/Facility world resources 承担，因此**Operation 不应默认塞一个 Roguelike商店**。

可能保留位置：

- Bastion services；
- Descent shop/reward room；
- 特定 Operation world service（Facility fabricator/merchant）作为 Template 内容。

最终 storefront/offer semantics 需要模式化再确认。

## 33.3 Economy — CONFLICT-RESOLVED DIRECTION

旧 `Personal Run Currency + Team Strategic resources` 的抽象经济不能直接覆盖新版 Operation。

当前：

- Operation Team Support = Knowledge/Scrap 支撑；
- Power/Mission Cells = 实体/战略资源；
- Relic/Weapon/Prototype 由 world/drop/Support；
- Descent 可重新设计更传统 Run currency/shop。

## 33.4 Respec — INHERITED CANON DIRECTION

旧选择 B：重大 Run choice 只能通过真实 Reconfiguration Service/Station/Device + Run-local cost 重配，不允许 pause menu 免费切换。不能 reroll loot/RNG/history。

当前无明显冲突，保留；但具体 Operation/Descent 可用性待 prototype。

## 33.5 Fast Travel / Transit — INHERITED CANON DIRECTION

旧选择 D：真实有限 Transit Network，需发现/激活 node/link；不是任意房间 teleport；在 active combat/high threat 中不可用；可受 power/faction/world state 影响。

新版 Operation 的 No Mandatory Backtracking 降低其“补救跑图”的必要性，但 Transit 仍是 Facility world system/Cart outcome；Descent 可用于已探索区域回流。保留为世界系统，不当主玩法。

---

# 34. Map / Navigation / Information UI

## 34.1 Navigation HUD — INHERITED CANON

旧选择 C Hybrid：

- Combat HUD：轻量 local navigation + compass；
- 已探索拓扑、connector、队友、Ping、known objective；
- Full Map 显示完整已发现 graph；
- 无 omniscient enemy radar；
- Unknown/Secret topology 未发现前不显示；
- 支持 vertical/Fold topology。

与新版 `Information not free HUD` 一致：Terminal Search 成功后才把某目标变成 known waypoint。

## 34.2 Map knowledge — CANON

Camera TPS、photo mode、graphics tricks 不能通过看见 pixel 自动产生 gameplay knowledge；knowledge 由合法 Player observation/sense/terminal/system event确认。

---

# 35. Narrative Delivery / Dialogue / Archive

## 35.1 Delivery channels — INHERITED CANON DIRECTION

Narrative 不应该以长 exposition 抢玩法。主要渠道：

- Operation briefing；
- Physical Terminal logs/data；
- world state/environmental storytelling；
- Bastion NPC/Handler；
- Archive/Knowledge；
- short radio/dialogue；
- Final Revelation 等少量高价值 sequence。

## 35.2 Dialogue system — INHERITED CANON DIRECTION

- Dialogue semantic state 与 voice playback 分离；
- combat 可按 conversation definition 暂停/降级为radio/继续/中断；
- 重要内容可在 Archive 恢复；
- skip/fast-forward 只影响 presentation，不重复/漏掉 committed world consequences；
- conversation choice 0..N，重大 team choice 才走 SharedDecision；
- online client 可按自己的 language/subtitle/skip preference 播放。

## 35.3 Localization — INHERITED CANON

Text/subtitle/voice language 独立；缺 voice asset 可 fallback；CJK/RTL/line-wrap进入 localization CI。First Builder Glyph 通常不按普通语言本地化。

---

# 36. Versioning / Save / Compatibility

## 36.1 Save / network schema — INHERITED CANON DIRECTION

Unified serialization schema/codegen；Save/Network/HostMigration 使用不同 profile，但共享语义 schema。

## 36.2 Run save — CANON DIRECTION

Snapshot + journal；strong transaction boundaries；Fusion/Support/Cart/World state 必须原子、可恢复。

## 36.3 1.0 compatibility — CANON DIRECTION

1.0 进入更强 save/API compatibility era。此前 Playtest/Demo 可以更积极 breaking change，但要有 migration/clear messaging。

## 36.4 Mod profile pinning — CANON

Gameplay mods/content versions 固定到 active/suspended run；避免恢复时静默使用新版逻辑改变结果。

---

# 37. 重大历史决策登记表（A/B/C/D 选择与后续覆盖）

> 这一节专门保存“我们到底选过什么”，防止未来只记住结论却忘记是哪个分支。被 Reset 覆盖的仍列出但标 LEGACY。

| 决策 | 用户选择 | 当前状态 |
|---|---|---|
| Public Team Voice topology | A — Global Team Voice | CANON |
| 旧 Layer Transition Recovery | D — Baseline floor, not reset | Operation: LEGACY；Descent: 可作为 profile TEST |
| Enemy same-faction damage | A — 默认不互伤 | CANON |
| Same-faction普通攻击拦截 | A — 不拦普通攻击 | CANON |
| Enemy blocking | C — Soft Horde + explicit Hard blockers | CANON |
| Basic flashlight | A — 人人基础手电 | CANON |
| 旧 Advanced Sensor baseline | A，但后改“Scan是战斗标记”，再经Reset改为Utility | LEGACY→当前 Scan Utility |
| Recoil style | C — Hybrid learnable, easy-control PvE | CANON |
| Utility baseline concept | C — Quick Utility/Throwable | 发展为2 Utility slots，CANON |
| 旧 Utility Recharge | C — Rechargeable Charges | Operation默认快速Recharge：LEGACY；Descent可用 |
| Utility shared cooldown | A — 无Global cooldown | CANON（具体Operation资源另算） |
| Revive Utility | B — 专门Utility/Build可Revive | CANON |
| Revive recovery | B — 中等Health + 短Grace | CANON |
| 旧 Character Active slots | B — 2个 | LEGACY；Reset后1个 Signature Active |
| Separate Ultimate slot | B — 不设通用Ultimate | CANON |
| Duplicate Character | A — 允许 | CANON |
| Mid-run Character swap | A — 不允许 | CANON |
| Layer1 Build guarantee | C — Hybrid guarantee | Descent CANON |
| Fusion discovery | C — Hybrid：知道强互动，不知道首次结果 | CANON |
| Fusion determinism | A — 条件满足结果确定 | CANON |
| Fusion consumption model | 用户纠正：A+B消失生成C | CANON |
| Fusion commit | A — 自动发生，Isaac-like | CANON |
| Fusion inheritance | C — Compatible preserve + recipe convert | CANON |
| Operation/Descent双模式 | 用户提出并批准 | CANON |
| Operation Earned Safety | C | CANON |
| Door system | C — 普通Delay，Security战略Seal | CANON |
| Alert decay | C曾选，但随后用户指出Alarm不适合并改DRG式Horde | LEGACY |
| Operation generation | C — Curated Template + Procedural Situation | CANON |
| Operation Wipe Recovery Anchor | 助手建议B，被用户否决 | LEGACY：无Gameplay checkpoint |
| Support pricing | B — Meter→discrete Support Charges | CANON |
| Supply ownership | Team/Public contents | CANON |
| Equipment/Accessory | 删除，只留Relic | CANON |
| Relic slots | Isaac式无限累计 | CANON |
| Staff spell count | 默认3，上限6，局内扩容 | CANON profile |
| Descent layer length | 约12 min ×5 | CANON pacing target |
| Facility Cart commit | A — 任意操作者直接Commit | CANON |

---

# 38. GTFO 社区建议文件：采纳/改造/拒绝统计

上传的社区建议被当作灵感，不是需求列表。

## 38.1 已采纳/改造

- Lobby失败显示明确原因；
- Supplies 可存回 empty locker/storage；
- Lefty viewmodel；
- 不可永久击杀但受伤害影响的 Threat → Predator Reversal；
- 更多不同 Melee → Hammer/Knife/Spear/Sword prototype；
- Portable fog/environment tool → Utility/Field 系统；
- Suppressed weapon → Acoustic stimulus；
- Bot Stay / On Me / Take / Tool use；
- Bot 不自动浪费 scarce resources；
- item pickup/swap QoL；
- sort/filter build items；
- distinctive operation/combat music；
- moving battlefield 作为未来 mission grammar 灵感。

## 38.2 转成 Rule-break / Mod/Descent 内容

- Trip mine on players → attachable mine Relic/Fusion；
- gun explodes on fire → Curse/Volatile Chamber；
- absurd recoil → Chaos mutator/cursed weapon only；
- player-controlled enemies / Among Us → 不进 core，可留给 mods/TC。

## 38.3 拒绝作为核心

- 所有枪统一巨 recoil；
- 删除 reload animation；
- 无限“Mom spawns baby X”换皮 enemy；
- FOMO限时奖励；
- 没 gameplay价值的纯梗 feature。

---

# 39. LEGACY / 已被覆盖的旧设计

以下内容不得被未来旧聊天“复活”：

1. **Hard Classes / mandatory Warrior-Healer-Tank-Mage composition** → Soft Archetype + 1 Signature Active。
2. **2 Character Active Abilities** → 1 Signature Active。
3. **Universal Weapon Active button** → 删除；weapon behavior使用Fire/ADS/R/hold/context。
4. **Scan as baseline universal ability / Scan merged with Ping** → 删除；Scan 是 Utility，Ping纯Ping。
5. **Equipment + Accessory + Relic** → Equipment/Accessory删除，只留Relic。
6. **Fixed Relic slots** → Isaac式无限累计。
7. **全游戏固定5 Layers** → 只有 Descent 5 Layers；Operation单Mission。
8. **Operation Layer baseline recovery/reset** → Operation持续资源，无阶段Reset。
9. **Operation所有Utility快速免费Recharge** → Operation有限/technical resource；Descent宽松。
10. **传统Extraction shooter/搜打撤核心** → 明确不做：无bring-in gear/stash-loss主循环。
11. **Persistent Facility Alarm / Alarm levels** → 删除通用系统；改 Horde/Objectives/System responses。
12. **Combat=被发现后的错误状态** → 删除；Operation更像mission-driven co-op PvE。
13. **Gameplay Recovery Anchor/Checkpoint rollback** → 删除；Operation可真实失败。
14. **Mandatory backtracking** → 禁止作为主线时长填充。
15. **Extraction hard countdown** → 删除；用世界恶化表达“现在走”。
16. **Retro dark sci-fi =唯一品牌** → 删除；需要独立Visual DNA。
17. **每个人永久自带完整Staff当无Ammo保底** → 删除；Staff占正常Weapon slot。
18. **Melee“几乎必然换血”作为平衡** → 删除；Skill应显著降低Health cost。
19. **复杂连续Power allocation/Excel** → 删除；小整数Cart。
20. **所有重大Team决定投票** → 普通Facility Cart由任意合法操作者直接Commit；仅极端终局动作可SharedDecision。
21. **Supply通过Facility Terminal订购** → 删除；Hub Support Beacon独立。
22. **Knowledge直接当Ammo货币** → 删除；Knowledge/Scrap贡献Support，同时Knowledge有永久研究价值。
23. **Fusion是可逆A+B active state** → 删除；Fusion是真正consume→C。
24. **Fusion需要Forge/手动确认** → 删除；满足合法Recipe后自动。
25. **公开Scenario Editor先做** → 延后；先内部工具。

---

# 40. 当前数字/规模统计（Canon vs Test）

| 项目 | 当前值 | 状态 |
|---|---:|---|
| 玩家人数 | 1–4 | CANON |
| Operation时长 | ~40–70 min | DIRECTION |
| BLACKSTART slice | ~35–45 min | TEST |
| Descent Layers | 5 | CANON |
| Descent单Layer | ~12 min平均 | CANON pacing target |
| Descent标准Run | ~60 min上下 | CANON pacing target |
| Weapon slots | 2 | Official CANON profile |
| Utility slots | 2 | Official CANON profile |
| Signature Active | 1 | CANON |
| Staff默认Spell | 3 | Official profile |
| Staff目标上限 | 6 | Official profile |
| Melee prototype | 4把 | TEST set |
| Character prototype | 3个Active原型 | TEST |
| Relic first pool | 30 | TEST |
| Curated Fusion first pool | 6–10 | TEST |
| Operation normal Support Charges | ~2–3 | TEST |
| Operation failure token payout | ~50% | TEST |
| Emergency Recovery Floor | ~20–25% HealthCap | TEST |
| Revive Health | ~35–50% HealthCap | TEST |
| Difficulties | 5，全开 | CANON |
| Steam Deck | 60 FPS（16.67ms frame budget）hard target | CANON target |
| AI stress | 1k/2.5k/5k | TEST benchmark |
| Projectile stress | 10k；50k torture | TEST benchmark |
| Public Quick Match voice | Global Team Voice，PTT default | CANON |
| Default Player FF | 0% | CANON |

---

# 41. 当前仍需确认的东西（按返工风险排序）

## 41.1 Phase 0：必须在大量制作前确认

1. **完整 Narrative Canon**：First Builders/JANUS/Breach/Machine Secession/Pale Bloom/Schism/Necropolis/Fold/Bastion 的因果与精确时间线；
2. **Descent 的 Canon 解释**；
3. **Player/Expeditioner 的公开名称**（`Reclaimer`需要改）；
4. **Main Story spine/acts 与 Final Revelation 的具体内容**；
5. **Visual DNA Bible**；
6. **Staff/Spell 在世界观里到底是什么（技术/Resonance/混合），以及 Fusion/Relic 的 lore 解释**；
7. **Character Signature Active 的世界观来源规则**；
8. **Demo 如何和当前双模式/Canon对齐**。

## 41.2 Combat prototype 必须验证

- Weapon swap手感；
- 4 Melee差异；
- Staff first 3 spells；
- Mana/Heat节奏；
- Energy为什么不成为数学上位；
- 3 Signature Active 是否像Hero Shooter；
- Utility select/controller flow。

## 41.3 Build prototype 必须验证

- 30 Relics；
- 6–10 Fusion recipes；
- Proc graph readability；
- sustainable loop；
- Fusion inheritance；
- Spell/Fusion interaction。

## 41.4 Operation prototype 必须验证

- Support具体资源价值；
- Facility local resource coverage；
- Relic Pod是否永远比Ammo更优；
- Horde/Objective pressure节奏；
- Cart固定meta风险；
- No-backtracking forward topology；
- Failure token比例；
- Earned Safety 是否真的让玩家喘气。

## 41.5 Descent prototype 必须验证

- 一Layer 12分钟是否真的合适；
- 每层Reward cadence；
- 每层Boss是否需要；
- Layer 3以前是否已经有明显Transformation；
- Layer 5是否真的God-build，而不是+damage堆叠；
- Support/Spell/Relic density。

## 41.6 技术 OPEN

- Unity vs Unreal；
- exact server/network stack/provider；
- canonical renderer/style pipeline；
- public Scenario Forge timeline；
- future dedicated/large hub scaling milestones。

## 41.7 UNRECOVERED / NEEDS SOURCE IF FOUND

- 任何真正被删除、且没有Summary/Memory/File痕迹的旧微观对白、角色名字、Lore细节；
- 早期Class原型的精确数值/所有技能文本；
- 某些更早版本的完整Narrative草稿（如果用户手头仍有，应未来导入审计，而不是由模型猜）。

---

# 42. 全项目 Preproduction 流程 — CURRENT

## Phase -1 — 全项目统计 / Canon Audit（当前）

目标：把所有可恢复决定归入 CANON/TEST/OPEN/LEGACY/UNRECOVERED，解决隐性冲突。**本文件即当前产物。**

## Phase 0A — Narrative Canon Freeze

确认世界前提、历史因果、模式Canon、主线、结局、Forbidden、Player身份、Character/Lore规则。

## Phase 0B — Visual DNA Freeze

确认Architecture/First Builder/Fold/Resonance/Faction/Weapon/Spell/UI视觉语言。

## Phase 0C — Cross-system Consistency Audit

逐条检查：

- Lore vs Gameplay；
- Operation vs Descent；
- Resource economy vs Weapon families；
- Character active vs no-class；
- Fusion/Relic vs narrative；
- Networking vs shared world state；
- Modding vs save/network compatibility；
- Visual vs gameplay readability。

## Phase 1 — Combat Sandbox v0.1

Greybox验证：

- AR/Shotgun；
- Hammer/Knife/Spear/Sword；
- Energy weapon；
- Staff + 3 spells；
- 2 Utility prototypes；
- 3 Signature Active prototypes；
- 3–5 Enemy roles。

**Gate：0 Relic也愿意连续打30分钟。**

## Phase 2 — Build Algebra Sandbox

加入30 Relic、6–10 Fusion、Proc-from-proc、Spell reward/Fusion。

**Gate：不是30条独立perks，而是真正能产生很多不同机器。**

## Phase 3 — BLACKSTART Operation Vertical Slice

固定拓扑、35–45分钟，验证 Terminal/Support/Cart/Horde/Forward topology/Failure。

**Gate：不能靠不停发Relic才能不无聊。**

## Phase 4 — Descent Prototype

先做3 Layer验证 high-resource build escalation，再扩正式5×~12 min。

## Phase 5 — Engine Lock / Production Architecture

用真实 Prototype benchmark Unity vs Unreal，最终锁Engine和生产技术栈。

---

# 43. Release / Product Gates

## 43.1 Combat Gate

> 裸Weapon family就好玩。

## 43.2 Operation Gate

玩家自然说出：

- “这群别打，省资源。”
- “先找Terminal。”
- “这个Charge买Ammo还是Relic？”
- “我们前面那个Cart决定把Finale改了。”

而不是“什么时候给我下一个upgrade”。

## 43.3 Descent Gate

玩家自然说出：

> “等等，我这个Proc为什么开始自己循环了？”

不是：

> “我最后+240% damage。”

## 43.4 Visual Gate

不看Logo/文字，只看截图/短视频，也能认出我们的Facility/First Builder/Fold/Weapon/Spell语言。

## 43.5 Stream Gate

20个不同Run要能自然产生让局外观众问：

> **“他那把武器到底怎么变成这样的？”**

---

# 44. 最终当前 Product Thesis

> **A 1–4 player systemic PvE combat game built around two complementary fantasies:**
>
> **Operations** — solve a real mission inside a living facility, manage resources, acquire information, reshape the situation, and survive the consequences with friends.
>
> **Descent** — take the same combat and build systems off the leash: accumulate Relics, grow a Staff repertoire, fuse items into new forms, close proc loops, and push a run toward controlled catastrophe.

玩家主要购买理由：

1. Weapons/Combat 本身极好玩；
2. Build 是 graph，不是 perk list；
3. Fusion 真正 A+B→C；
4. Operation 给团队真正的问题，而不是只清怪；
5. 同一套系统还能在 Descent 里释放到 God Build；
6. 世界、敌人、任务、Build 会一起参与同一局故事。

---

# 45. SSOT 维护纪律

1. 不再用聊天记录本身作为权威；
2. 新决定必须更新本文；
3. 旧决定不删除历史记录，但降级到 LEGACY；
4. OPEN 不伪装成锁定；
5. TEST 数值不因为写在文档里就自动变Final；
6. 所有新Feature先说明它增强哪个产品支柱；
7. 如果Feature主要作用是“更难/更多/更复杂”而不增加Fun/decision/story，默认拒绝；
8. Preproduction Freeze 完成前，不进入大规模正式Content production。

---

# Appendix A — 当前全项目一句话状态

**产品：**方向清楚。  
**Operation：**核心Loop与系统结构基本成形，数值/Content待验证。  
**Descent：**宏观结构已定，Reward/Layer content待验证。  
**Combat：**规则清楚，但尚未通过Prototype。  
**Build Algebra：**架构哲学强，尚未用30 Relic证明。  
**Narrative：**核心终局规则存在，但完整世界因果/主线仍是最大Preproduction缺口。  
**Visual：**明确知道不能generic，但Visual DNA仍未完成。  
**Networking/Performance/Mods：**技术方向相当完整。  
**Engine：**未锁。  
**Production readiness：**尚未；必须先完成Phase 0 Canon/Visual consistency audit。

# Appendix B — 本版本相对 SSOT v1.0 的主要变化

- 把“Project Archaeology”正式改名为**全项目统计**；
- 扩展详细 Benchmark/学习库并记录“学什么/不学什么”；
- 加入大量 v1.0 漏掉的 Audio/Voice/Social/Networking/Modding/Business/Agent/QA细节；
- 加入完整 decision ledger；
- 加入 narrative recovered timeline + 明确 OPEN；
- 加入 Difficulty/Storyteller/Mutator/Map/Inventory/Shop/Respec等旧非冲突决策和 Reset 后状态；
- 合并最新 Operation 无 Alarm、Horde、Earned Safety、Door、Support Charges、公共Supply、No checkpoint、No mandatory backtracking、No extraction timer；
- 合并最新 Input、4 Melee、Staff 3→6、Descent 12min、Relic 30、失败收益等；
- 将所有被推翻内容集中到 Legacy Ledger，防止未来反复。
