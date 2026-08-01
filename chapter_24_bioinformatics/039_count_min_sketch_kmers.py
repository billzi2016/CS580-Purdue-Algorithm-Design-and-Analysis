"""k-mer Count-Min Sketch 教学实现。

适用场景：在超大测序数据流中近似统计 k-mer 频次，接受“只高估不低估”的误差特性。
核心思想：用多组哈希函数把每个 k-mer 映射到多行计数器，查询时取各行最小值作为频次估计。
输入输出：输入 DNA 序列列表、k、sketch 宽度和深度；输出支持 update/query 的 sketch 结构。
时间复杂度：单次 update/query 为 O(depth)，空间复杂度为 O(width * depth)。
关键边界情况：本实现只接受大写 A/C/G/T/N；序列短于 k 时不产生任何 k-mer；估计值不会小于真实值。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")


def canonical_kmer(kmer: str) -> str:
    """返回 k-mer 与其反向互补中字典序较小的规范表示。"""

    complement = str.maketrans("ACGTN", "TGCAN")
    reverse = kmer.translate(complement)[::-1]
    return min(kmer, reverse)


def iter_kmers(sequence: str, k: int) -> list[str]:
    """枚举序列中的规范化 k-mer。"""

    _validate_dna(sequence)
    if k <= 0:
        raise ValueError("k 必须为正整数")
    if len(sequence) < k:
        return []
    return [
        canonical_kmer(sequence[index : index + k])
        for index in range(len(sequence) - k + 1)
    ]


@dataclass
class CountMinSketch:
    """Count-Min Sketch 计数结构。"""

    width: int
    depth: int

    def __post_init__(self) -> None:
        if self.width <= 0 or self.depth <= 0:
            raise ValueError("width 和 depth 必须为正整数")
        self.table = [[0] * self.width for _ in range(self.depth)]

    def update(self, token: str, count: int = 1) -> None:
        """把 token 的计数增加 count。"""

        if count < 0:
            raise ValueError("count 不能为负数")
        for row in range(self.depth):
            self.table[row][self._bucket(token, row)] += count

    def query(self, token: str) -> int:
        """返回 token 的频次估计。"""

        return min(
            self.table[row][self._bucket(token, row)] for row in range(self.depth)
        )

    def _bucket(self, token: str, row: int) -> int:
        """使用带 row 偏移的稳定哈希。"""

        seed = 1469598103934665603 + row * 1099511628211
        for symbol in token:
            seed ^= ord(symbol)
            seed *= 1099511628211
            seed &= (1 << 64) - 1
        return seed % self.width


def build_kmer_sketch(
    sequences: list[str], k: int, width: int, depth: int
) -> CountMinSketch:
    """从多条 DNA 序列构建 k-mer Count-Min Sketch。"""

    sketch = CountMinSketch(width, depth)
    for sequence in sequences:
        for kmer in iter_kmers(sequence, k):
            sketch.update(kmer)
    return sketch


def _validate_dna(sequence: str) -> None:
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    sketch = build_kmer_sketch(["ACGTAC", "ACGT"], 3, width=64, depth=4)
    exact = {}
    for kmer in iter_kmers("ACGTAC", 3) + iter_kmers("ACGT", 3):
        exact[kmer] = exact.get(kmer, 0) + 1
    for kmer, count in exact.items():
        assert sketch.query(kmer) >= count
    assert sketch.query("AAA") >= 0
    assert iter_kmers("AC", 3) == []
    print("039_count_min_sketch_kmers: all examples passed")
