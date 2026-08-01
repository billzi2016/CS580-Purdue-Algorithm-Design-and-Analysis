"""
文件意图：
    本文件手写实现并查集（Union-Find / Disjoint Set Union），用于维护动态连通分量。

适用场景：
    Kruskal 最小生成树、动态合并集合、判断两个元素是否属于同一连通分量。

核心思想：
    每个集合用一棵树表示，根节点是集合代表。路径压缩让查找过程中访问到的
    节点直接指向根；按大小合并让较小树挂到较大树下，避免树过高。

输入输出：
    输入可哈希元素集合，支持 find、union、connected 和 component_size 操作。

时间复杂度：
    单次操作均摊接近 O(1)，严格为 O(alpha(n))。

空间复杂度：
    O(n)
"""

from collections.abc import Hashable, Iterable

Node = Hashable


class UnionFind:
    """
    并查集数据结构。

    设计说明：
        本实现支持任意可哈希节点，而不只支持整数下标，便于图算法示例复用。
    """

    def __init__(self, nodes: Iterable[Node]) -> None:
        """
        初始化并查集，每个节点单独成为一个集合。
        """
        unique_nodes = list(dict.fromkeys(nodes))
        self.parent: dict[Node, Node] = {node: node for node in unique_nodes}
        self.size: dict[Node, int] = {node: 1 for node in unique_nodes}
        self.components = len(unique_nodes)

    def find(self, node: Node) -> Node:
        """
        返回 node 所在集合的代表元。

        边界情况：
            如果 node 未在初始化集合中，抛出 KeyError，避免静默创建错误节点。
        """
        if node not in self.parent:
            raise KeyError(f"未知节点：{node}")

        if self.parent[node] != node:
            # 路径压缩：把 node 到根路径上的节点直接挂到根上。
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, first: Node, second: Node) -> bool:
        """
        合并 first 和 second 所在集合。

        返回：
            如果原本属于不同集合并发生合并，返回 True；否则返回 False。
        """
        root_first = self.find(first)
        root_second = self.find(second)

        if root_first == root_second:
            return False

        if self.size[root_first] < self.size[root_second]:
            root_first, root_second = root_second, root_first

        self.parent[root_second] = root_first
        self.size[root_first] += self.size[root_second]
        self.components -= 1
        return True

    def connected(self, first: Node, second: Node) -> bool:
        """
        判断 first 和 second 是否在同一集合。
        """
        return self.find(first) == self.find(second)

    def component_size(self, node: Node) -> int:
        """
        返回 node 所在集合大小。
        """
        return self.size[self.find(node)]


if __name__ == "__main__":
    uf = UnionFind(["A", "B", "C", "D"])
    assert uf.components == 4
    assert uf.union("A", "B")
    assert uf.connected("A", "B")
    assert uf.component_size("A") == 2
    assert not uf.union("A", "B")
    assert uf.union("C", "D")
    assert uf.union("B", "C")
    assert uf.components == 1
    assert uf.component_size("D") == 4

    try:
        uf.find("Z")
        raise AssertionError("未知节点必须抛出 KeyError")
    except KeyError:
        pass

    print("001_union_find: all examples passed")
