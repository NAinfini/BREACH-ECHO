---
doc_id: DDD-0008
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 技术与产品负责人
canon_basis: "SRC-USER-2026-09-05-UNITY-ENGINE-LOCK；SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST；SRC-USER-2026-09-05-AI-AGENT-FIRST-STRUCTURE；官方Unity 2026许可资料"
depends_on: ["../decision-register.md", "../../technical/architecture-and-performance.md", "../../technical/modding-and-toolchain.md", "../../production/platform-and-release.md"]
---

# 引擎锁定：Unity 6

## Context / User intent

用户在比较价格、资产生态、单人开发难度、性能、画质、AI-agent-first开发、Modding、联网与长期维护后，明确决定本项目使用 **Unity 6**。随后进一步明确：正式渲染管线采用 **URP**；架构默认使用普通 **GameObject/MonoBehaviour**，只有Profiler/Profile数据证明某系统需要更高数据导向性能时才迁入DOTS/Entities/Burst/Jobs；并要求正式定义AI-agent-first项目结构。

## USER DECISION

DDD-0008-DEC · CANON · 来源：SRC-USER-2026-09-05-UNITY-ENGINE-LOCK。

**BREACH: ECHO / 《裂界残响》正式锁定 Unity 6 作为游戏引擎。** 后续技术设计不再要求保持Unreal兼容，也不再默认维护双引擎原型。若未来要改引擎，必须作为新的高返工成本SUPERSEDING决策处理，而不是普通实现替换。

DDD-0008-DEC2 · CANON · 来源：SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST。

**正式渲染管线锁定为 Unity 6 + URP。** HDRP不再作为并行正式生产管线，也不要求为其保留资产兼容层。若未来真实画质/性能证据证明URP无法满足产品目标，可另开SUPERSEDING决策；在此之前所有正式材质、Shader、VFX、Lighting、Fog、Decal、资产采购与性能预算均以URP为唯一生产基线。

DDD-0008-DEC3 · CANON · 来源：SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST。

**默认使用GameObject/MonoBehaviour；DOTS不是默认架构。** 玩家、武器、敌人、交互物、任务对象等首先按可维护的常规Unity方案实现。只有Profiler/Profile数据证明某一具体系统在目标硬件和真实负载下成为显著瓶颈，且DOTS/Entities/Burst/Jobs能够以可接受复杂度提供明确收益时，才迁移该热路径。不得为了“用了DOTS”提前把整套游戏数据化，也不得把DOTS存在本身当成性能证明。

DDD-0008-DEC4 · CANON · 来源：SRC-USER-2026-09-05-AI-AGENT-FIRST-STRUCTURE。

**项目必须正式采用AI-agent-first的工程结构。** 代码、内容、验证、构建和文档应尽量可由Agent通过文本、稳定ID、CLI/batch/headless流程读取、修改、验证和回滚；不得把关键Gameplay真相只藏在Inspector手填引用、不可diff的临时场景状态或纯手工Editor步骤里。具体目录、Assembly、Data Schema、自动化入口和Agent权限边界需作为独立结构决策逐项确认后冻结。

## Current implementation direction

DDD-0008-DIR · DIRECTION · 来源：此前Unity技术讨论；未逐项冻结部分保留为DIRECTION。

当前仍待验证/选择的Unity实现方向：
- 联网优先评估 **Netcode for Entities / Netcode for GameObjects / FishNet / Photon Fusion或其他Unity可用方案** 是否满足server-authoritative、player-hosted、host migration与snapshot/journal恢复合同；具体网络栈尚未CANON。
- AI-agent-first与Modding继续共用文本化、可验证、可CLI/headless的生产哲学；具体项目目录与SDK结构尚未冻结。
- Mod作者的主要工作流不应被强制绑定为“必须拿完整Unity工程直接改”；优先自定义ContentPackage/manifest/data/graph/script能力面。

## Why Unity won for this project

Unity的项目特定优势主要来自：C#文本代码与Agent可编辑性、较低单人迭代摩擦、Unity Asset Store/Fab等资产来源、必要时DOTS/Burst对高数量模拟的扩展能力、可自定义数据驱动Mod runtime，以及当前许可模式不按游戏销售额抽成。Unreal在默认高端画质、现成FPS框架和Fab/UE视觉整合上仍有优势，但这些优势不足以覆盖本项目对Agent-first、Modding、可维护性与系统模拟的权重。

## Licensing snapshot — not eternal canon

截至2026-09-05核对Unity官方当前条款：Unity 6 Runtime可在满足适用订阅/Tier条件时 **without royalty, revenue share, or runtime fee** 分发。Unity Personal当前适用于不超过US$200k年收入/融资门槛的游戏开发者；Pro当前起价US$2,310/年/席位，超过US$200k门槛时需要；Enterprise在超过US$25M年收入时进入定制方案。许可和价格会变化，发行前及续订前必须重新核验最新官方条款。

## Risks / tradeoffs

- Unity不会自动解决多人FPS、Host Migration、Mod安全、Steam Deck或大规模模拟；这些仍需原型证明。
- GameObject-first不意味着禁止DOTS；真正瓶颈必须以Profile证据处理，不能等性能崩坏后才设计数据边界。
- URP是正式基线，但仍必须通过本项目真实场景的Visual/Performance Gate；若画质不足，应先改资产、材质、灯光、Shader和表现策略，再考虑推翻管线。
- 购买资产可减少产量成本，但会增加视觉统一和许可证管理责任。
- AI-agent-first若变成“所有东西必须纯文本”，会损害美术和关卡制作效率；原则是关键真相可验证、可自动化，而不是禁止Unity Editor。

## Owner GDD links

[模拟架构](../../technical/architecture-and-performance.md)；[Modding与Agent工具链](../../technical/modding-and-toolchain.md)；[网络与持久化](../../technical/network-and-persistence.md)；[视觉方向](../../gdd/art-direction.md)；[平台与发行](../../production/platform-and-release.md)。

## Supersedes / next gate

SUPERSEDES：SRC-SSOT-2.0 §29.1中“引擎未锁”、旧URP/HDRP并行候选，以及旧“Hybrid GameObject+DOTS作为默认分工”的宽泛方向。新的规则是：Unity 6 + URP；GameObject/MonoBehaviour默认，DOTS仅在Profile证明需要时采用。

下一设计Gate：先正式定义AI-agent-first项目结构；之后逐项裁决联网栈、资产采购/license pipeline、Mod运行时格式与首个Unity技术Spike。

## 2026-09-05 implementation closure

本文件已确认的引擎/内容/命令/60Hz/复制合同继续有效；当时列出的provider、回溯、迁移算法、脚本、旧hash和UI未决项现在由DDD-0015–0017与其责任文档关闭。历史段落用于追溯，不要求重复询问所有者；具体TEST尚未执行。
