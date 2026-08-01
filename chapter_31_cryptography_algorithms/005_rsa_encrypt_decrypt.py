"""教科书 RSA 整数编解密教学实现。

输入是小于模数的单个非负整数和 (n, exponent) 密钥，输出是整数密文或明文。未实现任何
随机填充、分块、字节序列编码或抗侧信道措施，因而绝不能用于实际保密通信。
"""


def _modular_power(base: int, exponent: int, modulus: int) -> int:
    """手写二进制模幂，避免把 RSA 核心幂运算交给库调用。"""
    result = 1
    base %= modulus
    while exponent:
        if exponent & 1:
            result = result * base % modulus
        base = base * base % modulus
        exponent >>= 1
    return result


def _validate_key_and_value(value: int, key: tuple[int, int]) -> tuple[int, int]:
    """校验 RSA 整数消息及二元密钥的基本范围。"""
    if not isinstance(key, tuple) or len(key) != 2:
        raise ValueError("key 必须是 (n, exponent) 元组")
    modulus, exponent = key
    if any(isinstance(item, bool) or not isinstance(item, int) for item in (value, modulus, exponent)) or modulus <= 1 or exponent <= 0 or not 0 <= value < modulus:
        raise ValueError("消息、模数和指数范围无效")
    return modulus, exponent


def rsa_encrypt_integer(message: int, public_key: tuple[int, int]) -> int:
    """计算 c=m^e mod n；message 必须小于 n，返回整数密文。"""
    modulus, exponent = _validate_key_and_value(message, public_key)
    return _modular_power(message, exponent, modulus)


def rsa_decrypt_integer(ciphertext: int, private_key: tuple[int, int]) -> int:
    """计算 m=c^d mod n；仅与匹配的教学私钥配合使用。"""
    modulus, exponent = _validate_key_and_value(ciphertext, private_key)
    return _modular_power(ciphertext, exponent, modulus)


if __name__ == "__main__":
    public_key, private_key = (3233, 17), (3233, 2753)
    ciphertext = rsa_encrypt_integer(65, public_key)
    assert ciphertext == 2790
    assert rsa_decrypt_integer(ciphertext, private_key) == 65
    assert rsa_decrypt_integer(rsa_encrypt_integer(0, public_key), private_key) == 0
    try:
        rsa_encrypt_integer(3233, public_key)
        raise AssertionError("不小于模数的消息应当抛出 ValueError")
    except ValueError:
        pass
    print("005_rsa_encrypt_decrypt: all examples passed")
