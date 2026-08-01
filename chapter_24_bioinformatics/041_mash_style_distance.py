"""Mash 风格 sketch 距离教学实现。

适用场景：用固定大小最小哈希 sketch 快速近似比较基因组序列距离。
核心思想：保留最小的若干 k-mer 哈希值，先估计 Jaccard，再用 Mash 的对数公式转换为距离。
输入输出：输入两条序列、k 和 sketch 大小；输出 sketch、Jaccard 和 Mash 风格距离。
时间复杂度：构建 sketch O(|k-mers| log s)，空间复杂度 O(s)。
关键边界情况：若 Jaccard 为 0，则距离上界截断为 1；完全相同序列距离为 0。
"""

from heapq import heappush, heapreplace
from math import log


DNA = frozenset("ACGTN")
COMPLEMENT = str.maketrans("ACGTN", "TGCAN")


def canonical_kmer(kmer: str) -> str:
    return min(kmer, kmer.translate(COMPLEMENT)[::-1])


def mash_sketch(sequence: str, k: int, sketch_size: int) -> list[int]:
    """保留最小的 sketch_size 个规范化 k-mer 哈希。"""

    _validate_dna(sequence)
    if k <= 0 or sketch_size <= 0:
        raise ValueError("k 和 sketch_size 必须为正整数")
    if len(sequence) < k:
        return []
    heap: list[int] = []
    seen: set[int] = set()
    for index in range(len(sequence) - k + 1):
        token = canonical_kmer(sequence[index : index + k])
        hashed = _stable_hash(token)
        if hashed in seen:
            continue
        seen.add(hashed)
        if len(heap) < sketch_size:
            heappush(heap, -hashed)
        elif hashed < -heap[0]:
            heapreplace(heap, -hashed)
    return sorted(-value for value in heap)


def sketch_jaccard(left: list[int], right: list[int]) -> float:
    """用 sketch 集合近似 Jaccard。"""

    left_set = set(left)
    right_set = set(right)
    if not left_set and not right_set:
        return 1.0
    if not left_set or not right_set:
        return 0.0
    intersection = len(left_set & right_set)
    union = len(left_set | right_set)
    return intersection / union


def mash_style_distance(left: str, right: str, k: int, sketch_size: int) -> float:
    """按 Mash 的 -1/k * ln(2j/(1+j)) 形式估计距离。"""

    jaccard = sketch_jaccard(
        mash_sketch(left, k, sketch_size), mash_sketch(right, k, sketch_size)
    )
    if jaccard <= 0:
        return 1.0
    if jaccard >= 1.0:
        return 0.0
    return max(0.0, min(1.0, -log((2 * jaccard) / (1 + jaccard)) / k))


def _stable_hash(token: str) -> int:
    value = 1469598103934665603
    for symbol in token:
        value ^= ord(symbol)
        value *= 1099511628211
        value &= (1 << 64) - 1
    return value


def _validate_dna(sequence: str) -> None:
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    left = mash_sketch("ACGTACGT", 3, 10)
    right = mash_sketch("ACGTACGT", 3, 10)
    assert left == right
    assert sketch_jaccard(left, right) == 1.0
    assert mash_style_distance("ACGTACGT", "ACGTACGT", 3, 10) == 0.0
    assert mash_style_distance("AAAAAA", "CCCCCC", 3, 10) == 1.0
    print("041_mash_style_distance: all examples passed")
