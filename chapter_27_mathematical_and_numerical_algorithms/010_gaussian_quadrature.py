"""
Gaussian quadrature 基础：这里实现二点 Gauss-Legendre。
"""

from math import sqrt


def gauss_legendre_two_point(function, left: float, right: float) -> float:
    """把 [-1,1] 上的二点公式映射到 [left,right]。"""

    midpoint = (left + right) / 2
    half_length = (right - left) / 2
    offset = 1 / sqrt(3)
    return half_length * (
        function(midpoint - half_length * offset)
        + function(midpoint + half_length * offset)
    )


if __name__ == "__main__":
    value = gauss_legendre_two_point(lambda x_value: x_value**3 + x_value, -1.0, 1.0)
    assert round(value, 6) == 0.0
    quad = gauss_legendre_two_point(lambda x_value: x_value * x_value, 0.0, 1.0)
    assert round(quad, 6) == 0.333333

    print("010_gaussian_quadrature: all examples passed")
