"""
Bully Leader Election：高编号进程优先成为 leader。

意图：当某节点发现 leader 失效时，向更高编号存活节点发起选举；最高存活者获胜。
"""


def bully_election(process_ids: list[int], alive: set[int], initiator: int) -> int:
    """返回 Bully 算法选出的 leader。"""

    if initiator not in alive:
        raise ValueError("initiator 必须存活")
    higher_alive = [pid for pid in process_ids if pid > initiator and pid in alive]
    if not higher_alive:
        return initiator
    return max(higher_alive)


def election_messages(
    process_ids: list[int], alive: set[int], initiator: int
) -> list[tuple[int, int, str]]:
    """返回教学用消息轨迹。"""

    messages: list[tuple[int, int, str]] = []
    for pid in process_ids:
        if pid > initiator:
            messages.append((initiator, pid, "ELECTION"))
            if pid in alive:
                messages.append((pid, initiator, "OK"))
    leader = bully_election(process_ids, alive, initiator)
    for pid in process_ids:
        if pid != leader and pid in alive:
            messages.append((leader, pid, "COORDINATOR"))
    return messages


if __name__ == "__main__":
    assert bully_election([1, 2, 3, 4], {1, 2, 4}, 2) == 4
    assert bully_election([1, 2, 3], {1, 2}, 2) == 2
    assert (4, 2, "COORDINATOR") in election_messages([1, 2, 3, 4], {1, 2, 4}, 2)

    print("006_leader_election_bully: all examples passed")
