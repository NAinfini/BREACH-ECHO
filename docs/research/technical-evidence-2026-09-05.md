---
doc_id: RESEARCH-TECH-20260905
doc_type: research
stage: BASELINE
updated: 2026-09-05
owner_role: 技术研究与证据维护
canon_basis: "Primary vendor documentation checked 2026-09-05; DDD-0015; DDD-0016; DDD-0017"
depends_on: ["../technical/technology-stack.md"]
---

# 技术选择证据与核验限制 · 2026-09-05

以下是外部能力和限制，不证明BREACH已集成成功。决策理由是本项目判断；兼容性、成本、玩法与性能必须另测。网页可能更新，正式锁版本/购买/部署时重新核验并保存许可证和版本证据。

| ID | 官方来源 | 本次可支持的事实与设计影响 |
|---|---|---|
| E-UNITY | [Unity 6 support](https://unity.com/releases/unity-6/support) | 6.3 LTS支持窗口至2027年12月；6.0窗口较早结束。选6.3 LTS是项目稳定性取舍，不能声称补丁/全部包兼容已经验证 |
| E-FISHNET | [FishNet networking models](https://fish-networking.gitbook.io/docs/guides/high-level-overview/networking-models) | 文档明确Host Migration不内建；必须建设BREACH恢复协议。页面以搜索可见正文核验，不能将其当本地库测试 |
| E-TRANSPORT | [FishySteamworks](https://fish-networking.gitbook.io/docs/fishnet-building-blocks/transports/fishysteamworks)、[维护方仓库](https://github.com/FirstGearGames/FishySteamworks) | Steam传输适配存在；具体FishNet/Steamworks.NET组合、依赖许可证及真实Steam账号测试仍是M0工作 |
| E-ROLLBACK | [ColliderRollback](https://fish-networking.gitbook.io/docs/fishnet-building-blocks/components/colliderrollback) | 官方将组件列为Pro；不把收费功能写成已拥有的免费能力。选择范围受限的项目命中体历史 |
| E-STEAM-NET | [Steam networking](https://partner.steamgames.com/doc/features/multiplayer/networking) | 新API支持Valve中继；旧ISteamNetworking已弃用。适配器负责具体认证/消息语义，不由品牌名自动保证迁移 |
| E-LOBBY | [ISteamMatchmaking](https://partner.steamgames.com/doc/api/isteammatchmaking) | Lobby owner离开会转移；该API不承诺BREACH世界状态、租约或Exactly-once资源事务 |
| E-AUTH | [Steam authentication](https://partner.steamgames.com/doc/features/auth) | 提供客户端/服务端身份和所有权认证流程；服务密钥不放客户端。票据验证与应用权限必须用测试账号实现验证 |
| E-WORKSHOP | [Workshop item versioning](https://partner.steamgames.com/doc/features/workshop/itemversioning) | 支持创作者按游戏branch维护兼容版本，涉及SDK/发布配置；不等于每个任意历史hash可永久获得。因此选精确hash缓存+缺失明确拒绝 |
| E-DO | [What are Durable Objects](https://developers.cloudflare.com/durable-objects/concepts/what-are-durable-objects/) | 唯一对象标识、持久强一致事务存储适合小型Run协调器。应用的租约/认证/重放防护仍须实现，不自动构成协议正确性证明 |
| E-DO-COST | [Durable Objects pricing](https://developers.cloudflare.com/durable-objects/platform/pricing/) | 计算与存储均可能计费，Free超限会失败；持续活动、请求、存储写入须建模。没有“无限免费在线”承诺；部署和预算待所有者授权 |
| E-ASSETS | [Unity Asset Store terms](https://unity.com/legal/as-terms) | 采购需核验实际条款/附加条款；不得假设可把原资产再分发到公开repo、Workshop或SDK示例。本文不是个案法律清查 |
| E-MIXAMO | [Adobe Mixamo FAQ](https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html) | 官方说明可用于包括游戏在内的项目；自动骨骼目标为双足人形。具体第三方模型权利和原文件再分发不可从此推导 |
| E-MESHY | [Meshy Rigging API](https://docs.meshy.ai/en/api/rigging)、[Image-to-3D API](https://docs.meshy.ai/en/api/image-to-3d) | API骨骼文档限制人形双足等输入条件；营销页面更宽泛的非人形能力不作为生产API保证。生成后仍需Blender拓扑、权重、碰撞、URP与许可验收 |

## 结论的边界

没有安装或购买FishNet Pro、Meshy付费方案、模型包、Unity额外许可证或在线服务。没有实际Steam四人连机、Cloudflare部署、资产导入、IL2CPP编译、Deck测试或安全审计。SDK/Editor精确补丁、第三方许可证hash与实测网络指标由M0/M3证据填写，不由本文猜测。

## 成本建模而不是报价承诺

协调器用`online_run_hours × messages_per_second × 3600`估计消息数，按实际HTTP/WebSocket计量区别换算；另计活跃duration、SQLite读写/存储、入口Worker、日志、税和汇率。租约与checkpoint ACK不得误估为每玩家零成本。部署前用1/10/100并发Run场景估算并压测限额，给出停止新会话的预算保护及现有会话安全挂起策略；不是现在授权支付。
