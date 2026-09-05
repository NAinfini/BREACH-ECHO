#!/usr/bin/env python3
"""One-time, source-preserving documentation migration. Not a game implementation.
Run only on the documentation-finalization branch. Subsequent maintenance uses
normal document edits and tools/validate_docs.py, not this historical migration.
"""
from __future__ import annotations
import hashlib
import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
D = ROOT / 'docs'
MARKER = D / 'governance/finalization-baseline.json'
SOURCE = 'SRC-USER-2026-09-05-DELEGATED-DOCUMENT-FINALIZATION'
PROTECTED = {
 'docs/sources/ssot-v2.0-original.md': '99721139befb62405c5b83067463161c9a9817435730d7ad72dddd2015accf0c',
 'docs/sources/chatgpt-brutal-review-v1.0.md': '1fd4d10f8f22b2ce0263e26edcba0eb85e554eabd43aec907fa603ff68b87c16',
}
RENAMES = {
 'gdd/build-algebra.md': 'gdd/modifications-and-effects.md',
 'content/relics-and-fusions.md': 'content/modification-catalog.md',
 'content/character-roster-v1.md': 'content/characters.md',
 'production/brutal-review.md': 'production/risk-register.md',
 'governance/decisions-and-questions.md': 'governance/decision-register.md',
}
CHANGES: list[dict] = []

def read(path: str) -> str:
 return (D/path).read_text(encoding='utf-8')

def put(path: str, text: str) -> None:
 p=D/path; p.parent.mkdir(parents=True, exist_ok=True)
 p.write_text(text.rstrip()+'\n', encoding='utf-8')

def document(path: str, doc_id: str, kind: str, title: str, body: str, stage: str='BASELINE', deps: list[str]|None=None) -> None:
 put(path, f'---\ndoc_id: {doc_id}\ndoc_type: {kind}\nstage: {stage}\nupdated: 2026-09-05\nowner_role: BREACH ECHO documentation stewardship\ncanon_basis: "{SOURCE}; delegated decisions DDD-0013–0018"\ndepends_on: {json.dumps(deps or [], ensure_ascii=False)}\n---\n\n# {title}\n\n{body}')

def rule(path: str, ident: str, body: str, status: str='DECIDED') -> None:
 text=read(path)
 pat=rf'(?ms)^{re.escape(ident)} · [^\n]*\n.*?(?=^[A-Z][A-Z0-9-]+ · |^#{{1,6}} |\Z)'
 replacement=f'{ident} · {status} · 来源：{SOURCE}；DDD-0013–0018；原规则历史保留于Git。\n\n{body.strip()}\n\n'
 text,count=re.subn(pat,lambda m: replacement,text,count=1)
 if count != 1: raise RuntimeError(f'Missing or ambiguous rule: {path} {ident}')
 put(path,text); CHANGES.append({'path':path,'rule':ident,'status':status,'action':'replace responsibility rule'})

def replace(path: str, old: str, new: str, required: bool=True) -> None:
 text=read(path)
 if old not in text:
  if required: raise RuntimeError(f'Expected text absent: {path}: {old[:70]}')
  return
 put(path,text.replace(old,new))

def append(path: str, text: str) -> None:
 put(path,read(path)+'\n\n'+text)

def approve(path: str, ids: list[str]) -> None:
 text=read(path)
 for ident in ids:
  pat=rf'(?m)^{re.escape(ident)} · (?:PROPOSED|DIRECTION)(?:\s*) · ([^\n]*)'
  text,n=re.subn(pat,lambda m:f'{ident} · DECIDED · 来源：{SOURCE}；授予决策权后采纳行为合同，数值/效果仍须TEST；原依据：'+m.group(1),text,count=1)
  if n != 1: raise RuntimeError(f'Cannot adopt rule {path} {ident}')
  CHANGES.append({'path':path,'rule':ident,'status':'DECIDED','action':'adopt specified behavior, not claim measured tuning'})
 put(path,text)

