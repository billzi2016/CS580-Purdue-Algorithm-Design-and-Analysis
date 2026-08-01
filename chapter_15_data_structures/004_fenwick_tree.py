"""
文件意图：手写实现 Fenwick 树维护动态前缀和。
适用场景：需要频繁点增量更新与区间和查询的整数数组。
核心思想：一号下标树节点 i 保存长度为 lowbit(i) 的后缀块之和。
输入输出：支持点加、半开前缀和与半开区间和。
时间复杂度：构建 O(n log n)，更新和查询 O(log n)。空间复杂度：O(n)。
关键边界：空数组可查询空前缀；所有下标与区间边界都会检查。
"""


class FenwickTree:
    """从零开始下标、维护整数和的 Fenwick 树。"""

    def __init__(self, values: list[int]) -> None:
        """按 values 构建 Fenwick 树。

        参数：values 为初始整数列表。
        返回：无，调用者列表不会被修改。
        边界情况：空列表会创建只有哨兵节点的空树。
        关键算法点：依次点加能够把每个元素贡献写入所有覆盖它的二进制块。
        """
        self.size = len(values)
        self.tree = [0] * (self.size + 1)
        for index, value in enumerate(values):
            self.add(index, value)

    def add(self, index: int, delta: int) -> None:
        """给指定位置累加 delta。

        参数：index 为从零开始的有效下标，delta 为增量。
        返回：无。
        边界情况：index 越界时抛出 IndexError。
        关键算法点：不断加 lowbit 可访问所有包含该元素的父级二进制块。
        """
        if index < 0 or index >= self.size:
            raise IndexError("下标越界")
        tree_index = index + 1
        while tree_index <= self.size:
            self.tree[tree_index] += delta
            tree_index += tree_index & -tree_index

    def prefix_sum(self, end: int) -> int:
        """返回半开区间 [0, end) 的元素和。

        参数：end 是允许取 0 和 size 的右边界。
        返回：前 end 个元素的和。
        边界情况：空前缀返回零，非法边界抛出 IndexError。
        关键算法点：不断减 lowbit 会把互不重叠的后缀块恰好拼成目标前缀。
        """
        if end < 0 or end > self.size:
            raise IndexError("边界越界")
        total = 0
        while end:
            total += self.tree[end]
            end -= end & -end
        return total

    def range_sum(self, left: int, right: int) -> int:
        """返回半开区间 [left, right) 的元素和。

        参数：left、right 为从零开始的半开区间边界。
        返回：该区间的整数和。
        边界情况：空区间返回零；逆序或越界区间抛出 IndexError。
        关键算法点：区间和等于两个前缀和之差。
        """
        if left < 0 or left > right or right > self.size:
            raise IndexError("区间越界")
        return self.prefix_sum(right) - self.prefix_sum(left)


if __name__ == "__main__":
    tree = FenwickTree([1, 2, 3, 4])
    assert tree.range_sum(1, 4) == 9
    tree.add(2, 5)
    assert tree.prefix_sum(3) == 11
    assert FenwickTree([]).prefix_sum(0) == 0
    print("004_fenwick_tree: all examples passed")
