---
doc_id: GOV-SOURCE-MAP
doc_type: governance
stage: ARCHIVE
updated: 2026-09-05
owner_role: 设计证据维护
canon_basis: "SRC-SSOT-2.0 全文；本轮新增证据"
depends_on: ["../sources/ssot-v2.0-original.md", "decision-register.md"]
---

# 源章节与规则迁移索引

MAP-001 · PROPOSED · 来源：本轮文档拆分合同。
源依据均为SRC-SSOT-2.0。行号对应[原快照](../sources/ssot-v2.0-original.md)；包括总标题、§0–§45、§4A/4B、附录A/B。这里只负责定位，不提供第二份玩法数值。新增用户决定与纠正见[证据登记](../sources/evidence-register.md)和[决策登记](decision-register.md)；最新玩家故事合同在[玩家故事与时间线](../gdd/player-story-and-canonical-timeline.md)。

## 全量顶层标题

| 原标题（逐字保留用于覆盖检查） | 源行范围 | 责任文件 | 处理 |
|---|---|---|---|
| # GAME PROJECT — 全项目统计与唯一真相 SSOT v2.0 | L1–L8 | [evidence-register](../sources/evidence-register.md)；[README](../README.md) | 源状态保留；扩写单独标注 |
| # 0. 权威规则、范围与证据等级 | L9–L75 | [authoring-guide](authoring-guide.md)；[evidence-register](../sources/evidence-register.md) | 源状态保留；扩写单独标注 |
| # 1. 项目定义与最高设计哲学 | L76–L144 | [vision](../gdd/game-vision-and-design-pillars.md)；[architecture-and-performance](../technical/architecture-and-performance.md) | 源状态保留；扩写单独标注 |
| # 2. 为什么玩家会买、为什么会继续玩 | L145–L207 | [vision](../gdd/game-vision-and-design-pillars.md) | 源状态保留；扩写单独标注 |
| # 3. 对标/学习库：每款游戏到底学什么 | L208–L397 | [references-and-methods](../research/references-and-methods.md) | 源状态保留；扩写单独标注 |
| # 4. 两个核心模式 | L398–L399 | [vision](../gdd/game-vision-and-design-pillars.md) | 源状态保留；扩写单独标注 |
| # 4A. SYSTEMIC OPERATIONS — 默认/主模式 | L400–L692 | [operations](../gdd/operation-game-mode.md)；[economy-and-support](../gdd/economy-and-support.md)；[world-and-information](../gdd/facility-systems-and-information-rules.md) | 源状态保留；扩写单独标注 |
| # 4B. DESCENT — Build/Combat Power Fantasy 模式 | L693–L755 | [descent](../gdd/descent-future-game-mode.md) | 源状态保留；扩写单独标注 |
| # 5. Player Loadout 与 Input | L756–L802 | [player-and-input](../gdd/player-and-input.md) | 源状态保留；扩写单独标注 |
| # 6. Weapon / Combat Arsenal | L803–L895 | [combat-and-arsenal](../gdd/combat-and-arsenal.md)；[combat-prototypes](../content/combat-prototypes.md) | 源状态保留；扩写单独标注 |
| # 7. Character System | L896–L945 | [player-and-input](../gdd/player-and-input.md)；[combat-prototypes](../content/combat-prototypes.md) | 源状态保留；扩写单独标注 |
| # 8. Utilities | L946–L990 | [player-and-input](../gdd/player-and-input.md)；[economy-and-support](../gdd/economy-and-support.md)；[survival-and-recovery](../gdd/survival-and-recovery.md) | 源状态保留；扩写单独标注 |
| # 9. Relic / Build Algebra / Proc / Fusion | L991–L1083 | [build-algebra](../gdd/field-modifications-and-effect-system.md)；[relics-and-fusions](../content/modification-catalog.md) | 源状态保留；扩写单独标注 |
| # 10. Combat Math / Crit / Reaction | L1084–L1107 | [build-algebra](../gdd/field-modifications-and-effect-system.md) | 源状态保留；扩写单独标注 |
| # 11. Player Movement / Damage / Life State | L1108–L1160 | [player-and-input](../gdd/player-and-input.md)；[survival-and-recovery](../gdd/survival-and-recovery.md) | 源状态保留；扩写单独标注 |
| # 12. Friendly Fire / Faction / Collision | L1161–L1188 | [combat-and-arsenal](../gdd/combat-and-arsenal.md) | 源状态保留；扩写单独标注 |
| # 13. Enemy / AI / Director | L1189–L1250 | [encounters-and-difficulty](../gdd/encounters-and-difficulty.md)；[missions-and-spaces](../gdd/missions-and-spaces.md) | 源状态保留；扩写单独标注 |
| # 14. World Systems / Door / Facility | L1251–L1287 | [world-and-information](../gdd/facility-systems-and-information-rules.md) | 源状态保留；扩写单独标注 |
| # 15. Operation Mission Architecture | L1288–L1337 | [missions-and-spaces](../gdd/missions-and-spaces.md) | 源状态保留；扩写单独标注 |
| # 16. BLACKSTART Vertical Slice — TEST SPEC | L1338–L1387 | [blackstart](../content/blackstart-greybox-mission.md) | 源状态保留；扩写单独标注 |
| # 17. Map / Room / Spatial Generation | L1388–L1406 | [missions-and-spaces](../gdd/missions-and-spaces.md) | 源状态保留；扩写单独标注 |
| # 18. Camera / HUD / Controller / Accessibility | L1407–L1447 | [ux-and-accessibility](../gdd/ux-and-accessibility.md) | 源状态保留；扩写单独标注 |
| # 19. Audio / Music / Voice / Subtitle / Haptics | L1448–L1495 | [audio-and-haptics](../gdd/audio-and-haptics.md)；[coop-and-social](../gdd/coop-and-social.md) | 源状态保留；扩写单独标注 |
| # 20. Co-op / Bots / Communication / Social | L1496–L1542 | [coop-and-social](../gdd/coop-and-social.md) | 源状态保留；扩写单独标注 |
| # 21. Network / Hosting / Authority | L1543–L1578 | [network-and-persistence](../technical/network-and-persistence.md) | 源状态保留；扩写单独标注 |
| # 22. Performance / Technical Architecture | L1579–L1648 | [architecture-and-performance](../technical/architecture-and-performance.md) | 源状态保留；扩写单独标注 |
| # 23. Dynamic Anatomy / Entity Composition | L1649–L1670 | [architecture-and-performance](../technical/architecture-and-performance.md)；[combat-and-arsenal](../gdd/combat-and-arsenal.md) | 源状态保留；扩写单独标注 |
| # 24. Hub / Bastion / Permanent Progression | L1671–L1708 | [progression-and-bastion](../gdd/progression-and-bastion.md) | 源状态保留；扩写单独标注 |
| # 25. Lore / Narrative Canon Audit | L1709–L1798 | [narrative-bible](../gdd/canonical-world-history-and-lore.md)；[central-story-spine](../gdd/player-story-and-canonical-timeline.md)；[world-naming](../gdd/world-naming.md) | 世界事实、中央故事与创作命名责任分开 |
| # 26. Visual DNA / Art Direction | L1799–L1831 | [art-direction](../gdd/art-direction.md) | 源状态保留；扩写单独标注 |
| # 27. Mods / SDK / UGC | L1832–L1864 | [modding-and-toolchain](../technical/modding-and-toolchain.md)；[platform-and-release](../production/platform-and-release.md) | 源状态保留；扩写单独标注 |
| # 28. Commercial / Platform / Distribution | L1865–L1921 | [platform-and-release](../production/platform-and-release.md) | 源状态保留；扩写单独标注 |
| # 29. Engine / Licensing / Selection | L1922–L1949 | [architecture-and-performance](../technical/architecture-and-performance.md) | 源状态保留；扩写单独标注 |
| # 30. AI-agent-first Development | L1950–L1973 | [modding-and-toolchain](../technical/modding-and-toolchain.md) | 源状态保留；扩写单独标注 |
| # 31. QA / Telemetry / Streamer Tooling | L1974–L1993 | [roadmap-and-validation](../production/roadmap-and-validation.md)；[ux-and-accessibility](../gdd/ux-and-accessibility.md) | 源状态保留；扩写单独标注 |
| # 32. Difficulty / Storyteller / Mutator / Challenge | L1994–L2039 | [encounters-and-difficulty](../gdd/encounters-and-difficulty.md) | 源状态保留；扩写单独标注 |
| # 33. Inventory / Shop / Economy / Respec / Transit — Reset后待模式化整合 | L2040–L2084 | [economy-and-support](../gdd/economy-and-support.md)；[world-and-information](../gdd/facility-systems-and-information-rules.md) | 源状态保留；扩写单独标注 |
| # 34. Map / Navigation / Information UI | L2085–L2105 | [ux-and-accessibility](../gdd/ux-and-accessibility.md)；[world-and-information](../gdd/facility-systems-and-information-rules.md) | 源状态保留；扩写单独标注 |
| # 35. Narrative Delivery / Dialogue / Archive | L2106–L2134 | [narrative-delivery](../gdd/narrative-delivery.md) | 源状态保留；扩写单独标注 |
| # 36. Versioning / Save / Compatibility | L2135–L2154 | [network-and-persistence](../technical/network-and-persistence.md) | 源状态保留；扩写单独标注 |
| # 37. 重大历史决策登记表（A/B/C/D 选择与后续覆盖） | L2155–L2199 | [decisions-and-questions](decision-register.md) | 源状态保留；扩写单独标注 |
| # 38. GTFO 社区建议文件：采纳/改造/拒绝统计 | L2200–L2236 | [references-and-methods](../research/references-and-methods.md) | 源状态保留；扩写单独标注 |
| # 39. LEGACY / 已被覆盖的旧设计 | L2237–L2268 | [decisions-and-questions](decision-register.md) | 源状态保留；扩写单独标注 |
| # 40. 当前数字/规模统计（Canon vs Test） | L2269–L2300 | [README](../README.md) | 数值逐项责任见下表，不在README复制数值 |
| # 41. 当前仍需确认的东西（按返工风险排序） | L2301–L2368 | [decisions-and-questions](decision-register.md)；[roadmap-and-validation](../production/roadmap-and-validation.md) | 源状态保留；扩写单独标注 |
| # 42. 全项目 Preproduction 流程 — CURRENT | L2369–L2431 | [roadmap-and-validation](../production/roadmap-and-validation.md) | 源状态保留；扩写单独标注 |
| # 43. Release / Product Gates | L2432–L2470 | [roadmap-and-validation](../production/roadmap-and-validation.md) | 源状态保留；扩写单独标注 |
| # 44. 最终当前 Product Thesis | L2471–L2489 | [vision](../gdd/game-vision-and-design-pillars.md) | 源状态保留；扩写单独标注 |
| # 45. SSOT 维护纪律 | L2490–L2502 | [authoring-guide](authoring-guide.md) | 源状态保留；扩写单独标注 |
| # Appendix A — 当前全项目一句话状态 | L2503–L2515 | [README](../README.md) | 源状态保留；扩写单独标注 |
| # Appendix B — 本版本相对 SSOT v1.0 的主要变化 | L2516–L2527 | [decisions-and-questions](decision-register.md) | 源状态保留；扩写单独标注 |

