---
doc_id: GOV-AUTHORING
doc_type: governance
stage: BASELINE
updated: 2026-09-05
owner_role: BREACH ECHO documentation stewardship
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; delegated decisions DDD-0013–0018"
depends_on: ["owner-decisions.md", "decision-register.md", "document-register.md"]
---

# 文档权威、命名、决定和维护规则

## 权威不是文档成熟度

CANON：有明确所有者来源的要求/作者事实。DECIDED：当前所有者授权下已选的普通设计/技术决策，不冒充直接用户原话。DIRECTION：有来源但尚非完整规格的意图。TEST：实验参数/假设/验收目标，不能称实测。PROPOSED：未采纳候选。OPEN：真正未决且必须指向owner-decisions或未来工作边界。LEGACY：已覆盖，只保留历史。UNRECOVERED：原资料确实缺失，不能补造。风险标签RISK及历史组合状态只解释当时语境，不把它们当新审批。

stage描述文件用途：BASELINE当前可执行责任规格；REVIEW待创作审批；FUTURE非当前生产；ARCHIVE历史；TEMPLATE写作模板。BASELINE不等于实现、试玩、性能、许可或安全已通过。创作候选可以完整可读但仍REVIEW。

## 谁决定什么

2026-09-05所有者明确委托助手选择普通技术和设计赢家。选择引擎依赖、网络恢复算法、schema、文件名、测试初值、一般内容取舍不再逐项询问所有者。涉及人物/故事最终身份、正式视觉/配音、真实付费合同账户以及变更明确要求，按[所有者队列](owner-decisions.md)。提出建议时给理由与代价，不盲目附和。

冲突处理：先确认时间、来源和适用模式；以新的明确用户决定为优先；当前授权可关闭已交付裁决的普通设计分叉，但不能伪称旧用户已说过。记录覆盖的旧规则ID、理由、范围、被否决方案、架构影响、测试与重审触发。原source快照不改。历史DDD的OPEN只在当时成立，当前状态以决策登记的替代关系为准。

## 命名和唯一责任

文件用描述性English kebab-case，不在活跃路径放v1/final/new。文档稳定doc_id、职责、依赖、日期、stage放frontmatter，Git拥有版本历史。规则稳定ID只由一个责任文件定义；其他文件链接，不复制容易漂移的参数表。参数必须有单位、TEST标记、唯一Owner和测量方法；未测量但需要实现时选择有理由的初值，不丢给新手所有者。

所有活跃文档必须进入[完整登记](document-register.md)和适当阅读路径。新增系统包含目的、范围、玩家流、状态/所有权、成本提交、取消/并发/断线/恢复、接口、反馈、正常/失败例及验收。先证明薄的完整链，不能以更多接口替代玩法。

## 本次采纳的边界

自动迁移脚本逐个列出被采纳的行为规则，审计JSON记录其ID；没有把全部PROPOSED改CANON。角色/历史候选保留REVIEW，内容数值和用户研究假设保留TEST，Lab/Descent保留FUTURE边界。原文保留和新决定必须能由Git差异追溯。

## 完成检查与诚实

运行文档validator、自测和inventory；检查远端commit与CI。游戏测试另按验收矩阵，报告实际运行与未运行。不能声称已购资产、正式许可证清查、独立盲审、Steam认证、Deck达标或可玩构建，除非存在真实证据。交接必须有当前状态与下一个可执行任务，不依赖聊天记忆。
