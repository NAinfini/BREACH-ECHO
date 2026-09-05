---
doc_id: DECISION-UNITY-ENGINE-RENDERING
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 技术与产品负责人
canon_basis: "SRC-USER-2026-09-05-UNITY-ENGINE-LOCK；SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST；SRC-USER-2026-09-05-AI-AGENT-FIRST-STRUCTURE；官方Unity 2026许可资料"
depends_on: ["modular-product-architecture.md", "../../research/technical-evidence-2026-09-05.md"]
---

# 引擎锁定：Unity 6

## 背景与用户意图

用户在比较价格、资产生态、单人开发难度、性能、画质、AI-agent-first开发、Modding、联网与长期维护后，明确决定本项目使用 **Unity 6**。随后进一步明确：正式渲染管线采用 **URP**；架构默认使用普通 **GameObject/MonoBehaviour**，只有Profiler/Profile数据证明某系统需要更高数据导向性能时才迁入DOTS/Entities/Burst/Jobs；并要求正式定义AI-agent-first项目结构。

## 用户决定

ENGINEDEC-001 · CANON · 来源：SRC-USER-2026-09-05-UNITY-ENGINE-LOCK。

**BREACH: ECHO / 《裂界残响》正式锁定 Unity 6 作为游戏引擎。** 后续技术设计不再要求保持Unreal兼容，也不再默认维护双引擎原型。若未来要改引擎，必须作为新的高返工成本SUPERSEDING决策处理，而不是普通实现替换。

ENGINEDEC-002 · CANON · 来源：SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST。

**正式渲染管线锁定为 Unity 6 + URP。** HDRP不再作为并行正式生产管线，也不要求为其保留资产兼容层。若未来真实画质/性能证据证明URP无法满足产品目标，可另开SUPERSEDING决策；在此之前所有正式材质、Shader、VFX、Lighting、Fog、Decal、资产采购与性能预算均以URP为唯一生产基线。

ENGINEDEC-003 · CANON · 来源：SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST。

**默认使用GameObject/MonoBehaviour；DOTS不是默认架构。** 玩家、武器、敌人、交互物、任务对象等首先按可维护的常规Unity方案实现。只有Profiler/Profile数据证明某一具体系统在目标硬件和真实负载下成为显著瓶颈，且DOTS/Entities/Burst/Jobs能够以可接受复杂度提供明确收益时，才迁移该热路径。不得为了“用了DOTS”提前把整套游戏数据化，也不得把DOTS存在本身当成性能证明。

ENGINEDEC-004 · CANON · 来源：SRC-USER-2026-09-05-AI-AGENT-FIRST-STRUCTURE。

**项目必须正式采用AI-agent-first的工程结构。** 代码、内容、验证、构建和文档应尽量可由Agent通过文本、稳定ID、CLI/batch/headless流程读取、修改、验证和回滚；不得把关键Gameplay真相只藏在Inspector手填引用、不可diff的临时场景状态或纯手工Editor步骤里。具体目录、Assembly、Data Schema、自动化入口和Agent权限边界需作为独立结构决策逐项确认后冻结。

## 当前实现方向

ENGINEDIR-001 · DIRECTION · 来源：此前Unity技术讨论；未逐项冻结部分保留为DIRECTION。

当前仍待验证/选择的Unity实现方向：
- 联网栈已确认为[Steam Lobby/SDR + FishNet + BREACH自有迁移协议](network-runtime-and-recovery.md)；初始版本平台侧能力与公开Mod分发全部只走Steam。FishySteamworks和具体迁移参数仍须Spike，不维持多框架并行生产线。
- AI-agent-first与Modding继续共用文本化、可验证、可CLI/headless的生产哲学；具体项目目录与SDK结构尚未冻结。
- Mod作者的主要工作流不应被强制绑定为“必须拿完整Unity工程直接改”；优先自定义ContentPackage/manifest/data/graph/script能力面。

## 本项目选择 Unity 的原因

Unity的项目特定优势主要来自：C#文本代码与Agent可编辑性、较低单人迭代摩擦、Unity Asset Store/Fab等资产来源、必要时DOTS/Burst对高数量模拟的扩展能力、可自定义数据驱动Mod runtime，以及当前许可模式不按游戏销售额抽成。Unreal在默认高端画质、现成FPS框架和Fab/UE视觉整合上仍有优势，但这些优势不足以覆盖本项目对Agent-first、Modding、可维护性与系统模拟的权重。

## 许可快照——并非永久正史

截至2026-09-05核对Unity官方当前条款：Unity 6 Runtime可在满足适用订阅/Tier条件时 **without royalty, revenue share, or runtime fee** 分发。Unity Personal当前适用于不超过US$200k年收入/融资门槛的游戏开发者；Pro当前起价US$2,310/年/席位，超过US$200k门槛时需要；Enterprise在超过US$25M年收入时进入定制方案。许可和价格会变化，发行前及续订前必须重新核验最新官方条款。

## 风险与取舍

- Unity不会自动解决多人FPS、Host Migration、Mod安全、Steam Deck或大规模模拟；这些仍需原型证明。
- GameObject-first不意味着禁止DOTS；真正瓶颈必须以Profile证据处理，不能等性能崩坏后才设计数据边界。
- URP是正式基线，但仍必须通过本项目真实场景的Visual/Performance Gate；若画质不足，应先改资产、材质、灯光、Shader和表现策略，再考虑推翻管线。
- 购买资产可减少产量成本，但会增加视觉统一和许可证管理责任。
- AI-agent-first若变成“所有东西必须纯文本”，会损害美术和关卡制作效率；原则是关键真相可验证、可自动化，而不是禁止Unity Editor。

## 责任设计文档

[模拟架构](../../technical/architecture-and-performance.md)；[Modding与Agent工具链](../../technical/modding-and-toolchain.md)；[网络与持久化](../../technical/network-and-persistence.md)；[视觉方向](../../gdd/art-direction.md)；[平台与发行](../../production/platform-and-release.md)。

## 替代关系与下一 Gate

SUPERSEDES：SRC-SSOT-2.0 §29.1中“引擎未锁”、旧URP/HDRP并行候选，以及旧“Hybrid GameObject+DOTS作为默认分工”的宽泛方向。新的规则是：Unity 6 + URP；GameObject/MonoBehaviour默认，DOTS仅在Profile证明需要时采用。

AI-agent-first项目结构与Mod Runtime已由[Agent-first Mod Runtime](agent-first-modding-runtime.md)完成；Host Authority、Tick、Replication与Lag Compensation已分别由[Host Authority](host-authority-and-gameplay-commands.md)、[固定Tick与多频模拟](fixed-tick-and-multirate-simulation.md)、[状态复制](state-replication.md)和[延迟补偿](lag-compensation-and-server-rewind.md)完成。Provider/Transport、Session和Host Migration原则已由[网络运行与恢复](network-runtime-and-recovery.md)确认，等待Spike。资产采购/license流程由[Asset Policy](../../production/asset-policy-and-provenance.md)接管，仍有OPEN项。
