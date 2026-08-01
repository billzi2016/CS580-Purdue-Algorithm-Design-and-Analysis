"""
Gossip Protocol：节点随机传播已知信息。

意图：模拟 epidemic dissemination，每轮每个节点随机联系 fanout 个节点。
"""

from random import Random


def gossip_rounds(
    nodes: list[str],
    initial_informed: set[str],
    fanout: int,
    rounds: int,
    seed: int | None = None,
) -> list[set[str]]:
    """返回每一轮结束后已知消息的节点集合。"""

    if fanout < 0 or rounds < 0:
        raise ValueError("fanout 和 rounds 不能为负数")
    rng = Random(seed)
    informed = set(initial_informed)
    history = [set(informed)]
    for _ in range(rounds):
        new_informed = set(informed)
        for node in sorted(informed):
            candidates = [candidate for candidate in nodes if candidate != node]
            for target in rng.sample(candidates, min(fanout, len(candidates))):
                new_informed.add(target)
        informed = new_informed
        history.append(set(informed))
    return history


if __name__ == "__main__":
    history = gossip_rounds(["A", "B", "C", "D"], {"A"}, fanout=1, rounds=3, seed=1)
    assert history[0] == {"A"}
    assert history[-1] == {"A", "B", "C", "D"}

    print("005_gossip_protocol: all examples passed")
