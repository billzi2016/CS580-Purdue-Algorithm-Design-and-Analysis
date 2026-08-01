"""
文件意图：手写实现非负整数集合的 mex（minimum excluded value）及滑动窗口 mex 查询。
适用场景：Sprague-Grundy 递推、数组分段、缺失最小值与窗口统计问题。
核心思想：长度为 n 的数组的 mex 必在 [0,n] 内；窗口移动时维护该范围内每个值的出现次数。
输入输出：输入整数序列或窗口大小，输出 mex 或每个完整窗口的 mex 列表。
时间复杂度：单次 mex O(n)，滑动窗口总计 O(n+window)；空间复杂度 O(window)。
关键边界情况：负数不影响 mex；空序列 mex 为 0；窗口大小必须位于合法范围。
"""


def minimum_excluded(values: list[int]) -> int:
    """返回 values 中未出现的最小非负整数。

    参数：values 是任意整数列表。
    返回：该列表的 mex。
    边界情况：空列表返回 0；负数和大于长度的值无需记录。
    关键算法点：n 个元素最多覆盖 n 个非负候选，故答案不可能大于 n。
    """
    present = [False] * (len(values) + 1)
    for value in values:
        if 0 <= value <= len(values):
            present[value] = True
    for candidate, exists in enumerate(present):
        if not exists:
            return candidate
    raise AssertionError("长度为 n 的序列必有不超过 n 的 mex")


def sliding_window_mex(values: list[int], window_size: int) -> list[int]:
    """计算每个长度为 window_size 的连续窗口的 mex。

    参数：values 是整数序列；window_size 是正窗口长度。
    返回：按窗口起点顺序排列的 mex 列表。
    边界情况：空序列或窗口越界抛出 ValueError；窗口内负数与过大值被忽略。
    关键算法点：只维护 [0,window_size]，因为任何窗口 mex 均在该闭区间；指针单向推进寻找缺失值。
    """
    if window_size <= 0 or window_size > len(values):
        raise ValueError("window_size 必须位于 1 到 len(values) 之间")
    counts = [0] * (window_size + 1)

    def add(value: int, delta: int) -> None:
        if 0 <= value <= window_size:
            counts[value] += delta

    for value in values[:window_size]:
        add(value, 1)
    answers: list[int] = []
    for start in range(len(values) - window_size + 1):
        candidate = 0
        while counts[candidate] > 0:
            candidate += 1
        answers.append(candidate)
        if start + window_size < len(values):
            # 先移出左端再加入右端，使 counts 始终精确对应下一窗口。
            add(values[start], -1)
            add(values[start + window_size], 1)
    return answers


if __name__ == "__main__":
    assert minimum_excluded([]) == 0
    assert minimum_excluded([0, 1, 3, -1, 8]) == 2
    assert minimum_excluded([1, 2, 3]) == 0
    assert sliding_window_mex([0, 1, 2, 0, 1], 3) == [3, 3, 3]
    assert sliding_window_mex([5], 1) == [0]
    try:
        sliding_window_mex([1, 2], 0)
        raise AssertionError("零窗口应抛出 ValueError")
    except ValueError:
        pass
    print("003_mex: all examples passed")
