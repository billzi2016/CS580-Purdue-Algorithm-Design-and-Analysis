"""
SJF（Shortest Job First）非抢占式最短作业优先调度。

意图：
- 在当前已经到达的进程中选择 burst 最短者运行到完成。
- CPU 空闲且没有可运行进程时，时间跳到下一进程到达时间。
- 该策略可降低平均等待时间，但长作业可能饥饿。
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
class ScheduleEntry:
    """非抢占式调度记录。"""

    pid: str
    start: int
    finish: int
    waiting: int
    turnaround: int


def shortest_job_first(processes: list[Process]) -> list[ScheduleEntry]:
    """执行非抢占式 SJF，返回调度顺序与统计信息。"""

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
            heappush(ready, (process.burst, process.arrival, process.pid, process))
            index += 1

        burst, _, _, process = heappop(ready)
        start = time
        finish = start + burst
        result.append(
            ScheduleEntry(
                process.pid,
                start,
                finish,
                start - process.arrival,
                finish - process.arrival,
            )
        )
        time = finish

    return result


def _validate(processes: list[Process]) -> None:
    """检查输入合法性。"""

    for process in processes:
        if process.arrival < 0 or process.burst <= 0:
            raise ValueError("arrival 必须非负，burst 必须为正")


if __name__ == "__main__":
    jobs = [
        Process("P1", 0, 7),
        Process("P2", 2, 4),
        Process("P3", 4, 1),
        Process("P4", 5, 4),
    ]
    schedule = shortest_job_first(jobs)
    assert [item.pid for item in schedule] == ["P1", "P3", "P2", "P4"]
    assert [(item.start, item.finish) for item in schedule] == [
        (0, 7),
        (7, 8),
        (8, 12),
        (12, 16),
    ]
    assert [item.waiting for item in schedule] == [0, 3, 6, 7]

    delayed = shortest_job_first([Process("A", 5, 2)])
    assert delayed[0].start == 5 and delayed[0].finish == 7

    print("002_shortest_job_first: all examples passed")
