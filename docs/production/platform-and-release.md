---
doc_id: PROD-PLATFORM
doc_type: production
stage: BASELINE
updated: 2026-09-05
owner_role: 产品发行负责人
canon_basis: "SRC-SSOT-2.0 §27.6、§28；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED；SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY"
depends_on: ["roadmap-and-validation.md", "../governance/decisions/agent-first-modding-runtime.md", "asset-policy-and-provenance.md"]
---

# 平台、商业、Demo 与发行关卡

PLAT-001 · CANON · 来源：SRC-SSOT-2.0 §28.1–§28.2；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED；SRC-USER-2026-09-05-STEAM-ONLY-NETWORK-STACK-APPROVED。

**初始版本商业与玩家平台范围锁定为Steam / PC。** Steam Deck官方支持继续保留；身份、好友、邀请、Lobby、匹配搜索、P2P/Relay与公开Mod分发也全部使用Steam平台能力。当前产品计划不同时上Epic Games Store、GOG或其他PC商店，不接入第二套平台在线服务，也不为非Steam商店承诺cross-store发行。Premium buy-to-play Base Game、持续免费内容更新、Paid Cosmetic DLC/Supporter Packs、Community Mods免费。无premium currency/loot box/battle pass/FOMO轮换店/daily login/付费战斗力/官方付费Mod市场。

未来若决定增加其他商店或主机，必须另开平台扩展决策；技术层应保持身份、Session、Mod Distribution和商店Entitlement边界可替换，但这种解耦不是未来发行承诺。

PLAT-002 · DIRECTION · 来源：SRC-SSOT-2.0 §28.3–§28.4、§27.6。
无Paid Early Access路线，先内部/封测/Steam Playtests、benchmark/public tests，Demo→Premium1.0。历史Demo目标15–25分钟、完整开中结、小下载、真3D、Workshop/Scenario/TC完整runtime方向；当前长Operation与之冲突，Demo格式OPEN。Limited Carryover历史方向只带cosmetics/title/badge/安全横向claims，不完整带Run saves/Archive Credits/Glyph/Forbidden/Main Evidence，需重审。

PLAT-003 · CANON · 来源：SRC-SSOT-2.0 §28.5、§40。
Deck稳定60FPS（16.67ms帧预算）硬目标；可以降渲染/表现，不降canonical结果；真机持续thermal soak与完整controller支持。

PLAT-007 · CANON · 来源：SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED；SRC-USER-2026-09-05-STEAM-ONLY-NETWORK-STACK-APPROVED。

**初始版本公开Mod发布、存储、发现、安装和多人自动同步只支持Steam Workshop。** 不建设mod.io、Epic/GOG Mod平台、Host临时传包、非Steam官方CAS或另一套官方公共Mod市场。BREACH自己的ContentPackage/Package Lock仍是运行时真相；Workshop只是Steam版分发服务，具体规则见[Agent-first Mod Runtime](../governance/decisions/agent-first-modding-runtime.md)与[Modding](../technical/modding-and-toolchain.md)。

Local/dev package继续允许内部开发、SDK示例、测试和恢复诊断，但不是与Workshop并列的公开商业Mod生态。第三方Mod Manager不是正常玩家使用Mod的前提。

## 最新发行建议

PLAT-004 · PROPOSED · 来源：本轮Operation优先评审。
不承诺两个完整模式、公开Editor/TC、完整Demo Workshop同时首发。Demo做一个短而完整的Operation模板，展示一个资源选择、一个设施后果和一次协作收束；不要两个模式各剪五分钟。该建议涉及源发行范围，必须经DDD决策和用户确认，不直接删基线。

“一个完整模板加两个seed变体”不足以自动成为可卖内容量；最低可卖量由重复体验、价格、内容工时和意愿数据决定。价格、销量、团队成本未知，不估算收入来安慰项目。首发宣传先卖高压团队任务与看得见的世界后果；底层图结构和API不做普通玩家第一购买理由。

## 平台状态、所有权与边界

PLAT-005 · PROPOSED · 来源：本轮发行扩写。
Internal→Closed Playtest→可公开验证Demo→1.0候选；每一步看[Gate](roadmap-and-validation.md)，不是日期到了自动升级。Package entitlements、runtime功能、官方内容访问、账号claims独立；免费runtime不意味着premium官方资产可任意重新分发。采购、来源、许可证据及Runtime/SDK/Workshop发布面由[Asset Policy](asset-policy-and-provenance.md)负责；本轮未作法律判断。

Demo发布前验证：完整controller输入、字号与glyph、目标硬件性能、退出/恢复、内容版本pin、网络加入失败原因、隐私说明、有限进度边界。Steam Playtest child app只是测试渠道，不代表steam验证或销量。未授权前不上传Steam、Workshop、不发公告、不采真实个人遥测。

PLAT-008 · CANON · 来源：SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED；SRC-USER-2026-09-05-STEAM-ONLY-NETWORK-STACK-APPROVED。

商店和平台服务必须与Gameplay Kernel解耦：Steam AppID、SteamID、Lobby/Workshop locator、Entitlement和好友邀请等不得成为武器、任务、Save、Content Registry或规则系统的唯一ID。若未来新增商店，只允许通过平台/服务Provider层接入，不要求重写Gameplay ContentPackage、Package Lock或Simulation语义。

## 指标与OPEN

PLAT-006 · TEST · 来源：本轮研究方法。
分别记录商店页看懂定位、试玩进入、完成、次日自发回流、组队邀请、愿望单意向；样本来源和重复参与者透明。小样本意向不是购买转化。Public Quick Match须先过陌生无语音风险Gate；Solo须无Bot完整通关；Deck须真实硬件而非分辨率模拟。

尚未输入的发行变量：首发内容量/价格、Demo模板、API冻结期、TC时间、语言/区域、退款预期、发行预算。它们在对应发行 Gate 前由所有者与发行负责人填写；未来其他商店、主机平台和跨平台联机只有在重新打开平台范围后才需要产品决策。当前没有任何发行检查已通过。
