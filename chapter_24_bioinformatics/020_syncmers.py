"""闭合与开放 syncmer 的 DNA k-mer 选择教学实现。

适用场景：从 DNA 序列稀疏选择 k-mer，使选择由 k-mer 内部的 s-mer 位置决定，而非外部滑动窗口。
核心思想：对每个 k-mer 找字典序最小的 s-mer；闭合 syncmer 要求它在首或尾，开放 syncmer 要求它在指定内部位置。
输入输出：输入序列、k、s（及开放位置），输出选中的 k-mer、起点和最小 s-mer 的全部并列位置。
时间复杂度：O((n-k+1)(k-s+1)s)，空间复杂度 O(r)，r 为被选 k-mer 数。
关键边界情况：同一最小 s-mer 可在多处并列；k=s 时闭合模式会选择所有 k-mer；仅支持大写 A/C/G/T/N。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class Syncmer:
    """一个入选 k-mer 及其内部最小 s-mer 的所有 0-based 起点。"""

    position: int
    kmer: str
    smallest_smer: str
    smallest_positions: tuple[int, ...]


def closed_syncmers(sequence: str, k: int, s: int) -> list[Syncmer]:
    """选择内部最小 s-mer 位于首端或尾端的闭合 syncmer。

    参数：sequence 为 DNA；k 是 k-mer 长度；s 满足 1 <= s <= k。
    返回：按序列起点升序的闭合 syncmer。
    边界情况：没有完整 k-mer 时返回空；最小 s-mer 并列时只要任一端点出现即选中。
    关键算法点：是否选中只取决于当前 k-mer 的内容，使相同 k-mer 在不同上下文中有一致选择结果。
    """
    return _select_syncmers(sequence, k, s, allowed_positions=None)


def open_syncmers(sequence: str, k: int, s: int, allowed_positions: set[int]) -> list[Syncmer]:
    """选择内部最小 s-mer 出现在指定位置集合的开放 syncmer。

    参数：allowed_positions 是 k-mer 内 s-mer 的 0-based 起点集合。
    返回：符合任一指定位置的 syncmer。
    边界情况：位置集合为空返回空；越过 0..k-s 的位置抛出 ValueError。
    关键算法点：并列最小 s-mer 采用“任何允许位置命中即选择”，避免任意破坏平局带来的上下文依赖。
    """
    _validate_parameters(sequence, k, s)
    maximum_position = k - s
    if any(position < 0 or position > maximum_position for position in allowed_positions):
        raise ValueError("开放 syncmer 位置必须在 0 到 k-s 之间")
    return _select_syncmers(sequence, k, s, allowed_positions)


def smallest_smer_positions(kmer: str, s: int) -> tuple[str, tuple[int, ...]]:
    """返回 k-mer 的最小 s-mer 及其全部起点。

    参数：kmer 是 DNA；s 为正且不超过 kmer 长度。
    返回：字典序最小 s-mer 与出现该最小值的 0-based 位置元组。
    边界情况：非法 DNA、s 不合法均抛出 ValueError。
    关键算法点：保留全部平局位置，闭合和开放选择均不能只依赖一个任意平局代表。
    """
    _validate_dna(kmer)
    if s <= 0 or s > len(kmer):
        raise ValueError("s 必须满足 1 <= s <= len(kmer)")
    words = [kmer[start : start + s] for start in range(len(kmer) - s + 1)]
    smallest = min(words)
    return smallest, tuple(start for start, word in enumerate(words) if word == smallest)


def _select_syncmers(sequence: str, k: int, s: int, allowed_positions: set[int] | None) -> list[Syncmer]:
    """实现两类 syncmer 共享的扫描与平局处理。"""
    _validate_parameters(sequence, k, s)
    selected: list[Syncmer] = []
    for position in range(max(0, len(sequence) - k + 1)):
        kmer = sequence[position : position + k]
        smallest, positions = smallest_smer_positions(kmer, s)
        if allowed_positions is None:
            choose = 0 in positions or k - s in positions
        else:
            choose = any(candidate in allowed_positions for candidate in positions)
        if choose:
            selected.append(Syncmer(position, kmer, smallest, positions))
    return selected


def _validate_parameters(sequence: str, k: int, s: int) -> None:
    """验证 DNA 与 k/s 关系，所有公开选择函数复用该边界检查。"""
    _validate_dna(sequence)
    if k <= 0 or s <= 0 or s > k:
        raise ValueError("必须满足 1 <= s <= k")


def _validate_dna(sequence: str) -> None:
    """限制输入为大写 DNA 教学字母表。"""
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    assert smallest_smer_positions("AACGA", 2) == ("AA", (0,))
    assert smallest_smer_positions("AAAA", 2) == ("AA", (0, 1, 2))
    assert [(item.position, item.kmer) for item in closed_syncmers("AACGAT", 4, 2)] == [(0, "AACG"), (1, "ACGA"), (2, "CGAT")]
    assert [(item.position, item.kmer) for item in open_syncmers("CAGT", 4, 2, {1})] == [(0, "CAGT")]
    assert closed_syncmers("AC", 3, 1) == []
    try:
        open_syncmers("ACGT", 3, 2, {2})
        raise AssertionError("应拒绝越界开放位置")
    except ValueError:
        pass
    print("020_syncmers: all examples passed")
