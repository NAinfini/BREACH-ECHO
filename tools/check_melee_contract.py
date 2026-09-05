"""检查文档参数算术；不是游戏命中、网络或手感测试。"""
from decimal import Decimal, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/内容/装备/首轮近战攻击与资源合同.md"
BALANCE = ROOT / "docs/内容/装备/战斗原型数值.md"
D = Decimal


def ticks(seconds):
    return int((seconds * 60).to_integral_value(rounding=ROUND_CEILING))


def main():
    text = DOC.read_text(encoding="utf-8")
    section = text.split("| 动作 | 身体伤害 |", 1)[1].split("\n\n", 1)[0]
    actions = {}
    for line in section.splitlines():
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) == 7 and cells[0].endswith(("普通", "蓄力")):
            actions[cells[0]] = tuple(D(cell) for cell in cells[1:])
    assert len(actions) == 6, "必须恰有三件普通与蓄力六行"
    count = 1
    for name, values in actions.items():
        damage, charge, windup, active, recovery, reach = values
        assert damage > 0 and reach > 0
        assert windup > 0 and active > 0 and recovery > 0 and charge >= 0
        assert all(D(ticks(v)) / 60 == v for v in (charge, windup, active, recovery))
        count += 3
        if name.endswith("蓄力"):
            normal = actions[name.replace("蓄力", "普通")]
            assert charge > D("0.25") and damage > normal[0]
            # 任意时刻松开有效；零蓄力接普通伤害，满蓄接满值。
            def charged_damage(t):
                q = max(D(0), min(D(1), t / charge))
                return normal[0] + (damage - normal[0]) * q
            assert charged_damage(D(0)) == normal[0]
            assert charged_damage(charge) == damage
            assert charged_damage(charge / 2) == (normal[0] + damage) / 2
            assert normal[0] < charged_damage(D(1) / 60) < damage
            assert charged_damage(charge * 2) == damage
            count += 6
        cycle = windup + active + (max(charge, recovery) if charge else recovery)
        print(f"{name}: 身体={damage}, 连续同类最短接触间隔={cycle}s")
    parts = {}
    for line in BALANCE.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) == 6 and cells[0].startswith(("逐能体 /", "压射体 /")):
            parts[cells[0]] = tuple(D(cell) for cell in cells[1:5])
    assert len(parts) == 5
    count += 1
    for values in parts.values():
        assert all(v >= 1 for v in values[:3]) and values[3] > 0
        count += 1
    sensor = parts["逐能体 / 感知器"]
    assert actions["战刃蓄力"][0] * sensor[0] == 100
    assert actions["刺矛蓄力"][0] * sensor[0] == 110
    assert actions["冲击锤蓄力"][0] * sensor[2] == 165
    assert actions["战刃蓄力"][0] * parts["逐能体 / 推进前肢"][0] == D("62.5")
    count += 1
    # 这些是当前实验的明确击杀/控制目标，调参时必须连同理由重审。
    assert actions["战刃蓄力"][0] < 70 and actions["刺矛蓄力"][0] < 70
    assert actions["冲击锤蓄力"][0] < 250
    count += 5
    hammer = actions["冲击锤蓄力"]
    hammer_gap = hammer[2] + hammer[3] + max(hammer[1], hammer[4])
    assert hammer_gap > D("0.80"), "单人同一重击不能自然覆盖整个循环"
    count += 1
    # 从噪声表读取，而非复制半径与强度成第二份配置。
    noise = {}
    for line in text.splitlines():
        cells = [cell.strip() for cell in line.split("|")[1:-1]]
        if len(cells) == 4 and cells[0] in ("满蓄命中血肉", "普通命中血肉"):
            noise[cells[0]] = [tuple(D(n.strip()) for n in cell.split("/")) for cell in cells[1:]]
    assert len(noise) == 2
    count += 1
    for radius, level in noise["满蓄命中血肉"]:
        assert radius > 0 and level > 0
        near = level * max(D(0), 1 - D(1) / radius)
        boundary = level * max(D(0), 1 - radius / radius)
        assert boundary == 0
        print(f"满蓄血肉声源: {radius}m/{level}刺激; 开放路径1m接收={near:.3f}")
        count += 2
    assert noise["满蓄命中血肉"][0][1] < 100
    assert noise["满蓄命中血肉"][1][1] < 100
    assert noise["满蓄命中血肉"][2][1] * (1 - D(1) / noise["满蓄命中血肉"][2][0]) >= 100
    count += 3
    print(f"PASS: {count}项静态参数断言；没有运行游戏碰撞、取消状态机或网络测试。")


if __name__ == "__main__":
    main()
