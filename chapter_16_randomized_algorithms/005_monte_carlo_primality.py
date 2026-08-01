"""
Monte Carlo 素性检查：用 Fermat 随机基测试快速排除合数。

本文件的意图：
1. 展示 Monte Carlo 算法的特点：速度快，但存在可控的错误概率。
2. 明确 Fermat 测试的风险：Carmichael 数可能骗过所有互素基。
3. 保持本章主题为随机化；确定性 Miller-Rabin 已在数论章节实现。

返回值语义：
- False：一定是合数。
- True：可能是素数，不是严格证明。
"""

from math import gcd
from random import Random


def is_probably_prime_fermat(
    number: int,
    rounds: int = 8,
    seed: int | None = None,
) -> bool:
    """用随机 Fermat 基判断 number 是否“可能为素数”。"""

    if rounds <= 0:
        raise ValueError("rounds 必须为正数")
    if number < 2:
        return False
    if number in (2, 3):
        return True
    if number % 2 == 0:
        return False

    rng = Random(seed)
    for _ in range(rounds):
        base = rng.randint(2, number - 2)
        if gcd(base, number) != 1:
            return False
        if pow(base, number - 1, number) != 1:
            return False

    return True


def passes_fermat_base(number: int, base: int) -> bool:
    """检查 number 是否通过指定 base 的 Fermat 条件。

    这个函数用于教学展示伪素数：如果合数 n 满足 a^(n-1) ≡ 1 (mod n)，
    那么它会骗过以 a 为基的 Fermat 测试。
    """

    if number < 2:
        return False
    if not 1 < base < number - 1:
        raise ValueError("base 必须满足 1 < base < number - 1")
    if gcd(base, number) != 1:
        return False
    return pow(base, number - 1, number) == 1


def find_composites_reported_probably_prime(
    candidates: list[int],
    rounds: int,
    seed: int | None = None,
) -> list[int]:
    """找出给定候选中被 Fermat 测试误报为“可能素数”的合数。

    这个函数用于教学：Monte Carlo primality check 不是数学证明。比如 561 是
    Carmichael 数，很多 Fermat 基会让它看起来像素数。
    """

    false_positives: list[int] = []
    for index, value in enumerate(candidates):
        if value < 4:
            continue
        if _has_small_factor(value) and is_probably_prime_fermat(
            value, rounds, seed=index + (seed or 0)
        ):
            false_positives.append(value)
    return false_positives


def _has_small_factor(number: int) -> bool:
    """朴素试除确认 number 是否为合数；只用于小规模教学检查。"""

    divisor = 2
    while divisor * divisor <= number:
        if number % divisor == 0:
            return True
        divisor += 1
    return False


if __name__ == "__main__":
    assert is_probably_prime_fermat(2)
    assert is_probably_prime_fermat(97, rounds=5, seed=1)
    assert not is_probably_prime_fermat(1)
    assert not is_probably_prime_fermat(100)
    assert not is_probably_prime_fermat(91, rounds=5, seed=2)
    assert not passes_fermat_base(91, 2)
    assert passes_fermat_base(561, 2)
    assert 561 in find_composites_reported_probably_prime([91, 561], rounds=3, seed=14)

    print("005_monte_carlo_primality: all examples passed")
