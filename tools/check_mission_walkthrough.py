"""复算三任务作者样例的静态兵力与火力账，不模拟命中、导航或通关。"""
from collections import Counter
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path
import re

from check_enemy_contract import table


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def main():
    walk = read("docs/制作/首轮配装三任务走读与风险验收.md")
    combat = read("docs/内容/装备/战斗原型数值.md")
    params = read("docs/制作/初始测试参数.md")
    matrix = read("docs/内容/任务/首轮任务难度敌人与配装矩阵.md")
    names = dict(zip(
        ("Runner", "Suppressor", "Holder", "Scout", "Flanker", "Lancer", "Breacher", "Bombard",
         "Sentry Turret", "Warden Robot", "Maintenance Drone"),
        ("逐能体", "压射体", "固守体", "探讯体", "缝行体", "穿线体", "破阵体", "投涌体",
         "哨戒炮塔", "守备机", "维护机"), strict=True))
    costs = {zh: int(re.search(re.escape(en) + r"=(\d+)/(\d+)", params)[1])
             for en, zh in names.items()}
    hp = {names[r[0]]: D(r[1].split("/")[0].strip())
          for r in table(combat, "## 八类敌人的测试参数")}
    hp.update({r[0]: D(re.search(r"\d+", r[1])[0])
               for r in table(combat, "COMBAT-FACILITY-PROFILE")})
    armor = {r[0].split(" / ")[0]: D(r[1])
             for r in table(combat, "COMBAT-ENEMY-ARMOR")}

    guns = table(combat, "## 枪械基础与资源")
    assert "后备等于该枪一份Ammo的补充量" in combat
    power = {}
    endurance = {}
    slots = {}
    for r in guns:
        magazine, reserve = map(int, r[3].split(" / "))
        refill = int(r[7])
        reserve = min(reserve, refill)
        assert 0 < refill <= int(r[3].split(" / ")[1])
        damage = r[2].replace("颗", "")
        if "→" in damage:
            # 本报告明确只取满蓄单体，不将范围收益重复算入。
            cost = int(re.search(r"每发1→(\d+)单位", r[6])[1])
            value = D(damage.split("→")[1]) * ((magazine + reserve) // cost)
            endurance[r[0]] = [
                D(damage.split("→")[1]) * ((magazine + reserve + refill * n) // cost)
                for n in range(4)]
        else:
            value = D(1)
            for part in damage.split("×"):
                value *= D(part)
            endurance[r[0]] = [value * (magazine + reserve + refill * n) for n in range(4)]
            value *= magazine + reserve
        power[r[0]] = value
        slots[r[0]] = r[1].split(" / ")[0]
    aliases = {"重型狙击": "重型狙击步枪", "线圈穿透": "线圈穿透步枪",
               "低声针束": "低声针束步枪", "速射脉冲": "速射脉冲枪",
               "泵动霰弹": "泵动霰弹枪", "蓄力爆破": "蓄力爆破枪"}
    teams = Counter()
    supplies = {}
    coverage = set()
    for r in table(walk, "## 三组代表配装"):
        mission = re.sub(r"\d+$", "", r[0])
        pair = [aliases.get(name, name) for name in r[1].split(" + ")]
        assert len(pair) == 2 and [slots[n] for n in pair] == ["第一", "第二"], r
        teams[mission] += sum(power[n] for n in pair)
        sums = supplies.setdefault(mission, [D(0)] * 4)
        for n in range(4):
            sums[n] += sum(endurance[gun][n] for gun in pair)
        coverage.update(pair)
    assert coverage == set(power) and len(coverage) == 9
    staged = table(walk, "LOADOUT-SUPPLY-PREFIX ·")
    assert len(staged) == 3
    for mission, amounts in supplies.items():
        print(f"{mission}累计供给：{amounts}")
    for row in staged:
        assert list(map(D, row[1:])) == supplies[row[0]], row
    efficiencies = {D(r[7]) / D(r[3].split(" / ")[1]) for r in guns}
    assert len(efficiencies) > 1, "逐枪补给不可退回统一后备比例"
    derived = table(combat, "### 补给效率的设计依据")
    assert {r[0]: D(r[1]) for r in derived} == {
        gun: values[1] - values[0] for gun, values in endurance.items()}

    fixtures = table(walk, "### 三份功能短图兵力账")
    assert len(fixtures) == 3
    reports = table(walk, "LOADOUT-MISSION-RESOURCE-AUDIT ·")
    assert len(reports) == 3
    source_rows = table(matrix, "四个有效Seat时，三份首轮来源的上限为")
    source_efficiency = max(hp[n] / costs[n] for n in ("逐能体", "压射体"))
    initial_markers = ("MATRIX-BLACKSTART-001", "MATRIX-FORENSICS-001", "MATRIX-FREIGHT-001")
    for index, row in enumerate(fixtures):
        roster = dict(zip(("逐能体", "压射体", "固守体", "缝行体", "哨戒炮塔"),
                          map(int, row[1:6]), strict=True))
        count = sum(roster.values())
        points = sum(costs[n] * c for n, c in roster.items())
        assert [count, points] == list(map(int, row[7:9])), row
        standard = next(r for r in table(matrix, initial_markers[index]) if r[0] == "Standard")
        bounds = re.findall(r"(\d+)–(\d+)", standard[1])
        assert len(bounds) == 3
        for value, (low, high) in zip((points, count, int(row[6])), bounds, strict=True):
            assert int(low) <= value <= int(high), (row[0], value, low, high)
        initial = sum((hp[n] + armor.get(n, D(0))) * c for n, c in roster.items())
        source = D(source_rows[index][2]) * source_efficiency
        total = initial + source
        theoretical = teams[row[0]]
        ratio = (total / theoretical * 100).quantize(D("0.1"), rounding=ROUND_HALF_UP)
        expected = [theoretical, initial, source, total]
        assert list(map(D, reports[index][1:5])) == expected, (row[0], expected)
        assert reports[index][5] == f"{ratio}%", (row[0], ratio)
        print(f"{row[0]}：初始{count}体/{points}点，火力{theoretical}，消耗侧上界{total}，比值{ratio}%")

    ranged = {"压射体", "穿线体", "投涌体", "哨戒炮塔"}
    heavy = {"固守体", "破阵体", "投涌体", "守备机"}
    later = table(walk, "### 四个后续兵种局部对照")
    assert len(later) == 4
    difficulty = {r[0]: r for r in table(matrix, "MATRIX-003A ·")}
    for row in later:
        roster = {name: int(n) for name, n in re.findall(r"([^、]+)×(\d+)", row[2])}
        count = sum(roster.values())
        points = sum(costs[n] * c for n, c in roster.items())
        rcount = sum(c for n, c in roster.items() if n in ranged)
        hcount = sum(c for n, c in roster.items() if n in heavy)
        assert [count, points] == list(map(int, row[3].split(" / ")))
        assert [rcount, hcount] == list(map(int, row[4].split(" / ")))
        assert rcount * 4 <= count, "远程超过四分之一"
        tier = difficulty[row[1].split("/")[1]]
        assert len(roster) <= int(tier[3])
        assert hcount <= int(re.match(r"\d+", tier[4])[0])
    print("四项后续局部对照成本、职责与远程/重型比例通过；不代表高难整图、导航或来源调度通过。")
    print("九枪覆盖及三份功能短图派生表通过。实际种子0、试玩0；长局资源张力与完整救援窗口尚未验证。")


if __name__ == "__main__":
    main()
