"""
文件意图：手写实现 Andrew monotone chain 凸包算法。
适用场景：从平面点集提取包含所有点的最小凸多边形边界。
核心思想：按字典序排序点后分别构造下凸壳和上凸壳，右转或共线内点被移除。
输入输出：输入整数坐标点，返回逆时针凸包顶点，不重复首尾。
时间复杂度：O(n log n)。空间复杂度：O(n)。
关键边界：空集、单点和全共线点可处理；输出仅保留共线端点。
"""

Point = tuple[int, int]


def _merge_sort_points(points: list[Point]) -> list[Point]:
    """按 (x, y) 使用手写归并排序点列表。"""
    if len(points) <= 1:
        return points[:]
    middle = len(points) // 2
    left = _merge_sort_points(points[:middle])
    right = _merge_sort_points(points[middle:])
    result: list[Point] = []
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


def _cross(origin: Point, first: Point, second: Point) -> int:
    """返回 origin->first 与 origin->second 的叉积。"""
    return (first[0] - origin[0]) * (second[1] - origin[1]) - (first[1] - origin[1]) * (second[0] - origin[0])


def convex_hull(points: list[Point]) -> list[Point]:
    """返回 points 的逆时针凸包顶点。

    参数：points 为可重复的二维整数坐标点。
    返回：不重复首尾的逆时针凸包；全共线时仅返回两个端点。
    边界情况：空集返回空，单点返回该点。
    关键算法点：维护的链始终凸；叉积非正时移除中间点以排除右转和共线内点。
    """
    ordered = _merge_sort_points(points)
    unique: list[Point] = []
    for point in ordered:
        if not unique or point != unique[-1]:
            unique.append(point)
    if len(unique) <= 1:
        return unique
    lower: list[Point] = []
    for point in unique:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper: list[Point] = []
    for point in reversed(unique):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


if __name__ == "__main__":
    assert convex_hull([]) == []
    assert convex_hull([(1, 1)]) == [(1, 1)]
    assert convex_hull([(0, 0), (1, 0), (2, 0), (1, 0)]) == [(0, 0), (2, 0)]
    assert convex_hull([(0, 0), (1, 1), (2, 0), (1, 2), (1, 0)]) == [(0, 0), (2, 0), (1, 2)]
    print("004_convex_hull: all examples passed")
