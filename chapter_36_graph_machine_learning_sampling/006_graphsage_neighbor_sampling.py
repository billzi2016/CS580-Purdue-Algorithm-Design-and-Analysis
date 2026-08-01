"""
GraphSAGE 邻居采样。

意图：
- 按层从 frontier 节点采样固定数量邻居。
- 不足 fanout 时返回全部邻居；可选是否有放回采样。
- 该采样结果可供后续聚合器使用，本文件不实现神经网络。
"""

from random import Random


Graph = dict[str, list[str]]


def graphsage_sample_neighbors(
    graph: Graph,
    seeds: list[str],
    fanouts: list[int],
    seed: int | None = None,
    replace: bool = False,
) -> list[set[str]]:
    """返回每一层采到的节点集合，第一层为输入 seeds。"""

    if any(fanout < 0 for fanout in fanouts):
        raise ValueError("fanout 不能为负数")

    rng = Random(seed)
    layers: list[set[str]] = [set(seeds)]
    frontier = set(seeds)

    for fanout in fanouts:
        sampled: set[str] = set()
        for node in sorted(frontier):
            neighbors = graph.get(node, [])
            if replace and neighbors:
                sampled.update(rng.choice(neighbors) for _ in range(fanout))
            else:
                count = min(fanout, len(neighbors))
                sampled.update(rng.sample(neighbors, count))
        layers.append(sampled)
        frontier = sampled

    return layers


if __name__ == "__main__":
    graph = {
        "A": ["B", "C", "D"],
        "B": ["E"],
        "C": ["E", "F"],
        "D": [],
        "E": [],
        "F": [],
    }
    layers = graphsage_sample_neighbors(graph, ["A"], [2, 1], seed=1)
    assert layers == [{"A"}, {"B", "D"}, {"E"}]
    assert graphsage_sample_neighbors(graph, ["D"], [2], seed=1) == [{"D"}, set()]

    print("006_graphsage_neighbor_sampling: all examples passed")
