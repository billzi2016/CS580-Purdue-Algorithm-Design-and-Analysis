"""
文件意图：手写预处理阶乘、逆阶乘，并在模素数意义下计算排列和组合数。
适用场景：竞赛组合计数、动态规划转移中大量重复查询 C(n, k) 的场景。
核心思想：先线性累乘得到 factorial，再由费马小定理求最大阶乘的逆元并反向递推。
输入输出：输入最大 n 和素数模数；查询返回对应的模运算结果。
时间复杂度：预处理 O(max_n + log mod)，每次查询 O(1)；空间复杂度 O(max_n)。
关键边界情况：拒绝负范围、非素数模数假设外的输入，以及不在预处理范围内的查询。
"""


class CombinatoricsTable:
    """在固定素数模数下支持阶乘、排列和组合数的预处理表。"""

    def __init__(self, max_n: int, modulus: int = 1_000_000_007) -> None:
        """建立 [0, max_n] 的组合数预处理表。

        参数：max_n 是最大可查询非负整数；modulus 是大于 max_n 的素数模数。
        返回：无，结果保存在 factorial 与 inverse_factorial 属性中。
        边界情况：max_n 为负、模数不大于 max_n 或小于 2 时抛出 ValueError。
        关键算法点：只对 factorial[max_n] 做一次快速幂，再利用 inv_fact[i-1]=inv_fact[i]*i 反推。
        """
        if max_n < 0:
            raise ValueError("max_n 不能为负数")
        if modulus <= max_n or modulus < 2:
            raise ValueError("modulus 必须是大于 max_n 的素数")
        self.max_n = max_n
        self.modulus = modulus
        self.factorial = [1] * (max_n + 1)
        for value in range(1, max_n + 1):
            self.factorial[value] = self.factorial[value - 1] * value % modulus

        self.inverse_factorial = [1] * (max_n + 1)
        # 费马小定理在 modulus 为素数时给出 a^(p-2) ≡ a^(-1) (mod p)。
        self.inverse_factorial[max_n] = pow(self.factorial[max_n], modulus - 2, modulus)
        for value in range(max_n, 0, -1):
            self.inverse_factorial[value - 1] = (
                self.inverse_factorial[value] * value % modulus
            )

    def permutations(self, n: int, k: int) -> int:
        """返回从 n 个不同元素中取有序 k 元组的数量 P(n, k)。

        参数：n 是元素数量，k 是选取数量。
        返回：P(n, k) 对模数取模的结果；当 k 不在 [0, n] 时返回 0。
        边界情况：n 超出预处理范围抛出 ValueError。
        关键算法点：P(n,k)=n!/(n-k)!，除法改为乘逆阶乘。
        """
        self._check_n(n)
        if k < 0 or k > n:
            return 0
        return self.factorial[n] * self.inverse_factorial[n - k] % self.modulus

    def combinations(self, n: int, k: int) -> int:
        """返回从 n 个不同元素中取无序 k 元组的数量 C(n, k)。

        参数：n 是元素数量，k 是选取数量。
        返回：C(n, k) 对模数取模的结果；当 k 不在 [0, n] 时返回 0。
        边界情况：n 超出预处理范围抛出 ValueError。
        关键算法点：C(n,k)=n!/(k!(n-k)!)，三个预处理值相乘即可完成查询。
        """
        self._check_n(n)
        if k < 0 or k > n:
            return 0
        return (
            self.factorial[n]
            * self.inverse_factorial[k]
            % self.modulus
            * self.inverse_factorial[n - k]
            % self.modulus
        )

    def _check_n(self, n: int) -> None:
        if not 0 <= n <= self.max_n:
            raise ValueError("n 必须位于预处理范围内")


if __name__ == "__main__":
    table = CombinatoricsTable(20)
    assert table.factorial[0] == 1
    assert table.factorial[5] == 120
    assert table.permutations(5, 3) == 60
    assert table.combinations(5, 2) == 10
    assert table.combinations(8, 0) == 1
    assert table.combinations(8, 9) == 0
    print("001_factorials_and_combinations: all examples passed")
