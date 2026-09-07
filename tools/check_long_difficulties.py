"""五档长局名单与首补前库存的文档算术检查，不模拟生成、AI或战斗。"""
from decimal import Decimal as D, ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP
from itertools import product
import re

from check_enemy_contract import table
from check_standard_run import ROOT, allocate, distribute, read_guns, scaled_initial


def rounded(value, mode):
    return int(value.to_integral_value(rounding=mode))


def initial_roster(base, scale, keep, extras, placements, seats):
    """累计取整基础名单；附加角色使用作者落位序列，不随机补满。"""
    cumulative, previous = [0] * 4, [0] * 4
    result = []
    for row in base:
        cumulative = [a + b for a, b in zip(cumulative, row, strict=True)]
        current = [rounded(D(n) * D(seats) / 4 * (scale if k < 2 else keep),
                           ROUND_CEILING) if k < 3 else n
                   for k, n in enumerate(cumulative)]
        result.append([a - b for a, b in zip(current, previous, strict=True)] + [0] * 5)
        previous = current
    # 结果顺序：逐能、压射、固守、炮塔、缝行、穿线、探讯、破阵、投涌。
    for count, sequence, slot in zip(extras, placements, (2, 4, 5, 6, 7, 8), strict=True):
        for n in range(rounded(D(count) * seats / 4, ROUND_CEILING)):
            result[sequence[n % len(sequence)] - 1][slot] += 1
    return result


