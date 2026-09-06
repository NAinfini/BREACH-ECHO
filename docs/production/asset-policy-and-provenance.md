---
doc_id: PROD-ASSET-POLICY
doc_type: production
stage: BASELINE
updated: 2026-09-05
owner_role: 制作与资产合规负责人
canon_basis: "SRC-SSOT-2.0 §26–§28；SRC-USER-2026-09-05-OFFICIAL-CONTENT-PACKAGES；SRC-USER-2026-09-05-TECH-OPEN-BATCH-AND-LAG-COMP-GATE；SRC-USER-2026-09-05-ASSET-SOURCING-NO-QUOTA"
depends_on: ["../gdd/art-direction.md", "../technical/modding-and-toolchain.md"]
---

# 资产采购、来源与许可政策

## 目的与边界

本文件把“可以买什么、能放到哪里、证据怎么留、能否随SDK或Workshop再分发”变成单一责任。它不是法律意见，也不声称任何商店条款已经永久核准；正式采购、外包签约和发布前仍需核对当时有效的原始许可证与合同。

ASSET-001 · CANON WORKFLOW · 来源：现行[美术ART-006至ART-007](../gdd/art-direction.md)、SRC-USER-2026-09-05-TECH-OPEN-BATCH-AND-LAG-COMP-GATE与SRC-USER-2026-09-05-ASSET-SOURCING-NO-QUOTA。

生产不预设免费、购买、自制或AI资产占比。每个资产按`视觉与玩法适配→技术可修复性→许可与再分发边界→预计人工修整工时→Unity运行预算→总成本`单独裁决。默认先寻找真正优秀且许可兼容的免费候选；没有合格免费候选时，优先AI生成后人工修整；AI持续不过Gate、修整时间失控或付费候选显著降低总风险时，允许购买止损。免费不等于低成本，AI生成不等于可直接出货，购买也不等于自动统一风格。任何来源比例只作事后复盘，不作为KPI或内容配额。

外部基础资产更适合人类工业设施、管线、梯道、容器、普通机械、基础枪模、Humanoid动画和通用VFX；四名角色关键轮廓、核心武器外壳语言、虚空兽主体、筑路者结构与界桥需要更强原创控制。唯一 Visual DNA 已锁为“分层壁垒”的中等多边形风格化工业科幻；Visual Production Gate 通过前仍只做少量代表性搜索、生成、采购和试装，不批量锁死资产库。

ASSET-002 · CANON · 来源：SRC-USER-2026-09-05-OFFICIAL-CONTENT-PACKAGES。

购买或获准在游戏中使用资产，不自动包含把raw source交给Mod作者、放入SDK、通过Workshop分发、交给外包方、用于营销素材或作为可提取源文件发布的权利。必须分别判断五种使用面：团队源文件、Cooked Runtime、SDK/Sample、Workshop/UGC依赖、Marketing。没有明确许可的使用面默认不得发布，不用“我们买过”替代条款证据。

ASSET-003 · DIRECTION · 来源：现行AI-agent-first与Modding生产规则。

自制、购买、外包、扫描、程序生成与AI辅助资产走同一条可追踪流程：Candidate→来源登记→隔离导入→许可/技术检查→改造与衍生链→Cook/Package→发布前复核。AI生成不等于无来源要求；应记录生成工具、日期、输入资产/参考来源、人工修改与适用服务条款。

## 来源登记

ASSET-004 · PROPOSED · 来源：本轮流程收敛。

正式登记应是可由Validator读取的机器数据；本文只定义字段，不维护第二份易过期的手工资产清单。每条记录至少包含：

- 稳定Asset ID、内容hash、包/版本、当前状态；
- 来源类型、供应商/作者、原始URL或合同号、取得日期与购买凭证位置；
- 许可证名称、原文/快照位置、适用版本、限制与不确定点；
- Team Source / Cooked Runtime / SDK / Workshop / Marketing五项允许矩阵；
- 修改记录、衍生Asset ID、上游依赖与可替换来源；
- 署名、notice、地域/期限/seat、AI或外包声明要求；
- 审核人、审核日期、下次复核Gate与最终Build/Package去向。

许可证文本、发票或合同可能含个人/商业敏感信息；公开仓库只保存必要的登记字段与受控证据引用，不把私人凭据直接提交进ContentPackage。

ASSET-005 · PROPOSED · 来源：本轮流程收敛。

资产生命周期候选为：`Candidate`、`Quarantined`、`Cleared-Internal`、`Cleared-Runtime`、`Cleared-Redistribution`、`Restricted`。状态必须表达允许范围，不能只有一个模糊的“Approved”。来源不明、证据丢失、条款冲突或供应商下架的资产进入Restricted/Quarantined，不得靠构建脚本静默继续发布。

## 验证与待决

ASSET-006 · TEST · 来源：本轮流程收敛；SRC-USER-2026-09-05-ASSET-SOURCING-NO-QUOTA修正。

进入批量正式资产生产前，用至少三类代表资产跑通全链：一个免费或付费的第三方3D/材质资产、一个具有不同许可条件的音频或动画资产、一个自制或AI辅助资产。没有合格付费候选时，不得为了凑来源比例而购买。验证登记可追到原始证据；Unity导入与Cook产物能反查Asset ID；Runtime包不泄露禁止再分发的raw source；SDK/Workshop样例只引用已获对应权限的内容；CI/Validator能阻止Restricted资产进入错误发布面。

ASSET-007 · DECIDED · 来源：本轮文档收敛。

Registry 使用版本化 JSON 和 schema，在 Unity 项目初始化时落位于 `config/assets/asset-registry.json`；公开登记只存脱敏元数据和 Evidence ID，发票、合同和完整条款快照放在受控私有存档。标准许可优先记录 SPDX 标识；商业或定制条款使用本地 Policy ID 并绑定快照。每个可独立替换或发布的 Runtime 资产必须有自己的 Asset ID，衍生关系以有向上游链记录。

Schema、hash、状态迁移、禁止发布面和构建路由自动检查执行；条款解释、AI/外包披露、例外和最终发布签署必须人工复核。Workshop 包只能重分发明确授权的内容；否则通过 Steam 依赖项引用用户合法获得的包，不复制原资产。证据的法定保存期、实际签署人和发布时披露文字取决于当时法域、平台和合同，必须在付费或发布 Gate 中核对，不伪装成可由 GDD 永久决定的法律事实。
