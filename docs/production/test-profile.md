---
doc_id: PROD-TEST-PROFILE
doc_type: production
stage: BASELINE
updated: 2026-09-05
owner_role: 系统平衡与测试负责人
canon_basis: "SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION; DDD-0014; DDD-0016"
depends_on: ["../gdd/operations.md", "../content/blackstart.md", "acceptance-matrix.md"]
---

# 初始测试参数：可执行起点，不是假平衡定稿

除表中明确CANON的60Hz外，下列数值均为**TEST**，均未测量。用于结束“没有一个可实现起点”的状态；后续开发者可依据受控实验调整并更新本表，无需让不懂编程的所有者逐个选数字。武器/敌人单体卡已有的数值仍由各内容卡拥有，不在这里复制另一套。

| 参数ID / 用途 | 初始值 | 单位、边界和失败解释 |
|---|---|---|
| TP-TICK / Authority | 60 Hz · CANON | Gameplay/协议合同，不是普通服务器开关 |
| TP-REPLICATION / 重要状态 | 30 Hz | 非全部对象；AI按重要性降频，Dormant可0 |
| TP-REWIND / hitscan历史 | 200 ms | 只接受服务器估计范围；禁止客户端任意时间旅行 |
| TP-INPUT / 输入缓冲 | 100 ms | 仅在合法动作阶段消费一次；对各渲染FPS回归 |
| TP-RADIAL / 长按阈值 | 250 ms | 点按/长按不能同时触发；控制器实测可调 |
| TP-MOVE / 地面走/跑/蹲 | 5 / 7.5 / 2.5 m/s | 不设置耐力；跳高1.2m、mantle最高1.5m作为灰盒尺度测试 |
| TP-HEALTH / 原型生命 | 100 HP | 正式角色无固定数值强弱；HealthCap按合法效果变化 |
| TP-FLOOR / 脱战低保 | 当前合法HealthCap的20% | 连续10s无受伤且无被确认追击才缓慢回到该线；不是回满 |
| TP-REVIVE / 手动救援 | 3s，恢复40%合法HealthCap | 最后提交才完成；移动/受击按动作合同中断，无半份资源复制 |
| TP-GRACE / 起身保护 | 最多2s，主动攻击立即结束 | 防动画秒倒，不保护主动无代价开火 |
| TP-BLEED / 倒地 | 45s | SimulationTime；搬运时以0.5倍消耗，不可无限暂停；全倒合法恢复候选继续按生命合同处理 |
| TP-LAST-WIND / 自救贡献 | 对本次有效威胁累计≥20%伤害且其死亡在贡献后10s内 | 去重EnemyID与lifeEpoch，接受队友补刀；必须是有真实战斗能力的合法敌人，不是生成靶/自造单位；原型先不增加永久次数税 |
| TP-METER / Support | threshold100；普通包1Charge | 主线BLACKSTART贡献240、Vault100由关卡卡拥有；无稳定击杀贡献 |
| TP-AMMO-POD / 弹药包 | 每个合资格Seat一份40%当前合法reserve上限的弹族补给 | 转成有限实体单位；不补重资产；超出容量留可分配bundle，不直接溢出消失 |
| TP-MED-POD / 医療包 | 四份各恢复40HP的医疗，Solo按同包规则允许携带/分配 | 这是包内容而非自动治疗；不等于Revive；资源密度需按人数再测 |
| TP-DRAFT / 首轮等待 | 20s | 断线暂保留；明确离队Pass；新Seat无追溯资格 |
| TP-MODS / 标准长局改装机会 | 2保证+1可选 / 玩家 | 两把枪各2挂点（handling、behavior），工具1挂点，队伍1协议位；同位替换不无限叠加 |
| TP-INSTALL / 改装 | 3s在合法维护点安装 | 未提交取消不消耗；换下实例留世界；信息预览不冻结模拟 |
| TP-OFFER / 任务板 | 6个Offer | 合同结束/回Hub生成新批；出发前可手动整批刷新，无费用/每日限制；锁Run后不重掷 |
| TP-DIFFICULTY / 外观奖励倍率 | Relaxed1.0、Standard1.0、Veteran1.2、Nightmare1.4、Cataclysm1.6 | 仅成功完成奖励/允许外观收益，不改变关键知识或掉落事实；不得变唯一刷钱答案 |
| TP-UPLOAD / 知识上传 | 3s；标准长局至少中段和撤离前两处合法点 | 重试幂等，失败只保留已banked；短灰盒至少一处 |
| TP-WIPE / 未撤离废料信用 | 0% | 银行知识保留100%；无完成bonus；取消旧“失败代币50%”试验，避免凭空出售没带回的废料 |
| TP-CHECKPOINT / 恢复点 | 1s一份逻辑全快照 | 完整认证点RPO目标≤1s；超过2s未认证停止继续积累；不是60Hz云写入 |
| TP-LEASE / 续约 | TTL4s；1s heartbeat；0.5s保守余量 | 客户端单调时钟、睡眠检测及协调器持久化共同测试 |
| TP-LIMITS / 不可信包输入 | manifest1MiB；单文件512MiB；单包展开2GiB；JSON深度32 | 初始拒绝服务防线；压缩比/纹理GPU内存另外校验；不是保证机器一定有足够内存 |
| TP-REPLAY / 位置采样 | 玩家5Hz，非玩家仅关键实体1Hz | 重要语义事件完整记录；只降非玩法表现采样，具体磁盘/CPU预算仍归TRP-006 |

## 操作取消优先级

死亡/不可行动状态先于新攻击；已经提交的弹药移动和射出结果不回滚。换弹定义RemoveMagazine、InsertMagazine、Chamber、Ready独立提交边界；枪型可无对应阶段，但必须声明。未插入新匣就取消不能获得新弹；插匣完成后取消不能再扣第二匣。切枪、ADS、Fire可以排队到最近合法窗口，不能穿过声明的不可取消安全阶段。损失反映实际已执行动作，不以动画播完与否猜账。

## 这些数字怎样改变

同seed/武器/人数先比较一个参数，再扩到三种情境和两种输入；记录原因、结果及风险。重要世界资源或任务总量仍由关卡预算卡拥有。重试、迁移、多人并发的守恒测试每次都跑；新数字不得放宽其正确性要求。
