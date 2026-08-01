"""
文件意图：
    本文件手写实现分数背包贪心算法，用于最大化可切分物品的总价值。

适用场景：
    物品可以取任意比例。若物品不可切分，应使用 0/1 背包动态规划。

核心思想：
    按单位重量价值从高到低排序，优先装入价值密度最高的物品。

时间复杂度：
    O(n log n)

空间复杂度：
    O(n)
"""

Item = tuple[str, float, float]
ChosenItem = tuple[str, float, float]


def fractional_knapsack(
    items: list[Item], capacity: float
) -> tuple[float, list[ChosenItem]]:
    """
    求分数背包的最大价值。

    参数：
        items: 物品列表，每项为 (name, value, weight)。
        capacity: 背包容量。

    返回：
        (maximum_value, chosen)，chosen 中每项为 (name, fraction, value_taken)。
    """
    if capacity < 0:
        raise ValueError("capacity 必须非负")

    for name, value, weight in items:
        if value < 0 or weight <= 0:
            raise ValueError(f"物品必须满足 value >= 0 且 weight > 0：{name}")

    remaining = capacity
    total_value = 0.0
    chosen: list[ChosenItem] = []

    for name, value, weight in sorted(
        items, key=lambda item: item[1] / item[2], reverse=True
    ):
        if remaining == 0:
            break

        take_weight = min(weight, remaining)
        fraction = take_weight / weight
        value_taken = value * fraction
        chosen.append((name, fraction, value_taken))
        total_value += value_taken
        remaining -= take_weight

    return total_value, chosen


if __name__ == "__main__":
    value, chosen_items = fractional_knapsack(
        [("gold", 60, 10), ("silver", 100, 20), ("bronze", 120, 30)],
        50,
    )
    assert value == 240.0
    assert chosen_items[-1] == ("bronze", 2 / 3, 80.0)
    assert fractional_knapsack([], 10) == (0.0, [])
    assert fractional_knapsack([("x", 10, 5)], 0) == (0.0, [])

    print("004_fractional_knapsack: all examples passed")
