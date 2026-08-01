"""
文件意图：
    本文件手写实现最长公共子序列（LCS）动态规划，并支持还原一个 LCS。

适用场景：
    字符串比较、diff 工具、序列相似度分析。

核心思想：
    dp[i][j] 表示 first 前 i 个字符和 second 前 j 个字符的 LCS 长度。
    若末尾字符相同，则来自 dp[i-1][j-1]+1；否则取删除一侧后的较优值。

时间复杂度：
    O(mn)

空间复杂度：
    O(mn)
"""


def longest_common_subsequence_length(first: str, second: str) -> int:
    """返回 LCS 长度。"""
    return _build_lcs_table(first, second)[-1][-1]


def reconstruct_lcs(first: str, second: str) -> str:
    """还原一个最长公共子序列。"""
    dp = _build_lcs_table(first, second)
    i, j = len(first), len(second)
    result: list[str] = []

    while i > 0 and j > 0:
        if first[i - 1] == second[j - 1]:
            result.append(first[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    result.reverse()
    return "".join(result)


def _build_lcs_table(first: str, second: str) -> list[list[int]]:
    """构建 LCS DP 表。"""
    dp = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    for i in range(1, len(first) + 1):
        for j in range(1, len(second) + 1):
            if first[i - 1] == second[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


if __name__ == "__main__":
    assert longest_common_subsequence_length("abcde", "ace") == 3
    assert reconstruct_lcs("abcde", "ace") == "ace"
    assert longest_common_subsequence_length("abc", "def") == 0
    assert reconstruct_lcs("abc", "def") == ""
    assert longest_common_subsequence_length("", "abc") == 0

    print("007_longest_common_subsequence: all examples passed")
