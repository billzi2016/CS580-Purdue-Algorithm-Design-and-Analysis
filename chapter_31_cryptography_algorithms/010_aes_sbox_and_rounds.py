"""AES 轮函数教学实现：S-box、SubBytes、ShiftRows、MixColumns 与 AddRoundKey。

本文件只展示 FIPS 197 的单轮状态变换，不含密钥扩展和完整 AES 加解密，不能用于生产。
状态按 16 个字节的列优先顺序存储；每个函数返回新列表，不原地修改调用方数据。
"""


def _multiply(left: int, right: int) -> int:
    """在 AES 的 GF(2^8) 中相乘，约化多项式为 x^8+x^4+x^3+x+1。"""
    result = 0
    while right:
        if right & 1:
            result ^= left
        left <<= 1
        if left & 0x100:
            left ^= 0x11B
        right >>= 1
    return result


def _inverse(value: int) -> int:
    """用有限域幂 a^254 求非零元素逆元；0 的 S-box 逆元约定为 0。"""
    if value == 0:
        return 0
    result = 1
    base = value
    exponent = 254
    while exponent:
        if exponent & 1:
            result = _multiply(result, base)
        base = _multiply(base, base)
        exponent >>= 1
    return result


def aes_sbox(value: int) -> int:
    """手写 AES S-box：有限域逆元后进行仿射变换。"""
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 255:
        raise ValueError("value 必须是 0 到 255 的整数")
    inverse = _inverse(value)
    transformed = inverse
    for shift in range(1, 5):
        transformed ^= ((inverse << shift) | (inverse >> (8 - shift))) & 0xFF
    return transformed ^ 0x63


def _state(values: list[int]) -> list[int]:
    """校验 AES 128 位状态或轮密钥。"""
    if (
        not isinstance(values, list)
        or len(values) != 16
        or any(
            isinstance(value, bool)
            or not isinstance(value, int)
            or not 0 <= value <= 255
            for value in values
        )
    ):
        raise ValueError("状态必须是 16 个字节的列表")
    return values


def sub_bytes(state: list[int]) -> list[int]:
    """对状态的每个字节独立应用 AES S-box。"""
    return [aes_sbox(value) for value in _state(state)]


def shift_rows(state: list[int]) -> list[int]:
    """按 AES 列优先布局，将第 r 行循环左移 r 个字节。"""
    source = _state(state)
    return [
        source[4 * ((column + row) % 4) + row]
        for column in range(4)
        for row in range(4)
    ]


def mix_columns(state: list[int]) -> list[int]:
    """对每列乘固定 MDS 矩阵，扩散该列的四个字节。"""
    source = _state(state)
    result: list[int] = []
    for column in range(0, 16, 4):
        a, b, c, d = source[column : column + 4]
        result.extend(
            (
                _multiply(2, a) ^ _multiply(3, b) ^ c ^ d,
                a ^ _multiply(2, b) ^ _multiply(3, c) ^ d,
                a ^ b ^ _multiply(2, c) ^ _multiply(3, d),
                _multiply(3, a) ^ b ^ c ^ _multiply(2, d),
            )
        )
    return result


def add_round_key(state: list[int], round_key: list[int]) -> list[int]:
    """逐字节 XOR 状态与同长度轮密钥。"""
    return [
        left ^ right
        for left, right in zip(_state(state), _state(round_key), strict=True)
    ]


if __name__ == "__main__":
    assert aes_sbox(0x53) == 0xED
    assert aes_sbox(0) == 0x63
    assert shift_rows(list(range(16))) == [
        0,
        5,
        10,
        15,
        4,
        9,
        14,
        3,
        8,
        13,
        2,
        7,
        12,
        1,
        6,
        11,
    ]
    assert add_round_key([1] * 16, [1] * 16) == [0] * 16
    print("010_aes_sbox_and_rounds: all examples passed")
