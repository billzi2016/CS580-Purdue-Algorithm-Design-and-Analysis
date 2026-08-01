"""
文件意图：
    本文件手写实现二维平面最近点对算法，用于找到欧氏距离最小的两个点。

适用场景：
    输入为二维点集，需要比 O(n^2) 暴力枚举更高效地求最近距离。

核心思想：
    按 x 坐标分治。递归求左右两侧最近距离 d 后，只需要检查靠近分割线、
    x 距离小于 d 的中间条带。条带按 y 坐标排序后，每个点只需检查后面
    少数可能点。

输入输出：
    输入点列表，返回最近点对和距离平方。使用距离平方避免不必要开方。

时间复杂度：
    O(n log n)

空间复杂度：
    O(n)
"""

from collections.abc import Sequence

Point = tuple[float, float]


def squared_distance(first: Point, second: Point) -> float:
    """
    计算两个二维点之间的欧氏距离平方。
    """
    dx = first[0] - second[0]
    dy = first[1] - second[1]
    return dx * dx + dy * dy


def closest_pair(points: Sequence[Point]) -> tuple[Point, Point, float]:
    """
    返回平面点集中距离最近的两个点和距离平方。

    参数：
        points: 二维点序列，每个点为 (x, y)。

    返回：
        (point_a, point_b, distance_squared)。

    边界情况：
        少于两个点时不存在点对，抛出 ValueError。
    """
    if len(points) < 2:
        raise ValueError("至少需要两个点才能计算最近点对")

    points_by_x = sorted(points, key=lambda point: (point[0], point[1]))
    points_by_y = sorted(points, key=lambda point: (point[1], point[0]))
    return _closest_pair_recursive(points_by_x, points_by_y)


def _closest_pair_recursive(points_by_x: list[Point], points_by_y: list[Point]) -> tuple[Point, Point, float]:
    """
    在已按 x/y 排序的点集中递归求最近点对。
    """
    count = len(points_by_x)

    if count <= 3:
        return _brute_force_closest_pair(points_by_x)

    middle = count // 2
    left_by_x = points_by_x[:middle]
    right_by_x = points_by_x[middle:]
    split_x = points_by_x[middle][0]

    left_set = set(left_by_x)
    left_by_y: list[Point] = []
    right_by_y: list[Point] = []

    for point in points_by_y:
        if point in left_set:
            left_by_y.append(point)
        else:
            right_by_y.append(point)

    left_best = _closest_pair_recursive(left_by_x, left_by_y)
    right_best = _closest_pair_recursive(right_by_x, right_by_y)
    best = left_best if left_best[2] <= right_best[2] else right_best
    best_distance = best[2]

    # 只保留距离分割线足够近的点。用平方比较避免开方。
    strip = [
        point
        for point in points_by_y
        if (point[0] - split_x) * (point[0] - split_x) < best_distance
    ]

    for i, current in enumerate(strip):
        # 平面最近点对性质保证只需检查后续有限个 y 接近的点。
        for j in range(i + 1, min(i + 8, len(strip))):
            candidate = strip[j]
            distance = squared_distance(current, candidate)
            if distance < best_distance:
                best = (current, candidate, distance)
                best_distance = distance

    return best


def _brute_force_closest_pair(points: Sequence[Point]) -> tuple[Point, Point, float]:
    """
    对小规模点集使用暴力枚举，作为分治递归的基础情况。
    """
    best_pair: tuple[Point, Point] | None = None
    best_distance = float("inf")

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = squared_distance(points[i], points[j])
            if distance < best_distance:
                best_distance = distance
                best_pair = (points[i], points[j])

    if best_pair is None:
        raise ValueError("至少需要两个点才能计算最近点对")

    return best_pair[0], best_pair[1], best_distance


if __name__ == "__main__":
    pair = closest_pair([(0, 0), (5, 5), (1, 1)])
    assert pair[2] == 2

    duplicate_pair = closest_pair([(2, 3), (2, 3), (10, 10)])
    assert duplicate_pair[2] == 0

    mixed_points = [(-1, -1), (4, 4), (2, 2), (2.5, 2.5), (100, 100)]
    assert closest_pair(mixed_points)[2] == 0.5

    try:
        closest_pair([(0, 0)])
        raise AssertionError("单点输入必须抛出 ValueError")
    except ValueError:
        pass

    print("002_closest_pair_of_points: all examples passed")
