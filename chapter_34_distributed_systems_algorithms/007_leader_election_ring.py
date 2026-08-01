"""
Ring Leader Election：沿环传递候选编号，最大编号成为 leader。

意图：展示环拓扑中选主消息如何收集候选并宣布协调者。
"""


def ring_election(ring: list[int], alive: set[int], initiator: int) -> int:
    """返回环选举 leader。"""

    if initiator not in alive:
        raise ValueError("initiator 必须存活")
    if not alive:
        raise ValueError("alive 不能为空")
    return max(pid for pid in ring if pid in alive)


def ring_election_path(ring: list[int], alive: set[int], initiator: int) -> list[int]:
    """返回 election 消息经过的存活节点顺序，直到回到 initiator。"""

    if initiator not in ring:
        raise ValueError("initiator 不在环中")
    start = ring.index(initiator)
    path: list[int] = []
    for step in range(len(ring)):
        pid = ring[(start + step) % len(ring)]
        if pid in alive:
            path.append(pid)
    return path


if __name__ == "__main__":
    ring = [1, 2, 3, 4, 5]
    assert ring_election(ring, {1, 3, 5}, 3) == 5
    assert ring_election_path(ring, {1, 3, 5}, 3) == [3, 5, 1]

    print("007_leader_election_ring: all examples passed")
