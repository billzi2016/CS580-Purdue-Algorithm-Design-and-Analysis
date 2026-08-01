"""
文件意图：手写单调队列计算滑动窗口最小值。
适用场景：固定长度窗口的在线最值查询。
核心思想：双端队列保存候选下标，且对应值从队首到队尾非递减。
输入输出：输入整数列表与窗口长度，返回每个完整窗口的最小值。
时间复杂度：O(n)。空间复杂度：O(k)。
关键边界：窗口长度必须在 1 到列表长度之间；重复最小值可正确处理。
"""

from collections import deque


def sliding_window_minimum(values: list[int], window: int) -> list[int]:
    """返回每个长度为 window 的滑动窗口最小值。

    参数：values 为整数列表，window 为正窗口长度。
    返回：从左至右各完整窗口的最小值。
    边界情况：window 非正或大于列表长度时抛出 ValueError。
    关键算法点：移除队尾所有不小于新值的候选，它们不可能再成为后续窗口最小值。
    """
    if window <= 0 or window > len(values):
        raise ValueError("window 必须在 1 到列表长度之间")

    candidates: deque[int] = deque()
    result: list[int] = []
    for index, value in enumerate(values):
        # 队首在窗口左侧时已失效。
        while candidates and candidates[0] <= index - window:
            candidates.popleft()
        while candidates and values[candidates[-1]] >= value:
            candidates.pop()
        candidates.append(index)
        if index >= window - 1:
            result.append(values[candidates[0]])

    return result


if __name__ == "__main__":
    assert sliding_window_minimum([1], 1) == [1]
    assert sliding_window_minimum([4, 2, 12, 3, 5, 1], 3) == [2, 2, 3, 1]
    assert sliding_window_minimum([2, 2, 2], 2) == [2, 2]
    try:
        sliding_window_minimum([], 1)
        assert False, "空数组上的非空窗口应被拒绝"
    except ValueError as error:
        assert "window" in str(error)
    print("003_monotonic_queue: all examples passed")
