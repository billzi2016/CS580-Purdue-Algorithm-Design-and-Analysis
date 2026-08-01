"""
文件意图：手写实现中位数的中位数确定性选择。
适用场景：需要第 k 小元素并要求 O(n) 最坏时间复杂度时。
核心思想：分成至多五个元素的小组，递归选择组中位数的中位数作为良好枢轴。
输入输出：输入可比较元素列表和从零开始的 k，返回第 k 小元素。
时间复杂度：O(n) 最坏情况。空间复杂度：O(n)，用于分组与三向划分。
关键边界：空列表或越界 k 会抛出 IndexError；重复值通过三向划分处理。
"""

from typing import TypeVar

T = TypeVar("T")


def _insertion_sorted(values: list[T]) -> list[T]:
    """返回 values 的手写插入排序副本，供固定大小小组使用。"""
    result = values[:]
    for index in range(1, len(result)):
        current = result[index]
        position = index - 1
        while position >= 0 and result[position] > current:
            result[position + 1] = result[position]
            position -= 1
        result[position + 1] = current
    return result


def median_of_medians_select(values: list[T], k: int) -> T:
    """返回 values 中从零开始计数的第 k 小元素。

    参数：values 为可比较元素列表；k 是目标秩。
    返回：第 k 小元素。
    边界情况：空列表或越界 k 抛出 IndexError。
    关键算法点：五元组中位数的中位数保证每轮至少丢弃固定比例元素。
    """
    if k < 0 or k >= len(values):
        raise IndexError("k 必须是 values 的有效下标")
    if len(values) <= 5:
        return _insertion_sorted(values)[k]

    group_medians: list[T] = []
    for start in range(0, len(values), 5):
        group = _insertion_sorted(values[start : start + 5])
        group_medians.append(group[len(group) // 2])
    pivot = median_of_medians_select(group_medians, len(group_medians) // 2)

    lower: list[T] = []
    equal: list[T] = []
    higher: list[T] = []
    for value in values:
        if value < pivot:
            lower.append(value)
        elif value > pivot:
            higher.append(value)
        else:
            equal.append(value)
    if k < len(lower):
        return median_of_medians_select(lower, k)
    if k < len(lower) + len(equal):
        return pivot
    return median_of_medians_select(higher, k - len(lower) - len(equal))


if __name__ == "__main__":
    assert median_of_medians_select([8], 0) == 8
    assert median_of_medians_select([12, 3, 5, 7, 4, 19, 26], 3) == 7
    assert median_of_medians_select([4, 2, 5, 2, 9, 2, 1], 2) == 2
    assert median_of_medians_select([9, 8, 7, 6, 5, 4, 3, 2, 1], 0) == 1
    try:
        median_of_medians_select([], 0)
        assert False, "空列表的选择应失败"
    except IndexError as error:
        assert "有效下标" in str(error)
    print("008_median_of_medians: all examples passed")
