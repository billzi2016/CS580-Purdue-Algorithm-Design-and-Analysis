"""
文件意图：
    本文件手写实现 Levenshtein 编辑距离，用于计算两个字符串之间的最少编辑操作数。

适用场景：
    字符串纠错、相似度计算、序列比对基础。

核心思想：
    dp[i][j] 表示 word1 前 i 个字符变成 word2 前 j 个字符的最少操作数。
    三种操作分别是插入、删除和替换。

时间复杂度：
    O(mn)

空间复杂度：
    O(mn)
"""


def edit_distance(first: str, second: str) -> int:
    """计算 first 到 second 的编辑距离。"""
    rows = len(first) + 1
    cols = len(second) + 1
    dp = [[0] * cols for _ in range(rows)]

    for i in range(rows):
        dp[i][0] = i
    for j in range(cols):
        dp[0][j] = j

    for i in range(1, rows):
        for j in range(1, cols):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])

    return dp[-1][-1]


if __name__ == "__main__":
    assert edit_distance("horse", "ros") == 3
    assert edit_distance("intention", "execution") == 5
    assert edit_distance("", "") == 0
    assert edit_distance("", "abc") == 3
    assert edit_distance("abc", "abc") == 0

    print("005_edit_distance: all examples passed")
