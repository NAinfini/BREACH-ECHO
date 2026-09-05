---
doc_id: PROD-PLATFORM
doc_type: production
stage: BASELINE
updated: 2026-09-05
owner_role: 产品发行负责人
canon_basis: "SRC-SSOT-2.0 §27.6、§28；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED；SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY"
depends_on: ["roadmap-and-validation.md", "../governance/decisions/DDD-0009-agent-first-modding-runtime.md"]
---

# 平台、商业、Demo 与发行关卡

PLAT-001 · CANON · 来源：SRC-SSOT-2.0 §28.1–§28.2；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED。

**当前商业发行范围锁定为 Steam / PC。** Steam Deck官方支持继续保留。当前产品计划不同时上 Epic Games Store、GOG 或其他PC商店，也不为非Steam商店承诺cross-store发行。Premium buy-to-play Base Game、持续免费内容更新、Paid Cosmetic DLC/Supporter Packs、Community Mods免费。无premium currency/loot box/battle pass/FOMO轮换店/daily login/付费战斗力/官方付费Mod市场。

未来若决定增加其他商店或主机，必须另开平台扩展决策；技术层应保持身份、Session、Mod Distribution和商店Entitlement边界可替换，但这种解耦不是未来发行承诺。

PLAT-002 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

无付费Early Access；内部/封测/Steam Playtest→短完整Demo→Premium1.0候选。Demo目标15–25min的短Operation，同一runtime较小内容集，与40–50min标准长局不冲突。支持好友合作和当时已通过验收的安全包路径，不先建完整TC/Forge生态。只迁移幂等外观/徽章和明确允许的横向声明，不迁移Run/任务资源/临时战报或整个秘密Archive；购买、最终售价/日期仍需OWNER-02。

PLAT-003 · CANON · 来源：SRC-SSOT-2.0 §28.5、§40。
Deck稳定60FPS（16.67ms帧预算）硬目标；可以降渲染/表现，不降canonical结果；真机持续thermal soak与完整controller支持。

PLAT-007 · CANON · 来源：SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED。

**当前公开Mod发布、存储、发现、安装和多人自动同步只支持 Steam Workshop。** 不建设mod.io、Epic/GOG Mod平台或另一套官方公共Mod市场。BREACH自己的ContentPackage/Package Lock仍是运行时真相；Workshop只是Steam版分发服务，具体规则见[DDD-0009](../governance/decisions/DDD-0009-agent-first-modding-runtime.md)与[Modding](../technical/modding-and-toolchain.md)。

Local/dev package继续允许内部开发、SDK示例、测试和恢复诊断，但不是与Workshop并列的公开商业Mod生态。第三方Mod Manager不是正常玩家使用Mod的前提。

## 选定发行路径

PLAT-004 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

首发唯一Operation；完整内容范围由release-scope.md拥有，不能从一个模板或某个房间数推导足够销售。Demo只用一个短完整合同展示资源选择、设施后果和合作收束。底层API不是主要商店卖点；先证明普通玩家愿意再玩，再作商业发布。

## 平台状态、所有权与边界

PLAT-005 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮发行扩写。
Internal→Closed Playtest→可公开验证Demo→1.0候选；每一步看[Gate](roadmap-and-validation.md)，不是日期到了自动升级。Package entitlements、runtime功能、官方内容访问、账号claims独立；免费runtime不意味着premium官方资产可任意重新分发。Mod授权/license/条款需真实审查，本轮未作法律判断。

Demo发布前验证：完整controller输入、字号与glyph、目标硬件性能、退出/恢复、内容版本pin、网络加入失败原因、隐私说明、有限进度边界。Steam Playtest child app只是测试渠道，不代表steam验证或销量。未授权前不上传Steam、Workshop、不发公告、不采真实个人遥测。

PLAT-008 · CANON · 来源：SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED。

商店和平台服务必须与Gameplay Kernel解耦：Steam AppID、SteamID、Lobby/Workshop locator、Entitlement和好友邀请等不得成为武器、任务、Save、Content Registry或规则系统的唯一ID。若未来新增商店，只允许通过平台/服务Provider层接入，不要求重写Gameplay ContentPackage、Package Lock或Simulation语义。

## 指标与商业审批

PLAT-006 · TEST · 来源：本轮研究方法。
分别记录商店页看懂定位、试玩进入、完成、次日自发回流、组队邀请、愿望单意向；样本来源和重复参与者透明。小样本意向不是购买转化。Public Quick Match须先过陌生无语音风险Gate；Solo须无Bot完整通关；Deck须真实硬件而非分辨率模拟。

当前：内容规划见范围合同；Demo采用短Operation；API以外部作者Gate冻结；TC未来；中英文本。价格、发行日期、预算与退款/支持政策需OWNER-02商业批准；未来其他商店/console/crossplay只有在重新打开平台范围后才需要产品决策。无任何发行检查已通过的声明。
