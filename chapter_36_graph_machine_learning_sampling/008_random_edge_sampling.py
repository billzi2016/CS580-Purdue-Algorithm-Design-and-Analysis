"""
随机边采样：从图的边集合中抽取子集。

意图：
- 常用于构造小规模训练子图或估计图统计量。
- 支持无向图去重，避免 (u,v) 与 (v,u) 重复计入。
- 不依赖 networkx 等库。
"""

from random import Random


Graph = dict[str, list[str]]
Edge = tuple[str, str]


def random_edge_sample(
    graph: Graph,
    sample_count: int,
    seed: int | None = None,
    undirected: bool = True,
) -> list[Edge]:
    """从图中不放回抽取 sample_count 条边。"""

    if sample_count < 0:
        raise ValueError("sample_count 不能为负数")

    edges = _edge_list(graph, undirected)
    rng = Random(seed)
    return rng.sample(edges, min(sample_count, len(edges)))


def _edge_list(graph: Graph, undirected: bool) -> list[Edge]:
    """展开图的边列表。"""

    seen: set[tuple[str, str]] = set()
    edges: list[Edge] = []
    for source in sorted(graph):
        for target in sorted(graph[source]):
            key = tuple(sorted((source, target))) if undirected else (source, target)
            if key in seen:
                continue
            seen.add(key)
            edges.append((source, target))
    return edges


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["A"], "C": ["A"]}
    sample = random_edge_sample(graph, 2, seed=2)
    assert sample == [("A", "B"), ("A", "C")]
    assert len(random_edge_sample(graph, 10, seed=1)) == 2

    print("008_random_edge_sampling: all examples passed")
