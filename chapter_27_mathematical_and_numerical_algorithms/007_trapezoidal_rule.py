"""
梯形积分。
"""


def trapezoidal_rule(function, left: float, right: float, intervals: int) -> float:
    """复合梯形公式。"""

    if intervals <= 0:
        raise ValueError("intervals 必须为正数")
    step = (right - left) / intervals
    total = 0.5 * (function(left) + function(right))
    for index in range(1, intervals):
        total += function(left + index * step)
    return total * step


if __name__ == "__main__":
    value = trapezoidal_rule(lambda x_value: x_value * x_value, 0.0, 1.0, 1000)
    assert round(value, 4) == 0.3333

    print("007_trapezoidal_rule: all examples passed")
