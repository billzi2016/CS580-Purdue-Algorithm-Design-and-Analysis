"""
文件意图：手写实现支持负整数的稳定计数排序。
适用场景：整数取值范围较小且需要线性时间排序时。
核心思想：统计每个值出现次数，再按值域顺序重建输出。
输入输出：输入整数列表，返回新的非递减排序列表。
时间复杂度：O(n + r)，r 为最大值与最小值之差加一。空间复杂度：O(r)。
关键边界：空列表直接返回；值域过大时不宜使用本算法。
"""


def counting_sort(values: list[int]) -> list[int]:
    """返回整数列表 values 的非递减排序副本。

    参数：values 为可包含负数和重复值的整数列表。
    返回：新排序列表。
    边界情况：空列表不访问最值，直接返回空列表。
    关键算法点：使用最小值偏移把任意整数映射到非负计数下标。
    """
    if not values:
        return []
    minimum = min(values)
    maximum = max(values)
    counts = [0] * (maximum - minimum + 1)
    for value in values:
        counts[value - minimum] += 1

    result: list[int] = []
    for offset, count in enumerate(counts):
        # 每次追加 count 个相同值，确保输出按值域递增。
        result.extend([offset + minimum] * count)
    return result


if __name__ == "__main__":
    assert counting_sort([]) == []
    assert counting_sort([0]) == [0]
    assert counting_sort([4, -2, 4, 0, -2, 1]) == [-2, -2, 0, 1, 4, 4]
    assert counting_sort([3, 2, 1]) == [1, 2, 3]
    print("004_counting_sort: all examples passed")
