---
doc_id: TECH-DATA
doc_type: technical
stage: BASELINE
updated: 2026-09-05
owner_role: 数据与存档负责人
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; DDD-0015; DDD-0016"
depends_on: ["architecture-and-performance.md", "host-migration.md", "mod-security-and-sync.md"]
---

# 数据、命令、事务和存档合同

## 标识与时间

DATA-001 · DECIDED。

稳定定义ID使用命名空间字符串，例如`breach.core/weapon/ar-01`；实例使用Run内唯一ID加generation；参与者使用内部ParticipantID，平台绑定只在服务适配层。RunID、TransactionID、ResultID、EventID、PackageID不得混用。自增tick为无符号64位；SimulationTime由tick/60推导，过场/轮盘/渲染不能改变其速率，迁移freeze不前进。WallClock仅用于联网租约、文件保留与诊断，不能驱动游戏伤害。

## 消息最小契约

DATA-002 · DECIDED。

| 记录 | 必需字段 | 接收校验 |
|---|---|---|
| GameplayCommand | protocol, run_id, epoch, participant_id, input_sequence, intended_tick, verb, target/instance IDs, bounded payload | 连接身份匹配；当前epoch；去重；tick窗口；动作阶段/资源/范围/权限 |
| CommittedEvent | schema, run_id, epoch, tick, event_id, transaction_id, cause/root_action, actor/target generation, result payload | 稳定ID去重；已发生事实，不重新扣费 |
| Transaction | transaction_id, expected revisions, read/write set, cost, outputs, commit_index | 前置版本全部匹配；先验证后一次原子提交；失败不发布半结果 |
| StateSnapshot | schema, run_id, epoch, tick, commit_index, chunk descriptors, state_digest | 长度上限；缺块拒绝；所有组件validate；恢复到隔离世界后才切换 |
| RunManifest | run_id, game_build, protocol, ruleset_id/version, seed hierarchy, package_lock_digest, capability_policy, participants/seats, difficulty, created_at | 不把账号秘密或任意脚本放入文件；完全锁定玩法依赖 |
| AccountClaim | result_id, run_id, participant_id, entitlement set, completion/recovery certificate reference | 只写本人账号；ResultID幂等；不可用Host提供的路径或账号ID越权写别人 |

消息枚举、单位、范围与拒绝码必须在第一个实现PR中落实为编译期DTO及正/负序列化测试；本表不是已经存在的SDK。

## 事务和效果顺序

DATA-003 · DECIDED。

每tick依次：冻结合法输入集合→稳定顺序校验命令→移动/碰撞与攻击候选→资源/伤害/状态事务→死亡/任务状态评估→派生Effect队列→提交事实和版本→统计/网络/存档投影。稳定排序键为phase、tick、actor stable ID、input sequence、effect index；同tick冲突不得取决于线程完成顺序或哈希表枚举。读写冲突需重验证，不做“最后一个网络包覆盖”。

资源不得从临时UI数字反算。重复支持信标只对应一个TransactionID；重试返回原结果。拾取先检查实例仍在世界，再原子移交旧/新持有状态。死亡取消未提交动作，已生成Projectile保留原root_action。Proc继承因果链，阻止同链重复环；合法配置超预算不能静默丢Damage，加载时拒绝不安全循环或将Run挂起并给出可定位错误。

## 保存格式与原子写

DATA-004 · DECIDED。

作者JSON UTF-8、字段明确、未知必需schema拒绝、数值范围有限且不能NaN/Infinity；类型选择必须使用允许枚举，不接受类名/反射表达式。运行时记录采用固定magic、format_version、schema_version、payload_length、压缩算法枚举、checksum及长度限定的组件块。整数little-endian；浮点仅在指定字段使用IEEE754且拒绝非有限数；字符串长度前缀UTF-8。不能把C#内存布局直接拷成长期文件。

写临时文件→flush并验证读回→同文件系统原子替换→保留上一个完好槽。先写payload后发布索引，断电不能得到“索引指向未写数据”。支持A/B轮换和generation计数，不能通过mtime猜最新。Steam Cloud只同步完成的账号文件及明确支持的已挂起Run，不同步不断改写的活动journal或临时回放。多设备冲突显示两份摘要并要求明确选择保留；不将两份Run资源相加。

## 进度、账号与会话信任

DATA-005 · DECIDED。

基础进度为本地优先横向解锁/收藏/外观，在线Steam身份不是竞技反作弊。玩家修改自己存档不是本项目要以侵入式系统消灭的问题，但不能借此写另一个玩家账号。完成结算以ResultID集合防重放；离线声明与在线声明使用不同签发来源且同样幂等。没有公开高风险排行榜或交易市场，因此不建立一套“证明本局没作弊”的经济后端。

正式发布前定义已发布schema的迁移测试夹具；仅维护明确支持的版本窗口和一次性迁移器，不保留多套旧运行时。预发布breaking change必须备份并说明重置范围；付费用户进度不能无告知丢弃。迁移失败保留旧文件和报告，不覆盖为默认空存档。

## 大小与安全

DATA-006 · DECIDED；初始限额TEST见测试参数。

解压前检查压缩大小、声明展开大小、chunk数和全局上限；流式解析并限深度，拒绝路径穿越、符号链接逃逸、重复规范化路径、整数溢出和未知可执行字段。Checksum/hash只能发现内容变化，不证明作者可信。日志默认记录内部诊断ID，不记录Steam票据、密钥、完整聊天或语音。世界秘密数据在Authority存在不表示UI可以向所有Client显示。