## 跨系统章节细分

| 来源定位 | 迁移责任/边界 |
|---|---|
| §1.5 Cardinality | architecture；官方数量各自参数表 |
| §4A.1/.2/.8/.15 | operations玩家旅程、退出与模式构筑；不复制共享规则 |
| §4A.3/.6/.13/.14 | world信息/安全/Cart/Door |
| §4A.4/.5 | encounters无Alarm、Horde与压力 |
| §4A.7 | missions前向拓扑 |
| §4A.9–.12 | economy资源/支援/公共draft/实体物资 |
| §4A.16恢复/终止/永久收益 | survival / operations / progression |
| §5、§7；§8.1/.2 | player；Active实例→combat-prototypes |
| §8.3/.4 | economy模式资源；survival明确ReviveEffect |
| §9–§10 | build；30件/8配方候选→relics-and-fusions |
| §11.1/.2–.5 | player移动；survival生命与失败 |
| §13.5 | encounters保留威胁原则，missions定义Predator语法 |
| §18与§34.1 | ux；§34.2知识所有权→world |
| §19.6 | coop语音语义；其余audio |
| §23 | architecture构成；combat部位效果 |
| §27.6与§28.4 | platform的Demo开放/runtime/继承冲突 |
| §31.1/.2/.4 | roadmap遥测；.3 streamer HUD→ux |
| §33.1–.4/.5 | 经济的携带/商店/重置；世界移动 |
| §35 | narrative-delivery；正史事实只narrative-bible/central-story |
| §36 | network；Mod包合同→modding |
| §37/39/Appendix B | decisions历史，不复活旧实现 |
| §41 | decisions OPEN与roadmap Gate互链 |
| §42/43 | roadmap当前流程与可否决验证 |

