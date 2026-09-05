---
doc_id: CONTENT-MODIFICATIONS
doc_type: content
stage: BASELINE
updated: 2026-09-05
owner_role: 构筑内容设计
canon_basis: "SRC-SSOT-2.0 §9、§40、§41.3；本轮配件讨论"
depends_on: ["../gdd/modifications-and-effects.md"]
---

# Operation修改目录与Lab实验

## 身份、范围与状态

REL-001 · TEST · 来源：SRC-SSOT-2.0 §9.1、§40、§41.3。
保留30件Relic与6–10配方的源试制规模。下面给出30件和8配方，全部具体效果为PROPOSED/TEST，不是已批准最终内容，不代表已实现、已平衡或所有模式可用。

REL-002 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮最新武器配件讨论。
Operation采用WeaponModule/ToolModule/TeamProtocol；传统Relic及自动Fusion在Lab/未来Descent验证。底层统一ModificationDefinition，配件不自动变成隐藏被动Relic，不被未知Fusion吞掉。共享语义见[Build](../gdd/modifications-and-effects.md)。

## Operation Weapon/Tool Modification 初版测试卡

MODC-001 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮武器改装用户意图与评审。
所有卡使用明确安装目标/挂点、相容Tag、tradeoff、冲突组、可见资产；mode_allowlist先为Operation实验profile。下面调整数值均TEST，未做平衡。

| ID/身份 | 安装与动作 | 收益/输出Tags | 代价与限制 | 反馈/验收 |
|---|---|---|---|---|
| WM-BREACH下挂破门弹 | WeaponInstance/Underbarrel；武器上下文选择 | Structure/Explosive，处理普通结构 | 重量/切换承诺+独立有限弹；不能免费开任务关键门 | 可见下挂、剩余弹；空弹仍有主线旁路 |
| WM-DAMPER后坐抑制 | WeaponInstance/Receiver；持续校准 | recoil降低候选20% | ADS进入慢候选10%，不改命中真相 | 比较页显示代价；偏好按场景分化 |
| WM-PRESSURE高压枪机 | WeaponInstance/Receiver；射击 | Armor/Piercing增加 | 每发耗弹/热提高；与Damper同挂点冲突 | 音/动作更重，不能凭空弹药 |
| WM-LINK智能链路 | WeaponInstance/Optic；授权瞄准标识 | KnownTarget信息辅助 | battery消耗，不穿墙发现未知目标 | 显示剩余电；无电不丢基础瞄准 |
| WM-REACTOR特殊弹仓 | WeaponInstance/Magazine；正常装填 | 兼容弹药增加ReactionTag | 弹族兼容收窄/容量降低 | 可见弹仓，明确能用什么ammo |
| TM-SINK应急冷却 | Tool/TechnicalMount；一次排热 | HeatReset，按工具资源消耗 | 用一次少一个耗材，非免费无限续航 | 明确消耗确认与冷却反馈 |
| TP-COVER协作协议 | Team；受掩护交叉火力窗口 | Team/Control短时稳定 | 只接受合法队伍事件，不叠乘Scan或复制资源 | 队友看见窗口，不新增常驻图表 |

每次改装均先预览冲突/损失，再原子装配，取消前不耗材；拆出的旧模块去向须由内容profile明确，当前候选放回世界而不是静默销毁。采用前线合法维护点3s安装，取消不耗材；不要求回Hub跑腿，具体见测试参数。

## Lab/未来Descent的30件Relic

REL-003 · PROPOSED · 来源：本轮内容扩写。
默认TargetScope=Player的自有合法攻击，SourceScope与成本以下逐卡覆盖；全部run-local，mode_allowlist=CombatLab候选，不直接进入Operation奖励池。输出均完整事件、保留Root/Owner。没有写数字的阈值OPEN，带数字的是TEST。

