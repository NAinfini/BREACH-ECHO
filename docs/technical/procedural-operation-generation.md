---
doc_id: TECH-PROCEDURAL-OPERATIONS
doc_type: technical
stage: BASELINE
updated: 2026-09-05
owner_role: 程序内容与验证负责人
canon_basis: "当前程序Operation管线、资源可解性与procedural-gen方法"
depends_on: ["architecture-and-performance.md", "gameplay-data-command-and-save-contracts.md", "../gdd/missions-and-spaces.md", "../content/mission-catalog.md", "../content/facility-cluster-catalog.md"]
---

# 程序Operation生成、种子与验证架构

## 单一责任与生成边界

PCG-001 · DECIDED。

生成器从已批准的区域、任务、Cluster、敌人Source和奖励表组合`MissionInstance`。它不创作任务规则、不修改内容定义、不动态照顾玩家Build，也不把无解地图交给玩家。生成先写入纯数据图并完成验证，最后才实例化Unity场景对象；场景`Awake`、PhysX结果、系统时间和全局Random不得参与内容选择。

## 确定性种子树

PCG-002 · DECIDED。

`MissionSeed`与game build、ruleset、content package lock一起写入RunManifest。每个生成阶段用语义路径独立派生子种子：`board/offer`、`region`、`site`、`primary`、`secondary`、`graph`、`objective-placement`、`resource`、`threat-source`、`ambient`、`secret`。新增一个装饰随机调用不能改变任务物或敌人位置；禁止共享一个顺序敏感的全局RNG。

同一Manifest必须得到相同逻辑MissionInstance、稳定InstanceID和验证摘要。表现性散布可有独立种子，但不能阻挡导航、遮挡交互或改变权威掩体。哈希算法和字段规范作为Protocol版本的一部分固定，升级后不假装旧Seed在新内容包下生成同一地图。

## 生成管线

PCG-003 · DECIDED。

生成阶段依次为：`RegionProfile → FacilityTheme → PrimaryTemplate → compatible Secondary → Situation/Mutator → Cluster Graph → Port binding → Objective placement → Required resources → Optional rewards → Threat Sources/Ingress → Navigation/visibility metadata → Validators → Frozen MissionInstance`。

每一步只读取前一步冻结结果与自己的内容表，并输出带revision的纯数据。失败包含阶段、规则、内容ID和Seed。单个Offer最多尝试32个派生候选TEST；超限后该Offer标为内容错误并由任务板生成新的独立Offer，不能无限循环、静默删掉目标或把资源塞到玩家脚下。CI或内容Cook出现稳定高拒绝率时阻止发布相关组合。

## Cluster Graph与端口绑定

PCG-004 · DECIDED。

先生成房间级有向多图，再选择满足端口类型、尺寸、方向、区域套件和任务Tag的Cluster变体。关键路径使用`Forward → Branch → Rejoin`，至少一个可解主路径；Optional支路长度、回接和风险受模板约束。连接后验证实体空间不重叠、所有行走/货运/维护/Fold端口相容、门两侧NavMesh链接存在、声学区和ThreatIngress归属明确。

图算法只证明结构，节奏由任务Beat约束：Introduce、Commit、Release、Escalate、Climax、Exit映射到可达Cluster，并保证高压间有允许的低压Beat。生成器不能为满足时长插入无任务、无信息、无风险选择的空走廊。

## 目标、资源与敌人布置

PCG-005 · DECIDED。

目标物放置使用显式约束求解：前置物不能在自己解锁的门后，多个模板不能争用唯一实例，任务物必须能被合法携带到目标，损坏/丢失有已设计降级。资源预算对每条批准主路径计算保证供给、必要设施成本、代表性战斗消耗和安全余量；具体数值来自测试Profile，不因玩家Build实时改变掉落。

敌人先放已记录休眠个体和守卫，再分配有限Source与Ingress。每个Source要有生态/设施理由、Budget、Telegraph、合法入口和结束条件；封闭全部入口后不能补怪。秘密奖励与额外威胁/Power/路线成本同一生成事务，重要故事不能依赖单一Seed或限时Offer。

## 验证器集合

PCG-006 · DECIDED。

| 验证器 | 必须证明 | 拒绝示例 |
|---|---|---|
| Schema/Package | 所有ID、版本、依赖与能力合法 | 缺定义、旧hash、禁止能力 |
| Topology | 插入到主目标/撤离可达，端口相容 | 孤岛、重叠、死端关键路径 |
| Objective FSM | 至少一条事件序列到Resolved/合法Degraded | 目标互锁、重复完成 |
| Resource Safety | 必需资源与任务物守恒 | Cell在需该Cell的门后 |
| Seat/Loadout | 1–4任意角色Seat、合法首发配装可完成 | 要求某角色/Staff/强制Bot |
| Navigation | 玩家、常规敌人、特殊体型与搬运路径成立 | 敌人只能穿墙抵达 |
| Encounter | Source、Ingress、预算、预兆、结束成立 | 封门后仍凭空spawn |
| Pacing | 教学先于致命测试，存在高低压与高潮前准备 | 连续全程高压、首见即团灭 |
| Secret/Narrative | 证据可推导、核心事实不永久错过 | 盲猜Glyph、唯一故事只在稀有Seed |
| Performance Budget | Cluster/灯光/AI/物件在静态预算内 | 已知超预算仍Cook |

验证通过后写`MissionDigest`并冻结。客户端加入只接收权威MissionInstance/必要表现数据，不自行重新Roll；本地重建摘要不符则拒绝进入。

## Authoring、Cook与诊断

PCG-007 · DECIDED。

内容作者通过JSON/Graph定义约束，CLI可执行`validate definition`、`generate seed`、`sweep seeds`、`render graph summary`和`explain rejection`。Unity Editor仅预览和摆放Cluster表现；关键端口、任务与资源合同必须可从文本检查。失败报告包含Seed、阶段、相关ID、最小冲突集合、图摘要和复现命令，不只显示“Generation failed”。

每日内容CI对每个主任务、区域和支线组合进行固定回归Seed与随机分层Seed扫描；失败Seed进入夹具。通过自动验证仍需人工评审路线、迷路、重复和节奏，因为连通图不能证明好玩。

## 网络、重连与版本

PCG-008 · DECIDED。

只有Authority创建MissionInstance；锁定后地图、目标、奖励与Source不因加入、离队、难度窥探、失败重试或Host迁移重Roll。恢复记录保存Frozen graph、实例、RNG子流状态和Digest，不依赖重新执行当前版本生成器。难度在RunStart前进入Manifest并影响公开Profile，不修改已经批准的任务事实。

## 验收与未证明项

PCG-009 · TEST。

每个合法组合至少自动扫1000个Seed，零崩溃、零无限循环、零无提示软锁、零非确定摘要；拒绝率、生成时间和内存须记录但阈值由真实实现校准。每组人工评审20个Seed，确认路线/系统/任务计划确有变化而非装饰变化。Host迁移前后MissionDigest与所有实例ID一致。所有结果当前为NOT RUN。
