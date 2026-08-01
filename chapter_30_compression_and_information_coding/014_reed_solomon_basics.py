"""Reed-Solomon 基础：GF(2^8) 系统码编码与 syndrome 检测。

适用场景：Reed-Solomon 码在有限域上添加校验符号，用于检测或纠正符号错误。本基础版在
GF(2^8) 上以本原多项式 0x11D 构造生成多项式，提供系统码编码与 syndrome 校验；它不实现
Berlekamp-Massey、Chien 搜索或 Forney 算法，因此只能报告是否检测到错误，不能定位或纠正。
该边界足以展示有限域乘法、生成多项式除法和 syndrome 的核心，但不应当用于生产恢复。

输入输出：输入消息 bytes 与校验符号数，输出原消息后接校验 bytes；校验函数返回是否通过。
时间复杂度：编码 O(nr)，syndrome 校验 O((n+r)r)，r 为校验符号数。空间复杂度 O(n+r)。
关键边界：消息加校验符号总长度至多 255；校验符号数为 1–254；本实现只接受 bytes。
来源：James S. Plank, “A Tutorial on Reed-Solomon Coding for Fault-Tolerance in RAID-like Systems”。
"""


FIELD_PRIMITIVE_POLYNOMIAL = 0x11D
FIELD_SIZE = 256
FIELD_ORDER = 255


def gf_multiply(left: int, right: int) -> int:
    """在 GF(2^8) 中用俄罗斯农夫乘法计算两个域元素的乘积。

    参数：left、right 均为 0 到 255 的整数。
    返回值：使用多项式 0x11D 约化后的域乘积。
    边界情况：任一输入越界、非整数或布尔值抛出 ValueError；乘以 0 返回 0。
    关键算法点：域加法为 XOR；每次左移若溢出 8 位，就 XOR 本原多项式以完成模多项式约化。
    """
    for value, name in ((left, "left"), (right, "right")):
        if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value < FIELD_SIZE:
            raise ValueError(f"{name} 必须是 0 到 255 的整数")
    product = 0
    while right:
        if right & 1:
            product ^= left
        right >>= 1
        left <<= 1
        if left & FIELD_SIZE:
            left ^= FIELD_PRIMITIVE_POLYNOMIAL
    return product


def gf_power(base: int, exponent: int) -> int:
    """在 GF(2^8) 中计算非负整数幂，供生成多项式与 syndrome 求值使用。"""
    if isinstance(exponent, bool) or not isinstance(exponent, int) or exponent < 0:
        raise ValueError("exponent 必须是非负整数")
    result = 1
    while exponent:
        if exponent & 1:
            result = gf_multiply(result, base)
        base = gf_multiply(base, base)
        exponent >>= 1
    return result


def _polynomial_multiply(left: list[int], right: list[int]) -> list[int]:
    """在 GF(2^8) 上相乘两个最高次项在前的系数多项式。"""
    result = [0] * (len(left) + len(right) - 1)
    for left_index, left_coefficient in enumerate(left):
        for right_index, right_coefficient in enumerate(right):
            result[left_index + right_index] ^= gf_multiply(left_coefficient, right_coefficient)
    return result


def rs_generator_polynomial(parity_symbols: int) -> list[int]:
    """构造根为 α^0 到 α^(r-1) 的 Reed-Solomon 生成多项式。

    参数：parity_symbols 是要添加的校验符号数 r。
    返回值：最高次项在前的生成多项式系数列表，首项必为 1。
    边界情况：r 不在 1–254 时抛出 ValueError。
    关键算法点：在特征为 2 的域中减法与加法都等于 XOR，故因子 ``(x - α^i)`` 表示为
        系数 ``[1, α^i]``。
    """
    if isinstance(parity_symbols, bool) or not isinstance(parity_symbols, int) or not 1 <= parity_symbols < FIELD_ORDER:
        raise ValueError("parity_symbols 必须是 1 到 254 的整数")
    generator = [1]
    for exponent in range(parity_symbols):
        generator = _polynomial_multiply(generator, [1, gf_power(2, exponent)])
    return generator


