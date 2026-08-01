"""
文件意图：手写实现闭线段相交判断。
适用场景：多边形边检测、地图几何和线段交叉约束。
核心思想：一般情形中两端点必须位于对方直线两侧；共线情形额外检查投影区间重叠。
输入输出：输入两条线段的端点，返回是否存在公共点。
时间复杂度：O(1)。空间复杂度：O(1)。
关键边界：端点接触、完全重合和部分共线重叠都视为相交。
"""

Point = tuple[int, int]


def _cross(first: Point, second: Point, third: Point) -> int:
    """返回向量 first->second 与 first->third 的二维叉积。"""
    return (second[0] - first[0]) * (third[1] - first[1]) - (second[1] - first[1]) * (
        third[0] - first[0]
    )


def _on_segment(first: Point, middle: Point, last: Point) -> bool:
    """在三点共线前提下，判断 middle 是否落在闭线段 first-last 上。"""
    return min(first[0], last[0]) <= middle[0] <= max(first[0], last[0]) and min(
        first[1], last[1]
    ) <= middle[1] <= max(first[1], last[1])


def segments_intersect(
    first_start: Point, first_end: Point, second_start: Point, second_end: Point
) -> bool:
    """判断两条闭线段是否相交。

    参数：first_start、first_end、second_start、second_end 为整数坐标端点。
    返回：只要共享任一点即返回 True。
    边界情况：端点触碰和共线重叠均返回 True。
    关键算法点：叉积符号相反处理一般相交，叉积为零时转为边界包含检查。
    """
    first_to_second_start = _cross(first_start, first_end, second_start)
    first_to_second_end = _cross(first_start, first_end, second_end)
    second_to_first_start = _cross(second_start, second_end, first_start)
    second_to_first_end = _cross(second_start, second_end, first_end)
    if (
        (first_to_second_start > 0 > first_to_second_end)
        or (first_to_second_start < 0 < first_to_second_end)
    ) and (
        (second_to_first_start > 0 > second_to_first_end)
        or (second_to_first_start < 0 < second_to_first_end)
    ):
        return True
    return (
        (
            first_to_second_start == 0
            and _on_segment(first_start, second_start, first_end)
        )
        or (
            first_to_second_end == 0 and _on_segment(first_start, second_end, first_end)
        )
        or (
            second_to_first_start == 0
            and _on_segment(second_start, first_start, second_end)
        )
        or (
            second_to_first_end == 0
            and _on_segment(second_start, first_end, second_end)
        )
    )


if __name__ == "__main__":
    assert segments_intersect((0, 0), (3, 3), (0, 3), (3, 0))
    assert not segments_intersect((0, 0), (1, 0), (2, 0), (3, 0))
    assert segments_intersect((0, 0), (2, 0), (2, 0), (2, 2))
    assert segments_intersect((0, 0), (3, 0), (1, 0), (4, 0))
    print("002_segment_intersection: all examples passed")
