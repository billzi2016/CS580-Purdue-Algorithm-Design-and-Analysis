"""
Ring Leader Election：沿环传递候选编号，最大编号成为 leader。

意图：展示环拓扑中选主消息如何收集候选并宣布协调者。
"""


def ring_election(ring: list[int], alive: set[int], initiator: int) -> int:
    """返回环选举 leader。

    参数：ring 是环中进程顺序，alive 是存活集合，initiator 是发起者。
    返回值：存活进程中的最大编号。
    边界情况：发起者必须在环中且存活，alive 必须是 ring 的子集。
    """

    ring_set = set(ring)
    if len(ring_set) != len(ring):
        raise ValueError("ring 不能包含重复编号")
    if not alive:
        raise ValueError("alive 不能为空")
    if not alive <= ring_set:
        raise ValueError("alive 必须是 ring 的子集")
    if initiator not in ring_set:
        raise ValueError("initiator 不在环中")
    if initiator not in alive:
        raise ValueError("initiator 必须存活")
    return max(pid for pid in ring if pid in alive)


def ring_election_path(ring: list[int], alive: set[int], initiator: int) -> list[int]:
    """返回 election 消息经过的存活节点顺序，直到回到 initiator。

    参数和约束与 ring_election 相同。
    返回值：从发起者开始、按环顺序经过的存活进程列表。
    关键算法点：故障节点被跳过，但不能让故障发起者创建无效选举路径。
    """

    ring_election(ring, alive, initiator)
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
    try:
        ring_election_path(ring, {1, 5}, 3)
        raise AssertionError("故障 initiator 应触发异常")
    except ValueError:
        pass

    print("007_leader_election_ring: all examples passed")
