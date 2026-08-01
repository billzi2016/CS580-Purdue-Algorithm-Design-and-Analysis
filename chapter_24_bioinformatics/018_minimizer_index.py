"""DNA minimizer 抽样与倒排索引教学实现。

适用场景：从每个连续 k-mer 窗口中选择规范化字典序最小词，以稀疏方式建立短序列候选匹配索引。
核心思想：先将 k-mer 与其反向互补取较小者，再在每个含 w 个 k-mer 的窗口选最右最小项；相同位置不会重复输出。
输入输出：输入 DNA、k、窗口 k-mer 数 w；输出 minimizer 及其位置，并可建立键到参考位置的索引。
时间复杂度：本教学版 O(nw k)，空间复杂度 O(n)；工业实现会用单调队列达到线性扫描。
关键边界情况：N 没有反向互补定义而保留为 N；序列不足一个窗口返回空；并列时固定选择最右项。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")
COMPLEMENT = str.maketrans("ACGTN", "TGCAN")


@dataclass(frozen=True)
class Minimizer:
    """一个规范化 k-mer 抽样项及其在正向序列中的起点。"""

    position: int
    kmer: str


def reverse_complement(sequence: str) -> str:
    """返回大写 DNA 序列的反向互补。

    参数：sequence 为 A/C/G/T/N 序列。
    返回：互补后再反转的序列，N 保持 N。
    边界情况：空串合法；非法字符抛出 ValueError。
    关键算法点：先互补后反转与逐字符反向扫描等价，直接表达 DNA 双链的反向方向。
    """
    _validate_dna(sequence)
    return sequence.translate(COMPLEMENT)[::-1]


def canonical_kmer(kmer: str) -> str:
    """返回 k-mer 与其反向互补中字典序较小的规范表示。"""
    _validate_dna(kmer)
    return min(kmer, reverse_complement(kmer))


def minimizers(sequence: str, k: int, window_kmers: int) -> list[Minimizer]:
    """按固定的最右并列规则选择所有窗口 minimizer。

    参数：sequence 为 DNA，k 为 k-mer 长度，window_kmers 为一个窗口含有的 k-mer 数。
    返回：按位置升序、跨窗口去重的 minimizer 列表。
    边界情况：参数非正抛出 ValueError；不足 k+w-1 个字符时没有完整窗口。
    关键算法点：选择最右最小项保证窗口右移时并列选择稳定且可复现。
    """
    _validate_dna(sequence)
    if k <= 0 or window_kmers <= 0:
        raise ValueError("k 和 window_kmers 必须为正整数")
    kmers = [
        canonical_kmer(sequence[start : start + k])
        for start in range(max(0, len(sequence) - k + 1))
    ]
    if len(kmers) < window_kmers:
        return []
    selected: list[Minimizer] = []
    previous_position = -1
    for window_start in range(len(kmers) - window_kmers + 1):
        window = kmers[window_start : window_start + window_kmers]
        minimum = min(window)
        offset = max(index for index, word in enumerate(window) if word == minimum)
        position = window_start + offset
        if position != previous_position:
            selected.append(Minimizer(position, kmers[position]))
            previous_position = position
    return selected


def build_minimizer_index(
    reference: str, k: int, window_kmers: int
) -> dict[str, list[int]]:
    """从 reference 的 minimizer 建立键到全部参考位置的倒排索引。"""
    index: dict[str, list[int]] = {}
    for item in minimizers(reference, k, window_kmers):
        index.setdefault(item.kmer, []).append(item.position)
    return index


def _validate_dna(sequence: str) -> None:
    """校验大写 DNA/N 输入。"""
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    assert reverse_complement("ACGN") == "NCGT"
    assert canonical_kmer("GTT") == "AAC"
    selected = minimizers("ACGTAC", 2, 3)
    assert selected == [Minimizer(2, "AC"), Minimizer(4, "AC")]
    assert build_minimizer_index("ACGTAC", 2, 3) == {"AC": [2, 4]}
    assert minimizers("ACG", 2, 3) == []
    print("018_minimizer_index: all examples passed")
