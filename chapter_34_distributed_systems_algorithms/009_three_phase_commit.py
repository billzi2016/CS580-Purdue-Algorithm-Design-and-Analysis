"""
Three-phase Commit（3PC）：CanCommit、PreCommit、DoCommit。

意图：用额外 pre-commit 阶段降低 2PC 阻塞风险；这里只模拟无故障路径。
"""


def three_phase_commit(votes: dict[str, bool]) -> tuple[str, list[str]]:
    """返回 3PC 决议和阶段消息。"""

    if not votes:
        raise ValueError("votes 不能为空")
    log: list[str] = ["CAN_COMMIT"]
    if not all(votes.values()):
        log.append("ABORT")
        return "ABORT", log
    log.append("PRE_COMMIT")
    acknowledgements = {participant: True for participant in votes}
    if not all(acknowledgements.values()):
        log.append("ABORT")
        return "ABORT", log
    log.append("DO_COMMIT")
    return "COMMIT", log


def participant_state_after(message: str) -> str:
    """参与者收到阶段消息后的状态。"""

    mapping = {
        "CAN_COMMIT": "WAITING",
        "PRE_COMMIT": "PRECOMMITTED",
        "DO_COMMIT": "COMMITTED",
        "ABORT": "ABORTED",
    }
    if message not in mapping:
        raise ValueError("未知 3PC 消息")
    return mapping[message]


if __name__ == "__main__":
    assert three_phase_commit({"A": True, "B": True}) == (
        "COMMIT",
        ["CAN_COMMIT", "PRE_COMMIT", "DO_COMMIT"],
    )
    assert three_phase_commit({"A": True, "B": False}) == (
        "ABORT",
        ["CAN_COMMIT", "ABORT"],
    )
    assert participant_state_after("PRE_COMMIT") == "PRECOMMITTED"

    print("009_three_phase_commit: all examples passed")
