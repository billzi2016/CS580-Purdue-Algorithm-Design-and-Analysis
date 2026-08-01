"""偶校验 Hamming Code 的单比特纠错教学实现。

适用场景：Hamming 码在位置为 2 的幂的位置放置校验位，并利用 syndrome 定位一个翻转位。
本实现处理任意长度二进制数据的基本 Hamming 码，采用偶校验；不附加总校验位，因此不是
SECDED，不能可靠地区分双比特错误与单比特错误。

输入输出：编码将 ``"0"``/``"1"`` 数据串转换为码字；解码会修正一个 syndrome 指向的位，
并返回 ``(数据串, 修正的 1 基位置或 0)``。
时间复杂度：编码与解码均为 O(n log n)，因为每个校验位扫描其覆盖的位置。空间复杂度 O(n)。
关键边界：空数据返回空码字；非法字符抛出 ValueError；多比特错误不在本基础版的可纠正范围。
来源：Cornell CS 414 Hamming code 教学材料。
"""


def _validate_bit_string(bits: str, name: str) -> None:
    """验证输入是只含 0 和 1 的字符串。"""
    if not isinstance(bits, str) or any(bit not in "01" for bit in bits):
        raise ValueError(f"{name} 必须是只含 0 和 1 的字符串")


def _is_power_of_two(value: int) -> bool:
    """判断正整数是否为 2 的幂；Hamming 码用这些 1 基位置保存校验位。"""
    return value > 0 and value & (value - 1) == 0


def _required_parity_bits(data_length: int) -> int:
    """计算满足 2^r >= m + r + 1 的最小校验位数量。"""
    parity_count = 0
    while (1 << parity_count) < data_length + parity_count + 1:
        parity_count += 1
    return parity_count


def hamming_encode(data_bits: str) -> str:
    """用偶校验编码一段二进制数据。

    参数：data_bits 为任意长度的 ``0``/``1`` 字符串。
    返回值：校验位位于 1、2、4、8……位置的 Hamming 码字。
    边界情况：空字符串返回空字符串；非法字符抛出 ValueError。
    关键算法点：先把数据填入非 2 的幂位置，再令每个校验覆盖集合的异或和为 0；这样接收端
        对同一覆盖集合求异或，非零结果的二进制值就是单个错误位置。
    """
    _validate_bit_string(data_bits, "data_bits")
    if not data_bits:
        return ""
    codeword_length = len(data_bits) + _required_parity_bits(len(data_bits))
    codeword = [0] * (
        codeword_length + 1
    )  # 下标 0 不使用，使数组下标等于 Hamming 的 1 基位置。
    data_index = 0
    for position in range(1, codeword_length + 1):
        if not _is_power_of_two(position):
            codeword[position] = int(data_bits[data_index])
            data_index += 1

    parity_position = 1
    while parity_position <= codeword_length:
        parity = 0
        for position in range(1, codeword_length + 1):
            if position & parity_position:
                parity ^= codeword[position]
        # 校验位初始为 0，故覆盖集合中已有数据位的异或即为要写入的偶校验值。
        codeword[parity_position] = parity
        parity_position <<= 1
    return "".join(str(bit) for bit in codeword[1:])


def hamming_decode_and_correct(codeword_bits: str) -> tuple[str, int]:
    """检查 Hamming 码字、修正一个 syndrome 指向的位并提取数据位。

    参数：codeword_bits 为 hamming_encode 输出或发生至多一个比特翻转的码字。
    返回值：``(恢复的数据位串, corrected_position)``；无错误时位置为 0。
    边界情况：空码字返回 ``("", 0)``；syndrome 超出码字长度或输入不合法时抛出 ValueError。
    关键算法点：每个失败的校验位贡献其位置权重，所有失败权重的异或和构成出错的 1 基位置。
    """
    _validate_bit_string(codeword_bits, "codeword_bits")
    if not codeword_bits:
        return "", 0
    codeword = [0] + [int(bit) for bit in codeword_bits]
    syndrome = 0
    parity_position = 1
    while parity_position <= len(codeword_bits):
        parity = 0
        for position in range(1, len(codeword)):
            if position & parity_position:
                parity ^= codeword[position]
        if parity:
            syndrome |= parity_position
        parity_position <<= 1
    if syndrome > len(codeword_bits):
        raise ValueError("syndrome 指向码字外位置，输入不是可修正的单比特错误")
    if syndrome:
        codeword[syndrome] ^= 1
    data_bits = "".join(
        str(codeword[position])
        for position in range(1, len(codeword))
        if not _is_power_of_two(position)
    )
    return data_bits, syndrome


if __name__ == "__main__":
    encoded = hamming_encode("1011")
    assert encoded == "0110011"
    assert hamming_decode_and_correct(encoded) == ("1011", 0)
    corrupted = encoded[:4] + ("1" if encoded[4] == "0" else "0") + encoded[5:]
    assert hamming_decode_and_correct(corrupted) == ("1011", 5)
    assert hamming_encode("") == ""
    assert hamming_decode_and_correct("") == ("", 0)
    try:
        hamming_encode("102")
        raise AssertionError("非法位串应当抛出 ValueError")
    except ValueError:
        pass

    print("013_hamming_code: all examples passed")
