"""
文件意图：
    本文件手写实现零钱兑换动态规划，包括最少硬币数和组合数量两个经典问题。

适用场景：
    给定硬币面额和目标金额，求最优数量或组合计数。

核心思想：
    最少硬币数使用 min 转移；组合数量按硬币外层循环，避免排列重复计数。

时间复杂度：
    O(amount * number_of_coins)

空间复杂度：
    O(amount)
"""


def min_coins(coins: list[int], amount: int) -> int:
    """返回组成 amount 所需的最少硬币数；不可达返回 -1。"""
    _validate(coins, amount)
    unreachable = amount + 1
    dp = [unreachable] * (amount + 1)
    dp[0] = 0
    for current_amount in range(1, amount + 1):
        for coin in coins:
            if current_amount >= coin:
                dp[current_amount] = min(dp[current_amount], dp[current_amount - coin] + 1)
    return -1 if dp[amount] == unreachable else dp[amount]


def count_combinations(coins: list[int], amount: int) -> int:
    """返回组成 amount 的组合数量，不区分硬币顺序。"""
    _validate(coins, amount)
    dp = [0] * (amount + 1)
    dp[0] = 1
    for coin in coins:
        for current_amount in range(coin, amount + 1):
            dp[current_amount] += dp[current_amount - coin]
    return dp[amount]


def _validate(coins: list[int], amount: int) -> None:
    if amount < 0:
        raise ValueError("amount 必须非负")
    if any(coin <= 0 for coin in coins):
        raise ValueError("硬币面额必须为正")


if __name__ == "__main__":
    assert min_coins([1, 2, 5], 11) == 3
    assert min_coins([2], 3) == -1
    assert min_coins([], 0) == 0
    assert count_combinations([1, 2, 5], 5) == 4
    assert count_combinations([2], 3) == 0

    print("006_coin_change: all examples passed")
