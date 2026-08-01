"""
Two-phase Locking（2PL）：事务先增长锁集合，再释放锁；释放后不能再加锁。

意图：展示 2PL 的状态约束，而不是实现完整数据库锁管理器。
"""

from dataclasses import dataclass, field


@dataclass
class LockManager2PL:
    """教学版独占锁管理器。"""

    owners: dict[str, str] = field(default_factory=dict)
    shrinking: set[str] = field(default_factory=set)
    held: dict[str, set[str]] = field(default_factory=dict)

    def acquire(self, transaction: str, item: str) -> bool:
        """事务申请独占锁；如果已进入 shrinking 阶段则拒绝。"""

        if transaction in self.shrinking:
            return False
        owner = self.owners.get(item)
        if owner is not None and owner != transaction:
            return False
        self.owners[item] = transaction
        self.held.setdefault(transaction, set()).add(item)
        return True

    def release(self, transaction: str, item: str) -> bool:
        """释放锁，并使事务进入 shrinking 阶段。"""

        if self.owners.get(item) != transaction:
            return False
        del self.owners[item]
        self.held.get(transaction, set()).discard(item)
        self.shrinking.add(transaction)
        return True

    def release_all(self, transaction: str) -> None:
        """释放事务持有的所有锁。"""

        for item in list(self.held.get(transaction, set())):
            self.release(transaction, item)


if __name__ == "__main__":
    manager = LockManager2PL()
    assert manager.acquire("T1", "A")
    assert not manager.acquire("T2", "A")
    assert manager.release("T1", "A")
    assert not manager.acquire("T1", "B")
    assert manager.acquire("T2", "A")

    print("013_two_phase_locking: all examples passed")
