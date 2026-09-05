---
doc_id: GDD-ART
doc_type: gdd
stage: REVIEW
updated: 2026-09-05
owner_role: 美术指导
canon_basis: "SRC-SSOT-2.0 §26；SRC-USER-2026-09-05-UNITY-ENGINE-LOCK；SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST；SRC-USER-2026-09-05-ASSET-SOURCING-NO-QUOTA；本轮美术讨论"
depends_on: ["canonical-world-history-and-lore.md", "../governance/decisions/unity-engine-and-rendering.md"]
---

# 视觉方向与可识别性

## 玩家目的与范围

一眼区分威胁、交互、阵营、武器与世界异常；项目独特性必须进入画面，不能停在筑路者/Fold/Resonance这些词里。

ART-001 · DIRECTION · 来源：SRC-SSOT-2.0 §26.1–§26.3。

Low-res retro dark sci-fi不能作为唯一品牌；canonical gameplay真3D，Retro/stylized/Full3D呈现可评估但不预先制作多套。Lore reason→shape/material→gameplay readability一致。人类/守门人建筑、筑路者、Fold空间、Resonance几何、材质/光、阵营、角色/武器/法杖、字体/图标、动画节奏与无色识别都需形成Visual DNA。当前尚未最终批准。

ART-006 · DIRECTION · 来源：本轮用户在单人开发、购入资产、Unity 6与游戏可读性约束下继续采用该候选进行讨论和图像验证；尚未明确冻结为CANON。

当前**领先候选**为 **Stylized Industrial Realism（风格化工业写实 / 半写实科幻）**：可信工业结构与材质逻辑 + 较强轮廓和大形体 + 控制表面噪声 + 明确游戏可读性。目标不是照片级AAA，也不是卡通低模，而是允许免费、购买、自制与AI辅助的基础资产经过Kitbash和统一修整后，仍能通过一致的材质、轮廓、比例、标识和光照形成项目自己的世界。

该候选目前是DIRECTION，不得因为已生成概念图就写成“Visual DNA Gate已通过”。

## 视觉语法候选

ART-002 · PROPOSED · 来源：本轮美术假设，非已制作资产。

| 对象 | 形状/材料候选 | 必须服务的玩法 | 不应发生 |
|---|---|---|---|
| 人类/守门人设施 | 可维修的分层设备、暴露维护逻辑 | 电力/门/交通状态可读 | 纯工业杂物遮挡交互 |
| 筑路者侵入 | 与人工尺度相冲的重复结构/负空间 | 识别异常区与禁忌接口 | 所有东西都成发光三角形 |
| Fold变化 | 连接关系变化有边界和连续线索 | 玩家理解前向重接与空间状态 | 闪光遮住真实传送/路径 |
| Weapon Module | 挂点、轮廓与动作可读变化 | 带入武器的改装身份 | 掉落等级颜色代替行为 |
| Team Ordnance | 明显双手体量、耗材/弹药显示 | 队友认出需要掩护的携带者 | 外观大但行为等同普通枪 |

ART-007 · CANON WORKFLOW · 来源：SRC-USER-2026-09-05-ASSET-SOURCING-NO-QUOTA。

资产生产**不设置免费、购买、自制或AI生成的目标占比**，也不按预设比例分配资产家族。每个资产独立选择能通过视觉、技术、许可、修整工时和Unity性能Gate的最低总风险路径。默认候选顺序为：先搜索真正优秀且许可兼容的免费资产；没有合格候选时，以AI生成加人工拓扑、UV、材质、绑定和动画修整为主要路径；只有AI结果持续不过门、修整成本高于采购，或某个付费资产能明显降低总风险时才购买。来源比例只允许在生产后作为成本复盘数据统计，不能成为采购或生成KPI。

人类工业设施、管线、梯道、容器、普通机械、基础枪模、Humanoid动画和通用VFX更容易接受外部基础资产；四名外勤角色的关键轮廓、Human armor/exoskeleton language、核心武器外壳语言、虚空兽主体轮廓、筑路者结构与界桥必须有更强原创控制。一个资产家族可以混合来源，但都必须收敛到同一Visual DNA。不得把不同Marketplace或生成批次的完整角色/怪物原样并排，再靠统一后处理冒充同一美术体系。

采购、来源、许可证据和SDK/Workshop再分发边界由[Asset Policy](../production/asset-policy-and-provenance.md)唯一负责。Visual Gate通过前只能做少量代表性搜索、生成、采购和试装，不因当前候选领先而批量锁死资产库。

## Unity渲染边界

ART-008 · CANON · 来源：SRC-USER-2026-09-05-UNITY-URP-GAMEOBJECT-FIRST；技术责任见[TECH-ARCH](../technical/architecture-and-performance.md)。

项目正式使用 **Unity 6 + URP** 作为唯一生产渲染管线。HDRP不建立平行正式资产版本，也不为未来可能切换而维护兼容层。材质、Shader、LOD、VFX、Fog、Decal、Lighting和资产采购全部以URP为基线，同时必须满足Steam Deck性能和多人战斗可读性。Visual Gate仍然有效：URP已经锁定不代表当前美术方向、palette、材质语言或光照方案已经通过测试。

## 流程、状态与所有权

ART-003 · PROPOSED · 来源：本轮扩写。

先三张关键帧候选→同主题greybox应用→无Logo辨识与战斗可读性测试→批准一种视觉语法→才批量制作。资源资产归内容包，碰撞/命中真相归模拟；broken/sealed/charged等状态驱动呈现，不能由贴图反推规则。

状态表：原型概念→受控关键帧→玩法应用→评审批准→版本化资产；未批准图不作为全项目约束。当前已有生成概念图用于方向讨论，但没有正式3D生产资产证明视觉Gate通过。

## 模式、内容与边界

ART-004 · PROPOSED · 来源：本轮扩写。

Operation密度服务视线、资源、路线；Lab高效果密度仍遵守同一形状身份。内容卡包括轮廓、材质、缩略可读性、LOD、低色彩辨识、动画姿势、危险状态、叙事理由。多人VFX须让队友区分谁创造了当前机会；表现密度可降，命中体积不随LOD缩水。色觉差异、夜间模式、Deck小屏是早期测试条件。

## 参数、示例与验证

ART-005 · TEST · 来源：SRC-CHATGPT-REVIEW-1.0 §4.9、§6；本轮适配。

三张无Logo/HUD关键帧给10名未知项目者各看5秒；候选通过目标≥7人识别同一视觉世界，<3人只说generic sci-fi。另以静态灰度图测试门状态、敌人轮廓、可交互物。此为小样本否决启发，不是市场统计。

正常：关门后的机械锁位变化让玩家无需看HP条知道状态。失败：Fold漂亮但挡住狙击预兆，删遮挡层而不是延长敌人前摇掩盖视觉错误。完整palette/fonts/style仍OPEN，不凭文字宣称Visual Gate通过。
