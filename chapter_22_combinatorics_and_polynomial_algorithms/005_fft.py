"""
文件意图：手写基于 Cooley-Tukey 迭代蝶形的复数快速傅里叶变换及多项式乘法。
适用场景：实系数多项式卷积、整数序列卷积和信号频域变换的教学实现。
核心思想：将偶、奇下标项递归分解为两个半规模 DFT，再用单位根旋转因子合并；实现采用位逆序迭代版本。
输入输出：输入复数系数列表或整数系数列表，输出变换值或精确的整数卷积结果。
时间复杂度：FFT 为 O(n log n)，补零后的多项式乘法为 O((n+m) log(n+m))；空间复杂度 O(n)。
关键边界情况：空多项式卷积为空；变换长度必须为二的幂；浮点舍入仅适合测试范围内的整数系数。
"""

import cmath
import math


def fft(values: list[complex], invert: bool = False) -> list[complex]:
    """计算长度为二的幂的离散傅里叶变换或其逆变换。

    参数：values 是复数输入；invert 为真时计算归一化后的逆 DFT。
    返回：与输入等长的频域或时域复数列表。
    边界情况：空输入返回空列表；非二次幂长度抛出 ValueError。
    关键算法点：位逆序使蝶形相邻块对应正确的子问题，逆变换只改变旋转方向并最终除以 n。
    """
    length = len(values)
    if length == 0:
        return []
    if length & (length - 1):
        raise ValueError("FFT 输入长度必须是二的幂")
    transformed = values.copy()
    _bit_reverse_permute(transformed)

    block_size = 2
    direction = 1 if invert else -1
    while block_size <= length:
        root = cmath.exp(direction * 2j * math.pi / block_size)
        half = block_size // 2
        for start in range(0, length, block_size):
            rotation = 1 + 0j
            for offset in range(half):
                even = transformed[start + offset]
                odd = transformed[start + offset + half] * rotation
                # 蝶形同时给出低频和高频部分，保持与递归合并相同的不变量。
                transformed[start + offset] = even + odd
                transformed[start + offset + half] = even - odd
                rotation *= root
        block_size *= 2
    if invert:
        return [value / length for value in transformed]
    return transformed


def convolution(left: list[int], right: list[int]) -> list[int]:
    """使用 FFT 计算两个整数系数多项式的卷积。

    参数：left 和 right 按升幂存储整数系数。
    返回：按升幂存储的整数卷积系数。
    边界情况：任一输入为空时返回空列表。
    关键算法点：频域逐点相乘对应时域卷积，逆变换后将微小浮点误差四舍五入。
    """
    if not left or not right:
        return []
    result_length = len(left) + len(right) - 1
    transform_length = 1
    while transform_length < result_length:
        transform_length *= 2
    left_values = [complex(value) for value in left] + [0j] * (
        transform_length - len(left)
    )
    right_values = [complex(value) for value in right] + [0j] * (
        transform_length - len(right)
    )
    left_spectrum = fft(left_values)
    right_spectrum = fft(right_values)
    product_spectrum = [
        first * second for first, second in zip(left_spectrum, right_spectrum)
    ]
    restored = fft(product_spectrum, invert=True)
    return [round(value.real) for value in restored[:result_length]]


def _bit_reverse_permute(values: list[complex]) -> None:
    """原地按二进制位反转下标重排，为迭代蝶形准备连续子问题。"""
    length = len(values)
    reversed_index = 0
    for index in range(1, length):
        bit = length >> 1
        while reversed_index & bit:
            reversed_index ^= bit
            bit >>= 1
        reversed_index ^= bit
        if index < reversed_index:
            values[index], values[reversed_index] = (
                values[reversed_index],
                values[index],
            )


if __name__ == "__main__":
    assert convolution([1, 2, 3], [4, 5]) == [4, 13, 22, 15]
    assert convolution([0], [7, -2]) == [0, 0]
    assert convolution([], [1]) == []
    original = [complex(1), complex(-2), complex(3), complex(0)]
    restored = fft(fft(original), invert=True)
    assert all(abs(first - second) < 1e-9 for first, second in zip(original, restored))
    try:
        fft([1 + 0j, 2 + 0j, 3 + 0j])
        raise AssertionError("非二次幂长度应抛出 ValueError")
    except ValueError:
        pass
    print("005_fft: all examples passed")
