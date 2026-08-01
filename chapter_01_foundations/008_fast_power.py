"""
文件意图：
    本文件手写实现快速幂和模快速幂，用于高效计算大指数幂。

适用场景：
    需要计算 base ** exponent，或在模意义下计算 base ** exponent mod modulus。

核心思想：
    将指数按二进制拆解。每次如果当前最低位是 1，就把当前底数贡献进答案；
    然后底数平方，指数右移一位。

时间复杂度：
    O(log exponent)

空间复杂度：
    O(1)
"""


def fast_power(base: float, exponent: int) -> float:
    """
    计算 base 的 exponent 次幂。

    参数：
        base: 底数。
        exponent: 整数指数，可以为负数。

    返回：
        base ** exponent 的结果。
    """
    if exponent == 0:
        return 1.0

    if exponent < 0:
        if base == 0:
            raise ZeroDivisionError("0 不能计算负指数幂")
        return 1.0 / fast_power(base, -exponent)

    result = 1.0
    current = base
    power = exponent

    while power > 0:
        if power & 1:
            result *= current
        current *= current
        power >>= 1

    return result


def modular_power(base: int, exponent: int, modulus: int) -> int:
    """
    计算 base ** exponent mod modulus。

    参数：
        base: 整数底数。
        exponent: 非负整数指数。
        modulus: 正整数模数。

    返回：
        模意义下的快速幂结果。
    """
    if exponent < 0:
        raise ValueError("模快速幂的 exponent 必须是非负整数")
    if modulus <= 0:
        raise ValueError("modulus 必须是正整数")

    result = 1 % modulus
    current = base % modulus
    power = exponent

    while power > 0:
        if power & 1:
            result = (result * current) % modulus
        current = (current * current) % modulus
        power >>= 1

    return result


if __name__ == "__main__":
    assert fast_power(2, 10) == 1024.0
    assert fast_power(2, -2) == 0.25
    assert fast_power(5, 0) == 1.0
    assert modular_power(2, 10, 1000) == 24
    assert modular_power(7, 0, 13) == 1

    print("008_fast_power: all examples passed")
