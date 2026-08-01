"""
文件意图：手写实现数组存储的最小堆。
适用场景：动态维护一组整数的最小值，例如优先队列和堆排序的基础。
核心思想：把完全二叉树映射到数组；插入时上浮，删除堆顶时用末尾元素替换后下沉。
输入输出：支持从列表建堆、插入、查看和删除最小元素。
时间复杂度：建堆 O(n)，插入与删除 O(log n)，查看堆顶 O(1)。
空间复杂度：O(n)。
关键边界：允许空堆；对空堆查看或删除会抛出 IndexError。
"""

class MinHeap:
    """不借助 heapq 的最小堆。"""
    def __init__(self, values: list[int] | None = None) -> None:
        """以 values 建立最小堆。

        参数：values 是可选整数列表，调用者列表不会被修改。
        返回：无，实例保存堆化后的副本。
        边界情况：None 与空列表均创建空堆。
        关键算法点：从最后一个非叶节点逆序下沉可在线性时间完成建堆。
        """
        self._data = [] if values is None else values[:]
        for index in range(len(self._data) // 2 - 1, -1, -1):
            self._down(index)
    def _down(self, index: int) -> None:
        """使 index 向下移动直到子树满足最小堆不变量。"""
        while True:
            child = 2 * index + 1
            if child >= len(self._data): return
            if child + 1 < len(self._data) and self._data[child + 1] < self._data[child]:
                child += 1
            if self._data[index] <= self._data[child]:
                return
            self._data[index], self._data[child] = self._data[child], self._data[index]
            index = child
    def push(self, value: int) -> None:
        """插入 value；沿父链上浮以恢复堆序。"""
        self._data.append(value)
        index = len(self._data) - 1
        while index and self._data[(index - 1) // 2] > self._data[index]:
            parent = (index - 1) // 2
            self._data[parent], self._data[index] = self._data[index], self._data[parent]
            index = parent
    def peek(self) -> int:
        """返回最小值；空堆抛出 IndexError。"""
        if not self._data:
            raise IndexError("空堆没有最小值")
        return self._data[0]
    def pop(self) -> int:
        """删除并返回最小值；空堆抛出 IndexError。"""
        result = self.peek()
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._down(0)
        return result

    def __len__(self) -> int:
        """返回当前堆中元素数。

        参数：无。
        返回：非负整数元素数。
        边界情况：空堆返回零。
        关键算法点：数组长度就是完全二叉树的节点数。
        """
        return len(self._data)
if __name__ == "__main__":
    heap = MinHeap([5, 1, 4, 1])
    assert [heap.pop() for _ in range(len(heap))] == [1, 1, 4, 5]
    heap.push(3)
    assert heap.peek() == 3
    print("001_heap: all examples passed")
