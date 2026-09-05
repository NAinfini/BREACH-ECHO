---
doc_id: TECH-MOD-SECURITY
doc_type: technical
stage: BASELINE
updated: 2026-09-05
owner_role: Mod Runtime与安全负责人
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; DDD-0017; DDD-0009"
depends_on: ["modding-and-toolchain.md", "data-contracts.md", "../gdd/mod-manager.md"]
---

# Mod信任边界、包固定与自动同步

## 首版能力决策

MODSEC-001 · DECIDED。官方公开Mod首版仅支持经过schema验证的Data与有界声明式Graph，以及由受支持构建管线产出的表现资源。**不支持Lua/JavaScript/C#脚本、Native DLL、任意WASM或系统命令自动执行**。这是明确的语言/沙箱决策，不是“以后再问用哪种语言”。更强脚本与TC能力在未来API版本另做威胁建模、资源约束和独立审查，不成为首发依赖。

Graph不是安全的魔法标签。只允许固定节点、有限常量/集合、声明读写能力、显式事件入口、受限迭代；禁止递归、无时间推进环、动态类型加载、文件/网络/进程/反射/账号写入。编译时验证边界和成本；运行时按包记账。超出预算拒绝激活或明确终止受影响会话，不能静默丢弃合法Gameplay结果。官方内容也通过同一Registry和规则验证，但引擎内部受审代码不作为可下载Mod能力暴露。

## 包结构与信任

MODSEC-002 · DECIDED。

PackageManifest必须包含`package_id, semantic_version, schema_version, sdk_version_range, kind, dependencies, conflicts, content_index, capabilities, distribution_locator, license/provenance`。每个文件记录规范化相对路径、byte size、SHA-256。计算包锁digest时按路径字节序排序，以明确长度前缀串联manifest原始规范发布字节与各路径/文件hash；发布后manifest不得在原hash下修改。构建器输出同一输入得到同一内容索引；平台压缩容器自身字节差异不冒充逻辑内容一致。

`breach.official`命名空间只由本地受信任发布登记/签名认可，不能仅凭字符串自称官方。Hash提供内容身份而非安全背书；publisher签名也不能代替沙箱校验。AssetBundle不是任意文件的安全沙箱：只接受支持版本、目标平台、允许资产类别与Shader策略，限制资源数量/展开大小；拒绝未审组件序列化、未知插件和外部文件引用。URP自定义Shader及复杂表现的公开能力先限制到SDK允许集合，避免GPU/加载型拒绝服务。

## 加入与激活状态机

MODSEC-003 · DECIDED。

`Discover → CompareLock → ConsentPolicy → Download → Validate → Stage → Activate → Handshake → Ready`。Host发布玩法包精确依赖图与hash；客户端验证分发地址仅为许可的Steam Workshop locator或本地已验证缓存，不能跟随Host指定任意HTTP地址。自动同步操作是一次整合流程，不要求用户逐个找Mod；首次外部内容需说明总大小、来源和支持的能力。玩家可取消，取消保持当前profile不半激活。

下载由ISteamUGC完成；Loader验证完整依赖拓扑，确定同层排序，不允许重复覆盖定义、循环依赖、隐藏能力升级、presentation标签夹带玩法修改。验证成功后复制/建立应用管理的不可变hash缓存，再一次切换profile；Steam更新安装目录不能直接改写正在进行的Run。失败返回明确错误码和修复操作，不清空用户订阅或覆盖旧hash。

## 旧版本、缺包和授权

MODSEC-004 · DECIDED。

Steam Workshop已有分支兼容版本能力；官方发布在升级游戏branch前先准备兼容mod版本和回归矩阵。它不能被解释为“任意历史hash永远可重新下载”。活跃/挂起Run固定精确hash，保留正在使用的完整本地缓存；磁盘清理不能删除被引用包。已安装且许可允许的旧内容可继续本地使用，但不绕过撤销授权、平台限制或删除要求。

新加入者无法取得Host需要的旧hash时**拒绝本次加入**，显示缺失包、所需版本/hash、现有版本以及“等待提供者恢复正确版本 / 返回 / 新建使用一致新版本的Run”。不静默升级旧Run、不伪造兼容、不通过Host直传第三方资产、不自建镜像规避许可。整局玩家明确选择新版本时也应创建新Run或经过专门验证的显式迁移，不能因某人点更新就改变他人当前Run。

## 存储、撤回和排错

MODSEC-005 · DECIDED。

Profile记录启用包集合、加载顺序和玩法锁，订阅列表不是实际激活状态。共享缓存用引用计数和磁盘预算；GC仅回收无活跃/挂起Run引用的artifact，执行前展示空间和影响。导出诊断仅含包IDs/hash、错误码、游戏/SDK版本和脱敏日志，不导出第三方内容、账号票据或个人聊天。退订与停用不同；卸载需要用户明确操作，不能加入好友房就改变其长期偏好。

多人安全验收覆盖Zip Slip、symlink、zip bomb、超深JSON、重复ID、hash篡改、Graph无限环、恶意能力声明、未知DLL、非法Shader、大纹理内存、磁盘满、断下载、Steam更新竞态、被删除旧版本。独立安全审查和真实恶意包测试仍未运行；文档不保证能防住所有恶意创作者。
