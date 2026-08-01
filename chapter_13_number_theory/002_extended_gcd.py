"""
文件意图：手写实现扩展欧几里得算法。
适用场景：求模逆元、解线性丢番图方程和合并同余方程。
核心思想：在普通欧几里得回代中同步维护贝祖系数。
输入输出：输入两个整数，返回 (g, x, y)，满足 ax + by = g。
时间复杂度：O(log min(|a|, |b|))。空间复杂度：O(1)。
关键边界：可处理负数与零；(0, 0) 返回 (0, 0, 0)。
"""


def extended_gcd(first: int, second: int) -> tuple[int, int, int]:
    """返回满足 first*x + second*y = gcd(first, second) 的 (gcd, x, y)。

    参数：first、second 为整数。
    返回：非负 gcd 与一组对应贝祖系数。
    边界情况：两个输入均为零时系数取零。
    关键算法点：每次余数更新同时对系数执行相同线性组合。
    """
    if first == 0 and second == 0:
        return 0, 0, 0
    old_remainder, remainder = abs(first), abs(second)
    old_x, x = 1, 0
    old_y, y = 0, 1
    while remainder != 0:
        quotient = old_remainder // remainder
        old_remainder, remainder = remainder, old_remainder - quotient * remainder
        old_x, x = x, old_x - quotient * x
        old_y, y = y, old_y - quotient * y
    if first < 0:
        old_x = -old_x
    if second < 0:
        old_y = -old_y
    return old_remainder, old_x, old_y


if __name__ == "__main__":
    divisor, coefficient_x, coefficient_y = extended_gcd(240, 46)
    assert divisor == 2 and 240 * coefficient_x + 46 * coefficient_y == divisor
    divisor, coefficient_x, coefficient_y = extended_gcd(-15, 6)
    assert divisor == 3 and -15 * coefficient_x + 6 * coefficient_y == divisor
    assert extended_gcd(0, 0) == (0, 0, 0)
    print("002_extended_gcd: all examples passed")
