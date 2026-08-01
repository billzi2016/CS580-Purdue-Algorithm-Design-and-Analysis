"""
文件意图：手写实现有根树的 Euler Tour（进入时间序）预处理。
适用场景：将每棵子树映射为连续数组区间，以支持子树求和、计数或线段树查询。
核心思想：DFS 第一次到达顶点时记录 tin 并写入序列，处理完其全部后代时记录 tout；
          因而任意顶点的所有后代恰好连续位于 order[tin: tout]。
输入输出：输入无向树邻接表和根，输出顶点进入序、退出位置、父节点和深度。
时间复杂度：预处理 O(n)，空间复杂度 O(n)。
关键边界情况：拒绝空图、非法根、非对称邻接表、自环、环和不连通图。
"""


class EulerTour:
    """固定根树的进入时间 Euler Tour。"""

    def __init__(self, tree: list[list[int]], root: int = 0) -> None:
        """构造树的 Euler Tour。

        参数：tree 是无自环、无重边的对称无向树邻接表；root 是根顶点。
        返回：无；结果保存在 tin、tout、order、parent、depth 属性中。
        边界情况：非树或非法 root 抛出 ValueError。
        关键算法点：顶点进入时写入 order，退出时的当前位置就是半开区间右端点。
        """
        self.vertex_count = len(tree)
        if self.vertex_count == 0 or not 0 <= root < self.vertex_count:
            raise ValueError("tree 必须非空且 root 必须有效")
        self._validate_adjacency(tree)

        self.tin = [-1] * self.vertex_count
        self.tout = [-1] * self.vertex_count
        self.parent = [root] * self.vertex_count
        self.depth = [-1] * self.vertex_count
        self.order: list[int] = []
        self.depth[root] = 0

        # 栈帧保存“下一条尚未检查的邻边”，从而精确模拟递归 DFS 的进入与退出时机。
        stack: list[list[int]] = [[root, root, 0]]
        while stack:
            vertex, parent, next_index = stack[-1]
            if next_index == 0:
                self.tin[vertex] = len(self.order)
                self.order.append(vertex)
            if next_index == len(tree[vertex]):
                self.tout[vertex] = len(self.order)
                stack.pop()
                continue
            neighbor = tree[vertex][next_index]
            stack[-1][2] += 1
            if neighbor == parent:
                continue
            if self.depth[neighbor] != -1:
                raise ValueError("tree 必须无环")
            self.parent[neighbor] = vertex
            self.depth[neighbor] = self.depth[vertex] + 1
            stack.append([neighbor, vertex, 0])
        if any(depth == -1 for depth in self.depth):
            raise ValueError("tree 必须连通")

    def subtree_interval(self, vertex: int) -> tuple[int, int]:
        """返回 vertex 子树在 order 中的半开区间。

        参数：vertex 是有效顶点编号。
        返回：(left, right)，其中 order[left:right] 恰好包含该子树顶点。
        边界情况：非法编号抛出 IndexError。
        关键算法点：DFS 完成子树前不会访问其外部顶点，故进入时间形成连续区间。
        """
        self._check_vertex(vertex)
        return self.tin[vertex], self.tout[vertex]

    def subtree_vertices(self, vertex: int) -> list[int]:
        """按进入顺序返回 vertex 子树中的全部顶点。

        参数：vertex 是有效顶点编号。
        返回：该子树的顶点列表副本。
        边界情况：叶子返回只含自身的列表。
        关键算法点：使用 Euler 区间切片，不再重复遍历树。
        """
        left, right = self.subtree_interval(vertex)
        return self.order[left:right]

    def _check_vertex(self, vertex: int) -> None:
        if not 0 <= vertex < self.vertex_count:
            raise IndexError("顶点编号超出范围")

    @staticmethod
    def _validate_adjacency(tree: list[list[int]]) -> None:
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
    tour = EulerTour(tree)
    assert tour.order == [0, 1, 3, 4, 2, 5]
    assert tour.subtree_interval(1) == (1, 4)
    assert tour.subtree_vertices(1) == [1, 3, 4]
    assert tour.subtree_vertices(3) == [3]
    assert EulerTour([[]]).subtree_interval(0) == (0, 1)
    print("001_euler_tour: all examples passed")
