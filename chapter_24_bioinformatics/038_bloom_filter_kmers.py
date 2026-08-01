"""用于 k-mer 集合查询的 Bloom Filter 教学实现。

适用场景：
- 需要用很小内存表示一个 k-mer 集合；
- 允许“可能存在”的假阳性，但不能漏掉已插入元素；
- 常见于大规模 reads 预过滤、图构建前 membership test 等场景。

核心思想：
- 使用长度固定的 bit array；
- 每个 k-mer 经多个独立哈希位置映射并置位；
- 查询时只要有一位为 0 就一定不存在；全部为 1 只能说明“可能存在”。

输入输出：
- 输入：bit 数组大小、哈希函数数量，以及待插入的 k-mer；
- 输出：支持插入、查询和从序列批量构建的 Bloom Filter 对象。

时间复杂度：
- 单次插入 / 查询均为 O(h)，其中 h 是哈希函数数量。

空间复杂度：O(m)，其中 m 是 bit 数组大小。

关键边界情况：
- bit 数组大小和哈希函数数量都必须为正；
- 本实现使用确定性 SHA-256 双重哈希，不依赖 Python 进程内置随机 hash；
- 这是 probabilistic membership 结构，不提供精确计数。
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass
class BloomFilter:
    """简单 Bloom Filter。"""

    bit_size: int
    hash_count: int

    def __post_init__(self) -> None:
        """初始化底层 bit array 并校验参数。"""

        if self.bit_size <= 0:
            raise ValueError("bit_size 必须为正整数")
        if self.hash_count <= 0:
            raise ValueError("hash_count 必须为正整数")
        self.bits = [0] * self.bit_size

    def add(self, item: str) -> None:
        """把一个元素插入 Bloom Filter。"""

        for position in self._positions(item):
            self.bits[position] = 1

    def contains(self, item: str) -> bool:
        """判断元素是否“可能存在”。"""

        return all(self.bits[position] == 1 for position in self._positions(item))

    @classmethod
    def from_sequences(
        cls,
        sequences: list[str],
        k: int,
        bit_size: int,
        hash_count: int,
    ) -> BloomFilter:
        """从序列集合中提取 k-mer 并构建 Bloom Filter。"""

        if k <= 0:
            raise ValueError("k 必须为正整数")

        bloom_filter = cls(bit_size=bit_size, hash_count=hash_count)
        for sequence in sequences:
            for start in range(len(sequence) - k + 1):
                bloom_filter.add(sequence[start : start + k])
        return bloom_filter

    def _positions(self, item: str) -> list[int]:
        """用双重哈希生成多个 bit 位置。"""

        encoded = item.encode("utf-8")
        first_hash = int.from_bytes(hashlib.sha256(b"seed1|" + encoded).digest(), "big")
        second_hash = int.from_bytes(
            hashlib.sha256(b"seed2|" + encoded).digest(), "big"
        )
        second_hash = second_hash or 1

        return [
            (first_hash + index * second_hash) % self.bit_size
            for index in range(self.hash_count)
        ]


if __name__ == "__main__":
    bloom = BloomFilter.from_sequences(
        sequences=["ATATA", "CGCG"],
        k=2,
        bit_size=97,
        hash_count=4,
    )
    assert bloom.contains("AT")
    assert bloom.contains("TA")
    assert bloom.contains("CG")
    assert bloom.contains("GC")
    assert not bloom.contains("TT")

    manual = BloomFilter(bit_size=31, hash_count=3)
    manual.add("AAA")
    manual.add("CCC")
    assert manual.contains("AAA")
    assert manual.contains("CCC")

    try:
        BloomFilter(bit_size=0, hash_count=2)
        raise AssertionError("非法 bit_size 应抛出异常")
    except ValueError:
        pass

    try:
        BloomFilter.from_sequences(["ACGT"], k=0, bit_size=31, hash_count=2)
        raise AssertionError("k=0 应抛出异常")
    except ValueError:
        pass

    print("038_bloom_filter_kmers: all examples passed")
