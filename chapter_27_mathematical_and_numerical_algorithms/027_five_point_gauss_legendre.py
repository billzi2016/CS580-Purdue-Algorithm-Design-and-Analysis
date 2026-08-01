"""
五点 Gauss-Legendre 积分：把 [-1, 1] 上的五点公式映射到任意区间。

意图：展示 Gaussian quadrature 如何选择节点和权重，使五个采样点能够精确积分
次数不超过 9 的多项式。输入是一元函数和积分区间，输出数值积分近似。

适用场景：被积函数在区间内足够光滑，且函数值计算成本高时适合用较少采样点
获得高精度。若区间左右端点相同，积分结果为 0。

时间复杂度：O(1)，单区间公式固定评估 5 次函数。
空间复杂度：O(1)。
"""

from math import sqrt


def gauss_legendre_five_point(function, left: float, right: float) -> float:
    """使用五点 Gauss-Legendre 公式近似积分。

    参数：
        function: 一元被积函数。
        left: 积分左端点。
        right: 积分右端点。

    返回：
        function 在 [left, right] 上的积分近似；若 left > right，结果自然为负。

    关键算法点：
        先在标准区间 [-1, 1] 上使用固定节点和权重，再通过线性变换映射到
        [left, right]。Jacobian 缩放因子是区间半长。
    """

    midpoint = (left + right) / 2
    half_length = (right - left) / 2
    if half_length == 0:
        return 0.0

    inner_node = sqrt(5 - 2 * sqrt(10 / 7)) / 3
    outer_node = sqrt(5 + 2 * sqrt(10 / 7)) / 3
    center_weight = 128 / 225
    inner_weight = (322 + 13 * sqrt(70)) / 900
    outer_weight = (322 - 13 * sqrt(70)) / 900

    total = center_weight * function(midpoint)
    for node, weight in (
        (inner_node, inner_weight),
        (-inner_node, inner_weight),
        (outer_node, outer_weight),
        (-outer_node, outer_weight),
    ):
        total += weight * function(midpoint + half_length * node)
    return half_length * total


if __name__ == "__main__":
    assert gauss_legendre_five_point(lambda _x: 7.0, -2.0, 3.0) == 35.0
    assert round(
        gauss_legendre_five_point(lambda x_value: x_value**2, 0.0, 1.0), 12
    ) == round(1 / 3, 12)
    assert (
        round(gauss_legendre_five_point(lambda x_value: x_value**9, -1.0, 1.0), 12)
        == 0.0
    )
    assert round(
        gauss_legendre_five_point(lambda x_value: x_value**8, -1.0, 1.0), 12
    ) == round(2 / 9, 12)
    assert gauss_legendre_five_point(lambda x_value: x_value * x_value, 2.0, 2.0) == 0.0

    print("027_five_point_gauss_legendre: all examples passed")
