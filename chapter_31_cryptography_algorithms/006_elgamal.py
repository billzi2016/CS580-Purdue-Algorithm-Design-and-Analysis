"""有限域 ElGamal 整数加解密教学实现。

本实现以调用方提供的小素数 p、底数 g、私钥与一次性随机指数 k 演示 ElGamal 的两个密文
分量。它不生成安全随机数、不验证生成元阶、不认证或编码任意消息，不能用于生产。
"""


def _power(base: int, exponent: int, modulus: int) -> int:
    """手写二进制模幂。"""
    result = 1
    while exponent:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result


def _inverse(value: int, modulus: int) -> int:
    """用扩展欧几里得计算模逆元。"""
    r0, r1, s0, s1 = value, modulus, 1, 0
    while r1:
        q = r0 // r1
        r0, r1, s0, s1 = r1, r0 - q * r1, s1, s0 - q * s1
    if r0 != 1:
        raise ValueError("域元素不可逆")
    return s0 % modulus


def elgamal_public_value(prime_modulus: int, generator: int, private_key: int) -> int:
    """计算公开值 y=g^x mod p；教学调用方负责提供可信域参数。"""
    if (
        any(
            isinstance(value, bool) or not isinstance(value, int)
            for value in (prime_modulus, generator, private_key)
        )
        or prime_modulus <= 3
        or not 2 <= generator < prime_modulus
        or not 1 <= private_key <= prime_modulus - 2
    ):
        raise ValueError("ElGamal 参数范围无效")
    return _power(generator, private_key, prime_modulus)


def elgamal_encrypt(
    message: int,
    prime_modulus: int,
    generator: int,
    public_value: int,
    ephemeral_exponent: int,
) -> tuple[int, int]:
    """返回 (c1,c2)=(g^k, m*y^k) mod p；k 必须每次新鲜且随机，本函数不生成它。"""
    if (
        any(
            isinstance(value, bool) or not isinstance(value, int)
            for value in (
                message,
                prime_modulus,
                generator,
                public_value,
                ephemeral_exponent,
            )
        )
        or not 0 <= message < prime_modulus
        or not 2 <= generator < prime_modulus
        or not 2 <= public_value < prime_modulus
        or not 1 <= ephemeral_exponent <= prime_modulus - 2
    ):
        raise ValueError("ElGamal 输入范围无效")
    first = _power(generator, ephemeral_exponent, prime_modulus)
    return first, message * _power(
        public_value, ephemeral_exponent, prime_modulus
    ) % prime_modulus


def elgamal_decrypt(
    ciphertext: tuple[int, int], prime_modulus: int, private_key: int
) -> int:
    """用共享因子 c1^x 的逆元恢复模 p 下的整数消息。"""
    if not isinstance(ciphertext, tuple) or len(ciphertext) != 2:
        raise ValueError("ciphertext 必须是 (c1, c2)")
    first, second = ciphertext
    if (
        any(
            isinstance(value, bool) or not isinstance(value, int)
            for value in (first, second, prime_modulus, private_key)
        )
        or prime_modulus <= 3
        or not 1 <= first < prime_modulus
        or not 0 <= second < prime_modulus
        or not 1 <= private_key <= prime_modulus - 2
    ):
        raise ValueError("ElGamal 输入范围无效")
    return (
        second
        * _inverse(_power(first, private_key, prime_modulus), prime_modulus)
        % prime_modulus
    )


if __name__ == "__main__":
    p, g, private, nonce = 23, 5, 6, 7
    public = elgamal_public_value(p, g, private)
    encrypted = elgamal_encrypt(13, p, g, public, nonce)
    assert encrypted == (17, 18)
    assert elgamal_decrypt(encrypted, p, private) == 13
    assert elgamal_decrypt(elgamal_encrypt(0, p, g, public, 1), p, private) == 0
    try:
        elgamal_encrypt(23, p, g, public, nonce)
        raise AssertionError("越界消息应当抛出 ValueError")
    except ValueError:
        pass
    print("006_elgamal: all examples passed")
