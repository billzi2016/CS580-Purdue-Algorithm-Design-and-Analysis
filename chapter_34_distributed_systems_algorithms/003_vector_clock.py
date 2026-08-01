"""
Vector Clock：用每个进程的逻辑计数判断因果关系。

意图：区分 happened-before、并发和相等事件。
"""

from dataclasses import dataclass


@dataclass
class VectorClock:
    """向量时钟。"""

    process_id: str
    clock: dict[str, int]

    def tick(self) -> None:
        """本地事件。"""

        self.clock[self.process_id] = self.clock.get(self.process_id, 0) + 1

    def send(self) -> dict[str, int]:
        """发送消息前 tick，并携带时钟副本。"""

        self.tick()
        return dict(self.clock)

    def receive(self, message_clock: dict[str, int]) -> None:
        """接收消息：逐维取最大，再 tick。"""

        for process, value in message_clock.items():
            self.clock[process] = max(self.clock.get(process, 0), value)
        self.tick()


def compare(left: dict[str, int], right: dict[str, int]) -> str:
    """比较两个向量时钟：before/after/equal/concurrent。"""

    processes = set(left) | set(right)
    le = all(left.get(p, 0) <= right.get(p, 0) for p in processes)
    ge = all(left.get(p, 0) >= right.get(p, 0) for p in processes)
    if le and ge:
        return "equal"
    if le:
        return "before"
    if ge:
        return "after"
    return "concurrent"


if __name__ == "__main__":
    a = VectorClock("A", {})
    b = VectorClock("B", {})
    msg = a.send()
    b.receive(msg)
    assert compare(msg, b.clock) == "before"
    a.tick()
    assert compare(a.clock, b.clock) == "concurrent"

    print("003_vector_clock: all examples passed")
