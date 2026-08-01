"""
Personalized PageRank：带重启偏好的随机游走稳态分数。

意图：
- 用 power iteration 手写 PPR，不调用图学习库。
- personalization 指定重启分布，alpha 表示继续沿边走的概率。
- 处理 dangling node：无出边节点按 personalization 分布跳转。
"""

Graph = dict[str, list[str]]


def personalized_pagerank(
    graph: Graph,
    personalization: dict[str, float],
    alpha: float = 0.85,
    iterations: int = 50,
) -> dict[str, float]:
    """返回每个节点的 PPR 分数。"""

    if not 0 <= alpha < 1:
        raise ValueError("alpha 必须在 [0, 1) 内")
    if iterations < 0:
        raise ValueError("iterations 不能为负数")

    nodes = sorted(graph)
    restart = _normalize_distribution(personalization, nodes)
    scores = restart.copy()

    for _ in range(iterations):
        next_scores = {node: (1 - alpha) * restart[node] for node in nodes}
        for node in nodes:
            neighbors = graph.get(node, [])
            if not neighbors:
                for target in nodes:
                    next_scores[target] += alpha * scores[node] * restart[target]
            else:
                share = alpha * scores[node] / len(neighbors)
                for target in neighbors:
                    next_scores[target] += share
        scores = next_scores

    total = sum(scores.values())
    return {node: value / total for node, value in scores.items()}


def _normalize_distribution(
    weights: dict[str, float], nodes: list[str]
) -> dict[str, float]:
    """把 personalization 权重归一化到图节点集合。"""

    total = sum(weights.get(node, 0.0) for node in nodes)
    if total <= 0:
        raise ValueError("personalization 在图节点上必须有正权重")
    return {node: weights.get(node, 0.0) / total for node in nodes}


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["C"], "C": ["A"]}
    scores = personalized_pagerank(graph, {"A": 1.0}, alpha=0.85, iterations=40)
    assert round(sum(scores.values()), 6) == 1.0
    assert scores["A"] > scores["B"]
    assert scores["C"] > scores["B"]

    print("002_personalized_pagerank: all examples passed")
