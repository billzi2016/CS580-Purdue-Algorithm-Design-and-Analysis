"""
Lamport Clock：标量逻辑时钟。

意图：保证如果 a happened-before b，则 C(a) < C(b)；但无法判断并发。
"""

from dataclasses import dataclass


@dataclass
class LamportClock:
    """单进程 Lamport 时钟。"""

    process_id: str
    time: int = 0

    def local_event(self) -> int:
        """本地事件递增时钟。"""

        self.time += 1
        return self.time

    def send(self) -> tuple[int, str]:
        """发送消息并附带时间戳。"""

        self.local_event()
        return self.time, self.process_id

    def receive(self, timestamp: int) -> int:
        """接收消息时取 max 后再加一。"""

        self.time = max(self.time, timestamp) + 1
        return self.time


def total_order_stamp(timestamp: int, process_id: str) -> tuple[int, str]:
    """用进程号打破同时间戳平局，形成全序。"""

    return timestamp, process_id


if __name__ == "__main__":
    a = LamportClock("A")
    b = LamportClock("B")
    message_time, sender = a.send()
    assert message_time == 1
    assert b.receive(message_time) == 2
    assert total_order_stamp(2, "A") < total_order_stamp(2, "B")

    print("004_lamport_clock: all examples passed")
