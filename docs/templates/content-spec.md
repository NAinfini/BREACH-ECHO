---
doc_id: TPL-CONTENT
doc_type: template
stage: TEMPLATE
updated: 2026-09-05
owner_role: 设计流程维护
canon_basis: "本轮模块化文档实施包"
depends_on: ["../governance/authoring-guide.md"]
---

# 内容卡模板

此模板用于Weapon/Modification/Spell/Enemy/Room/Mission/Ordnance，不是预先批准一个新功能。填写已存在系统合同，缺能力先提出问题。

## 身份与状态
唯一content_id、definition/version、名称、owner_role、PROPOSED/TEST、源定位、profile eligibility、canon_namespace。

## 用途
玩家为何使用/遭遇它；与已有内容的动作差异；若仅数值皮肤，说明为何仍值得存在。

## 触发、动作与成本
触发事件/SourceScope/目标前置；输入阶段；每一成本何时commit；取消可保留什么。

## 输出、Tags与交互
效果图、Damage/Reaction/World等输出；TargetScope、能力许可、冲突/stack、被哪些合法效果消费；挂点/视觉/动画如适用。

## 模式差异
允许的ruleset与reward source；是否可Fusion/安装/掉落；禁止自行复制另一模式的经济。

## 状态与多人语义
实例所有者/公共性、拾取并发、draft资格、离队/死亡/断线、resource守恒、save/network字段和版本。

## 正常、失败与软锁
正常行动例；资源用尽例；重复/失效事件；任务物不可提前耗尽成为唯一钥匙；替代路线是设计而非隐形补资源。

## 反馈
动作前读懂代价、过程看懂进度、结果看懂世界变化；无色/静音/控制器/小屏条件。

## 验收
所需灰盒对象、合法状态组合、至少一项区别性观察、失败阈值与证据日志。内容未验证时明写未验证。

## 发布/依赖
包、依赖、权限、hash/版本、成熟度；正式内容、Lab、未来模式与归档用途分开。



## 当前生产补充

内容必须声明Operation/Lab/FUTURE的准入，数值TEST不等于发布完成；购入/AI来源记录provenance和许可，禁止未经允许提交原资源到本公开仓库。普通已选行为可DECIDED，人物等创作身份按OWNER-01审阅。
