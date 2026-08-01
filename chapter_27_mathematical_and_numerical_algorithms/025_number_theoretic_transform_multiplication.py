"""
NTT 乘法：在模域内用原根实现快速卷积。
"""


MOD = 998244353
ROOT = 3


def ntt(values: list[int], invert: bool) -> list[int]:
    """迭代位逆序 NTT。"""

    n_value = len(values)
    result = values[:]
    j_value = 0
    for i_value in range(1, n_value):
        bit = n_value >> 1
        while j_value & bit:
            j_value ^= bit
            bit >>= 1
        j_value ^= bit
        if i_value < j_value:
            result[i_value], result[j_value] = result[j_value], result[i_value]
    length = 2
    while length <= n_value:
        wlen = pow(ROOT, (MOD - 1) // length, MOD)
        if invert:
            wlen = pow(wlen, MOD - 2, MOD)
        for start in range(0, n_value, length):
            w_value = 1
            for offset in range(length // 2):
                u_value = result[start + offset]
                v_value = result[start + offset + length // 2] * w_value % MOD
                result[start + offset] = (u_value + v_value) % MOD
                result[start + offset + length // 2] = (u_value - v_value) % MOD
                w_value = w_value * wlen % MOD
        length *= 2
    if invert:
        inv_n = pow(n_value, MOD - 2, MOD)
        result = [value * inv_n % MOD for value in result]
    return result


def multiply_polynomials_ntt(left: list[int], right: list[int]) -> list[int]:
    """用 NTT 做模卷积。"""

    size = 1
    while size < len(left) + len(right) - 1:
        size *= 2
    fa = left[:] + [0] * (size - len(left))
    fb = right[:] + [0] * (size - len(right))
    transform_a = ntt(fa, False)
    transform_b = ntt(fb, False)
    transform_c = [transform_a[i] * transform_b[i] % MOD for i in range(size)]
    result = ntt(transform_c, True)
    return result[: len(left) + len(right) - 1]


if __name__ == "__main__":
    assert multiply_polynomials_ntt([1, 2, 3], [4, 5]) == [4, 13, 22, 15]

    print("025_number_theoretic_transform_multiplication: all examples passed")
