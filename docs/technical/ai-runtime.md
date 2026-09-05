---
doc_id: TECH-AI
doc_type: technical
stage: BASELINE
updated: 2026-09-05
owner_role: AI与导航负责人
canon_basis: "当前敌人感知管线、Unity AI Navigation、60 Hz多频模拟与game-ai方法"
depends_on: ["architecture-and-performance.md", "unity-steam-and-modding-technology-stack.md", "../gdd/encounters-and-difficulty.md", "../content/enemy-catalog.md"]
---

# AI决策、感知、群组与导航架构

## 单一责任与选定模型

AI-001 · DECIDED。

AI分为`Perception → Belief → Cohort → Intent → Action → Motor`六层。感知产生有限证据，Belief保存带时间与置信度的已知事实，Cohort只传播合法通信，Intent选择目标与动作，Action管理多帧前摇/Commit/恢复，Motor在权威模拟中执行移动和碰撞。任何层不得直接读取玩家输入、客户端相机、未复制秘密或全局玩家Transform。

首发采用“顶层有限状态机 + Combat内共享行为树”：FSM负责Dormant/Idle/Suspicious/Combat/Disabled/Dead等少量模式；行为树处理调查、接近、攻击、撤位、通信和部位失能后的优先级。暂不引入全局Utility AI、在线LLM或每敌人独立脚本框架；只有真实行为复杂度无法由共享树清楚表达时再评估。

## 频率与权威

AI-002 · DECIDED。

Authority拥有所有AI真相。感知采样、Belief更新和高层Think默认5–10 Hz TEST并按Cohort错峰；已选择Intent的移动、碰撞、攻击Commit和受击在60 Hz权威时基执行。可见/交战单位提高Think频率，远距单位降低，Dormant对象只响应事件。降频不能延长已公开攻击前摇、跳过合法受击、重置冷却或改变资源事务。

每次Think读取一个固定tick的只读世界快照，输出`IntentCandidate`；统一提交阶段按稳定EntityID排序验证目标、部位、路径、动作阶段和成本后写入。工作线程完成先后不影响选择。行为随机只使用RunSeed派生的`AI/{entity-id}/{purpose}`语义RNG流，不用帧时间或全局随机。

## Blackboard与Belief合同

AI-003 · DECIDED。

每个实体Blackboard至少包含：当前FSM状态、目标EntityID/generation、最后已知位置/tick/置信度、最近刺激列表、Home/Guard区、当前路径与revision、Intent/Action阶段、冷却、部位能力快照、CohortID、SourceID和Stuck状态。Blackboard只存稳定ID和有界数据，不保存Unity对象引用或行为节点私有世界真相。

Belief记录`subject/position/fact-kind/source-sense/confidence/observed-tick/expiry-tick`。看见玩家可刷新精确位置；只听到声音得到区域与不确定度；失去视线后只能调查最后已知区域。通信传递发送者当时的Belief，不把接收者升级成实时全知。过期事实衰减或移除，不能因为行为树重新进入Combat又恢复旧精确坐标。

## 感知与通信

AI-004 · DECIDED。

感知通道为视觉、声音、接触、伤害、能量梯度和明确设施信号。每种敌人内容卡声明通道、范围/角度、遮挡层、采样频率、刺激阈值和记忆；UI或渲染不可成为感知源。视觉必须做视锥与遮挡，声音通过房间/门传播图衰减，接触与伤害为Authority事件，能量只指向已供能区域而不是玩家坐标。

通信需要发送能力、接收范围/拓扑、前摇和真实响应Source。Scout完成呼叫只向已存在且有budget、Ingress和路径的Source提交请求；所有入口封闭时请求失败或延迟，不能生成隐形单位。部位破坏、门隔离、失去供能或协议重写可中断通信，并产生可读反馈。

## 行为树与动作合同

AI-005 · DECIDED。

