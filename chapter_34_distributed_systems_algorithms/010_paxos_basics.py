"""
Paxos 基础：prepare/promise 与 accept/accepted。

意图：实现单值 Paxos 的核心规则：更高 proposal number 覆盖承诺，已接受值需被继承。
"""

from dataclasses import dataclass


@dataclass
class Acceptor:
    """Paxos acceptor 状态。"""

    promised: int = -1
    accepted_number: int = -1
    accepted_value: str | None = None

    def prepare(self, proposal_number: int) -> tuple[bool, int, str | None]:
        """处理 prepare 请求。"""

        if proposal_number <= self.promised:
            return False, self.accepted_number, self.accepted_value
        self.promised = proposal_number
        return True, self.accepted_number, self.accepted_value

    def accept(self, proposal_number: int, value: str) -> bool:
        """处理 accept 请求。"""

        if proposal_number < self.promised:
            return False
        self.promised = proposal_number
        self.accepted_number = proposal_number
        self.accepted_value = value
        return True


def propose(acceptors: list[Acceptor], proposal_number: int, value: str) -> str | None:
    """向 acceptor quorum 提案，成功返回被选择的值。"""

    quorum = len(acceptors) // 2 + 1
    promises = [a.prepare(proposal_number) for a in acceptors]
    ok_promises = [item for item in promises if item[0]]
    if len(ok_promises) < quorum:
        return None
    inherited = [(number, accepted) for _, number, accepted in ok_promises if accepted is not None]
    chosen = max(inherited)[1] if inherited else value
    accepted_count = sum(1 for acceptor in acceptors if acceptor.accept(proposal_number, chosen))
    return chosen if accepted_count >= quorum else None


if __name__ == "__main__":
    acceptors = [Acceptor(), Acceptor(), Acceptor()]
    assert propose(acceptors, 1, "v1") == "v1"
    assert propose(acceptors, 0, "old") is None
    assert propose(acceptors, 2, "v2") == "v1"

    print("010_paxos_basics: all examples passed")
