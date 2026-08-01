"""
文件意图：手写实现最大公约数与最小公倍数。
适用场景：分数约分、模运算、周期计算和整除关系分析。
核心思想：欧几里得算法不断用余数替换较大数，直到余数为零。
输入输出：输入两个整数，输出非负最大公约数或最小公倍数。
时间复杂度：O(log min(|a|, |b|))。空间复杂度：O(1)。
关键边界：gcd(0, 0)=0；lcm 中任一参数为零时定义为零。
"""


def gcd(first: int, second: int) -> int:
    """计算 first 与 second 的非负最大公约数。

    参数：first、second 为整数。
    返回：二者的最大公约数；两个零返回零。
    边界情况：负数先取绝对值，零可自然参与余数迭代。
    关键算法点：gcd(a, b) 等于 gcd(b, a mod b)。
    """
    first, second = abs(first), abs(second)
    while second != 0:
        first, second = second, first % second
    return first


def lcm(first: int, second: int) -> int:
    """计算 first 与 second 的非负最小公倍数。

    参数：first、second 为整数。
    返回：最小公倍数；任一参数为零时返回零。
    边界情况：先检查零以避免除以零。
    关键算法点：先除以 gcd 再乘，减少中间值并保持整除性。
    """
    if first == 0 or second == 0:
        return 0
    return abs((first // gcd(first, second)) * second)


if __name__ == "__main__":
    assert gcd(54, 24) == 6
    assert gcd(-54, 24) == 6
    assert gcd(0, 0) == 0
    assert lcm(21, 6) == 42
    assert lcm(-4, 6) == 12 and lcm(0, 9) == 0
    print("001_gcd_lcm: all examples passed")
