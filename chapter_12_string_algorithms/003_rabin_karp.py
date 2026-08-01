"""
文件意图：手写实现 Rabin-Karp 单模式字符串匹配。
适用场景：需要使用滚动哈希快速过滤候选位置，或作为多模式哈希匹配的基础时。
核心思想：维护长度等于模式串的窗口哈希，窗口右移时 O(1) 更新哈希。
输入输出：输入文本和模式串，返回所有匹配起始下标。
时间复杂度：平均 O(n + m)，最坏 O(nm)。空间复杂度：O(1)。
关键边界：空模式串匹配每个边界；哈希相等后逐字符验证以避免碰撞误报。
"""


def rabin_karp_search(
    text: str, pattern: str, base: int = 257, modulus: int = 1_000_000_007
) -> list[int]:
    """返回 pattern 在 text 中全部（可重叠）出现的起始下标。

    参数：text、pattern 为字符串；base 和 modulus 是正的滚动哈希参数。
    返回：全部匹配起始下标。
    边界情况：空模式串匹配所有边界，模式长于文本返回空。
    关键算法点：哈希相等只是候选，仍逐字符确认真实匹配。
    """
    if base <= 0 or modulus <= 1:
        raise ValueError("base 必须为正且 modulus 必须大于 1")
    pattern_length = len(pattern)
    if pattern_length == 0:
        return list(range(len(text) + 1))
    if pattern_length > len(text):
        return []
    highest_power = pow(base, pattern_length - 1, modulus)
    pattern_hash = window_hash = 0
    for index in range(pattern_length):
        pattern_hash = (pattern_hash * base + ord(pattern[index])) % modulus
        window_hash = (window_hash * base + ord(text[index])) % modulus
    matches: list[int] = []
    for start in range(len(text) - pattern_length + 1):
        if (
            window_hash == pattern_hash
            and text[start : start + pattern_length] == pattern
        ):
            matches.append(start)
        if start + pattern_length < len(text):
            window_hash = (window_hash - ord(text[start]) * highest_power) % modulus
            window_hash = (
                window_hash * base + ord(text[start + pattern_length])
            ) % modulus
    return matches


if __name__ == "__main__":
    assert rabin_karp_search("ababa", "aba") == [0, 2]
    assert rabin_karp_search("aaaa", "aa") == [0, 1, 2]
    assert rabin_karp_search("abc", "") == [0, 1, 2, 3]
    assert rabin_karp_search("abc", "abcd") == []
    assert rabin_karp_search("abcabc", "abc", 3, 101) == [0, 3]
    print("003_rabin_karp: all examples passed")
