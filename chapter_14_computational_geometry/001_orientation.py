"""
文件意图：手写实现平面三点方向判断。
适用场景：凸包、线段相交、点在多边形内和旋转卡壳等二维几何算法的基础谓词。
核心思想：二维叉积的符号表示从 AB 转到 AC 的旋转方向。
输入输出：输入三个整数坐标点，返回逆时针、顺时针或共线标志。
时间复杂度：O(1)。空间复杂度：O(1)。
关键边界：重复点与三点共线都返回 0；整数坐标避免浮点精度问题。
"""

Point = tuple[int, int]


def orientation(first: Point, second: Point, third: Point) -> int:
    """判断有向折线 first->second->third 的方向。

    参数：三个二维整数坐标点。
    返回：1 表示逆时针，-1 表示顺时针，0 表示共线。
    边界情况：重合点使叉积为零，按共线处理。
    关键算法点：只关心叉积符号，避免进行除法或角度计算。
    """
    cross_product = (second[0] - first[0]) * (third[1] - first[1]) - (
        second[1] - first[1]
    ) * (third[0] - first[0])
    if cross_product > 0:
        return 1
    if cross_product < 0:
        return -1
    return 0


if __name__ == "__main__":
    assert orientation((0, 0), (1, 0), (0, 1)) == 1
    assert orientation((0, 0), (0, 1), (1, 0)) == -1
    assert orientation((0, 0), (1, 1), (2, 2)) == 0
    assert orientation((1, 1), (1, 1), (2, 2)) == 0
    print("001_orientation: all examples passed")
