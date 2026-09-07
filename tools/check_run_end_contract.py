"""核对文档中的撤离扫描算术与身体分类；不模拟Unity、奖励服务或网络。"""

from fractions import Fraction
from itertools import product
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]


def parameter_value(text, key):
    matches = [line for line in text.splitlines() if line.startswith(f"| {key} /")]
    if len(matches) != 1:
        raise ValueError(f"参数缺失或重复：{key}")
    return matches[0].split("|")[2].strip()


def main():
    text = (ROOT / "docs/制作/初始测试参数.md").read_text(encoding="utf-8")
    work = Fraction(parameter_value(text, "TP-EXTRACTION-WORK").removesuffix("工作秒"))
    rates = {
        int(count): Fraction(rate)
        for count, rate in re.findall(
            r"([1-4])人([0-9.]+)", parameter_value(text, "TP-EXTRACTION-RATE")
        )
    }
    item_rate = Fraction(parameter_value(text, "TP-EXTRACTION-ITEM-RATE"))
    assert work > 0 and item_rate > 0 and set(rates) == {1, 2, 3, 4}
    assert all(rates[n] > 0 for n in rates)
    assert all(rates[n] <= rates[n + 1] for n in range(1, 4))

    # 每具身体的状态、区内/区外和控制资格；断线Alive不自动贡献扫描。
    states = tuple(product(("Alive", "Downed", "Out", "Disconnected"), (False, True)))
    tested = 0
    for size in range(1, 5):
        for bodies in product(states, repeat=size):
            scanners = sum(life == "Alive" and inside for life, inside in bodies)
            inside_ids = {i for i, (_, inside) in enumerate(bodies) if inside}
            left_ids = set(range(size)) - inside_ids
            assert not inside_ids.intersection(left_ids)
            assert inside_ids.union(left_ids) == set(range(size))
            for item_mode, item_present in ((False, False), (True, False), (True, True)):
                rate = (item_rate if item_mode else rates.get(scanners, 0))
                if scanners == 0 or (item_mode and not item_present):
                    rate = Fraction(0)
                prior = work / 2
                after_second = min(work, prior + rate)
                if not scanners or (item_mode and not item_present):
                    assert after_second == prior  # 暂停，不清零或倒退。
                else:
                    assert rate > 0 and inside_ids
                    duration = work / rate
                    assert min(work, duration * rate) == work
                    # 终局按位置分类，不要求区外队员全部进入或保持Alive。
                    assert len(inside_ids) + len(left_ids) == size
                tested += 1

    # 普通单扫描者能够完成；一人守圈三人在外，不得成为全员站圈扫描。
    assert work / rates[1] > 0
    assert {0} | {1, 2, 3} == set(range(4))
    ops = (ROOT / "docs/玩法/系统化战术行动模式.md").read_text(encoding="utf-8")
    assert "LeftBehind（被留下）" in ops and "不要求全员到齐" in ops
    assert "不存在个人先撤离" in ops and "进度暂停并保留" in ops
    print(f"PASS：{tested}项有限扫描状态组合；4档普通速率及实物扫描参数合法。")
    print("普通扫描秒数：" + ", ".join(f"{n}人={float(work / rates[n]):.3f}" for n in rates))
    print("范围：文档算术与分类。Unity、同tick动作、奖励事务、迁移与真人体验均未测试。")


if __name__ == "__main__":
    main()
