"""有限域 Diffie-Hellman 密钥协商的教学实现。

适用场景：本文件展示双方由公开素数模数 p、底数 g 和各自私有指数计算相同共享整数的步骤。
它仅用于教学：不生成密码学安全随机数、不验证 g 的阶或标准群、不认证对方公钥、不做 KDF，
因此绝不能直接用于生产密钥协商。NIST SP 800-56A 将 DH 置于完整密钥建立方案中。

输入输出：显式提供参数和私钥，计算公开值及共享整数。时间复杂度 O(log exponent)，空间 O(1)。
边界：p 必须是本实现试除法可验证的奇素数；测试的小参数故意不安全，仅用于算术断言。
"""


def modular_power(base: int, exponent: int, modulus: int) -> int:
    """手写二进制模幂计算 base^exponent mod modulus。

    参数均为整数，exponent 非负且 modulus 大于 1；返回模幂结果。
    关键点：循环不变量为 result * base^remaining 与初始幂在模 modulus 下相等。
    """
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (base, exponent, modulus)) or exponent < 0 or modulus <= 1:
        raise ValueError("base、exponent 必须为整数，exponent 非负且 modulus 大于 1")
    result = 1
    base %= modulus
    while exponent:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result


def _is_prime(value: int) -> bool:
    """用试除法验证教学参数的素数模数；不适用于生产级大素数生成。"""
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def _validate_domain(prime_modulus: int, generator: int) -> None:
    """验证教学有限域参数；不替代标准群、子群和对手公钥完整验证。"""
    if any(isinstance(value, bool) or not isinstance(value, int) for value in (prime_modulus, generator)):
        raise ValueError("域参数必须是整数")
    if not _is_prime(prime_modulus) or prime_modulus <= 3:
        raise ValueError("prime_modulus 必须是大于 3 的素数")
    if not 2 <= generator <= prime_modulus - 2:
        raise ValueError("generator 必须位于 [2, prime_modulus - 2]")


def dh_public_value(prime_modulus: int, generator: int, private_exponent: int) -> int:
    """计算公开值 g^private_exponent mod p。

    参数：prime_modulus 和 generator 为公开域参数，private_exponent 为调用方私钥。
    返回值：可公开发送的有限域元素。私钥必须在 [1, p-2]；本函数不负责安全随机生成。
    """
    _validate_domain(prime_modulus, generator)
    if isinstance(private_exponent, bool) or not isinstance(private_exponent, int) or not 1 <= private_exponent <= prime_modulus - 2:
        raise ValueError("private_exponent 必须位于 [1, prime_modulus - 2]")
    return modular_power(generator, private_exponent, prime_modulus)


def dh_shared_secret(prime_modulus: int, own_private_exponent: int, peer_public_value: int) -> int:
    """计算 peer_public_value^own_private_exponent mod p 的共享整数。

    参数：p、己方私钥和对方公开值。返回共享整数。
    边界：拒绝不在 [2, p-2] 的对方公开值；这仍不构成生产所需的完整子群验证。
    关键点：两方分别得到 (g^b)^a 与 (g^a)^b，指数乘法交换性使其相同。
    """
    if isinstance(prime_modulus, bool) or not isinstance(prime_modulus, int) or not _is_prime(prime_modulus):
        raise ValueError("prime_modulus 必须是素数")
    if isinstance(own_private_exponent, bool) or not isinstance(own_private_exponent, int) or not 1 <= own_private_exponent <= prime_modulus - 2:
        raise ValueError("own_private_exponent 必须位于 [1, p-2]")
    if isinstance(peer_public_value, bool) or not isinstance(peer_public_value, int) or not 2 <= peer_public_value <= prime_modulus - 2:
        raise ValueError("peer_public_value 必须位于 [2, p-2]")
    return modular_power(peer_public_value, own_private_exponent, prime_modulus)


if __name__ == "__main__":
    p, g, alice_private, bob_private = 23, 5, 6, 15
    alice_public = dh_public_value(p, g, alice_private)
    bob_public = dh_public_value(p, g, bob_private)
    assert alice_public == 8 and bob_public == 19
    assert dh_shared_secret(p, alice_private, bob_public) == 2
    assert dh_shared_secret(p, alice_private, bob_public) == dh_shared_secret(p, bob_private, alice_public)
    assert modular_power(7, 0, 13) == 1
    try:
        dh_public_value(21, 5, 2)
        raise AssertionError("合数模数应当抛出 ValueError")
    except ValueError:
        pass
    print("003_diffie_hellman: all examples passed")
