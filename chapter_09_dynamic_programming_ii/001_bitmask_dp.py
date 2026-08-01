"""
文件意图：
    本文件手写实现状压 DP，以旅行商路径（TSP path）为例展示集合状态压缩。

适用场景：
    n 较小、状态可以用二进制集合表示的问题，例如访问子集、任务集合、匹配状态。

核心思想：
    mask 表示已经访问的节点集合，dp[mask][last] 表示访问 mask 且最后停在 last 的最小代价。

时间复杂度：
    O(2^n * n^2)

空间复杂度：
    O(2^n * n)
"""


def shortest_hamiltonian_path_cost(cost: list[list[int]], start: int = 0) -> int:
    """返回从 start 出发访问所有节点一次的最短路径代价，不要求回到起点。"""
    n = len(cost)
    if n == 0:
        return 0
    if any(len(row) != n for row in cost):
        raise ValueError("cost 必须是方阵")
    if not 0 <= start < n:
        raise ValueError("start 超出范围")

    full_mask = 1 << n
    infinity = 10**18
    dp = [[infinity] * n for _ in range(full_mask)]
    dp[1 << start][start] = 0

    for mask in range(full_mask):
        for last in range(n):
            if dp[mask][last] == infinity:
                continue
            for nxt in range(n):
                if mask & (1 << nxt):
                    continue
                next_mask = mask | (1 << nxt)
                dp[next_mask][nxt] = min(
                    dp[next_mask][nxt], dp[mask][last] + cost[last][nxt]
                )

    return min(dp[full_mask - 1])


if __name__ == "__main__":
    matrix = [
        [0, 10, 15, 20],
        [10, 0, 35, 25],
        [15, 35, 0, 30],
        [20, 25, 30, 0],
    ]
    assert shortest_hamiltonian_path_cost(matrix, 0) == 65
    assert shortest_hamiltonian_path_cost([[0]], 0) == 0
    assert shortest_hamiltonian_path_cost([], 0) == 0

    print("001_bitmask_dp: all examples passed")
