"""
文件意图：手写实现模快速幂。
适用场景：模算术、密码学教学、组合数和大整数指数计算。
核心思想：将指数分解为二进制位，按位累积底数的平方贡献。
输入输出：输入底数、非负指数和正模数，输出幂的模值。
时间复杂度：O(log exponent)。空间复杂度：O(1)。
关键边界：指数零返回 1 mod modulus；负指数与非正模数会被拒绝。
"""


def modular_power(base: int, exponent: int, modulus: int) -> int:
    """计算 base 的 exponent 次幂模 modulus。

    参数：base 为整数，exponent 为非负整数，modulus 为正整数。
    返回：范围在 [0, modulus) 的结果。
    边界情况：exponent 为零时返回 1 % modulus。
    关键算法点：每轮右移指数，底数平方对应处理下一二进制位。
    """
    if exponent < 0:
        raise ValueError("exponent 必须是非负整数")
    if modulus <= 0:
        raise ValueError("modulus 必须是正整数")
    result = 1 % modulus
    current = base % modulus
    while exponent > 0:
        if exponent & 1:
            result = result * current % modulus
        current = current * current % modulus
        exponent >>= 1
    return result


if __name__ == "__main__":
    assert modular_power(2, 10, 1000) == 24
    assert modular_power(-2, 3, 5) == 2
    assert modular_power(7, 0, 13) == 1
    try:
        modular_power(2, -1, 5)
        assert False, "负指数应被拒绝"
    except ValueError as error:
        assert "非负" in str(error)
    print("003_modular_exponentiation: all examples passed")
