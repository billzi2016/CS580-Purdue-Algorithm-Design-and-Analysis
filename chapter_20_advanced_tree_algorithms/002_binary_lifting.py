"""
文件意图：手写实现支持第 k 级祖先、LCA 与距离查询的树上二进制提升。
适用场景：静态树上有大量祖先、最近公共祖先或两点距离查询时。
核心思想：up[j][v] 保存 v 的 2^j 级祖先；把跳跃长度分解为二进制位即可快速上跳。
输入输出：输入无向树邻接表和根，提供 kth_ancestor、lca、distance 查询。
预处理时间复杂度：O(n log n)，每次查询 O(log n)，空间复杂度 O(n log n)。
关键边界情况：根向上越界返回 None；非法树和非法顶点明确报错。
"""


class BinaryLifting:
    """静态有根树的二进制提升查询结构。"""

    def __init__(self, tree: list[list[int]], root: int = 0) -> None:
        """从无向树建立倍增祖先表。

        参数：tree 为对称无向树邻接表；root 为根顶点。
        返回：无。
        边界情况：空树、非树或非法根抛出 ValueError。
        关键算法点：第 j 层祖先由两个连续的第 j-1 层跳跃拼接得到。
        """
        self.vertex_count = len(tree)
        if self.vertex_count == 0 or not 0 <= root < self.vertex_count:
            raise ValueError("tree 必须非空且 root 必须有效")
        self._validate_tree_adjacency(tree)
        self.depth = [-1] * self.vertex_count
        parent_zero = [root] * self.vertex_count
        self.depth[root] = 0
        stack = [root]
        while stack:
            vertex = stack.pop()
            for neighbor in tree[vertex]:
                if neighbor == parent_zero[vertex]:
                    continue
                if self.depth[neighbor] != -1:
                    raise ValueError("tree 必须无环")
                parent_zero[neighbor] = vertex
                self.depth[neighbor] = self.depth[vertex] + 1
                stack.append(neighbor)
        if any(depth == -1 for depth in self.depth):
            raise ValueError("tree 必须连通")
        self.levels = self.vertex_count.bit_length()
        self.up = [parent_zero]
        for _ in range(1, self.levels):
            previous = self.up[-1]
            self.up.append(
                [previous[previous[vertex]] for vertex in range(self.vertex_count)]
            )

    def kth_ancestor(self, vertex: int, steps: int) -> int | None:
        """返回 vertex 向根方向走 steps 步后的祖先。

        参数：vertex 为有效顶点；steps 为非负整数。
        返回：祖先编号；若越过根则返回 None。
        边界情况：steps 为 0 返回自身，负步数抛出 ValueError。
        关键算法点：仅对 steps 中为 1 的二进制位执行对应长度的跳跃。
        """
        self._check_vertex(vertex)
        if steps < 0:
            raise ValueError("steps 必须非负")
        if steps > self.depth[vertex]:
            return None
        for level in range(self.levels):
            if steps & (1 << level):
                vertex = self.up[level][vertex]
        return vertex

    def lca(self, first: int, second: int) -> int:
        """返回两个顶点在当前根下的最近公共祖先。

        参数：first、second 为有效顶点编号。
        返回：最近公共祖先编号。
        边界情况：相同顶点或其中一个是另一个祖先时正常返回。
        关键算法点：深度对齐后，从大到小同步跳过仍不相交的祖先块。
        """
        self._check_vertex(first)
        self._check_vertex(second)
        if self.depth[first] < self.depth[second]:
            first, second = second, first
        lifted = self.kth_ancestor(first, self.depth[first] - self.depth[second])
        assert lifted is not None
        first = lifted
        if first == second:
            return first
        for level in range(self.levels - 1, -1, -1):
            if self.up[level][first] != self.up[level][second]:
                first = self.up[level][first]
                second = self.up[level][second]
        return self.up[0][first]

    def distance(self, first: int, second: int) -> int:
        """返回无权树中两个顶点间的边数距离。

        参数：first、second 为有效顶点编号。
        返回：唯一路径上的边数。
        边界情况：相同顶点距离为 0。
        关键算法点：路径在 LCA 处分为两段，长度是两个深度差之和。
        """
        ancestor = self.lca(first, second)
        return self.depth[first] + self.depth[second] - 2 * self.depth[ancestor]

    def _check_vertex(self, vertex: int) -> None:
        if not 0 <= vertex < self.vertex_count:
            raise IndexError("顶点编号超出范围")

    @staticmethod
    def _validate_tree_adjacency(tree: list[list[int]]) -> None:
        for vertex, neighbors in enumerate(tree):
            if vertex in neighbors or len(set(neighbors)) != len(neighbors):
                raise ValueError("tree 不能包含自环或平行边")
            if any(
                neighbor < 0 or neighbor >= len(tree) or vertex not in tree[neighbor]
                for neighbor in neighbors
            ):
                raise ValueError("tree 必须是对称无向邻接表")


if __name__ == "__main__":
    tree = [[1, 2], [0, 3, 4], [0, 5], [1], [1], [2]]
    solver = BinaryLifting(tree)
    assert solver.kth_ancestor(4, 0) == 4
    assert solver.kth_ancestor(4, 2) == 0
    assert solver.kth_ancestor(4, 3) is None
    assert solver.lca(3, 4) == 1
    assert solver.lca(3, 5) == 0
    assert solver.distance(3, 5) == 4
    assert BinaryLifting([[]]).distance(0, 0) == 0
    print("002_binary_lifting: all examples passed")
