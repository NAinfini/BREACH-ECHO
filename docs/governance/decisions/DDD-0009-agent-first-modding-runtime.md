---
doc_id: DDD-0009
doc_type: decision
stage: BASELINE
updated: 2026-09-05
owner_role: 技术与Modding负责人
canon_basis: "SRC-USER-2026-09-05-AGENT-FIRST-STRUCTURE-A；SRC-USER-2026-09-05-OFFICIAL-CONTENT-PACKAGES；SRC-USER-2026-09-05-HOST-MOD-AUTO-SYNC；SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED；Steamworks Workshop官方实现资料"
depends_on: ["../decision-register.md", "../../technical/modding-and-toolchain.md", "../../technical/network-and-persistence.md", "../../production/platform-and-release.md", "DDD-0008-engine-unity6.md"]
---

# AI-Agent-first 工程结构与内置 Mod Runtime

## Context / User intent

项目已锁定 Unity 6 + URP，并明确采用 AI-agent-first 开发与开放 Modding。用户希望 Modder 能查看、继承、覆盖和修改官方 baseline gameplay data；希望官方内容自己使用同一套 Package 系统；多人加入 Host 时，Client 不应手工寻找、编辑和安装 Host 所需 Mods，而应由游戏自动完成匹配与安装流程。当前商业发行与公开Mod分发范围进一步收敛为 Steam-only，但底层结构必须与 Steam 平台服务解耦，避免把商店/Workshop ID写成Runtime真相。

## USER DECISIONS

DDD-0009-DEC-A · CANON · 来源：SRC-USER-2026-09-05-AGENT-FIRST-STRUCTURE-A。

采用 **Local UPM Packages + 独立 Content 数据层 + Assets 主要承担 Unity 表现/第三方资源** 的工程结构。Gameplay 语义真相优先保持文本/结构化、可 diff、可 validate、可由 Agent 修改；不把大量核心规则只藏在 Inspector/Prefab 引用中。

DDD-0009-DEC-B · CANON · 来源：SRC-USER-2026-09-05-OFFICIAL-CONTENT-PACKAGES。

**Official Content 自己也走与社区 Mod 相同的 ContentPackage / Registry / Schema / dependency / version / hash 加载体系。** 官方包拥有官方 namespace 和权限，但不得维护一套与 Mod 平行的隐藏内容模型。Official content 必须 dogfood public extension path；只有确有安全/平台/账号理由的能力可以保持内部专用。

DDD-0009-DEC-C · CANON · 来源：SRC-USER-2026-09-05-HOST-MOD-AUTO-SYNC。

多人加入使用 **Host Package Lock 自动同步**：Host 在正式连接前提供本局精确 gameplay package graph（package_id、version/content hash、依赖、来源标识、权限级别）；Client 自动比较本地状态，并为缺失或不匹配的可自动获取 Mod 执行下载、安装、验证、staging 和 profile 激活。玩家不需要手工修改 baseline 文件或逐个寻找 Host Mods。

自动同步不能绕过安全边界：Data/Graph/受支持 Sandbox Script 可以走标准一键同步；若未来允许 Native/unsafe code，则必须独立标识并要求显式授权，不能静默自动执行任意本地代码。

DDD-0009-DEC-D · CANON · 来源：SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY；SRC-USER-2026-09-05-STEAM-ONLY-SALES-MODS-DECOUPLED。

**当前公开Mod生态只以 Steam Workshop 作为正式发布、存储、发现、安装和自动同步渠道。** 当前不建设 mod.io、Epic/GOG Mod分发或另一套公开Mod Marketplace。Steam Workshop负责分发文件；BREACH 自己的 `package_id`、manifest、schema、dependency、permission、content hash 和最终 Registry 才是运行时权威。

Workshop `PublishedFileId` 只是 distribution locator，不得成为 Save、Network、Gameplay、Registry 或 Mod依赖关系的唯一身份。未来若商业发行范围发生变化，可以增加新的 Distribution Provider，而不改变 ContentPackage 格式和 Gameplay API；这只是架构解耦，不代表已承诺非Steam发行或跨商店Mod支持。

DDD-0009-DEC-E · CANON · 来源：SRC-USER-2026-09-05-OFFICIAL-CONTENT-PACKAGES；本轮用户要求 Modder 可改 baseline data。

