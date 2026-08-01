"""
Two-phase Commit（2PC）：prepare/vote 与 commit/abort 两阶段提交。

意图：展示协调者如何先发送 PREPARE 收集投票，再根据所有参与者是否同意来
广播 COMMIT 或 ABORT。输入是每个参与者的可提交布尔值，输出全局决议、消息
轨迹和参与者最终状态。

教学范围：这是单协调者、无超时、无日志恢复的基础版，用来说明 2PC 的两个
阶段和状态转移；不冒充分布式数据库的工业级容错实现。

时间复杂度：O(n log n)，排序参与者用于稳定消息轨迹。空间复杂度：O(n)。
边界情况：参与者集合不能为空，且参与者名称不能是空字符串。
"""


def two_phase_commit(
    votes: dict[str, bool],
) -> tuple[str, list[tuple[str, str]], dict[str, str]]:
    """根据参与者 vote 结果返回最终决议、消息和状态。

    参数：votes 把参与者名称映射到本地能否提交。
    返回值：全局决议、协调者/参与者消息轨迹、每个参与者最终状态。
    关键算法点：任一参与者投 NO 时，全局必须 ABORT；只有全 YES 才 COMMIT。
    """

    if not votes:
        raise ValueError("votes 不能为空")
    if any(not participant for participant in votes):
        raise ValueError("参与者名称不能为空")
    messages: list[tuple[str, str]] = []
    states = {participant: "INIT" for participant in votes}
    for participant in sorted(votes):
        messages.append(("coordinator", f"PREPARE->{participant}"))
        states[participant] = "READY" if votes[participant] else "ABORT"
        messages.append((participant, participant_vote(votes[participant])))
    decision = "COMMIT" if all(votes.values()) else "ABORT"
    for participant in sorted(votes):
        messages.append(("coordinator", f"{decision}->{participant}"))
        states[participant] = decision
    return decision, messages, states


def participant_vote(can_commit: bool) -> str:
    """参与者本地检查后的投票。

    参数：can_commit 表示本地约束、锁和资源是否允许提交。
    返回值：YES 或 NO。
    边界情况：本教学函数只表达投票，不模拟日志、锁等待和超时恢复。
    """

    return "YES" if can_commit else "NO"


if __name__ == "__main__":
    decision, messages, states = two_phase_commit({"A": True, "B": True})
    assert decision == "COMMIT"
    assert messages[-1] == ("coordinator", "COMMIT->B")
    assert states == {"A": "COMMIT", "B": "COMMIT"}
    assert two_phase_commit({"A": True, "B": False})[0] == "ABORT"
    assert participant_vote(False) == "NO"
    try:
        two_phase_commit({})
        raise AssertionError("空参与者集合应触发异常")
    except ValueError:
        pass

    print("008_two_phase_commit: all examples passed")
