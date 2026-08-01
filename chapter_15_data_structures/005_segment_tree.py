"""
文件意图：手写实现迭代线段树，支持点赋值和区间和。
适用场景：底层数组会变化，且需要反复进行区间聚合查询时。
核心思想：叶子保存数组元素，父节点始终保存两个子区间的和。
输入输出：支持点赋值与半开区间求和。
时间复杂度：构建 O(n)，更新与查询 O(log n)。空间复杂度：O(n)。
关键边界：空数组允许空区间查询；所有下标和区间都会检查。
"""


class SegmentTree:
    """从零开始下标、使用半开区间的整数求和线段树。"""

    def __init__(self, values: list[int]) -> None:
        """以 values 构建线段树。

        参数：values 为初始整数列表。
        返回：无，树内部使用补零的 2 的幂容量。
        边界情况：空列表仍建立可查询 [0, 0) 的树。
        关键算法点：父节点的值始终等于两个孩子区间和，因此自底向上一次遍历即可建树。
        """
        self.length = len(values)
        self.size = 1
        while self.size < self.length:
            self.size *= 2
        self.tree = [0] * (2 * self.size)
        for index, value in enumerate(values):
            self.tree[self.size + index] = value
        for node in range(self.size - 1, 0, -1):
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def set(self, index: int, value: int) -> None:
        """把 index 位置赋值为 value。

        参数：index 是有效下标，value 是新整数值。
        返回：无。
        边界情况：无效下标抛出 IndexError。
        关键算法点：叶子改变后只需要沿根路径重算父节点。
        """
        if index < 0 or index >= self.length:
            raise IndexError("下标越界")
        node = self.size + index
        self.tree[node] = value
        while node > 1:
            node //= 2
            self.tree[node] = self.tree[2 * node] + self.tree[2 * node + 1]

    def range_sum(self, left: int, right: int) -> int:
        """返回半开区间 [left, right) 的元素和。

        参数：left、right 是半开区间边界。
        返回：区间内整数和。
        边界情况：空区间返回零；逆序或越界区间抛出 IndexError。
        关键算法点：每次选取恰好完全落在查询范围内的左右边界节点。
        """
        if left < 0 or left > right or right > self.length:
            raise IndexError("区间越界")
        left += self.size
        right += self.size
        total = 0
        while left < right:
            if left & 1:
                total += self.tree[left]
                left += 1
            if right & 1:
                right -= 1
                total += self.tree[right]
            left //= 2
            right //= 2
        return total


if __name__ == "__main__":
    tree = SegmentTree([1, 2, 3, 4])
    assert tree.range_sum(1, 3) == 5
    tree.set(1, 8)
    assert tree.range_sum(0, 2) == 9
    assert SegmentTree([]).range_sum(0, 0) == 0
    print("005_segment_tree: all examples passed")
