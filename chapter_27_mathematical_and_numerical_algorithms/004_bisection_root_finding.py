"""
二分求根。
"""


def bisection_root(function, left: float, right: float, steps: int) -> float:
    """假设 function(left) 与 function(right) 异号。"""

    if steps < 0:
        raise ValueError("steps 不能为负数")
    if function(left) * function(right) > 0:
        raise ValueError("区间端点必须异号")
    for _ in range(steps):
        middle = (left + right) / 2
        if function(left) * function(middle) <= 0:
            right = middle
        else:
            left = middle
    return (left + right) / 2


if __name__ == "__main__":
    root = bisection_root(lambda x_value: x_value**3 - 2.0, 1.0, 2.0, 20)
    assert round(root, 6) == 1.259921

    print("004_bisection_root_finding: all examples passed")