| ID/分类 | Trigger/Scope→输出/Tags | 成本、推进、冲突 | 与其他卡的连接及反馈 |
|---|---|---|---|
| R01稳相透镜/Scalar | 自有Direct Projectile→Damage×1.08 | 同Zone加算，不放大World来源 | Projectile增幅有来源列表 |
| R02沉稳机芯/Scalar | ReloadCompleted→下次Direct更稳 | 不返Ammo，单次消耗状态 | 与R09换弹触发；枪体小标 |
| R03重击垫层/Scalar | Melee Impact→Posture增幅 | 相同Zone、无额外攻击 | 与R13部位窗口；护甲音变化 |
| R04导热壳/Scalar | 停火冷却→Cooling增幅 | 缩短冷却不生成HeatSink | 与R12热锁链；热条可读 |
| R05长弧体/Scalar | 自有Electric Attack→range增幅 | 不自动加chain target数 | 与R17链弧；展示受益标签 |
| R06反应催化/Scalar | 自有ReactionEvent→effect增幅 | 不重复消费同状态对 | 与R11反应弹；明确zone |
| R07聚焦符/Scalar | Spell Channel→stability增幅 | 仍需引导承诺和家族资源 | 与R18折射；施法形状 |
| R08协作镜/Scalar | 合法TeamWindow→本人成本不变的precision | 不叠加团队伤害taken | 与R16窗口；队友小图标 |
| R09换弹线圈/Connector | ReloadCompleted→下一次Attack带Electric | 消耗一次武器已有overcharge状态 | 接R05/R17；首发电弧 |
| R10偏转计/Connector | 成功Parry→一次ReloadAdvance | 需真实威胁碰撞，不对空刷 | 接R09；装填阶段提示 |
| R11反应棱/Connector | ReactionEvent→短延迟Projectile | 明确delay与已有状态消耗 | 接R01/R17；可追溯子弹 |
| R12热锁转轮/Connector | OverheatEntered→短Range pulse | 热锁真实发生，不能反复同阈值 | 接R06；声波环 |
| R13碎甲指针/Connector | PartBroken→短TeamWindow | 只首次部位破坏 | 接R08；弱点开口 |
| R14回身缆/Connector | ProjectileReturn→UtilityChargeProgress | 弹体需真实返回，Lab资源权限 | 接R23/R25；回收反馈 |
| R15印记继电/Connector | MarkedTargetDeath→传递合法Mark | 需死目标与合法已知下一目标 | 接R16；转移线，不穿墙发现 |
| R16焦点转换/Connector | TeamWindow内合法Hit→短Overcharge | 每窗口状态消耗、不是每弹无限加 | 接R09；窗口状态可见 |
| R17支路弧/Rule | Electric Attack→有限邻近chain | 目标集合去重，每跳有travel | 接R11；弧线可读 |
| R18棱面/Rule | 自有Projectile进入自有Field→改变方向 | 同Field同Projectile只一次，非复制 | 接R07；折射平面 |
| R19借势/Rule | Melee命中staggered目标→位移 | 需实际目标状态；不teleport穿门 | 接R03；落点预览 |
| R20延时封装/Rule | 已支付Spell→延迟同定义输出 | 不绕cast cost，queue可保存 | 接R11；节奏信号 |
| R21余响许可/Rule | Triggered Attack可供指定connector消费 | 明确scope，拒绝零推进环 | 接R09/R11；Build页显示边 |
| R22自耗回补/Rule | HealthSacrifice→资源转换 | 扣合法HealthCap内真实生命，Lab许可 | 不以EmergencyFloor无限白赚；警示成本 |
| R23回旋阵列/Transformer | 一种ProjectileWeapon→可回收轨道 | 转换Magazine/Reload语义，仍占Weapon | 接R14；形态明显改变 |
| R24导流阵地/Transformer | 既有Field与攻击→网络节点路径 | 需部署位置与通道资源 | 接R18；地面/墙面节点 |
| R25循环电枢/Transformer | 有时间推进的return/recharge→周期回路 | 明确cadence/charge gate，非同commit自发 | 接R14/R21；核心环摘要 |
| R26共振战旗/Transformer | 多人不同合法输出→团队control区 | 需两个不同贡献，不做纯DPS吸血 | 接R08/R13；每贡献可见 |
| R27合成芯/Ingredient | 仅提供Fusion材料Tag SynthesisCore | 不独立发Proc；有可读用途 | 可与R09合成；成本预览 |
| R28轨道种/Ingredient | 提供OrbitSeed与轻Projectile稳定 | 不新增free ammo | 可与R23合成；轨道轮廓 |
| R29回声片/Ingredient | 提供EchoShard，记录合法延迟潜能 | 无同commit回声 | 可与R20合成；迟延音色 |
| R30界面钥/Ingredient | 提供ScopeBridge，允许明确scope转换 | 不开放MissionAdvance权限 | 可与R26合成；权限显示 |

