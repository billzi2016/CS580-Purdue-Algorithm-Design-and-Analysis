"""
Simpson 积分。
"""


def simpson_rule(function, left: float, right: float, intervals: int) -> float:
    """复合 Simpson 公式，intervals 必须为偶数。"""

    if intervals <= 0 or intervals % 2 != 0:
        raise ValueError("intervals 必须是正偶数")
    step = (right - left) / intervals
    total = function(left) + function(right)
    for index in range(1, intervals):
        coefficient = 4 if index % 2 == 1 else 2
        total += coefficient * function(left + index * step)
    return total * step / 3


if __name__ == "__main__":
    value = simpson_rule(lambda x_value: x_value * x_value, 0.0, 1.0, 100)
    assert round(value, 6) == 0.333333

    print("008_simpson_rule: all examples passed")
