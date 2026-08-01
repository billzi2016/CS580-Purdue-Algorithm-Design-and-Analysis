"""
文件意图：手写实现扫描线计算轴对齐矩形并集面积。
适用场景：计算平面中多个无旋转矩形覆盖区域的面积。
核心思想：按 x 坐标扫描，维护当前竖直条带覆盖的 y 区间并集长度。
输入输出：输入 (left,bottom,right,top) 矩形列表，返回并集面积。
时间复杂度：O(n^2 log n) 的基础教学版本。空间复杂度：O(n)。
关键边界：空输入和零面积矩形返回零；反向边界会被拒绝。
"""

Rectangle = tuple[float, float, float, float]
Interval = tuple[float, float]


def _merge_sort(items: list[tuple]) -> list[tuple]:
    """按元组字典序使用手写归并排序。"""
    if len(items) <= 1:
        return items[:]
    middle = len(items) // 2
    left = _merge_sort(items[:middle])
    right = _merge_sort(items[middle:])
    result: list[tuple] = []
    left_index = right_index = 0
    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1
    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def _covered_length(intervals: list[Interval]) -> float:
    """返回 intervals 的一维并集长度。"""
    if not intervals:
        return 0.0
    ordered = _merge_sort(intervals)
    total = 0.0
    start, end = ordered[0]
    for next_start, next_end in ordered[1:]:
        if next_start > end:
            total += end - start
            start, end = next_start, next_end
        elif next_end > end:
            end = next_end
    return total + end - start


def rectangle_union_area(rectangles: list[Rectangle]) -> float:
    """返回轴对齐矩形列表的并集面积。

    参数：每个矩形为 (left, bottom, right, top)，且 left<=right、bottom<=top。
    返回：非负并集面积。
    边界情况：零面积矩形忽略，边界反向抛出 ValueError。
    关键算法点：两个相邻 x 事件之间覆盖集合不变，可用该区间宽度乘当前 y 并集长度。
    """
    events: list[tuple[float, int, float, float]] = []
    for left, bottom, right, top in rectangles:
        if left > right or bottom > top:
            raise ValueError("矩形边界必须满足 left<=right 且 bottom<=top")
        if left != right and bottom != top:
            events.append((left, 1, bottom, top))
            events.append((right, -1, bottom, top))
    if not events:
        return 0.0
    ordered_events = _merge_sort(events)
    active: list[Interval] = []
    area = 0.0
    previous_x = ordered_events[0][0]
    index = 0
    while index < len(ordered_events):
        current_x = ordered_events[index][0]
        area += (current_x - previous_x) * _covered_length(active)
        while index < len(ordered_events) and ordered_events[index][0] == current_x:
            _, event_type, bottom, top = ordered_events[index]
            interval = (bottom, top)
            if event_type == 1:
                active.append(interval)
            else:
                active.remove(interval)
            index += 1
        previous_x = current_x
    return area


if __name__ == "__main__":
    assert rectangle_union_area([]) == 0.0
    assert rectangle_union_area([(0, 0, 2, 2)]) == 4.0
    assert rectangle_union_area([(0, 0, 2, 2), (1, 1, 3, 3)]) == 7.0
    assert rectangle_union_area([(0, 0, 1, 1), (1, 0, 2, 1)]) == 2.0
    assert rectangle_union_area([(0, 0, 0, 4)]) == 0.0
    print("006_sweep_line: all examples passed")