## §37 全部36项决策

| 项目 | 来源定位 | 去向 |
|---|---|---|
| H37-01 Public Team Voice topology | SRC-SSOT-2.0 §37 第1项 | [原选择账](decision-register.md)；[当前责任](../gdd/coop-and-social.md) |
| H37-02 旧 Layer Transition Recovery | SRC-SSOT-2.0 §37 第2项 | [原选择账](decision-register.md)；[当前责任](../gdd/descent-future-game-mode.md) |
| H37-03 Enemy same-faction damage | SRC-SSOT-2.0 §37 第3项 | [原选择账](decision-register.md)；[当前责任](../gdd/combat-and-arsenal.md) |
| H37-04 Same-faction普通攻击拦截 | SRC-SSOT-2.0 §37 第4项 | [原选择账](decision-register.md)；[当前责任](../gdd/combat-and-arsenal.md) |
| H37-05 Enemy blocking | SRC-SSOT-2.0 §37 第5项 | [原选择账](decision-register.md)；[当前责任](../gdd/combat-and-arsenal.md) |
| H37-06 Basic flashlight | SRC-SSOT-2.0 §37 第6项 | [原选择账](decision-register.md)；[当前责任](../gdd/player-and-input.md) |
| H37-07 旧 Advanced Sensor baseline | SRC-SSOT-2.0 §37 第7项 | [原选择账](decision-register.md)；[当前责任](../gdd/player-and-input.md) |
| H37-08 Recoil style | SRC-SSOT-2.0 §37 第8项 | [原选择账](decision-register.md)；[当前责任](../gdd/combat-and-arsenal.md) |
| H37-09 Utility baseline concept | SRC-SSOT-2.0 §37 第9项 | [原选择账](decision-register.md)；[当前责任](../gdd/player-and-input.md) |
| H37-10 旧 Utility Recharge | SRC-SSOT-2.0 §37 第10项 | [原选择账](decision-register.md)；[当前责任](../gdd/economy-and-support.md) |
| H37-11 Utility shared cooldown | SRC-SSOT-2.0 §37 第11项 | [原选择账](decision-register.md)；[当前责任](../gdd/player-and-input.md) |
| H37-12 Revive Utility | SRC-SSOT-2.0 §37 第12项 | [原选择账](decision-register.md)；[当前责任](../gdd/survival-and-recovery.md) |
| H37-13 Revive recovery | SRC-SSOT-2.0 §37 第13项 | [原选择账](decision-register.md)；[当前责任](../gdd/survival-and-recovery.md) |
| H37-14 旧 Character Active slots | SRC-SSOT-2.0 §37 第14项 | [原选择账](decision-register.md)；[当前责任](../gdd/player-and-input.md) |
| H37-15 Separate Ultimate slot | SRC-SSOT-2.0 §37 第15项 | [原选择账](decision-register.md)；[当前责任](../gdd/player-and-input.md) |
| H37-16 Duplicate Character | SRC-SSOT-2.0 §37 第16项 | [原选择账](decision-register.md)；[当前责任](../gdd/player-and-input.md) |
| H37-17 Mid-run Character swap | SRC-SSOT-2.0 §37 第17项 | [原选择账](decision-register.md)；[当前责任](../gdd/player-and-input.md) |
| H37-18 Layer1 Build guarantee | SRC-SSOT-2.0 §37 第18项 | [原选择账](decision-register.md)；[当前责任](../gdd/descent-future-game-mode.md) |
| H37-19 Fusion discovery | SRC-SSOT-2.0 §37 第19项 | [原选择账](decision-register.md)；[当前责任](../gdd/field-modifications-and-effect-system.md) |
| H37-20 Fusion determinism | SRC-SSOT-2.0 §37 第20项 | [原选择账](decision-register.md)；[当前责任](../gdd/field-modifications-and-effect-system.md) |
| H37-21 Fusion consumption model | SRC-SSOT-2.0 §37 第21项 | [原选择账](decision-register.md)；[当前责任](../gdd/field-modifications-and-effect-system.md) |
| H37-22 Fusion commit | SRC-SSOT-2.0 §37 第22项 | [原选择账](decision-register.md)；[当前责任](../gdd/field-modifications-and-effect-system.md) |
| H37-23 Fusion inheritance | SRC-SSOT-2.0 §37 第23项 | [原选择账](decision-register.md)；[当前责任](../gdd/field-modifications-and-effect-system.md) |
| H37-24 Operation/Descent双模式 | SRC-SSOT-2.0 §37 第24项 | [原选择账](decision-register.md)；[当前责任](../gdd/game-vision-and-design-pillars.md) |
| H37-25 Operation Earned Safety | SRC-SSOT-2.0 §37 第25项 | [原选择账](decision-register.md)；[当前责任](../gdd/facility-systems-and-information-rules.md) |
| H37-26 Door system | SRC-SSOT-2.0 §37 第26项 | [原选择账](decision-register.md)；[当前责任](../gdd/facility-systems-and-information-rules.md) |
| H37-27 Alert decay | SRC-SSOT-2.0 §37 第27项 | [原选择账](decision-register.md)；[当前责任](../gdd/encounters-and-difficulty.md) |
| H37-28 Operation generation | SRC-SSOT-2.0 §37 第28项 | [原选择账](decision-register.md)；[当前责任](../gdd/missions-and-spaces.md) |
| H37-29 Operation Wipe Recovery Anchor | SRC-SSOT-2.0 §37 第29项 | [原选择账](decision-register.md)；[当前责任](../gdd/survival-and-recovery.md) |
| H37-30 Support pricing | SRC-SSOT-2.0 §37 第30项 | [原选择账](decision-register.md)；[当前责任](../gdd/economy-and-support.md) |
| H37-31 Supply ownership | SRC-SSOT-2.0 §37 第31项 | [原选择账](decision-register.md)；[当前责任](../gdd/economy-and-support.md) |
| H37-32 Equipment/Accessory | SRC-SSOT-2.0 §37 第32项 | [原选择账](decision-register.md)；[当前责任](../gdd/player-and-input.md) |
| H37-33 Relic slots | SRC-SSOT-2.0 §37 第33项 | [原选择账](decision-register.md)；[当前责任](../gdd/field-modifications-and-effect-system.md) |
| H37-34 Staff spell count | SRC-SSOT-2.0 §37 第34项 | [原选择账](decision-register.md)；[当前责任](../gdd/combat-and-arsenal.md) |
| H37-35 Descent layer length | SRC-SSOT-2.0 §37 第35项 | [原选择账](decision-register.md)；[当前责任](../gdd/descent-future-game-mode.md) |
| H37-36 Facility Cart commit | SRC-SSOT-2.0 §37 第36项 | [原选择账](decision-register.md)；[当前责任](../gdd/facility-systems-and-information-rules.md) |

