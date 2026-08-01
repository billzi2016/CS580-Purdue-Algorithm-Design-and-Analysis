"""
文件意图：手写实现 Miller-Rabin 概率素性测试。
适用场景：快速筛除大整数合数；对任意整数，有限底数集只能提供“可能为素数”的结论。
核心思想：将 n-1 写成 d*2^s，检查每个底数的幂序列是否给出合数见证。
输入输出：输入待测整数与可选底数列表，返回其是否通过所有测试。
时间复杂度：O(b log n * log n)，b 为底数个数。空间复杂度：O(1)。
关键边界：小于二的数不是素数；该教学版本不声称对任意大整数具有确定性。
"""


def _modular_power(base: int, exponent: int, modulus: int) -> int:
    """使用二进制快速幂计算 base**exponent mod modulus。"""
    result = 1
    base %= modulus
    while exponent:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result


def is_probable_prime(value: int, bases: tuple[int, ...] = (2, 3, 5, 7, 11)) -> bool:
    """判断 value 是否通过给定 bases 的 Miller-Rabin 测试。

    参数：value 为待测整数；bases 为测试底数元组。
    返回：合数一定返回 False；返回 True 表示对该底数集而言可能为素数。
    边界情况：小于二返回 False，小质数直接返回 True，偶数直接返回 False。
    关键算法点：非平凡平方根 1 会暴露合数，连续平方应最终到达 n-1 才能通过该底数。
    """
    if value < 2:
        return False
    small_primes = (2, 3, 5, 7, 11)
    if value in small_primes:
        return True
    if value % 2 == 0:
        return False
    odd_part = value - 1
    power_of_two = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        power_of_two += 1
    for base in bases:
        if base % value == 0:
            continue
        witness = _modular_power(base, odd_part, value)
        if witness == 1 or witness == value - 1:
            continue
        for _ in range(power_of_two - 1):
            witness = witness * witness % value
            if witness == value - 1:
                break
        else:
            return False
    return True


if __name__ == "__main__":
    assert not is_probable_prime(0)
    assert is_probable_prime(2) and is_probable_prime(97)
    assert not is_probable_prime(91)
    assert not is_probable_prime(561)
    assert is_probable_prime(1_000_000_007)
    print("008_miller_rabin: all examples passed")
