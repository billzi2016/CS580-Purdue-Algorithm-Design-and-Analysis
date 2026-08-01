"""
文件意图：手写实现针对非负整数的 LSD 基数排序。
适用场景：固定或较短十进制整数键的大量排序。
核心思想：从最低有效位开始，反复以稳定计数分配处理每一位。
输入输出：输入非负整数列表，返回新的非递减排序列表。
时间复杂度：O(d(n + b))，d 为最大位数，b=10。空间复杂度：O(n + b)。
关键边界：空列表返回空；出现负数时明确拒绝，因为本基础版本不处理符号位。
"""


def _sort_by_digit(values: list[int], exponent: int) -> list[int]:
    """按 exponent 所代表的十进制位稳定排序 values。"""
    counts = [0] * 10
    for value in values:
        counts[(value // exponent) % 10] += 1
    for digit in range(1, 10):
        counts[digit] += counts[digit - 1]
    result = [0] * len(values)
    # 从右向左放置，使相同当前位的元素保持此前低位的相对顺序。
    for index in range(len(values) - 1, -1, -1):
        value = values[index]
        digit = (value // exponent) % 10
        counts[digit] -= 1
        result[counts[digit]] = value
    return result


def radix_sort(values: list[int]) -> list[int]:
    """返回非负整数 values 的非递减排序副本。

    参数：values 为非负整数列表。
    返回：新排序列表。
    边界情况：空列表直接返回；负数会抛出 ValueError。
    关键算法点：每一轮必须稳定，低位排序信息才能在高位排序后保留。
    """
    if any(value < 0 for value in values):
        raise ValueError("本基础版 radix_sort 只支持非负整数")
    result = values[:]
    if not result:
        return result
    exponent = 1
    maximum = max(result)
    while maximum // exponent > 0:
        result = _sort_by_digit(result, exponent)
        exponent *= 10
    return result


if __name__ == "__main__":
    assert radix_sort([]) == []
    assert radix_sort([0]) == [0]
    assert radix_sort([170, 45, 75, 90, 802, 24, 2, 66]) == [
        2,
        24,
        45,
        66,
        75,
        90,
        170,
        802,
    ]
    assert radix_sort([10, 1, 10, 0]) == [0, 1, 10, 10]
    try:
        radix_sort([1, -1])
        assert False, "负数应被拒绝"
    except ValueError as error:
        assert "非负整数" in str(error)
    print("005_radix_sort: all examples passed")
