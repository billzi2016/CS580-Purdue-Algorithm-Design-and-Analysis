"""
文件意图：手写实现旋转卡壳计算凸多边形直径的平方。
适用场景：已获得逆时针凸包后，在线性时间寻找最远顶点对。
核心思想：对每条边维护使平行四边形面积最大的对踵顶点，指针只沿多边形前进。
输入输出：输入逆时针凸多边形顶点，返回最大欧氏距离平方。
时间复杂度：O(n)。空间复杂度：O(1)。
关键边界：空或单点返回 0；输入必须是无重复顶点、按逆时针顺序给出的凸多边形。
"""

Point = tuple[int, int]


def _distance_squared(first: Point, second: Point) -> int:
    """返回两点欧氏距离的平方，避免不必要的浮点开方。"""
    return (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2


def _double_area(first: Point, second: Point, third: Point) -> int:
    """返回三角形 first-second-third 的两倍绝对面积。"""
    return abs(
        (second[0] - first[0]) * (third[1] - first[1])
        - (second[1] - first[1]) * (third[0] - first[0])
    )


def convex_diameter_squared(polygon: list[Point]) -> int:
    """返回逆时针凸多边形 polygon 的直径平方。

    参数：polygon 为无重复顶点的逆时针凸多边形；允许少于三个顶点。
    返回：任意两顶点间最大的欧氏距离平方。
    边界情况：空和单点为零，两点直接返回其距离平方。
    关键算法点：对踵指针 j 只在三角形面积增大时前进，总前进次数为线性级别。
    """
    count = len(polygon)
    if count <= 1:
        return 0
    if count == 2:
        return _distance_squared(polygon[0], polygon[1])
    farthest = 1
    best = 0
    for index in range(count):
        next_index = (index + 1) % count
        while _double_area(
            polygon[index], polygon[next_index], polygon[(farthest + 1) % count]
        ) > _double_area(polygon[index], polygon[next_index], polygon[farthest]):
            farthest = (farthest + 1) % count
        best = max(
            best,
            _distance_squared(polygon[index], polygon[farthest]),
            _distance_squared(polygon[next_index], polygon[farthest]),
        )
    return best


if __name__ == "__main__":
    assert convex_diameter_squared([]) == 0
    assert convex_diameter_squared([(1, 1)]) == 0
    assert convex_diameter_squared([(0, 0), (3, 4)]) == 25
    assert convex_diameter_squared([(0, 0), (2, 0), (2, 2), (0, 2)]) == 8
    assert convex_diameter_squared([(0, 0), (4, 0), (5, 2), (2, 5), (-1, 3)]) == 37
    print("005_rotating_calipers: all examples passed")
