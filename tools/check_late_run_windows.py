"""文档驱动的高难混编库存与动作算术；不是战斗、导航或通关模拟。"""
from decimal import Decimal as D
from math import ceil, prod
import re

from check_enemy_contract import table
from check_long_difficulties import initial_roster
from check_standard_run import ROOT, allocate, read_guns


def read(relative):
    return (ROOT / relative).read_text(encoding="utf-8")


def main():
    study = read("docs/制作/高难后段火力补给与行动窗口验算.md")
    combat = read("docs/内容/装备/战斗原型数值.md")
    matrix = read("docs/内容/任务/首轮任务难度敌人与配装矩阵.md")
    parameters = read("docs/制作/初始测试参数.md")
    guns, slots = read_guns()
    hp = {r[0]: int(r[1].split("/")[0]) for r in table(combat, "## 八类敌人的测试参数")}
    heavy = {r[0]: r for r in table(combat, "COMBAT-HEAVY-BREAKPOINTS")}
    # 与共享名单函数相同：R/S/H/T/F/L/Scout/Breacher/Bombard。
    for row in table(combat, "## 枪械基础与资源"):
        name = row[0]
        charged = "→" in row[2]
        damage = float(row[2].split("→")[-1]) if charged else prod(
            map(float, row[2].replace("颗", "").split("×")))
        label = name + "（满蓄直击）" if charged else name
        hits = [ceil(hp[k] / damage) for k in ("Flanker", "Lancer", "Scout")]
        hits += [int(heavy[label][2].split(" / ")[2]), ceil(hp["Bombard"] / damage)]
        extra = tuple((ceil(n * 5 / 4) + int(name in ("突击步枪", "速射脉冲枪")))
                      * (4 if charged else 1) for n in hits)
        start, cap, refill, costs = guns[name]
        guns[name] = (start, cap, refill, costs + extra)

    teams = {}
    for label, seat, primary, secondary, *_ in table(study, "LATE-LOADOUTS ·"):
        assert primary in slots["第一"] and secondary in slots["第二"]
        group = teams.setdefault(label, [])
        assert int(seat) == len(group) + 1
        group.append((primary, secondary))
    assert all(len(group) == 4 for group in teams.values()) and len(teams) == 2
    assignments = {}
    for row in table(study, "LATE-ASSIGNMENT ·"):
        sequences = [tuple(int(n) - 1 for n in re.findall(r"\d+", cell)) for cell in row[1:]]
        assert len(sequences) == 8 and all(s and all(0 <= n < 4 for n in s) for s in sequences)
        assignments[row[0]] = sequences[:3] + [()] + sequences[3:]
    assert set(assignments) == set(teams)
    scales = {r[0]: (D(r[1]), D(r[2])) for r in table(matrix, "LONG-DIFFICULTY-SCALE ·")}
    fixed = {r[0]: D(r[1]) for r in table(matrix, "LONG-SUPPLY-SCALING ·")}
    sources = {r[0]: tuple(map(int, r[1:])) for r in table(matrix, "LONG-SOURCE-ROSTER ·")}
    specs = (
        ("黑启动", "换流器黑启动任务合同与灰盒规格.md", "BST", "黑启动与货运", 3, 5, 4),
        ("取证补全并覆盖", "分布式数据取证任务合同.md", "FORENSICS", "取证覆盖", 2, 4, 3),
        ("全吞吐货运", "货运线夺回任务合同.md", "FREIGHT", "黑启动与货运", 3, 5, 4),
    )
    reports, tested, cases = [], 0, []
    for name, filename, marker, source_key, first, second, late_start in specs:
        task = read("docs/内容/任务/" + filename)
        base = [tuple(map(int, r[3:7])) for r in table(task, marker + "-STANDARD-LONG ·")]
        extras = {r[0]: tuple(map(int, r[1:])) for r in table(task, marker + "-LONG-DIFFICULTY ·")}
        placements = [list(map(int, re.findall(r"\d+", r[1]))) for r in table(task, marker + "-LONG-PLACEMENT ·")]
        for difficulty in ("Veteran", "Nightmare", "Cataclysm"):
            roster = initial_roster(base, *scales[difficulty], extras[difficulty], placements, 4)
            initial = [[0] * 9 for _ in range(7)]
            for k, n in enumerate((8, 1)):
                initial[1][k] = min(roster[1][k], ceil(n * scales[difficulty][0]))
            for phase in range(late_start, 7):
                initial[phase] = roster[phase].copy()
            assert all(initial[p][k] <= roster[p][k] for p in range(7) for k in range(9))
            assert all(row[3] == 0 for row in initial), "本对照不含炮塔击杀或收益"
            stages = [row.copy() for row in initial]
            source = sources[source_key + " / " + difficulty]
            for slot, count in zip((0, 1, 4, 5, 6, 7, 8), source, strict=True):
                if marker == "FORENSICS":
                    stages[late_start][slot] += count
                elif slot in (7, 8):
                    stages[6][slot] += count
                else:
                    cumulative = (0, count // 4, 3 * count // 4, count)
                    for part in range(3):
                        stages[4 + part][slot] += cumulative[part + 1] - cumulative[part]
            assert sum(map(sum, stages)) - sum(map(sum, initial)) == sum(source)
            for label, team in teams.items():
                players = [[[] for _ in range(7)] for _ in range(4)]
                turn = [0] * 9
                for phase, counts in enumerate(stages):
                    for target, count in enumerate(counts):
                        sequence = assignments[label][target]
                        for _ in range(count):
                            player = sequence[turn[target] % len(sequence)]
                            players[player][phase].append(target)
                            turn[target] += 1
                assert sum(len(stage) for player in players for stage in player) == sum(map(sum, stages))
                results = []
                for plan in ((1, 1), (1, 0), (0, 1)):
                    supplies = [D(0)] * 7
                    supplies[first] = fixed[difficulty] + plan[0]
                    supplies[second] = D(plan[1])
                    failures = []
                    for pair, targets in zip(team, players, strict=True):
                        start, cap, refill, costs = [tuple(guns[g][k] for g in pair) for k in range(4)]
                        fail = allocate(start, cap, refill, costs,
                                        tuple(tuple(stage) for stage in targets), tuple(supplies))
                        if fail:
                            failures.append(fail)
                    cases.append((name, difficulty, label, plan, tuple(team),
                                  tuple(tuple(tuple(s) for s in p) for p in players),
                                  tuple(supplies), guns))
                    results.append("有库存解" if not failures else f"第{min(failures)}段缺口")
                    tested += 1
                reports.append([name, difficulty, label, *results])
    for row in reports:
        print("| " + " | ".join(row) + " |")
    if "LATE-COMPUTED ·" in study:
        assert table(study, "LATE-COMPUTED ·") == reports, "高难混编派生结果未同步"

    # 小数权益不能发射一整发；未来Pod、跨槽余额、容量上限的反例。
    cost = ((1,), (1,))
    assert allocate((0, 0), (5, 5), (1, 1), cost, ((0,),), (D("0.75"),)) == 1
    assert allocate((0, 0), (5, 5), (1, 1), cost, ((0,), ()), (D(0), D(1))) == 1
    assert allocate((D("0.5"), D("0.5")), (5, 5), (1, 1), cost, ((0,),), (D(0),)) == 1
    assert allocate((0, 0), (1, 1), (10, 10), ((2,), (2,)), ((0,),), (D(1),)) == 1
    # 参数直接从责任表取，时序仅做下界，不能当作敌人模拟。
    params = {r[0].split(" / ")[0]: r[1] for r in table(parameters, "除表中明确")}
    work = D(re.match(r"[\d.]+", params["TP-EXTRACTION-WORK"])[0])
    rates = [D(x) for x in re.findall(r"\d人([\d.]+)", params["TP-EXTRACTION-RATE"])]
    revive = D(re.match(r"[\d.]+", params["TP-REVIVE"])[0])
    walk = D(params["TP-MOVE"].split("/")[0].strip())
    rescue = {r[0]: r[1] for r in table(parameters, "## TP-RESCUE-ACTIONS")}
    pickup = D(re.search(r"搬起([\d.]+)s", rescue["搬起/放下伤员"])[1])
    grace = D(re.search(r"([\d.]+)s", params["TP-GRACE"])[1])
    assert len(rates) == 4 and all(r > 0 for r in rates)
    delivery = table(read("docs/玩法/资源回收额度与公共物资.md"), "ECO-DELIVERY-TIMING ·")
    stages_seconds = [D(r[1].rstrip("s")) for r in delivery[:3]]
    economy = read("docs/玩法/资源回收额度与公共物资.md").split("ECO-PACK-CONSERVATION ·", 1)[1]
    use = D(re.search(r"使用包为([\d.]+)s", economy)[1])
    total = sum(stages_seconds) + use
    sniper = next(r for r in table(combat, "## 枪械基础与资源") if r[0] == "重型狙击步枪")
    chamber = D(re.search(r"空仓额外在(\d+)%", combat)[1]) / 100
    reload_time = D(sniper[5].rstrip("s")) * chamber
    move = D(6) / walk
    # 搬运半速出血是生命责任合同；本样例取无受击。
    assert "Carry按半速消耗" in read("docs/玩法/生存倒地与失败恢复.md")
    print(f"窗口下界：新点{total}s；旧点{total-stages_seconds[0]}s；搬6m后救{pickup+move+revive}s；出血消耗{pickup+move/2+revive}s。")
    print(f"空仓重狙可取消换弹{reload_time}s，大于起身保护{grace}s；普通扫描60Hz tick数：{[ceil(work/r*60) for r in rates]}。")
    assert reload_time > grace, "若参数改变，应重审对应风险而非静默保留结论"
    assert work >= 8
    print(f"分段扫描：{8+5+(work-8*rates[0])/rates[1]}s（含5s无人守圈）。")
    print(f"PASS：{tested}个固定四席分工库存条件已复算（允许明确缺口），小数/未来/槽位/容量负例通过。生成Seed 0，试玩0。")
    return cases


if __name__ == "__main__":
    main()
