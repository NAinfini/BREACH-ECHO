"""校验文档的交互声学算术与映射；不模拟地图、AI、网络或玩家行为。"""
from decimal import Decimal as D
from pathlib import Path
import re

from check_enemy_contract import table

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def main():
    combat = read("docs/内容/装备/战斗原型数值.md")
    params = read("docs/制作/初始测试参数.md")
    economy = read("docs/玩法/资源回收额度与公共物资.md")
    profiles = {r[0]: (D(r[1]), D(r[2])) for r in
                table(combat, "COMBAT-INTERACTION-NOISE ·")}
    assert len(profiles) == 8
    threshold = D(re.search(r"WakeExposure阈值(\d+)", params)[1])
    decay = D(re.search(r"每秒衰减(\d+)", params)[1])
    door = D(re.search(r"关闭普通门([\d.]+)", params)[1])

    def amount(profile, distance, coefficient=D(1)):
        radius, intensity = profiles[profile]
        return intensity * max(D(0), 1 - D(distance) / radius) * coefficient

    def sequence(events, initial=D(0)):
        # events仅为声明声学距离和无持续光照/接近输入的离散样例。
        exposure, prior_time, peak = initial, D(0), initial
        maxima = {}
        for time, root, contribution in events:
            time = D(time)
            assert time >= prior_time
            exposure = max(D(0), exposure - decay * (time - prior_time))
            old = maxima.get(root, D(0))
            exposure += max(D(0), contribution - old)
            maxima[root] = max(old, contribution)
            peak = max(peak, exposure)
            prior_time = time
        return exposure, peak

    assert amount("接口", 3) == amount("卡扣", 3) == 0
    assert amount("校准", 3) == 5
    assert amount("机构", 4) < 14
    assert amount("机构", 4, D(0)) == 0
    assert amount("安保广播", 10, door) == 15
    three = [(t, f"calibrate:{t}", amount("校准", 3)) for t in range(3)]
    assert sequence(three, D(20))[1] == 25 < threshold
    # 同根重传只补最大值差额，不把重复消息当脉冲；取消不抹已发事件。
    assert sequence([(0, "a", D(20)), (0, "a", D(20))])[0] == 20
    assert sequence([(0, "a", D(20)), (0, "a", D(30))])[0] == 30
    assert sequence(three[:1])[0] == 5
    # 新的合法近距尝试会重新发声；这不是网络重复包。
    spam = [(D(t) / 5, f"attempt:{t}", amount("校准", 1)) for t in range(8)]
    assert sequence(spam)[1] >= threshold
    alarm = [(t, f"alarm:{t}", amount("安保广播", 10)) for t in range(2)]
    assert sequence(alarm)[1] >= threshold
    assert sequence([(0, "fan:0", amount("稳态设备", 3)),
                     (1, "fan:1", amount("稳态设备", 3))])[1] == 5
    # 只检查剩余Dormant个体的符号化路径；不声称跨过阈值后会自行回睡。
    route = [(0, "record", amount("接口", 3)),
             (1, "anchor1", amount("接口", 3)),
             (2, "anchor2", amount("接口", 3)),
             *[(3 + t, f"timebase:{t}", amount("校准", 3)) for t in range(3)],
             (7, "seal", amount("卡扣", 3)),
             (8, "dock", amount("卡扣", 3)),
             *[(9 + t, f"upload:{t}", amount("校准", 3)) for t in range(3)],
             (13, "door", amount("机构", 4))]
    assert sequence(route, D(20))[1] < threshold

    paths = {
        "换流器黑启动任务合同与灰盒规格.md": "BST-INTERACTION-MAP ·",
        "分布式数据取证任务合同.md": "FORENSICS-INTERACTION-MAP ·",
        "货运线夺回任务合同.md": "FREIGHT-INTERACTION-MAP ·",
    }
    for name, marker in paths.items():
        actions = table(read("docs/内容/任务/" + name), marker)
        assert len(actions) >= 10
        assert all(any(profile in row[2] for profile in profiles) for row in actions)
    times = table(economy, "ECO-DELIVERY-TIMING ·")
    preparation, confirmation, shipping = [D(r[1].removesuffix("s")) for r in times[:3]]
    use_time = D(re.search(r"使用包为(\d+)s", economy)[1])
    assert preparation + confirmation + shipping + use_time == 13
    assert confirmation + shipping + use_time == 11
    print("PASS：8种交互输入、3份动作映射、累计/去重/取消/重复反例、最低证据符号化路径及投送时长算术。")
    print("未验证真实地图传播、移动、失败退款事务、主机迁移或潜行通关；实际Seed与试玩均0。")


if __name__ == "__main__":
    main()
