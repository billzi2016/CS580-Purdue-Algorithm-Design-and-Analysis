"""教学版 LCP（最长公共前缀）数组。

适用场景：结合后缀数组描述相邻后缀的重复程度，是重复序列、BWT 和全文索引的基础组件。
核心思想：Kasai 算法复用相邻文本位置的公共前缀下界，使字符比较总量保持线性。
输入输出：输入文本与其后缀数组，输出同长 LCP 数组，首项固定为零。
时间复杂度：O(n)，空间复杂度 O(n)。
关键边界情况：空文本只接受空数组；后缀数组必须恰为 0..n-1 的排列；重复字符可产生长 LCP。
"""


def build_lcp_array(text: str, suffix_array: list[int]) -> list[int]:
    """使用 Kasai 算法构建与后缀数组同长的 LCP 数组。

    参数：text 为文本，suffix_array 为其字典序后缀起点排列。
    返回：lcp[rank] 是 suffix_array[rank-1] 与 suffix_array[rank] 的最长公共前缀长度，lcp[0] 为 0。
    边界情况：空文本返回空列表；不合法下标、重复下标或不匹配排序均抛出 ValueError。
    关键算法点：当前位置与其后继后缀的 LCP 至少是上一个 LCP 减一，因为两后缀都向右移动一格。
    """
    _validate_suffix_array(text, suffix_array)
    size = len(text)
    if size == 0:
        return []
    rank = [0] * size
    for position, start in enumerate(suffix_array):
        rank[start] = position
    lcp = [0] * size
    common = 0
    for start in range(size):
        position = rank[start]
        if position == 0:
            common = 0
            continue
        previous_start = suffix_array[position - 1]
        while (
            start + common < size
            and previous_start + common < size
            and text[start + common] == text[previous_start + common]
        ):
            common += 1
        lcp[position] = common
        # 下一轮的两个后缀都少了首字符，故保留的已知共同部分最多少一个。
        if common:
            common -= 1
    return lcp


def _validate_suffix_array(text: str, suffix_array: list[int]) -> None:
    """验证数组是文本后缀的完整且正确字典序排列，避免对错误索引给出误导性结果。"""
    expected = list(range(len(text)))
    if len(suffix_array) != len(text) or set(suffix_array) != set(expected):
        raise ValueError("后缀数组必须是 0 到 len(text)-1 的排列")
    for left, right in zip(suffix_array, suffix_array[1:]):
        if text[left:] > text[right:]:
            raise ValueError("后缀数组未按字典序排列")


if __name__ == "__main__":
    banana_suffix_array = [5, 3, 1, 0, 4, 2]
    assert build_lcp_array("banana", banana_suffix_array) == [0, 1, 3, 0, 0, 2]
    assert build_lcp_array("AAAA", [3, 2, 1, 0]) == [0, 1, 2, 3]
    assert build_lcp_array("", []) == []
    try:
        build_lcp_array("abc", [0, 2, 1])
        raise AssertionError("应拒绝非字典序后缀数组")
    except ValueError:
        pass
    print("012_lcp_array: all examples passed")