R01–R08为8 Scalar；R09–R16为8 Connector；R17–R22为6 Rule Modifier；R23–R26为4 Transformer；R27–R30为4高交互材料。分类可重叠，但此池不靠重复换色达到数量。

## 8个自动消费Fusion候选

FUS-001 · PROPOSED · 来源：本轮内容扩写；自动消费原则继承SRC-SSOT-2.0 §9.5。
仅Lab候选ruleset启用。所有输入均为同一玩家实例，消费/继承/发现/输出同事务。表中每个结果是新Provider实例，可被下一配方消费；未知隐藏结果名称/效果但展示哪些旧件会消失。模式不能暗启用。

| RecipeID | 消费→新输出 | 继承与真实变化 | 成本/进度门与失败 | 反馈与验收 |
|---|---|---|---|---|
| F01 | R09+R27→C01回充线圈 | Preserve Electric标签，Merge合法属性；换弹后电击形态 | 仍需真实Reload；缺材料拒绝 | 新实例，旧listener全移除 |
| F02 | R23+R28→C02轨道架 | Magazine→OrbitCount，ReloadSpeed→ReturnSpeed | 公开转换，目标选择与travel推进 | 武器轨道可见，不只加伤 |
| F03 | C02+R14→C03回收引擎 | Preserve轨道与return，Rebind UtilityProgress到回收事件 | Lab资源许可；无返回则不回补 | Fusion-on-Fusion谱系完整 |
| F04 | R20+R29→C04延迟回声 | Convert部分cast节奏为已支付delay queue | 每次copy须有明确资源/状态门 | 迁移后delay只执行一次 |
| F05 | R13+R26→C05破阵旗 | Promote PartBreak为团队阵地触发，Preserve贡献 | 真实部位只破一次，不刷尸体 | 队友控制空间，不只强者清场 |
| F06 | R18+R24→C06折射网络 | Merge Field/Projectile交互，Rebind到节点port | 同弹同节点单次，路径travel推进 | 能预测轨迹，拒绝零推进环 |
| F07 | C01+R21→C07继电心 | Preserve换弹electric，扩大明确Triggered scope | 编译需验证没有同commit Reload循环 | Build页解释被允许的新边 |
| F08 | C03+R25→C08闭环轨道 | Convert回收进度为可持续周期，保留投入 | cadence+弹体travel+charge状态推进 | 合法loop持续；无目标时不拖LastChance |

Lab配方优先级TEST为F08=30、F03/F07=20、其余=10，再按稳定ID，规则仲裁责任在Build文档。不得把配方结果同时注册为原件listener制造双倍继承。

## 状态、边界与验证

REL-004 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：来源：本轮内容扩写。
每张卡都包含定义ID与版本、运行Instance、Owner、目标scope、效果图、模式许可、挂点/冲突、可见资产、成本与provenance；参数未定应使validator报告缺失，不按隐含0生成伪成功。实例消失后已提交弹体按提交快照继续，不能双重监听。

REL-005 · TEST · 来源：本轮候选池验收。
每卡单测触发/不触发/资源不足/目标失效/重复消息；每recipe测缺件、已发现/未知、重叠仲裁、输入同帧变化、迁移、返回队列。构筑测试至少包含一条合法时间循环与一个非法零推进环；四人能解释主链、自动消耗没有误解、Operation常规池无法铸造战略资源。全部尚未运行。


## 首发挂点映射与目录边界

MODC-002 · DECIDED · 来源：SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION；DDD-0014。

Damper与Pressure占handling槽；Breach、Link、Reactor占behavior槽，即使视觉分别装在枪下/瞄具/弹仓也不能同时占同一逻辑槽。Sink占tool槽；Cover占唯一team protocol槽。Breach附带固定2发独立破结构弹，不补关键Cell，基础枪参数不能复制出无限弹。Pressure初值每次有效射击耗2单位ammo且穿甲能力增加，倍耗同事务；Link用自身有限电池，不显示未知敌人；Reactor容量降低25%以换允许ReactionTag；Cover持续窗口不加倍Scan。数值均TEST，不扩充正式已验证目录。

30Relic/8Fusion全部明确留在Lab/FUTURE，缺参数的未来卡不可激活为生产内容；保留文案不是默许默认0或假装完成制作。