## §38 全部社区条目

社区原上传文件尚未独立恢复，不能将其内容当直接证据。源文的已采用/转候选/拒绝状态在研究责任文档区分。

| 条目 | 来源定位 | 去向 |
|---|---|---|
| C38-01 Lobby失败显示明确原因 | SRC-SSOT-2.0 §38 L2206 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-02 Supplies 可存回 empty locker/storage | SRC-SSOT-2.0 §38 L2207 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-03 Lefty viewmodel | SRC-SSOT-2.0 §38 L2208 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-04 不可永久击杀但受伤害影响的 Threat → Predator Reversal | SRC-SSOT-2.0 §38 L2209 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-05 更多不同 Melee → Hammer/Knife/Spear/Sword prototype | SRC-SSOT-2.0 §38 L2210 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-06 Portable fog/environment tool → Utility/Field 系统 | SRC-SSOT-2.0 §38 L2211 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-07 Suppressed weapon → Acoustic stimulus | SRC-SSOT-2.0 §38 L2212 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-08 Bot Stay / On Me / Take / Tool use | SRC-SSOT-2.0 §38 L2213 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-09 Bot 不自动浪费 scarce resources | SRC-SSOT-2.0 §38 L2214 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-10 item pickup/swap QoL | SRC-SSOT-2.0 §38 L2215 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-11 sort/filter build items | SRC-SSOT-2.0 §38 L2216 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-12 distinctive operation/combat music | SRC-SSOT-2.0 §38 L2217 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-13 moving battlefield 作为未来 mission grammar 灵感。 | SRC-SSOT-2.0 §38 L2218 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-14 Trip mine on players → attachable mine Relic/Fusion | SRC-SSOT-2.0 §38 L2222 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-15 gun explodes on fire → Curse/Volatile Chamber | SRC-SSOT-2.0 §38 L2223 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-16 absurd recoil → Chaos mutator/cursed weapon only | SRC-SSOT-2.0 §38 L2224 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-17 player-controlled enemies / Among Us → 不进 core，可留给 mods/TC。 | SRC-SSOT-2.0 §38 L2225 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-18 所有枪统一巨 recoil | SRC-SSOT-2.0 §38 L2229 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-19 删除 reload animation | SRC-SSOT-2.0 §38 L2230 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-20 无限“Mom spawns baby X”换皮 enemy | SRC-SSOT-2.0 §38 L2231 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-21 FOMO限时奖励 | SRC-SSOT-2.0 §38 L2232 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |
| C38-22 没 gameplay价值的纯梗 feature。 | SRC-SSOT-2.0 §38 L2233 | [采纳/改造/拒绝逐项账](../research/references-and-methods.md) |

