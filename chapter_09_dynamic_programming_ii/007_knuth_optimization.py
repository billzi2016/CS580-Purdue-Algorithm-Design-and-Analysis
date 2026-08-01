"""
文件意图：
    本文件手写实现 Knuth 优化，以最优二叉搜索树 DP 为例。

适用场景：
    区间 DP 满足四边形不等式和决策单调性时，可把 O(n^3) 优化到 O(n^2)。

核心思想：
    dp[i][j] 的最优切分点 root[i][j] 位于 root[i][j-1] 到 root[i+1][j] 之间。

时间复杂度：
    O(n^2)

空间复杂度：
    O(n^2)
"""


def optimal_bst_cost(frequencies: list[int]) -> int:
    """给定有序 key 的访问频率，返回最优 BST 搜索代价。"""
    n = len(frequencies)
    if n == 0:
        return 0
    if any(freq < 0 for freq in frequencies):
        raise ValueError("频率必须非负")

    prefix = [0]
    for freq in frequencies:
        prefix.append(prefix[-1] + freq)

    dp = [[0] * n for _ in range(n)]
    root = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = frequencies[i]
        root[i][i] = i

    for length in range(2, n + 1):
        for left in range(0, n - length + 1):
            right = left + length - 1
            dp[left][right] = 10**18
            start = root[left][right - 1]
            end = root[left + 1][right]
            weight_sum = prefix[right + 1] - prefix[left]

            for candidate_root in range(start, end + 1):
                left_cost = dp[left][candidate_root - 1] if candidate_root > left else 0
                right_cost = (
                    dp[candidate_root + 1][right] if candidate_root < right else 0
                )
                cost = left_cost + right_cost + weight_sum
                if cost < dp[left][right]:
                    dp[left][right] = cost
                    root[left][right] = candidate_root

    return dp[0][n - 1]


if __name__ == "__main__":
    assert optimal_bst_cost([]) == 0
    assert optimal_bst_cost([10]) == 10
    assert optimal_bst_cost([10, 12]) == 32
    assert optimal_bst_cost([3, 3, 1]) == 11

    print("007_knuth_optimization: all examples passed")
