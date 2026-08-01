"""
文件意图：
    本文件实现 Master Theorem 的教学分类器，用于判断常见分治递归式的渐进复杂度。

适用场景：
    递归式形如 T(n) = aT(n / b) + f(n)，且 f(n) 可写成 Theta(n^k log^p n)。

核心思想：
    比较 f(n) 中的 n^k 与临界项 n^log_b(a)：
        k < log_b(a)：子问题主导；
        k = log_b(a)：平衡情况；
        k > log_b(a)：合并代价主导。

输入输出：
    输入 a、b、k、log_power，返回 Master Theorem 分类和复杂度描述。

时间复杂度：
    O(1)

空间复杂度：
    O(1)
"""

import math


def classify_master_theorem(a: int, b: int, k: float, log_power: float = 0.0) -> tuple[str, str]:
    """
    分类 T(n) = aT(n / b) + Theta(n^k log^p n)。

    参数：
        a: 子问题数量，必须大于等于 1。
        b: 子问题规模缩小倍数，必须大于 1。
        k: 合并代价中 n 的指数。
        log_power: 合并代价中 log n 的指数 p。

    返回：
        (case_name, complexity_description)。
    """
    if a < 1:
        raise ValueError("a 必须大于等于 1")
    if b <= 1:
        raise ValueError("b 必须大于 1")

    critical_exponent = math.log(a, b)
    epsilon = 1e-9

    if k < critical_exponent - epsilon:
        return "case 1", f"Theta(n^{_format_number(critical_exponent)})"

    if abs(k - critical_exponent) <= epsilon:
        return "case 2", _balanced_case_complexity(k, log_power)

    return "case 3", f"Theta(n^{_format_number(k)} log^{_format_number(log_power)} n)"


def _balanced_case_complexity(k: float, log_power: float) -> str:
    """
    处理 k = log_b(a) 的平衡情况。

    关键点：
        若 f(n) = Theta(n^k log^p n)，平衡情况下通常增加一个 log 因子，
        得到 Theta(n^k log^(p + 1) n)。
    """
    next_log_power = log_power + 1
    if abs(next_log_power) < 1e-9:
        return f"Theta(n^{_format_number(k)})"
    return f"Theta(n^{_format_number(k)} log^{_format_number(next_log_power)} n)"


def _format_number(value: float) -> str:
    """
    格式化指数，避免整数显示为 2.0。
    """
    rounded = round(value)
    if abs(value - rounded) < 1e-9:
        return str(rounded)
    return f"{value:.6g}"


if __name__ == "__main__":
    assert classify_master_theorem(2, 2, 0) == ("case 1", "Theta(n^1)")
    assert classify_master_theorem(2, 2, 1) == ("case 2", "Theta(n^1 log^1 n)")
    assert classify_master_theorem(2, 2, 2) == ("case 3", "Theta(n^2 log^0 n)")
    assert classify_master_theorem(4, 2, 2, 1) == ("case 2", "Theta(n^2 log^2 n)")
    assert classify_master_theorem(1, 2, 0) == ("case 2", "Theta(n^0 log^1 n)")

    try:
        classify_master_theorem(0, 2, 1)
        raise AssertionError("非法 a 必须抛出 ValueError")
    except ValueError:
        pass

    print("005_master_theorem_examples: all examples passed")