## §39 全部25项旧路径

| 旧路径索引 | 来源定位 | 去向 |
|---|---|---|
| H39-01 **Hard Classes / mandatory Warrior-Healer-Tank-Mage composition** | SRC-SSOT-2.0 §39 第1项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-02 **2 Character Active Abilities** | SRC-SSOT-2.0 §39 第2项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-03 **Universal Weapon Active button** | SRC-SSOT-2.0 §39 第3项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-04 **Scan as baseline universal ability / Scan merged with Ping** | SRC-SSOT-2.0 §39 第4项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-05 **Equipment + Accessory + Relic** | SRC-SSOT-2.0 §39 第5项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-06 **Fixed Relic slots** | SRC-SSOT-2.0 §39 第6项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-07 **全游戏固定5 Layers** | SRC-SSOT-2.0 §39 第7项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-08 **Operation Layer baseline recovery/reset** | SRC-SSOT-2.0 §39 第8项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-09 **Operation所有Utility快速免费Recharge** | SRC-SSOT-2.0 §39 第9项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-10 **传统Extraction shooter/搜打撤核心** | SRC-SSOT-2.0 §39 第10项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-11 **Persistent Facility Alarm / Alarm levels** | SRC-SSOT-2.0 §39 第11项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-12 **Combat=被发现后的错误状态** | SRC-SSOT-2.0 §39 第12项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-13 **Gameplay Recovery Anchor/Checkpoint rollback** | SRC-SSOT-2.0 §39 第13项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-14 **Mandatory backtracking** | SRC-SSOT-2.0 §39 第14项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-15 **Extraction hard countdown** | SRC-SSOT-2.0 §39 第15项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-16 **Retro dark sci-fi =唯一品牌** | SRC-SSOT-2.0 §39 第16项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-17 **每个人永久自带完整Staff当无Ammo保底** | SRC-SSOT-2.0 §39 第17项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-18 **Melee“几乎必然换血”作为平衡** | SRC-SSOT-2.0 §39 第18项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-19 **复杂连续Power allocation/Excel** | SRC-SSOT-2.0 §39 第19项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-20 **所有重大Team决定投票** | SRC-SSOT-2.0 §39 第20项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-21 **Supply通过Facility Terminal订购** | SRC-SSOT-2.0 §39 第21项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-22 **Knowledge直接当Ammo货币** | SRC-SSOT-2.0 §39 第22项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-23 **Fusion是可逆A+B active state** | SRC-SSOT-2.0 §39 第23项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-24 **Fusion需要Forge/手动确认** | SRC-SSOT-2.0 §39 第24项 | [覆盖结论与禁止恢复](decision-register.md) |
| H39-25 **公开Scenario Editor先做** | SRC-SSOT-2.0 §39 第25项 | [覆盖结论与禁止恢复](decision-register.md) |

## §40 全部25项数字/规模

值保留在责任文件参数表和只读源文，不复制到索引。源表把部分profile/pacing称为CANON时保留其性质；Staff上限同时在§6.4称测试上限，迁移明确“官方测试profile”，不变成内核硬限制。

