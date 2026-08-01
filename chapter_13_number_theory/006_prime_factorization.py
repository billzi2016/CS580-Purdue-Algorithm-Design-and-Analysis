"""
文件意图：手写实现试除法质因数分解。
适用场景：分解中小规模整数、计算约数函数或验证数论样例。
核心思想：先处理 2，再只尝试奇数因子；剩余大于一的数必为质数。
输入输出：输入非零整数，返回按非递减顺序列出的质因数及其重复次数。
时间复杂度：O(sqrt(|n|))。空间复杂度：O(log |n|)。
关键边界：负数的第一个因子为 -1；零没有有限质因数分解并被拒绝。
"""


def prime_factorization(value: int) -> list[int]:
    """返回 value 的质因数列表。

    参数：value 为非零整数。
    返回：正数返回升序质因数；负数以 -1 开头。
    边界情况：1 返回空列表，-1 返回 [-1]，零抛出 ValueError。
    关键算法点：试除到 divisor*divisor 大于剩余数时，剩余数若大于一即为最后质因数。
    """
    if value == 0:
        raise ValueError("0 没有有限的质因数分解")
    factors: list[int] = []
    if value < 0:
        factors.append(-1)
        value = -value
    while value % 2 == 0 and value > 1:
        factors.append(2)
        value //= 2
    divisor = 3
    while divisor * divisor <= value:
        while value % divisor == 0:
            factors.append(divisor)
            value //= divisor
        divisor += 2
    if value > 1:
        factors.append(value)
    return factors


if __name__ == "__main__":
    assert prime_factorization(1) == []
    assert prime_factorization(360) == [2, 2, 2, 3, 3, 5]
    assert prime_factorization(97) == [97]
    assert prime_factorization(-12) == [-1, 2, 2, 3]
    print("006_prime_factorization: all examples passed")
