"""RSA 教学密钥构造。

本文件从调用方显式提供的两个不同小素数构造 (n,e) 与 (n,d)。它不生成安全随机素数、
不做大整数素性检验或 CRT 优化，绝不能用于生产。时间复杂度由试除法和扩展欧几里得决定。
"""


def _gcd(left: int, right: int) -> int:
    """用 Euclid 算法求最大公约数。"""
    while right:
        left, right = right, left % right
    return abs(left)


def _inverse(value: int, modulus: int) -> int:
    """用扩展欧几里得求 value 在 modulus 下的乘法逆元。"""
    old_r, remainder, old_s, coefficient = value, modulus, 1, 0
    while remainder:
        quotient = old_r // remainder
        old_r, remainder = remainder, old_r - quotient * remainder
        old_s, coefficient = coefficient, old_s - quotient * coefficient
    if old_r != 1:
        raise ValueError("e 与 phi(n) 必须互素")
    return old_s % modulus


def _is_prime(value: int) -> bool:
    """试除法验证教学用小素数，不是生产级素性测试。"""
    if value < 2:
        return False
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 1
    return True


def rsa_keypair_from_primes(
    first_prime: int, second_prime: int, public_exponent: int = 65537
) -> tuple[tuple[int, int], tuple[int, int]]:
    """以两个不同素数构造 RSA ``((n,e),(n,d))``。

    参数为 p、q 与 e；返回公钥和私钥。非素数、相同素数或不互素 e 会抛出 ValueError。
    核心：d 是 e 对 φ(n)=(p-1)(q-1) 的逆元，故 ed≡1 mod φ(n)。
    """
    if any(
        isinstance(value, bool) or not isinstance(value, int)
        for value in (first_prime, second_prime, public_exponent)
    ):
        raise ValueError("p、q、e 必须是整数")
    if (
        first_prime == second_prime
        or not _is_prime(first_prime)
        or not _is_prime(second_prime)
    ):
        raise ValueError("p、q 必须是不同素数")
    modulus = first_prime * second_prime
    phi = (first_prime - 1) * (second_prime - 1)
    if not 1 < public_exponent < phi or _gcd(public_exponent, phi) != 1:
        raise ValueError("e 必须位于 (1, phi) 且与 phi 互素")
    return (modulus, public_exponent), (modulus, _inverse(public_exponent, phi))


if __name__ == "__main__":
    assert rsa_keypair_from_primes(61, 53, 17) == ((3233, 17), (3233, 2753))
    assert rsa_keypair_from_primes(3, 11, 3)[0] == (33, 3)
    try:
        rsa_keypair_from_primes(15, 17, 3)
        raise AssertionError("合数应当抛出 ValueError")
    except ValueError:
        pass
    print("004_rsa_key_generation: all examples passed")
