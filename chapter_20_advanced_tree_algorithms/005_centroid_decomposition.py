"""
文件意图：手写实现点分治，并支持动态激活顶点集合中的最近距离查询。
适用场景：树结构固定、顶点可激活且需要反复查询“距任一激活点最近的距离”时。
核心思想：递归删除当前连通块的重心，原树被分为深度 O(log n) 的重心树；每个顶点预存到
          重心祖先的距离，激活和查询只需沿这条祖先链取最小值。
输入输出：输入无权无向树，调用 set_active 改变状态，nearest_active 返回最短边数或 None。
构建 O(n log n)，激活与查询 O(log n)，教学版停用 O(n log n)，空间 O(n log n)。
关键边界情况：无激活点查询返回 None；重复激活幂等；非法树与非法编号明确报错。
"""


class CentroidDecomposition:
    """支持最近激活点查询的点分治结构。"""

    def __init__(self, tree: list[list[int]]) -> None:
        """建立重心树及原顶点到各重心祖先的距离。

        参数：tree 是非空、对称、无自环无重边的无向树邻接表。
        返回：无。
        边界情况：非树输入抛出 ValueError；单顶点树可正常构建。
        关键算法点：每次选择的重心删除后，各子块规模至多为原块一半。
        """
        self.vertex_count = len(tree)
        if self.vertex_count == 0:
            raise ValueError("tree 必须非空")
        self._validate_adjacency(tree)
        self.tree = tree
        self._validate_connected_acyclic()
        self.blocked = [False] * self.vertex_count
        self.centroid_parent = [-1] * self.vertex_count
        self.centroid_distances: list[list[tuple[int, int]]] = [[] for _ in range(self.vertex_count)]
        self._best_distance = [float("inf")] * self.vertex_count
        self._active = [False] * self.vertex_count
        self._decompose(0, -1)

    def set_active(self, vertex: int, active: bool = True) -> None:
        """激活或停用一个顶点。

        参数：vertex 为有效顶点；active=True 表示激活，False 表示停用。
        返回：无。
        边界情况：重复设置同一状态无影响；停用后会重建受影响重心的最优值。
        关键算法点：激活时沿重心祖先链取最小值，停用时仅扫描该重心覆盖的顶点距离。
        """
        self._check_vertex(vertex)
        if self._active[vertex] == active:
            return
        self._active[vertex] = active
        if active:
            for centroid, distance in self.centroid_distances[vertex]:
                self._best_distance[centroid] = min(self._best_distance[centroid], distance)
            return
        # 为保持实现透明，教学版停用时从全部顶点重建相关重心的最优值，代价 O(n log n)。
        # 高性能可删除版本通常为每个重心维护可惰性删除的堆。
        affected_centroids = [centroid for centroid, _ in self.centroid_distances[vertex]]
        for centroid in affected_centroids:
            best = float("inf")
            for candidate, is_active in enumerate(self._active):
                if not is_active:
                    continue
                for candidate_centroid, distance in self.centroid_distances[candidate]:
                    if candidate_centroid == centroid:
                        best = min(best, distance)
                        break
            self._best_distance[centroid] = best

    def nearest_active(self, vertex: int) -> int | None:
        """返回 vertex 到任一激活顶点的最短边数。

        参数：vertex 为有效顶点。
        返回：最短距离；当前没有激活顶点时返回 None。
        边界情况：查询激活顶点自身返回 0。
        关键算法点：任一路径在重心树上可由某个共同重心拆开，枚举全部重心祖先即可覆盖最优解。
        """
        self._check_vertex(vertex)
        answer = float("inf")
        for centroid, distance in self.centroid_distances[vertex]:
            answer = min(answer, distance + self._best_distance[centroid])
        return None if answer == float("inf") else int(answer)

    def _decompose(self, start: int, parent_centroid: int) -> None:
        component = self._collect_component(start)
        centroid = self._find_centroid(component)
        self.centroid_parent[centroid] = parent_centroid
        self._append_distances(centroid, centroid, -1, 0)
        self.blocked[centroid] = True
        for neighbor in self.tree[centroid]:
            if not self.blocked[neighbor]:
                self._decompose(neighbor, centroid)

    def _collect_component(self, start: int) -> list[int]:
        component: list[int] = []
        stack = [start]
        seen = {start}
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            for neighbor in self.tree[vertex]:
                if not self.blocked[neighbor] and neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        return component

    def _find_centroid(self, component: list[int]) -> int:
        component_set = set(component)
        root = component[0]
        parent = {root: -1}
        order = [root]
        for vertex in order:
            for neighbor in self.tree[vertex]:
                if neighbor in component_set and neighbor != parent[vertex]:
                    parent[neighbor] = vertex
                    order.append(neighbor)
        size = {vertex: 1 for vertex in component}
        for vertex in reversed(order):
            if parent[vertex] != -1:
                size[parent[vertex]] += size[vertex]
        total = len(component)
        best_vertex = root
        best_largest_part = total
        for vertex in component:
            largest_part = total - size[vertex]
            for neighbor in self.tree[vertex]:
                if neighbor in component_set and parent.get(neighbor) == vertex:
                    largest_part = max(largest_part, size[neighbor])
            if largest_part < best_largest_part:
                best_largest_part = largest_part
                best_vertex = vertex
        return best_vertex

    def _append_distances(self, centroid: int, vertex: int, parent: int, distance: int) -> None:
        self.centroid_distances[vertex].append((centroid, distance))
        for neighbor in self.tree[vertex]:
            if neighbor != parent and not self.blocked[neighbor]:
                self._append_distances(centroid, neighbor, vertex, distance + 1)

    def _validate_connected_acyclic(self) -> None:
        seen = {0}
        stack = [0]
        edge_twice = 0
        while stack:
            vertex = stack.pop()
            edge_twice += len(self.tree[vertex])
            for neighbor in self.tree[vertex]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)
        if len(seen) != self.vertex_count or edge_twice // 2 != self.vertex_count - 1:
            raise ValueError("tree 必须连通且无环")

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
    decomposition = CentroidDecomposition(tree)
    assert decomposition.nearest_active(3) is None
    decomposition.set_active(4)
    assert decomposition.nearest_active(3) == 2
    assert decomposition.nearest_active(4) == 0
    decomposition.set_active(5)
    assert decomposition.nearest_active(2) == 1
    decomposition.set_active(4, False)
    assert decomposition.nearest_active(3) == 4
    assert CentroidDecomposition([[]]).nearest_active(0) is None
    print("005_centroid_decomposition: all examples passed")
