---
doc_id: GDD-FRONTEND-FLOW
doc_type: gdd
stage: BASELINE
updated: 2026-09-05
owner_role: 前端与会话体验设计
canon_basis: "当前Steam-only、Operation、Mod Manager与game-ui-ux基线"
depends_on: ["operation-game-mode.md", "coop-and-social.md", "ux-and-accessibility.md", "mod-manager.md"]
---

# 前端、房间与会话状态流

## 玩家目的与单一责任

UIFLOW-001 · DECIDED。

玩家从启动到开始行动、处理中断并返回壁垒的路径必须可预测、可返回、可用控制器完成。本文拥有页面层级、会话状态和错误恢复；具体HUD信息归[UX](ux-and-accessibility.md)，匹配规则归[合作与社交](coop-and-social.md)，Mod包流程归[Mod Manager](mod-manager.md)，网络真相归[网络与持久化](../technical/network-and-persistence.md)。

## 顶层状态机

UIFLOW-002 · DECIDED。

顶层页面顺序固定为：`Boot → LegalAndSafety → ProfileLoad → ServiceCheck → Title → BastionHub → MissionBoard → Loadout → Lobby → ReadyCheck → Loading → Operation → Debrief → ReplayOptional → BastionHub`。

离线Solo在`ServiceCheck`后进入`OfflineProfile`，不创建Steam Lobby。在线服务不可用时给出“重试 / 查看状态 / 离线Solo / 退出”，不能无限转圈。活动Run存在可恢复证书时，在Title显示“恢复行动”，并在覆盖本地较新或较旧状态前展示Run、时间、成员、包锁和恢复水位。

界面采用单一`ScreenStack`：基础屏幕占底层，设置、确认、错误、邀请、文本输入和下载进度是Modal；只有栈顶接收UI输入。在线Operation打开暂停菜单不会暂停模拟，离线Solo才允许暂停SimulationTime。返回动作关闭最上层，不能从深层设置直接误退整局。

## 页面清单与完成条件

UIFLOW-003 · DECIDED。

| 页面 | 必须显示/允许 | 离开条件 |
|---|---|---|
| Title | 继续、进入壁垒、训练、Mods、设置、制作人员、退出；服务/版本状态 | Profile合法或明确错误 |
| BastionHub | 小队、任务板、配装、Archive、训练、Mods入口；不做50人社交Hub | 选择一个明确目的 |
| MissionBoard | 6个Offer、区域/设施、主/支线、警告、奖励、长度、难度 | 锁定Offer与MissionSeed |
| Loadout | 角色Seat、两枪/工具/模块、冲突、资源与详情比较 | 每名真人配装合法 |
| Lobby | 隐私、成员、语音/静音、Ping、包锁、准备、邀请/踢出权限 | 全部真人Ready且依赖齐全 |
| Loading | 阶段、成员与包状态、取消规则、错误归属 | 全员进入或明确恢复/失败 |
| Operation HUD/Pause | 当前任务、队友、资源、Ping、设置、离队/恢复说明 | 权威结果或明确离开 |
| Debrief | 团队结果、个人/团队详细统计、关键因果、奖励领取 | 玩家确认返回或打开回放 |
| Replay | 简化地图、时间轴、事件筛选、播放速度 | 返回Debrief，不改变奖励 |
| Settings | 显示/性能、音频、控制、可访问性、语言、网络/隐私 | Apply成功或放弃未提交改动 |

Archive、训练和Mod Manager是独立基础屏幕，可从Title或Hub进入；离开后返回原入口。制作人员、许可、隐私告知和第三方声明在发行前必须可离线打开。

## 会话创建与加入

UIFLOW-004 · DECIDED。

创建流程为选择Solo/好友/私密/公开→创建Session→选任务→锁Mission→配装/Seat→包锁验证→Ready。加入流程为Steam邀请/好友/公开搜索→显示地区、延迟估计、任务阶段、难度、人数、是否Modded及下载量→确认→身份/版本/包锁验证→下载与Staging→分配Seat→进入Lobby或中途加入快照。

