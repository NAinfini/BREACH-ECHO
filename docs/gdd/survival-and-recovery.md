---
doc_id: GDD-SURVIVAL
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 生命与失败系统设计
canon_basis: "SRC-SSOT-2.0 §4A.16、§8.4、§11"
depends_on: ["../technical/network-and-persistence.md"]
---

# 生存、倒地与失败恢复

## 玩家目的

失败前有可理解、可执行的补救机会；真正失误有代价，但死亡不能用来洗掉资源和任务后果。

## 范围与术语

Downed 是仍有有限行动的状态；Last Wind 是有效贡献触发自救；Last Chance 是团队无站立成员时检查已提交恢复路径；技术迁移恢复不等于游戏 checkpoint。永久收益归[进度](progression-and-bastion.md)。

## 已确认规则

LIFE-001 · CANON · 来源：SRC-SSOT-2.0 §4A.16、§11.2–§11.5。

Operation 没有 Gameplay Recovery Anchor/checkpoint rollback。恢复梯子是活着临场处理→Downed/Last Wind→队友 revive/carry→专用 ReviveEffect→已提交 Last Chance→不可恢复 Wipe。坏资源状态与 Cart 后果不能靠死亡重置。玩家不承受长期残肢惩罚。

LIFE-002 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0013–0018；原规则历史保留于Git。

Operation不回满；脱战低恢复线20%、手动救援3s/40%生命、起身Grace最多2s且攻击解除、倒地45s、Carry按半速消耗为TEST初值，归测试参数。所有比例基于当前合法HealthCap，不能恢复被牺牲/封印部分。Downed可爬行/Ping及用规则允许的枪，不能执行需要双手的重资产/Carry。普通Healing不等于Revive。

LIFE-003 · CANON · 来源：SRC-SSOT-2.0 §4A.16、§11.5。

Last Wind 接受有效击杀/贡献，队友助攻不能抢走恢复；已提交 DoT、Summon、Turret、Projectile、Reaction、ReviveDrone 继续运行。全员 Downed 不立即判死，合法恢复出现便取消 Wipe；防故意保留弱敌当无限保险。

## 玩家流程

LIFE-004 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

受伤→找安全或消耗医疗→倒地仍输出/标记→队友选择拉起或搬离→显示可用自救目标/贡献提示→团队全倒时显示仍存续的恢复来源→恢复或结算。失败画面列最后可观察的因果链，不能把未公开数据当“你应该知道”。

## 状态与数据所有权

LIFE-005 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

Authority 拥有 HealthCap、Health、lifeEpoch、DownedSince、eligibleContribution、ReviveTransaction、Grace、RecoveryCandidateSet。每次倒地生成唯一 lifeEpoch，所有恢复事务只可提交一次；呈现可提前准备但不能先改生命。医疗、投射物所有权与 Last Wind 贡献保持根事件关联。

| 当前 | 条件 | 提交结果 |
|---|---|---|
| Alive | FatalEvent且模式允许倒地 | Downed，登记倒地前已提交效果 |
| Downed | 有效 ReviveEffect/LastWind | Alive，原子恢复生命与短Grace |
| Downed | Carry开始/结束 | 更新搬运关系与bleedout策略，不复制身体 |
| TeamRecovering | 任一合法复活提交 | TeamActive，取消失败候选 |
| TeamRecovering | 所有恢复路径证明失效 | WipeFinal，发一次结果 |
| WipeFinal | 重复旧消息 | 只重发既有结果，不再次结算 |

## 模式配置

LIFE-006 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写；基线 SRC-SSOT-2.0 §11.5。

Operation 连续资源且无回滚；Descent 可有更宽松的层转换/增援 profile，但不回滚历史。恢复量只在公开 profile定义，不因团队“表现太差”隐形加保底。

## 内容接口与 Last Chance 存续

LIFE-007 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

可恢复 Provider 声明目标资格、触发条件、需要资源、未来推进条件与终止条件。Last Chance 建立有限可达候选集：已发弹、仍有目标的 DoT、已部署且能执行救援的设备等。任意视觉残留、无目标炮塔或不会产生 Revive 的循环不能拖住失败。

有时间推进的合法自救链继续模拟；不加随意十秒处决。若状态分析不能证明终止，必须让玩家看到还在等待哪条路径，并提供全体真人明确放弃此次尝试的候选动作；采用全体仍连接真人一致确认放弃，30秒未形成一致则继续合法恢复模拟；这不是任意处决计时，流程须测试。自动循环既无活目标也无恢复能力时可证明退出，不需要靠偷偷删伤害结束。

## 边界

LIFE-008 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

双人同时拉起同一玩家：一个事务胜出，其余取消未消耗成本；已消耗且已生效的过程成本不回滚。射手倒地后击杀由 AttackRoot 分配贡献，不按最后一击抢恢复。新倒地 epoch 不重复消费旧自救。断线身体保留权威状态，重连不刷新 Grace；Host 迁移冻结模拟时间。搬运者倒地则在最后合法位置解除携带，禁止掉出地图。刷弱敌防护候选是单次倒地贡献资格/有效威胁条件，初始贡献阈值与有效威胁资格见测试参数，不能全局封禁召唤物或队友助攻。

## 参数

| 参数 | 值/状态 | 来源 |
|---|---|---|
| Emergency Recovery Floor | 当前合法HealthCap的20% · TEST；数值归测试参数 | SRC-SSOT-2.0 §11.3、§40 |
| Revive Health | 当前合法HealthCap的40% · TEST；数值归测试参数 | SRC-SSOT-2.0 §11.4、§40 |
| Grace/bleedout/脱战判定/Carry影响 | 2s/45s/10s/半速 · TEST，详见测试参数 | SRC-SSOT-2.0 §11.3–§11.4 |
| 无限无恢复候选拖延 | 0例 · TEST验收 | 本轮边界测试建议 |

## 示例

LIFE-009 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮系统扩写。

正常：玩家倒地后先前火焰持续伤害满足贡献，Last Wind复起。失败：全队倒地，最后炮塔只会打尸体且无复活接口，候选集为空后结算。跨系统：医疗胶囊只有 Healing，不能因队伍全倒临时升级为复活；已提交 Revive Drone 仍沿合法路径救人。

## 验收与尚未实测项

LIFE-010 · TEST · 来源：本轮实验建议。

覆盖同帧死亡/击杀、双人Revive、断线搬运、迁移中DoT、无限无目标召唤、Wipe结果重发；要求零双重结算、零免费资源重置、零已提交合法自救被截断。测试尚未执行。防farm按唯一威胁/贡献资格，放弃按全体明确确认，Wipe不进入正史死亡；仍需实测。
