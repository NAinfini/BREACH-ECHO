---
doc_id: RESEARCH-METHODS
doc_type: research
stage: BASELINE
updated: 2026-09-05
owner_role: 设计研究负责人
canon_basis: "SRC-SSOT-2.0 §3、§38；外部一手资料"
depends_on: ["../sources/evidence-register.md"]
---

# 研究资料、技能与文档格式

## 使用方法与限制

REF-001 · PROPOSED · 来源：本轮研究综合；访问日期均2026-09-04。

没有唯一强制GDD模板。按受众与决策拆分，系统规则单一责任、内容卡可制作、技术契约可验证、制作Gate可否决。采用短且可追溯的活文档，而不是机械按源45章拆成45份镜像。网上“skill”或提示词不能替代游戏研究/测试；本轮未下载或安装第三方技能。适合当前任务的是设计方法、GDD、主题决策记录、内容卡与实验格式，见[作者规则](../governance/authoring-guide.md)及[模板](../templates/system-spec.md)。

E1=原论文/官方文档/原始演讲；E2=专业实践/案例；E3=本项目推断。外部材料不决定本项目CANON，也不证明商业成功。

## 文档、体验与验证方法

| 来源ID / 等级 | 原始资料 | 本项目采用 | 不能推出 |
|---|---|---|---|
| REF-MDA / E1 | [MDA原论文](https://www.cs.northwestern.edu/~hunicke/MDA.pdf) | 从想要的体验A反推动态D与机制M，写可证伪假设 | 系统越多就越深或越好玩 |
| REF-GDC-DOC / E1 | [GDC 2007设计文档演讲](https://media.gdcvault.com/gdc07/slides/S3782i1.pdf) | 面向使用者、清楚结构与有效传递，短文档和责任归属 | 存在所有游戏通用的唯一章节表 |
| REF-DOCS / E1 | [Google软件工程文档实践](https://abseil.io/resources/swe-book/html/ch10.html) | 文档作为维护资产，明确读者与单一信息源 | 软件写作方法可替代游戏制作 |
| REF-UNITY-SLICE / E1 | [Unity学习课程切片案例](https://learn.unity.com/course/welcome-to-the-course/tutorial/explore-out-of-circulation?version=2022.3) | 用代表性可玩片段检验完整体验 | 本项目必须选Unity |
| REF-CMU-SLICE / E2 | [CMU ETC切片案例资料](https://press.etc.cmu.edu/file/download/434/53aa6e75-7488-4454-870e-70fbf9c4b291) | 用有限场景验证制作与体验风险 | 某案例工期能直接预测本项目 |
| REF-GUR / E2 | [设计游戏用户研究](https://gamesuserresearch.com/designing-a-games-user-research-study/) | 假设、招募、观察、行为指标、访谈；分开人群 | 小样本偏好可当销量预测 |
| REF-PLAYTEST / E1 | [Steam Playtest](https://partner.steamgames.com/doc/features/playtest) | 用独立child app组织低风险测试 | Playtest参与自动代表购买 |

## 可访问性与平台

| 来源ID / 等级 | 原始资料 | 对应文档与采用 |
|---|---|---|
| REF-XAG / E1 | [Xbox Accessibility Guidelines](https://learn.microsoft.com/en-us/xbox/accessibility/guidelines) | [UX](../gdd/ux-and-accessibility.md)的早期设计guardrail，不宣称法律或认证通过 |
| REF-XAG103 / E1 | [XAG103多通道提示](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103) | Horde、倒地、任务危机用合法等价通道 |
| REF-XAG104 / E1 | [XAG104字幕](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/104) | 字幕/SDH、重要口语、可读设置 |
| REF-XAG107 / E1 | [XAG107输入](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/107) | 输入可调整、核心流程控制器完成 |
| REF-XAG108 / E1 | [XAG108游戏难度](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/108) | 能力差异与难度选择，避免把难度只理解为敌人HP |
| REF-DECK / E1 | [Steam Deck兼容性](https://partner.steamgames.com/doc/steamhardware/compat?l=english) | 输入/glyph/字号/分辨率/性能早介入；不把普通PC测试当Deck验证 |

## 网络、遥测与隐私

| 来源ID / 等级 | 原始资料 | 采用与边界 |
|---|---|---|
| REF-UE-NET / E1 | [Unreal networking overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/networking-overview-for-unreal-engine?lang=en-US) | authority/replication方法参考，不选引擎 |
| REF-UE-EMU / E1 | [Unreal network emulation](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-network-emulation-in-unreal-engine?lang=en-US) | 延迟/丢包/抖动情景化测试，不能只测本机LAN |
| REF-STEAM-NET / E1 | [Steam networking](https://partner.steamgames.com/doc/features/multiplayer/networking) | 连接/relay能力调研，不能等同完整gameplay server |
| REF-STEAM-LOBBY / E1 | [Steam Matchmaking与Lobby API](https://partner.steamgames.com/doc/api/ISteamMatchmaking) | Lobby搜索、邀请、metadata和单一Owner；Owner转移只属于控制面，不能推出Gameplay世界自动迁移 |
| REF-STEAM-SDR / E1 | [Steam Datagram Relay](https://partner.steamgames.com/doc/features/multiplayer/steamdatagramrelay) | P2P relay与IP保护；不替本项目定义Authority、Snapshot或Migration |
| REF-FISHNET-RUNTIME / E1 | [FishNet网络模型](https://fish-networking.gitbook.io/docs/guides/high-level-overview/networking-models)、[Prediction](https://fish-networking.gitbook.io/docs/guides/features/prediction) | listen server、预测与transport抽象候选；官方文档同时说明当前无内建Host Migration，因此迁移必须自有实现 |
| REF-FISHY-STEAMWORKS / E1 | [FishySteamworks文档](https://fish-networking.gitbook.io/docs/fishnet-building-blocks/transports/fishysteamworks)、[当前源码](https://github.com/FirstGearGames/FishySteamworks/blob/main/FishNet/Plugins/FishySteamworks/Core/ClientSocket.cs) | 当前adapter源码核对到ISteamNetworkingSockets/ConnectP2P路径；仍需真实版本、channel、IL2CPP与Steam Deck Spike |
| REF-UNITY-NETCODE / E1 | [Unity Netcode包总览](https://docs.unity.com/en-us/multiplayer/netcode/netcode)、[NGO Client Anticipation](https://docs-multiplayer.unity3d.com/netcode/2.1.1/advanced-topics/client-anticipation/) | NGO是GameObject高层框架候选，但官方文档把完整prediction/reconciliation留给开发者；不同时维护第二套Gameplay框架 |
| REF-UNITY-HOST-MIGRATION / E1 | [Unity Host Migration](https://docs.unity.com/en-us/relay/host-migration)、[Relay协议](https://docs.unity.com/relay/relay-message-protocol) | 区分host election与network data migration；Relay自身不自动迁移本游戏世界，不据此改用Distributed Authority |
| REF-PF-EVENT / E1 | [PlayFab实时分析概念](https://learn.microsoft.com/en-us/gaming/playfab/features/analytics/metrics/real-time-analytics-core-concepts) | 事件/指标定义方法；未选PlayFab |
| REF-PF-EXP / E1 | [PlayFab实验术语](https://learn.microsoft.com/en-us/gaming/playfab/live-service-management/game-configuration/experiments/experimentation-key-terms) | 对照分组、预定义指标，避免事后挑结果 |
| REF-PF-PRIVACY / E1 | [PlayFab玩家数据删除](https://learn.microsoft.com/en-us/gaming/playfab/data-analytics/privacy-compliance/gdpr-deleting-player-data) | 最少采集、可删除/可追溯，不构成法律合规意见 |
| REF-STEAM-STATS / E1 | [Steam stats与achievements](https://partner.steamgames.com/doc/features/achievements?l=english) | 平台统计与成就能力边界，不把统计当可信反作弊后端 |
| REF-GTFO-REPLAY / E1 | [GTFOReplay源码仓库](https://github.com/randomuserhi/GTFOReplay)、[Thunderstore页面](https://thunderstore.io/c/gtfo/p/randomuserhi/GTFOReplay/)与[发布记录](https://github.com/randomuserhi/GTFOReplay/releases) | 2026-09-05核对：项目分离Recorder与Viewer，本地保存回放，查看器支持内容profile；发布记录显示记录数据可派生友伤明细和伤害类奖章。本项目只借鉴“结构化事件→详细统计+简化战术回看”的产品模式，不复制其完整3D回放范围或MVP导向；仓库根目录未观察到明确LICENSE，禁止复制代码或资产 |

## Mods与工具链

| 来源ID / 等级 | 原始资料 | 采用与边界 |
|---|---|---|
| REF-WORKSHOP / E1 | [Steam Workshop总览](https://partner.steamgames.com/doc/features/workshop?language=english)、[实现](https://partner.steamgames.com/doc/features/workshop/implementation) | 内容工具、staging、上传/验证、客户端相同内容；接入Workshop不自动生成SDK |
| REF-WORKSHOP-UGC / E1 | [ISteamUGC](https://partner.steamgames.com/doc/api/isteamugc?language=english) | `DownloadItem`、下载进度、安装信息与UGC查询；Steam把文件送到本机，不替游戏验证Package schema/hash，也不把soft dependency自动变成运行时合法依赖 |
| REF-WORKSHOP-VERSIONING / E1 | [Steam Workshop Item Versioning](https://partner.steamgames.com/doc/features/workshop/itemversioning) | Workshop可按游戏beta branch标注兼容版本；默认仍传播当前适用版本。该机制不是任意`content_hash`历史仓库，不能替代Run本地精确缓存 |
| REF-LUAU-SANDBOX / E1 | [Luau嵌入式Sandbox](https://luau.org/sandbox/)、[Luau C API](https://luau.org/api/)、[Luau官方仓库/构建/许可证](https://github.com/luau-lang/luau) | Luau Core可把Compiler/VM作为C++库嵌入，提供只读环境、线程隔离、interrupt与内存分类等宿主控制点，并采用MIT许可证；默认没有内存上限，宿主暴露API仍可能破坏Sandbox，因此必须自建Capability与配额并先过Unity绑定Spike |
| REF-LUAU-LUTE / E1 | [Lute官方仓库](https://github.com/luau-lang/lute) | Lute主动提供文件、网络请求与socket等通用程序能力；本项目安全优先，不把这些能力引入游戏后再封堵，因此只用Luau Core Compiler/VM，不采用Lute Runtime |
| REF-MOONSHARP / E1 | [MoonSharp Sandbox](https://www.moonsharp.org/sandbox.html)、[当前版本](https://www.moonsharp.org/) | 纯C#、Unity友好，明确警告默认/自动interop及`io/os/file`风险；稳定版2.0较旧而3.0仍为beta，保留为Spike对照，不作为当前首选锁定 |
| REF-DOTNET-UNTRUSTED-CODE / E1 | [Microsoft安全编码指南](https://learn.microsoft.com/en-us/dotnet/standard/security/secure-coding-guidelines)、[CAS已废弃](https://learn.microsoft.com/en-us/dotnet/core/compatibility/core-libraries/5.0/code-access-security-apis-obsolete) | CAS/partial trust不是现代.NET安全边界；未知Managed Assembly不能因“托管代码”而当作安全Workshop脚本 |
| REF-UNITY-PLUGINS / E1 | [Unity 6 Plug-ins](https://docs.unity.cn/6000.0/Documentation/Manual/Plugins.html) | Unity区分Managed与Native plug-ins，Native可访问OS与第三方库；支持插件不等于适合从陌生Lobby自动下载执行 |
| REF-FACTORIO / E1 | [Factorio API](https://lua-api.factorio.com/latest/index.html)、[数据生命周期](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html) | 阶段化可预测加载案例，不借用其技术栈当默认 |
| REF-LUA / E2 | [Lua安全环境](https://www.lua.org/pil/6.1.html) | 不受信代码需受限环境；资料版本较旧，仅支持原则 |
| REF-UE-MOD / E1 | [Unreal Game Features](https://dev.epicgames.com/documentation/unreal-engine/game-features-and-modular-gameplay-in-unreal-engine?lang=en-US) | 模块化插件案例；本轮页面功能状态需关注Beta，不据此选引擎 |

## 市场与竞争快照

REF-002 · PROPOSED · 来源：本轮E1市场页面综合推断E3。

下列评论比例/数量是2026-09-04抓取的近似英语快照，随时变化；不是销量、代表性市场调研或本项目预期结果。

| 官方商店来源 / E1 | 本轮可观察基线 | 项目推断 / E3 |
|---|---|---|
| [GTFO](https://store.steampowered.com/app/493520/GTFO/?l=english) | hardcore co-op horror FPS，stealth/strategy/teamwork；约25.6k英语评论、88%正面 | 忠实受众存在，不等于大众都会接受长局惩罚 |
| [Deep Rock Galactic: Rogue Core](https://store.steampowered.com/app/2605790/_/?l=english) | 1–4人合作FPS roguelite、程序设施/洞穴、Reclaimers；EA 2026-05-20；英语约70%正面、近期约52% | 纯co-op roguelite不是空白市场；Reclaimer命名有明显重叠 |
| [Den of Wolves](https://store.steampowered.com/app/1818140/Den_of_Wolves/) | 计划/执行的合作FPS，未发布，时长表达更有弹性 | 团队协作想象存在；未发售项目不是市场成功证明 |
| [SCP:5K](https://store.steampowered.com/app/872670/SCP_5K/) | tactical horror co-op，EA；约8.6k英语评论、80% | 相邻而非同构竞争 |
| [The Forever Winter](https://store.steampowered.com/app/2828860/The_Forever_Winter/) | tactical co-op/extraction/horror；约16k英语评论、69% | 稀缺题材同样会因执行问题受罚，评论不证明具体差评根因 |

“供给少”既可能是未满足需求，也可能是受众小或制作贵。必须用访谈、blind positioning、试玩复玩和愿望单/试玩意向验证；不凭用户个人偏好或评论数宣布市场会接受。

## 源文学习库保留索引

REF-003 · DIRECTION · 来源：SRC-SSOT-2.0 §3.1–§3.19；这些项目观察未全部在本轮独立复测。

Isaac：局内累计/形态变化，不强迫Wiki；Noita：可组合语法/有推进递归；DRG：清楚任务/资源与压力节奏；GTFO：物理信息/共享规划，不继承全局Alarm/开枪即错误/强制长回跑；Helldivers2：方向输入/热量；Borderlands：有贡献的Last Wind；RoR2：成长剧变；Roboquest/Returnal/Witchfire：枪感/动作/反馈；Gunfire Reborn：breadth同时警惕perk堆积；Abyssus：包装与interaction density区别；Rogue Core：直接重叠；Moros/HELLBREAK：表面同质化；Holy Shoot：dead-end proc警告；ANVIL：拼装感风险；Far Far West：枪法术/任务/视觉主题；Iron's Spells：Staff repertoire；Darktide：caster资源身份；Mario Maker/StarCraft Editor：内部工具先验证再开放。

## §38社区建议采用账

REF-004 · DIRECTION · 来源：SRC-SSOT-2.0 §38.1；社区原上传未独立恢复。

已采纳/改造：Lobby失败原因、储物柜回存、左手viewmodel、Predator反转、四Melee、便携雾/环境工具、消音武器作为Acoustic stimulus、Bot命令与不浪费资源、拾取/换物QoL、Build筛选排序、独特任务/战斗音乐、未来Moving battlefield。分别归合作/经济/UX/任务/内容/敌人/音频责任文件；不是本轮新增全部制作承诺。

REF-005 · DIRECTION · 来源：SRC-SSOT-2.0 §38.2。
玩家身上Trip Mine→可附着Relic/Fusion候选；开枪爆炸→Curse/Volatile Chamber；夸张后坐→Chaos/诅咒内容；玩家控敌/Among Us→只留mods/TC。未成为官方核心玩法。

REF-006 · LEGACY · 来源：SRC-SSOT-2.0 §38.3。
拒绝核心：全枪巨后坐、删reload动画、无限Mom换皮、FOMO奖励、无玩法价值的纯梗。保留作为避免重复提案的历史，不恢复到生产范围。
