"""variation graph 基础教学实现。

适用场景：把多个等位序列或变异位点压入同一个有向无环图中，避免单一线性 reference 丢失多样性。
核心思想：节点保存片段序列，边表示可拼接路径；路径名字映射到一条具体单倍型或参考路径。
输入输出：输入节点、边和路径；支持枚举路径序列、查节点入出边以及线性化展示。
时间复杂度：路径展开 O(路径长度)，邻接查询 O(度数)。
关键边界情况：本实现不处理循环检测和复杂拓扑压缩；路径中的节点必须存在。
"""

from dataclasses import dataclass, field


@dataclass
class VariationGraph:
    """最小 variation graph 结构。"""

    node_labels: dict[str, str] = field(default_factory=dict)
    edges: dict[str, list[str]] = field(default_factory=dict)
    paths: dict[str, list[str]] = field(default_factory=dict)

    def add_node(self, node_id: str, label: str) -> None:
        """加入一个带标签的图节点。"""

        if node_id in self.node_labels:
            raise ValueError("node_id 不能重复")
        self.node_labels[node_id] = label
        self.edges.setdefault(node_id, [])

    def add_edge(self, source: str, target: str) -> None:
        """加入有向边 source -> target。"""

        self._require_node(source)
        self._require_node(target)
        self.edges.setdefault(source, []).append(target)

    def add_path(self, name: str, node_ids: list[str]) -> None:
        """记录一条命名路径。"""

        for node_id in node_ids:
            self._require_node(node_id)
        self.paths[name] = node_ids[:]

    def path_sequence(self, name: str) -> str:
        """把命名路径展开成序列。"""

        if name not in self.paths:
            raise ValueError("路径不存在")
        return "".join(self.node_labels[node_id] for node_id in self.paths[name])

    def outgoing(self, node_id: str) -> list[str]:
        """返回节点的所有后继。"""

        self._require_node(node_id)
        return self.edges.get(node_id, [])[:]

    def _require_node(self, node_id: str) -> None:
        if node_id not in self.node_labels:
            raise ValueError("节点不存在")


if __name__ == "__main__":
    graph = VariationGraph()
    graph.add_node("n1", "AC")
    graph.add_node("n2", "G")
    graph.add_node("n3", "T")
    graph.add_edge("n1", "n2")
    graph.add_edge("n1", "n3")
    graph.add_path("ref", ["n1", "n2"])
    graph.add_path("alt", ["n1", "n3"])
    assert graph.path_sequence("ref") == "ACG"
    assert graph.path_sequence("alt") == "ACT"
    assert graph.outgoing("n1") == ["n2", "n3"]
    print("042_variation_graph_basics: all examples passed")