匹配筛选首发只提供地区/延迟、难度、任务长度、语音偏好、Modded/Vanilla和空位；不建立隐藏技术评分或战力分数。搜索无结果时提供扩大地区、放宽筛选、创建公开房和返回，不自动改变玩家选择。中途加入前明确任务已进行时间、回放前段缺失、当前配装限制及奖励资格。

## Ready、倒计时与取消

UIFLOW-005 · DECIDED。

任何Mission、Difficulty、Ruleset、Package Lock、Seat或Loadout变化都会使受影响玩家退出Ready并说明原因。房主不能在倒计时最后一秒静默换难度或包。启动倒计时只是UI阶段，最终开始由Authority在全员合法后提交唯一`RunStartTransaction`；重复消息不创建第二个Run。

下载、构建包验证或服务请求可以取消，取消不得半激活Profile。已经进入Operation后，离队确认必须说明Seat保留时间、队伍影响和本地临时回放处理。Host离开优先进入迁移界面；只有恢复被判定不可能时才显示挂起/结束选项。

## UI数据与所有权

UIFLOW-006 · DECIDED。

UI读取只读`ViewModel`，通过语义Command请求变化，不直接写Simulation、库存、Ready或包状态。每个异步操作包含`OperationID`、当前阶段、可取消性、进度单位、超时责任与结构化错误码；旧响应因页面重开或revision变化到达时丢弃，不覆盖新状态。

设置采用`Draft → Validate → PreviewOptional → Commit → Applied`。显示模式等可能导致黑屏的设置使用15秒回退确认；重绑定发现冲突时必须选择替换、互换或取消。语言、字幕、文字大小和降低动态效果可在Operation中修改并立即作用于表现，不改变权威玩法。

## 响应式、控制器与本地化

UIFLOW-007 · DECIDED。

uGUI使用CanvasScaler参考1920×1080、锚点与Layout Group，不用单分辨率绝对定位。关键HUD和按钮遵守安全区；16:10 Steam Deck、16:9、21:9和32:9采用扩展画布并保持关键内容在可读列宽。每页打开时有明确初始焦点、可见且不只靠颜色的焦点态、显式邻接与Modal焦点陷阱。键鼠与控制器可随时切换，不清空焦点或重复提交。

全部文本使用本地化键和内容自适应容器；中文、英文至少用最长实际字符串做伪本地化压力测试。图标与文字分离，错误不能只给代码；代码可作为诊断详情复制。

## 错误与恢复矩阵

UIFLOW-008 · DECIDED。

| 失败 | 必须解释 | 合法下一步 |
|---|---|---|
| Steam离线/认证失效 | 哪项在线能力不可用，本地档案是否安全 | 重试、离线Solo、返回 |
| Build/Protocol不一致 | 本机与房间版本 | 更新、返回；不硬读 |
| Mod缺失/旧hash不可得 | 包、版本、hash、来源和下载状态 | 重试、等待作者恢复、创建一致新Run、返回 |
| Lobby满/Seat冲突 | 变化后的成员与可用Seat | 选其他Seat、重新搜索 |
| Host迁移 | 冻结原因、认证恢复点和预计阶段 | 等待、挂起或在明确失败后离开 |
| 存档冲突 | 两份时间、进度摘要和设备 | 明确选一份，不合并资源 |
| 生成失败 | Offer或内容包无法产生合法任务 | 标记内容错误并换Offer；不把坏Seed交玩家 |

## 验收与未证明项

UIFLOW-009 · TEST。

8名新玩家以键鼠和控制器完成：离线Solo、好友创建、公开搜索、一个缺Mod自动同步房、设置并撤销显示模式、任务选择/Ready、结算与回放返回；至少7人不需口头指导，零半激活包、零误退Run、零无焦点死页。覆盖720p、1080p、1440p、4K、16:10、21:9、32:9、200%文字与伪本地化。所有结果当前为NOT RUN。