| 项目 | 原状态/来源 | 唯一数值责任 |
|---|---|---|
| N40-01 玩家人数 | CANON；来源：SRC-SSOT-2.0 §40 第1行项目 | [数值责任](../gdd/game-vision-and-design-pillars.md) |
| N40-02 Operation时长 | DIRECTION；来源：SRC-SSOT-2.0 §40 第2行项目 | [数值责任](../gdd/operation-game-mode.md) |
| N40-03 BLACKSTART slice | TEST；来源：SRC-SSOT-2.0 §40 第3行项目 | [数值责任](../content/blackstart-greybox-mission.md) |
| N40-04 Descent Layers | CANON；来源：SRC-SSOT-2.0 §40 第4行项目 | [数值责任](../gdd/descent-future-game-mode.md) |
| N40-05 Descent单Layer | CANON pacing target；来源：SRC-SSOT-2.0 §40 第5行项目 | [数值责任](../gdd/descent-future-game-mode.md) |
| N40-06 Descent标准Run | CANON pacing target；来源：SRC-SSOT-2.0 §40 第6行项目 | [数值责任](../gdd/descent-future-game-mode.md) |
| N40-07 Weapon slots | Official CANON profile；来源：SRC-SSOT-2.0 §40 第7行项目 | [数值责任](../gdd/player-and-input.md) |
| N40-08 Utility slots | Official CANON profile；来源：SRC-SSOT-2.0 §40 第8行项目 | [数值责任](../gdd/player-and-input.md) |
| N40-09 Signature Active | CANON；来源：SRC-SSOT-2.0 §40 第9行项目 | [数值责任](../gdd/player-and-input.md) |
| N40-10 Staff默认Spell | Official profile；来源：SRC-SSOT-2.0 §40 第10行项目 | [数值责任](../gdd/combat-and-arsenal.md) |
| N40-11 Staff目标上限 | Official profile；来源：SRC-SSOT-2.0 §40 第11行项目 | [数值责任](../gdd/combat-and-arsenal.md) |
| N40-12 Melee prototype | TEST set；来源：SRC-SSOT-2.0 §40 第12行项目 | [数值责任](../gdd/combat-and-arsenal.md) |
| N40-13 Character prototype | TEST；来源：SRC-SSOT-2.0 §40 第13行项目 | [数值责任](../gdd/player-and-input.md) |
| N40-14 Relic first pool | TEST；来源：SRC-SSOT-2.0 §40 第14行项目 | [数值责任](../gdd/field-modifications-and-effect-system.md) |
| N40-15 Curated Fusion first pool | TEST；来源：SRC-SSOT-2.0 §40 第15行项目 | [数值责任](../gdd/field-modifications-and-effect-system.md) |
| N40-16 Operation normal Support Charges | TEST；来源：SRC-SSOT-2.0 §40 第16行项目 | [数值责任](../gdd/economy-and-support.md) |
| N40-17 Operation failure token payout | TEST；来源：SRC-SSOT-2.0 §40 第17行项目 | [数值责任](../gdd/progression-and-bastion.md) |
| N40-18 Emergency Recovery Floor | TEST；来源：SRC-SSOT-2.0 §40 第18行项目 | [数值责任](../gdd/survival-and-recovery.md) |
| N40-19 Revive Health | TEST；来源：SRC-SSOT-2.0 §40 第19行项目 | [数值责任](../gdd/survival-and-recovery.md) |
| N40-20 Difficulties | CANON；来源：SRC-SSOT-2.0 §40 第20行项目 | [数值责任](../gdd/encounters-and-difficulty.md) |
| N40-21 Steam Deck | CANON target；来源：SRC-SSOT-2.0 §40 第21行项目 | [数值责任](../production/platform-and-release.md) |
| N40-22 AI stress | TEST benchmark；来源：SRC-SSOT-2.0 §40 第22行项目 | [数值责任](../technical/architecture-and-performance.md) |
| N40-23 Projectile stress | TEST benchmark；来源：SRC-SSOT-2.0 §40 第23行项目 | [数值责任](../technical/architecture-and-performance.md) |
| N40-24 Public Quick Match voice | CANON；来源：SRC-SSOT-2.0 §40 第24行项目 | [数值责任](../gdd/coop-and-social.md) |
| N40-25 Default Player FF | CANON；来源：SRC-SSOT-2.0 §40 第25行项目 | [数值责任](../gdd/combat-and-arsenal.md) |

## 新增材料与讨论

