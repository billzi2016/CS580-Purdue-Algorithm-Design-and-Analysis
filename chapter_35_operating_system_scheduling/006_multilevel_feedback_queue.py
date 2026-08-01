"""
MLFQ（Multilevel Feedback Queue）多级反馈队列调度。

意图：
- 用多个时间片队列近似交互式系统调度。
- 新任务从最高优先级进入；用完整个时间片仍未完成则降级。
- 这里只实现核心机制，不加入 aging / I/O boost 等扩展策略。
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
    """MLFQ 执行片段，level 表示当时所在队列。"""

    pid: str
    level: int
    start: int
    finish: int


def multilevel_feedback_queue(
    processes: list[Process],
    quantums: list[int],
) -> tuple[list[Segment], dict[str, int]]:
    """执行简化 MLFQ，返回 timeline 和完成时间。"""

    if not quantums or any(quantum <= 0 for quantum in quantums):
        raise ValueError("quantums 必须是正整数列表")
    _validate(processes)

    ordered = sorted(processes, key=lambda item: (item.arrival, item.pid))
    queues: list[deque[Process]] = [deque() for _ in quantums]
    levels: dict[str, int] = {}
    remaining = {process.pid: process.burst for process in ordered}
    timeline: list[Segment] = []
    completion: dict[str, int] = {}
    time = 0
    index = 0

    while index < len(ordered) or any(queues):
        if not any(queues) and index < len(ordered) and time < ordered[index].arrival:
            time = ordered[index].arrival
        while index < len(ordered) and ordered[index].arrival <= time:
            levels[ordered[index].pid] = 0
            queues[0].append(ordered[index])
            index += 1

        level = _first_non_empty_queue(queues)
        process = queues[level].popleft()
        run_time = min(quantums[level], remaining[process.pid])
        start = time
        time += run_time
        remaining[process.pid] -= run_time
        timeline.append(Segment(process.pid, level, start, time))

        while index < len(ordered) and ordered[index].arrival <= time:
            levels[ordered[index].pid] = 0
            queues[0].append(ordered[index])
            index += 1

        if remaining[process.pid] == 0:
            completion[process.pid] = time
        else:
            next_level = min(level + 1, len(queues) - 1)
            levels[process.pid] = next_level
            queues[next_level].append(process)

    return timeline, completion


def _first_non_empty_queue(queues: list[deque[Process]]) -> int:
    """返回最高优先级的非空队列下标。"""

    for index, queue in enumerate(queues):
        if queue:
            return index
    raise RuntimeError("没有可运行进程")


def _validate(processes: list[Process]) -> None:
    """检查进程字段。"""

    for process in processes:
        if process.arrival < 0 or process.burst <= 0:
            raise ValueError("arrival 必须非负，burst 必须为正")


if __name__ == "__main__":
    jobs = [Process("A", 0, 5), Process("B", 1, 2)]
    timeline, completion = multilevel_feedback_queue(jobs, [1, 2, 4])
    assert [(item.pid, item.level, item.start, item.finish) for item in timeline] == [
        ("A", 0, 0, 1),
        ("B", 0, 1, 2),
        ("A", 1, 2, 4),
        ("B", 1, 4, 5),
        ("A", 2, 5, 7),
    ]
    assert completion == {"B": 5, "A": 7}

    print("006_multilevel_feedback_queue: all examples passed")
