---
doc_id: GDD-PLAYER
doc_type: gdd
stage: DRAFT
updated: 2026-09-05
owner_role: 玩家系统设计
canon_basis: "SRC-SSOT-2.0 §5、§7、§8、§11.1、§37、§40；SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY"
depends_on: ["combat-and-arsenal.md"]
---

# 玩家、配装与输入

## 玩家目的

从第一局就能移动、射击、近战、施法和救人；角色改变起点，玩家不必先招齐固定职业才能开始。

## 范围与术语

Weapon 是装备平台，Staff/Melee/Energy 均占正常武器位；Utility 是独立战术工具；Signature Active 是角色特征动作；Ping 只表达沟通意图。资源见[经济](economy-and-support.md)，伤害见[战斗](combat-and-arsenal.md)，UI见[可访问性](ux-and-accessibility.md)。

## 已确认规则

PLY-001 · CANON · 来源：SRC-SSOT-2.0 §5.1、§7.1–§7.4、§8.1、§37、§40。

官方默认两个 Weapon、两个 Utility、一个 Signature Active，并具备 Quick Melee、Ping、无限累计 Relic；Character 是 Soft Archetype，不锁定武器类别。官方小队由四名固定角色组成，同一局每个角色只有一个Seat且Run内不换角色；装备和Build可以重复。特殊 Artifact/TC 可显式改变规则。无 Equipment/Accessory、通用 Ultimate、通用 Weapon Active 或第二角色 Active。

PLY-002 · CANON · 来源：SRC-SSOT-2.0 §5.3、§6.3、§11.1、§37。

所有角色有基础手电、高速移动、无限 Sprint、Jump/Crouch/Slide/Mantle/Air Control/Quick Melee lunge；不设全局体力攻击税。Gun 点 R Reload/Cycle；只有实际存在模式才长按 R 出轮盘。Staff 长按 R 选择 Spell、松开确认、Fire 施放。Melee 左键轻击/蓄力、右键即时防御；R 不硬塞动作。合法 Rocket jump/impulse 可存在。

PLY-003 · DIRECTION · 来源：SRC-SSOT-2.0 §5.2、§7.2。

键盘 1/2 武器，3/4 Utility 快捷入口；Utility 保留 Tactical Use + select 的正式语义。Active 至少满足新动作、改变战场解法、丰富 Build hook 三项中的两项；不是单纯限时加伤，也不能成为 Operation 必带任务钥匙。

PLY-004 · CANON · 来源：SRC-SSOT-2.0 §8.2、§8.4、§37。

Scan 是 Utility，对合法目标提供团队标记/承伤窗口，不穿墙、不揭秘密、不默认多人线性叠加；Ping 不附加 Scan。Utility 不共享全局冷却。普通 Healing 不能自动 Revive，须有明确 ReviveEffect。

## 玩家流程

PLY-005 · PROPOSED · 来源：本轮系统扩写。

局前看角色动作与武器/工具成本→进入后直接使用完整动作→取得物品时比较当前装备→选择替换或放回世界→法杖轮盘只列当前持有法术。新手先学移动/攻击/交互/救人，再在实际遇到时学习工具和合成。界面显示已确认的行为差异，不用永久战力等级诱导配装。

## 状态与所有权

PLY-006 · PROPOSED · 来源：本轮系统扩写。

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

PLY-007 · PROPOSED · 来源：本轮系统扩写。

两模式共用动作语义；工具补给、施法资源和强度归各自经济 profile。Character 卡声明初始倾向、Signature verb、hook、反馈与禁用场景；Utility 卡声明目标验证、投掷/部署阶段、消耗点、共享标签。内容实例见[战斗原型](../content/combat-prototypes.md)。

## 边界

PLY-008 · PROPOSED · 来源：本轮系统扩写。

双人抢武器按世界拾取事务的首次有效提交裁决；失败者不丢原武器。死亡取消未提交切换，不取消已射出的投射物。换出的 dormant 物品不监听被动事件。轮盘中的 Spell 被消耗合成时按新 repertoire 重算，不选隐藏默认项。输入序号去重；重连回放权威配装，不以客户端缓存覆盖。任意一至四个不同角色Seat的组合都不得要求某 Active 才能完成主目标。

## 参数

| 参数 | 值与状态 | 来源 |
|---|---|---|
| 官方 Weapon / Utility / Signature | 2 / 2 / 1 · CANON | SRC-SSOT-2.0 §5.1、§40 |
| Framework 槽位 | 0..N · CANON | SRC-SSOT-2.0 §1.5、§8.1 |
| Active 原型数量 | 3 · TEST | SRC-SSOT-2.0 §7.2、§40 |
| 操作至可见输入反馈 | ≤50ms 本地目标 · TEST | 本轮候选，不等于网络命中确认时间 |

## 示例

PLY-009 · PROPOSED · 来源：本轮系统扩写。

正常：Staff+Sword 玩家先用场域阻挡射线，再冲入近战，两个武器各付对应成本。失败：控制器松开轮盘时目标法术已 Fusion，界面告知替换原因并要求重新选择，不偷偷施法。跨系统：两名不同角色都可带Scan；标记按规则刷新，不能按人数无限倍增承伤。

## 验证与 OPEN

PLY-010 · TEST · 来源：本轮实验建议。

8 名从未读文档的玩家在无口头指导下完成切武器、使用两个工具、Staff 换 Spell、Ping、Revive；每个动作成功率目标 ≥7/8，误消耗次数为零。精确按键、轮盘阈值、移动速度、跳跃高度、冲量上限均 OPEN，需结合关卡尺度实测。
## 最新入场配装意图

PLY-011 · DIRECTION · 来源：本轮用户固定Loadout/武器配件讨论。
用户更希望像GTFO先选两把枪与工具入场，局内围绕原武器改装，不不断拿彩色等级枪。其“一工具”的描述与PLY-001两个Utility及一个Active基线冲突，当前OPEN；不能静默删除槽位或把Staff移到免费第三武器。

PLY-012 · PROPOSED · 来源：本轮评审。
Operation推荐入场锁定装备身份，局内少量Weapon/Tool Modification；具体次数由[模式参数](operations.md)拥有。世界Team Ordnance独立于loadout，不占位，拿起时占双手，切主武器即放下，详细规则归[战斗](combat-and-arsenal.md)。

PLY-013 · PROPOSED · 来源：SRC-USER-2026-09-04-RESPONSIVE-GUNPLAY-CANCEL-WINDOWS；SRC-USER-2026-09-04-PLAYER-MASTERY-PROGRESSION。

输入层须支持[战斗CMB-014](combat-and-arsenal.md)定义的换弹取消、切枪/ADS/Fire预输入与蓄力衔接，并让每个窗口基于动作阶段而非帧率偶然性。bunny hopping及其他移动技巧只作为TEST，不改PLY-002现行移动基线；缓冲、移动、受击与换弹如何互相中断仍OPEN。不得要求宏、隐藏Bug或外部攻略才能稳定执行。

PLY-014 · OPEN（READY FOR USER VERDICT） · 来源：SRC-CODEX-2026-09-05-FOUR-CHARACTER-ROSTER-V1；角色候选见[CHAR-007](../content/character-roster-v1.md)。

固定四人且Seat不可重复后，PLY-001的角色Signature Active会让人物选择同时成为职业与强度选择。当前推荐保留一个Active槽，但把Active改成所有角色都能选择的`个人战术模块`，角色只固定叙事与视听身份。用户尚未批准，因此PLY-001暂不改；批准解绑时必须同步修改Character卡、选人界面、配装、存档和四人原型，不保留人物专属与自由选择两套并行规则。
