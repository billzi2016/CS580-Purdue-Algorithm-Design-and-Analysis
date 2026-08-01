"""
图随机游走：从起点反复随机选择邻居。

意图：
- 手写基本 random walk，作为 DeepWalk、Node2Vec、PPR 采样基础。
- 支持 seed 以保证示例测试可复现。
- 遇到孤立点时停止，避免伪造不存在的下一跳。
"""

from random import Random


Graph = dict[str, list[str]]


def random_walk(
    graph: Graph, start: str, walk_length: int, seed: int | None = None
) -> list[str]:
    """从 start 开始生成最多 walk_length 个节点的随机游走序列。"""

    if walk_length <= 0:
        return []
    if start not in graph:
        raise KeyError("start 不在图中")

    rng = Random(seed)
    walk = [start]
    current = start

    while len(walk) < walk_length:
        neighbors = graph.get(current, [])
        if not neighbors:
            break
        current = rng.choice(neighbors)
        walk.append(current)

    return walk


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["A"], "C": ["A", "D"], "D": []}
    assert random_walk(graph, "A", 5, seed=1) == ["A", "B", "A", "C", "A"]
    assert random_walk(graph, "D", 5, seed=1) == ["D"]
    assert random_walk(graph, "A", 0, seed=1) == []

    print("001_random_walk: all examples passed")
