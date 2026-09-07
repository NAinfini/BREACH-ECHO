"""补给算术与固定弹耗压力枚举；不是玩家、生成器或命中模拟。"""
from itertools import product
from math import ceil, comb, prod
from pathlib import Path

from check_enemy_contract import table


ROOT = Path(__file__).resolve().parents[1]


def expected_kills(shots, hits, probability):
    # 连续射击同一种身体靶，击杀后立即换目标；末尾伤而未杀不算击杀。
    return sum((successes // hits) * comb(shots, successes)
               * probability ** successes * (1 - probability) ** (shots - successes)
               for successes in range(shots + 1))


def survive(pair, guns, demands, efficiency):
    """每目标只用一把枪；固定增加空枪成本，不表示随机通关概率。"""
    states = {tuple(guns[name][0] + guns[name][1] for name in pair)}
    stages = [["逐能体"] * 6 + ["压射体"],
              ["逐能体"] * 6 + ["压射体", "固守体"]]
    for stage_index, stage in enumerate(stages):
        if stage_index:
            # 一席一包，不凭四人补给舱给单人四包；按合法后备上限裁切。
            states = {tuple(min(left + guns[name][1], guns[name][0] + guns[name][2])
                            for name, left in zip(pair, state)) for state in states}
        for target in stage:
            following = set()
            for state in states:
                for slot, name in enumerate(pair):
                    cost = ceil(demands[name][target] / efficiency) * guns[name][3]
                    if state[slot] >= cost:
                        remaining = list(state)
                        remaining[slot] -= cost
                        following.add(tuple(remaining))
            # 同样已经完成的目标，只保留库存不被另一状态完全覆盖的分配。
            states = {s for s in following if not any(
                other != s and all(a >= b for a, b in zip(other, s)) for other in following)}
            if not states:
                return False
    return True


def main():
    combat = (ROOT / "docs/内容/装备/战斗原型数值.md").read_text(encoding="utf-8")
    walk = (ROOT / "docs/制作/首轮配装三任务走读与风险验收.md").read_text(encoding="utf-8")
    review = {r[0]: r for r in table(combat, "### 同条件击杀与补给")}
    heavy = {r[0]: r for r in table(combat, "COMBAT-HEAVY-BREAKPOINTS")}
    runner_hp = float(next(r[1].split("/")[0].strip()
                          for r in table(combat, "## 八类敌人的测试参数") if r[0] == "Runner"))
    guns, demands, by_slot, report = {}, {}, {"第一": [], "第二": []}, []
    for r in table(combat, "## 枪械基础与资源"):
        name = r[0]
        magazine, capacity = map(int, r[3].split(" / "))
        refill = int(r[7])
        charged = "→" in r[2]
        cost = 4 if charged else 1
        label = name + "（满蓄直击）" if charged else name
        guns[name] = (magazine, refill, capacity, cost)
        by_slot[r[1].split(" / ")[0]].append(name)
        body = int(review[label][1].split(" / ")[0])
        weak = int(review[label][1].split(" / ")[1])
        demands[name] = {"逐能体": body,
                         "压射体": int(review[label][2].split(" / ")[0]),
                         "固守体": int(heavy[label][1].split(" / ")[2])}
        shots = refill // cost
        # 霰弹漏丸并非一发全中/全失，单独列条件，不套普通子弹伯努利模型。
        expected = "不套用" if "颗" in r[2] else f"{expected_kills(shots, body, .8):.2f}"
        damage = (float(r[2].split("→")[-1]) if charged else
                  prod(map(float, r[2].replace("颗", "").split("×"))))
        overkill = (body * damage - runner_hp) / (body * damage)
        assert 0 <= overkill < 1, "身体断点或伤害读取错误"
        report.append([name, str(magazine + refill), f"{refill / magazine:.2f}",
                       str(shots // body), str(shots // weak), expected, f"{overkill:.1%}"])
    for row in report:
        print("| " + " | ".join(row) + " |")
    documented = table(walk, "LOADOUT-AMMO-YIELD ·")
    assert documented == report, "补给产出派生表未同步"
    candidate_rows = []
    for count in (36, 45, 60, 75, 90):
        row = [str(count), f"{count / 30:.2f}", f"{count / 10:.1f}", str(count // 4),
               f"{expected_kills(count, 4, .8):.2f}", f"{expected_kills(count, 4, .6):.2f}"]
        candidate_rows.append(row)
        print("| " + " | ".join(row) + " |")
    assert table(walk, "LOADOUT-AMMO-CANDIDATES ·") == candidate_rows
    assert expected_kills(36, 4, 0) == 0
    assert expected_kills(36, 4, 1) == 9
    assert abs(expected_kills(4, 4, .5) - .5 ** 4) < 1e-12
    # 从空库存使用一份补给，检验连续两段个人火力投入；不是入场+补给混算。
    ar = demands["突击步枪"]
    pressure_rows = []
    for efficiency in (1, .8, .6):
        runner = ceil(ar["逐能体"] / efficiency) + 1
        suppressor = ceil(ar["压射体"] / efficiency) + 1
        first, second = 4 * runner + suppressor, 3 * runner
        pressure_rows.append([str(int(efficiency * 100)) + "%", str(first), str(second),
                              str(first + second), str(guns["突击步枪"][1] - first - second)])
    for row in pressure_rows:
        print("| " + " | ".join(row) + " |")
    assert table(walk, "LOADOUT-AMMO-RECOVERY ·") == pressure_rows
    # 拒绝把有空枪成本时的负余额，当作游戏真的允许超支开火。
    assert int(pressure_rows[1][-1]) >= 0
    assert int(pressure_rows[2][-1]) < 0
    assert all(mag + 2 * refill <= mag + capacity for mag, refill, capacity, _ in guns.values()), \
        "此靶序列要求中间补给不发生容量裁切；若调整容量须显式模拟留包再领取"
    pairs = list(product(by_slot["第一"], by_slot["第二"]))
    assert len(pairs) == 20
    body_yields = [sum((guns[n][1] // guns[n][3]) // demands[n]["逐能体"] for n in p)
                   for p in pairs]
    print(f"20组合法双槽：单包理想逐能身体击杀范围{min(body_yields)}至{max(body_yields)}，不计尾弹互补。")
    pass_counts = []
    for p in (1, .8, .6):
        passed = [pair for pair in pairs if survive(pair, guns, demands, p)]
        pass_counts.append(len(passed))
        print(f"单人固定弹耗压力，效率{p}：{len(passed)}/20存在分配解；不是成功率。")
        print("无分配解：", [pair for pair in pairs if pair not in passed])
    result = (f"本次枚举：单份双槽身体击杀{min(body_yields)}至{max(body_yields)}只；"
              f"独立单人靶序列在p=1/0.8/0.6时分别有{'/'.join(map(str, pass_counts))}组分配解。")
    assert result in walk, "双槽范围或单人结果说明未同步"
    print("PASS：九枪、五档突击候选、概率边界及20组静态分配；未模拟战斗或生成。")


if __name__ == "__main__":
    main()
