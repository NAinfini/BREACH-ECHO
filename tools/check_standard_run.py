"""标准长局有限库存检查；无生成、战斗或玩家模拟，不输出通关概率。"""
from functools import lru_cache
from itertools import product
from math import ceil, prod, floor
from pathlib import Path
import re

from check_enemy_contract import table

ROOT = Path(__file__).resolve().parents[1]


def pareto(states):
    best = -1
    result = set()
    for a, b in sorted(states, reverse=True):
        if b > best:
            result.add((a, b))
            best = b
    return result


@lru_cache(maxsize=None)
def allocate(start, cap, refill, costs, stages, supplies):
    """只向前领取，每目标交给一个槽；保留所有互不支配的剩余库存。"""
    states = {start}
    for index, targets in enumerate(stages):
        states = pareto({tuple(min(cap[s], state[s] + supplies[index] * refill[s])
                               for s in range(2)) for state in states})
        for target in targets:
            following = set()
            for state in states:
                for slot in range(2):
                    cost = costs[slot][target]
                    if state[slot] >= cost:
                        remaining = list(state)
                        remaining[slot] -= cost
                        following.add(tuple(remaining))
            states = pareto(following)
            if not states:
                return index + 1
    return 0


def scaled_initial(rows, seats):
    previous = [0] * 4
    cumulative = [0] * 4
    result = []
    for row in rows:
        cumulative = [a + b for a, b in zip(cumulative, row)]
        scaled = [ceil(x * seats / 4) if k < 3 else x
                  for k, x in enumerate(cumulative)]
        result.append(tuple(a - b for a, b in zip(scaled, previous)))
        previous = scaled
    return result


def distribute(stages, seats):
    result = [[[] for _ in stages] for _ in range(seats)]
    turn = 0
    for phase, counts in enumerate(stages):
        for target, count in enumerate(counts):
            for _ in range(count):
                result[turn % seats][phase].append(target)
                turn += 1
    return [tuple(tuple(stage) for stage in player) for player in result]


def read_guns():
    """从唯一武器表读取库存与80%命中体部成本，供静态预算检查共用。"""
    combat = (ROOT / "docs/内容/装备/战斗原型数值.md").read_text(encoding="utf-8")
    review = {r[0]: r for r in table(combat, "### 同条件击杀与补给")}
    heavy = {r[0]: r for r in table(combat, "COMBAT-HEAVY-BREAKPOINTS")}
    turret_hp = int(next(r[1].split("HP")[0] for r in table(combat, "COMBAT-FACILITY-PROFILE")
                         if "炮塔" in r[0]))
    guns, slots = {}, {"第一": [], "第二": []}
    for row in table(combat, "## 枪械基础与资源"):
        name = row[0]
        mag, reserve = map(int, row[3].split(" / "))
        refill = int(row[7])
        charged = "→" in row[2]
        label = name + "（满蓄直击）" if charged else name
        damage = float(row[2].split("→")[-1]) if charged else prod(
            map(float, row[2].replace("颗", "").split("×")))
        hits = [int(review[label][1].split(" / ")[0]),
                int(review[label][2].split(" / ")[0]),
                int(heavy[label][1].split(" / ")[2]), ceil(turret_hp / damage)]
        waste = int(name in ("突击步枪", "速射脉冲枪"))
        costs = tuple((ceil(h * 5 / 4) + waste) * (4 if charged else 1) for h in hits)
        guns[name] = (mag + refill, mag + reserve, refill, costs)
        slots[row[1].split(" / ")[0]].append(name)
    return guns, slots


