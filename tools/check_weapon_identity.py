"""复算九枪文档的断点与补给表；不模拟命中、硬直、网络或玩家手感。"""
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/内容/装备/战斗原型数值.md"
D = Decimal


def rows(section):
    return [[cell.strip() for cell in line.split("|")[1:-1]]
            for line in section.splitlines() if line.startswith("|")]


def ceiling(value):
    return int(value.to_integral_value(rounding=ROUND_CEILING))


def armored_shots(damage, hp, armor):
    count = 0
    while hp > 0:
        absorbed = min(armor, damage * D("0.8"))
        armor -= absorbed
        hp -= damage - absorbed
        count += 1
    return count


def main():
    text = DOC.read_text(encoding="utf-8")
    base = rows(text.split("## 枪械基础与资源", 1)[1].split("\n\n蓄力爆破", 1)[0])[2:]
    assert len(base) == 9 and len({r[0] for r in base}) == 9
    enemies = {r[0]: D(r[1].split("/")[0].strip())
               for r in rows(text.split("## 八类敌人的测试参数", 1)[1].split("###", 1)[0])[2:]}
    assert len(enemies) == 8
    parts = {r[0]: r for r in rows(text) if len(r) == 6 and r[0].startswith(("逐能体 /", "压射体 /"))}
    expected = []
    damage_by_name = {}
    for r in base:
        name, _, damage_text, inventory, *_ = r
        reserve = D(inventory.split("/")[1].strip())
        damage_values = damage_text.replace("颗", "").split("→")
        profiles = [(name, D(damage_values[0]), 1)] if len(damage_values) == 1 and "×" not in damage_text else []
        if "×" in damage_text:
            pellets, pellet_damage = map(D, damage_text.replace("颗", "").split("×"))
            profiles = [(name, pellets * pellet_damage, 1)]
        elif "→" in damage_text:
            charge_min, charge_max = map(D, re.search(r"蓄力([\d.]+)→([\d.]+)s", r[6]).groups())
            cost_min, cost_max = map(D, re.search(r"每发(\d+)→(\d+)单位", r[6]).groups())
            profiles = [(name + "（最低蓄力）", D(damage_values[0]), 1),
                        (name + "（满蓄直击）", D(damage_values[1]), 4)]
        for label, damage, cost in profiles:
            budget = D(r[7]) * 5
            assert budget == budget.to_integral_value(), "五份合并复算须为整数库存"
            shots = int(budget // cost)
            part_index = 2 if name == "低声针束步枪" else 1
            runner, suppressor = enemies["Runner"], enemies["Suppressor"]
            multipliers = [D(parts[f"{target} / 感知器"][part_index]) for target in ("逐能体", "压射体")]
            counts = [ceiling(runner / damage), ceiling(runner / (damage * multipliers[0])),
                      ceiling(suppressor / damage), ceiling(suppressor / (damage * multipliers[1]))]
            kills = [shots // n for n in counts]
            cell = lambda a, b: f"{a} / {b}"
            expected.append([label, cell(*counts[:2]), cell(*counts[2:]), str(shots), cell(*kills[:2]), cell(*kills[2:])])
            damage_by_name[label] = damage
    print("| 枪械 | 逐能体身体 / 感知器发数 | 压射体身体 / 感知器发数 | 五份可发射数 | 逐能体击杀数（身体 / 感知器） | 压射体击杀数（身体 / 感知器） |")
    for row in expected:
        print("| " + " | ".join(row) + " |")
    review = text.split("COMBAT-NINE-GUN-REVIEW", 1)[1]
    documented = [r for r in rows(review) if len(r) == 6 and r[0] in {r[0] for r in expected}]
    assert documented == expected, "文档断点/补给表与唯一参数不一致"
    # 明确正面厚甲反例，不用裸露弱点倍率替代甲面。
    sniper = damage_by_name["重型狙击步枪"]
    holder_row = next(r for r in rows(text) if r[0] == "Holder")
    armor = D(re.search(r"(\d+)装甲Integrity", holder_row[2])[1])
    assert armored_shots(sniper, enemies["Holder"], armor) == 3
    assert armored_shots(D(36), enemies["Holder"], armor) == 11
    assert armored_shots(D(18), enemies["Holder"], armor) == 21
    assert 7 * pellet_damage < enemies["Runner"] <= pellets * pellet_damage
    assert [ceiling(enemies["Runner"] / (D(36) * D(2) * c))
            for c in (D(1), D("0.75"), D("0.5"))] == [1, 2, 2]
    # 爆破连续伤害与整数支付在三个台阶有可见效率折点。
    def charge(t):
        u = max(D(0), min(D(1), (t - charge_min) / (charge_max - charge_min)))
        low = damage_by_name["蓄力爆破枪（最低蓄力）"]
        high = damage_by_name["蓄力爆破枪（满蓄直击）"]
        return low + (high - low) * u, ceiling(cost_min + (cost_max - cost_min) * u)
    assert [charge(t) for t in map(D, ("0.3", "0.7", "1.1", "1.5"))] == [(30, 1), (60, 2), (90, 3), (120, 4)]
    assert charge(D("0.7") + D(1) / 60)[1] == 3
    print("PASS：九枪十种直击条件、五份补给、厚甲反例、霰弹漏弹、穿透衰减与爆破支付台阶；不代表试玩。")


if __name__ == "__main__":
    main()