共享树节点只返回`Success / Failure / Running`，多帧Action在Running时保存游标，不允许每个Think从头播放。Condition无副作用；Action只能请求明确Command，资源与世界变化仍由Simulation事务提交。树的顶层优先级为：致命状态/失能→已提交动作续行→近距反应→明确战斗Intent→调查Belief→守区/取食→Idle。

每个动作定义：前置能力与部位、目标范围、最小/最大距离、路径要求、前摇、Commit点、恢复、取消来源、冷却、输出事件和失败原因。选中Action后使用短期承诺与明确重评事件，避免每个Think在两个目标间振荡。目标评分只用距离、可达性、威胁、任务角色和最近互动等公开事实，不读取玩家血量UI外的秘密Build来克制。

## Cohort与遭遇Source

AI-006 · DECIDED。

Cohort负责有限共享Belief、阵形/占位意图和同一目标的角色分配，不是全图蜂群意识。一个Cohort最多在声明通信域内共享；域被门、距离或部位切断时分裂，恢复后可以合并但不回填从未观察的事实。Cohort可让Runner逼位、Suppressor封线、Flanker走侧路，但每个单位仍需合法路径与动作。

Director/Source决定“哪些单位可以在何处进入”，AI决定“已经存在的单位如何行动”。AI不能自行创建单位，Source不能给单位写玩家位置。Source预算、Ingress和Decay归[遭遇系统](../gdd/encounters-and-difficulty.md)。

## 导航与局部移动

AI-007 · DECIDED。

使用Unity AI Navigation：每个手制Cluster提供已烘焙NavMesh数据与显式门/梯/维护口/特殊体型链接，程序图拼接后验证连通区和链接revision。普通3D路径使用NavMesh，不自研密集网格A*；房间级战术选择使用Cluster Graph，多个单位前往同一区域时可共享房间级路径或flow cost。

路径只在目标跨过显著阈值、门/链接revision变化、超时或Stuck时重算，不每帧寻路。全局Path Queue有每tick预算与优先级，交战近距、脱困和任务关键单位优先。Motor沿下一个路径拐点Steer，局部避让不能把角色推出NavMesh、穿门或永久软占位卡住玩家。连续无进展进入`Stuck`，先重寻路，再选合法替代Intent；禁止传送到玩家身边，开发构建可以在明确日志后重置到最近合法点，发行版必须通过关卡/行为避免该状态。

## 设施单位与阵营改写

AI-008 · DECIDED。

设施炮塔、机器人和维护机复用感知、Belief、Action与Faction合同，但使用不同FSM。协议改写原子更新Faction、AllowedCommands、FacilityControlRevision和当前目标合法性；已经Commit的弹体/维修保留，未Commit的敌对前摇取消。己方命令限定为守区、跟随、守门、停火和指定合法目标等战术命令；不能接受玩家任意脚本或代替任务决策。

## 存档、复制与调试

AI-009 · DECIDED。

恢复状态包含FSM、Belief、Blackboard有界字段、Cohort/Source、Intent/Action阶段、冷却、RNG和路径目标/revision；具体NavMesh path可在恢复后重算，不把Unity内部引用序列化。客户端只接收表现所需的状态、目标提示和动作阶段，不复制完整Blackboard或未发现位置。

开发构建必须能显示实体ID、FSM、当前Intent/Action、最后刺激、Belief置信度、Cohort、Source、路径、NavMesh链接和Think耗时；能冻结/单步AI并导出Seed+事件，不修改正式结果。性能Profile按Perception、Think、Path、Motor、Animation分桶。

## 验收与未证明项

AI-010 · TEST。

固定Seed验证隔墙玩家移动不改变AI、失去视线只追最后位置、Scout无Source不召怪、封门后路径失效、部位破坏取消能力、协议改写换阵营、Host迁移不重置攻击和100/500/1000轻量敌人分频负载。代表性四人场景中AI Think错峰不得产生周期性帧尖峰；准确预算由性能Spike确定。行为、导航与性能当前均NOT RUN。

