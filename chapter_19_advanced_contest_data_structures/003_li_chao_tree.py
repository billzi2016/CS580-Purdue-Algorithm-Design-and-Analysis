"""
文件意图：手写实现整数闭区间上的最小值 Li Chao Tree。
适用场景：动态插入直线 f(x)=slope*x+intercept，并在固定整数定义域查询最小值。
核心思想：每个节点保留其中点处更优的直线，另一条直线只需递归到可能获胜的一侧。
输入输出：构造时给出整数定义域，支持 add_line 与 query。
时间复杂度：插入和查询均为 O(log C)，C 为定义域长度。空间复杂度：O(number of created nodes)。
关键边界：查询点必须在定义域内；没有插入直线时 query 返回 None。
"""


class _Line:
    """表示 y=slope*x+intercept 的整数直线。"""

    def __init__(self, slope: int, intercept: int) -> None:
        self.slope = slope
        self.intercept = intercept

    def value_at(self, x: int) -> int:
        """计算该直线在整数 x 处的函数值。"""
        return self.slope * x + self.intercept


class _Node:
    """Li Chao Tree 节点，保存当前区间的候选直线与两个子节点。"""

    def __init__(self, line: _Line) -> None:
        self.line = line
        self.left: _Node | None = None
        self.right: _Node | None = None


class LiChaoTree:
    """维护固定整数闭区间内直线最小值的 Li Chao Tree。"""

    def __init__(self, domain_left: int, domain_right: int) -> None:
        """创建定义域为 [domain_left, domain_right] 的空树。

        参数：两个整数端点，要求左端点不大于右端点。
        返回：无。
        边界情况：单点定义域合法，反向定义域抛出 ValueError。
        关键算法点：定义域固定后，每次递归按整数中点二分。
        """
        if domain_left > domain_right:
            raise ValueError("定义域左端点不能大于右端点")
        self.domain_left = domain_left
        self.domain_right = domain_right
        self._root: _Node | None = None

    def add_line(self, slope: int, intercept: int) -> None:
        """插入直线 slope*x+intercept。

        参数：slope、intercept 为整数。
        返回：无。
        边界情况：相同直线或平行直线可正常插入。
        关键算法点：中点较优直线留在节点，另一条只递归到端点相对胜负发生变化的一侧。
        """
        self._root = self._insert(
            self._root, _Line(slope, intercept), self.domain_left, self.domain_right
        )

    def _insert(self, node: _Node | None, line: _Line, left: int, right: int) -> _Node:
        """把 line 插入 node 所代表的整数闭区间。"""
        if node is None:
            return _Node(line)
        middle = (left + right) // 2
        if line.value_at(middle) < node.line.value_at(middle):
            node.line, line = line, node.line
        if left == right:
            return node
        if line.value_at(left) < node.line.value_at(left):
            node.left = self._insert(node.left, line, left, middle)
        elif line.value_at(right) < node.line.value_at(right):
            node.right = self._insert(node.right, line, middle + 1, right)
        return node

    def query(self, x: int) -> int | None:
        """返回所有已插入直线在 x 的最小函数值。

        参数：x 为定义域内整数。
        返回：最小值；树为空时返回 None。
        边界情况：定义域外查询抛出 IndexError。
        关键算法点：答案只可能来自根到目标叶路径上保存的直线。
        """
        if x < self.domain_left or x > self.domain_right:
            raise IndexError("查询点超出定义域")
        node = self._root
        left, right = self.domain_left, self.domain_right
        best: int | None = None
        while node is not None:
            candidate = node.line.value_at(x)
            best = candidate if best is None or candidate < best else best
            middle = (left + right) // 2
            if left == right:
                break
            if x <= middle:
                node = node.left
                right = middle
            else:
                node = node.right
                left = middle + 1
        return best


if __name__ == "__main__":
    tree = LiChaoTree(-5, 5)
    assert tree.query(0) is None
    tree.add_line(2, 1)
    tree.add_line(-1, 4)
    tree.add_line(0, 0)
    assert tree.query(-2) == -3
    assert tree.query(0) == 0
    assert tree.query(5) == -1
    print("003_li_chao_tree: all examples passed")
