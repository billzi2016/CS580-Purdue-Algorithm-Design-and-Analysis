"""
文件意图：手写实现快速选择，用于查找第 k 小元素。
适用场景：只需一个顺序统计量而不需要完整排序时。
核心思想：原地划分数组，根据 k 落入的分区继续处理一侧。
输入输出：输入可比较元素列表和从零开始的 k，返回第 k 小元素。
时间复杂度：平均 O(n)，最坏 O(n^2)。空间复杂度：O(n) 副本。
关键边界：空列表或越界 k 会抛出 IndexError；重复值由三向划分正确处理。
"""

from typing import TypeVar

T = TypeVar("T")


def quick_select(values: list[T], k: int) -> T:
    """返回 values 中从零开始计数的第 k 小元素。

    参数：values 为可比较元素列表；k 是目标秩。
    返回：第 k 小元素。
    边界情况：k 不在有效下标范围内时抛出 IndexError。
    关键算法点：三向划分后，等于枢轴的整个区间拥有相同秩值。
    """
    if k < 0 or k >= len(values):
        raise IndexError("k 必须是 values 的有效下标")
    work = values[:]
    left, right = 0, len(work) - 1
    while left <= right:
        pivot = work[(left + right) // 2]
        less, scan, greater = left, left, right
        # 循环不变量：左侧小于、中央等于、右侧大于枢轴；scan 右侧尚未分类。
        while scan <= greater:
            if work[scan] < pivot:
                work[less], work[scan] = work[scan], work[less]
                less += 1
                scan += 1
            elif work[scan] > pivot:
                work[scan], work[greater] = work[greater], work[scan]
                greater -= 1
            else:
                scan += 1
        if k < less:
            right = less - 1
        elif k > greater:
            left = greater + 1
        else:
            return work[k]
    raise RuntimeError("划分过程未能找到目标秩")


if __name__ == "__main__":
    assert quick_select([3], 0) == 3
    assert quick_select([7, 2, 1, 9, 5], 0) == 1
    assert quick_select([7, 2, 1, 9, 5], 2) == 5
    assert quick_select([4, 1, 4, 2, 4], 3) == 4
    try:
        quick_select([], 0)
        assert False, "空列表的选择应失败"
    except IndexError as error:
        assert "有效下标" in str(error)
    print("007_quick_select: all examples passed")
