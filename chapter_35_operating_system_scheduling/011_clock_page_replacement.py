"""
Clock（二次机会）页面置换算法。

意图：
- 用循环指针和 reference bit 近似 LRU。
- 命中时设置引用位；置换时遇到引用位 1 就清零并跳过。
- 返回每步 frame 状态，便于观察指针行为。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class ClockEvent:
    """一次页面访问事件。"""

    page: int
    hit: bool
    frames: tuple[int | None, ...]
    reference_bits: tuple[int, ...]


def clock_page_replacement(references: list[int], frame_count: int) -> tuple[int, list[ClockEvent]]:
    """执行 Clock 页面置换，返回缺页次数和事件列表。"""

    if frame_count <= 0:
        raise ValueError("frame_count 必须为正数")

    frames: list[int | None] = [None] * frame_count
    reference_bits = [0] * frame_count
    hand = 0
    faults = 0
    events: list[ClockEvent] = []

    for page in references:
        if page in frames:
            index = frames.index(page)
            reference_bits[index] = 1
            events.append(ClockEvent(page, True, tuple(frames), tuple(reference_bits)))
            continue

        faults += 1
        while frames[hand] is not None and reference_bits[hand] == 1:
            reference_bits[hand] = 0
            hand = (hand + 1) % frame_count

        frames[hand] = page
        reference_bits[hand] = 1
        hand = (hand + 1) % frame_count
        events.append(ClockEvent(page, False, tuple(frames), tuple(reference_bits)))

    return faults, events


if __name__ == "__main__":
    faults, events = clock_page_replacement([1, 2, 3, 1, 4, 2, 5], 3)
    assert faults == 5
    assert events[3].hit
    assert len(events[-1].frames) == 3
    assert set(page for page in events[-1].frames if page is not None) == {4, 2, 5}

    print("011_clock_page_replacement: all examples passed")
