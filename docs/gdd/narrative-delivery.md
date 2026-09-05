---
doc_id: GDD-NARRATIVE-DELIVERY
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 叙事系统设计
canon_basis: "SRC-SSOT-2.0 §35；SRC-USER-2026-09-05-COLLECTIBLE-ACHIEVEMENT-LORE"
depends_on: ["narrative-bible.md"]
---

# 叙事交付、对白与本地化

## 玩家目的与范围

玩家在行动中理解任务，重要信息错过后可补读，剧情播放不控制权威世界结果。正史归[世界观](narrative-bible.md)。

NDL-001 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：SRC-SSOT-2.0 §35.1–§35.2；来源属性：INHERITED。

通过briefing、Terminal日志、环境、壁垒NPC/Handler、Archive、短radio与少量高价值sequence交付；不长篇抢玩法。Dialogue semantic state与voice播放分离，战斗时可按定义暂停/转radio/继续/中断；重要内容Archive可恢复。Skip/快进只改呈现，不重复/漏掉已提交世界后果。选择0..N，重大team choice才SharedDecision，在线客户端按各自语言/字幕/skip偏好播放。

NDL-002 · CANON · 来源：SRC-SSOT-2.0 §35.3。

Text/subtitle/voice语言独立；缺voice asset允许内容回退，CJK/RTL/换行进入本地化验证。Glyph通常不作为普通语言翻译。

## 玩家流程、状态与所有权

NDL-003 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写；按SRC-USER-2026-09-05-COLLECTIBLE-ACHIEVEMENT-LORE调整。

触发语义事件→按优先级排队→本地播放→玩家可跳过/战斗打断→Archive保存合法发现。Authority提交ConversationChoice/WorldConsequence；Client拥有PlaybackCursor，不能以音频结束时间推进任务。公共行动知识不依赖Archive解锁，收藏只补充局部人物、事件与技术细节。

| 当前 | 事件 | 结果 |
|---|---|---|
| Pending | 高优先级战斗提示 | 延后普通台词 |
| Playing | 本地Skip | 已提交后果不变，转完成呈现 |
| Playing | 按定义被战斗中断 | 保存resume或转Archive摘要 |
| ChoiceOpen | 合法选择提交 | 唯一世界结果，关闭旧revision |
| Disconnected | 重连 | 恢复semantic state，不重复奖励 |

## 模式、内容与边界

NDL-004 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写；SRC-USER-2026-09-05-COLLECTIBLE-ACHIEVEMENT-LORE。

Operation短信息支撑设施决策；Lab不要求叙事。台词卡记录speaker role、text key、事实状态、触发前置、priority、interrupt policy、字幕/SDH、Archive target、world effect ID。收藏卡另记录载体、作者、可信度类别、语义兼容Cluster、关联集合、重复获取与成就条件。缺录音用已验证文字/字幕表达，不伪造已经制作配音。字幕方向不透露未知敌人位置。

日志、维护记录、私人通信、物品说明、Prototype来源、环境痕迹、守门人状态与隐藏字形房可以共同讲述同一局部事件。环境摆设不能单独冒充精确事实；带立场的文本必须保留作者身份；Archive明确标记`记录事实`、`当事人陈述`或`环境推断`。程序生成只移动完整的语义场景Cluster及其进入成本，不能把彼此关联的关键道具随机拆散到不相关房间。

## 参数、示例与验证

NDL-005 · TEST · 来源：本轮扩写。
普通战斗radio候选每条≤8秒、关键操作句≤20个中文字，作为可读性试测，非叙事硬约束。正常：一个玩家英文语音，一个中文字幕，共同任务同一提交。失败：播放未完成就跳过，门不会因此开两次。跨系统：上传后Archive补读证据，普通Lore不占紧急倒地提示通道。

NDL-006 · TEST · 来源：本轮实验建议。
测试CJK/RTL长文本、缺音频、全员同时skip、战斗中断、迁移及不同Archive完成度玩家组队；零重复世界效果，关键任务可在静音和零收藏条件完成。让未读世界观的测试者用两条独立线索复述一个局部事件，并检查其能否分清事实、证词与推断。完整语言列表、配音预算、演员方案、首批收藏数量和成就命名OPEN。
## 最新唯一历史与玩家故事约束

客观历史归[世界观](narrative-bible.md)，固定小队、非递进Operation与碎片收藏归[玩家故事](central-story-spine.md)。基础游戏不采用五幕、Final Truth任务、主结局、账号剧情stage或Post-Revelation双状态。本文只负责如何把公共事实和可选碎片交给玩家，不复制第二份历史。


## 本次定稿：执行边界

优先级采用关键战术事实→短人物评论→可选长背景；战斗不强播长档案，不让关闭语音失去关键操作信息。重复合同不重复假装首次发现核心历史。人物与创作事实仍按OWNER-01，短句/冷却初值为TEST；完整故事审阅入口已独立提供。

Authority: delegated，SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018。所有未提供实测的参数与验证仍为TEST；未展开的未来功能不在当前实现关键路径。
