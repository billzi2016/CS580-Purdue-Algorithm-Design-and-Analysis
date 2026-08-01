"""
文件意图：手写实现 Z Algorithm 与基于 Z 数组的字符串匹配。
适用场景：需要比较字符串任意后缀与整体前缀的长度，或进行线性时间模式匹配时。
核心思想：维护当前最右 Z-box，盒内位置可复用此前计算的前缀匹配长度。
输入输出：输入字符串得到 Z 数组；输入文本和模式得到全部匹配位置。
时间复杂度：O(n) 或 O(n + m)。空间复杂度：O(n) 或 O(n + m)。
关键边界：空串的 Z 数组为空；匹配时选择未出现在任一输入中的分隔符。
"""


def z_algorithm(text: str) -> list[int]:
    """返回 text 的 Z 数组。

    参数：text 为任意字符串。
    返回：z[i] 是 text[i:] 与 text 的最长公共前缀长度，z[0] 为 0。
    边界情况：空字符串返回空列表。
    关键算法点：区间 [left, right] 始终表示当前已知的最右前缀匹配区间。
    """
    z_values = [0] * len(text)
    left = right = 0
    for index in range(1, len(text)):
        if index <= right:
            z_values[index] = min(right - index + 1, z_values[index - left])
        while index + z_values[index] < len(text) and text[z_values[index]] == text[index + z_values[index]]:
            z_values[index] += 1
        if index + z_values[index] - 1 > right:
            left, right = index, index + z_values[index] - 1
    return z_values


def z_search(text: str, pattern: str) -> list[int]:
    """返回 pattern 在 text 中全部（可重叠）出现的起始下标。

    参数：text 为待搜索文本，pattern 为模式串。
    返回：所有匹配起始下标。
    边界情况：空模式串匹配全部边界。
    关键算法点：分隔符确保组合字符串中的前缀匹配不会跨越模式与文本边界。
    """
    if not pattern:
        return list(range(len(text) + 1))
    separator = "\x00"
    while separator in text or separator in pattern:
        separator += "\x00"
    combined = pattern + separator + text
    z_values = z_algorithm(combined)
    offset = len(pattern) + len(separator)
    return [index - offset for index in range(offset, len(combined)) if z_values[index] >= len(pattern)]


if __name__ == "__main__":
    assert z_algorithm("aabxaabx") == [0, 1, 0, 0, 4, 1, 0, 0]
    assert z_search("ababa", "aba") == [0, 2]
    assert z_search("aaaa", "aa") == [0, 1, 2]
    assert z_search("abc", "") == [0, 1, 2, 3]
    assert z_search("abc", "d") == []
    print("002_z_algorithm: all examples passed")
