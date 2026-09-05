---
doc_id: GDD-COOP
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 合作体验设计
canon_basis: "SRC-SSOT-2.0 §19.6、§20、§21.5；SRC-USER-2026-09-05-FOUR-LIVING-FIELD-SQUAD-NONPROGRESSIVE-STORY"
depends_on: ["economy-and-support.md"]
---

# 合作、单人、Bots 与公共匹配

## 玩家目的与范围

每个人都能对局势有用，不开麦也能完成必要合作。固定好友队通过不能证明随机匹配和单人成立。

COP-001 · CANON · 来源：SRC-SSOT-2.0 §20.1–§20.3。

Bots可选默认OFF，单人无Bot可独立玩，最多0–3 AI队友；使用同样角色、武器、弹药、倒地规则，无隐藏无限资源。Human join可替代Bot slot。Bots不做Glyph/Forbidden/Gamble/Fusion/唯一团队资源的最终战略选择，不自主浪费稀缺物资。命令含Stay Here、On Me、Defend Here、Take this、Use Tool/处理Ping对象；真人全倒可打破Stay去救人。

COP-002 · CANON · 来源：SRC-SSOT-2.0 §19.6、§20.3、§20.5、§37、§40。

Public语音可用且默认Push-to-Talk；Global Team Voice不因房间/距离失声，非proximity-only；Party/Team成员相同可合并。语音独立于gameplay authority，迁移不应切断。Ping纯沟通，Quick Chat用Need Ammo/Healing/Group Up/Wait/Ready/Thanks/Sorry/Enemy/Go Here等semantic intent；Text默认Team/Party。无默认长期raw voice录制，沟通不暂停在线模拟。同一局四名固定角色的Seat不可重复，但武器与Build可以重复；物资公共，draft规则归经济。

COP-003 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：SRC-SSOT-2.0 §20.4。

颗粒度mute/block、Recent Players；公开Vote Kick且NetworkHost无单方owner kick，Private owner可移除私局玩家。AFK先警告、可接管/保护、投票/admin移除，不因轻微AFK永久惩罚。最小留存；Host可靠性与社会信用分开。

## 玩家流程与多人语义

COP-004 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

局前展示模式/资源/Mod profile→Ready→加入后简报当前目标和已提交选择→队友Ping目标→语义文字/图标同步→执行→结果页承认控制、救援、探路、供给和任务贡献，不能只按DPS排第一。

| 状态 | 事件 | 结果/Owner |
|---|---|---|
| Lobby | 所有内容hash与权限可接受 | 进入；不匹配明确原因 |
| ActiveHuman | 断线 | Authority保留seat/body/loadout |
| Reconnecting | 资格与profile一致 | 接回原seat，不增加draft额度 |
| BotSeat | 真人接替 | 转移同seat状态，Bot不复制装备 |
| AFK | 警告与公开阈值达成 | 依session profile接管/移除 |
| Blocked/Mute | 本地隐私选择 | 改通信呈现，不篡改权威战斗 |

## 内容接口与边界

COP-005 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

任务动作声明所需并发人数；官方主线必须有单人顺序解法。Bot只执行可验证的局部移动、射击、救援与明确工具指令，不规划最佳Cart、替玩家探索秘密或自动做战略经济。关键动作必须有non-voice表达：请求等候/集合/物资、提议路线、解释已提交配置、标记可接管资产。

抢拾取和并发花费归[经济](economy-and-support.md)；Cart失误归[世界](world-and-information.md)；Team Ordnance归[战斗](combat-and-arsenal.md)。离队/被踢不能删除已提交世界后果。Public不能让网络Host获得资源优先。恶意反复丢关键物、耗Support仍可能伤害队伍，UI日志不足以保证解决，列入风险Gate。

## 参数与模式配置

| 参数 | 值/状态 | 来源 |
|---|---|---|
| 官方参与人数 | 1–4 · CANON | SRC-SSOT-2.0 §1.1 |
| AI teammates | 0–3，默认OFF · CANON | SRC-SSOT-2.0 §20.1 |
| Voice | Global Team、PTT默认 · CANON | SRC-SSOT-2.0 §19.6、§40 |
| 公开Kick/AFK阈值/补位时机 | COP-009初值 · TEST | 需陌生人测试 |

COP-006 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

Public/Private可有不同社交授权profile，不能偷偷改武器战斗结果。是否首发公开Quick Match由无语音陌生人Gate决定；尚无证据时不能宣传“朋友能玩所以公共匹配没问题”。

## 示例与验证

COP-007 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

正常：无语音玩家Ping重武器，队友看到弹药和携带状态，授权Bot留守。失败：网络Host无法以Host身份单方面踢Public玩家。跨系统：接替Bot的真人继承当前座位已领Modification记录，不再获得一件首轮draft。

COP-008 · TEST · 来源：本轮实验建议。

分开测试好友队、陌生无语音队、单人无Bot、单人带Bot；记录无事可做时长、误拿、冲突、离队、任务理解和继续游玩。最强玩家也不能让其余三人连续多个遭遇仅观战。


## 已选社交初值与语音传输

COP-009 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0018。

Public踢人需除目标外仍连接真人的严格多数赞成，4人时需2票、3人时需2票；2人Public不允许单方踢人，允许离开/屏蔽并新建私房。投票30s，发起者120s冷却，避免轰炸；Private owner按公开规则可移除。AFK120s警告，180s可投票移除；不自动消耗玩家关键物或让Bot接管账号购买。重连Seat保留120s初值，之后可允许真人接替但继承同一身体/物资/claim状态，不刷新资源；旧玩家回来需要合法空Seat。以上时值均TEST。

Voice使用独立于Gameplay Host的Steam对等语音连接，1–4人小队最多每人三个发送目标，限流/声道优先级与Mute/Block本地生效；Host迁移不重建其余仍可用语音连接。真实提供者故障仍可能中断，不能保证“永不中断”。不把压缩语音写入Run或Replay。
