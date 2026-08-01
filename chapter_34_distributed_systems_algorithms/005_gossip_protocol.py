"""
Gossip Protocol：节点随机传播已知信息。

意图：模拟 epidemic dissemination，每轮每个已知消息的节点随机联系 fanout 个
其他节点。输入是节点列表、初始已知集合、fanout、轮数和随机种子，输出每轮
结束后的已知节点集合。

时间复杂度：O(r * i * n)，r 为轮数，i 为每轮已知节点数，n 为节点总数。
空间复杂度：O(r * n)，用于保存教学轨迹。
边界情况：初始已知节点必须属于节点列表，fanout 和 rounds 不能为负。
"""

from random import Random


def gossip_rounds(
    nodes: list[str],
    initial_informed: set[str],
    fanout: int,
    rounds: int,
    seed: int | None = None,
) -> list[set[str]]:
    """返回每一轮结束后已知消息的节点集合。

    参数：nodes 是所有节点；initial_informed 是已经知道消息的节点集合。
    返回值：第 0 项是初始状态，之后每项是一轮传播后的集合。
    关键算法点：每轮基于上一轮快照传播，避免同一轮中新感染节点立刻继续传播。
    """

    if fanout < 0 or rounds < 0:
        raise ValueError("fanout 和 rounds 不能为负数")
    node_set = set(nodes)
    if len(node_set) != len(nodes):
        raise ValueError("nodes 不能包含重复节点")
    if not initial_informed <= node_set:
        raise ValueError("initial_informed 必须是 nodes 的子集")
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
    assert gossip_rounds(["A"], set(), fanout=1, rounds=2, seed=1) == [
        set(),
        set(),
        set(),
    ]
    try:
        gossip_rounds(["A"], {"Z"}, fanout=1, rounds=1)
        raise AssertionError("未知初始节点应触发异常")
    except ValueError:
        pass

    print("005_gossip_protocol: all examples passed")
