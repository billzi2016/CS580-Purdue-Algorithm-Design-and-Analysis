"""
文件意图：
    本文件手写实现区间 DP，以矩阵链乘法最小代价为例。

适用场景：
    问题可按连续区间拆分，最优解依赖区间内某个切分点。

核心思想：
    dp[left][right] 表示从第 left 个矩阵乘到第 right 个矩阵的最小标量乘法次数。

时间复杂度：
    O(n^3)

空间复杂度：
    O(n^2)
"""


def matrix_chain_min_cost(dimensions: list[int]) -> int:
    """给定矩阵维度链，返回最少标量乘法次数。"""
    if len(dimensions) < 2:
        raise ValueError("至少需要一个矩阵的维度")
    n = len(dimensions) - 1
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n + 1):
        for left in range(0, n - length + 1):
            right = left + length - 1
            dp[left][right] = 10**18
            for split in range(left, right):
                cost = (
                    dp[left][split]
                    + dp[split + 1][right]
                    + dimensions[left] * dimensions[split + 1] * dimensions[right + 1]
                )
                dp[left][right] = min(dp[left][right], cost)

    return dp[0][n - 1]


if __name__ == "__main__":
    assert matrix_chain_min_cost([10, 30, 5, 60]) == 4500
    assert matrix_chain_min_cost([40, 20, 30, 10, 30]) == 26000
    assert matrix_chain_min_cost([5, 10]) == 0

    print("004_interval_dp: all examples passed")
