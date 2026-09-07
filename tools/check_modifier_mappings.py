"""核对修改器文档的白名单、绑定覆盖和算术；不是游戏编译器或地图模拟。"""
from itertools import combinations
from pathlib import Path
import re

from check_enemy_contract import table

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def main():
    mapping = read("docs/内容/任务/修改器任务映射与组合准入.md")
    environment = read("docs/内容/设施与资源/关卡环境修正器候选与验证.md")
    events = read("docs/内容/活动/特殊活动修改器候选库.md")
    combat = read("docs/内容/活动/玩家与敌人强化修改器候选.md")
    live = read("docs/玩法/在线活动特殊挑战与赛季边界.md")
    # 原始候选定义行有反引号；后续参数表和任务表只是同ID引用。
    catalog = {}
    for doc in (environment, events, combat):
        for line in doc.splitlines():
            found = re.match(r"\| `(?P<id>MOD-[A-Z-]+)` ", line)
            if found:
                key = found["id"]
                assert key not in catalog, f"候选定义重复：{key}"
                last = line.split("|")[-2].strip()
                cost = re.search(r"(?:^|；)([123])(?:；|$)", last)
                assert cost, f"复杂度无法读取：{line}"
                catalog[key] = int(cost[1])
    assert len(catalog) == 80, f"当前候选全集数量改变，请核查去重：{len(catalog)}"
    roster = table(mapping, "MOD-MISSION-ROSTER ·")
    assert len(roster) == 9 and len({r[0] for r in roster}) == 9
    costs = {r[0]: int(r[2]) for r in roster}
    categories = {r[0]: r[1] for r in roster}
    assert all(catalog[key] == cost for key, cost in costs.items())
    for task, prefix in (("BLACKSTART", "B"), ("FORENSICS", "F"), ("FREIGHT", "L")):
        bindings = table(mapping, f"MOD-MISSION-{task} ·")
        assert len(bindings) == 9 and {r[0] for r in bindings} == set(costs)
        assert all(len(r) == 4 and all(r) for r in bindings)
        for key, target, *_ in bindings:
            assert re.search(prefix + r"\d{2}", target), f"缺语义区域：{task}/{key}"
    budget = re.search(r"标准活动初值建议总成本不超过(\d+)，极限挑战不超过(\d+)", live)
    assert budget
    limits = dict(zip(("普通", "高级"), map(int, budget.groups())))
    groups = table(mapping, "MOD-MISSION-COMBINATIONS ·")
    pairs = {frozenset(r[1:3]): r[3] for r in groups}
    assert len(groups) == len(pairs) == 9

    def paper_selection(ids, tier="普通"):
        """仅检查本文件选项白名单；不声称目标、几何或运行时可用。"""
        if any(key not in costs for key in ids):
            return "未登记映射"
        if len(ids) != len(set(ids)):
            return "未列组合"
        if sum(costs[key] for key in ids) > limits[tier] or sum(costs[key] == 3 for key in ids) > 1:
            return "预算超限"
        if len(ids) == 1:
            return "允许测试"
        pair = frozenset(ids)
        if len(ids) != 2 or pair not in pairs or (pairs[pair] == "高级" and tier != "高级"):
            return "未列组合"
        return "允许测试"

    positives = negatives = 0
    for _task in range(3):
        for key in costs:
            assert paper_selection([key], "高级" if costs[key] == 3 else "普通") == "允许测试"
            positives += 1
        for pair, tier in pairs.items():
            assert len(pair) == 2 and pair <= costs.keys()
            assert sum(categories[k] == "环境" for k in pair) <= 1
            assert paper_selection(list(pair), tier) == "允许测试"
            positives += 1
        for pair in combinations(costs, 2):
            if frozenset(pair) not in pairs:
                assert paper_selection(pair, "高级") != "允许测试"
                negatives += 1
    for ids, tier, expected in (
        (["MOD-UNKNOWN"], "普通", "未登记映射"),
        (["MOD-EM-STORM"] * 2, "普通", "未列组合"),
        (["MOD-EM-STORM", "MOD-UNLIMITED-TOOLS"], "普通", "预算超限"),
        (["MOD-LOW-GRAVITY", "MOD-UNLIMITED-TOOLS"], "高级", "预算超限"),
        (["MOD-FAST-HANDLING", "MOD-BODY-PIERCING", "MOD-PRIMARY-OVERDRIVE"], "普通", "未列组合"),
    ):
        assert paper_selection(ids, tier) == expected
        negatives += 1
    rejections = table(mapping, "MOD-MISSION-REJECT ·")
    assert len(rejections) == 16 and len({r[0] for r in rejections}) == 16
    params = {r[0]: r for r in table(environment, "ENV-MOD-PARAMETERS ·")}
    storm = tuple(map(int, re.findall(r"(?:正常|预警|干扰|恢复)(\d+)s", params["MOD-EM-STORM"][1])))
    period = int(re.search(r"周期(\d+)s", params["MOD-EM-STORM"][1])[1])
    assert len(storm) == 4 and all(t > 0 for t in storm) and sum(storm) == period
    noise = tuple(map(int, re.findall(r"(?:平稳|预告|轰鸣)(\d+)s", params["MOD-INDUSTRIAL-NOISE"][1])))
    assert len(noise) == 3 and sum(noise) == int(re.search(r"周期(\d+)s", params["MOD-INDUSTRIAL-NOISE"][1])[1])
    flood = params["MOD-CONDUCTIVE-FLOOD"][1]
    retries = int(re.search(r"最多(\d+)次", flood)[1])
    active = int(re.search(r"带电(\d+)s", flood)[1])
    assert retries * active == 9  # 文中按0/1/2秒判定；不是实际伤害命中测试。
    factor = float(re.search(r"普通值×([\d.]+)", params["MOD-LOW-GRAVITY"][1])[1])
    assert 0 < factor < 1
    for _, per_seat, team, _ in table(events, "EVENT-MOD-TOOL-CAPS ·"):
        assert 0 < int(per_seat) * 4 == int(team)
    print(f"通过：80项候选唯一、9项本批规则、27条绑定、9个白名单组合；{positives}项选项正例、{negatives}项选项负例。")
    print(f"算术：风暴周期{period}s/停机{sum(storm[2:])}s；噪声周期{sum(noise)}s；积水最多{retries * active}次脉冲；低重力同初速跳高/滞空×{1/factor:.4f}。")
    print("16类生成拒绝条件仅已登记；未运行地图/声学/战斗/事务/联网/真人验证。")


if __name__ == "__main__":
    main()
