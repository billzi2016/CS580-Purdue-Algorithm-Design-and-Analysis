"""
文件意图：手写实现可回滚并查集。
适用场景：离线动态连通性、分治时间线和需要撤销合并操作的算法。
核心思想：按大小合并但不使用路径压缩，把每次合并改动压入历史栈以便恢复。
输入输出：支持 unite、connected、snapshot 和 rollback。
时间复杂度：单次查找/合并 O(log n)，回滚每条历史 O(1)。空间复杂度：O(n+m)。
关键边界：无效顶点和非法快照抛出 IndexError；重复合并也记录历史以保持快照语义。
"""


class RollbackUnionFind:
    """支持恢复到任意历史快照的并查集。"""

    def __init__(self, size: int) -> None:
        """创建包含 size 个互不连通顶点的结构。

        参数：size 为非负顶点数。
        返回：无。
        边界情况：size 为零合法，负数抛出 ValueError。
        关键算法点：不使用路径压缩，否则 find 的改动无法以常数历史恢复。
        """
        if size < 0:
            raise ValueError("size 不能为负数")
        self.parent = list(range(size))
        self.component_size = [1] * size
        self.history: list[tuple[int, int, int] | None] = []

    def find(self, vertex: int) -> int:
        """返回 vertex 所在集合代表元。

        参数：vertex 为有效顶点编号。
        返回：该集合当前根节点。
        边界情况：非法编号抛出 IndexError。
        关键算法点：只沿父边行走而不压缩路径，以保证历史可逆。
        """
        self._check_vertex(vertex)
        while self.parent[vertex] != vertex:
            vertex = self.parent[vertex]
        return vertex

    def unite(self, first: int, second: int) -> bool:
        """合并 first 和 second 所在集合。

        参数：first、second 为有效顶点编号。
        返回：发生真实合并时为 True，原本连通时为 False。
        边界情况：重复合并压入 None 历史，确保一次 rollback 对应一次 unite。
        关键算法点：小集合挂到大集合下，使树高维持对数级别。
        """
        first_root = self.find(first)
        second_root = self.find(second)
        if first_root == second_root:
            self.history.append(None)
            return False
        if self.component_size[first_root] < self.component_size[second_root]:
            first_root, second_root = second_root, first_root
        self.history.append((second_root, first_root, self.component_size[first_root]))
        self.parent[second_root] = first_root
        self.component_size[first_root] += self.component_size[second_root]
        return True

    def connected(self, first: int, second: int) -> bool:
        """判断 first 与 second 当前是否连通。

        参数：两个有效顶点编号。
        返回：代表元相同时为 True。
        边界情况：非法顶点由 find 抛出 IndexError。
        关键算法点：连通性只依赖当前父链根，不需要维护额外图结构。
        """
        return self.find(first) == self.find(second)

    def snapshot(self) -> int:
        """返回当前可用于 rollback 的历史长度快照。

        参数：无。
        返回：非负快照编号。
        边界情况：初始快照为零。
        关键算法点：所有状态变动对应一项历史，因此栈长度唯一确定状态。
        """
        return len(self.history)

    def rollback(self, snapshot: int) -> None:
        """撤销操作直到恢复到 snapshot 时的状态。

        参数：snapshot 必须来自当前或历史 snapshot 调用。
        返回：无。
        边界情况：小于零或大于当前历史长度时抛出 IndexError。
        关键算法点：逆序恢复被挂接根的父指针与接收根原有大小。
        """
        if snapshot < 0 or snapshot > len(self.history):
            raise IndexError("快照编号越界")
        while len(self.history) > snapshot:
            change = self.history.pop()
            if change is None:
                continue
            child, root, old_size = change
            self.parent[child] = child
            self.component_size[root] = old_size

    def _check_vertex(self, vertex: int) -> None:
        """验证 vertex 是有效顶点编号。"""
        if vertex < 0 or vertex >= len(self.parent):
            raise IndexError("顶点编号越界")


if __name__ == "__main__":
    union_find = RollbackUnionFind(4)
    initial = union_find.snapshot()
    assert union_find.unite(0, 1)
    middle = union_find.snapshot()
    assert union_find.unite(1, 2) and union_find.connected(0, 2)
    union_find.rollback(middle)
    assert union_find.connected(0, 1) and not union_find.connected(0, 2)
    union_find.rollback(initial)
    assert not union_find.connected(0, 1)
    print("005_rollback_union_find: all examples passed")
