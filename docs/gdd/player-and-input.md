---
doc_id: GDD-PLAYER
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 玩家系统设计
canon_basis: "SRC-SSOT-2.0 §5、§7、§8、§11.1、§37、§40；SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY"
depends_on: ["operation-game-mode.md"]
---

# 玩家、配装与输入

## 玩家目的

从第一局就能移动、射击、快速近战、使用工具和救人；角色提供身份，玩家不必先招齐固定职业才能开始。

## 范围与术语

Weapon是Operation枪械平台；Utility是独立工具；Tactical Module是自由选择的个人战术动作；Ping 只表达沟通意图。资源见[经济](economy-and-support.md)，伤害见[战斗](combat-and-arsenal.md)，UI见[可访问性](ux-and-accessibility.md)。

## 已确认规则

PLY-001 · DECIDED · 来源：当前产品基线；历史见Git。

官方Operation入场固定两把枪、一件Utility工具、一件自由选择的个人战术模块，另有Quick Melee、手电、Ping。四名固定角色同局不重复Seat、Run内不换身份；装备与战术模块可重复。人物只固定叙事/视听身份，不锁职业能力。武器与工具身份在Run中稳定，通过明确挂点改装而非彩色等级换枪；世界Team Ordnance独立，不是免费第三把随身枪。旧两Utility/人物专属Active/无限Relic配置退出Operation。

PLY-002 · DECIDED · 来源：当前产品基线；历史见Git。

保留手电、Sprint、Jump/Crouch/Slide/Mantle/Air Control与Quick Melee lunge，无全局体力税。Gun点R执行真实Reload/Cycle；只有实际具有上下文动作才长按R显示轮盘。Operation不显示Staff/Spell入口。移动、输入缓冲和取消初值见[测试参数](../production/initial-test-parameters.md)，阶段提交不随渲染FPS变化。

PLY-003 · DECIDED · 来源：当前产品基线；历史见Git。

键盘默认1/2切枪、3选择/使用工具、4个人战术模块，E交互、Q语义Ping、R换弹、F手电、V快速近战；所有键可重绑并进行冲突检查。控制器用两个武器切换、工具选择/使用与战术动作的独立语义映射，具体物理键在首个InputAction资产及图示中固定并测试。模块需新动作/战场解法/效果连接至少满足两项，不能成为主任务必带钥匙。

PLY-004 · CANON · 来源：SRC-SSOT-2.0 §8.2、§8.4、§37。

Scan 是 Utility，对合法目标提供团队标记/承伤窗口，不穿墙、不揭秘密、不默认多人线性叠加；Ping 不附加 Scan。Utility 不共享全局冷却。普通 Healing 不能自动 Revive，须有明确 ReviveEffect。

## 玩家流程

PLY-005 · DECIDED · 来源：当前产品基线；历史见Git。

选角色与两枪/一工具/一战术模块→查看资源成本→进入任务→实际遇到时学习工具、救援、支援和改装。改装显示收益、代价、冲突与拆出物去向；取消不消耗，原子提交后才改变装备。不教授首发不存在的法术轮盘或自动Fusion。

## 状态与所有权

PLY-006 · DECIDED · 来源：本轮系统扩写。

Authority 拥有 CharacterLock、LoadoutRevision、装备 InstanceID、动作阶段、当前合法姿态；Client 拥有绑定、轮盘焦点、镜头偏好。动作命令携带 player、sequence、instance、input phase；权威检查角色存活/允许动作/物品仍装备后提交。UI选择不直接改装备。

| 起点 | 事件/前置 | 结果 |
|---|---|---|
| Ready | 按下攻击，装备合法 | Windup/Fire；即时本地输入反馈 |
| Windup/Reload | 被允许的取消动作 | 保存已完成阶段，进入新动作 |
| Ready | 长按上下文且存在候选 | RadialOpen；模拟继续 |
| RadialOpen | 松开且候选仍合法 | 提交选择；否则维持原选择并解释 |
| 任意可行动状态 | FatalEvent | 转生命系统，取消未提交动作 |
| Connected | 断线/接管 | 保留角色与配装，不生成新实例 |

## 模式配置与内容接口

PLY-007 · DECIDED · 来源：当前产品基线；历史见Git。

动作语义由共享系统实现，资源与允许内容由规则集控制。Character卡不声明独占Signature；TacticalModule卡独立声明verb、目标、成本/冷却、动作阶段和禁止场景。工具与模块资源分账。序列化保存CharacterID和TacticalModuleID为两个字段，不保留绑定与自由选择两套逻辑。

## 边界

PLY-008 · DECIDED · 来源：当前产品基线；历史见Git。

抢取世界物按首次合法事务提交，失败者不丢原物。死亡取消未提交切换，已发弹保留。拆下/dormant修改不监听新事件；轮盘目标失效时取消并解释，不能暗选另一个动作。重连以当前权威装备重建，不以客户端缓存覆盖；所有合法Seat组合均可完成主任务。

## 参数

