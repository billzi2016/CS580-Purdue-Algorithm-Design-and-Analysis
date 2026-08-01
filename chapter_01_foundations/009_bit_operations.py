"""
文件意图：
    本文件手写实现常见位运算工具，用于集合状态、奇偶判断和低位操作。

适用场景：
    需要用整数的二进制位表示状态，或需要 O(1) 完成低位检查。

核心思想：
    使用与、或、异或、移位等基础位运算直接操作整数二进制表示。
"""


def is_power_of_two(value: int) -> bool:
    """
    判断 value 是否为 2 的幂。

    关键点：
        正的 2 的幂只有一个二进制位为 1，因此 value & (value - 1) 等于 0。
    """
    return value > 0 and (value & (value - 1)) == 0


def lowbit(value: int) -> int:
    """
    返回 value 的最低位 1 所代表的值。

    例子：
        lowbit(12) = lowbit(0b1100) = 0b0100 = 4。
    """
    return value & -value


def count_set_bits(value: int) -> int:
    """
    统计非负整数 value 的二进制表示中 1 的个数。
    """
    if value < 0:
        raise ValueError("本函数只处理非负整数")

    count = 0
    current = value
    while current:
        # 每次清掉最低位的 1。
        current &= current - 1
        count += 1
    return count


def has_bit(mask: int, index: int) -> bool:
    """
    判断 mask 的第 index 位是否为 1。
    """
    if index < 0:
        raise ValueError("index 必须非负")
    return (mask & (1 << index)) != 0


def set_bit(mask: int, index: int) -> int:
    """
    将 mask 的第 index 位设置为 1，并返回新 mask。
    """
    if index < 0:
        raise ValueError("index 必须非负")
    return mask | (1 << index)


def clear_bit(mask: int, index: int) -> int:
    """
    将 mask 的第 index 位清零，并返回新 mask。
    """
    if index < 0:
        raise ValueError("index 必须非负")
    return mask & ~(1 << index)


if __name__ == "__main__":
    assert is_power_of_two(1)
    assert is_power_of_two(16)
    assert not is_power_of_two(18)
    assert lowbit(12) == 4
    assert count_set_bits(0b101101) == 4
    assert set_bit(0b1000, 1) == 0b1010
    assert has_bit(0b1010, 3)
    assert clear_bit(0b1010, 3) == 0b0010

    print("009_bit_operations: all examples passed")
