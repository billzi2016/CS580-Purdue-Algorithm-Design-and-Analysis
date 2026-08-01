"""
文件意图：
    本文件手写实现活动选择问题，用于在活动开始/结束时间给定时选择最大兼容集合。

适用场景：
    活动互斥且权重相同，需要安排最多活动。

核心思想：
    与区间调度相同，选择最早结束的活动是安全选择；它不会减少后续可选活动数量。

时间复杂度：
    O(n log n)

空间复杂度：
    O(n)
"""

Activity = tuple[str, int, int]


def activity_selection(activities: list[Activity]) -> list[Activity]:
    """
    选择最多数量的兼容活动。

    参数：
        activities: 活动列表，每个元素为 (name, start, finish)。

    返回：
        按执行顺序排列的活动列表。
    """
    for _, start, finish in activities:
        if start > finish:
            raise ValueError("活动必须满足 start <= finish")

    selected: list[Activity] = []
    last_finish: int | None = None

    for activity in sorted(activities, key=lambda item: (item[2], item[1], item[0])):
        _, start, finish = activity
        if last_finish is None or start >= last_finish:
            selected.append(activity)
            last_finish = finish

    return selected


if __name__ == "__main__":
    activities = [
        ("a1", 1, 4),
        ("a2", 3, 5),
        ("a3", 0, 6),
        ("a4", 5, 7),
        ("a5", 8, 9),
        ("a6", 5, 9),
    ]
    assert [name for name, _, _ in activity_selection(activities)] == ["a1", "a4", "a5"]
    assert activity_selection([]) == []
    assert activity_selection([("single", 2, 2)]) == [("single", 2, 2)]

    print("002_activity_selection: all examples passed")
