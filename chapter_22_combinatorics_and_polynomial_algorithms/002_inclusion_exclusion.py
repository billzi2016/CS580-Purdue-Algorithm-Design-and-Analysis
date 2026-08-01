"""
文件意图：手写实现有限集合并集大小的容斥原理计算。
适用场景：多个条件的“至少满足一个”计数，且能直接计算任意交集大小的场景。
核心思想：奇数个集合交集相加、偶数个集合交集相减，抵消同一元素被重复计数的次数。
输入输出：输入集合数和交集大小回调，输出所有集合并集的大小。
时间复杂度：O(2^m) 次交集查询，其中 m 为集合数量；额外空间 O(m)。
关键边界情况：零个集合返回 0；交集回调给出负数时拒绝该无效计数。
"""

from collections.abc import Callable
from itertools import combinations


def union_size_by_inclusion_exclusion(
    set_count: int,
    intersection_size: Callable[[tuple[int, ...]], int],
) -> int:
    """用容斥原理计算编号为 0 到 set_count-1 的集合并集大小。

    参数：set_count 是集合数量；intersection_size 接收非空集合编号元组并返回其交集大小。
    返回：所有集合并集的精确基数。
    边界情况：set_count 为负或回调返回负交集大小时抛出 ValueError。
    关键算法点：一个元素若属于 r 个集合，会在 Σ(-1)^(k+1)C(r,k)=1 中恰好保留一次。
    """
    if set_count < 0:
        raise ValueError("set_count 不能为负数")
    union_size = 0
    indices = tuple(range(set_count))
    for subset_size in range(1, set_count + 1):
        sign = 1 if subset_size % 2 == 1 else -1
        for subset in combinations(indices, subset_size):
            size = intersection_size(subset)
            if size < 0:
                raise ValueError("交集大小不能为负数")
            # 同一层的所有交集具有相同符号，严格对应容斥公式的一项。
            union_size += sign * size
    return union_size


def multiples_union_count(limit: int, divisors: list[int]) -> int:
    """计算 1 到 limit 中能被至少一个给定正整数整除的整数个数。

    参数：limit 是闭区间上界；divisors 是非零正除数列表。
    返回：满足至少一个整除条件的整数数量。
    边界情况：limit 小于 1 返回 0；重复除数先去重，非正除数抛出 ValueError。
    关键算法点：多个整除条件的交集由其最小公倍数决定，再交给通用容斥函数。
    """
    if limit < 1:
        return 0
    if any(divisor <= 0 for divisor in divisors):
        raise ValueError("divisors 必须全部为正整数")
    unique_divisors = sorted(set(divisors))

    def intersection_size(subset: tuple[int, ...]) -> int:
        least_common_multiple = 1
        for index in subset:
            divisor = unique_divisors[index]
            greatest_common_divisor = _gcd(least_common_multiple, divisor)
            least_common_multiple = (
                least_common_multiple // greatest_common_divisor * divisor
            )
            if least_common_multiple > limit:
                return 0
        return limit // least_common_multiple

    return union_size_by_inclusion_exclusion(len(unique_divisors), intersection_size)


def _gcd(left: int, right: int) -> int:
    """返回两个非负整数的最大公因数，供最小公倍数计算使用。"""
    while right:
        left, right = right, left % right
    return left


if __name__ == "__main__":
    sets = [{1, 2, 3}, {3, 4}, {2, 4, 5}]
    assert (
        union_size_by_inclusion_exclusion(
            3, lambda chosen: len(set.intersection(*(sets[i] for i in chosen)))
        )
        == 5
    )
    assert union_size_by_inclusion_exclusion(0, lambda chosen: 0) == 0
    assert multiples_union_count(10, [2, 3]) == 7
    assert multiples_union_count(20, [2, 2, 5]) == 12
    assert multiples_union_count(0, [2]) == 0
    print("002_inclusion_exclusion: all examples passed")
