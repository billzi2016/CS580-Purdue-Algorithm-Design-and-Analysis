"""
文件意图：手写 Number Theoretic Transform（NTT）及模素数多项式卷积。
适用场景：需要避免 FFT 浮点误差的整数卷积、组合数模运算和竞赛多项式计算。
核心思想：在 998244353 这一支持二次幂单位根的素数域中，使用原根 3 做迭代 Cooley-Tukey 蝶形。
输入输出：输入非负或任意整数系数列表，输出模 998244353 的卷积系数。
时间复杂度：NTT 与卷积均为 O(n log n)；空间复杂度 O(n)。
关键边界情况：空多项式返回空；变换长度必须为二的幂且不能超过该模数支持的最大二次幂长度。
"""


MODULUS = 998_244_353
PRIMITIVE_ROOT = 3


def ntt(values: list[int], invert: bool = False) -> list[int]:
    """计算模 MODULUS 的数论变换或归一化逆变换。

    参数：values 是整数域元素；invert 为真时计算逆 NTT。
    返回：模 MODULUS 归一化后的等长结果。
    边界情况：空输入返回空，非二次幂长度或过长长度抛出 ValueError。
    关键算法点：每层单位根为 g^((p-1)/len)，逆变换使用其乘法逆元并最终乘 n 的逆元。
    """
    length = len(values)
    if length == 0:
        return []
    if length & (length - 1) or (MODULUS - 1) % length:
        raise ValueError("NTT 长度必须是 MODULUS-1 的二次幂因子")
    transformed = [value % MODULUS for value in values]
    _bit_reverse_permute(transformed)
    block_size = 2
    while block_size <= length:
        root = pow(PRIMITIVE_ROOT, (MODULUS - 1) // block_size, MODULUS)
        if invert:
            root = pow(root, MODULUS - 2, MODULUS)
        half = block_size // 2
        for start in range(0, length, block_size):
            rotation = 1
            for offset in range(half):
                lower = transformed[start + offset]
                upper = transformed[start + offset + half] * rotation % MODULUS
                transformed[start + offset] = (lower + upper) % MODULUS
                transformed[start + offset + half] = (lower - upper) % MODULUS
                rotation = rotation * root % MODULUS
        block_size *= 2
    if invert:
        inverse_length = pow(length, MODULUS - 2, MODULUS)
        transformed = [value * inverse_length % MODULUS for value in transformed]
    return transformed


def convolution_mod(left: list[int], right: list[int]) -> list[int]:
    """在模 MODULUS 下计算两个整数系数多项式卷积。

    参数：left/right 是按升幂存储的整数系数。
    返回：长度为 len(left)+len(right)-1 的模 MODULUS 系数列表。
    边界情况：任一多项式为空时返回空。
    关键算法点：对补零后的两个序列 NTT，逐点乘法，再逆 NTT 恢复 Cauchy 乘积。
    """
    if not left or not right:
        return []
    result_length = len(left) + len(right) - 1
    transform_length = 1
    while transform_length < result_length:
        transform_length *= 2
    left_values = left + [0] * (transform_length - len(left))
    right_values = right + [0] * (transform_length - len(right))
    left_spectrum = ntt(left_values)
    right_spectrum = ntt(right_values)
    product_spectrum = [first * second % MODULUS for first, second in zip(left_spectrum, right_spectrum)]
    return ntt(product_spectrum, invert=True)[:result_length]


def _bit_reverse_permute(values: list[int]) -> None:
    """原地二进制位逆序排列，使迭代蝶形与递归子问题的顺序一致。"""
    length = len(values)
    reversed_index = 0
    for index in range(1, length):
        bit = length >> 1
        while reversed_index & bit:
            reversed_index ^= bit
            bit >>= 1
        reversed_index ^= bit
        if index < reversed_index:
            values[index], values[reversed_index] = values[reversed_index], values[index]


if __name__ == "__main__":
    assert convolution_mod([1, 2, 3], [4, 5]) == [4, 13, 22, 15]
    assert convolution_mod([MODULUS - 1], [2]) == [MODULUS - 2]
    assert convolution_mod([], [1]) == []
    original = [1, 7, MODULUS - 2, 0]
    assert ntt(ntt(original), invert=True) == original
    try:
        ntt([1, 2, 3])
        raise AssertionError("非二次幂长度应抛出 ValueError")
    except ValueError:
        pass
    print("006_ntt: all examples passed")
