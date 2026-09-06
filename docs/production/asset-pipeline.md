---
doc_id: PROD-ASSETS
doc_type: production
stage: BASELINE
updated: 2026-09-05
owner_role: 美术技术与资产集成负责人
canon_basis: "当前生产基线；用户确认不预设资产来源比例"
depends_on: ["../gdd/art-direction.md", "asset-policy-and-provenance.md", "../technical/unity-steam-and-modding-technology-stack.md", "../research/technical-evidence-2026-09-05.md"]
---

# 资产制作、绑定与 Unity 导入管线

## 单一责任

本文档只负责把一个已通过来源审查的候选资产变成可在 Unity 中验收的 Runtime 资产：尺度、拓扑、UV、材质、绑定、动画、碰撞、LOD、性能与导入。美术语法只由[视觉方向](../gdd/art-direction.md)决定；能否采购、保留证据或再分发只由[资产许可政策](asset-policy-and-provenance.md)决定。本文不再维护第二份许可登记表。

## 选定策略

PIPE-001 · DECIDED。先用原始灰盒证明玩法，再对通过来源、许可和视觉预审的候选资产做小批量集成。唯一 Visual DNA 已锁为“分层壁垒”：中等多边形的风格化工业科幻；低模只用于灰盒、远景、普通小道具、碰撞代理和 LOD。正式资产仍需通过同屏 Style Target、Unity 游戏视角、变形和目标硬件 Gate。

日常建模/修复/rig/LOD加工使用Blender受支持LTS并固定实际验证版本。可选AI来源先用Meshy API做一个人形和一个静态道具的受控试验；需要信用或商业条款时先获预算批准。没有购买任何方案，也不保证Meshy自动输出可以直接发布。Tripo等不建并行自动化链，除非实测Meshy失败且新决策记录替换收益。

## 端到端状态机

PIPE-002 · DECIDED。

`需求卡 → 参考/概念批准 → 来源与许可证登记 → 模型生成/采购/原创 → Blender清理 → UV/材质 → rig/权重 → 动画/retarget → 碰撞/LOD → Unity URP导入 → 游戏内验收 → 发布登记`。每一步有输入输出和失败回退，只有最后通过才标Ready。生成成功、FBX能打开、自动骨架出现，都不是Ready。

需求卡记录稳定AssetID、用途/视角/轮廓、米制尺寸、枢轴/握点/挂点、碰撞类型、骨架类型、动画需求、材质槽、目标内存/多边形预算、可破部位、引用文档和负责人。先用实际屏幕占比和最弱设备定预算，不靠统一“所有模型必须X三角形”替代性能测量。

## 可动资源的具体检查

| 阶段 | 产出 | 必须检查 |
|---|---|---|
| 图像/概念 | 轮廓、正侧背/关键机构说明 | 四名人物未批准前不得替他们定身体/年龄/面孔；概念图不是精确拓扑 |
| 3D与拓扑 | Blender工作文件+中间mesh | 实际尺度、法线、非流形、厚度、穿插、UV、材质槽；需要变形处有合适拓扑 |
| 人形rig | Humanoid映射、权重、root规则 | T/A pose、关节方向、肘膝/肩髋极限、手指/握把、脚底滑动、武器挂点 |
| 非人形rig | Generic骨架+稳定部位映射 | 足/触手数量、身体拓扑、各PartID与hit proxy；不依赖Humanoid假设 |
| 动画 | locomotion、瞄准、开火、换弹、受击、倒地、救援、携带、交互 | 原地/Root Motion策略声明；Authority移动不被动画位移偷改；取消阶段与事件语义对齐 |
| 游戏导入 | URP材质、LOD、collider、prefab、包内稳定引用 | Shader支持、贴图空间、GPU/内存、阴影、遮挡、视角/手型、碰撞不使用复杂渲染mesh默认值 |

Meshy Rigging API的人形限制不允许推导为所有四足/异形敌人可自动rig。Mixamo可用作获准人形占位动作来源，非人型仍需专用骨架和动画。游戏动作触发语义来自Authority动作定义；动画事件只能服务表现或回报受控标记，不能独立生成Ammo/Damage。

## 输入门槛与隔离

PIPE-003 · DECIDED。

只接受在[资产许可政策](asset-policy-and-provenance.md)中至少达到 `Cleared-Internal` 的输入。未登记、来源不明、条款存疑或可能泄露付费原文件的资产必须留在隔离区，不进入正式 Content Package。管线只读取 `AssetID`、允许面和证据引用，不自行重新解释许可证。

## 智能体自动化边界

PIPE-004 · DECIDED。

允许CLI完成命名、尺度检查、导入、LOD批处理、材质检查、截图和报告；每次外部生成请求记录参数、模型版本、任务ID、费用上限、结果hash和失败次数。未批准费用不调用收费API；重试有上限，不能无限耗积分。自动化不替代轮廓/变形/权利审查，失败任务留下诊断而不是往正式Content塞坏文件。

## 验收和后续

先用一件道具、一件人形占位和一个两种部位拓扑的敌人走完管线。记录实际人工修复时间、失败比例、三角形/材质/纹理内存及动画覆盖，再决定扩大来源。任何采购节省的建模时间都必须扣除风格统一、清理、rig、动画和集成成本。角色与最终配音只能在人物批准后排产。
