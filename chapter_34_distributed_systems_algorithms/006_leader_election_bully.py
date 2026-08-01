"""
Bully Leader Election：高编号进程优先成为 leader。

意图：当某节点发现 leader 失效时，向更高编号存活节点发起选举；最高存活者获胜。
"""


def bully_election(process_ids: list[int], alive: set[int], initiator: int) -> int:
    """返回 Bully 算法选出的 leader。

    参数：process_ids 是系统中的进程编号，alive 是当前存活进程集合。
    返回值：发起者可观察到的最高编号存活进程。
    边界情况：发起者必须既存在于系统中也处于存活状态。
    """

    process_set = set(process_ids)
    if len(process_set) != len(process_ids):
        raise ValueError("process_ids 不能包含重复编号")
    if not alive <= process_set:
        raise ValueError("alive 必须是 process_ids 的子集")
    if initiator not in process_set:
        raise ValueError("initiator 必须存在于 process_ids")
    if initiator not in alive:
        raise ValueError("initiator 必须存活")
    higher_alive = [pid for pid in process_ids if pid > initiator and pid in alive]
    if not higher_alive:
        return initiator
    return max(higher_alive)


def election_messages(
    process_ids: list[int], alive: set[int], initiator: int
) -> list[tuple[int, int, str]]:
    """返回教学用消息轨迹。

    参数和约束与 bully_election 相同。
    返回值：按发送顺序记录 ELECTION、OK 和 COORDINATOR 消息。
    关键算法点：只有更高编号且存活的进程会回复 OK。
    """

    leader = bully_election(process_ids, alive, initiator)
    messages: list[tuple[int, int, str]] = []
    for pid in process_ids:
        if pid > initiator:
            messages.append((initiator, pid, "ELECTION"))
            if pid in alive:
                messages.append((pid, initiator, "OK"))
    for pid in process_ids:
        if pid != leader and pid in alive:
            messages.append((leader, pid, "COORDINATOR"))
    return messages


if __name__ == "__main__":
    assert bully_election([1, 2, 3, 4], {1, 2, 4}, 2) == 4
    assert bully_election([1, 2, 3], {1, 2}, 2) == 2
    assert (4, 2, "COORDINATOR") in election_messages([1, 2, 3, 4], {1, 2, 4}, 2)
    try:
        bully_election([1, 2, 3], {1, 2}, 4)
        raise AssertionError("不存在的 initiator 应触发异常")
    except ValueError:
        pass

    print("006_leader_election_bully: all examples passed")
