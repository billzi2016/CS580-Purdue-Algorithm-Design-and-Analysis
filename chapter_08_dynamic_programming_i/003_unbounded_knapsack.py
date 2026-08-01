"""
文件意图：
    本文件手写实现完全背包动态规划，用于每个物品可以选择无限次的容量约束最大价值问题。

适用场景：
    物品不可切分但可重复选择，例如硬币组合、无限供应物品选择。

核心思想：
    dp[c] 表示容量 c 的最大价值。正序枚举容量，使同一物品可以在当前轮被重复使用。

时间复杂度：
    O(n * capacity)

空间复杂度：
    O(capacity)
"""

Item = tuple[str, int, int]


def unbounded_knapsack(items: list[Item], capacity: int) -> int:
    """返回完全背包最大价值。"""
    if capacity < 0:
        raise ValueError("capacity 必须非负")
    dp = [0] * (capacity + 1)
    for name, weight, value in items:
        if weight <= 0 or value < 0:
            raise ValueError(f"物品必须满足 weight > 0 且 value >= 0：{name}")
        for current_capacity in range(weight, capacity + 1):
            dp[current_capacity] = max(dp[current_capacity], dp[current_capacity - weight] + value)
    return dp[capacity]


if __name__ == "__main__":
    assert unbounded_knapsack([("a", 2, 3), ("b", 3, 5)], 7) == 11
    assert unbounded_knapsack([], 5) == 0
    assert unbounded_knapsack([("x", 4, 10)], 3) == 0
    assert unbounded_knapsack([("x", 4, 10)], 8) == 20

    print("003_unbounded_knapsack: all examples passed")
