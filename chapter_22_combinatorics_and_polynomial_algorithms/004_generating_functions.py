"""
文件意图：手写有限截断形式生成函数的多项式卷积与硬币找零系数计算。
适用场景：组合计数中用乘法组合独立选择，并只关心某个最大次数以内的系数。
核心思想：普通生成函数的乘法系数是指数和相同项的乘积之和；每种硬币对应 1+x^c+x^(2c)+...。
输入输出：输入多项式系数或硬币面额和目标和，输出截断卷积或无序找零方案数。
时间复杂度：卷积 O(degree^2)，硬币 DP O(coin_count * target)；空间复杂度 O(target)。
关键边界情况：空多项式、负截断次数、非正硬币面额和负目标值均有明确处理。
"""


def truncated_polynomial_product(
    left: list[int], right: list[int], max_degree: int
) -> list[int]:
    """计算两个普通生成函数系数的截断乘积。

    参数：left/right 按升幂存储系数；max_degree 是保留的最高次数。
    返回：长度 max_degree+1 的系数列表，缺失高次项视为零。
    边界情况：max_degree 为负抛出 ValueError；任一空多项式返回全零。
    关键算法点：x^i 与 x^j 的乘积只贡献给 x^(i+j)，因此逐对系数累加。
    """
    if max_degree < 0:
        raise ValueError("max_degree 不能为负数")
    product = [0] * (max_degree + 1)
    for left_degree, left_coefficient in enumerate(left):
        if left_degree > max_degree:
            break
        for right_degree, right_coefficient in enumerate(right):
            degree = left_degree + right_degree
            if degree > max_degree:
                break
            # 这是普通生成函数乘法的 Cauchy 乘积，不使用现成多项式库。
            product[degree] += left_coefficient * right_coefficient
    return product


def unordered_coin_change_count(coins: list[int], target: int) -> int:
    """计算用给定硬币面额凑出 target 的无序方案数量。

    参数：coins 是互异正整数面额列表；target 是非负目标和。
    返回：每种面额可无限使用时的无序组合数。
    边界情况：target 为 0 返回 1；负目标或重复/非正面额抛出 ValueError。
    关键算法点：逐个乘入 (1+x^coin+x^(2coin)+...)；正向更新保证同一面额可重复使用而不计排列。
    """
    if target < 0:
        raise ValueError("target 必须是非负整数")
    if any(coin <= 0 for coin in coins) or len(set(coins)) != len(coins):
        raise ValueError("coins 必须是互异正整数")
    coefficients = [0] * (target + 1)
    coefficients[0] = 1
    for coin in coins:
        for total in range(coin, target + 1):
            # 加入一枚当前面额后，余下 total-coin 的合法方案都可延伸到 total。
            coefficients[total] += coefficients[total - coin]
    return coefficients[target]


if __name__ == "__main__":
    assert truncated_polynomial_product([1, 1], [1, 1], 2) == [1, 2, 1]
    assert truncated_polynomial_product([1, 2], [3, 4], 1) == [3, 10]
    assert truncated_polynomial_product([], [1], 3) == [0, 0, 0, 0]
    assert unordered_coin_change_count([1, 2, 5], 5) == 4
    assert unordered_coin_change_count([], 0) == 1
    assert unordered_coin_change_count([], 4) == 0
    print("004_generating_functions: all examples passed")