官方 gameplay baseline **可 inspect / inherit / patch / override / replace**，但官方安装文件保持只读语义。Mod 不通过破坏性直接编辑 `Official/...` 源文件实现修改，而是声明 target stable ID 与显式 patch/override。运行时将 Official baseline + 已排序 Mod patches 编译为最终 Registry。这样更新、卸载、多人 hash、存档恢复、冲突诊断均可重现。

购买的第三方 raw assets 不因 gameplay baseline 开放而自动进入 SDK；只在许可证允许时分发源资产。否则 Mod 只通过受支持 runtime asset reference 或自带资产使用。

DDD-0009-DEC-F · CANON · 来源：SRC-USER-2026-09-05-HOST-MOD-AUTO-SYNC；SRC-USER-2026-09-05-STEAM-WORKSHOP-PRIMARY。

**BREACH 自带 Mod Loader 与多人同步协调层，玩家不需要安装第三方 Loader/Manager 才能正常使用官方支持的Mods。** Loader负责读取Package、验证Schema/依赖/权限/hash、编译Registry、启停Profile和Host同步。Steam Workshop可承担浏览/订阅/下载UI的一部分；游戏内完整Mod Manager的最终界面与功能密度仍可后续设计，但“第三方Mod Manager不是基础依赖”已经锁定。

## Multiplayer join flow

1. Host 冻结本局 Package Lock。
2. Client 在连接 gameplay authority 前读取 Package Lock。
3. 比对 package_id / schema / exact content hash / dependency / permission。
4. 对可自动获取的缺失包，从 Steam Workshop 自动下载；当前正式公开分发源只有 Workshop。
5. 显示总下载量、单包进度、权限级别、失败原因。
6. 下载完成后由 BREACH Loader validate + compile + stage。
7. 所有 gameplay package hash 与 Host 一致后才进入 Run。
8. 不一致、缺依赖、Workshop item 被删除/私有化、权限拒绝或验证失败则明确阻止加入，不做静默降级。

## Versioning caveat

Steam Workshop 默认会向订阅者传播当前适用的最新 item 版本，并提供与游戏 beta branch 绑定的版本兼容机制；这不等于我们可以随意按任意旧 content hash 从 Workshop 取回历史包。因此 active/suspended Run 仍应缓存其已验证 package artifact/hash，且 Steam 后续更新不得在 Run 中途热替换 gameplay package。新 Client 若无法从已批准来源获得 Host 锁定的精确版本，则不得伪装兼容；是否增加受限的安全包直传或官方内容寻址缓存留作后续网络设计裁决。

## Project structure consequence

正式结构保持：
- `Packages/com.breachecho.*`：Kernel、Gameplay、Content、Networking、Modding、Tools 等本地 UPM 包；
- `Content/Official`：官方 package 源定义；
- `Content/Schemas`：共享 schema；
- `Assets`：Unity presentation、Scene、Art、Audio、ThirdParty、Generated；
- `Mods/Dev` 与 `Mods/Samples`：开发和测试 Mod；
- `SDK`：公开 schema、模板、示例、文档；
- `Tools`：validate/build/pack/inspect/diff/test CLI 与 headless 入口。

Steam Workshop 是当前唯一正式公开 Distribution Provider，但 Runtime Package Model 与 Distribution Provider 解耦，因此不会把 Workshop 路径、PublishedFileId 或Steam API渗透进Kernel/Gameplay/Save schema。

## Risks / next gate

最大风险不是下载本身，而是版本锁、依赖冲突、unsafe code、安全提示、被删除 Workshop item、长局恢复和多人精确一致性。首个 Modding Spike 至少要证明：官方武器包与社区测试包走同一 Registry；Client 加入缺一个安全测试 Mod 的 Host 时可以通过 Workshop 自动下载、验证、启用并成功 join；缺失 exact hash 时明确失败；Vanilla profile 可一键恢复；关闭Steam分发适配器后，Kernel/Gameplay/Content验证测试仍不需要引用Steam类型。


## 2026-09-05 implementation closure

本文件已确认的引擎/内容/命令/60Hz/复制合同继续有效；当时列出的provider、回溯、迁移算法、脚本、旧hash和UI未决项现在由DDD-0015–0017与其责任文档关闭。历史段落用于追溯，不要求重复询问所有者；具体TEST尚未执行。
