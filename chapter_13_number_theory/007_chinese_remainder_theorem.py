"""
文件意图：手写实现可处理非互素模数的广义中国剩余定理。
适用场景：合并多个线性同余约束，包含模数之间不互素的情况。
核心思想：逐个合并 x≡a(mod m) 与 x≡b(mod n)，先检查差值是否可被 gcd(m,n) 整除。
输入输出：输入 (余数, 正模数) 列表，返回最小非负解及其合并模数，或 None。
时间复杂度：O(k log M)，M 为中间模数规模。空间复杂度：O(1)。
关键边界：空约束返回 (0,1)；不相容同余返回 None；模数必须为正。
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


def chinese_remainder(congruences: list[tuple[int, int]]) -> tuple[int, int] | None:
    """合并同余约束并返回 (最小非负解, 最小正合并模数)。

    参数：congruences 的元素为 (remainder, modulus)，modulus 必须为正。
    返回：存在公共解时返回规范化解与 lcm 模数，否则返回 None。
    边界情况：空列表返回 (0, 1)，非正模数抛出 ValueError。
    关键算法点：只有余数差可被两模数 gcd 整除时，两式才相容。
    """
    residue, modulus = 0, 1
    for next_residue, next_modulus in congruences:
        if next_modulus <= 0:
            raise ValueError("所有模数必须为正整数")
        next_residue %= next_modulus
        divisor, coefficient, _ = _extended_gcd(modulus, next_modulus)
        difference = next_residue - residue
        if difference % divisor != 0:
            return None
        reduced_modulus = next_modulus // divisor
        multiplier = (difference // divisor * coefficient) % reduced_modulus
        combined_modulus = modulus * reduced_modulus
        residue = (residue + modulus * multiplier) % combined_modulus
        modulus = combined_modulus
    return residue, modulus


if __name__ == "__main__":
    assert chinese_remainder([]) == (0, 1)
    assert chinese_remainder([(2, 3), (3, 5), (2, 7)]) == (23, 105)
    assert chinese_remainder([(1, 4), (3, 6)]) == (9, 12)
    assert chinese_remainder([(1, 2), (0, 4)]) is None
    print("007_chinese_remainder_theorem: all examples passed")
