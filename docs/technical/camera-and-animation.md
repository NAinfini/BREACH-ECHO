---
doc_id: TECH-CAMERA-ANIMATION
doc_type: technical
stage: BASELINE
updated: 2026-09-05
owner_role: 摄像机与动画负责人
canon_basis: "当前FPS/TPS双视角、响应性动作阶段、Unity Animator/Animation Rigging/Cinemachine技术栈与camera-systems方法"
depends_on: ["unity-steam-and-modding-technology-stack.md", "../gdd/player-and-input.md", "../gdd/combat-and-arsenal.md", "../production/asset-pipeline.md"]
---

# FPS/TPS摄像机、动画与玩法时序合同

## 责任边界

CAM-001 · DECIDED。

FPS为默认视角，TPS可在任务中切换；二者共享同一玩家实体、武器实例、输入Command、射击起点规则和Authority命中结果。摄像机、Viewmodel、动画、IK和Shake只负责表现与输入投影，不能成为第二套伤害、交互距离、遮挡或敌人感知真相。

## 摄像机状态

CAM-002 · DECIDED。

基础状态为`FPS-Hip / FPS-ADS / TPS-Hip / TPS-ADS / Sprint / CrouchSlide / OrdnanceCarry / Downed / Interaction / Replay`。状态切换读取权威/预测动作阶段与本地视角偏好，使用显式Blend或Hard Cut；重生、传送、Host迁移恢复和回放跳转重置平滑速度，不能让相机跨地图甩动。

FPS yaw旋转玩家身体、pitch只转视角/瞄准枢轴；TPS使用Cinemachine Orbital Follow与Deoccluder，限制pitch并允许换肩。跟随在玩家Motor更新后执行，平滑用帧率无关阻尼，不用每帧固定lerp系数。TPS碰撞从角色枢轴到目标相机位置检测并推近，不能穿墙窥视；空间过窄时平滑压到近肩或FPS，不把玩家推离Gameplay位置。

## 瞄准、公平与遮挡

CAM-003 · DECIDED。

客户端视线产生Aim Intent，Authority按统一武器合同验证姿态、射击起点、方向、散布、遮挡与回溯。TPS准星不能让枪口穿过镜头看见但枪口被墙挡住的目标；近墙时显示受阻并由枪口/合法弹道决定结果。FPS/TPS的有效命中、后坐恢复、ADS精度、声音和移动成本相同，不能让某视角成为数值上位选择。

客户端可以预测相机后坐、枪口闪光与Viewmodel，服务器拒绝射击时必须快速纠正弹药/命中表现且不留下假伤害。Camera shake与真实weapon recoil分离；玩家可降低/关闭Shake而不改变弹道。

## 动画层与动作阶段

CAM-004 · DECIDED。

玩家使用Humanoid Animator + Animation Rigging；非人敌人使用Generic自定义骨架。玩家Animator至少分为Locomotion基础层、UpperBody Weapon层、Hands/Interaction层、Additive Reaction层和Viewmodel表现层。状态由语义参数与动作阶段驱动，不由动画事件私自扣弹、发伤害、开门或发奖励。

每个玩法动作定义`Windup → FunctionalCommit → Recovery → Complete`及合法取消窗口。换弹的弹匣就位、可开火、可ADS和动画完整结束是不同标记；`FunctionalCommit`由权威动作系统拥有，动画只消费并对齐。蓄力、射击、切枪、Quick Melee、Revive、拾取/放下重资产、攀爬和任务交互都使用同一阶段合同。动画缺失或低LOD时玩法时序仍相同。

## Root Motion、IK与多体型

CAM-005 · DECIDED。

玩家移动不使用动画Root Motion决定权威位置；Motor产生速度，Animator匹配。敌人攻击可使用经内容卡声明并由Authority验证的有限Root Motion/位移曲线，但碰撞和最终位置仍由Motor提交，不能借动画穿门。所有Root Motion曲线有固定SimulationTime采样和取消规则。

Animation Rigging负责手握武器、双手约束、脚部适配、瞄准与重资产持握。每件武器/工具提供Grip、Muzzle、Shell/Effect、ADS、Holster和Collision proxy锚点；每个角色骨架通过统一Avatar/手部姿态验证。IK失败必须回落到明确的武器专用姿态并报告，不允许手腕反折、手穿枪或枪口与弹道明显分离而仍通过资产Gate。

## 网络表现与LOD

CAM-006 · DECIDED。

网络复制动作语义、开始tick、阶段/normalized time、装备InstanceID和必要目标，不逐骨骼同步。远端客户端按权威阶段播放/校正；小误差平滑，大阶段错误切到正确动作。Host Migration保存玩法动作阶段，新Host恢复后动画从阶段重建，不重复FunctionalCommit。

动画LOD可以降低骨骼更新、IK、面部和次级运动，但不能隐藏敌人攻击前兆、部位失能、持枪状态或炮塔阵营。FPS Viewmodel只本地渲染且不参与世界碰撞；第三人称世界模型仍供队友、影子和回放使用。简化回放使用记录状态与代理动画，不加载完整旧物理模拟。

## 舒适性与设置

CAM-007 · DECIDED。

提供独立的鼠标/手柄水平与垂直灵敏度、反转Y、ADS倍率、FOV、镜头抖动、武器摆动、冲刺视野变化、动态模糊和降低动态效果。切FPS/TPS与换肩可重绑。调整FOV或关闭Shake不改变敌人可见性判断、弹道散布或后坐数值；强制动画镜头移动不得覆盖玩家视角超过完成交互所需的最短时段。

## 内容接口

CAM-008 · DECIDED。

可动内容资产必须声明SkeletonProfile、Avatar/Generic、AnimatorSet、动作阶段标记、Root Motion政策、IK Rig、WeaponPoseSet、CameraCollision proxy、第一/第三人称可见性、LOD与事件键。关键时序使用结构化数据并由Validator比较动画长度/标记与玩法动作；不能只靠Inspector里匿名Animation Event。

## 验收与未证明项

CAM-009 · TEST。

以30/60/120/144 FPS测试FPS/TPS移动、ADS、近墙开火、换肩、滑铲、换弹取消、蓄力预输入、重资产、Revive、Host迁移与回放；同一输入在视角间产生相同权威命中和资源。TPS零穿墙窥视，FPS/TPS无一帧跟随抖动，取消不复制弹药，LOD不丢攻击前兆。每个正式角色×六枪×三工具×三重资产跑握持/IK矩阵。结果当前为NOT RUN。

