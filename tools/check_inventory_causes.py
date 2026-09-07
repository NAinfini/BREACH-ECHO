"""复算库存缺口成因；只重分配现有目标，不实现游戏或改变参数。"""
from contextlib import redirect_stdout
from io import StringIO
from itertools import permutations

from check_standard_run import allocate, read_guns, pareto, ROOT, scaled_initial
from check_enemy_contract import table
from check_late_run_windows import main as late_cases


def states_after(start, cap, refill, costs, stages, supplies):
    """与原求解器同样的双槽前向状态，用于解释末段剩余量。"""
    states = {start}
    traces = []
    for targets, supply in zip(stages, supplies, strict=True):
        states = pareto({tuple(min(cap[s], a[s] + supply * refill[s])
                               for s in range(2)) for a in states})
        for target in targets:
            following = set()
            for state in states:
                for slot in range(2):
                    if state[slot] >= costs[slot][target]:
                        remaining = list(state)
                        remaining[slot] -= costs[slot][target]
                        following.add(tuple(remaining))
            states = pareto(following)
        traces.append(sorted(states))
    assert (not states) == bool(allocate(start, cap, refill, costs, stages, supplies))
    return traces


def solo():
    guns, _ = read_guns()
    pair = ("低声针束步枪", "蓄力爆破枪")
    args = [tuple(guns[g][k] for g in pair) for k in range(4)]
    budget = (ROOT / "docs/制作/标准长局节奏与资源验算.md").read_text(encoding="utf-8")
    sources = table(budget, "RUN-LOCKED-ROSTER ·")
    task = (ROOT / "docs/内容/任务/换流器黑启动任务合同与灰盒规格.md").read_text(encoding="utf-8")
    initial = scaled_initial([tuple(map(int, r[3:7])) for r in
                              table(task, "BST-STANDARD-LONG ·")], 1)
    stages = [[] for _ in range(7)]
    for phase, counts in ((4, (1, 0, 0, 0)), (5, (1, 0, 1, 0)), (6, (1, 1, 0, 0))):
        row = [min(n, initial[phase][k]) for k, n in enumerate(counts)]
        for target, count in enumerate(map(int, sources[0][1].split("/"))):
            cumulative = (0, count // 4, 3 * count // 4, count)
            row[target] += cumulative[phase - 3] - cumulative[phase - 4]
        stages[phase] = tuple(t for t, n in enumerate(row) for _ in range(n))
    stages = tuple(tuple(s) for s in stages)
    freight = (ROOT / "docs/内容/任务/货运线夺回任务合同.md").read_text(encoding="utf-8")
    freight_initial = scaled_initial([tuple(map(int, r[3:7])) for r in
                                     table(freight, "FREIGHT-STANDARD-LONG ·")], 1)
    for phase, counts in ((4, (1, 0, 0, 0)), (5, (1, 0, 1, 0)), (6, (1, 1, 0, 0))):
        assert [min(n, freight_initial[phase][k]) for k, n in enumerate(counts)] == [
            min(n, initial[phase][k]) for k, n in enumerate(counts)]
    assert sources[0][1] == sources[2][1], "两任务来源不再相同时需分别复算"
    print("单人实际逐阶段目标", stages)
    for name, supplies in (("弹药/医疗", (0, 0, 0, 2, 0, 0, 0)),
                           ("医疗/弹药", (0, 0, 0, 1, 0, 1, 0)),
                           ("弹药/弹药", (0, 0, 0, 2, 0, 1, 0))):
        fail = allocate(*args, stages, supplies)
        print("单人", name, "缺口阶段", fail,
              "第六段后可行余量", states_after(*args, stages, supplies)[5])
        # 一次只减少一种有实体身份的末段目标；是准备收益敏感性，非免费扣怪。
        witnesses = []
        for target in (0, 1):
            final = list(stages[-1])
            for count in range(final.count(target) + 1):
                revised = stages[:-1] + (tuple(final),)
                if not allocate(*args, revised, supplies):
                    witnesses.append((target, count))
                    break
                if target in final:
                    final.remove(target)
        print("末段少处理目标的最小条件（逐能0/压射1）", witnesses)
        # 从第六段真实可行余量测敏感性，不伪装成游戏新增补给。
        additions = []
        frontier = states_after(*args, stages, supplies)[5]
        for slot in range(2):
            for extra in range(args[1][slot] + 1):
                candidates = [tuple(min(args[1][s], state[s] + (extra if s == slot else 0))
                                    for s in range(2)) for state in frontier]
                if any(not allocate(state, *args[1:], (stages[-1],), (0,))
                       for state in candidates):
                    additions.append((pair[slot], extra))
                    break
        print("只增加一种弹药时的末段最小余量增量（非参数修改）", additions)


def main():
    solo()
    with redirect_stdout(StringIO()):
        cases = late_cases()
    totals = [0, 0, 0]
    for mission, difficulty, group, plan, team, players, supplies, guns in cases:
        def failures(order):
            result = []
            for seat, source in enumerate(order):
                args = [tuple(guns[g][k] for g in team[seat]) for k in range(4)]
                result.append(allocate(*args, players[source], supplies))
            return result
        original = failures((0, 1, 2, 3))
        if not any(original):
            totals[0] += 1
            continue
        witness = next((order for order in permutations(range(4))
                        if not any(failures(order))), None)
        totals[1 if witness else 2] += 1
        print(mission, difficulty, group, plan, "各席缺口", original,
              "现有目标职责换手见证", tuple(i + 1 for i in witness) if witness else "24种整体换手仍无解")
    assert sum(totals) == 54
    doc = (ROOT / "docs/制作/高难后段火力补给与行动窗口验算.md").read_text(encoding="utf-8")
    rows = table(doc, "LATE-CAUSE-RESULT ·")
    assert [int(row[1]) for row in rows] == totals, "职责换手派生汇总未同步"
    print("54条件：原分工有解/仅换射手后有解/仍未找到解", totals)
    print("目标数量、类型、阶段、弹药、补给、命中及甲面成本均未改变。")
    print("整体换手没有枚举所有逐目标混合分工，未找到不等于全队无解；没有空间/时间/战斗验证。")


if __name__ == "__main__":
    main()
