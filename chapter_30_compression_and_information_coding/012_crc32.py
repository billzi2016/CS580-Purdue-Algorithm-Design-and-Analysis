"""CRC-32 差错检测码的逐位教学实现。

适用场景：循环冗余校验可为字节序列生成固定宽度校验值，用于检测传输或存储中的许多
意外错误。本文件实现 RFC 1952 所述 gzip 使用的 CRC-32 计算过程：初值与最终异或均为
全 1，采用反射形式多项式 0xEDB88320。CRC 不是密码学完整性或认证机制。

输入输出：输入 bytes，输出范围为 [0, 2^32) 的整数 CRC；另提供校验比较函数。
时间复杂度：O(8n)=O(n)。空间复杂度：O(1)。
关键边界：空字节串有效；非 bytes 输入、超出 32 位范围或布尔期望值抛出 ValueError。
来源：RFC 1952，第 2.3.1 节及附录的 CRC 示例代码。
"""

CRC32_POLYNOMIAL = 0xEDB88320
CRC32_MASK = 0xFFFFFFFF


def crc32(data: bytes) -> int:
    """逐位计算 bytes 的 CRC-32 校验值。

    参数：data 为待校验的原始字节串。
    返回值：0 到 0xFFFFFFFF 的 CRC-32 整数值。
    边界情况：空 bytes 返回其定义的 CRC 值；bytearray、字符串等其他类型抛出 ValueError。
    关键算法点：每处理一个字节先异或进入寄存器低位，随后执行 8 次右移；最低位为 1 时
        额外异或反射多项式，这正是模二多项式除法在位级上的递推。
    """
    if not isinstance(data, bytes):
        raise ValueError("data 必须是 bytes")
    remainder = CRC32_MASK
    for byte in data:
        remainder ^= byte
        for _ in range(8):
            if remainder & 1:
                remainder = (remainder >> 1) ^ CRC32_POLYNOMIAL
            else:
                remainder >>= 1
    return remainder ^ CRC32_MASK


def verify_crc32(data: bytes, expected_crc: int) -> bool:
    """检查 data 的 CRC-32 是否等于给定的 32 位期望值。

    参数：data 为待检查字节串；expected_crc 为预期的无符号 32 位整数。
    返回值：二者相等时为 True，否则为 False。
    边界情况：expected_crc 不是 32 位整数时抛出 ValueError；数据本身沿用 crc32 的类型要求。
    关键算法点：校验必须重新计算完整数据的 CRC，而非比较某个局部哈希或长度。
    """
    if (
        isinstance(expected_crc, bool)
        or not isinstance(expected_crc, int)
        or not 0 <= expected_crc <= CRC32_MASK
    ):
        raise ValueError("expected_crc 必须是 32 位非负整数")
    return crc32(data) == expected_crc


if __name__ == "__main__":
    assert crc32(b"") == 0
    assert crc32(b"123456789") == 0xCBF43926
    message = b"algorithm design"
    assert verify_crc32(message, crc32(message))
    assert not verify_crc32(message + b"!", crc32(message))
    try:
        crc32(bytearray(b"data"))
        raise AssertionError("非 bytes 输入应当抛出 ValueError")
    except ValueError:
        pass

    print("012_crc32: all examples passed")
