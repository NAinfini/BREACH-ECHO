"""检查敌人责任表覆盖并复算九枪断点；不是游戏状态机或命中测试。"""
from decimal import Decimal as D
import re

from check_weapon_identity import DOC, rows, ceiling, armored_shots


def table(text, marker):
    section = text.split(marker, 1)[1]
    lines = section.splitlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("|"))
    block = []
    for line in lines[start:]:
        if not line.startswith("|"):
            break
        block.append(line)
    return rows("\n".join(block))[2:]


def main():
    text = DOC.read_text(encoding="utf-8")
    enemies = table(text, "## 八类敌人的测试参数")
    names = dict(zip(
        ("Runner", "Suppressor", "Holder", "Scout", "Flanker", "Lancer", "Breacher", "Bombard"),
        ("逐能体", "压射体", "固守体", "探讯体", "缝行体", "穿线体", "破阵体", "投涌体"), strict=True))
    hp = {names[r[0]]: D(r[1].split("/")[0].strip()) for r in enemies}
    assert len(hp) == 8 and all(v > 0 for v in hp.values())
    parts = table(text, "COMBAT-MULTI-WEAKPOINT")
    assert len(parts) == 19 and len({r[0] for r in parts}) == 19
    assert {r[0].split(" / ")[0] for r in parts} == set(hp)
    for r in parts:
        assert all(D(v) >= 1 for v in r[1:4])
        assert 0 < D(r[4]) < hp[r[0].split(" / ")[0]]
    parts = {r[0]: r for r in parts}
    armor_rows = table(text, "COMBAT-ENEMY-ARMOR")
    armor = {r[0].split(" / ")[0]: D(r[1]) for r in armor_rows}
    assert len(armor) == 4
    for r in enemies:
        m = re.search(r"(\d+)(?:冲撞甲|装甲)Integrity", r[2])
        if m:
            assert D(m[1]) == armor[names[r[0]]], "基础表甲值与装甲责任表冲突"
    geometry = table(text, "COMBAT-ENEMY-GEOMETRY")
    facilities = table(text, "COMBAT-FACILITY-PROFILE")
    all_names = set(hp) | {"猎界体"} | {r[0] for r in facilities}
    assert len(all_names) == 12 and {r[0] for r in geometry} == all_names
    for r in geometry:
        height, radius = map(D, r[1].split(" / "))
        assert height > 0 and radius > 0 and D(r[4]) > 0
    facility_parts = table(text, "COMBAT-FACILITY-PARTS")
    assert len(facility_parts) == 3
    assert {r[0].split(" / ")[0] for r in facility_parts} == {r[0] for r in facilities}
    for r in facility_parts:
        assert D(r[1]) >= 1 and D(r[2]) > 0
    actions = table(text, "COMBAT-ENEMY-ACTIONS")
    assert len(actions) == 12
    for r in actions:
        lock, first, last, next_start = map(D, r[2:6])
        assert 0 <= lock < first <= last < next_start, r[0]
        assert all(t * 60 == (t * 60).to_integral_value() for t in (lock, first, last, next_start)), r[0]
        assert D(r[1]) >= 0
    # 复算每把枪的八类身体/可持续命中的裸露精确部位，不模拟命中率。
    guns = table(text, "## 枪械基础与资源")
    heavy_result = []
    profiles = 0
    for gun in guns:
        damage_text = gun[2].replace("颗", "")
        if "×" in damage_text:
            a, b = map(D, damage_text.split("×"))
            variants = [(gun[0], a * b)]
        elif "→" in damage_text:
            low, high = map(D, damage_text.split("→"))
            variants = [(gun[0] + "（最低蓄力）", low), (gun[0] + "（满蓄直击）", high)]
        else:
            variants = [(gun[0], D(damage_text))]
        for label, damage in variants:
            profiles += 1
            counts = {}
            for enemy, health in hp.items():
                key = "侧感知器" if enemy == "缝行体" else "散热囊" if enemy == "投涌体" else "感知器"
                part = parts[f"{enemy} / {key}"]
                mult = D(part[2 if gun[0] == "低声针束步枪" else 1])
                body, weak = ceiling(health / damage), ceiling(health / (damage * mult))
                assert 0 < weak <= body
                front = armored_shots(damage, health, armor.get(enemy, D(0)))
                assert front >= body
                counts[enemy] = (body, weak, front)
            cell = lambda values: " / ".join(map(str, values))
            heavy_result.append([label, cell(counts["固守体"]), cell(counts["破阵体"]), cell(counts["投涌体"][:2])])
    documented = table(text, "COMBAT-HEAVY-BREAKPOINTS") if "COMBAT-HEAVY-BREAKPOINTS" in text else None
    for r in heavy_result:
        print("| " + " | ".join(r) + " |")
    assert documented == heavy_result, "重敌派生表缺失或不一致"
    # 只验证候选储备算术，不把该循环称为游戏再生逻辑测试。
    predator = {r[0]: D(r[1]) for r in table(text, "COMBAT-PREDATOR-PROFILE")}
    reserve, transfer, total = predator["再生储备"], predator["每次失能恢复生命上限"], D(0)
    assert reserve >= 0 and transfer > 0 and predator["每秒修复生命"] > 0
    while reserve > 0:
        healed = min(transfer, reserve)
        reserve -= healed
        total += healed
    assert total == predator["再生储备"]
    partial = min(predator["每秒修复生命"] * D("1.5"), predator["再生储备"])
    assert partial + (predator["再生储备"] - partial) == total
    assert predator["再生囊完整度"] < predator["肌体生命上限"]
    print(f"PASS：12类覆盖、19生物部位、3设施部位、4甲面、12动作时序、{profiles}种射击条件×8常规敌人及有限再生算术；几何/运行/联网/试玩未验证。")


if __name__ == "__main__":
    main()
