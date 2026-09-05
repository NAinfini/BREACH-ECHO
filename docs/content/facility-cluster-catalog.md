---
doc_id: CONTENT-FACILITY-CLUSTERS
doc_type: content
stage: BASELINE
updated: 2026-09-05
owner_role: 关卡与环境内容设计
canon_basis: "当前手制Cluster+程序图、两区域首发范围与level-design方法"
depends_on: ["../gdd/missions-and-spaces.md", "../gdd/player-and-input.md"]
---

# 设施模块、空间指标与首发套件

## 单一责任与生产原则

CLST-001 · DECIDED。

本文拥有可拼接手制Cluster的空间指标、端口、功能与首发最低套件。生成器只组合经过灰盒验证的空间，不凭算法生成未经设计的走廊。流程固定为`指标→全灰盒→固定任务测试→程序组合测试→视觉装饰→性能/可访问性复测`；任何正式美术不得用来掩盖迷路、软锁或战斗视线问题。

## 玩家与空间指标

CLST-002 · TEST。

| 指标 | 灰盒初值 | 验证目的 |
|---|---:|---|
| 玩家胶囊 | 高1.8m、直径0.6m | Unity碰撞与门宽基准 |
| 单人通道净宽 | 1.2m | 可错身但不适合作战阵地 |
| 双向战斗通道 | 2.4–3.2m | 四人、敌人和重资产通过 |
| 标准门净开口 | 宽1.4m、高2.2m | TPS相机、搬运与敌人通过 |
| 重资产/搬运门 | 宽2.4m、高2.6m | 防止任务物卡死 |
| 标准层高 | 3.2m；战斗厅5–8m | 灯光、相机、弹道与敌人轮廓 |
| 交互距离 | 1.5m | 不让镜头贴面或隔墙操作 |
| 舒适楼梯 | 0.18m高/0.28m深 | 键鼠、控制器与NavMesh |
| 必经落差 | 不超过无需跳跃可达范围 | 主线不考精密平台跳跃 |
| TPS相机退距空间 | 目标后方至少1.0m可压缩区 | 狭窄空间不穿墙 |

这些是第一版Unity灰盒值，不是已经测试的最终人体工学。移动速度、跳跃、滑铲和重资产尺寸改变时必须重新跑指标场景；不能只改玩家Controller。

## 端口合同

CLST-003 · DECIDED。

端口类型为`Personnel / Cargo / Maintenance / Vent / Power / Data / Fold / ThreatIngress / Optional`。每个端口声明局部坐标/朝向、包围体、双向性、门/锁能力、NavMesh link、相机净空、可通过实体类别、封闭行为、声音传播和视觉遮挡。连接只允许兼容类型与尺寸，连接后必须有实体接缝、密封/门框或明确断裂表现；禁止两个房间网格重叠但逻辑上相连。

Power/Data是逻辑连接，不自动生成可行走通道；ThreatIngress只能由遭遇系统消费，不能同时当秘密出口。Optional支路默认至少有前方重接或清楚标示的返回成本。Fold端口只连接已经验证的界桥过渡Cluster，不让普通门随意传送。

## 共享功能Cluster

CLST-004 · TEST。

| Cluster ID / 工作名 | 功能与节奏 | 端口/关键对象 | 战斗与失败边界 |
|---|---|---|---|
| `cluster/insertion-lock` 插入闸 | 安全落点、任务建立 | Personnel×1–2、Data | 不在出生点立即射击玩家 |
| `cluster/junction-small` 小型分岔 | 二选一路线与方向记忆 | Personnel×3、Optional×1 | 至少一个可识别地标 |
| `cluster/cargo-spine` 货运脊线 | 搬运、长视线、重资产 | Cargo×2、Personnel×2 | 提供侧掩体，不成无解射击走廊 |
| `cluster/maintenance-loop` 维护回环 | 潜行侧路与前向重接 | Maintenance×3、Vent×1 | 封门后仍有合法返路 |
| `cluster/power-room` 配电室 | Power选择与设施变化 | Power×3、Personnel×2 | 提交前可预览影响 |
| `cluster/terminal-hall` 终端厅 | 查询、载波与权限 | Data×2、Personnel×2 | 终端前不靠无限守圈填时长 |
| `cluster/security-control` 安控室 | 接管炮塔/机器人 | Data、Power、ThreatIngress | 接管保留资产现状 |
| `cluster/storage-grid` 仓储格 | 搜索、价值与伏击 | Cargo、Optional×2 | 任务物不生成在同钥匙锁后 |
| `cluster/research-lab` 研究舱 | 数据校验与样本 | Data×2、Power、Optional | 证据与危险同区但可观察 |
| `cluster/coolant-works` 冷却工段 | 泄漏、环境状态 | Cargo、Power×2 | 热/毒路径有非颜色提示 |
| `cluster/fabricator` 制造间 | 技术/维修选择 | Cargo、Power、Data | 不能无限制造任务资源 |
| `cluster/quarantine-ring` 隔离环 | Predator诱导与封锁 | Personnel×3、Power、ThreatIngress | 敌人有真实路径，门态可验证 |
| `cluster/glyph-branch` 字形支路 | 秘密风险/奖励 | Fold或Optional×2 | 不盲猜，不是主线唯一解 |
| `cluster/extraction-bay` 撤离舱 | 结局、最后资源决策 | Cargo、Personnel×2 | 撤离压力有来源且可结束 |

## 两套首发区域套件

CLST-005 · TEST。

限界探索区“防线套件”首批需要：插入闸、小型分岔、货运脊线、维护回环、配电室、安控室、仓储格、冷却工段、隔离环、撤离舱各至少两个灰盒变体；特点是门区、射界、备用电源、炮塔底座、机器人路径和清楚的隔离分区。

无限探索区“远拓套件”首批需要：插入闸、小型分岔、货运脊线、维护回环、终端厅、研究舱、制造间、仓储格、字形支路、撤离舱各至少两个灰盒变体；特点是未完成扩建、长物流链、临时实验接缝、较少固定防御和更多资料/废料空间。

“两个变体”必须改变路线、视线、端口或系统位置，不能只是旋转、换材质或移动箱子。两套可共享结构语言和生产组件，但不能共享到区域问题消失。

## 导航、节奏与可读性

CLST-006 · DECIDED。

每个Cluster提供玩家NavMesh、至少两种敌人半径的可达标记、门链接、攀行/特殊链接、掩体候选、声音区和相机测试轨迹。关键路径有一致的灯光/结构引导，Optional和危险入口使用不同形状语言且不只靠颜色。任务Beat采用上升锯齿：高压Cluster之间必须允许生成低压缓冲；高潮前至少一个可读准备空间，不保证免费补给。

## 验收与未证明项

CLST-007 · TEST。

每个灰盒以FPS/TPS、1–4人、三种携带尺寸、五种常规敌人、门全开/全关和控制器跑通；无相机穿墙、NavMesh断裂、不可达任务物、不可见单向落差或重资产卡死。每套至少组合1000个图做结构验证、20个Seed人工路径评审、8名新玩家迷路观察。正式装饰后重跑视线、碰撞、性能和可访问性。所有结果当前为NOT RUN。

