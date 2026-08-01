"""
LADIES 采样基础：按邻居重要性抽取上一层节点。

意图：
- LADIES 完整算法涉及矩阵归一化和层依赖采样；这里实现核心的 layer-dependent
  importance sampling 思路。
- 对目标节点集合，候选源节点的重要性按连接到目标集合的边数计算。
- 不调用图学习库，保持算法步骤可审查。
"""

from random import Random


Graph = dict[str, list[str]]


def ladies_sample_sources(
    graph: Graph,
    target_nodes: set[str],
    sample_count: int,
    seed: int | None = None,
) -> list[str]:
    """根据连接到 target_nodes 的边数加权抽样源节点，不放回。"""

    if sample_count < 0:
        raise ValueError("sample_count 不能为负数")

    weights: dict[str, int] = {}
    for source, neighbors in graph.items():
        score = sum(1 for neighbor in neighbors if neighbor in target_nodes)
        if score > 0:
            weights[source] = score

    rng = Random(seed)
    selected: list[str] = []
    available = dict(weights)
    for _ in range(min(sample_count, len(available))):
        chosen = _weighted_choice(available, rng)
        selected.append(chosen)
        del available[chosen]
    return selected


def _weighted_choice(weights: dict[str, int], rng: Random) -> str:
    """从 name->weight 映射中按权重抽取一个键。"""

    total = sum(weights.values())
    threshold = rng.random() * total
    cumulative = 0.0
    for item in sorted(weights):
        cumulative += weights[item]
        if cumulative >= threshold:
            return item
    return sorted(weights)[-1]


if __name__ == "__main__":
    graph = {"A": ["X", "Y"], "B": ["Y"], "C": ["Z"], "D": ["X", "Y", "Z"]}
    assert ladies_sample_sources(graph, {"X", "Y"}, 2, seed=1) == ["A", "D"]
    assert ladies_sample_sources(graph, {"Q"}, 3, seed=1) == []

    print("007_ladies_sampling_basics: all examples passed")