def main():
    matrix = (ROOT / "docs/内容/任务/首轮任务难度敌人与配装矩阵.md").read_text(encoding="utf-8")
    parameters = (ROOT / "docs/制作/初始测试参数.md").read_text(encoding="utf-8")
    budget = (ROOT / "docs/制作/标准长局节奏与资源验算.md").read_text(encoding="utf-8")
    scales = table(matrix, "LONG-DIFFICULTY-SCALE ·")
    tiers = table(parameters, "## TP-DIFFICULTY-COMBAT")
    assert [r[0] for r in scales] == [r[0] for r in tiers]
    costs = {name: int(value) for name, value in re.findall(
        r"(Runner|Suppressor|Holder|Scout|Flanker|Lancer|Breacher|Bombard|Sentry Turret)=(\d+)/\d+", parameters)}
    order = ("Runner", "Suppressor", "Holder", "Sentry Turret", "Flanker", "Lancer", "Scout", "Breacher", "Bombard")
    initial_costs = [costs[k] for k in order]
    source_costs = [costs[k] for k in ("Runner", "Suppressor", "Flanker", "Lancer", "Scout", "Breacher", "Bombard")]
    sources = {r[0]: tuple(map(int, r[1:])) for r in table(matrix, "LONG-SOURCE-ROSTER ·")}
    supplies = table(matrix, "LONG-SUPPLY-SCALING ·")
    assert len(sources) == 10 and len(supplies) == 5
    for row, tier in zip(supplies, tiers, strict=True):
        multiplier = D(tier[3])
        assert row[0] == tier[0] and D(row[1]) == multiplier
        assert int(row[2]) == rounded(320 * multiplier, ROUND_HALF_UP)
        assert int(row[3]) == rounded(160 * multiplier, ROUND_HALF_UP)
        assert int(row[4]) == 8
    guns, slots = read_guns()
    pairs = list(product(slots["第一"], slots["第二"]))
    assert len(pairs) == 20
    specifications = (
        ("黑启动", "换流器黑启动任务合同与灰盒规格.md", "BST", "黑启动与货运", 4),
        ("取证", "分布式数据取证任务合同.md", "FORENSICS", "取证覆盖", 3),
        ("货运", "货运线夺回任务合同.md", "FREIGHT", "黑启动与货运", 4),
    )
    reports, inventories, source_cases = [], 0, 0
    for spec, standard_source in zip(specifications, table(budget, "RUN-LOCKED-ROSTER ·"), strict=True):
        name, filename, marker, source_key, first_ammo = spec
        text = (ROOT / "docs/内容/任务" / filename).read_text(encoding="utf-8")
        rows = table(text, marker + "-STANDARD-LONG ·")
        base = [tuple(map(int, r[3:7])) for r in rows]
        assert len(base) == 7
        extras_rows = table(text, marker + "-LONG-DIFFICULTY ·")
        placement_rows = table(text, marker + "-LONG-PLACEMENT ·")
        assert len(placement_rows) == 6
        assert [r[0] for r in placement_rows] == ["额外固守", "缝行", "穿线", "探讯", "破阵", "投涌"]
        placements = [list(map(int, re.findall(r"\d+", r[1]))) for r in placement_rows]
        assert all(seq and all(first_ammo < p <= 7 for p in seq) for seq in placements)
        if name == "取证":
            assert all(placements[k] == [6] for k in (0, 4, 5))
        source_base = int(standard_source[5])
        for scale_row, tier, extra_row in zip(scales, tiers, extras_rows, strict=True):
            difficulty = tier[0]
            assert difficulty == extra_row[0]
            scale, keep = D(scale_row[1]), D(scale_row[2])
            extras = list(map(int, extra_row[1:]))
            assert len(extras) == 6 and all(n >= 0 for n in extras)
            if difficulty in ("Relaxed", "Standard"):
                assert not any(extras)
            if difficulty == "Veteran":
                assert not any(extras[4:])
            four_source = sources[source_key + " / " + difficulty]
            if name == "取证":
                assert not any(four_source[-2:])
            if difficulty in ("Relaxed", "Standard"):
                assert not any(four_source[2:])
            if difficulty == "Veteran":
                assert not any(four_source[-2:])
            passed = []
            for seats in range(1, 5):
                roster = initial_roster(base, scale, keep, extras, placements, seats)
                totals = [sum(r[k] for r in roster) for k in range(9)]
                expected = [rounded(D(sum(r[k] for r in base)) * seats / 4 * (scale if k < 2 else keep),
                                    ROUND_CEILING) for k in range(3)] + [sum(r[3] for r in base)] + [0] * 5
                for k, n in zip((2, 4, 5, 6, 7, 8), extras, strict=True):
                    expected[k] += rounded(D(n) * seats / 4, ROUND_CEILING)
                assert totals == expected and all(n >= 0 for r in roster for n in r)
                if difficulty == "Standard":
                    assert [tuple(r[:4]) for r in roster] == scaled_initial(base, seats)
                if name == "取证":
                    assert not any(roster[6])
                if seats == 4:
                    reports.append([name, difficulty, str(sum(totals)),
                                    str(sum(n * c for n, c in zip(totals, initial_costs, strict=True)))])
                # 来源人数独立于初始人数：验证全部16对，不重写初始账。
                for source_seats in range(1, 5):
                    seat_multiplier = D(("1", "1.5", "2", "2.5")[source_seats - 1])
                    if difficulty == "Standard":
                        source = tuple(map(int, standard_source[source_seats].split("/"))) + (0,) * 5
                    else:
                        source = tuple(rounded(D(n) * seat_multiplier / D("2.5"), ROUND_FLOOR) for n in four_source)
                    cap = rounded(D(source_base) * D(tier[1]) * seat_multiplier, ROUND_HALF_UP)
                    assert sum(n * c for n, c in zip(source, source_costs, strict=True)) <= cap
                    assert (source[1] + source[3] + source[6]) * 4 <= sum(source)
                    if name != "取证":
                        stages = [[n // 4, 3 * n // 4 - n // 4, n - 3 * n // 4]
                                  if k < 5 else [0, 0, n] for k, n in enumerate(source)]
                        assert all(sum(parts) == n for parts, n in zip(stages, source, strict=True))
                    source_cases += 1
                mistake = tuple(min(roster[1][k], rounded(D(n) * scale * seats / 4, ROUND_CEILING))
                                for k, n in enumerate((8, 1))) + (0, 0)
                players = distribute((mistake,), seats)
                passing = 0
                for pair in pairs:
                    start, cap, refill, target_costs = [tuple(guns[g][k] for g in pair) for k in range(4)]
                    passing += all(allocate(start, cap, refill, target_costs, player, (0,)) == 0 for player in players)
                    inventories += 1
                passed.append(passing)
            reports[-1].append("/".join(map(str, passed)))
    print("| 任务 | 难度 | 四席初始实体 | 初始威胁点 | 首补前一次误响：库存有解配装数（1/2/3/4席，各20） |")
    for row in reports:
        print("| " + " | ".join(row) + " |")
    if "LONG-COMPUTED-RESULTS ·" in budget:
        assert table(budget, "LONG-COMPUTED-RESULTS ·") == reports, "五档派生报告需要同步"
    # 负例只证明算术约束能辨别这些错误，不冒充网络迁移或真实入口测试。
    assert allocate((0, 0), (10, 10), (5, 5), ((2,), (2,)), ((0,), ()), (0, 1)) == 1
    assert not (2 * 4 <= 5), "五个单位中两个远程必须超限"
    assert not (costs["Breacher"] <= 4), "剩余四点不能提交破阵体"
    assert rounded(D("1.5"), ROUND_HALF_UP) == 2
    print(f"PASS：60组初始名单、{source_cases}组独立人数来源账、{inventories}组首补前双枪条件；医疗/资源表与3项负例。")
    print("库存有解不是实战成功率；未检查完整混编火力、实体入口、批次调度或追击汇合。生成Seed 0，试玩0。")


if __name__ == "__main__":
    main()
