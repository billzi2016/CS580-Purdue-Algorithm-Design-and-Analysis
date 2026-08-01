"""
DeepWalk 风格随机游走采样。

意图：
- 为每个节点生成若干条均匀随机游走序列。
- 这些序列通常会交给 Skip-Gram 训练；本文件只实现采样算法，不做神经网络训练。
- 输出顺序固定为排序后的节点，seed 控制随机性。
"""

from random import Random


Graph = dict[str, list[str]]


def deepwalk_sample(
    graph: Graph,
    walk_length: int,
    walks_per_node: int,
    seed: int | None = None,
) -> list[list[str]]:
    """为每个节点生成 walks_per_node 条随机游走。"""

    if walk_length <= 0 or walks_per_node < 0:
        raise ValueError("walk_length 必须为正，walks_per_node 不能为负")

    rng = Random(seed)
    walks: list[list[str]] = []
    for _ in range(walks_per_node):
        nodes = sorted(graph)
        rng.shuffle(nodes)
        for node in nodes:
            walks.append(_walk_once(graph, node, walk_length, rng))
    return walks


def _walk_once(graph: Graph, start: str, walk_length: int, rng: Random) -> list[str]:
    """生成单条均匀随机游走。"""

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
    graph = {"A": ["B"], "B": ["A", "C"], "C": ["B"]}
    walks = deepwalk_sample(graph, walk_length=4, walks_per_node=2, seed=3)
    assert len(walks) == 6
    assert all(1 <= len(walk) <= 4 for walk in walks)
    assert set(walk[0] for walk in walks) == {"A", "B", "C"}

    print("003_deepwalk_sampling: all examples passed")
