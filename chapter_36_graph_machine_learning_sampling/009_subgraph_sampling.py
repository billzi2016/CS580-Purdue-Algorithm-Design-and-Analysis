"""
子图采样：从种子节点扩展得到诱导子图。

意图：
- 以 BFS frontier 方式采样节点，再返回这些节点上的诱导边。
- 适合小批量 GNN 训练前的局部子图构造。
- 明确区分“采样节点集合”和“诱导边集合”，避免只返回节点的半成品。
"""

from collections import deque
from dataclasses import dataclass


Graph = dict[str, list[str]]
Edge = tuple[str, str]


@dataclass(frozen=True)
class SampledSubgraph:
    """采样得到的子图。"""

    nodes: set[str]
    edges: set[Edge]


def bfs_subgraph_sample(graph: Graph, seeds: list[str], max_nodes: int) -> SampledSubgraph:
    """从 seeds 出发按 BFS 扩展最多 max_nodes 个节点，并返回诱导子图。"""

    if max_nodes < 0:
        raise ValueError("max_nodes 不能为负数")
    selected: set[str] = set()
    queue: deque[str] = deque(seeds)

    while queue and len(selected) < max_nodes:
        node = queue.popleft()
        if node in selected or node not in graph:
            continue
        selected.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in selected:
                queue.append(neighbor)

    edges = _induced_edges(graph, selected)
    return SampledSubgraph(selected, edges)


def _induced_edges(graph: Graph, nodes: set[str]) -> set[Edge]:
    """返回 nodes 上的有向诱导边集合。"""

    edges: set[Edge] = set()
    for source in nodes:
        for target in graph.get(source, []):
            if target in nodes:
                edges.add((source, target))
    return edges


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": ["A"], "E": []}
    subgraph = bfs_subgraph_sample(graph, ["A"], 3)
    assert subgraph.nodes == {"A", "B", "C"}
    assert subgraph.edges == {("A", "B"), ("A", "C")}
    assert bfs_subgraph_sample(graph, ["Z"], 3) == SampledSubgraph(set(), set())

    print("009_subgraph_sampling: all examples passed")
