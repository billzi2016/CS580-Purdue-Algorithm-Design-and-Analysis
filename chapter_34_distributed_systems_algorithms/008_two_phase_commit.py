"""
Two-phase Commit（2PC）：prepare/vote 与 commit/abort 两阶段提交。

意图：展示协调者如何在所有参与者同意时提交，否则中止。
"""


def two_phase_commit(votes: dict[str, bool]) -> tuple[str, list[tuple[str, str]]]:
    """根据参与者 vote 结果返回最终决议和消息。"""

    if not votes:
        raise ValueError("votes 不能为空")
    messages: list[tuple[str, str]] = []
    for participant in sorted(votes):
        messages.append(("coordinator", f"PREPARE->{participant}"))
    decision = "COMMIT" if all(votes.values()) else "ABORT"
    for participant in sorted(votes):
        messages.append(("coordinator", f"{decision}->{participant}"))
    return decision, messages


def participant_vote(can_commit: bool) -> str:
    """参与者本地检查后的投票。"""

    return "YES" if can_commit else "NO"


if __name__ == "__main__":
    decision, messages = two_phase_commit({"A": True, "B": True})
    assert decision == "COMMIT"
    assert messages[-1] == ("coordinator", "COMMIT->B")
    assert two_phase_commit({"A": True, "B": False})[0] == "ABORT"
    assert participant_vote(False) == "NO"

    print("008_two_phase_commit: all examples passed")
