"""
文件意图：手写实现树上最近公共祖先的二进制提升数据结构。
适用场景：固定根树中需要大量 LCA 查询，或需要跳过祖先链上的 2 的幂长度时。
核心思想：预处理每个顶点的 2^j 级祖先，查询时先对齐深度再从高位向低位同步上跳。
输入输出：以无向树邻接表和根构造对象，调用 lca 查询两个顶点的最近公共祖先。
预处理时间复杂度：O(n log n)，单次查询 O(log n)，空间复杂度：O(n log n)。
关键边界：空树和非树输入被拒绝；根的 LCA 查询、相同顶点和祖先关系均可处理。
"""


class LcaBinaryLifting:
    """固定根树的二进制提升 LCA 查询结构。"""

    def __init__(self, tree: list[list[int]], root: int = 0) -> None:
        """预处理 tree 中以 root 为根的祖先表。

        参数：tree 为对称、无自环的无向树邻接表；root 为根顶点。
        返回：无，构造完成后使用 lca 查询。
        边界情况：空树、非法根、非对称图、含环或不连通图均抛出 ValueError。
        关键算法点：parent[j][v] 表示 v 的第 2^j 个祖先。
        """
        self.vertex_count = len(tree)
        if self.vertex_count == 0 or root < 0 or root >= self.vertex_count:
            raise ValueError("tree 必须非空且 root 必须是有效顶点")
        for vertex, neighbors in enumerate(tree):
            if len(set(neighbors)) != len(neighbors) or vertex in neighbors:
                raise ValueError("tree 不能包含自环或平行边")
            if any(neighbor < 0 or neighbor >= self.vertex_count or vertex not in tree[neighbor] for neighbor in neighbors):
                raise ValueError("tree 必须是对称无向邻接表")

        self.depth = [-1] * self.vertex_count
        parent_zero = [root] * self.vertex_count
        self.depth[root] = 0
        pending = [root]
        while pending:
            vertex = pending.pop()
            for neighbor in tree[vertex]:
                if self.depth[neighbor] == -1:
                    self.depth[neighbor] = self.depth[vertex] + 1
                    parent_zero[neighbor] = vertex
                    pending.append(neighbor)
                elif neighbor != parent_zero[vertex]:
                    raise ValueError("tree 必须无环")
        if any(depth == -1 for depth in self.depth):
            raise ValueError("tree 必须连通")

        self.levels = self.vertex_count.bit_length()
        self.parent = [parent_zero]
        for level in range(1, self.levels):
            previous = self.parent[-1]
            self.parent.append([previous[previous[vertex]] for vertex in range(self.vertex_count)])

    def lca(self, first: int, second: int) -> int:
        """返回 first 与 second 在构造根树中的最近公共祖先。

        参数：first、second 为有效顶点编号。
        返回：二者的最近公共祖先顶点编号。
        边界情况：相同顶点返回自身，非法编号抛出 IndexError。
        关键算法点：深度对齐后，同时从最高可用位向下跳，避免越过最近公共祖先。
        """
        if first < 0 or first >= self.vertex_count or second < 0 or second >= self.vertex_count:
            raise IndexError("查询顶点必须在 tree 范围内")
        if self.depth[first] < self.depth[second]:
            first, second = second, first
        difference = self.depth[first] - self.depth[second]
        for level in range(self.levels):
            if difference & (1 << level):
                first = self.parent[level][first]
        if first == second:
            return first
        for level in range(self.levels - 1, -1, -1):
            if self.parent[level][first] != self.parent[level][second]:
                first = self.parent[level][first]
                second = self.parent[level][second]
        return self.parent[0][first]


if __name__ == "__main__":
    tree = [[1, 2], [0, 3, 4], [0, 5, 6], [1], [1], [2], [2]]
    lca_solver = LcaBinaryLifting(tree)
    assert lca_solver.lca(3, 4) == 1
    assert lca_solver.lca(3, 5) == 0
    assert lca_solver.lca(6, 6) == 6
    assert lca_solver.lca(0, 4) == 0
    print("006_lca_binary_lifting: all examples passed")