def main() -> None:
 for path,digest in PROTECTED.items():
  if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest: raise RuntimeError('Historical source changed: '+path)
 if MARKER.exists():
  print('Historical finalization migration already completed; no changes made.'); return
 for old,new in RENAMES.items():
  if not (D/old).is_file() or (D/new).exists(): raise RuntimeError(f'Unexpected rename state: {old} -> {new}')

 # Preserve the old decision ledger with correctly relocated links.
 old=read('governance/decisions-and-questions.md')
 old=re.sub(r'(?m)^doc_id:.*$', 'doc_id: GOV-DECISIONS-HISTORY-20260905',old,count=1)
 old=re.sub(r'(?m)^stage:.*$', 'stage: ARCHIVE',old,count=1)
 old=re.sub(r'\]\((?![a-zA-Z]+:|#)([^)]+)\)',lambda m:'](../'+m.group(1)+')',old)
 old=old.replace('# 决策与未决问题','# 决策与未决问题（2026-09-05定稿前历史）',1)
 put('governance/history/decision-register-before-finalization-2026-09-05.md',old)
 for before,after in RENAMES.items(): (D/before).rename(D/after)
 for p in list(ROOT.rglob('*.md')):
  rel=p.relative_to(ROOT).as_posix()
  if rel in PROTECTED: continue
  text=p.read_text(encoding='utf-8').replace('\n doc_type:', '\ndoc_type:')
  for before,after in RENAMES.items(): text=text.replace(Path(before).name,Path(after).name)
  if text.startswith('---\n'):
   text=re.sub(r'(?m)^updated:.*$', 'updated: 2026-09-05',text,count=1)
   stage='BASELINE'
   if '/history/' in rel or p.name in ['discussion-log-2026-09-04.md','source-map.md']: stage='ARCHIVE'
   if p.name in ['characters.md','narrative-bible.md','story-overview.md']: stage='REVIEW'
   if p.name=='descent.md': stage='FUTURE'
   if '/templates/' in rel: stage='TEMPLATE'
   if '/decisions/DDD-000' in rel and int(p.name[4:8])<=7: stage='ARCHIVE'
   text=re.sub(r'(?m)^stage:.*$',f'stage: {stage}',text,count=1)
  p.write_text(text,encoding='utf-8')

 # Product, equipment and mode contradictions are replaced at their owners.
 rule('gdd/vision.md','VIS-001','唯一基础产品为1–4人合作PvE Operation：裸枪手感、有限资源、真实设施后果与合作执行。少量有边界的武器/工具改装增加情境解法。Descent保留为FUTURE扩展；共享内核不等于两套首发内容。完整范围由[首发合同](../production/release-scope.md)拥有。')
 rule('gdd/vision.md','VIS-002','Operation-only方向已在本次授权下裁决，普通技术选择不再等待所有者逐一批准。保留无改装对照实验用于验证增益；不是同时制作另一个可售产品。')
 rule('gdd/vision.md','VIS-003','选择Operation+有限Field Modification；拒绝对等双模式首发、无限Relic累积和Operation自动Fusion。模式规则共享可验证的命令/效果/事务，不共享所有奖励能力。公开扩展采用Data/有界Graph，完整编辑器/脚本/TC后置；具体权限见[模组安全](../technical/mod-security-and-sync.md)。')
 rule('gdd/vision.md','VIS-008','首发远程武器为传统动能、电磁实体弹与有限Energy Block枪械。Staff/Spell及独立主武器近战谱系只在Lab/未来候选，不进入Operation制作清单；Quick Melee保留。旧条件分叉已由授权裁决，不维护旧运行时兼容分支。')
 replace('gdd/vision.md','再决定属于1.0后期内容、扩展或DLC','再决定未来扩展的实际制作与商业形式')
 replace('gdd/vision.md','12 个月应砍什么、具体伤害机制、Severity、实验阈值与 30/90/180 天否决关卡','范围控制、具体伤害机制、Severity、实验阈值与按依赖排列的否决关卡')

 rule('gdd/player-and-input.md','PLY-001','官方Operation入场固定两把枪、一件Utility工具、一件自由选择的个人战术模块，另有Quick Melee、手电、Ping。四名固定角色同局不重复Seat、Run内不换身份；装备与战术模块可重复。人物只固定叙事/视听身份，不锁职业能力。武器与工具身份在Run中稳定，通过明确挂点改装而非彩色等级换枪；世界Team Ordnance独立，不是免费第三把随身枪。旧两Utility/人物专属Active/无限Relic配置退出Operation。')
 rule('gdd/player-and-input.md','PLY-002','保留手电、Sprint、Jump/Crouch/Slide/Mantle/Air Control与Quick Melee lunge，无全局体力税。Gun点R执行真实Reload/Cycle；只有实际具有上下文动作才长按R显示轮盘。Operation不显示Staff/Spell入口。移动、输入缓冲和取消初值见[测试参数](../production/test-profile.md)，阶段提交不随渲染FPS变化。')
 rule('gdd/player-and-input.md','PLY-003','键盘默认1/2切枪、3选择/使用工具、4个人战术模块，E交互、Q语义Ping、R换弹、F手电、V快速近战；所有键可重绑并进行冲突检查。控制器用两个武器切换、工具选择/使用与战术动作的独立语义映射，具体物理键在首个InputAction资产及图示中固定并测试。模块需新动作/战场解法/效果连接至少满足两项，不能成为主任务必带钥匙。')
 rule('gdd/player-and-input.md','PLY-005','选角色与两枪/一工具/一战术模块→查看资源成本→进入任务→实际遇到时学习工具、救援、支援和改装。改装显示收益、代价、冲突与拆出物去向；取消不消耗，原子提交后才改变装备。不教授首发不存在的法术轮盘或自动Fusion。')
 rule('gdd/player-and-input.md','PLY-007','动作语义由共享系统实现，资源与允许内容由规则集控制。Character卡不声明独占Signature；TacticalModule卡独立声明verb、目标、成本/冷却、动作阶段和禁止场景。工具与模块资源分账。序列化保存CharacterID和TacticalModuleID为两个字段，不保留绑定与自由选择两套逻辑。')
 rule('gdd/player-and-input.md','PLY-008','抢取世界物按首次合法事务提交，失败者不丢原物。死亡取消未提交切换，已发弹保留。拆下/dormant修改不监听新事件；轮盘目标失效时取消并解释，不能暗选另一个动作。重连以当前权威装备重建，不以客户端缓存覆盖；所有合法Seat组合均可完成主任务。')
 rule('gdd/player-and-input.md','PLY-009','正常：AR+Shotgun玩家用Foam延缓侧路，再用自由选Aegis掩护队友救援，各付工具/模块成本。失败：改装预览后目标revision已变，安装拒绝且不吞旧件。跨系统：两人同带Scan可刷新合法窗口，但不按人数线性乘算承伤。')
 rule('gdd/player-and-input.md','PLY-010','8名新手无口头指导完成移动、切两枪、用一工具/战术模块、Ping与Revive，目标每项≥7/8且零误扣关键资源。键鼠/控制器和不同FPS均测试；初值由测试参数拥有，未实测不称最终平衡。','TEST')
 rule('gdd/player-and-input.md','PLY-011','两枪一工具的最新意图与旧两Utility基线的冲突已关闭：采用两枪+一工具+一自由战术模块，理由和覆盖关系见DDD-0014。')
 rule('gdd/player-and-input.md','PLY-014','采用所有角色均可自由选择的个人战术模块；这是本次delegated决定，不冒充用户过去逐字确认。Character、选人UI、Loadout、存档和示例统一解绑；人物代号与人格仍由OWNER-01批准。')
 replace('gdd/player-and-input.md','移动、射击、近战、施法和救人；角色改变起点','移动、射击、快速近战、使用工具和救人；角色提供身份')
 replace('gdd/player-and-input.md','Weapon 是装备平台，Staff/Melee/Energy 均占正常武器位；Utility 是独立战术工具；Signature Active 是角色特征动作','Weapon是Operation枪械平台；Utility是独立工具；Tactical Module是自由选择的个人战术动作')
 replace('gdd/player-and-input.md','| 官方 Weapon / Utility / Signature | 2 / 2 / 1 · CANON | SRC-SSOT-2.0 §5.1、§40 |','| 官方 Weapon / Utility / Tactical Module | 2 / 1 / 1 · DECIDED | DDD-0014 |')
 replace('gdd/player-and-input.md','缓冲、移动、受击与换弹如何互相中断仍OPEN','缓冲、移动、受击与换弹按测试参数的动作提交/取消优先级实现')

 rule('gdd/operations.md','OPS-001','Run是一个连续Operation/Facility/Mission，无玩家可见Layers；资源、门、Cart、Knowledge、Support和Optional后果连续保留。Mission比改装更核心；采用有限Field Modification，不启用自动Fusion或无限Relic池。移除改装后的同任务对照仍应有趣。')
 rule('gdd/operations.md','OPS-003','唯一首发Operation；入场锁装备身份，局内以WeaponModule/ToolModule/TeamProtocol改变解法。标准长局初值每玩家2保证+1可选机会；安装预览后3s在合法维护点提交，同挂点替换、旧件留世界。原自动Fusion仅Lab/FUTURE，不能吞掉Operation配件。数量和挂点归[测试参数](../production/test-profile.md)，统一数学归[修改与效果](modifications-and-effects.md)。')
 replace('gdd/operations.md','具体倍率仍OPEN','具体初始外观奖励倍率见测试参数，核心知识和任务事实不受倍率改变')
 replace('gdd/operations.md','任务板Offer数量、刷新触发及是否允许手动刷新仍OPEN','任务板采用6个Offer，回Hub/完成合同刷新，出发前可免费手动整批刷新；锁定Run后不可重掷，初值见测试参数')
 start=read('gdd/operations.md').index('## 模式配置与参数唯一表')
 end=read('gdd/operations.md').index('## 内容接口与边界',start)
 text=read('gdd/operations.md')
 text=text[:start]+'''## 模式配置与参数唯一表

| 项目 | 当前合同 | 唯一责任 |
|---|---|---|
| 标准长局 / Demo / 首个灰盒 | 40–50 / 15–25 / 10–15分钟体验目标，TEST | [首发范围](../production/release-scope.md) |
| 现场改装机会与挂点 | 2保证+1可选初值；明确安装替换 | [测试参数](../production/test-profile.md) |
| 自动Fusion / 无限Relic | Operation禁用；Lab/FUTURE隔离 | [修改与效果](modifications-and-effects.md) |
| 入场槽位 | 2枪 / 1工具 / 1自由战术模块 | [玩家合同](player-and-input.md) |
| 任务板与难度倍率 | 六Offer与免费局前刷新；倍率仅允许外观收益 | [测试参数](../production/test-profile.md) |

'''+text[end:]
 put('gdd/operations.md',text)
 replace('gdd/operations.md','Week12微BLACKSTART后','M2微BLACKSTART验收后')

 rule('gdd/combat-and-arsenal.md','CMB-002','官方Operation采用有限实体弹动能、电磁实体弹和有限Energy Block枪械；Heat限制爆发但不产生新弹药。快速近战付距离、动作与暴露成本；独立Hammer/Knife/Spear/Sword及Staff/Spell完整谱系只作Lab/FUTURE试验，不进入基础版装备池。Heavy/Prototype使用稀缺资源，对部位/装甲/结构有真实作用，不用隐藏CanKillBoss钥匙。')
 rule('gdd/combat-and-arsenal.md','CMB-013','Energy Block固定为三把独立枪：单发、连发、强制蓄力，全部扣有限能量单位。蓄力从最低合法阈值到满蓄力提高伤害/资源成本，只有声明的高蓄力段产生范围效果；中断未发射时取消未提交弹药，但已经发生的暴露/时间不退。行为与初值由[战斗试制参数](../content/combat-balance.md)拥有。旧“等冷却即可无限续航”退出Operation，不保留两套长期实现。未来DLC标准Operation武器也必须是有成本的sidegrade。')
 rule('gdd/combat-and-arsenal.md','CMB-016','Operation枪械核心已裁决。Staff 3/6法术和四主武器近战试验仅归Lab/FUTURE；Quick Melee、有限资源和已有动作纪律继续有效。该选择见DDD-0014，后续不再作为等待所有者选技术的OPEN。')
 replace('gdd/combat-and-arsenal.md','| Staff 初始 Spell | 3 · CANON 官方 profile |','| Lab/FUTURE Staff 初始 Spell | 3 · 历史实验profile |')
 replace('gdd/combat-and-arsenal.md','| Staff 局内目标上限 | 6 · TEST 官方 profile；不是内核上限 |','| Lab/FUTURE Staff 局内目标上限 | 6 · TEST；不是Operation或内核上限 |')
 replace('gdd/combat-and-arsenal.md','| 精确DPS/护甲/姿态/热曲线 | OPEN | 待裸武器对照 |','| DPS/护甲/姿态/热初值 | TEST | 见战斗试制参数；实际平衡待裸武器对照 |')
 replace('gdd/combat-and-arsenal.md','缓冲时点、移动/受击/换弹中断均OPEN','缓冲时点和移动/受击/换弹中断采用测试参数的阶段优先级')

 rule('gdd/modifications-and-effects.md','BLD-001','官方Operation只注册允许的WeaponModule、ToolModule与TeamProtocol，有限挂点同位替换，不累计通用Relic。数值与事件声明Tag、Zone、SourceScope和目标；重要Proc是一等事件，默认可被明确允许的后续节点消费。Lab/FUTURE才可开启无限Relic容量，容量不等于无限供给。')
 rule('gdd/modifications-and-effects.md','BLD-003','Operation使用明确安装事务，不自动Fusion，不设Forge合成玩法。Lab/FUTURE可开启自动、确定的consuming synthesis A+B→C：预览消费对象与重大损失，未知只隐藏结果，继承Preserve/Merge/Convert/RebindScope/Promote/显式Discard，原件消失、新实例可继续合成。此隔离覆盖原来把自动Fusion当全局默认的表述。')
 rule('gdd/modifications-and-effects.md','BLD-004','Stat顺序为Base→装备/动作→角色Core（官方四人不设固定战力差）→已安装Modification/允许的Lab Relic→Team/Conditional→Crit→Target DamageTaken→Element/Reaction→Defense。同区加算、跨区乘算。初始暴击公式：tier=floor(chance/100)+Bernoulli((chance mod100)/100)，倍率=1+tier×(critMultiplier−1)，基础critMultiplier=2为TEST；chance需非负且有限。伤害/抗性/装甲路由由可验证定义执行，不使用隐藏Boss cap或随Build暗增抗性。Reaction以Tag/Registry定义，每一状态对消费一次。')
 rule('gdd/modifications-and-effects.md','BLD-005','Operation：找到兼容模块→预览目标、挂点、代价和被换下实例→在维护点安装→Authority原子切换Provider→旧件留合法世界位置→反馈行为变化。Lab自动合成另按BLD-003流程，不能把其拾取即消费UI复制到Operation。')
 rule('gdd/modifications-and-effects.md','BLD-008','共享事件/数学/事务，但Operation禁用自动Fusion/无限Relic与ResourceMint能力。Lab是按需验证规则接缝的内部测试场，不是必须先做完30Relic才能开始M2。内容字段为Trigger/Filter/Scope、成本/推进、输出、继承、RNG、并发、失效、模式准入和反馈。目录保留未来样本但明确不进入Operation。')
 rule('gdd/modifications-and-effects.md','BLD-012','采用唯一ModificationDefinition：target_scope、mount_point、compatible_tags、effect_graph、capability_permissions、tradeoffs、stack/conflict_group、visual_asset、mode_allowlist、schema version。presentationKind区分WeaponModule/ToolModule/TeamProtocol/Relic，不建立平行RelicBase效果引擎。枪的handling/behavior是逻辑槽，具体Receiver/Optic/Underbarrel/Magazine为视觉挂点；同逻辑槽冲突先于视觉位置。安装验证实例/revision/能力/代价，失败不吞件；TeamProtocol只一个共享协议位，所有人可见，先有效提交，不给Host特权。具体初值见测试参数。')
 replace('gdd/modifications-and-effects.md','# Relic、Proc、数值与自动 Fusion','# 修改、效果、数值与模式隔离')
 replace('gdd/modifications-and-effects.md','每tier增量系数待测 · PROPOSED','倍率1+tier×(基础暴击倍率−1)，基础2 · TEST')
 replace('gdd/modifications-and-effects.md','仲裁顺序、Crit tier公式、跨玩家Fusion均待批准','仲裁顺序采用BLD-007，Crit公式采用BLD-004；跨玩家Fusion首版不支持，Lab扩展需新决策与共同消费授权')

 rule('gdd/economy-and-support.md','ECO-001','Operation所有远程主枪均使用有限资源。Ballistic和EM扣实体弹，Energy Block扣有限能量单位，热量只限制节奏而非生成补给；Quick Melee付距离/时间/暴露风险，Heavy扣独立固定弹药/燃料。Staff等续航家族不进入Operation。生成器必须保证初始合法配置存在数学上可行的主任务解法；玩家后续错误仍可能耗到真实失败。')
 rule('gdd/economy-and-support.md','ECO-010','Operation不设置通用商店、Gamble、免费Respec或重掷RNG服务。任务Cart是一次真实设施预算，不是可退款购物车；支援通过Charge与Beacon，改装通过合法维护点和原子替换。Lab/FUTURE的商店与Respec不进入基础产品。')
 replace('gdd/economy-and-support.md','Operation可持续Melee/Energy仍合法','Operation有限Energy和Quick Melee按各自真实成本合法')
 replace('gdd/economy-and-support.md','需 DEC-001批准','由DDD-0014在授权下确认')
 replace('gdd/economy-and-support.md','| Meter threshold/value | OPEN；Greybox例仅供content卡 |','| Meter threshold/value | 100 · TEST；包内容见测试参数 |')
 append('gdd/economy-and-support.md','## 当前边界闭合\n\nECO-016 · DECIDED · 来源：'+SOURCE+'；DDD-0014。\n\nOperation文中的旧Weapon/Relic draft实例现为允许的Modification/供给实例，传统Relic只在Lab。包的实际弹量、Med量、首轮等待采用测试参数；高价值各Seat资格一次，后进者继承Seat状态不重置。非法投递的返费事务必须与“不生成物资”一起提交，合法Pod落地后的战术损失不返费。废料同凭据用于Support或成功撤离外观收益二选一，不双算；未撤离部分收益0，已Banked知识100%保留。')

 rule('gdd/progression-and-bastion.md','PRG-001','官方四人及基础可用装备从起点可选，不靠刷永久战力解锁主任务能力。长期进度是武器/工具/模块的横向选项、外观/称号、Archive、知识、挑战和玩家掌握。无永久伤害/血量升级、无把Run强武器/资源存入跨局装备仓；Saved Loadout只保存合法定义选择和外观，不保存局内改装/弹药。Lab的Fusion/Spell发现不混入Operation能力门锁。')
 rule('gdd/progression-and-bastion.md','PRG-003','唯一可消费外观货币名称为外观信用点，来自成功撤离且未用于Support的合法废料；Knowledge/字形/筑路者资料不是货币，不沿用含糊Archive Credits。壁垒实体Hub和快捷菜单共享任务/配装/Archive/Test Chamber数据，不强迫跑NPC。完整战报/回放不保留历史，长期Archive和成就不是战报录像。')
 replace('gdd/progression-and-bastion.md','| 失败Operation/Archive代币 | 约成功应得50% · TEST | SRC-SSOT-2.0 §4A.16、§40 |','| 失败未撤离废料收益 | 0% · DECIDED；旧50%测试停止 | DDD-0014；已banked知识仍100% |')
 replace('gdd/progression-and-bastion.md','| Upload节点频率/一次用时 | OPEN | 不以任意数字假装解决长局失败 |','| Upload节点频率/一次用时 | 标准长局至少中段/撤离前；3s · TEST | 测试参数；不宣称已解决长局失败 |')
 replace('gdd/progression-and-bastion.md','具体pool策展OPEN','玩家在Hub选择已解锁的合法装备，不强迫把不喜欢的横向解锁加入随机必选池')
 replace('gdd/progression-and-bastion.md','普通Offer的数量、刷新方式和周期仍OPEN','普通Offer采用测试参数的六卡与局前免费整批刷新，不按现实日期锁内容')
 append('gdd/progression-and-bastion.md','## 资格与最终提交\n\nPRG-015 · DECIDED · 来源：'+SOURCE+'；DDD-0014/0016。\n\n上传资格为在该发现/采集后参与且上传时仍在本次Run名册的Seat；断线宽限内保留，明确离队者保留此前已Banked权利但不领取后来新发现。late join不补发加入前所有历史发现；同场后续再次合法发现可按账号已有集合去重。任务完成奖励要求在最终目标完成前加入并实际参与至少一个任务/战斗/支援事件，非伤害竞赛；Host不得手填名单。主任务Final Result须经过最终恢复证书后幂等写账号。')

 rule('gdd/survival-and-recovery.md','LIFE-002','Operation不回满；脱战低恢复线20%、手动救援3s/40%生命、起身Grace最多2s且攻击解除、倒地45s、Carry按半速消耗为TEST初值，归测试参数。所有比例基于当前合法HealthCap，不能恢复被牺牲/封印部分。Downed可爬行/Ping及用规则允许的枪，不能执行需要双手的重资产/Carry。普通Healing不等于Revive。')
 replace('gdd/survival-and-recovery.md','这是待验证提案，不取代已确认规则','采用全体仍连接真人一致确认放弃，30秒未形成一致则继续合法恢复模拟；这不是任意处决计时，流程须测试')
 replace('gdd/survival-and-recovery.md','具体阈值 OPEN','初始贡献阈值与有效威胁资格见测试参数')
 replace('gdd/survival-and-recovery.md','| Grace/bleedout/脱战判定/Carry影响 | OPEN |','| Grace/bleedout/脱战判定/Carry影响 | 2s/45s/10s/半速 · TEST，详见测试参数 |')
 replace('gdd/survival-and-recovery.md','防farm、主动放弃语义与失败叙事仍 OPEN','防farm按唯一威胁/贡献资格，放弃按全体明确确认，Wipe不进入正史死亡；仍需实测')

 # Technical contracts replace the old unresolved questions in their original owners.
 replace('technical/network-and-persistence.md','具体网络provider和部署OPEN','provider选择已由技术栈与DDD-0015关闭，实际部署/费用批准由OWNER-02保留')
 replace('technical/network-and-persistence.md','但rewind窗口与具体hitscan/projectile算法仍OPEN','采用技术栈STACK-003的有限命中体历史，初值200ms；非整世界回滚')
 replace('technical/network-and-persistence.md','**具体网络provider、选主算法、迁移快照频率和安全校验仍未锁。**','**provider、选主、租约、1s恢复快照与安全校验已由[技术栈](technology-stack.md)、[主机迁移](host-migration.md)、[数据合同](data-contracts.md)关闭。**')
 replace('technical/network-and-persistence.md','后续需独立裁决受限安全包直传、官方内容寻址缓存或明确拒绝加入','按[模组安全](mod-security-and-sync.md)明确拒绝加入；不直传第三方原资产、不静默升级')
 replace('technical/network-and-persistence.md','断线中的pickup/Fusion/Support以最后已提交事务为准','断线中的pickup/Fusion/Support以最后已认证恢复点内的事务为准；突然失联可回退短暂未认证模拟，区别与RPO见主机迁移合同')
 replace('technical/network-and-persistence.md','且资源/任务/实例零重复零丢失','且已认证恢复点内资源/任务/实例零重复零丢失，并报告未认证窗口的实际回退量')
 replace('technical/network-and-persistence.md','Data/Graph/受支持Sandbox内容可进入标准自动同步','首版仅Data/受限Graph及允许资源进入标准自动同步，不执行任意脚本')
 append('technical/network-and-persistence.md','## 当前专门责任链接\n\nProvider与包版本安装： [技术栈](technology-stack.md)。选主/租约/恢复点/RPO： [主机迁移](host-migration.md)。消息字段/原子文件/账号claim： [数据合同](data-contracts.md)。旧hash、拒绝执行代码和同步： [模组安全](mod-security-and-sync.md)。旧DDD中保留的provider/算法OPEN是当时的历史未决项，已由DDD-0015–0017裁决，不再要求用户选择。')
 replace('technical/modding-and-toolchain.md','Data/Graph/受支持Sandbox Script可走标准同步','首版Data/受限Graph和允许资源可走标准同步，任意脚本不允许')
 replace('technical/modding-and-toolchain.md','具体允许渠道待决定','首版Native DLL全部拒绝，未来能力扩展须新安全决策')
 rule('technical/modding-and-toolchain.md','MOD-018','完整游戏内信息架构采用[Mod Manager](../gdd/mod-manager.md)：我的内容、Workshop浏览、Profile、加入同步、下载缓存、诊断帮助。主流程不要求外部Manager；Steam Overlay仅作平台详情/报告等补充，不替代一键同步与可理解错误。')
 replace('technical/modding-and-toolchain.md','团队人数、公开API日期、脚本语言、license、完整Mod Manager UI与TC计划仍有OPEN部分','团队/预算由OWNER-02决定；公开API依M5作者验收而非臆造日期；首版Data/Graph、拒绝脚本/Native、完整Mod Manager、TC后置已由DDD-0017关闭；个别资源license须实际采购核验')
 append('technical/modding-and-toolchain.md','## 首版公开能力与历史范围\n\nMOD-019 · DECIDED · 来源：'+SOURCE+'；DDD-0017。\n\n源文“支持Sandbox/Native/Total Conversion”是长线扩展愿景，不是首版自动执行承诺。首版只交付Data、有界Graph与受支持资源，权限、包规范、hash缓存、Loader失败策略由[模组安全](mod-security-and-sync.md)拥有。任何旧脚本超预算描述仅适用于未来新决策通过后的能力，当前Loader直接拒绝该包类。完整Forge编辑器后置，作者先用JSON/schema/验证CLI及少量Editor辅助工具。')

 # Social defaults and controller-safe current behavior.
 append('gdd/coop-and-social.md','## 已选社交初值与语音传输\n\nCOP-009 · DECIDED · 来源：'+SOURCE+'；DDD-0018。\n\nPublic踢人需除目标外仍连接真人的严格多数赞成，4人时需2票、3人时需2票；2人Public不允许单方踢人，允许离开/屏蔽并新建私房。投票30s，发起者120s冷却，避免轰炸；Private owner按公开规则可移除。AFK120s警告，180s可投票移除；不自动消耗玩家关键物或让Bot接管账号购买。重连Seat保留120s初值，之后可允许真人接替但继承同一身体/物资/claim状态，不刷新资源；旧玩家回来需要合法空Seat。以上时值均TEST。\n\nVoice使用独立于Gameplay Host的Steam对等语音连接，1–4人小队最多每人三个发送目标，限流/声道优先级与Mute/Block本地生效；Host迁移不重建其余仍可用语音连接。真实提供者故障仍可能中断，不能保证“永不中断”。不把压缩语音写入Run或Replay。')
 replace('gdd/coop-and-social.md','| 公开Kick/AFK阈值/补位时机 | OPEN | 需陌生人测试 |','| 公开Kick/AFK阈值/补位时机 | COP-009初值 · TEST | 需陌生人测试 |')

 # Content cards retain experiments but cannot masquerade as the launch list.
 rule('content/combat-prototypes.md','PRT-001','首发试制先AR/Shotgun+工具/自由战术模块，再EM与三把独立Energy Block枪。独立四近战、Staff和Spell卡完整保留为Lab/FUTURE资料，不进入Operation奖励、教程或必需工作量；全部数值未测。','TEST')
 rule('content/combat-prototypes.md','PRT-005','首批生产使用人类来源的通用枪械与维修重资产，不将任何具体卡擅自宣布为筑路者原件。NAR-010“部分Prototype源于筑路者技术”的明确事实保留；哪一把正式命名武器属于哪条历史谱系随OWNER-01的内容审阅再批准，不阻塞灰盒。')
 rule('content/combat-prototypes.md','PRT-006','三枪械家族和三把Energy子型已选定，全部扣有限资源。初始HP、弹仓、射速、成本、蓄力、敌人和工具数值见[战斗试制参数](combat-balance.md)，均TEST不是已完成平衡。Staff/Spell表只是未来实验保存。')
 replace('content/combat-prototypes.md','正式HP/DPS仍OPEN','正式平衡未测，首个可执行数值采用战斗试制参数')
 replace('content/combat-prototypes.md','## Utility 与 Signature 卡','## Utility 与自由战术模块卡')
 replace('content/combat-prototypes.md','三Signature身份来源','三个战术模块的历史候选来源')
 replace('content/combat-prototypes.md','占Weapon位，Operation初始完整','只限Lab/FUTURE，Operation不加载')
 append('content/combat-prototypes.md','## 首发工具与重资产裁决\n\nPRT-007 · DECIDED · 来源：'+SOURCE+'；DDD-0014。\n\n三工具为Scan、Foam、Decoy；Decoy投掷有限物理声源，引导能听见且路径可达的敌人，不改写已确认视野或任务来源预算。三自由战术模块沿Aegis/Breaker/Echo原型，资源与冷却详见战斗试制参数；没有人物专属。首发三件Team Ordnance选择Cutter、HMG、Anti-armor Cannon；GL/Sonic保留未来候选，不能因为目录有五行就承诺全部首发。')
 replace('content/modification-catalog.md','具体安装是否要工作台为OPEN，不能默认加入每次回Hub跑腿','采用前线合法维护点3s安装，取消不耗材；不要求回Hub跑腿，具体见测试参数')
 replace('content/modification-catalog.md','Recipe priority候选F08最高、然后F03/F07、其余按稳定ID；该排序是TEST','Lab配方优先级TEST为F08=30、F03/F07=20、其余=10，再按稳定ID')
 append('content/modification-catalog.md','## 首发挂点映射与目录边界\n\nMODC-002 · DECIDED · 来源：'+SOURCE+'；DDD-0014。\n\nDamper与Pressure占handling槽；Breach、Link、Reactor占behavior槽，即使视觉分别装在枪下/瞄具/弹仓也不能同时占同一逻辑槽。Sink占tool槽；Cover占唯一team protocol槽。Breach附带固定2发独立破结构弹，不补关键Cell，基础枪参数不能复制出无限弹。Pressure初值每次有效射击耗2单位ammo且穿甲能力增加，倍耗同事务；Link用自身有限电池，不显示未知敌人；Reactor容量降低25%以换允许ReactionTag；Cover持续窗口不加倍Scan。数值均TEST，不扩充正式已验证目录。\n\n30Relic/8Fusion全部明确留在Lab/FUTURE，缺参数的未来卡不可激活为生产内容；保留文案不是默许默认0或假装完成制作。')
 rule('content/characters.md','CHAR-007','所有角色自由选择个人战术模块；不再将人物身份与Signature绑定。该装备决定来自当前授权，人物代号/人格/关系仍待OWNER-01；批准人物不等于批准其年龄、身体、外观或演员。')
 append('content/characters.md','## 审阅入口\n\n完整上下文已汇总到[故事总览](../gdd/story-overview.md)。本文件REVIEW仅指人物创作身份尚需所有者裁决，不指技术配装还在两方案之间。候选人物细节不能在未批准前转成付费美术或配音订单。')
 replace('content/blackstart.md','源Relic奖励在最新武器改装提案下需作A/B版本，不自行抹掉旧测试','当前Operation只使用Modification；原Relic版本是Lab历史对照，不混入首发验收组')
 replace('content/blackstart.md','Supply包内实际弹量/医疗量OPEN，先按试测记录，不给假精确经济','Supply包内弹量/医疗量采用测试参数初值并记录真实支出，不能把初值称作已平衡经济')
 replace('content/blackstart.md','对照profile沿源规则测试Relic，二者不能混在同一数据组声称某方案更好','主要对照为同场景无改装；原Relic只在Lab，不能混在Operation数据组声称改装更好')
 append('content/blackstart.md','## 分阶段构建而非一口气做整图\n\nBST-010 · DECIDED · 来源：'+SOURCE+'；DDD-0018。\n\nM2 miniature只搭B00/B01→B03→B05→B07/B08，保留一处合法查找、一项电力选择、一条顺序Fault、一处上传、退出/Wipe及资源事务；目标10–15min。完整房间表用于随后扩展，不把35–45分钟历史切片误当第一周任务。标准长局40–50min、Demo15–25min为不同内容profile；固定拓扑证明后M4才组合PCG。')

 # Future content receives a clear disposition, not a false completion claim.
 replace('gdd/descent.md','当前推荐先用内部Combat Lab验证通用接缝','已选择未来扩展，内部Combat Lab仅按实际契约测试需要使用')
 replace('gdd/descent.md','| 是否首发/是否制作 | OPEN，当前推荐延后 | DEC-001 |','| 是否首发/是否制作 | 不进入基础1.0；未来另过制作Gate | DDD-0013/0018 |')
 append('gdd/descent.md','## FUTURE状态如何解释\n\n本文件的奖励、层Boss、Endless、活动阈值等OPEN均是未来产品实验，不是当前基础版待所有者选择的技术问题。基础游戏不需要实现这些系统才能通过文档或M0。未来启动时先用单一行星、三层原型证明内容/节奏，再按五层历史目标扩展；未通过不对外承诺日期或销量。')
 rule('gdd/narrative-bible.md','NAR-005','Descent叙事边界已由NAR-030及DES-008/010定义：未来公共事件打开真实行星端点，每次为新区域远征，不是空间重置、时间循环或复活旧敌人。旧未稳定Fold副本解释退出现行方向；具体首个行星内容在未来扩展Gate裁决，不阻塞Operation。')
 append('gdd/narrative-bible.md','## 本次审阅闭合范围\n\nNAR-031 · DECIDED · 来源：'+SOURCE+'；DDD-0018；创作批准仍属OWNER-01。\n\n[完整故事总览](story-overview.md)整合历史因果与当代玩家常态供所有者审核。原明确CANON继续有效；NAR-011连接性细节、四人创作身份与次要未闭合历史不能因文档定稿而伪称批准。基础版不要求精确列出所有古代伤亡/小时数/设施真名，禁止用未审核细节填空。数月供应危机解释重开决定；常规合同无现实时间城市倒计时、无个人章节或节点征服。苍白增生等支线不承担基础核心因果，未展开阵营不进入首发敌人制作清单。')
 append('gdd/central-story-spine.md','## 全文审阅与状态\n\n当前入口为[完整故事总览](story-overview.md)，所有者需裁决的是OWNER-01的创作内容，而非网络或装备技术。个人故事阶段、永久节点清场、按账号推进的旧主线均非基础版规则。故事审阅后才进行真正独立、只读、无项目上下文的审查；本轮编辑没有执行或冒充该审查。')

 # Adopt only explicitly enumerated reviewed behavior contracts. Numeric tests,
 # narrative candidates, experimental cards and uncertain audience claims remain tests/review.
 ADOPT={
 'gdd/player-and-input.md':['PLY-006','PLY-012','PLY-013'],
 'gdd/operations.md':['OPS-004','OPS-005','OPS-006','OPS-008','OPS-010'],
 'gdd/combat-and-arsenal.md':['CMB-005','CMB-006','CMB-007','CMB-008','CMB-009','CMB-012','CMB-014','ORD-001','ORD-002','ORD-003'],
 'gdd/modifications-and-effects.md':['BLD-006','BLD-007','BLD-009','BLD-010'],
 'gdd/economy-and-support.md':['ECO-004','ECO-005','ECO-006','ECO-007','ECO-008','ECO-009','ECO-011','ECO-013','ECO-014','ECO-015'],
 'gdd/progression-and-bastion.md':['PRG-004','PRG-005','PRG-006','PRG-007','PRG-009','PRG-011'],
 'gdd/survival-and-recovery.md':['LIFE-004','LIFE-005','LIFE-006','LIFE-007','LIFE-008','LIFE-009'],
 'gdd/coop-and-social.md':['COP-003','COP-004','COP-005','COP-006','COP-007'],
 'gdd/encounters-and-difficulty.md':['ENC-004','ENC-005','ENC-006','ENC-007','ENC-008','ENC-009','ENC-012'],
 'gdd/missions-and-spaces.md':['MIS-004','MIS-005','MIS-006','MIS-007','MIS-008','MIS-009','MIS-010','MIS-012','MIS-013','MIS-014','MIS-015'],
 'gdd/world-and-information.md':['WRD-004','WRD-005','WRD-006','WRD-007','WRD-008','WRD-009','WRD-010','WRD-012','WRD-013','WRD-017'],
 'gdd/ux-and-accessibility.md':['UX-003','UX-004','UX-005','UX-008'],
 'gdd/audio-and-haptics.md':['AUD-002','AUD-003','AUD-004'],
 'gdd/art-direction.md':['ART-002','ART-003','ART-004','ART-007'],
 'gdd/debrief-and-replay.md':['RPL-002','RPL-003','RPL-004','RPL-007'],
 'gdd/narrative-delivery.md':['NDL-001','NDL-003','NDL-004'],
 'technical/architecture-and-performance.md':['ARC-002','ARC-003','ARC-004','ARC-008','ARC-009'],
 'technical/network-and-persistence.md':['NET-003','NET-004','NET-005','NET-006'],
 'technical/modding-and-toolchain.md':['MOD-002','MOD-003','MOD-004','MOD-005','MOD-006','MOD-007','MOD-008','MOD-009','MOD-011','MOD-012'],
 'technical/replay-recording.md':['TRP-001','TRP-002','TRP-003','TRP-004','TRP-005'],
 'content/blackstart.md':['BST-003','BST-004','BST-005','BST-006','BST-008'],
 'content/modification-catalog.md':['REL-002','MODC-001','REL-004'],
 'production/platform-and-release.md':['PLAT-005'],
 }
 for path,ids in ADOPT.items(): approve(path,ids)

 # System-specific finalization notes resolve remaining scope/tuning ambiguity.
 CLOSURES={
 'gdd/encounters-and-difficulty.md': '首批用Runner/Suppressor，随后Holder/Scout/Flanker；AI只基于合法感知/记忆/通信，Source存量有限。五档难度全部可选，组合、资源与环境约束先变，禁止动态读玩家Build加抗性。无来源spawn、被封Ingress偷刷新、无意义HP海都是否决条件；数量/声距按战斗试制与种子预算实测。',
 'gdd/missions-and-spaces.md': 'PCG按区域→任务/兼容支线→typed graph→Cluster与port→门/电力→资源可解证明→敌人来源→奖励/信息→终检顺序生成，各步独立seed stream。失败最多重试32个派生seed后使用同任务族已验证fallback，仍失败则拒绝开局并记录seed，不生成坏局给玩家。单人顺序、关键Cell可达、重资产耗尽旁路、Optional重接、信息不软锁为硬约束；1000seed自动检查加20seed人工辨识为M4门槛。',
 'gdd/world-and-information.md': 'Cart采用三Cell基线，普通选项1、Vault2，无撤销退款和常规多数投票。操作者3s保持确认期间全队看到影响与成本；其他合法提交造成revision改变就取消旧确认。Terminal只查合法已知信息和局部权限，不连全知雷达/全局Alarm。重要操作有键鼠/控制器等价短选项，不要求玩家输入晦涩真实命令才能做主任务。地图只显示确认信息；可破与不可破边界由材质/任务语义明确解释。',
 'gdd/ux-and-accessibility.md': '运行时统一uGUI/TMP。主流程固定为启动/语言与无障碍→主菜单→Hub任务板/选人配装→Lobby/包同步→任务HUD→暂停设置/社交→结算/临时回放→Hub。每页必须有loading、empty、error、offline、controller focus和返回路径。中英文本为首发基线；字幕/语音独立，重点危险双通道，字号缩放/重绑/色觉友好/减少运动闪光/镜头摇晃可调。TPS与Bot仍是首发合同，不以原型只做FPS为由删除。',
 'gdd/audio-and-haptics.md': '使用Unity AudioMixer，层级优先关键危险/团队战术事实，其次武器命中/动作，再环境/音乐/人物闲谈。语音ducking不能吞掉危机预兆；声音位置来自合法世界声源。动态混音和声部限制只影响表现，不改变AI听觉事件。玩家语音默认PTT且不录制；字幕覆盖影响玩法的信息。最终录音语言、演员和真实付款由OWNER-02/03批准，灰盒不伪装成正式配音。',
 'gdd/art-direction.md': 'Stylized Industrial Realism被选择为制作方向，实际视觉样张与人物外观仍需OWNER-03。环境先灰盒和单一kit统一，规范、许可和图像→可动资源完整管线归资产生产文档；未选palette/字体不是让用户选技术，开发者先用合法系统字体和中性测试材质证明可读性，最终品牌视觉才付费生产。',
 'gdd/debrief-and-replay.md': '详细权威统计与临时本地回放均保留首发。回放是低频位置+关键事件查看器，不是录像/全PhysX可重演证明，不记录玩家语音。离开结算或进入新Run清除临时记录，异常退出下次启动清残留；永久Archive/成就和必要恢复文件属于不同数据域。无MVP/KD公开排名；因果不足则写共同/环境/无法归因，不为故事性编造破坏潜行者。',
 'gdd/narrative-delivery.md': '优先级采用关键战术事实→短人物评论→可选长背景；战斗不强播长档案，不让关闭语音失去关键操作信息。重复合同不重复假装首次发现核心历史。人物与创作事实仍按OWNER-01，短句/冷却初值为TEST；完整故事审阅入口已独立提供。',
 'technical/architecture-and-performance.md': '具体依赖现在由technology-stack.md拥有；旧讨论的网络provider/编辑器/脚本选择不再OPEN。普通GameObject-first与局部热路径优化继续，禁止为未来Descent先写通用游戏引擎。数据合同定义稳定ID、字段和状态写入；网络/持久化共用语义但不同投影。所有性能要求仍NOT RUN，显示密度优化不能成为丢合法结果借口。',
 'technical/replay-recording.md': '采用数据合同的版本化有界二进制块和权威事件去重；初始玩家5Hz、关键非玩家1Hz，统计按事件完整归因而非位置采样推测。TRP-006的CPU/磁盘预算继续作为测试目标，不把位置采样值说成已通过50分钟压力测试。回放渲染不依赖所有历史物理对象重演，丢失非关键轨迹可明确显示缺口，不能篡改统计。',
 }
 for path,body in CLOSURES.items():
  append(path,'## 本次定稿：执行边界\n\n'+body+'\n\nAuthority: delegated，'+SOURCE+'；DDD-0013–0018。所有未提供实测的参数与验证仍为TEST；未展开的未来功能不在当前实现关键路径。')

 # Production removes obsolete time promises and records scope honestly.
 document('production/roadmap-and-validation.md','PROD-ROADMAP','production','制作路线与验证关卡','''本计划按依赖与证据推进，不承诺12个月、Week12或Day180必然发布。团队人数、预算和吞吐未知；旧日期只是历史研究节点，不能当排程事实。首发范围由[范围合同](release-scope.md)拥有，逐任务顺序由[实施交接](implementation-handoff.md)拥有，具体通过线由[验收矩阵](acceptance-matrix.md)与[风险登记](risk-register.md)拥有。

## 当前顺序

M0可复现工程→M1裸枪/移动/有限资源→M2完整无Bot微型BLACKSTART→M3真实合作/包锁/迁移→M4程序任务和六任务族→M5首发全部玩家/内容/Mod/回放能力→M6真实发布证据。关键路径不包含Descent、完整可视Forge、任意脚本或新商店。

每步只扩大已经证明有用的系统。裸战斗无趣先修枪感，任务层无贡献先修选择，程序局无聊先修Cluster而非加房间数，网络恢复失败先修一致性，Deck超预算先剖析而非删结果。使用同条件对照，保留失败证据；不可用新奖励掩盖等待和认知税。

## 决策与状态

全部游戏里程碑NOT STARTED；文档基线与文档测试不改变这一状态。M0可使用免费本地替身立即开始，不依赖人物美术或付费API。实际云部署、资产购买、合同、最终名字/价格/日期由OWNER-02授权。TPS、Bot、Deck60、迁移、详细战报等若需缩减，必须按OWNER-04提供证据，不静默放弃。

## 每Gate交付

提供独立可运行构建、最短操作说明、源码commit和依赖锁、实跑测试/日志/设备设置、实际工时、未过风险与下一任务。真实玩家招募先说明隐私与记录范围，未获授权不采集个人遥测；内部事件调试可用本地合成数据。发布前再核验平台条款、许可证、AI内容披露、商店描述和支持渠道，不用历史文档代替当前法律/平台检查。''',deps=['release-scope.md','implementation-handoff.md','acceptance-matrix.md'])
 rule('production/platform-and-release.md','PLAT-002','无付费Early Access；内部/封测/Steam Playtest→短完整Demo→Premium1.0候选。Demo目标15–25min的短Operation，同一runtime较小内容集，与40–50min标准长局不冲突。支持好友合作和当时已通过验收的安全包路径，不先建完整TC/Forge生态。只迁移幂等外观/徽章和明确允许的横向声明，不迁移Run/任务资源/临时战报或整个秘密Archive；购买、最终售价/日期仍需OWNER-02。')
 rule('production/platform-and-release.md','PLAT-004','首发唯一Operation；完整内容范围由release-scope.md拥有，不能从一个模板或某个房间数推导足够销售。Demo只用一个短完整合同展示资源选择、设施后果和合作收束。底层API不是主要商店卖点；先证明普通玩家愿意再玩，再作商业发布。')
 replace('production/platform-and-release.md','OPEN：首发内容量/价格、Demo模板、API冻结期、TC时间、语言/区域、退款预期、发行预算','当前：内容规划见范围合同；Demo采用短Operation；API以外部作者Gate冻结；TC未来；中英文本。价格、发行日期、预算与退款/支持政策需OWNER-02商业批准')
 replace('production/risk-register.md','# 残酷评审与风险登记','# 风险登记与否决条件')
 replace('production/risk-register.md','下面所有修正和阈值都是PROPOSED/TEST','下面风险机制和阈值仍为TEST，已选缓解行为按当前范围和DDD执行')
 replace('production/risk-register.md','唯一stage/命名空间/首次提交','唯一作者历史/命名空间/幂等发现，不存在账号剧情stage')
 append('production/risk-register.md','## 当前风险处置分类\n\nRK01/RK06/RK07/RK09/RK28中独立双模式、自动Fusion、Staff、四近战与完整Lab内容的生产风险已通过后置隔离，不是测试通过；只有共享效果正确性进入当前基线。RK10由人物/战术模块解绑减轻，仍须验证。RK22采用明确认证恢复点与租约，不能宣称零未认证时间回退。RK23、RK31、RK35继续是硬证据关卡。增加RK38：小型在线协调器可用性/费用，OWNER-02部署前给出预算与停服策略；RK39：公开repo第三方资产泄漏，未具再分发权不得上传；RK40：文档看似定稿而代码仍不存在，里程碑保持NOT STARTED。')

 # Authoring and decisions are generated here to keep one active register.
 document('governance/authoring-guide.md','GOV-AUTHORING','governance','文档权威、命名、决定和维护规则','''## 权威不是文档成熟度

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

运行文档validator、自测和inventory；检查远端commit与CI。游戏测试另按验收矩阵，报告实际运行与未运行。不能声称已购资产、正式许可证清查、独立盲审、Steam认证、Deck达标或可玩构建，除非存在真实证据。交接必须有当前状态与下一个可执行任务，不依赖聊天记忆。''',deps=['owner-decisions.md','decision-register.md','document-register.md'])

 decisions=[
 ('0013','delegated-baseline-and-scope','授权定稿与Operation唯一基础产品','采用Operation-only基础版；允许助手关闭普通技术/设计分叉；明确CANON/DECIDED/TEST与创作审批，完整登记和可复现交接。','项目有大量历史提案，所有者不懂编程；逐项技术投票会让责任空转。','拒绝对等双模式首发（内容/教程/QA/匹配成本翻倍）；拒绝全量无条件CANON（会伪造用户批准与测试）；拒绝只加新概要而不改旧责任规则。','TPS、Bot、Deck、主机迁移和详细战报等明确要求保留，按阶段证明；修改它们需OWNER-04。历史来源不改。','DDD-0001与DDD-0006的未决产品/排期方向；旧DEC-001/005等普通分叉。','若M1/M2不能证明裸战斗和设施选择有价值，停止扩内容并以证据改设计；不是自动恢复双模式。','../owner-decisions.md; ../../production/release-scope.md; ../../production/implementation-handoff.md'),
 ('0014','operation-loadout-and-modifications','Operation装备、有限经济与修改规则','两枪+一工具+一自由战术模块；有限Energy Blocks；Operation不加载Staff/无限Relic/自动Fusion；统一Modification、有限槽与前线安装。','旧两Utility/人物Signature/自动合成与最新固定两枪一工具意图相冲突。','拒绝角色独占强度与职业钥匙；拒绝免费无限Energy抢走弹药选择；拒绝隐藏吞配件；拒绝平行两套效果引擎。','四角色身份与Seat保留，装备可重复；世界重资产双手/有限/可回收；知识banked100%，未撤离废料0；数值全部TEST。','DDD-0002/0004与旧PLY-001、BLD-001/003、CMB-002的Operation解释；不是删除历史实验内容。','若改装不增加可复述选择，减少/删减该层；若单一家族成为所有情境上位，改成本/动作而非暗削玩家结果。','../../gdd/player-and-input.md; ../../gdd/modifications-and-effects.md; ../../gdd/economy-and-support.md; ../../production/test-profile.md'),
 ('0015','steam-networking-and-data-stack','Steam网络栈、数据格式与命中历史','Unity6.3LTS/URP、FishNet+FishySteamworks+Steamworks.NET、Steam Lobbies/SDR；uGUI/TMP；JSON作者定义和有界版本化binary DTO；自有受限hitscan历史。','必须给实现者具体依赖赢家，同时保持Kernel不依赖平台。','拒绝NGO/EOS/Photon等并行方案；拒绝以Steam Lobby转移冒充恢复；拒绝假装FishNet内建迁移或已购买Pro ColliderRollback；拒绝任意对象图反序列化。','M0真实构建后固定精确补丁/commit/许可证；未安装兼容组合不编造版本。离线Solo不依赖Steam/云。','DDD-0008继续有效并细化6.3；DDD-0010–0012继续拥有命令/60Hz/复制；其中历史provider与rewind OPEN由本决定关闭。','实际依赖兼容或性能Spike失败时重审适配实现，保持Gameplay合同；禁止因示例连网就宣布4人恢复通过。','../../technical/technology-stack.md; ../../technical/data-contracts.md; ../../research/technical-evidence-2026-09-05.md'),
 ('0016','host-migration-and-recovery-certificates','主机迁移、租约和认证恢复点','每Run小型Durable Object协调epoch/租约；1s逻辑快照+备份ACK认证；快照/已提交状态变更恢复，不重跑PhysX输入。','玩家主机离开与网络分区需要明确唯一权威和实际可恢复状态。','拒绝Lobby owner即完整游戏Host方案、全世界60Hz云模拟、零延迟零丢失虚假承诺、分区各侧都继续写。','在线需要可用协调器与合法身份；实际部署/费用OWNER-02。已认证状态无重复遗漏，未认证窗口有明确RPO；拿不到一致证据冻结/挂起。','细化NET-002/003/005/006与DDD-0010–0012原恢复要求，区分普通复制与持久恢复水位。','分区双主、证书遗漏、可恢复组件不完整即阻止公开联机；若TTL造成过多暂停按真实网络证据重新调TEST，不能牺牲唯一权威。','../../technical/host-migration.md; ../../technical/network-and-persistence.md; ../../production/acceptance-matrix.md'),
 ('0017','safe-mods-and-native-manager','安全模组首版、精确包锁与原生管理器','首版Data/有界Graph/允许资源；无任意脚本/Native；完整内置Mod Manager；Workshop分支版本配合应用hash缓存，旧hash不可得明确拒绝。','全开放愿景与普通玩家自动同步的安全/授权边界必须可执行。','拒绝加入Lobby即运行DLL；拒绝把hash当安全认证；拒绝静默更新挂起Run；拒绝Host直传他人购入资产或另建公共分发市场。','官方内容同路径验证，敏感运行时权力不公开；依赖/资源/Graph成本有界；完整TC/Forge/更强脚本未来单独Gate。','细化DDD-0003/0004/0009及MOD-015/018的语言、UI、Native和旧版本未决项；Steam-only既有要求保留。','恶意包执行、路径逃逸、半激活、旧hash丢失被掩盖即阻止发布；新脚本能力需新的威胁建模和独立评审。','../../technical/mod-security-and-sync.md; ../../gdd/mod-manager.md; ../../technical/modding-and-toolchain.md'),
 ('0018','production-assets-and-handoff','制作顺序、资产管线和完整交接','M0→M6证据驱动；买通用做品牌；Blender加工，Meshy API仅获准受控试验；固定入口/完整目录/风险/验收/所有者队列。','新手所有者需要可玩构建和清晰决定，不是大量要手装的功能或未经批准的消费。','拒绝假12月排期、灰盒前批量买资产、AI模型直接当成品、公开仓库泄漏受限原资源、自称完成独立故事盲审。','所有游戏任务NOT STARTED；故事总览与人物REVIEW，正式视觉和配音OWNER-03；真实钱/账号OWNER-02；源快照SHA保持。','DDD-0005/0006/0007的未完成讨论由当前生产/故事审阅路径承接，不替所有者批准创作；旧路径改为描述性命名。','M1/2失败先修体验；M3/Deck/许可Gate失败不得发售；有实测吞吐才排日期，预算/人力改变可重估范围。','../../production/implementation-handoff.md; ../../production/asset-pipeline.md; ../../gdd/story-overview.md; ../owner-decisions.md'),
 ]
 rows=[]
 for num,slug,title,decision,problem,rejected,constraints,supersedes,revisit,links in decisions:
  path=f'governance/decisions/DDD-{num}-{slug}.md'
  linked='；'.join(f'[{Path(x).stem}]({x})' for x in links.split('; '))
  body=f'''**Date:** 2026-09-05 · **Authority:** delegated by owner · **Status:** DECIDED, implementation NOT STARTED.

## Decision
{decision}

## Problem and rationale
{problem}

## Alternatives and rejection reasons
{rejected}

## Constraints and architecture impact
{constraints}

## Supersedes / preserves
{supersedes}

## Reconsideration trigger
{revisit}

## Implementation and tests
按实施交接的M0–M6任务落实；验收矩阵保留所有未运行状态。每个实现PR提供原子性、取消/并发/恢复负面测试、真实构建与设备证据。不得把本文选择当作测试结果。

## Responsibility documents and evidence
{linked}

决策来源为当前所有者授权；外部技术事实及限制见[技术证据](../../research/technical-evidence-2026-09-05.md)。保留原用户来源与历史Git差异；本文不是用户逐字选择每个技术的记录。
'''
  document(path,'DDD-'+num,'decision',title,body)
  rows.append(f'| DDD-{num} | DECIDED / delegated | [{title}](decisions/DDD-{num}-{slug}.md) |')
 older=[]
 for p in sorted((D/'governance/decisions').glob('DDD-*.md')):
  num=int(p.name[4:8])
  if num<13:
   status='ARCHIVE：被后续决定承接' if num<=7 else '保留CANON，具体未决实现见DDD-0015–0017'
   older.append(f'| DDD-{num:04d} | {status} | [{p.stem}](decisions/{p.name}) |')
   if num<=7:
    append(p.relative_to(D).as_posix(),'## 2026-09-05 disposition / 历史状态\n\n本文件保留当时的选项和理由，旧OPEN不是当前未决入口。产品/装备/技术/制作问题已由DDD-0013–0018决定，人物与完整故事仍通过OWNER-01审阅；请读[当前决策登记](../decision-register.md)。不再按本文旧日期或未批准推荐直接实施。')
   else:
    append(p.relative_to(D).as_posix(),'## 2026-09-05 implementation closure\n\n本文件已确认的引擎/内容/命令/60Hz/复制合同继续有效；当时列出的provider、回溯、迁移算法、脚本、旧hash和UI未决项现在由DDD-0015–0017与其责任文档关闭。历史段落用于追溯，不要求重复询问所有者；具体TEST尚未执行。')
 document('governance/decision-register.md','GOV-DECISIONS','governance','当前决策登记与覆盖关系','''这是一份当前索引，不是另一个复制GDD。每条决定的理由、替代方案、边界、影响、重审条件和测试在DDD中。历史DEC-001…问题账完整保存在[定稿前历史](history/decision-register-before-finalization-2026-09-05.md)，不要把其中旧OPEN当现行要求。

| 决定 | 当前状态 | 责任记录 |
|---|---|---|
'''+ '\n'.join(rows+older)+'''

## 旧问题如何关闭

产品单/双模式、固定配装/槽位、角色Active绑定、枪械/Staff、有限Energy、改装与Fusion：DDD-0013/0014。网络Provider、回溯算法、选主/快照、存档格式：DDD-0015/0016。脚本语言、Native政策、完整Mod Manager、Workshop旧hash、公开TC时间：DDD-0017。Demo、阶段范围、资产生产、语言、交接、排期：DDD-0018。数值采用测试参数和内容试制卡，不以“未实测”要求新手用户选。

## 仍需所有者的决定

仅[OWNER-01–04](owner-decisions.md)：故事/人物、钱与账户/商业承诺、最终视听身份、明确需求缩减。创作REVIEW没有被本次技术授权偷换成CANON。未来Descent/未发布脚本等FUTURE条目只在实际启动该范围时重开，不阻塞基础游戏。

## 改变决定

新信息使决定失效时增加新的DDD并在责任文档同步修改；记录被否决方案和证据，不删除坏消息，不把聊天当唯一记录。普通架构可重构，未发布旧运行时可移除；已发布用户进度需明确迁移。''',deps=['owner-decisions.md','authoring-guide.md'])

 append('sources/evidence-register.md','## '+SOURCE+'\n\n类型：用户直接授权；日期：2026-09-05；适用范围：本次GitHub游戏文档定稿与后续普通设计/技术裁决。\n\n用户请求查看BREACH ECHO仓库、使用skills、完成整个游戏文档，说明自己不懂制作或编码游戏，要求助手选择明确赢家而非每件事等待本人；确实需要本人决定的事项保留。用户要求名称合理、后续参与者能完整读取与接手。\n\nDDD-0013–0018中的具体技术/系统选择是助手在此授权下的决定，不是用户曾逐字说过。没有授权花钱、公开发布游戏、替其同意合同或伪造创作批准。')
 append('templates/system-spec.md','## 授权后的写作补充\n\n普通已裁决选择可标DECIDED并链接DDD，不必保留PROPOSED等待所有者技术投票。参数选TEST初值并给单位/测量条件；只有真正创作/商业/明确需求变更指向owner-decisions。stage用BASELINE/REVIEW/FUTURE/ARCHIVE/TEMPLATE，不能把BASELINE当游戏已实现。')
 append('templates/content-spec.md','## 当前生产补充\n\n内容必须声明Operation/Lab/FUTURE的准入，数值TEST不等于发布完成；购入/AI来源记录provenance和许可，禁止未经允许提交原资源到本公开仓库。普通已选行为可DECIDED，人物等创作身份按OWNER-01审阅。')

 document('governance/finalization-review.md','GOV-FINALIZATION-REVIEW','governance','定稿审阅、覆盖范围与未完成边界','''## 审阅范围

本轮对原55份Markdown作清单登记并对当前职责文档进行产品/玩法、架构/生产、内容/安全、交接/完整性四轮同一助手审阅；不是四名外部专家或独立盲审。两份原始source快照保持byte-for-byte不变。具体替换/采纳规则ID、重命名和源hash在finalization-baseline.json中。

## 解决的问题

旧双模式首发与Operation焦点冲突；两工具/人物Signature与固定配装冲突；无限Energy/Relic/Fusion与资源管理冲突；网络Provider/恢复协议/旧hash未定；Mod UI与脚本安全未定；Demo与长局混用；旧日期和未知预算被误当排程；原README计数过期；缺新手入口和完整交接。

## 文件改名

build-algebra→modifications-and-effects：解释当前修改/效果而非数学黑箱。relics-and-fusions→modification-catalog：当前目录首先服务Operation，未来卡保留分区。character-roster-v1→characters：Git负责版本号。brutal-review→risk-register：名称说明维护职责。decisions-and-questions→decision-register：当前只保留可执行决定索引，旧长账归档。其余有清楚职责的名称保留，避免为了重命名而重命名。

## 验证的真实边界

文档validator检查元数据、稳定ID、相对文件链接、登记覆盖、DDD索引、protected source hash与选定矛盾模式；其自测验证能抓到缺文件/重复ID/坏依赖等错误。工具输出及CI是结构检查证据。它不能证明所有语义无误、游戏可玩、经济平衡、网络协议形式正确、模组安全、商业许可已清或Deck达标。

所有游戏构建、设备性能、真正多人/故障注入、用户研究、资产rig和许可个案检查、第三方独立故事盲审均未运行。OWNER-01/02/03保留明确审批，OWNER-04只在需要改变原需求时使用。实施从M0开始，不以文档数量假装已完成游戏。''',deps=['decision-register.md','document-register.md','../production/implementation-handoff.md'])

 # Fix metadata/links in new files too, then create an exhaustive index.
 for p in ROOT.rglob('*.md'):
  if p.relative_to(ROOT).as_posix() in PROTECTED: continue
  t=p.read_text(encoding='utf-8').replace('\n doc_type:', '\ndoc_type:')
  for before,after in RENAMES.items(): t=t.replace(Path(before).name,Path(after).name)
  p.write_text(t,encoding='utf-8')
 document('governance/document-register.md','GOV-DOCUMENT-REGISTER','governance','完整文档登记 / All documents','Generated below.')
 entries=[]
 for p in sorted(ROOT.rglob('*.md')):
  if any(x in p.parts for x in ['.git','artifacts','node_modules','Library']): continue
  t=p.read_text(encoding='utf-8'); meta={}
  if t.startswith('---\n'):
   for line in t.split('---',2)[1].splitlines():
    m=re.match(r'([a-z_]+):\s*(.*)',line)
    if m: meta[m.group(1)]=m.group(2).strip('"')
  title=next((l[2:].strip() for l in t.splitlines() if l.startswith('# ')),p.stem)
  rel=p.relative_to(ROOT).as_posix()
  link=Path(os.path.relpath(p,D/'governance')).as_posix()
  stage=meta.get('stage','ARCHIVE' if rel in PROTECTED else 'ENTRY/SKILL')
  entries.append((rel,f'| `{meta.get("doc_id",rel)}` | {stage} | [{title.replace("|","/")}]({link}) |'))
 body='这份登记列出所有Markdown，包括根入口、项目skill、当前规格、创作审阅、未来设计、历史source和模板；没有依赖聊天记忆的隐藏文档。BASELINE不是游戏实现状态。按角色先读[文档地图](../README.md)，再按需要读所有职责文件。\n\n自动登记文件数：'+str(len(entries))+'。新增/改名后运行`python3 tools/validate_docs.py --reindex`更新本表。\n\n| ID / path | 用途/状态 | 文档 |\n|---|---|---|\n'+'\n'.join(row for _,row in entries)
 document('governance/document-register.md','GOV-DOCUMENT-REGISTER','governance','完整文档登记 / All documents',body,deps=['../README.md'])
 MARKER.write_text(json.dumps({'baseline_date':'2026-09-05','authority':SOURCE,'protected_source_sha256':PROTECTED,'renames':RENAMES,'rule_changes':CHANGES,'game_implementation':'NOT STARTED','game_validation':'NOT RUN','independent_story_review':'NOT RUN'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(f'Finalized {len(entries)} Markdown entries; {len(CHANGES)} explicit rule replacements/adoptions. No game tests claimed.')

if __name__=='__main__': main()
