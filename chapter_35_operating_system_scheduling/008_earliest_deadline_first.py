"""
EDF（Earliest Deadline First）最早截止期优先实时调度。

意图：
- 动态选择绝对截止期最早的已释放 job。
- 记录每个时间单位的运行任务，并检测是否有 job 错过截止期。
- EDF 在单处理器、可抢占、deadline=period 的模型下利用率不超过 1 时可调度。
"""

from dataclasses import dataclass
from heapq import heappop, heappush


@dataclass(frozen=True)
class PeriodicTask:
    """周期任务。"""

    name: str
    execution: int
    period: int
    deadline: int


def earliest_deadline_first(
    tasks: list[PeriodicTask], horizon: int
) -> tuple[list[str | None], bool]:
    """返回 EDF timeline 和是否无截止期违约。"""

    _validate(tasks, horizon)
    ready: list[tuple[int, str, int]] = []
    timeline: list[str | None] = []
    feasible = True

    for time in range(horizon):
        for task in tasks:
            if time % task.period == 0:
                heappush(ready, (time + task.deadline, task.name, task.execution))

        while ready and ready[0][0] <= time:
            # 截止期到达但仍未完成，说明调度失败。
            feasible = False
            heappop(ready)

        if not ready:
            timeline.append(None)
            continue

        deadline, name, remaining = heappop(ready)
        timeline.append(name)
        remaining -= 1
        if remaining > 0:
            heappush(ready, (deadline, name, remaining))

    return timeline, feasible


def _validate(tasks: list[PeriodicTask], horizon: int) -> None:
    """检查输入合法性。"""

    if horizon < 0:
        raise ValueError("horizon 不能为负数")
    for task in tasks:
        if task.execution <= 0 or task.period <= 0 or task.deadline <= 0:
            raise ValueError("execution、period、deadline 必须为正")
        if task.execution > task.deadline:
            raise ValueError("单个 job 执行时间不能超过相对截止期")


if __name__ == "__main__":
    tasks = [PeriodicTask("A", 1, 4, 4), PeriodicTask("B", 2, 5, 5)]
    timeline, feasible = earliest_deadline_first(tasks, 8)
    assert timeline == ["A", "B", "B", None, "A", "B", "B", None]
    assert feasible

    overloaded = [PeriodicTask("X", 2, 3, 3), PeriodicTask("Y", 2, 4, 4)]
    _, ok = earliest_deadline_first(overloaded, 12)
    assert not ok

    print("008_earliest_deadline_first: all examples passed")
