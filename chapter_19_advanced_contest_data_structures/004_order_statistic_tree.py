"""
文件意图：手写实现支持重复键的顺序统计 Treap。
适用场景：动态多重集合，需要插入、删除、排名与第 k 小元素查询。
核心思想：BST 按键有序，Treap 按优先级成堆，子树大小把键顺序映射为秩。
输入输出：支持 insert、discard、rank、kth 与 count。
时间复杂度：各操作期望 O(log n)。空间复杂度：O(n)。
关键边界：重复键用 count 聚合；kth 使用从零开始的 k，非法 k 抛出 IndexError。
"""


class _Node:
    """顺序统计 Treap 节点，包含键、重复数、优先级和子树元素总数。"""

    def __init__(self, key: int, priority: int) -> None:
        self.key = key
        self.priority = priority
        self.count = 1
        self.size = 1
        self.left: _Node | None = None
        self.right: _Node | None = None


def _size(node: _Node | None) -> int:
    """返回节点子树的总元素数，空节点为零。"""
    return node.size if node is not None else 0


def _refresh(node: _Node | None) -> None:
    """重新计算节点的子树元素数。"""
    if node is not None:
        node.size = node.count + _size(node.left) + _size(node.right)


class OrderStatisticTree:
    """基于手写 Treap 的整数多重集合。"""

    def __init__(self) -> None:
        """创建空多重集合。

        参数：无。
        返回：无。
        边界情况：空集合的长度为零。
        关键算法点：确定性伪随机优先级避免依赖随机库并保持测试可复现。
        """
        self._root: _Node | None = None
        self._seed = 7

    def _priority(self) -> int:
        """生成确定性伪随机优先级。"""
        self._seed = (1664525 * self._seed + 1013904223) & 0x7FFFFFFF
        return self._seed

    def _rotate_right(self, node: _Node) -> _Node:
        """右旋 node，使左孩子提升并恢复局部堆序。"""
        child = node.left
        if child is None:
            return node
        node.left = child.right
        child.right = node
        _refresh(node)
        _refresh(child)
        return child

    def _rotate_left(self, node: _Node) -> _Node:
        """左旋 node，使右孩子提升并恢复局部堆序。"""
        child = node.right
        if child is None:
            return node
        node.right = child.left
        child.left = node
        _refresh(node)
        _refresh(child)
        return child

    def insert(self, key: int) -> None:
        """插入一个 key。

        参数：key 为整数。
        返回：无。
        边界情况：重复键仅增加同一节点 count。
        关键算法点：递归插入后若孩子优先级更高，通过旋转恢复堆序。
        """

        def visit(node: _Node | None) -> _Node:
            if node is None:
                return _Node(key, self._priority())
            if key == node.key:
                node.count += 1
            elif key < node.key:
                node.left = visit(node.left)
                if node.left is not None and node.left.priority < node.priority:
                    node = self._rotate_right(node)
            else:
                node.right = visit(node.right)
                if node.right is not None and node.right.priority < node.priority:
                    node = self._rotate_left(node)
            _refresh(node)
            return node

        self._root = visit(self._root)

    def discard(self, key: int) -> bool:
        """删除一个 key，若不存在则不修改集合。

        参数：key 为整数。
        返回：删除成功为 True，否则 False。
        边界情况：重复键仅减 count；删除最后一个副本才移除节点。
        关键算法点：两个孩子都存在时先旋转优先级更高的孩子，再继续删除。
        """
        removed = False

        def visit(node: _Node | None) -> _Node | None:
            nonlocal removed
            if node is None:
                return None
            if key < node.key:
                node.left = visit(node.left)
            elif key > node.key:
                node.right = visit(node.right)
            else:
                removed = True
                if node.count > 1:
                    node.count -= 1
                elif node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
                elif node.left.priority < node.right.priority:
                    node = self._rotate_right(node)
                    node.right = visit(node.right)
                else:
                    node = self._rotate_left(node)
                    node.left = visit(node.left)
            _refresh(node)
            return node

        self._root = visit(self._root)
        return removed

    def rank(self, key: int) -> int:
        """返回严格小于 key 的元素个数。

        参数：key 为整数。
        返回：从零开始的插入秩。
        边界情况：空集合返回零，key 不存在也返回其应插入位置。
        关键算法点：向右走时把左子树和当前节点重复数都计入答案。
        """
        node = self._root
        result = 0
        while node is not None:
            if key <= node.key:
                node = node.left
            else:
                result += _size(node.left) + node.count
                node = node.right
        return result

    def kth(self, k: int) -> int:
        """返回从零开始第 k 小元素。

        参数：k 是有效秩。
        返回：对应整数键。
        边界情况：k 越界抛出 IndexError。
        关键算法点：左子树大小和节点 count 将 k 定位到左、当前或右子树。
        """
        if k < 0 or k >= len(self):
            raise IndexError("秩越界")
        node = self._root
        while node is not None:
            left_size = _size(node.left)
            if k < left_size:
                node = node.left
            elif k < left_size + node.count:
                return node.key
            else:
                k -= left_size + node.count
                node = node.right
        raise RuntimeError("有效秩必须可达")

    def count(self, key: int) -> int:
        """返回 key 的出现次数。

        参数：key 为整数。
        返回：非负出现次数。
        边界情况：不存在键返回零。
        关键算法点：BST 查找只沿一条根到叶路径。
        """
        node = self._root
        while node is not None:
            if key == node.key:
                return node.count
            node = node.left if key < node.key else node.right
        return 0

    def __len__(self) -> int:
        """返回多重集合元素总数。

        参数：无。
        返回：包含重复元素的数量。
        边界情况：空集合返回零。
        关键算法点：根节点 size 汇总所有子树与重复数。
        """
        return _size(self._root)


if __name__ == "__main__":
    tree = OrderStatisticTree()
    for value in [5, 1, 5, 3, 2]:
        tree.insert(value)
    assert len(tree) == 5 and tree.count(5) == 2
    assert [tree.kth(index) for index in range(len(tree))] == [1, 2, 3, 5, 5]
    assert tree.rank(5) == 3
    assert tree.discard(5) and tree.count(5) == 1
    assert not tree.discard(9)
    print("004_order_statistic_tree: all examples passed")
