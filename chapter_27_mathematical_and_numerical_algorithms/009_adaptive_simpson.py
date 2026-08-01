"""
自适应 Simpson 积分。
"""


def simpson_segment(function, left: float, right: float) -> float:
    middle = (left + right) / 2
    return (right - left) * (function(left) + 4 * function(middle) + function(right)) / 6


def adaptive_simpson(function, left: float, right: float, tolerance: float, depth: int = 20) -> float:
    """递归自适应 Simpson。"""

    if tolerance <= 0 or depth < 0:
        raise ValueError("参数范围非法")
    whole = simpson_segment(function, left, right)
    return _adaptive(function, left, right, tolerance, whole, depth)


def _adaptive(function, left: float, right: float, tolerance: float, whole: float, depth: int) -> float:
    middle = (left + right) / 2
    left_part = simpson_segment(function, left, middle)
    right_part = simpson_segment(function, middle, right)
    if depth == 0 or abs(left_part + right_part - whole) < 15 * tolerance:
        return left_part + right_part + (left_part + right_part - whole) / 15
    return _adaptive(function, left, middle, tolerance / 2, left_part, depth - 1) + _adaptive(
        function, middle, right, tolerance / 2, right_part, depth - 1
    )


if __name__ == "__main__":
    value = adaptive_simpson(lambda x_value: x_value**4, 0.0, 1.0, 1e-8)
    assert round(value, 6) == 0.2

    print("009_adaptive_simpson: all examples passed")
