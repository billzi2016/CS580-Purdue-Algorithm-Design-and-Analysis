"""
随机化选择：期望线性时间寻找第 k 小元素。

本文件的意图：
1. 手写 Quickselect，不通过排序“一击必杀”。
2. 使用三路划分处理重复元素，避免 k 落在大量相等元素区域时继续递归。
3. k 采用 0-based 下标，和 Python 序列习惯保持一致。

复杂度：
- 期望 O(n)。
- 最坏 O(n^2)，但随机 pivot 使固定输入难以稳定触发最坏情况。
"""

from random import Random


def randomized_select(values: list[int], k: int, seed: int | None = None) -> int:
    """返回 values 中第 k 小的元素，k 从 0 开始。

    函数会复制输入列表，因此不会修改调用方数据。k 越界时抛出 IndexError，
    这比静默返回错误值更适合维护和调试。
    """

    if not 0 <= k < len(values):
        raise IndexError("k 必须满足 0 <= k < len(values)")

    numbers = values[:]
    rng = Random(seed)
    left = 0
    right = len(numbers) - 1

    while left <= right:
        pivot = numbers[rng.randint(left, right)]
        less, greater = _partition_three_way(numbers, left, right, pivot)

        if k < less:
            right = less - 1
        elif k > greater:
            left = greater + 1
        else:
            return numbers[k]

    raise RuntimeError("quickselect 状态不应走到这里")


def _partition_three_way(
    numbers: list[int],
    left: int,
    right: int,
    pivot: int,
) -> tuple[int, int]:
    """围绕 pivot 三路划分，返回等于 pivot 的闭区间边界。"""

    less = left
    index = left
    greater = right

    while index <= greater:
        if numbers[index] < pivot:
            numbers[less], numbers[index] = numbers[index], numbers[less]
            less += 1
            index += 1
        elif numbers[index] > pivot:
            numbers[index], numbers[greater] = numbers[greater], numbers[index]
            greater -= 1
        else:
            index += 1

    return less, greater


if __name__ == "__main__":
    data = [9, 1, 8, 2, 7, 3, 6]
    assert randomized_select(data, 0, seed=1) == 1
    assert randomized_select(data, 3, seed=1) == 6
    assert randomized_select(data, 6, seed=1) == 9
    assert randomized_select([5, 5, 1, 5, 2], 2, seed=5) == 5
    assert data == [9, 1, 8, 2, 7, 3, 6]

    print("002_randomized_select: all examples passed")
