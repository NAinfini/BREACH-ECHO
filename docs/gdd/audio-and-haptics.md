---
doc_id: GDD-AUDIO
doc_type: gdd
stage: DRAFT
updated: 2026-09-04
owner_role: 音频与触觉设计
canon_basis: "SRC-SSOT-2.0 §19"
depends_on: ["ux-and-accessibility.md"]
---

# 音频、音乐、字幕与触觉

## 玩家目的与范围

在枪声、四人语音和效果密集时仍能识别危险、队友危机和任务变化。语音网络与频道规则归[合作](coop-and-social.md)。

AUD-001 · CANON · 来源：SRC-SSOT-2.0 §19.1、§19.3、§19.5。

Gameplay发语义事件，audio backend选clip/layer/spatialization，音频资产不驱动伤害/任务。Horde声源individual→cluster→virtualized，不为5000 AI保持5000 voice；用crowd beds与高价值单体线索。关键口语必须字幕，带speaker/priority/direction/location语义，关键字幕优先；方向字幕不泄露非法信息，SDH不把所有环境音变文字噪声。

AUD-002 · DIRECTION · 来源：SRC-SSOT-2.0 §19.2、§19.4、§19.7。

Audio bus数据驱动0..N，官方常用Master/Music/SFX/Weapons/Dialogue/VoiceChat/UI/Ambience/CriticalCue；致命预兆/倒地/任务危机不能被普通声音淹没。动态音乐读取CombatIntensity/Momentum/Boss/Faction/Biome/Quiet/Objective/LastChance/Victory等状态，不驱动gameplay，不假设固定三阶段。关键语义同时映射Audio/Visual/Haptic/Subtitle，呈现不改时序。

## 流程、状态与所有权

AUD-003 · PROPOSED · 来源：本轮扩写。

权威事件→可知性过滤→本地priority队列→关键cue保留→常规voice按距离/价值虚拟化→字幕/触觉同步。声音资产播放失败仍保留合法视觉提示与日志，不假装敌人动作没发生。

| 状态 | 事件 | 结果 |
|---|---|---|
| QuietMix | 有真实Horde来源预兆 | ThreatCue先于接敌，音乐按状态变化 |
| CombatMix | Boss/倒地/目标critical | duck非关键层，保留关键定位 |
| Virtualized | 进入相关范围 | 恢复合适表现，不补播所有旧声音 |
| LastChance | 合法恢复待定 | 读取生命状态，不以曲目结束判Wipe |
| HostMigration | 模拟冻结 | 音乐/语音可继续，游戏cue不多播 |

## 模式、接口与边界

AUD-004 · PROPOSED · 来源：本轮扩写。

Operation要有真正低压安静；Lab高密度也不把每个Proc都发独立高优先音。事件接口带root/source/known location、priority、interruptibility、semantic duration、SDH key与haptic类别。听不到的玩家需等价行动线索，不额外全图雷达。

同AttackRoot大量命中聚合声，不删除战斗事件。断线重放避免爆音堆积；客户端语言不同不影响战斗时机。硬件无haptic或用户关掉时，其他合法通道仍完整。Headphone/TV/夜间混音都要测试；默认不长期保存raw voice。

## 参数、示例与验证

AUD-005 · TEST · 来源：SRC-CHATGPT-REVIEW-1.0 §6；本轮适配。

四人语音+枪声+Horde混音中，≥80%参与者应在视觉接敌前识别压力来临；<60%失败，中间需更多样本。精确voice预算、duck量、haptic强度OPEN，不能把torture规模当实际音轨数。

正常：远处机械启动+合法字幕让队伍准备封门。失败：Gun音量淹没即死预兆，调整优先级而非事后暗改敌人时间。跨系统：Last Chance音乐只跟生命系统；音乐播完但Drone仍合法救人时不能判死。

