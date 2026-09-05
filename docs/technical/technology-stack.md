---
doc_id: TECH-STACK
doc_type: technical
stage: BASELINE
updated: 2026-09-05
owner_role: 技术负责人
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; DDD-0015"
depends_on: ["architecture-and-performance.md", "host-migration.md", "../research/technical-evidence-2026-09-05.md"]
---

# 选定技术栈与安装验收

## 结论与适用范围

STACK-001 · DECIDED · delegated。以下是实现选择，不是已安装、兼容性已验证或性能已通过的声明。版本在M0做一次真实构建后写入ProjectVersion、manifest、packages-lock及第三方依赖登记，禁止使用浮动Git分支或把“最新”写进可复现构建命令。当前仓库没有Unity工程。

| 层 | 唯一选定实现 | 不采用的平行方案 / 理由 |
|---|---|---|
| 引擎 | Unity 6.3 LTS，固定验证后的补丁版本 | 不重做UE比较，不同时维护多个Editor |
| 渲染与常规玩法 | URP；C#、GameObject/MonoBehaviour；CPU热路径按Profiler决定Jobs/Burst | 不预先全DOTS化，不建HDRP资产分支 |
| Unity网络框架 | FishNet，Steam路径使用FishySteamworks和Steamworks.NET；Tugboat仅本机/LAN开发测试 | 不并行建设NGO、Mirror、Photon Fusion、EOS，避免多套连接/预测/对象生命周期 |
| Steam平台 | Steam Lobbies、Steam身份/邀请、SteamNetworkingSockets/SDR、ISteamUGC | 不用旧ISteamNetworking；不将Steam标识写进玩法schema |
| 在线权威协调 | 小型TypeScript Worker + 每Run一个SQLite-backed Durable Object | 不承载60 Hz模拟、完整世界、聊天历史或账号经济；不是官方游戏模拟服务器 |
| 输入 | Unity Input System产生语义命令；Steam Input只做设备映射 | 禁止Input System和Steam同时重复触发一次动作 |
| 运行时UI | uGUI + TextMeshPro；统一焦点导航和本地化键值 | 不同时维护两套运行时UI框架；UI Toolkit限Editor工具 |
| 摄像机 | Cinemachine辅助FPS/TPS表现，弹道仍由Authority控制 | 摄像机射线不能成为另一套伤害事实 |
| 动画 | Animator + Animation Rigging；角色Humanoid，非人敌人Generic自定义骨架 | 不把任意怪物强套人形自动骨骼 |
| 导航 | Unity AI Navigation，模块内烘焙NavMesh、门与连接点显式链接；运行时校验可达 | 先不开发全新导航引擎；必要时对高数量敌人作分层调度 |
| 内容与加载 | UTF-8 JSON定义、版本化Registry、Addressables/AssetBundle表现引用；本地UPM代码包 | 不反射执行包内任意C#；不能把Unity场景或ScriptableObject引用当存档身份 |
| 存档/快照 | 明确定义的版本化二进制DTO；JSON诊断导出仅开发工具；长度、范围和checksum验证 | 不用BinaryFormatter/任意多态类型反序列化，不保存Unity对象图 |
| 音频 | Unity AudioMixer + 项目自己的有限声部/优先级路由；Steam Voice只作在线语音采集压缩 | 首发不依赖FMOD/Wwise付费中间件；不录玩家语音进回放 |
| 测试与构建 | Unity Test Framework、命令行批处理、GitHub Actions文档检查；游戏构建由有合法Unity环境的受控runner执行 | 不假设托管runner已有Unity许可证；不提交密钥或有再分发限制的资源 |
| 资产加工 | Blender受支持LTS、FBX/纹理导出、URP导入检查 | AI生成只作为可选来源，不跳过拓扑、碰撞、骨架、许可验收 |

技术事实及核验限制见[证据登记](../research/technical-evidence-2026-09-05.md)。Unity的6.3 LTS选择是本项目稳定性判断，不是声称所有新项目必须用LTS。

## 网络边界

STACK-002 · DECIDED。

FishNet负责连接生命周期、受控对象生成、消息传输和可复用预测基础设施。BREACH拥有GameplayCommand、事务顺序、稳定Entity/Part ID、Interest规则、包锁、恢复schema及Host Migration。不要创建与FishNet争夺同一Transform的第二套同步组件；每个组件只能有一个权威写入路径。项目网络适配程序集可引用FishNet；Kernel和规则包不能。

FishNet当前没有内建Host Migration；它的ColliderRollback文档也将该组件列为Pro功能。首发选择自有、范围受限的命中体历史，而不是假装买到了付费回滚插件。先证明命中和迁移，再扩大对象量。技术Spike失败时在相同合同下更换适配实现并写新DDD；不因一个例子连上网就宣布全部满足。

## 服务器回溯命中

STACK-003 · DECIDED；时间值TEST，归测试参数。

仅对经验证的hitscan请求进行有限历史命中体查询。Authority保存稳定EntityID/PartID、碰撞代理形状、位置、姿态及门/可破坏遮挡的相关历史；客户端发送输入序号和经服务器时钟估计限制的射击时间，不发送可信的命中结果。最大回看初值200 ms，未来时间、过旧请求、非法射速/弹药/姿态均拒绝或按明确当前时刻规则处理并计数。

采用独立查询数据/物理场景，不倒转正在运行的世界、AI或存档。历史查询结果只产生候选命中；伤害在当前权威tick提交，已销毁或generation不符的目标不被“复活”。历史遮挡和现时不可穿越边界都必须满足防穿门规则；宁可明确失配为未命中，也不让客户端历史时间绕过现时实心墙。此规则需在关门边缘测试公平性。投射物由Authority spawn并连续sweep/CCD，首版不进行整世界历史弹道重演；本地弹丸仅预测表现。

## 本机、离线、在线

STACK-004 · DECIDED。

离线Solo不启动Steam匹配和云协调器，不请求账号秘密，不要求在线校验已经合法安装的本地内容。在线多人用Steam认证绑定本次连接，再由协调器发会话/epoch授权；Steam Lobby owner、PartyLeader、HubOwner、SimulationHost是不同概念。Steam不可用时显示在线服务不可用，允许进入合法离线Solo；不让在线Run在分区时无提示分叉为多个离线Run。

协调服务只有建立会话、成员更新、恢复证书和租约接口；认证使用服务端验证的Steam Web API票据，服务密钥保存在服务器秘密配置。客户端不是可信计费/会员/进度数据库。部署需要OWNER-02预算和账户批准；M0–M2用接口兼容的本地协调器测试替身。

## M0必须交付的版本证据

记录Editor补丁、URP/Input/Cinemachine/Animation Rigging/AI Navigation/Addressables/Test Framework版本、FishNet/FishySteamworks/Steamworks.NET commit及许可证文件hash、Scripting Backend、目标架构、API兼容级别、构建命令、两台机器的联机结果。至少Windows x64开发构建与一次非Editor运行；Steam路径须用合法测试账号/应用条件验证，不承诺同一Steam账号能模拟四台客户端。

编译错误、许可证缺失或传输不兼容属于M0失败；不能把未验证版本标为已锁定。安全补丁升级可以重新做兼容矩阵，不以“无旧代码”删除已发布玩家进度。
