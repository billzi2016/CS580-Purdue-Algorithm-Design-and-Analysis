"""
FCFS（First-Come First-Served）先来先服务调度。

意图：
- 按进程到达时间排序，CPU 空闲时等待下一进程到达。
- 计算开始时间、完成时间、等待时间和周转时间。
- 作为后续 SJF、SRTF、Round Robin 的基准算法。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Process:
    """进程描述：pid 为进程名，arrival 为到达时间，burst 为运行时间。"""

    pid: str
    arrival: int
    burst: int


@dataclass(frozen=True)
class ScheduleEntry:
    """一次完整非抢占式执行记录。"""

    pid: str
    start: int
    finish: int
    waiting: int
    turnaround: int


def first_come_first_served(processes: list[Process]) -> list[ScheduleEntry]:
    """按到达顺序执行所有进程，返回每个进程的调度统计。"""

    _validate_processes(processes)
    time = 0
    result: list[ScheduleEntry] = []

    for process in sorted(processes, key=lambda item: (item.arrival, item.pid)):
        # 如果 CPU 在该进程到达前已经空闲，需要把时间推进到 arrival。
        start = max(time, process.arrival)
        finish = start + process.burst
        result.append(
            ScheduleEntry(
                pid=process.pid,
                start=start,
                finish=finish,
                waiting=start - process.arrival,
                turnaround=finish - process.arrival,
            )
        )
        time = finish

    return result


def average_waiting_time(entries: list[ScheduleEntry]) -> float:
    """计算平均等待时间；空列表返回 0.0。"""

    if not entries:
        return 0.0
    return sum(entry.waiting for entry in entries) / len(entries)


def _validate_processes(processes: list[Process]) -> None:
    """校验进程时间字段，避免负时间或零运行时间污染调度结果。"""

    for process in processes:
        if process.arrival < 0:
            raise ValueError("arrival 不能为负数")
        if process.burst <= 0:
            raise ValueError("burst 必须为正数")


if __name__ == "__main__":
    jobs = [Process("P1", 0, 5), Process("P2", 2, 3), Process("P3", 4, 1)]
    schedule = first_come_first_served(jobs)
    assert [(item.pid, item.start, item.finish) for item in schedule] == [
        ("P1", 0, 5),
        ("P2", 5, 8),
        ("P3", 8, 9),
    ]
    assert [item.waiting for item in schedule] == [0, 3, 4]
    assert average_waiting_time(schedule) == 7 / 3
    assert first_come_first_served([]) == []

    print("001_first_come_first_served: all examples passed")
