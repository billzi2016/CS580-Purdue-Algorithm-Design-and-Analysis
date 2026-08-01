"""
随机化快速排序：用随机 pivot 降低输入排列对性能的控制能力。

本文件的意图：
1. 手写 quicksort 的 partition 过程，不调用内置 sort / sorted 完成核心排序。
2. 展示随机化算法的常见思想：不假设输入随机，而是由算法自己引入随机性。
3. 为了测试可复现，公开函数允许传入 seed；真实竞赛使用时可以不传 seed。

关键结论：
- 期望时间复杂度 O(n log n)。
- 最坏情况仍可能 O(n^2)，但随机 pivot 让对抗性输入更难稳定触发最坏路径。
"""

from random import Random


def randomized_quicksort(values: list[int], seed: int | None = None) -> list[int]:
    """返回 values 的升序副本，原列表不被修改。

    这里采用三路划分，原因是重复元素很多时，普通二路划分会产生大量无意义递归；
    三路划分把“小于 pivot / 等于 pivot / 大于 pivot”一次分开，更稳。
    """

    numbers = values[:]
    rng = Random(seed)
    _quicksort_in_place(numbers, 0, len(numbers) - 1, rng)
    return numbers


def _quicksort_in_place(numbers: list[int], left: int, right: int, rng: Random) -> None:
    """在闭区间 [left, right] 内原地排序。"""

    if left >= right:
        return

    pivot_index = rng.randint(left, right)
    pivot = numbers[pivot_index]

    # Dutch national flag 三路划分：
    # [left, less) < pivot, [less, index) == pivot, (greater, right] > pivot。
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

    _quicksort_in_place(numbers, left, less - 1, rng)
    _quicksort_in_place(numbers, greater + 1, right, rng)


if __name__ == "__main__":
    assert randomized_quicksort([3, 1, 2], seed=7) == [1, 2, 3]
    assert randomized_quicksort([5, 5, 1, 5, 2], seed=11) == [1, 2, 5, 5, 5]
    assert randomized_quicksort([], seed=1) == []
    assert randomized_quicksort([9], seed=1) == [9]
    original = [4, 3, 2, 1]
    assert randomized_quicksort(original, seed=3) == [1, 2, 3, 4]
    assert original == [4, 3, 2, 1]

    print("001_randomized_quicksort: all examples passed")
