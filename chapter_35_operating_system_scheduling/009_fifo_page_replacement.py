"""
FIFO 页面置换算法。

意图：
- 页面缺失时淘汰最早进入内存的页面。
- 实现简单，但可能出现 Belady anomaly。
- 返回每一步是否命中，便于调试页面访问轨迹。
"""

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class PageEvent:
    """一次页面访问事件。"""

    page: int
    hit: bool
    frames: tuple[int, ...]


def fifo_page_replacement(
    references: list[int], frame_count: int
) -> tuple[int, list[PageEvent]]:
    """执行 FIFO 页面置换，返回缺页次数和事件列表。"""

    if frame_count <= 0:
        raise ValueError("frame_count 必须为正数")

    queue: deque[int] = deque()
    resident: set[int] = set()
    faults = 0
    events: list[PageEvent] = []

    for page in references:
        hit = page in resident
        if not hit:
            faults += 1
            if len(queue) == frame_count:
                evicted = queue.popleft()
                resident.remove(evicted)
            queue.append(page)
            resident.add(page)
        events.append(PageEvent(page, hit, tuple(queue)))

    return faults, events


if __name__ == "__main__":
    faults, events = fifo_page_replacement([1, 2, 3, 1, 4, 2, 5], 3)
    assert faults == 5
    assert [event.hit for event in events] == [
        False,
        False,
        False,
        True,
        False,
        True,
        False,
    ]
    assert events[-1].frames == (3, 4, 5)

    print("009_fifo_page_replacement: all examples passed")
