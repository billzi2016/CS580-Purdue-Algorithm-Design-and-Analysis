"""
文件意图：手写实现 DSU on Tree（Small-to-Large）并计算各子树中最高频颜色之和。
适用场景：需要为树上每个顶点独立统计子树颜色频率、众数等可增量维护的信息时。
核心思想：保留重儿子的统计状态，临时加入各轻儿子；每个顶点只在 O(log n) 个轻子树中被重建。
输入输出：输入树、整数颜色和根，输出 answer[v]，即 v 子树中出现次数最多的颜色编号之和。
时间复杂度：O(n log n)，空间复杂度 O(n + c)，其中 c 是不同颜色数。
关键边界情况：颜色可为负数；单顶点树正常工作；非法树和长度不匹配会报错。
"""


class DsuOnTree:
    """以重儿子统计复用为核心的子树颜色统计器。"""

    def __init__(self, tree: list[list[int]], colors: list[int], root: int = 0) -> None:
        """预处理父子关系、子树大小及重儿子。

        参数：tree 为无向树邻接表；colors[v] 是顶点颜色；root 为根。
        返回：无。
        边界情况：空树、颜色数不匹配、非法根或非树输入抛出 ValueError。
        关键算法点：Euler 序使任一子树可用一个连续区间整体加入或删除。
        """
        self.vertex_count = len(tree)
        if (
            self.vertex_count == 0
            or len(colors) != self.vertex_count
            or not 0 <= root < self.vertex_count
        ):
            raise ValueError("tree、colors 和 root 必须描述一棵非空树")
        self._validate_adjacency(tree)
        self.tree = tree
        self.colors = colors[:]
        self.root = root
        self.parent = [root] * self.vertex_count
        self.depth = [-1] * self.vertex_count
        self.depth[root] = 0
        traversal: list[int] = []
        pending = [root]
        while pending:
            vertex = pending.pop()
            traversal.append(vertex)
            for neighbor in tree[vertex]:
                if neighbor == self.parent[vertex]:
                    continue
                if self.depth[neighbor] != -1:
                    raise ValueError("tree 必须无环")
                self.parent[neighbor] = vertex
                self.depth[neighbor] = self.depth[vertex] + 1
                pending.append(neighbor)
        if len(traversal) != self.vertex_count:
            raise ValueError("tree 必须连通")
        self.size = [1] * self.vertex_count
        self.heavy = [-1] * self.vertex_count
        for vertex in reversed(traversal):
            for neighbor in tree[vertex]:
                if self.parent[neighbor] == vertex:
                    self.size[vertex] += self.size[neighbor]
                    if (
                        self.heavy[vertex] == -1
                        or self.size[neighbor] > self.size[self.heavy[vertex]]
                    ):
                        self.heavy[vertex] = neighbor
        self.tin = [0] * self.vertex_count
        self.tout = [0] * self.vertex_count
        self.euler = [0] * self.vertex_count
        for index, vertex in enumerate(traversal):
            self.tin[vertex] = index
            self.euler[index] = vertex
        # 前序序列与子树大小直接给出半开区间右端点。
        for vertex in range(self.vertex_count):
            self.tout[vertex] = self.tin[vertex] + self.size[vertex]

    def most_frequent_color_sums(self) -> list[int]:
        """计算每个子树内最高频颜色的颜色编号总和。

        参数：无。
        返回：answer[v] 为顶点 v 的子树中所有最高频颜色的和。
        边界情况：单一颜色或多个并列众数均正确处理。
        关键算法点：轻子树统计会清除，重子树统计保留给父节点复用。
        """
        self._frequency: dict[int, int] = {}
        self._maximum_frequency = 0
        self._maximum_color_sum = 0
        answer = [0] * self.vertex_count

        def add_subtree(vertex: int, delta: int) -> None:
            for index in range(self.tin[vertex], self.tout[vertex]):
                color = self.colors[self.euler[index]]
                new_count = self._frequency.get(color, 0) + delta
                if new_count == 0:
                    del self._frequency[color]
                else:
                    self._frequency[color] = new_count
                    if delta > 0:
                        if new_count > self._maximum_frequency:
                            self._maximum_frequency = new_count
                            self._maximum_color_sum = color
                        elif new_count == self._maximum_frequency:
                            self._maximum_color_sum += color

        def solve(vertex: int, keep: bool) -> None:
            for neighbor in self.tree[vertex]:
                if self.parent[neighbor] == vertex and neighbor != self.heavy[vertex]:
                    solve(neighbor, False)
            if self.heavy[vertex] != -1:
                solve(self.heavy[vertex], True)
            # 保留的重子树已经在频率表中，逐个加入轻子树与当前根即可得到完整子树。
            for neighbor in self.tree[vertex]:
                if self.parent[neighbor] == vertex and neighbor != self.heavy[vertex]:
                    add_subtree(neighbor, 1)
            color = self.colors[vertex]
            add_subtree_vertex = self._frequency.get(color, 0) + 1
            self._frequency[color] = add_subtree_vertex
            if add_subtree_vertex > self._maximum_frequency:
                self._maximum_frequency = add_subtree_vertex
                self._maximum_color_sum = color
            elif add_subtree_vertex == self._maximum_frequency:
                self._maximum_color_sum += color
            answer[vertex] = self._maximum_color_sum
            if not keep:
                add_subtree(vertex, -1)
                self._maximum_frequency = 0
                self._maximum_color_sum = 0

        solve(self.root, True)
        return answer

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
    solver = DsuOnTree(tree, [1, 2, 1, 2, 3, 3])
    assert solver.most_frequent_color_sums() == [6, 2, 4, 2, 3, 3]
    assert DsuOnTree([[]], [-7]).most_frequent_color_sums() == [-7]
    print("004_dsu_on_tree: all examples passed")
