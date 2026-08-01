"""
CRDT G-Counter：只增计数器。

意图：每个副本只增加自己的槽位，merge 时逐维取最大，保证最终一致。
"""

from dataclasses import dataclass, field


@dataclass
class GCounter:
    """Grow-only Counter。"""

    replica_id: str
    counts: dict[str, int] = field(default_factory=dict)

    def increment(self, amount: int = 1) -> None:
        """增加本副本计数。"""

        if amount < 0:
            raise ValueError("G-Counter 只能增加")
        self.counts[self.replica_id] = self.counts.get(self.replica_id, 0) + amount

    def value(self) -> int:
        """读取全局计数值。"""

        return sum(self.counts.values())

    def merge(self, other: "GCounter") -> None:
        """合并另一个副本状态。"""

        for replica, count in other.counts.items():
            self.counts[replica] = max(self.counts.get(replica, 0), count)


if __name__ == "__main__":
    a = GCounter("A")
    b = GCounter("B")
    a.increment(2)
    b.increment(3)
    a.merge(b)
    b.merge(a)
    assert a.value() == 5 and b.value() == 5
    a.increment()
    assert a.value() == 6

    print("012_crdt_g_counter: all examples passed")
