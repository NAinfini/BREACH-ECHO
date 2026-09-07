"""复算工业危险文档的窗口与代价；不运行设施、导航、网络或游戏状态机。"""
from decimal import Decimal as D
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def assess(p, walk, crawl, run, tick):
    """返回独立参数关系；倒地无法自行逃离是必须保留的风险见证。"""
    escape = p["ESCAPE-DISTANCE"] / walk + p["RESPONSE-ALLOWANCE"]
    crawl_escape = p["ESCAPE-DISTANCE"] / crawl + p["RESPONSE-ALLOWANCE"]
    heat_warning = (p["HEAT-HOT"] - p["HEAT-PREWARN"]) / p["HEAT-RISE"]
    return {
        "热阈值顺序": D(0) <= p["HEAT-RESET"] < p["HEAT-PREWARN"] < p["HEAT-HOT"] < p["HEAT-TRIP"],
        "热预警覆盖站立逃离": heat_warning > escape,
        "喷流预警覆盖站立逃离": p["JET-WARNING"] > escape,
        "倒地需要外部处置": crawl_escape > max(heat_warning, p["JET-WARNING"]),
        "运动包络提前量": p["MACHINE-CLEARANCE"] > 2 * run * (p["MACHINE-BRAKE"] + 1 / tick),
        "恢复阈值低于热区": p["HEAT-RESET"] < p["HEAT-HOT"],
        "电弧预告覆盖站立逃离": p["ARC-WARNING"] > escape,
        "电弧间隔允许无阻爬出": p["ARC-WARNING"] + p["ARC-RECOVERY"] > crawl_escape,
        "放电不比现有脉冲更早结束": p["ARC-DISCHARGE"] >= p["ARC-ACTIVE"],
    }


def main():
    text = (ROOT / "docs/内容/设施与资源/工业危险与故障处置合同.md").read_text(encoding="utf-8")
    matches = re.findall(r"^\| ([A-Z]+(?:-[A-Z]+)+) \| ([\d.]+) \|", text, re.M)
    p = {key: D(value) for key, value in matches}
    assert len(p) == len(matches) == 29, "参数行缺失或重复，需要同步审阅"
    assert all(value > 0 for value in p.values())
    params = (ROOT / "docs/制作/初始测试参数.md").read_text(encoding="utf-8")
    move_row = next(line for line in params.splitlines() if line.startswith("| TP-MOVE /"))
    # 从现行责任行取值，不在验算脚本维护第二套玩家速度。
    walk, run, _crouch = map(D, re.search(r"\| ([\d.]+) / ([\d.]+) / ([\d.]+) m/s", move_row).groups())
    crawl_row = next(line for line in params.splitlines() if line.startswith("| 倒地爬行 |"))
    crawl = D(re.search(r"([\d.]+)\s*m/s", crawl_row)[1])
    tick_row = next(line for line in params.splitlines() if line.startswith("| TP-TICK /"))
    tick = D(re.search(r"([\d.]+) Hz", tick_row)[1])
    checks = assess(p, walk, crawl, run, tick)
    assert all(checks.values()), checks
    warning = (p["HEAT-HOT"] - p["HEAT-PREWARN"]) / p["HEAT-RISE"]
    trip = (p["HEAT-TRIP"] - p["HEAT-HOT"]) / p["HEAT-RISE"]
    reset = (p["HEAT-TRIP"] - p["HEAT-RESET"]) / p["HEAT-FALL"]
    assert (warning, trip, reset) == (D(2), D("7.5"), D(10))
    assert p["PRESSURE-INITIAL"] > p["PRESSURE-SAFE"]
    equalize_to_safe = p["PRESSURE-EQUALIZE"] * (1 - p["PRESSURE-SAFE"] / p["PRESSURE-INITIAL"])
    assert D(0) < equalize_to_safe < p["PRESSURE-EQUALIZE"]
    med_row = next(line for line in params.splitlines() if line.startswith("| TP-MED-POD /"))
    heal = D(re.search(r"恢复([\d.]+)HP", med_row)[1])
    thermal = 3 * p["HEAT-CONTACT"]
    assert thermal <= heal and p["JET-DAMAGE"] <= heal < thermal + p["JET-DAMAGE"]
    assert p["ARC-PULSES"] == p["ARC-PULSES"].to_integral_value()
    assert p["ARC-DAMAGE"] < heal < p["ARC-PULSES"] * p["ARC-DAMAGE"]
    negatives = (
        ("JET-WARNING", D(1), "喷流预警覆盖站立逃离"),
        ("HEAT-PREWARN", D(69), "热预警覆盖站立逃离"),
        ("HEAT-RESET", D(80), "恢复阈值低于热区"),
        ("MACHINE-CLEARANCE", D(4), "运动包络提前量"),
        ("ARC-WARNING", D(1), "电弧预告覆盖站立逃离"),
        ("ARC-RECOVERY", D(1), "电弧间隔允许无阻爬出"),
        ("ARC-DISCHARGE", D("0.1"), "放电不比现有脉冲更早结束"),
    )
    for key, value, failed_check in negatives:
        assert not assess({**p, key: value}, walk, crawl, run, tick)[failed_check]
    assert not assess(p, walk, crawl, D(10), tick)["运动包络提前量"]
    print(f"PASS：{len(p)}参数、{len(checks)}关系、{len(negatives) + 1}项反例；热预警{warning}s / 停机余量{trip}s / 复位{reset}s。")
    print(f"电弧无伤间隔{p['ARC-WARNING'] + p['ARC-RECOVERY']}s；同一故障每实体最多{p['ARC-PULSES'] * p['ARC-DAMAGE']}HP，不代表安全救援实测。")
    print(f"伤害例：热接触{thermal}HP + 独立喷流{p['JET-DAMAGE']}HP = {thermal + p['JET-DAMAGE']}HP > 单份医疗{heal}HP。")
    print("倒地逃离与更高接近速度不能沿用站立窗口/8米保护距离；必须另验处置与几何。")
    print("范围：仅文档算术；喷流去重、材料事务、暂停恢复、实体可达性与游戏Seed均未测试。")


if __name__ == "__main__":
    main()
