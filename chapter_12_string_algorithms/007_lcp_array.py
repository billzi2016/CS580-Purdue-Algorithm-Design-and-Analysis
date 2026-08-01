"""
文件意图：手写实现 Kasai 算法构造相邻后缀的 LCP 数组。
适用场景：与后缀数组配合进行最长重复子串、子串比较或后缀树替代查询。
核心思想：相邻文本位置的后缀最长公共前缀长度最多只会下降一，因此复用 h - 1。
输入输出：输入文本及其后缀数组，返回对应的 LCP 数组。
时间复杂度：O(n)。空间复杂度：O(n)。
关键边界：空文本对应空数组；后缀数组必须是 0 到 n-1 的完整排列。
"""


def lcp_array(text: str, suffixes: list[int]) -> list[int]:
    """返回与 suffixes 对齐的 LCP 数组。

    参数：text 是原字符串，suffixes 是其后缀数组。
    返回：result[0] 为 0，result[i] 是 suffixes[i] 与 suffixes[i-1] 的 LCP 长度。
    边界情况：空文本只能搭配空后缀数组；非法排列抛出 ValueError。
    关键算法点：比较 text[i:] 后把起点右移一位，至少保留此前匹配长度减一。
    """
    length = len(text)
    if len(suffixes) != length or set(suffixes) != set(range(length)):
        raise ValueError("suffixes 必须是 text 下标的完整排列")
    if length == 0:
        return []
    rank = [0] * length
    for position, suffix_start in enumerate(suffixes):
        rank[suffix_start] = position
    result = [0] * length
    matched = 0
    for start in range(length):
        position = rank[start]
        if position == 0:
            matched = 0
            continue
        previous_start = suffixes[position - 1]
        while (
            start + matched < length
            and previous_start + matched < length
            and text[start + matched] == text[previous_start + matched]
        ):
            matched += 1
        result[position] = matched
        if matched > 0:
            matched -= 1
    return result


if __name__ == "__main__":
    assert lcp_array("", []) == []
    assert lcp_array("banana", [5, 3, 1, 0, 4, 2]) == [0, 1, 3, 0, 0, 2]
    assert lcp_array("aaaa", [3, 2, 1, 0]) == [0, 1, 2, 3]
    try:
        lcp_array("abc", [0, 1])
        assert False, "非法后缀数组应被拒绝"
    except ValueError as error:
        assert "完整排列" in str(error)
    print("007_lcp_array: all examples passed")
