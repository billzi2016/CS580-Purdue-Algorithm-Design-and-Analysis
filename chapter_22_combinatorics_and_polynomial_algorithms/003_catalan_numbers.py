"""
文件意图：手写计算 Catalan 数，并展示其二叉树、括号匹配等组合意义。
适用场景：计数合法括号序列、不同二叉搜索树形状、凸多边形三角剖分等问题。
核心思想：第 n 个对象按根或首次匹配位置划分为两个独立子对象，得到卷积型递推。
输入输出：输入非负整数 n，输出第 n 个 Catalan 数的精确整数值。
时间复杂度：动态规划 O(n^2)，空间复杂度 O(n)。
关键边界情况：n=0 时空对象也有一种构造；负数输入必须拒绝。
"""


def catalan_number(n: int) -> int:
    """通过递推式计算第 n 个 Catalan 数。

    参数：n 是非负序号。
    返回：第 n 个 Catalan 数 C_n。
    边界情况：n 为负数抛出 ValueError；n 为 0 时返回 1。
    关键算法点：根左侧有 left 个元素时，右侧必须有 n-1-left 个元素，二者构造数相乘。
    """
    if n < 0:
        raise ValueError("n 必须是非负整数")
    values = [0] * (n + 1)
    values[0] = 1
    for size in range(1, n + 1):
        for left_size in range(size):
            right_size = size - 1 - left_size
            # 枚举根划分位置，所有左右子结构组合在这里累加。
            values[size] += values[left_size] * values[right_size]
    return values[n]


def count_balanced_parentheses(pair_count: int) -> int:
    """返回由 pair_count 对括号组成的合法括号序列数量。

    参数：pair_count 是左右括号对数。
    返回：对应的 Catalan 数。
    边界情况：零对括号对应唯一空串；负数输入抛出 ValueError。
    关键算法点：合法序列中首个左括号的匹配右括号将问题分割为两个独立合法片段。
    """
    return catalan_number(pair_count)


if __name__ == "__main__":
    assert catalan_number(0) == 1
    assert catalan_number(1) == 1
    assert catalan_number(3) == 5
    assert catalan_number(5) == 42
    assert count_balanced_parentheses(4) == 14
    try:
        catalan_number(-1)
        raise AssertionError("负数输入应抛出 ValueError")
    except ValueError:
        pass
    print("003_catalan_numbers: all examples passed")
