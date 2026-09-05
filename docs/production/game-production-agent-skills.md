---
doc_id: PROD-AGENT-SKILLS
doc_type: production
stage: BASELINE
updated: 2026-09-05
owner_role: AI工程与制作流程负责人
canon_basis: "SRC-USER-2026-09-05-AGENT-SKILL-AUDIT；SRC-USER-2026-09-05-INSTALL-PRODUCTION-SKILLS-NOW；OpenAI、Unity与Blender官方资料；第三方Skill仓库只作已审计候选来源"
depends_on: ["../technical/architecture-and-performance.md", "../technical/modding-and-toolchain.md", "asset-policy-and-provenance.md"]
---

# 游戏制作 Agent Skills 能力地图

## 裁决摘要

用户已明确要求：不要等到某制作阶段才临时安装能力，当前就把已知完整游戏流水线需要的Skills准备好。因此本轮把此前的“到阶段再装”改为“现在安装、到阶段再启用工具与项目包”。这不等于安装互相冲突的所有社区Skill；采用标准仍是**最小完整覆盖、单一工具控制面、来源可追溯、全部可校验**。

当前项目级`.agents/skills/`共有 **36项，36/36通过Codex Skill格式校验**。加上环境已有的10项关键全局游戏Skill，当前生产能力面为46项。Skill可被发现不等于对应Unity工程、测试Harness、Blender会话或Steam后台已经可用；工具状态必须单独证明。

## 已安装能力总览

### 产品、玩法与内容

| Skill | 来源/状态 | 责任 |
|---|---|---|
| `game-design` | 全局已有 | 核心循环、经济、难度、残酷评审 |
| `prototype-fast` | 项目已装 | 用灰盒回答单一“好不好玩”问题 |
| `fps-shooter` | 全局已有 | 第一人称移动、枪感、TTK、后坐与命中 |
| `level-design` | 项目已装 | 尺度、白盒、路径、遭遇与张弛 |
| `procedural-gen` | 项目已装 | Seed、生成图、权重、确定性与掉落 |
| `puzzle` | 项目已装 | 机关、信息、状态与可解性；服务Operation任务，不把游戏改成纯解谜 |
| `dialogue-systems` | 项目已装 | 终端、语音、收藏叙事和分支数据结构 |
| `roguelike` | 项目已装，首发不触发 | 为Descent准备；不得污染Operation首发边界 |

### Unity实现与表现

| Skill | 来源/状态 | 责任 |
|---|---|---|
| `new-unity-project` | Unity官方，已装 | 新建真实Unity工程时的引导流程 |
| `unity-cli` | Unity官方，已装 | Editor/项目/测试/构建/CLI控制面 |
| `unity-package-management` | Unity官方，已装 | UPM包发现、版本核对与自动安装 |
| `unity-csharp-scripting` | 项目已装 | Unity 6.3 C# gameplay基础 |
| `unity-scriptableobjects` | 项目已装 | 编辑器数据与解耦；服从ContentPackage事实源 |
| `unity-input-system` + `input-systems` | 项目/全局 | Input Actions、重绑定、多设备、缓冲与无障碍 |
| `unity-physics` + `physics-tuning` | 项目 | 物理API、时间步、CCD、Layer与稳定性 |
| `unity-animation` | 项目已装 | Animator、Blend Tree、Layer、Avatar IK |
| `unity-navmesh` | 项目已装 | NavMesh、Agent与动态障碍 |
| `unity-build-pipeline` | 项目已装 | BuildPlayer、IL2CPP、stripping、CI |
| `ui-ugui` + `game-ui-ux` | Unity官方/全局 | Canvas层级、响应式HUD、菜单与焦点导航 |
| `shader-programming` | 项目已装 | Shader基础与跨引擎数学 |
| `unity-urp-dev` | 社区专项，已装 | Unity 6 URP/RenderGraph；精确API必须复核本地包和官方文档 |
| `validate-urp-render-graph-renderer-feature` | Unity官方，已装 | 自定义URP RenderGraph Feature复核 |
| `camera-systems` | 项目已装 | 第一人称观察、碰撞、舒适度与Shake接口 |
| `game-feel` | 全局已有 | 命中、射击、拾取与移动反馈 |
| `audio-design` | 项目已装 | Mixer、ducking、动态音乐、SFX变化与同步 |

### AI、网络、存档与性能

| Skill | 来源/状态 | 责任 |
|---|---|---|
| `game-ai` + `ai-behavior-trees-utility-ai` | 全局/项目 | FSM、BT、Utility AI与路径决策 |
| `multiplayer-netcode` | 全局已有 | Authority、预测、校正与Lag Compensation原则 |
| `save-systems` | 项目已装 | 原子写入、Slot、版本与迁移 |
| `performance-optimization` | 全局已有 | Profile-first、帧预算、GC、LOD与批处理 |
| `security-threat-model` | OpenAI curated，已装 | Luau、Workshop、MCP和后端的威胁建模 |
| `security-best-practices` | OpenAI curated，已装 | 安全实现与检查 |

### 美术、资产与发布

| Skill | 来源/状态 | 责任 |
|---|---|---|
| `create-game-assets` | 全局已有 | Art target、资产族、模型/贴图/来源/引擎验证 |
| `blender-mcp` | 项目已装，上游哈希一致 | Blender检查、编辑、渲染与数值/视觉复核规范 |
| `steam-publish` | 全局已有 | Steamworks、SteamPipe、Depot、分支与发布清单 |

