"""
蓄水池抽样：从未知长度数据流中等概率抽取 k 个样本。

本文件的意图：
1. 展示流式算法如何在不知道总长度 n 的情况下保持均匀抽样。
2. 手写替换概率逻辑，不依赖 random.sample 对完整列表的一次性处理。
3. 支持任意可迭代对象，适合大文件、日志流、在线数据流等场景。

核心不变量：
处理完第 i 个元素后，前 i 个元素中每个元素出现在容量为 k 的水库中的概率都是
min(1, k / i)。
"""

from collections.abc import Iterable
from random import Random
from typing import TypeVar


T = TypeVar("T")


def reservoir_sample(stream: Iterable[T], k: int, seed: int | None = None) -> list[T]:
    """从 stream 中均匀抽取最多 k 个元素。

    如果数据流长度小于 k，则返回所有元素。函数只保存 k 个样本，因此空间复杂度
    是 O(k)，不随 stream 总长度增长。
    """

    if k < 0:
        raise ValueError("k 不能为负数")
    if k == 0:
        return []

    rng = Random(seed)
    reservoir: list[T] = []

    for count, item in enumerate(stream, start=1):
        if count <= k:
            reservoir.append(item)
            continue

        # 在 [1, count] 中随机选一个位置；只有落入前 k 个位置才替换。
        chosen_position = rng.randint(1, count)
        if chosen_position <= k:
            reservoir[chosen_position - 1] = item

    return reservoir


def weighted_reservoir_key(weight: float, random_value: float) -> float:
    """Efraimidis-Spirakis 加权抽样的单元素 key。

    这个函数不直接做完整加权水库，只提供关键公式：key = U^(1/w)。
    权重越大，key 越可能接近 1，因此越容易被保留。这里作为算法扩展点保留，
    便于后续实现加权 Top-k 水库。
    """

    if weight <= 0:
        raise ValueError("weight 必须为正数")
    if not 0 < random_value < 1:
        raise ValueError("random_value 必须在开区间 (0, 1) 内")
    return random_value ** (1.0 / weight)


if __name__ == "__main__":
    assert reservoir_sample([1, 2, 3], 5, seed=1) == [1, 2, 3]
    assert reservoir_sample(range(10), 0, seed=1) == []
    assert reservoir_sample(range(10), 3, seed=42) == [4, 1, 9]
    assert len(reservoir_sample((x * x for x in range(100)), 7, seed=3)) == 7
    assert round(weighted_reservoir_key(2.0, 0.25), 3) == 0.5

    print("003_reservoir_sampling: all examples passed")
