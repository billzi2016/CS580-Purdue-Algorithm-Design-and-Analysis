"""
文件意图：手写实现鞋带公式计算简单多边形的有向面积与绝对面积。
适用场景：计算顶点按边界顺序给出的二维简单多边形面积。
核心思想：累加每条边端点坐标构成的叉积，闭合边由最后点连回首点。
输入输出：输入整数坐标顶点列表，输出两倍有向面积或非负面积。
时间复杂度：O(n)。空间复杂度：O(1)。
关键边界：少于三个点面积为零；输入必须是按边界顺序给出的简单多边形。
"""

Point = tuple[int, int]


def signed_double_area(polygon: list[Point]) -> int:
    """返回 polygon 的两倍有向面积。

    参数：polygon 是按顺时针或逆时针边界顺序给出的顶点列表。
    返回：逆时针为正、顺时针为负的两倍面积。
    边界情况：少于三个顶点返回零。
    关键算法点：每条边贡献 x_i*y_next - y_i*x_next，最后一条边闭合到首点。
    """
    total = 0
    for index, point in enumerate(polygon):
        next_point = polygon[(index + 1) % len(polygon)] if polygon else point
        total += point[0] * next_point[1] - point[1] * next_point[0]
    return total


def polygon_area(polygon: list[Point]) -> float:
    """返回简单多边形的非负面积。

    参数：polygon 是按边界顺序给出的整数坐标顶点列表。
    返回：非负浮点面积。
    边界情况：空、多于零但少于三个顶点均返回 0.0。
    关键算法点：有向面积绝对值消除顶点方向对几何面积的影响。
    """
    return abs(signed_double_area(polygon)) / 2.0


if __name__ == "__main__":
    assert signed_double_area([(0, 0), (2, 0), (0, 2)]) == 4
    assert polygon_area([(0, 0), (4, 0), (4, 3), (0, 3)]) == 12.0
    assert polygon_area([(0, 0), (0, 3), (4, 3), (4, 0)]) == 12.0
    assert polygon_area([]) == 0.0
    print("003_polygon_area: all examples passed")