| 参数 | 值与状态 | 来源 |
|---|---|---|
| 官方 Weapon / Utility / Tactical Module | 2 / 1 / 1 · DECIDED | Operation装备与改装决策 |
| Framework 槽位 | 0..N · CANON | SRC-SSOT-2.0 §1.5、§8.1 |
| Active 原型数量 | 3 · TEST | SRC-SSOT-2.0 §7.2、§40 |
| 操作至可见输入反馈 | ≤50ms 本地目标 · TEST | 本轮候选，不等于网络命中确认时间 |

## 示例

PLY-009 · DECIDED · 来源：当前产品基线；历史见Git。

正常：AR+Shotgun玩家用Foam延缓侧路，再用自由选Aegis掩护队友救援，各付工具/模块成本。失败：改装预览后目标revision已变，安装拒绝且不吞旧件。跨系统：两人同带Scan可刷新合法窗口，但不按人数线性乘算承伤。

## 验收与尚未实测项

PLY-010 · TEST · 来源：当前产品基线；历史见Git。

8名新手无口头指导完成移动、切两枪、用一工具/战术模块、Ping与Revive，目标每项≥7/8且零误扣关键资源。键鼠/控制器和不同FPS均测试；初值由测试参数拥有，未实测不称最终平衡。

## 最新入场配装意图

PLY-011 · DECIDED · 来源：当前产品基线；历史见Git。

两枪一工具的最新意图与旧两Utility基线的冲突已关闭：采用两枪+一工具+一自由战术模块，理由和覆盖关系见Operation装备与改装决策。

PLY-012 · DECIDED · 来源：本轮评审。
Operation入场锁定装备身份，局内有限Weapon/Tool Modification；具体次数由[测试参数](../production/initial-test-parameters.md)拥有。世界Team Ordnance独立于loadout，不占位，拿起时占双手，切主武器即放下，详细规则归[战斗](combat-and-arsenal.md)。

PLY-013 · DECIDED · 来源：SRC-USER-2026-09-04-RESPONSIVE-GUNPLAY-CANCEL-WINDOWS；SRC-USER-2026-09-04-PLAYER-MASTERY-PROGRESSION。

输入层须支持[战斗CMB-014](combat-and-arsenal.md)定义的换弹取消、切枪/ADS/Fire预输入与蓄力衔接，并让每个窗口基于动作阶段而非帧率偶然性。bunny hopping及其他移动技巧只作为TEST，不改PLY-002现行移动基线；缓冲、移动、受击与换弹按测试参数的动作提交/取消优先级实现。不得要求宏、隐藏Bug或外部攻略才能稳定执行。

PLY-014 · DECIDED · 来源：当前产品基线；历史见Git。

采用所有角色均可自由选择的个人战术模块；这是本次delegated决定，不冒充用户过去逐字确认。Character、选人UI、Loadout、存档和示例统一解绑；人物代号与人格仍由OWNER-01批准。

## PLY-015 · 默认实体输入映射（TEST）

下表是M0的明确可执行初值，不是要求所有者选择键位；玩家可重绑，所有冲突均在设置中提示。提示图标按当前输入设备更新。战斗中的菜单不暂停在线模拟；只有真正离线Solo暂停菜单暂停SimulationTime。

| 动作 | 键鼠默认 | 标准Xbox布局控制器默认 |
|---|---|---|
| 移动/瞄准 | WASD / Mouse | 左/右摇杆 |
| ADS / 开火 | 右键 / 左键 | LT / RT |
| 跑、跳、蹲/跑中滑铲 | Shift、Space、Ctrl | L3、A、B |
| 1/2号枪 | 1 / 2；滚轮切换 | Y切换；持重资产时Y先放下并切枪 |
| 单一工具 | 3选择工具，再Fire提交 | 持LB预备工具，RT提交；松LB取消预备；不能同时发主枪 |
| 个人战术模块 | 4 | RB；动作持续/取消依模块定义 |
| 交互/换弹 | E / R | X点按有合法近距交互时优先交互，否则换弹；持X明确换弹，点按与长按不能双触发 |
| Quick Melee | V | R3 |
| Ping/语义轮盘 | Q点按/长按 | D-pad右点按/长按 |
| 手电 | F | D-pad上 |
| 支援请求 | 持C打开，方向键输入，松C保留/关闭预览不扣费 | 持D-pad下打开支援选择，确认后方向输入；首个打开按键不计入代码 |
| 地图/物资 | M / Tab | View打开地图和物资分页 |
| 视角/换肩 | Z / Alt（TPS） | D-pad左点按切FPS/TPS、长按换肩；可拆分重绑 |
| 暂停/设置/社交 | Escape | Menu |

高风险支援代码完成后仍需合法投掷/放置信标；不会按完方向就远程扣费。控制器的交互/换弹双用途必须在首轮测试检查误操作，并提供将二者拆到任意可用按键/组合的选项；不能强迫残障玩家执行长按或高速代码，可开启等价顺序菜单/切换式输入，但仍付相同模拟时间与资源承诺。宏与设备高帧率不能改变提交时点。