| 新证据 | 责任 |
|---|---|
| SRC-CHATGPT-REVIEW-1.0（外部助手NON-CANON） | [快照](../sources/chatgpt-brutal-review-v1.0.md)；[35项风险](../production/risk-register.md) |
| 用户产品分叉/模块化/配件/统一模型 | 基础模式、模块化产品、局内改装与统一修改模型四份决策记录；产品愿景/Operation/修改系统/Mod 工具链 |
| 用户重资产/Predator/Breach | 团队重资产与 Predator/Breach 两份决策记录；战斗/任务/BLACKSTART 灰盒规格 |
| 用户唯一中央故事 | 单一客观正史决策；玩家故事与单一世界时间线 |
| 用户First Builder初始用途与部分Prototype谱系 | [narrative-bible NAR-010](../gdd/canonical-world-history-and-lore.md)；combat/prototypes只引用 |
| 用户界桥、外星生态、断网衰亡与守门人/人类内战设想 | [narrative-bible NAR-011、NAR-013–NAR-030](../gdd/canonical-world-history-and-lore.md)；单项用户裁决为CANON，完整连接因果仍PROPOSED |
| SRC-ASTRO-COSMIC-VOIDS（天文学边界） | [证据登记](../sources/evidence-register.md)；只约束现实术语，不证明科幻设定 |
| 用户故事总览与全新agent盲审流程 | [authoring-guide GOV-007](authoring-guide.md)；[central-story-spine STORY-006](../gdd/player-story-and-canonical-timeline.md)；当前未触发 |
| 用户世界命名系统、英文候选否决与中文正式选择 | [world-naming NAM-001–NAM-006](../gdd/world-naming.md)；选择为CANON，全部LEGAL NOT CLEARED |
| 用户外部威胁分类、虚空兽逐能/休眠生态、其他入网阵营与壁垒/太阳系边界 | [narrative-bible NAR-015、NAR-027](../gdd/canonical-world-history-and-lore.md)；已确认规则为CANON |
| 用户外勤旧制身份与设施低权限 | [narrative-bible NAR-028](../gdd/canonical-world-history-and-lore.md)；[world-and-information WRD-015](../gdd/facility-systems-and-information-rules.md)；[operations OPS-009](../gdd/operation-game-mode.md)；CANON |
| 用户载波重置、近距恢复与远端携盘逐节点重写 | [narrative-bible NAR-016、NAR-029](../gdd/canonical-world-history-and-lore.md)；[world-and-information WRD-016](../gdd/facility-systems-and-information-rules.md)；CANON |
| 用户限界/无限区域资产与风险收益、可选字形秘密支路 | [operations OPS-010](../gdd/operation-game-mode.md)；[missions MIS-014–MIS-015](../gdd/missions-and-spaces.md)；[economy ECO-015](../gdd/economy-and-support.md)；CANON/DIRECTION |
| 用户节点永久清场与真实行星端点Descent | [narrative-bible NAR-030](../gdd/canonical-world-history-and-lore.md)；CANON（LORE ONLY）；基础游戏玩家进度实现已被用户后续决定否决 |
| 用户程序Operation、随机主/支线、多任务族、中央Hub任务板与难度选择 | [operations OPS-011–OPS-012](../gdd/operation-game-mode.md)；[missions MIS-016–MIS-017](../gdd/missions-and-spaces.md)；[progression PRG-012](../gdd/progression-and-bastion.md)；[UX-008](../gdd/ux-and-accessibility.md)；CANON/DIRECTION |
| 用户Descent发布期全服务器节点恢复行动 | [vision VIS-009](../gdd/game-vision-and-design-pillars.md)；[operations OPS-013](../gdd/operation-game-mode.md)；[progression PRG-013](../gdd/progression-and-bastion.md)；[descent DES-008、DES-010](../gdd/descent-future-game-mode.md)；[network NET-008](../technical/network-and-persistence.md)；CANON/DIRECTION |
| 用户匹配后端复用Descent活动汇总 | [network NET-001、NET-008](../technical/network-and-persistence.md)；CANON/DIRECTION |
| 用户合作PVE不建设玩法反作弊 | [network NET-008](../technical/network-and-persistence.md)；[operations OPS-013](../gdd/operation-game-mode.md)；[progression PRG-013](../gdd/progression-and-bastion.md)；CANON/DIRECTION |
| 用户详细团队/个人统计、潜行破坏归因、轻量本地回放与结算确认后删除 | [debrief/replay RPL-001至RPL-008](../gdd/debrief-and-replay.md)；[technical TRP-001至TRP-006](../technical/replay-recording.md)；[UX-009](../gdd/ux-and-accessibility.md)；CANON/DIRECTION |
| 用户固定四人壁垒外勤小队与非递进玩家故事 | [central story STORY-007至STORY-010](../gdd/player-story-and-canonical-timeline.md)；CANON/DIRECTION，人物细节OPEN |
| 用户成就与可收集碎片叙事 | [central story STORY-011](../gdd/player-story-and-canonical-timeline.md)；[narrative delivery NDL-004](../gdd/narrative-delivery.md)；[missions MIS-018](../gdd/missions-and-spaces.md)；[progression PRG-014](../gdd/progression-and-bastion.md)；CANON/DIRECTION |
| 用户四名角色设计请求、人格范围与中文代号纠正 | [character roster CHAR-001至CHAR-011](../content/field-team-character-personalities.md)；[central story STORY-008](../gdd/player-story-and-canonical-timeline.md)；真实姓名取消、美术延后，`断桥/回声/铁砧/寒蝉`仍待用户裁决 |
| 用户壁垒—守门人联系与结构化交易 | [world-and-information WRD-013–WRD-014](../gdd/facility-systems-and-information-rules.md)；当前PROPOSED/TEST |
| 用户Sol重联DLC与Earth武器边界 | [narrative-bible NAR-011](../gdd/canonical-world-history-and-lore.md)；DLC仍PROPOSED且不承诺 |
| 用户枪械-only条件、三枪族、无限界桥枪否决与响应窗口 | [vision VIS-008](../gdd/game-vision-and-design-pillars.md)；[combat CMB-012–CMB-016](../gdd/combat-and-arsenal.md)；[combat prototypes](../content/combat-prototypes.md) |
| 用户玩家掌握成长原则 | [progression PRG-009–PRG-010](../gdd/progression-and-bastion.md)；[player PLY-013](../gdd/player-and-input.md)；[UX UX-007](../gdd/ux-and-accessibility.md) |
| 用户“总览”命名 | discussion log；README导航 |
| 用户Unity 6、URP、GameObject-first与AI-agent-first决定 | [Unity引擎与渲染](decisions/unity-engine-and-rendering.md)；[架构ARC-006至ARC-009](../technical/architecture-and-performance.md)；CANON |
| 用户Local UPM/Content结构、官方内容同模组系统、Host Package Lock自动同步 | [Agent-first Mod Runtime](decisions/agent-first-modding-runtime.md)；[Modding MOD-013至MOD-018](../technical/modding-and-toolchain.md)；[Network NET-009至NET-010](../technical/network-and-persistence.md)；CANON |
| 用户Steam/PC与Workshop唯一公开Mod渠道、Runtime与Steam解耦 | [Agent-first Mod Runtime](decisions/agent-first-modding-runtime.md)；[平台PLAT-001/PLAT-007/PLAT-008](../production/platform-and-release.md)；CANON |
| 用户Host Authority与Gameplay Command Replication | [Host Authority与Gameplay Command](decisions/host-authority-and-gameplay-commands.md)；[Network NET-011](../technical/network-and-persistence.md)；CANON |
| 用户固定60 Hz Authority Simulation与multi-rate更新 | [固定Tick与多频模拟](decisions/fixed-tick-and-multirate-simulation.md)；[Network NET-012](../technical/network-and-persistence.md)；CANON |
| 用户Snapshot/Delta/Event/Interest/Dormancy复制架构 | [状态复制架构](decisions/state-replication.md)；[Network NET-013](../technical/network-and-persistence.md)；CANON |
| 用户技术OPEN清单 | [Network NET-015](../technical/network-and-persistence.md)；[Modding MOD-019](../technical/modding-and-toolchain.md)；[Asset Policy](../production/asset-policy-and-provenance.md)；OPEN/DIRECTION |
| 用户Lag Compensation基线批准 | [延迟补偿决定](decisions/lag-compensation-and-server-rewind.md)；[Network NET-014](../technical/network-and-persistence.md)；CANON/DIRECTION + 150 ms TEST |
| 用户可读文件名与更大决策批次 | [作者规则GOV-008](authoring-guide.md)；现有决策文件改为描述性名称；CANON |
| 用户初始版本全Steam平台栈、Steam Workshop Mod与网络批次批准 | [网络运行与恢复](decisions/network-runtime-and-recovery.md)；[Network NET-015](../technical/network-and-persistence.md)；[平台PLAT-001/PLAT-007/PLAT-008](../production/platform-and-release.md)；[Modding MOD-016/MOD-019](../technical/modding-and-toolchain.md)；组合CANON/DIRECTION，数值TEST |
| 用户批准Mod Runtime、安全优先、无社区DLL并授权脚本选择 | [Steam Workshop Mod Runtime](decisions/steam-workshop-mod-runtime.md)；[Modding MOD-018至MOD-025](../technical/modding-and-toolchain.md)；Luau Core与内容能力原则CANON/DIRECTION，绑定及预算为TEST |
| 用户要求批次交付直接说明下一批 | [作者指南GOV-009](authoring-guide.md)；[证据登记](../sources/evidence-register.md)；CANON工作规则 |
| 助手建议下一批“视觉制作与资产治理” | [Asset Policy](../production/asset-policy-and-provenance.md)；[视觉方向](../gdd/art-direction.md)；已完成策略与Visual DNA裁决，生产Gate待实测 |
| 用户要求先确定并立即安装完整游戏制作Agent Skills、更新Blender与Blender MCP，并明确授权Online Access | [Agent Skills能力地图](../production/game-production-agent-skills.md)；36项项目Skill已校验，Unity CLI已安装，Blender MCP已完成26-tool端到端只读验证 |
| 用户否决资产来源固定比例，采用合格免费优先、否则AI生成修整、付费止损 | [视觉方向ART-007](../gdd/art-direction.md)；[Asset Policy ASSET-001/006](../production/asset-policy-and-provenance.md)；CANON WORKFLOW |
| 用户委托正式比较三套视觉候选并质疑工业与低模的产能风险 | [Visual DNA决策](decisions/visual-dna-and-art-direction.md)；[视觉方向ART-006/012](../gdd/art-direction.md)；分层壁垒与中等多边形生产档位为CANON/DIRECTION，实机Gate未执行 |