def main():
    guns, slots = read_guns()
    pairs = list(product(slots["第一"], slots["第二"]))
    assert len(pairs) == 20
    specifications = [
        ("黑启动", "换流器黑启动任务合同与灰盒规格.md", "BST", (100, 123, 21), 3, 5),
        ("取证", "分布式数据取证任务合同.md", "FORENSICS", (108, 120, 24), 2, 4),
        ("货运", "货运线夺回任务合同.md", "FREIGHT", (94, 112, 20), 3, 5),
    ]
    budget_doc = (ROOT / "docs/制作/标准长局节奏与资源验算.md").read_text(encoding="utf-8")
    source_rows = table(budget_doc, "RUN-LOCKED-ROSTER ·")
    assert len(source_rows) == 3
    profiles = {}
    for (name, filename, marker, expected, first, second), source in zip(specifications, source_rows, strict=True):
        assert source[0].startswith(name), "来源名单必须对应正确任务"
        text = (ROOT / "docs/内容/任务" / filename).read_text(encoding="utf-8")
        rows = table(text, marker + "-STANDARD-LONG ·")
        initial = [tuple(map(int, r[3:7])) for r in rows]
        assert len(initial) == 7
        quantity = sum(map(sum, initial))
        points = sum(sum(n * c for n, c in zip(r, (1, 2, 4, 3))) for r in initial)
        groups = sum(int(r[7]) for r in rows)
        assert (quantity, points, groups) == expected
        roster = [tuple(map(int, r.split("/"))) for r in source[1:5]]
        base = int(source[5])
        authored = text.split(marker + "-STANDARD-LONG ·", 1)[1]
        assert int(re.search(r"基础(\d+)点", authored)[1]) == base
        assert tuple(map(int, re.search(r"候选(?:名单为)?(\d+)逐能\+(\d+)压射", authored).groups())) == roster[3]
        for seats, (r, s) in enumerate(roster, 1):
            assert r + 2 * s == floor(base * (1, 1.5, 2, 2.5)[seats - 1] + .5)
            assert 0 <= s / (r + s) <= .25
            scaled = scaled_initial(initial, seats)
            assert sum(x[3] for x in scaled) == sum(x[3] for x in initial)
        profiles[name] = (initial, roster, first, second)
        print(f"名单：{name}，四席初始{quantity}体/{points}点/{groups}群；来源{roster}")
    # 起始枪战集合以责任文档RUN-PATHS为输入；自动检查不超实际阶段名单。
    prepared = {4: (4, 0, 0, 0), 5: (4, 0, 1, 0), 6: (4, 1, 0, 0)}
    once = {1: (8, 1, 0, 0)}
    cases = [
        ("黑启动/准备", "黑启动", prepared, True),
        ("黑启动/一次失误", "黑启动", prepared | once, True),
        ("黑启动/连续失误", "黑启动", None, True),
        ("取证/准备", "取证", {}, False),
        ("取证/一次失误", "取证", once, False),
        ("取证/连续失误并覆盖", "取证", None, True),
        ("货运隔离/准备", "货运", {}, False),
        ("货运隔离/一次失误", "货运", once, False),
        ("货运吞吐/准备", "货运", prepared, True),
        ("货运吞吐/连续失误", "货运", None, True),
    ]
    plans = ((1, 1), (1, 0), (0, 1))
    tested = 0
    print("| 路线 | 弹药+弹药：1/2/3/4席 | 弹药+医疗 | 医疗+弹药 |")
    reports = []
    for label, mission, selected, enabled in cases:
        initial, sources, first, second = profiles[mission]
        counts = [[] for _ in plans]
        failures = []
        for seats in range(1, 5):
            initial_n = scaled_initial(initial, seats)
            stages = [list(r) for r in initial_n] if selected is None else [
                [min(r[k], ceil(selected.get(index, (0,) * 4)[k] * seats / 4))
                 for k in range(4)] for index, r in enumerate(initial_n)]
            assert all(stages[i][k] <= initial_n[i][k] for i in range(7) for k in range(4))
            before = sum(map(sum, stages))
            if enabled:
                if mission == "取证":
                    for k in range(2):
                        stages[1][k] += sources[seats - 1][k]
                else:
                    for k, count in enumerate(sources[seats - 1]):
                        cumulative = [0, count // 4, 3 * count // 4, count]
                        for phase in range(3):
                            stages[4 + phase][k] += cumulative[phase + 1] - cumulative[phase]
            assert sum(map(sum, stages)) - before == (sum(sources[seats - 1]) if enabled else 0)
            players = distribute(stages, seats)
            for plan_index, plan in enumerate(plans):
                supplies = [0] * 7
                supplies[first] = 1 + plan[0]
                supplies[second] = plan[1]
                passes = 0
                for pair in pairs:
                    # 同配装队只检验固定轮转分工，不宣称覆盖所有混编队/最优团队分工。
                    start, cap, refill, costs = [tuple(guns[g][k] for g in pair) for k in range(4)]
                    failure = [allocate(start, cap, refill, costs, player, tuple(supplies)) for player in players]
                    passes += not any(failure)
                    if any(failure):
                        failures.append(min(f for f in failure if f))
                        if seats == 1 and selected == prepared and plan_index == 1:
                            print(f"单人准备路线缺口：{label}，{' + '.join(pair)}，第{min(f for f in failure if f)}段，弹药+医疗。")
                    tested += 1
                counts[plan_index].append(passes)
        row = [label] + ["/".join(map(str, c)) for c in counts]
        reports.append(row)
        print("| " + " | ".join(row) + " |")
        if failures:
            print(f"失败定位：{label}最早第{min(failures)}段；是固定分工库存无解，不是实战必败。")
    # 前向库存和槽位隔离的负例，避免未来补给或溢出弹药制造伪通过。
    costs = ((2,), (2,))
    assert allocate((0, 0), (10, 10), (5, 5), costs, ((0,), ()), (0, 1)) == 1
    assert allocate((0, 0), (10, 10), (5, 5), costs, ((0,), ()), (1, 0)) == 0
    assert allocate((1, 1), (10, 10), (5, 5), costs, ((0,),), (0,)) == 1
    assert allocate((0, 0), (1, 1), (5, 5), costs, ((0,),), (1,)) == 1
    assert pareto({(1, 2), (2, 2), (3, 1)}) == {(2, 2), (3, 1)}
    if "RUN-COMPUTED-RESULTS ·" in budget_doc:
        assert table(budget_doc, "RUN-COMPUTED-RESULTS ·") == reports, "长局派生结果未同步"
    print(f"PASS：{tested}个队伍条件，20种同配装双槽×1至4席×10路线×3种Pod；前向库存负例通过。生成Seed 0，试玩0。")


if __name__ == "__main__":
    main()
