"""
Node2Vec 二阶有偏随机游走采样。

意图：
- 根据前一个节点 prev、当前节点 current 和候选下一跳 next 调整采样权重。
- p 控制返回上一节点的倾向，q 控制向外探索的倾向。
- 这里只实现采样路径，不调用 embedding 或 Word2Vec 库。
"""

from random import Random


Graph = dict[str, list[str]]


def node2vec_walk(
    graph: Graph,
    start: str,
    walk_length: int,
    p: float = 1.0,
    q: float = 1.0,
    seed: int | None = None,
) -> list[str]:
    """生成一条 Node2Vec 有偏随机游走。"""

    if p <= 0 or q <= 0:
        raise ValueError("p 和 q 必须为正数")
    if walk_length <= 0:
        return []
    if start not in graph:
        raise KeyError("start 不在图中")

    rng = Random(seed)
    walk = [start]
    while len(walk) < walk_length:
        current = walk[-1]
        neighbors = graph.get(current, [])
        if not neighbors:
            break
        if len(walk) == 1:
            walk.append(rng.choice(neighbors))
        else:
            previous = walk[-2]
            walk.append(_weighted_next(graph, previous, current, neighbors, p, q, rng))
    return walk


def _weighted_next(
    graph: Graph,
    previous: str,
    current: str,
    neighbors: list[str],
    p: float,
    q: float,
    rng: Random,
) -> str:
    """按 Node2Vec 权重从 neighbors 中选下一跳。"""

    previous_neighbors = set(graph.get(previous, []))
    weights: list[float] = []
    for candidate in neighbors:
        if candidate == previous:
            weights.append(1 / p)
        elif candidate in previous_neighbors:
            weights.append(1.0)
        else:
            weights.append(1 / q)

    threshold = rng.random() * sum(weights)
    cumulative = 0.0
    for candidate, weight in zip(neighbors, weights, strict=True):
        cumulative += weight
        if cumulative >= threshold:
            return candidate
    return neighbors[-1]


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["A", "C", "D"], "C": ["A", "B"], "D": ["B"]}
    walk = node2vec_walk(graph, "A", 6, p=0.5, q=2.0, seed=4)
    assert walk == ["A", "B", "A", "C", "A", "B"]
    assert node2vec_walk(graph, "A", 0, seed=1) == []

    print("004_node2vec_sampling: all examples passed")
