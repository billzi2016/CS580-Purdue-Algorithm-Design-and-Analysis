"""
文件意图：
    本文件手写实现 0/1 背包动态规划，用于每个物品最多选择一次的容量约束最大价值问题。

适用场景：
    物品不可切分、不可重复选择，目标是在容量限制内最大化总价值。

核心思想：
    dp[c] 表示容量为 c 时可获得的最大价值。倒序枚举容量，避免同一物品被重复使用。

时间复杂度：
    O(n * capacity)

空间复杂度：
    O(capacity)
"""

Item = tuple[str, int, int]


def zero_one_knapsack(items: list[Item], capacity: int) -> int:
    """返回 0/1 背包最大价值。"""
    if capacity < 0:
        raise ValueError("capacity 必须非负")
    dp = [0] * (capacity + 1)
    for name, weight, value in items:
        if weight <= 0 or value < 0:
            raise ValueError(f"物品必须满足 weight > 0 且 value >= 0：{name}")
        for current_capacity in range(capacity, weight - 1, -1):
            dp[current_capacity] = max(
                dp[current_capacity], dp[current_capacity - weight] + value
            )
    return dp[capacity]


if __name__ == "__main__":
    assert zero_one_knapsack([("a", 2, 3), ("b", 3, 4), ("c", 4, 5)], 5) == 7
    assert zero_one_knapsack([], 10) == 0
    assert zero_one_knapsack([("a", 5, 10)], 4) == 0
    assert zero_one_knapsack([("a", 5, 10)], 5) == 10

    print("002_zero_one_knapsack: all examples passed")
