"""
文件意图：
    本文件手写实现 Karatsuba 大整数乘法，用于演示分治降低乘法次数的思想。

适用场景：
    需要理解大整数乘法如何从四次子乘法优化为三次子乘法。

核心思想：
    将 x 和 y 分成高位与低位：
        x = high_x * base + low_x
        y = high_y * base + low_y
    普通分治需要四次乘法；Karatsuba 使用 z1 - z2 - z0 得到交叉项，
    只需要三次递归乘法。

输入输出：
    输入两个整数，返回它们的乘积。

时间复杂度：
    O(n^log2(3))，约 O(n^1.585)

空间复杂度：
    O(log n) 递归栈，不计大整数临时对象。
"""


def karatsuba_multiply(x: int, y: int) -> int:
    """
    使用 Karatsuba 算法计算 x * y。

    参数：
        x: 整数，可以为负数。
        y: 整数，可以为负数。

    返回：
        x 与 y 的乘积。
    """
    sign = -1 if (x < 0) ^ (y < 0) else 1
    product = _karatsuba_non_negative(abs(x), abs(y))
    return sign * product


def _karatsuba_non_negative(x: int, y: int) -> int:
    """
    对非负整数执行 Karatsuba 递归。
    """
    if x < 10 or y < 10:
        return x * y

    digits = max(_decimal_digits(x), _decimal_digits(y))
    half = digits // 2
    base = 10**half

    high_x, low_x = divmod(x, base)
    high_y, low_y = divmod(y, base)

    z0 = _karatsuba_non_negative(low_x, low_y)
    z2 = _karatsuba_non_negative(high_x, high_y)
    z1 = _karatsuba_non_negative(low_x + high_x, low_y + high_y)

    # 交叉项等于 high_x * low_y + low_x * high_y。
    cross = z1 - z2 - z0
    return z2 * base * base + cross * base + z0


def _decimal_digits(value: int) -> int:
    """
    返回非负整数的十进制位数。
    """
    if value == 0:
        return 1

    digits = 0
    current = value
    while current > 0:
        digits += 1
        current //= 10
    return digits


if __name__ == "__main__":
    assert karatsuba_multiply(0, 12345) == 0
    assert karatsuba_multiply(9, 8) == 72
    assert karatsuba_multiply(1234, 5678) == 1234 * 5678
    assert karatsuba_multiply(-1234, 5678) == -1234 * 5678
    assert karatsuba_multiply(123456789, 987654321) == 123456789 * 987654321

    print("003_karatsuba_multiplication: all examples passed")
