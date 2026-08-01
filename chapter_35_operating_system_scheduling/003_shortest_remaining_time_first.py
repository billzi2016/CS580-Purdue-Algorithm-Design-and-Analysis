"""
SRTF（Shortest Remaining Time First）抢占式最短剩余时间优先。

意图：
- 每当新进程到达时，重新选择剩余运行时间最短的进程。
- 输出执行片段 timeline，同时统计每个进程完成时间。
- 适合展示“抢占”如何改变 SJF 的执行顺序。
"""

from dataclasses import dataclass
from heapq import heappop, heappush


@dataclass(frozen=True)
class Process:
    """进程输入。"""

    pid: str
    arrival: int
    burst: int


@dataclass(frozen=True)
class Segment:
    """一次连续执行片段。"""

    pid: str
    start: int
    finish: int


def shortest_remaining_time_first(
    processes: list[Process],
) -> tuple[list[Segment], dict[str, int]]:
    """返回抢占式执行片段和每个进程的完成时间。"""

    _validate(processes)
    ordered = sorted(processes, key=lambda item: (item.arrival, item.pid))
    remaining = {process.pid: process.burst for process in processes}
    completion: dict[str, int] = {}
    ready: list[tuple[int, int, str]] = []
    timeline: list[Segment] = []
    time = 0
    index = 0

    while index < len(ordered) or ready:
        if not ready and index < len(ordered) and time < ordered[index].arrival:
            time = ordered[index].arrival

        while index < len(ordered) and ordered[index].arrival <= time:
            process = ordered[index]
            heappush(ready, (remaining[process.pid], process.arrival, process.pid))
            index += 1

        remain, arrival, pid = heappop(ready)
        next_arrival = ordered[index].arrival if index < len(ordered) else 10**18
        run_time = min(remain, next_arrival - time)
        start = time
        time += run_time
        remain -= run_time
        _append_segment(timeline, pid, start, time)

        if remain == 0:
            completion[pid] = time
        else:
            heappush(ready, (remain, arrival, pid))

    return timeline, completion


def turnaround_times(
    processes: list[Process], completion: dict[str, int]
) -> dict[str, int]:
    """根据完成时间计算周转时间。"""

    return {
        process.pid: completion[process.pid] - process.arrival for process in processes
    }


def _append_segment(timeline: list[Segment], pid: str, start: int, finish: int) -> None:
    """合并相邻同进程片段，保持 timeline 简洁。"""

    if start == finish:
        return
    if timeline and timeline[-1].pid == pid and timeline[-1].finish == start:
        last = timeline.pop()
        timeline.append(Segment(pid, last.start, finish))
    else:
        timeline.append(Segment(pid, start, finish))


def _validate(processes: list[Process]) -> None:
    """检查输入合法性。"""

    for process in processes:
        if process.arrival < 0 or process.burst <= 0:
            raise ValueError("arrival 必须非负，burst 必须为正")


if __name__ == "__main__":
    jobs = [Process("P1", 0, 8), Process("P2", 1, 4), Process("P3", 2, 2)]
    timeline, done = shortest_remaining_time_first(jobs)
    assert [(item.pid, item.start, item.finish) for item in timeline] == [
        ("P1", 0, 1),
        ("P2", 1, 2),
        ("P3", 2, 4),
        ("P2", 4, 7),
        ("P1", 7, 14),
    ]
    assert done == {"P3": 4, "P2": 7, "P1": 14}
    assert turnaround_times(jobs, done) == {"P1": 14, "P2": 6, "P3": 2}

    print("003_shortest_remaining_time_first: all examples passed")
