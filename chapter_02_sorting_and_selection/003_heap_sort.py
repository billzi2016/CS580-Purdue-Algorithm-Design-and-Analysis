"""
文件意图：手写实现原地堆排序。
适用场景：需要 O(1) 辅助空间且能接受不稳定排序时。
核心思想：先建最大堆，再反复将堆顶最大值交换到数组末尾并向下调整。
输入输出：输入可比较元素列表，返回新的非递减排序列表。
时间复杂度：O(n log n)。空间复杂度：O(n)，用于不修改调用者列表的副本。
关键边界：空列表、单元素和重复元素均可处理。
"""

from typing import TypeVar

T = TypeVar("T")


def _sift_down(heap: list[T], root: int, size: int) -> None:
    """将 root 向下调整，使以 root 为根的子树恢复最大堆性质。"""
    while True:
        largest = root
        left = 2 * root + 1
        right = left + 1
        if left < size and heap[left] > heap[largest]:
            largest = left
        if right < size and heap[right] > heap[largest]:
            largest = right
        if largest == root:
            return
        heap[root], heap[largest] = heap[largest], heap[root]
        root = largest


def heap_sort(values: list[T]) -> list[T]:
    """返回 values 的非递减排序副本。

    参数：values 为彼此可比较的元素列表。
    返回：不修改原列表的新排序列表。
    边界情况：长度小于等于一时直接返回副本。
    关键算法点：堆大小逐步缩小，已移至尾部的元素不再参与调整。
    """
    heap = values[:]
    for root in range(len(heap) // 2 - 1, -1, -1):
        _sift_down(heap, root, len(heap))
    for end in range(len(heap) - 1, 0, -1):
        heap[0], heap[end] = heap[end], heap[0]
        _sift_down(heap, 0, end)
    return heap


if __name__ == "__main__":
    assert heap_sort([]) == []
    assert heap_sort([2]) == [2]
    assert heap_sort([4, 1, 6, 1, 2]) == [1, 1, 2, 4, 6]
    assert heap_sort([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]
    print("003_heap_sort: all examples passed")
