"""无符号变长整数（Varint）编码的教学实现。

适用场景：Varint 将整数拆为 7 位数据组，并用每字节最高位标记后续组；较小的非负整数
可使用更少字节。本文件采用低位组优先的 LEB128 风格表示，不包含有符号 ZigZag 变换。

输入输出：编码一个非负整数为 bytes；解码从 bytes 的指定偏移返回 ``(数值, 下一个偏移)``。
时间复杂度：O(b)，b 为所需字节数。空间复杂度：编码为 O(b)，解码为 O(1)。
关键边界：0 编码为单个零字节；负数、截断序列、非规范冗余表示和越界偏移抛出 ValueError。
"""


CONTINUATION_BIT = 0x80
PAYLOAD_MASK = 0x7F


def encode_unsigned_varint(value: int) -> bytes:
    """将非负整数编码为低位组优先的无符号 Varint。

    参数：value 为待编码的非负 Python 整数。
    返回值：由 7 位数据组与延续位组成的最短 bytes 序列。
    边界情况：0 返回 ``b"\\x00"``；负数、布尔值和非整数抛出 ValueError。
    关键算法点：每轮先输出最低 7 位，再右移 7 位；仅当高位尚未清空时设置延续位。
    """
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError("value 必须是非负整数")
    encoded = bytearray()
    while True:
        byte = value & PAYLOAD_MASK
        value >>= 7
        if value:
            encoded.append(byte | CONTINUATION_BIT)
        else:
            encoded.append(byte)
            return bytes(encoded)


def decode_unsigned_varint(data: bytes, offset: int = 0) -> tuple[int, int]:
    """从指定偏移解码一个无符号 Varint。

    参数：data 为字节串；offset 为第一个 Varint 字节的零基位置。
    返回值：``(decoded_value, next_offset)``，next_offset 指向该 Varint 之后。
    边界情况：截断延续字节、越界偏移和非规范冗余编码抛出 ValueError。
    关键算法点：第 i 组的 7 位数据放入结果的第 ``7*i`` 位；遇到无延续位字节即结束。
    """
    if not isinstance(data, bytes):
        raise ValueError("data 必须是 bytes")
    if isinstance(offset, bool) or not isinstance(offset, int) or not 0 <= offset < len(data):
        raise ValueError("offset 必须指向 data 中的有效字节")

    value = 0
    shift = 0
    position = offset
    while position < len(data):
        byte = data[position]
        value |= (byte & PAYLOAD_MASK) << shift
        position += 1
        if not byte & CONTINUATION_BIT:
            # 规范表示必须正好等于编码器的最短输出，拒绝如 b"\\x80\\x00" 这样的冗余形式。
            if encode_unsigned_varint(value) != data[offset:position]:
                raise ValueError("Varint 不是规范的最短表示")
            return value, position
        shift += 7
    raise ValueError("Varint 在延续位后截断")


if __name__ == "__main__":
    assert encode_unsigned_varint(0) == b"\x00"
    assert encode_unsigned_varint(300) == b"\xac\x02"
    assert decode_unsigned_varint(b"\xac\x02") == (300, 2)
    assert decode_unsigned_varint(b"\x01\x80\x01", 1) == (128, 3)
    assert encode_unsigned_varint(2**80 + 12345)
    try:
        decode_unsigned_varint(b"\x80")
        raise AssertionError("截断 Varint 应当抛出 ValueError")
    except ValueError:
        pass

    print("011_varint_encoding: all examples passed")
