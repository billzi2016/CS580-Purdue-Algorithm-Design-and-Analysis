"""
文件意图：手写实现树链剖分，并支持顶点权路径和与单点更新。
适用场景：静态树拓扑上交替进行大量路径查询与点修改。
核心思想：每个顶点选择最大的子树作为重儿子，重边连成链；任意路径只跨越 O(log n) 条链，
          再将每条链映射到同一棵手写线段树的连续区间。
输入输出：输入树、每个顶点的数值和根；提供 path_sum 与 update。
预处理 O(n)，单点更新 O(log n)，路径和 O(log^2 n)，空间 O(n)。
关键边界情况：单顶点树、负权、同一顶点路径和非法顶点均可处理或明确报错。
"""


class HeavyLightDecomposition:
    """顶点权树的树链剖分和路径和数据结构。"""

    def __init__(self, tree: list[list[int]], values: list[int], root: int = 0) -> None:
        """预处理重链，并建立保存顶点权值的线段树。

        参数：tree 是无向树邻接表；values[v] 是顶点 v 的初始权值；root 是根。
        返回：无。
        边界情况：values 长度不匹配、非法树或非法根抛出 ValueError。
        关键算法点：重儿子先分配位置，使得同一重链在底层数组中连续。
        """
        self.vertex_count = len(tree)
        if self.vertex_count == 0 or len(values) != self.vertex_count or not 0 <= root < self.vertex_count:
            raise ValueError("tree、values 和 root 必须描述一棵非空树")
        self._validate_adjacency(tree)
        self.values = values[:]
        self.parent = [root] * self.vertex_count
        self.depth = [-1] * self.vertex_count
        self.depth[root] = 0
        traversal_order = [root]
        for vertex in traversal_order:
            for neighbor in tree[vertex]:
                if neighbor == self.parent[vertex]:
                    continue
                if self.depth[neighbor] != -1:
                    raise ValueError("tree 必须无环")
                self.parent[neighbor] = vertex
                self.depth[neighbor] = self.depth[vertex] + 1
                traversal_order.append(neighbor)
        if len(traversal_order) != self.vertex_count:
            raise ValueError("tree 必须连通")

        self.size = [1] * self.vertex_count
        self.heavy = [-1] * self.vertex_count
        for vertex in reversed(traversal_order):
            largest_child_size = 0
            for neighbor in tree[vertex]:
                if self.parent[neighbor] != vertex:
                    continue
                self.size[vertex] += self.size[neighbor]
                if self.size[neighbor] > largest_child_size:
                    largest_child_size = self.size[neighbor]
                    self.heavy[vertex] = neighbor

        self.head = [0] * self.vertex_count
        self.position = [0] * self.vertex_count
        base = [0] * self.vertex_count
        next_position = 0
        pending_chains = [(root, root)]
        while pending_chains:
            chain_start, chain_head = pending_chains.pop()
            vertex = chain_start
            while vertex != -1:
                self.head[vertex] = chain_head
                self.position[vertex] = next_position
                base[next_position] = self.values[vertex]
                next_position += 1
                # 轻儿子必须另开链；逆序并不影响正确性，只影响位置的确定性。
                for neighbor in reversed(tree[vertex]):
                    if self.parent[neighbor] == vertex and neighbor != self.heavy[vertex]:
                        pending_chains.append((neighbor, neighbor))
                vertex = self.heavy[vertex]
        self._segment_size = 1
        while self._segment_size < self.vertex_count:
            self._segment_size *= 2
        self._segment = [0] * (2 * self._segment_size)
        for index, value in enumerate(base):
            self._segment[self._segment_size + index] = value
        for index in range(self._segment_size - 1, 0, -1):
            self._segment[index] = self._segment[index * 2] + self._segment[index * 2 + 1]

    def update(self, vertex: int, value: int) -> None:
        """将一个顶点的权值更新为 value。

        参数：vertex 为有效顶点；value 为新整数权值。
        返回：无。
        边界情况：非法顶点抛出 IndexError。
        关键算法点：仅沿线段树中该叶子到根的路径重算区间和。
        """
        self._check_vertex(vertex)
        self.values[vertex] = value
        index = self._segment_size + self.position[vertex]
        self._segment[index] = value
        while index > 1:
            index //= 2
            self._segment[index] = self._segment[index * 2] + self._segment[index * 2 + 1]

    def path_sum(self, first: int, second: int) -> int:
        """返回 first 到 second 的唯一简单路径上的顶点权值和。

        参数：first、second 为有效顶点。
        返回：路径包含的全部顶点权值和。
        边界情况：相同顶点返回其自身权值。
        关键算法点：每次整段取更深链头到当前顶点，保证至少跨过一条轻边。
        """
        self._check_vertex(first)
        self._check_vertex(second)
        total = 0
        while self.head[first] != self.head[second]:
            if self.depth[self.head[first]] < self.depth[self.head[second]]:
                first, second = second, first
            total += self._range_sum(self.position[self.head[first]], self.position[first] + 1)
            first = self.parent[self.head[first]]
        if self.depth[first] > self.depth[second]:
            first, second = second, first
        return total + self._range_sum(self.position[first], self.position[second] + 1)

    def _range_sum(self, left: int, right: int) -> int:
        left += self._segment_size
        right += self._segment_size
        result = 0
        while left < right:
            if left % 2:
                result += self._segment[left]
                left += 1
            if right % 2:
                right -= 1
                result += self._segment[right]
            left //= 2
            right //= 2
        return result

    def _check_vertex(self, vertex: int) -> None:
        if not 0 <= vertex < self.vertex_count:
            raise IndexError("顶点编号超出范围")

    @staticmethod
    def _validate_adjacency(tree: list[list[int]]) -> None:
        for vertex, neighbors in enumerate(tree):
            if vertex in neighbors or len(set(neighbors)) != len(neighbors):
                raise ValueError("tree 不能包含自环或平行边")
            if any(neighbor < 0 or neighbor >= len(tree) or vertex not in tree[neighbor] for neighbor in neighbors):
                raise ValueError("tree 必须是对称无向邻接表")


if __name__ == "__main__":
    tree = [[1, 2], [0, 3, 4], [0, 5], [1], [1], [2]]
    decomposition = HeavyLightDecomposition(tree, [5, 1, 3, 2, 4, -1])
    assert decomposition.path_sum(3, 5) == 10
    assert decomposition.path_sum(4, 4) == 4
    decomposition.update(1, 10)
    assert decomposition.path_sum(3, 5) == 19
    assert HeavyLightDecomposition([[]], [7]).path_sum(0, 0) == 7
    print("003_heavy_light_decomposition: all examples passed")
