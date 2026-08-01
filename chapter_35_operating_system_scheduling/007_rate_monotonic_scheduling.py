"""
Rate Monotonic Scheduling（RMS）固定优先级实时调度。

意图：
- 周期越短，静态优先级越高。
- 在离散时间轴上模拟周期任务释放、截止期和执行。
- 提供 Liu-Layland 利用率充分条件检查。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PeriodicTask:
    """周期实时任务：execution 为每个 job 需要的执行时间，period 也是相对截止期。"""

    name: str
    execution: int
    period: int


def rate_monotonic_schedule(
    tasks: list[PeriodicTask], horizon: int
) -> list[str | None]:
    """模拟 [0, horizon) 内每个时间单位运行哪个任务；None 表示 CPU 空闲。"""

    _validate(tasks, horizon)
    remaining = {task.name: 0 for task in tasks}
    timeline: list[str | None] = []
    ordered = sorted(tasks, key=lambda task: (task.period, task.name))

    for time in range(horizon):
        for task in ordered:
            if time % task.period == 0:
                remaining[task.name] += task.execution

        chosen = None
        for task in ordered:
            if remaining[task.name] > 0:
                chosen = task
                break

        if chosen is None:
            timeline.append(None)
        else:
            timeline.append(chosen.name)
            remaining[chosen.name] -= 1

    return timeline


def liu_layland_bound(task_count: int) -> float:
    """返回 n 个周期任务的 RMS 利用率充分上界。"""

    if task_count <= 0:
        raise ValueError("task_count 必须为正数")
    return task_count * (2 ** (1 / task_count) - 1)


def utilization(tasks: list[PeriodicTask]) -> float:
    """计算任务集 CPU 利用率。"""

    return sum(task.execution / task.period for task in tasks)


def _validate(tasks: list[PeriodicTask], horizon: int) -> None:
    """检查实时任务字段。"""

    if horizon < 0:
        raise ValueError("horizon 不能为负数")
    for task in tasks:
        if task.execution <= 0 or task.period <= 0 or task.execution > task.period:
            raise ValueError("任务必须满足 0 < execution <= period")


if __name__ == "__main__":
    tasks = [PeriodicTask("T1", 1, 4), PeriodicTask("T2", 2, 5)]
    assert rate_monotonic_schedule(tasks, 8) == [
        "T1",
        "T2",
        "T2",
        None,
        "T1",
        "T2",
        "T2",
        None,
    ]
    assert round(utilization(tasks), 2) == 0.65
    assert round(liu_layland_bound(2), 3) == 0.828

    print("007_rate_monotonic_scheduling: all examples passed")
