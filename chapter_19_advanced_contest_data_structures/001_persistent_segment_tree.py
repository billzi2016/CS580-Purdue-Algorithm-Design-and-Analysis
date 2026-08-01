"""
文件意图：手写实现路径复制式可持久化线段树。
适用场景：数组有多个历史版本，且需要对任一版本执行点赋值与区间和查询。
核心思想：每次更新只复制根到叶的一条路径，未受影响子树与历史版本共享。
输入输出：从初始数组构建版本 0；update 返回新版本编号，range_sum 查询指定版本。
时间复杂度：构建 O(n)，单次更新与查询 O(log n)。空间复杂度：每次更新额外 O(log n)。
关键边界：空数组只允许查询空区间；所有版本、下标与半开区间都会验证。
"""


class _Node:
    """持久化线段树节点，保存区间和与两个不可变子引用。"""

    def __init__(self, total: int, left: _Node | None = None, right: _Node | None = None) -> None:
        self.total = total
        self.left = left
        self.right = right


class PersistentSegmentTree:
    """支持版本化点赋值与区间和的可持久化线段树。"""

    def __init__(self, values: list[int]) -> None:
        """以 values 创建第 0 个版本。

        参数：values 为初始整数数组。
        返回：无。
        边界情况：空数组创建一个空版本，仅允许查询 [0, 0)。
        关键算法点：初始构建后节点从不修改，以确保旧版本始终可访问。
        """
        self.length = len(values)
        self._roots: list[_Node | None] = [self._build(values, 0, self.length) if values else None]

    def _build(self, values: list[int], left: int, right: int) -> _Node:
        """递归构建 [left, right) 的初始节点。"""
        if right - left == 1:
            return _Node(values[left])
        middle = (left + right) // 2
        left_child = self._build(values, left, middle)
        right_child = self._build(values, middle, right)
        return _Node(left_child.total + right_child.total, left_child, right_child)

    def update(self, version: int, index: int, value: int) -> int:
        """基于 version 把 index 赋值为 value，并返回新版本编号。

        参数：version 是已有版本，index 是有效数组下标，value 是新整数值。
        返回：追加到版本列表的新版本编号。
        边界情况：空数组或非法版本/下标抛出 IndexError。
        关键算法点：只复制更新路径，其余节点由新旧版本共享。
        """
        self._check_version(version)
        if index < 0 or index >= self.length:
            raise IndexError("下标越界")
        root = self._update(self._roots[version], 0, self.length, index, value)
        self._roots.append(root)
        return len(self._roots) - 1

    def _update(self, node: _Node | None, left: int, right: int, index: int, value: int) -> _Node:
        """路径复制 [left, right) 中 index 所在节点。"""
        if node is None:
            raise RuntimeError("非空更新不应访问空根")
        if right - left == 1:
            return _Node(value)
        middle = (left + right) // 2
        if index < middle:
            left_child = self._update(node.left, left, middle, index, value)
            right_child = node.right
        else:
            left_child = node.left
            right_child = self._update(node.right, middle, right, index, value)
        if left_child is None or right_child is None:
            raise RuntimeError("内部节点必须拥有两个孩子")
        return _Node(left_child.total + right_child.total, left_child, right_child)

    def range_sum(self, version: int, query_left: int, query_right: int) -> int:
        """查询指定版本中半开区间 [query_left, query_right) 的和。

        参数：version 是已有版本，query_left/query_right 是半开区间边界。
        返回：该版本对应区间和。
        边界情况：空区间为零；非法版本或范围抛出 IndexError。
        关键算法点：完全覆盖时直接使用节点汇总，部分覆盖时递归合并两个孩子。
        """
        self._check_version(version)
        if query_left < 0 or query_left > query_right or query_right > self.length:
            raise IndexError("区间越界")
        if self.length == 0:
            return 0
        return self._range_sum(self._roots[version], 0, self.length, query_left, query_right)

    def _range_sum(self, node: _Node | None, left: int, right: int, query_left: int, query_right: int) -> int:
        """递归查询指定节点和目标区间的交集。"""
        if node is None or query_right <= left or right <= query_left:
            return 0
        if query_left <= left and right <= query_right:
            return node.total
        middle = (left + right) // 2
        return self._range_sum(node.left, left, middle, query_left, query_right) + self._range_sum(node.right, middle, right, query_left, query_right)

    def _check_version(self, version: int) -> None:
        """验证 version 是已有版本编号。"""
        if version < 0 or version >= len(self._roots):
            raise IndexError("版本编号越界")


if __name__ == "__main__":
    tree = PersistentSegmentTree([1, 2, 3, 4])
    first_update = tree.update(0, 1, 8)
    second_update = tree.update(first_update, 3, -1)
    assert tree.range_sum(0, 0, 4) == 10
    assert tree.range_sum(first_update, 0, 2) == 9
    assert tree.range_sum(second_update, 1, 4) == 10
    assert PersistentSegmentTree([]).range_sum(0, 0, 0) == 0
    print("001_persistent_segment_tree: all examples passed")
