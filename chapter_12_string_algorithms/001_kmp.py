"""
文件意图：手写实现 KMP 单模式字符串匹配。
适用场景：在长文本中重复查找同一模式串，且需要线性时间保证时。
核心思想：失配时利用模式串前缀函数跳转，避免重新比较已经确认匹配的文本字符。
输入输出：输入文本与模式串，返回所有匹配起始下标。
时间复杂度：O(n + m)。空间复杂度：O(m)。
关键边界：空模式串匹配每个边界；模式串长于文本时返回空列表。
"""


def prefix_function(pattern: str) -> list[int]:
    """计算 pattern 的 KMP 前缀函数。

    参数：pattern 为任意字符串。
    返回：每个位置的最长真前后缀长度。
    边界情况：空串返回空列表。
    关键算法点：回退到此前已计算的前缀长度，不重新扫描旧字符。
    """
    prefix = [0] * len(pattern)
    matched = 0
    for index in range(1, len(pattern)):
        while matched > 0 and pattern[index] != pattern[matched]:
            matched = prefix[matched - 1]
        if pattern[index] == pattern[matched]:
            matched += 1
        prefix[index] = matched
    return prefix


def kmp_search(text: str, pattern: str) -> list[int]:
    """返回 pattern 在 text 中全部（可重叠）出现的起始下标。

    参数：text 为待搜索文本，pattern 为模式串。
    返回：所有匹配的从零开始下标。
    边界情况：空模式串返回从 0 到 len(text) 的全部边界。
    关键算法点：完成一次匹配后按前缀函数回退，因此重叠匹配不会遗漏。
    """
    if not pattern:
        return list(range(len(text) + 1))
    prefix = prefix_function(pattern)
    matches: list[int] = []
    matched = 0
    for index, character in enumerate(text):
        while matched > 0 and character != pattern[matched]:
            matched = prefix[matched - 1]
        if character == pattern[matched]:
            matched += 1
        if matched == len(pattern):
            matches.append(index - len(pattern) + 1)
            matched = prefix[matched - 1]
    return matches


if __name__ == "__main__":
    assert prefix_function("ababaca") == [0, 0, 1, 2, 3, 0, 1]
    assert kmp_search("ababa", "aba") == [0, 2]
    assert kmp_search("aaaa", "aa") == [0, 1, 2]
    assert kmp_search("abc", "") == [0, 1, 2, 3]
    assert kmp_search("abc", "abcd") == []
    print("001_kmp: all examples passed")
