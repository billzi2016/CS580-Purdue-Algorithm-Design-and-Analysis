"""
优先级调度：选择已到达进程中优先级最高者运行。

意图：
- 实现非抢占式 priority scheduling。
- 默认数值越小优先级越高，这是操作系统教材中常见约定。
- 用 arrival 和 pid 作为稳定 tie-breaker，保证结果可复现。
"""

from dataclasses import dataclass
from heapq import heappop, heappush


@dataclass(frozen=True)
class Process:
    """带优先级的进程输入。"""

    pid: str
    arrival: int
    burst: int
    priority: int


@dataclass(frozen=True)
class ScheduleEntry:
    """调度记录。"""

    pid: str
    start: int
    finish: int


def priority_scheduling(processes: list[Process]) -> list[ScheduleEntry]:
    """执行非抢占式优先级调度。"""

    _validate(processes)
    ordered = sorted(processes, key=lambda item: (item.arrival, item.pid))
    ready: list[tuple[int, int, str, Process]] = []
    result: list[ScheduleEntry] = []
    time = 0
    index = 0

    while index < len(ordered) or ready:
        if not ready and index < len(ordered) and time < ordered[index].arrival:
            time = ordered[index].arrival
        while index < len(ordered) and ordered[index].arrival <= time:
            process = ordered[index]
            heappush(ready, (process.priority, process.arrival, process.pid, process))
            index += 1

        _, _, _, process = heappop(ready)
        start = time
        finish = start + process.burst
        result.append(ScheduleEntry(process.pid, start, finish))
        time = finish

    return result


def _validate(processes: list[Process]) -> None:
    """检查输入合法性。"""

    for process in processes:
        if process.arrival < 0 or process.burst <= 0:
            raise ValueError("arrival 必须非负，burst 必须为正")


if __name__ == "__main__":
    jobs = [
        Process("P1", 0, 4, 3),
        Process("P2", 1, 3, 1),
        Process("P3", 2, 2, 2),
    ]
    schedule = priority_scheduling(jobs)
    assert [(item.pid, item.start, item.finish) for item in schedule] == [
        ("P1", 0, 4),
        ("P2", 4, 7),
        ("P3", 7, 9),
    ]

    print("005_priority_scheduling: all examples passed")
