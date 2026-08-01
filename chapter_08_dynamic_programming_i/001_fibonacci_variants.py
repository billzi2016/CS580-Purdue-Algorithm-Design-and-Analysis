"""
文件意图：
    本文件手写实现 Fibonacci 数列的多种计算方式，用于对比递归、记忆化、循环 DP、
    滚动变量、矩阵快速幂和 fast doubling。

适用场景：
    入门动态规划、递归优化、状态转移和分治加速示例。

核心思想：
    Fibonacci 满足 F(n)=F(n-1)+F(n-2)。不同实现方式的差别在于是否重复计算、
    是否保存状态、以及是否利用矩阵或倍增公式加速。

时间复杂度：
    朴素递归 O(2^n)，记忆化/循环/滚动 O(n)，矩阵快速幂/fast doubling O(log n)。

空间复杂度：
    视实现方式从 O(1) 到 O(n) 不等。
"""


def fibonacci_recursive(n: int) -> int:
    """朴素递归计算 Fibonacci，仅适合小 n，用于展示重复子问题。"""
    _validate_non_negative(n)
    if n <= 1:
        return n
    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_memoized(n: int) -> int:
    """使用记忆化递归避免重复计算。"""
    _validate_non_negative(n)
    memo = {0: 0, 1: 1}

    def solve(index: int) -> int:
        if index not in memo:
            memo[index] = solve(index - 1) + solve(index - 2)
        return memo[index]

    return solve(n)


def fibonacci_loop_dp(n: int) -> int:
    """使用 DP 数组自底向上计算 Fibonacci。"""
    _validate_non_negative(n)
    if n <= 1:
        return n
    dp = [0] * (n + 1)
    dp[1] = 1
    for index in range(2, n + 1):
        dp[index] = dp[index - 1] + dp[index - 2]
    return dp[n]


def fibonacci_rolling(n: int) -> int:
    """使用两个变量滚动保存最近两个状态。"""
    _validate_non_negative(n)
    previous, current = 0, 1
    for _ in range(n):
        previous, current = current, previous + current
    return previous


def fibonacci_matrix(n: int) -> int:
    """使用矩阵快速幂计算 Fibonacci。"""
    _validate_non_negative(n)
    if n == 0:
        return 0
    matrix = ((1, 1), (1, 0))
    powered = _matrix_power_2x2(matrix, n - 1)
    return powered[0][0]


def fibonacci_fast_doubling(n: int) -> int:
    """使用 fast doubling 公式计算 Fibonacci。"""
    _validate_non_negative(n)
    return _fib_pair(n)[0]


def _fib_pair(n: int) -> tuple[int, int]:
    """返回 (F(n), F(n+1))。"""
    if n == 0:
        return 0, 1
    a, b = _fib_pair(n // 2)
    c = a * (2 * b - a)
    d = a * a + b * b
    if n % 2 == 0:
        return c, d
    return d, c + d


def _matrix_power_2x2(
    matrix: tuple[tuple[int, int], tuple[int, int]], exponent: int
) -> tuple[tuple[int, int], tuple[int, int]]:
    """手写 2x2 矩阵快速幂。"""
    result = ((1, 0), (0, 1))
    current = matrix
    power = exponent
    while power > 0:
        if power & 1:
            result = _multiply_2x2(result, current)
        current = _multiply_2x2(current, current)
        power >>= 1
    return result


def _multiply_2x2(
    left: tuple[tuple[int, int], tuple[int, int]],
    right: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    """手写 2x2 矩阵乘法。"""
    return (
        (
            left[0][0] * right[0][0] + left[0][1] * right[1][0],
            left[0][0] * right[0][1] + left[0][1] * right[1][1],
        ),
        (
            left[1][0] * right[0][0] + left[1][1] * right[1][0],
            left[1][0] * right[0][1] + left[1][1] * right[1][1],
        ),
    )


def _validate_non_negative(n: int) -> None:
    if n < 0:
        raise ValueError("n 必须非负")


if __name__ == "__main__":
    expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    for index, value in enumerate(expected):
        assert fibonacci_recursive(index) == value
        assert fibonacci_memoized(index) == value
        assert fibonacci_loop_dp(index) == value
        assert fibonacci_rolling(index) == value
        assert fibonacci_matrix(index) == value
        assert fibonacci_fast_doubling(index) == value
    assert fibonacci_fast_doubling(50) == 12586269025

    print("001_fibonacci_variants: all examples passed")
