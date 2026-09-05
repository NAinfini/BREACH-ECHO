---
doc_id: GUIDE-GLOSSARY
doc_type: guide
stage: BASELINE
updated: 2026-09-05
owner_role: 文档维护负责人
canon_basis: "当前产品基线"
depends_on: ["start-here.md", "governance/authoring-guide.md"]
---

# 术语表 / Glossary

| 术语 | 在本项目中的意思 |
|---|---|
| Authority / 权威 | 唯一允许决定真实Gameplay结果的模拟，不等于谁发起聊天或谁的Hub |
| Host / 房主机器 | 同时运行本地玩家与共享世界的电脑；Host玩家仍走相同命令校验 |
| Epoch | 一代权威的编号；换主后旧编号消息不能再写世界 |
| Lease / 租约 | 在线协调器授予的短期权威资格；过期必须停止写入 |
| Snapshot / 快照 | 在明确tick边界足以重建游戏状态的数据，不是屏幕截图 |
| Recovery certificate | 一份已完整验证、有备份持有的恢复点证明，不等于所有最新画面都已持久化 |
| Command / 命令 | 玩家/Bot/测试提出的动作意图，可能被拒绝 |
| Event / 事件 | 已经发生并提交的事实，重复传输不能再次扣费 |
| Transaction / 事务 | 多个相关状态变化一起成功或一起不发生，例如扣资源并生成物品 |
| Idempotent / 幂等 | 同一个请求重试仍只有同一结果，不会多拿一次奖励 |
| Ruleset / 规则集 | 明确的一组模式政策；Operation和未来Descent不能偷偷混用 |
| ContentPackage / 内容包 | 有稳定身份、版本、依赖、hash与能力声明的内容集合 |
| Package Lock / 包锁 | 当前Run精确使用的所有内容及其hash；不是“都装最新版” |
| Hash | 对内容字节的身份检查；不是安全或许可证保证 |
| Graph | 本项目限定节点和能力的声明式规则图；不是任意代码执行权限 |
| PCG / 程序生成 | 用受约束规则组合人工制作内容，并验证可达与可解，不是随便随机摆房间 |
| Cluster | 带类型接口、路线/风险/资源语义的手制关卡片段 |
| MissionInstance / 任务实例 | 由锁定Seed、规则与内容包生成并验证通过的单局地图、目标、资源和威胁事实 |
| Source / 威胁来源 | 有预算、入口、预兆与结束条件的敌人进入依据；不是Director凭空刷怪 |
| Belief / AI认知 | AI依据合法视觉、声音、接触或通信保存的有限事实，不等于世界真相或玩家实时坐标 |
| ScreenStack / 页面栈 | 只让最上层页面或弹窗接收UI输入的前端状态结构，避免多个菜单同时响应 |
| FunctionalCommit / 功能提交点 | 动作真正产生弹药、伤害、物资或任务结果的权威阶段；可与动画收尾分离 |
| LearningObjective / 学习目标 | 本地提示系统记录的“未见/引入/练习/展示”状态，不是战力或匹配门槛 |
| Cell | 任务/设施供能资源，不是通用货币或Support Charge |
| Support Charge | 团队支援预算，提交合法Beacon才消耗 |
| Team Ordnance | 有唯一实例和有限弹药、拿起占双手的世界重资产，不是免费第三把枪 |
| Modification | 枪/工具/队伍协议的有边界修改；Operation不无限累计Relic或自动Fusion |
| Vertical slice / 垂直切片 | 一小段从开始到结束完整且代表产品的体验，不是很多不相连的功能 |
| Gate / 验收关卡 | 有明确证据要求的继续生产条件；没有测试不能标通过 |
| 决策记录 | 记录一项选择的理由、否决方案、边界、后果和重审条件；文件名与 ID 必须直接表达主题 |
| CANON / DECIDED / TEST | 明确用户事实 / 授权下已选决定 / 仍需测量的初始实验值；详见作者指南 |

世界内专有名词、创作别名和法律清查状态由[世界命名](gdd/world-naming.md)拥有；本表只解释开发与玩法术语，不再造另一套名字。
