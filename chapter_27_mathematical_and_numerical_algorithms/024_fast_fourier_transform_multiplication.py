"""
FFT 乘法：用复数快速傅里叶变换做多项式卷积。
"""

from cmath import exp, pi


def fft(values: list[complex], invert: bool) -> list[complex]:
    """递归 Cooley-Tukey FFT。"""

    n_value = len(values)
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
    """返回两多项式系数卷积。"""

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

    print("024_fast_fourier_transform_multiplication: all examples passed")
