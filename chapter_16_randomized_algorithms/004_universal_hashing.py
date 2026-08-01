"""
通用哈希：从一族哈希函数中随机选择，降低固定输入导致大量冲突的风险。

本文件的意图：
1. 实现 Carter-Wegman 形式 h(x) = ((a*x + b) mod p) mod m。
2. 说明随机性来自哈希函数选择，而不是来自每次查询。
3. 提供一个简单链地址哈希表，展示通用哈希如何落到数据结构里。

约束：
- p 必须是大于 key 范围的素数；这里由调用方传入，避免把素性测试混进本文件。
- 表大小 m 应为正数。
"""

from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class UniversalHashFunction:
    """Carter-Wegman 通用哈希函数。"""

    a: int
    b: int
    prime: int
    bucket_count: int

    def __call__(self, key: int) -> int:
        """把非负整数 key 映射到 [0, bucket_count) 桶编号。"""

        if key < 0:
            raise ValueError("key 必须是非负整数")
        return ((self.a * key + self.b) % self.prime) % self.bucket_count


def build_universal_hash(
    bucket_count: int,
    prime: int,
    seed: int | None = None,
) -> UniversalHashFunction:
    """随机选择一个通用哈希函数。"""

    if bucket_count <= 0:
        raise ValueError("bucket_count 必须为正数")
    if prime <= bucket_count:
        raise ValueError("prime 应大于 bucket_count，通常还要大于最大 key")

    rng = Random(seed)
    a = rng.randint(1, prime - 1)
    b = rng.randint(0, prime - 1)
    return UniversalHashFunction(a, b, prime, bucket_count)


class ChainedHashSet:
    """基于通用哈希的整数集合。"""

    def __init__(self, bucket_count: int, prime: int, seed: int | None = None) -> None:
        """创建链地址哈希表。"""

        self.hash_function = build_universal_hash(bucket_count, prime, seed)
        self.buckets: list[list[int]] = [[] for _ in range(bucket_count)]

    def add(self, key: int) -> None:
        """插入 key；已存在时不重复插入。"""

        bucket = self.buckets[self.hash_function(key)]
        if key not in bucket:
            bucket.append(key)

    def contains(self, key: int) -> bool:
        """判断 key 是否在集合中。"""

        return key in self.buckets[self.hash_function(key)]

    def remove(self, key: int) -> bool:
        """删除 key；如果原本存在返回 True，否则返回 False。"""

        bucket = self.buckets[self.hash_function(key)]
        for index, value in enumerate(bucket):
            if value == key:
                bucket.pop(index)
                return True
        return False


if __name__ == "__main__":
    hash_fn = build_universal_hash(bucket_count=10, prime=101, seed=7)
    assert 0 <= hash_fn(42) < 10
    assert hash_fn(42) == hash_fn(42)

    table = ChainedHashSet(bucket_count=5, prime=101, seed=3)
    table.add(10)
    table.add(15)
    table.add(10)
    assert table.contains(10)
    assert table.contains(15)
    assert not table.contains(11)
    assert table.remove(10)
    assert not table.contains(10)
    assert not table.remove(10)

    print("004_universal_hashing: all examples passed")
