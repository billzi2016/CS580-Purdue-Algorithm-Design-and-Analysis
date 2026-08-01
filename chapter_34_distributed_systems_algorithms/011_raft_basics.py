"""
Raft 基础：选举和日志复制的核心规则。

意图：实现 request vote 和 append entries 的关键状态转移，便于理解 Raft 安全性。
"""

from dataclasses import dataclass, field


@dataclass
class RaftNode:
    """Raft 节点局部状态。"""

    node_id: str
    current_term: int = 0
    voted_for: str | None = None
    log: list[tuple[int, str]] = field(default_factory=list)

    def request_vote(self, term: int, candidate_id: str, last_log_index: int, last_log_term: int) -> bool:
        """处理 RequestVote RPC。"""

        if term < self.current_term:
            return False
        if term > self.current_term:
            self.current_term = term
            self.voted_for = None
        if self.voted_for not in (None, candidate_id):
            return False
        if not self._candidate_log_at_least_up_to_date(last_log_index, last_log_term):
            return False
        self.voted_for = candidate_id
        return True

    def append_entries(self, term: int, prev_log_index: int, prev_log_term: int, entries: list[tuple[int, str]]) -> bool:
        """处理 AppendEntries RPC 的日志一致性检查。"""

        if term < self.current_term:
            return False
        self.current_term = term
        if prev_log_index >= 0:
            if prev_log_index >= len(self.log) or self.log[prev_log_index][0] != prev_log_term:
                return False
        self.log = self.log[: prev_log_index + 1] + entries
        return True

    def _candidate_log_at_least_up_to_date(self, index: int, term: int) -> bool:
        my_term = self.log[-1][0] if self.log else 0
        my_index = len(self.log) - 1
        return (term, index) >= (my_term, my_index)


if __name__ == "__main__":
    follower = RaftNode("F", current_term=1, log=[(1, "set x")])
    assert follower.request_vote(2, "C", 0, 1)
    assert not follower.request_vote(2, "D", 0, 1)
    assert follower.append_entries(3, 0, 1, [(3, "set y")])
    assert follower.log == [(1, "set x"), (3, "set y")]

    print("011_raft_basics: all examples passed")