## BREACH 专用验收技能

通用Skill不知道本项目的Authority Epoch、Package Lock、Luau能力边界、程序任务语法和资产许可制度，因此以下8项已现在创建并安装，不再拖到实现阶段。它们有真实Gate和证据格式，不是TODO占位。

| Skill | 项目责任 |
|---|---|
| `breach-unity-verification` | EditMode/PlayMode、Console、build、截图和性能证据 |
| `breach-network-soak` | 多客户端、延迟/丢包/抖动、迁移、JIP、Package Lock与状态hash |
| `breach-mission-generation-validation` | Seed复现、连通、Nav、可解、资源边界、逃生与隐藏房软锁 |
| `breach-mod-package-validation` | Schema、依赖、hash、Luau capability、无DLL、Cooked资产与Workshop边界 |
| `breach-asset-intake-and-rig-validation` | provenance、比例、拓扑、UV/PBR、骨架、权重、IK、LOD、碰撞与Unity实机动作 |
| `breach-release-gate` | Steam问卷、AI披露、许可、Depot、Deck、存档/Mod兼容与回滚 |
| `breach-localization-and-accessibility` | 稳定String Key、CJK字体、伪本地化、字幕、输入与UI无障碍 |
| `breach-visual-regression` | 固定场景/相机/曝光捕获、视觉差异和基线变更纪律 |

## 工具运行时现状

### Unity

- Unity CLI已按官方清单和SHA-256安装为`1.0.0-beta.8`，路径为`%LOCALAPPDATA%\Unity\bin\unity.exe`。
- `unity doctor --format json`成功；Windows long paths、Git credential helper和credential store通过。
- 当前进程尚未重载新增User PATH，因此doctor暂报PATH warning；新终端应重新验证。
- Unity账号未登录，CLI尚未登记Editor；这两项必须在创建真实工程前完成，当前不得写成“Unity工具链全部可用”。
- CLI仍是beta。必须固定版本，升级前先过项目Spike。

### Blender与Blender MCP

- Blender已由用户安装并验证为`5.2.1 LTS`。
- Blender官方Lab MCP扩展`1.0.0`已通过Blender自身TOML验证器安装并启用，位于Blender 5.2用户扩展目录。
- Codex侧使用`vinhelysia/blender-mcp`提交`a23c7fc4ca0a62ee09f3ee1f0edc0cb11191ceb2`，并以绝对路径注册为`blender`服务；`BLENDER_BINARY`固定到Blender 5.2.1。该连接器仍使用FastMCP v1 API，安装最新版`mcp 2.1.1`会启动失败，因此隔离环境已固定为最新兼容的`mcp 1.29.1`，不得无验证升级到2.x。
- 用户在知悉风险后明确授权持久开启Blender全局Online Access。端口只在Blender运行时绑定`localhost:9876`；端到端测试已完成MCP initialize、枚举26个工具，并通过`blender_get_objects_summary`只读取得Blender 5.2.1默认场景3个对象，`isError=False`。状态为**INSTALLED / CONNECTED / VALIDATED**。
- Blender官方明确警告：该MCP会执行未沙箱化的LLM生成Python。即使连通，也必须先读Scene、做小变更、验证并保存到版本控制；不得暴露密钥或个人目录，不得多代理同时写同一`.blend`。

## 明确不安装

- Godot、Unreal、Web Engine和2D Tilemap：引擎已锁Unity 6 + URP。
- IAP、广告、抽卡、移动商店：商业模型没有这些需求。
- 第二套Unity MCP或第二套Blender MCP：避免Editor控制面、端口和权限冲突。
- Unity Gaming Services live-game套件：当前Steam-only网络方案不采用UGS。
- Native DLL Mod工具：首发明确禁止。
- VFX Graph专用社区MCP：项目尚未安装VFX Graph；届时通过单一Unity CLI控制面操作，不引入第二套Editor桥。
- `security-ownership-map`：单人/早期仓库没有真实CODEOWNERS关系，当前只会制造假责任图。

## 使用与升级规则

1. 语义匹配才加载Skill，不把36项同时塞进单次任务上下文。
2. 项目决定与责任文档高于任何社区Skill；冲突时停止并报告，不让Skill偷偷重写产品方向。
3. 上游Skill升级前比较内容和触发描述，并重新运行`quick_validate.py`；Unity两个官方Skill因描述含`<genre>`已做仅frontmatter的Codex兼容修正。
4. 工具型Skill必须同时证明运行时、版本、权限和往返测试；文字说明不算工具可用。
5. Descent、对话、解谜等已提前安装的Skill，只有对应范围正式进入当前批次时才触发，不得预先实现未来模式。

## 完成判定

本轮“能力准备”完成条件为：36个项目Skills可发现且格式有效；Unity CLI和Blender MCP运行时完成安装与版本记录；Blender MCP通过26-tool端到端只读Spike；未执行的Unity工程、测试Harness和Steam后台环节明确保持NOT RUN；文档、来源和下一批状态同步。完整生产管线仍须等真实Unity工程和各专项Harness分别完成Spike后再升为“已验证”。
