"""
FFT 乘法：用复数快速傅里叶变换做多项式卷积。

意图：展示递归 Cooley-Tukey FFT 如何把多项式卷积从 O(n^2) 降到
O(n log n)。输入是整数系数列表，输出是卷积后的整数系数列表。

适用范围：本教学版 FFT 只接受非空、长度为 2 的幂的序列；多项式乘法会
自动补零到合适长度。空多项式按零多项式处理并返回空列表。

时间复杂度：FFT 为 O(n log n)，卷积总复杂度 O(n log n)。
空间复杂度：递归拆分和结果数组需要 O(n log n) 临时空间。
"""

from cmath import exp, pi


def fft(values: list[complex], invert: bool) -> list[complex]:
    """递归 Cooley-Tukey FFT。

    参数：values 是长度为 2 的幂的复数序列；invert 为 True 时执行逆变换。
    返回值：与输入等长的频域或时域系数。
    边界情况：空序列和非 2 的幂长度会破坏偶奇拆分，必须显式拒绝。
    """

    n_value = len(values)
    if n_value == 0 or n_value & (n_value - 1):
        raise ValueError("FFT 输入长度必须是非空的 2 的幂")
    if n_value == 1:
        return values[:]
    even = fft(values[0::2], invert)
    odd = fft(values[1::2], invert)
    angle = 2 * pi / n_value * (-1 if not invert else 1)
    root = 1 + 0j
    root_step = exp(1j * angle)
    result = [0j] * n_value
    for index in range(n_value // 2):
        temp = root * odd[index]
        result[index] = even[index] + temp
        result[index + n_value // 2] = even[index] - temp
        root *= root_step
    if invert:
        return [value / 2 for value in result]
    return result


def multiply_polynomials(left: list[int], right: list[int]) -> list[int]:
    """返回两多项式系数卷积。

    参数：left 和 right 是从低次到高次排列的整数系数。
    返回值：卷积后的整数系数；若任一输入为空，视为零多项式并返回 []。
    关键算法点：先补零到 2 的幂，频域逐点相乘，再逆 FFT 回到系数域。
    """

    if not left or not right:
        return []
    size = 1
    while size < len(left) + len(right) - 1:
        size *= 2
    fa = [complex(value, 0.0) for value in left] + [0j] * (size - len(left))
    fb = [complex(value, 0.0) for value in right] + [0j] * (size - len(right))
    fft_a = fft(fa, False)
    fft_b = fft(fb, False)
    fft_c = [fft_a[i] * fft_b[i] for i in range(size)]
    result = fft(fft_c, True)
    return [round(result[i].real) for i in range(len(left) + len(right) - 1)]


if __name__ == "__main__":
    assert multiply_polynomials([1, 2, 3], [4, 5]) == [4, 13, 22, 15]
    assert multiply_polynomials([], [1, 2, 3]) == []
    assert multiply_polynomials([7], [6]) == [42]
    assert multiply_polynomials([1, 0, 1], [1, 0, 1]) == [1, 0, 2, 0, 1]
    try:
        fft([1 + 0j, 2 + 0j, 3 + 0j], False)
        raise AssertionError("非 2 的幂长度应触发异常")
    except ValueError:
        pass

    print("024_fast_fourier_transform_multiplication: all examples passed")
