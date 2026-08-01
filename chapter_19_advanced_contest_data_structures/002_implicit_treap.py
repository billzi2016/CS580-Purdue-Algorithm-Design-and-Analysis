"""
文件意图：手写实现隐式 Treap，维护可按位置编辑的整数序列。
适用场景：需要在中间插入、删除、按位置读取及区间和的动态序列。
核心思想：BST 顺序由子树大小隐式决定，堆顺序由优先级决定；split/merge 维护两种不变量。
输入输出：支持 insert、remove、get 与 range_sum，位置均从零开始。
时间复杂度：期望 O(log n) 每次操作。空间复杂度：O(n)。
关键边界：非法位置或区间抛出 IndexError；使用确定性伪随机优先级使示例可复现。
"""


class _Node:
    """隐式 Treap 节点，保存值、优先级、子树大小和子树和。"""

    def __init__(self, value: int, priority: int) -> None:
        self.value = value
        self.priority = priority
        self.left: _Node | None = None
        self.right: _Node | None = None
        self.size = 1
        self.total = value


def _size(node: _Node | None) -> int:
    """返回节点子树大小，空子树大小为零。"""
    return node.size if node is not None else 0


def _total(node: _Node | None) -> int:
    """返回节点子树和，空子树和为零。"""
    return node.total if node is not None else 0


def _refresh(node: _Node | None) -> None:
    """根据两个孩子重新计算 node 的大小与和。"""
    if node is not None:
        node.size = 1 + _size(node.left) + _size(node.right)
        node.total = node.value + _total(node.left) + _total(node.right)


class ImplicitTreap:
    """使用隐式下标的序列 Treap。"""

    def __init__(self, values: list[int] | None = None) -> None:
        """用可选初始值创建序列。

        参数：values 为可选整数列表，调用者列表不会被修改。
        返回：无。
        边界情况：None 或空列表创建空序列。
        关键算法点：逐项 merge 保持中序顺序等于插入顺序。
        """
        self._root: _Node | None = None
        self._seed = 1
        if values is not None:
            for value in values:
                self.insert(len(self), value)

    def _next_priority(self) -> int:
        """生成可复现的伪随机优先级，避免依赖随机库。"""
        self._seed = (1103515245 * self._seed + 12345) & 0x7FFFFFFF
        return self._seed

    def _split(self, node: _Node | None, count: int) -> tuple[_Node | None, _Node | None]:
        """按前 count 个元素把 node 分成左右两棵 Treap。"""
        if node is None:
            return None, None
        if _size(node.left) >= count:
            left, node.left = self._split(node.left, count)
            _refresh(node)
            return left, node
        node.right, right = self._split(node.right, count - _size(node.left) - 1)
        _refresh(node)
        return node, right

    def _merge(self, left: _Node | None, right: _Node | None) -> _Node | None:
        """连接两个中序序列相邻的 Treap。"""
        if left is None:
            return right
        if right is None:
            return left
        if left.priority < right.priority:
            left.right = self._merge(left.right, right)
            _refresh(left)
            return left
        right.left = self._merge(left, right.left)
        _refresh(right)
        return right

    def insert(self, index: int, value: int) -> None:
        """在 index 前插入 value。

        参数：index 可取 0 到当前长度，value 为待插整数。
        返回：无。
        边界情况：index 越界抛出 IndexError。
        关键算法点：两次 split 把插入点隔开，再 merge 新单节点。
        """
        if index < 0 or index > len(self):
            raise IndexError("插入位置越界")
        left, right = self._split(self._root, index)
        self._root = self._merge(self._merge(left, _Node(value, self._next_priority())), right)

    def remove(self, index: int) -> int:
        """删除并返回 index 位置元素。

        参数：index 为有效位置。
        返回：原位置的整数值。
        边界情况：空序列或越界位置抛出 IndexError。
        关键算法点：第二次 split 精确隔离一个节点，剩余两段直接合并。
        """
        if index < 0 or index >= len(self):
            raise IndexError("删除位置越界")
        left, tail = self._split(self._root, index)
        middle, right = self._split(tail, 1)
        if middle is None:
            raise RuntimeError("有效位置必须对应节点")
        self._root = self._merge(left, right)
        return middle.value

    def get(self, index: int) -> int:
        """返回 index 位置元素。

        参数：index 为有效位置。
        返回：对应整数值。
        边界情况：无效位置抛出 IndexError。
        关键算法点：左子树大小将隐式中序位置转换为当前节点或右子树位置。
        """
        if index < 0 or index >= len(self):
            raise IndexError("查询位置越界")
        node = self._root
        while node is not None:
            left_size = _size(node.left)
            if index < left_size:
                node = node.left
            elif index == left_size:
                return node.value
            else:
                index -= left_size + 1
                node = node.right
        raise RuntimeError("有效位置必须可达")

    def range_sum(self, left: int, right: int) -> int:
        """返回半开区间 [left, right) 的和。

        参数：left、right 为半开区间边界。
        返回：区间整数和。
        边界情况：空区间返回零，非法范围抛出 IndexError。
        关键算法点：临时 split 读取中段汇总后必须按原顺序 merge 回去。
        """
        if left < 0 or left > right or right > len(self):
            raise IndexError("区间越界")
        first, tail = self._split(self._root, left)
        middle, last = self._split(tail, right - left)
        result = _total(middle)
        self._root = self._merge(first, self._merge(middle, last))
        return result

    def __len__(self) -> int:
        """返回序列长度。

        参数：无。
        返回：当前元素数。
        边界情况：空序列返回零。
        关键算法点：根节点维护的 size 是完整中序序列长度。
        """
        return _size(self._root)


if __name__ == "__main__":
    treap = ImplicitTreap([1, 3, 4])
    treap.insert(1, 2)
    assert [treap.get(index) for index in range(len(treap))] == [1, 2, 3, 4]
    assert treap.range_sum(1, 3) == 5
    assert treap.remove(2) == 3
    assert [treap.get(index) for index in range(len(treap))] == [1, 2, 4]
    print("002_implicit_treap: all examples passed")
