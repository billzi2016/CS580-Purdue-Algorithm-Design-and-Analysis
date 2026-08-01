"""
Round Robin 时间片轮转调度。

意图：
- 每个就绪进程最多运行 quantum 时间，然后未完成则回到队尾。
- 显式处理进程到达、CPU 空闲和完成时间统计。
- 体现交互式系统中公平性和上下文切换频率的权衡。
"""

from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Process:
    """进程输入。"""

    pid: str
    arrival: int
    burst: int


@dataclass(frozen=True)
class Segment:
    """执行时间片。"""

    pid: str
    start: int
    finish: int


def round_robin(processes: list[Process], quantum: int) -> tuple[list[Segment], dict[str, int]]:
    """执行 Round Robin，返回 timeline 和完成时间。"""

    if quantum <= 0:
        raise ValueError("quantum 必须为正数")
    _validate(processes)

    ordered = sorted(processes, key=lambda item: (item.arrival, item.pid))
    remaining = {process.pid: process.burst for process in ordered}
    ready: deque[Process] = deque()
    timeline: list[Segment] = []
    completion: dict[str, int] = {}
    time = 0
    index = 0

    while index < len(ordered) or ready:
        if not ready and index < len(ordered) and time < ordered[index].arrival:
            time = ordered[index].arrival
        while index < len(ordered) and ordered[index].arrival <= time:
            ready.append(ordered[index])
            index += 1

        process = ready.popleft()
        run_time = min(quantum, remaining[process.pid])
        start = time
        time += run_time
        remaining[process.pid] -= run_time
        timeline.append(Segment(process.pid, start, time))

        # 新到达进程应在当前进程重新入队前进入队列，符合常见 RR 语义。
        while index < len(ordered) and ordered[index].arrival <= time:
            ready.append(ordered[index])
            index += 1
        if remaining[process.pid] > 0:
            ready.append(process)
        else:
            completion[process.pid] = time

    return timeline, completion


def _validate(processes: list[Process]) -> None:
    """检查进程字段。"""

    for process in processes:
        if process.arrival < 0 or process.burst <= 0:
            raise ValueError("arrival 必须非负，burst 必须为正")


if __name__ == "__main__":
    jobs = [Process("P1", 0, 5), Process("P2", 1, 3), Process("P3", 2, 1)]
    timeline, completion = round_robin(jobs, quantum=2)
    assert [(item.pid, item.start, item.finish) for item in timeline] == [
        ("P1", 0, 2),
        ("P2", 2, 4),
        ("P3", 4, 5),
        ("P1", 5, 7),
        ("P2", 7, 8),
        ("P1", 8, 9),
    ]
    assert completion == {"P3": 5, "P2": 8, "P1": 9}

    print("004_round_robin: all examples passed")
