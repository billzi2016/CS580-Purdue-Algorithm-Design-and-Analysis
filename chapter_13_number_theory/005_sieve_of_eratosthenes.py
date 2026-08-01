"""
文件意图：手写实现埃拉托斯特尼筛法。
适用场景：一次预处理范围 [2, limit] 内全部质数，供多次查询或枚举使用。
核心思想：每个合数都有不大于其平方根的质因子，因此从质数平方开始标记倍数即可。
输入输出：输入非负上界，返回不超过该上界的所有质数。
时间复杂度：O(n log log n)。空间复杂度：O(n)。
关键边界：limit 小于二时返回空列表；负上界被拒绝。
"""


def sieve_of_eratosthenes(limit: int) -> list[int]:
    """返回所有不大于 limit 的质数。

    参数：limit 为非负整数上界。
    返回：升序质数列表。
    边界情况：0 与 1 没有质数；负数抛出 ValueError。
    关键算法点：从 candidate*candidate 开始，较小倍数此前已被更小质因子标记。
    """
    if limit < 0:
        raise ValueError("limit 不能为负数")
    if limit < 2:
        return []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    candidate = 2
    while candidate * candidate <= limit:
        if is_prime[candidate]:
            for multiple in range(candidate * candidate, limit + 1, candidate):
                is_prime[multiple] = False
        candidate += 1
    return [value for value in range(2, limit + 1) if is_prime[value]]


if __name__ == "__main__":
    assert sieve_of_eratosthenes(0) == []
    assert sieve_of_eratosthenes(2) == [2]
    assert sieve_of_eratosthenes(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    print("005_sieve_of_eratosthenes: all examples passed")
