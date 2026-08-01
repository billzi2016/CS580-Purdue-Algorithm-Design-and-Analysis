"""
文件意图：手写实现基于扩展欧几里得算法的模逆元。
适用场景：模除法、中国剩余定理和线性同余求解。
核心思想：当 gcd(a, m)=1 时，贝祖等式中的 a 系数即为 a 在模 m 下的逆元。
输入输出：输入整数 a 与正模数 m，输出范围 [0, m) 内的逆元。
时间复杂度：O(log m)。空间复杂度：O(1)。
关键边界：模数必须大于一；不存在逆元时抛出 ValueError。
"""


def _extended_gcd(first: int, second: int) -> tuple[int, int, int]:
    """返回 first*x + second*y = gcd(first, second) 的一组系数。"""
    old_remainder, remainder = first, second
    old_x, x = 1, 0
    old_y, y = 0, 1
    while remainder:
        quotient = old_remainder // remainder
        old_remainder, remainder = remainder, old_remainder - quotient * remainder
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    return old_remainder, old_x, old_y


def modular_inverse(value: int, modulus: int) -> int:
    """计算 value 在模 modulus 意义下的乘法逆元。

    参数：value 为整数，modulus 为大于一的正整数。
    返回：满足 value * result ≡ 1 (mod modulus) 的最小非负 result。
    边界情况：不互素时没有逆元并抛出 ValueError。
    关键算法点：扩展 gcd 给出的 value 系数在模 modulus 下就是候选逆元。
    """
    if modulus <= 1:
        raise ValueError("modulus 必须大于 1")
    divisor, coefficient, _ = _extended_gcd(value, modulus)
    if divisor != 1:
        raise ValueError("value 与 modulus 不互素，不存在模逆元")
    return coefficient % modulus


if __name__ == "__main__":
    assert modular_inverse(3, 11) == 4
    assert modular_inverse(-3, 11) == 7
    assert modular_inverse(1, 2) == 1
    try:
        modular_inverse(6, 9)
        assert False, "不互素时应拒绝"
    except ValueError as error:
        assert "不互素" in str(error)
    print("004_modular_inverse: all examples passed")
