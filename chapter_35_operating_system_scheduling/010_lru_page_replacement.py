"""
LRU（Least Recently Used）最近最少使用页面置换。

意图：
- 命中页面时更新其最近使用时间。
- 缺页且内存满时淘汰最久未访问页面。
- 用有序字典表达从旧到新的访问顺序。
"""

from collections import OrderedDict
from dataclasses import dataclass


@dataclass(frozen=True)
class PageEvent:
    """一次页面访问事件。"""

    page: int
    hit: bool
    frames_old_to_new: tuple[int, ...]


def lru_page_replacement(
    references: list[int], frame_count: int
) -> tuple[int, list[PageEvent]]:
    """执行 LRU 页面置换，返回缺页次数和事件列表。"""

    if frame_count <= 0:
        raise ValueError("frame_count 必须为正数")

    frames: OrderedDict[int, None] = OrderedDict()
    faults = 0
    events: list[PageEvent] = []

    for page in references:
        hit = page in frames
        if hit:
            frames.move_to_end(page)
        else:
            faults += 1
            if len(frames) == frame_count:
                frames.popitem(last=False)
            frames[page] = None
        events.append(PageEvent(page, hit, tuple(frames.keys())))

    return faults, events


if __name__ == "__main__":
    faults, events = lru_page_replacement([1, 2, 3, 1, 4, 2, 5], 3)
    assert faults == 6
    assert events[3].frames_old_to_new == (2, 3, 1)
    assert events[-1].frames_old_to_new == (4, 2, 5)

    print("010_lru_page_replacement: all examples passed")