def _validate_message(message: bytes, parity_symbols: int) -> None:
    """检查系统码输入及 GF(2^8) 最大码字长度限制。"""
    if not isinstance(message, bytes):
        raise ValueError("message 必须是 bytes")
    rs_generator_polynomial(parity_symbols)
    if len(message) + parity_symbols > FIELD_ORDER:
        raise ValueError("消息长度与校验符号数之和不能超过 255")


def reed_solomon_encode(message: bytes, parity_symbols: int) -> bytes:
    """对消息执行系统化 Reed-Solomon 编码，返回原消息加校验符号。

    参数：message 为原始 bytes；parity_symbols 为要附加的校验字节数。
    返回值：长度为 ``len(message) + parity_symbols`` 的系统码字。
    边界情况：空消息可编码为全校验码字；长度超过域上限或参数非法时抛出 ValueError。
    关键算法点：将消息多项式乘 x^r 后除以生成多项式；余数就是追加的校验符号，使最终码字
        能被生成多项式整除。
    """
    _validate_message(message, parity_symbols)
    generator = rs_generator_polynomial(parity_symbols)
    working = list(message) + [0] * parity_symbols
    for message_index in range(len(message)):
        leading = working[message_index]
        if leading:
            # 消去当前最高次项；首项系数为 1，因此无需做域除法。
            for generator_index in range(1, len(generator)):
                working[message_index + generator_index] ^= gf_multiply(generator[generator_index], leading)
    return message + bytes(working[-parity_symbols:])


def _evaluate_polynomial(coefficients: bytes, point: int) -> int:
    """用 Horner 法在 GF(2^8) 中求最高次项在前的多项式值。"""
    value = 0
    for coefficient in coefficients:
        value = gf_multiply(value, point) ^ coefficient
    return value


def reed_solomon_syndromes(codeword: bytes, parity_symbols: int) -> list[int]:
    """计算 Reed-Solomon 码字在生成多项式各根处的 syndrome。

    参数：codeword 为待检查码字；parity_symbols 必须与编码时一致。
    返回值：r 个 syndrome 整数；全部为 0 表示通过本构造的校验。
    边界情况：空码字、长度超限或参数非法抛出 ValueError。
    关键算法点：合法码字被生成多项式整除，故在生成多项式的每个根 α^i 处求值都应为 0。
    """
    _validate_message(codeword[:-parity_symbols] if isinstance(codeword, bytes) and len(codeword) >= parity_symbols else b"", parity_symbols)
    if not isinstance(codeword, bytes) or len(codeword) < parity_symbols:
        raise ValueError("codeword 长度至少应等于 parity_symbols")
    if len(codeword) > FIELD_ORDER:
        raise ValueError("codeword 长度不能超过 255")
    return [_evaluate_polynomial(codeword, gf_power(2, exponent)) for exponent in range(parity_symbols)]


def reed_solomon_verify(codeword: bytes, parity_symbols: int) -> bool:
    """检查码字是否通过 Reed-Solomon syndrome 校验。

    参数：codeword 是可能被篡改的完整码字；parity_symbols 与编码时的值相同。
    返回值：所有 syndrome 为 0 时返回 True，否则返回 False。
    边界情况：格式或参数错误抛出 ValueError；本函数检测错误但不定位或修正错误。
    关键算法点：只要至少一个根处求值非零，码字就不再满足生成多项式的整除条件。
    """
    return all(syndrome == 0 for syndrome in reed_solomon_syndromes(codeword, parity_symbols))


if __name__ == "__main__":
    assert gf_multiply(0x57, 0x83) == 0x31
    message = b"RS basics"
    codeword = reed_solomon_encode(message, parity_symbols=8)
    assert codeword[: len(message)] == message
    assert reed_solomon_verify(codeword, parity_symbols=8)
    corrupted = codeword[:3] + bytes([codeword[3] ^ 0x01]) + codeword[4:]
    assert not reed_solomon_verify(corrupted, parity_symbols=8)
    assert reed_solomon_encode(b"", parity_symbols=2) == b"\x00\x00"
    try:
        reed_solomon_encode(b"data", parity_symbols=0)
        raise AssertionError("非法校验符号数应当抛出 ValueError")
    except ValueError:
        pass

    print("014_reed_solomon_basics: all examples passed")
