"""FASTA 风格的 k-tuple 种子查找教学实现。

适用场景：为短 DNA 查询序列建立 k-mer 查询表，在目标序列中找相同词并按对角线聚合。
核心思想：同一对角线上的精确 k-mer 命中暗示无缺口局部相似区域；这里只实现候选对角线生成，不做 FASTA 后续重评分。
输入输出：输入 query、target、词长 k，输出每条对角线的种子命中及连续命中统计。
时间复杂度：O(q+t+h)，其中 h 是命中数；空间复杂度 O(q+h)。
关键边界情况：空序列、k 大于序列长度、重复 k-mer 与非法 DNA 字符均明确处理。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class SeedHit:
    """一个查询和目标的精确 k-mer 命中，diagonal=target_start-query_start。"""

    query_start: int
    target_start: int
    kmer: str

    @property
    def diagonal(self) -> int:
        """返回同一无缺口对齐所共有的对角线编号。"""
        return self.target_start - self.query_start


@dataclass(frozen=True)
class DiagonalCandidate:
    """聚合到同一对角线的种子及相邻种子最多连续个数。"""

    diagonal: int
    hits: tuple[SeedHit, ...]
    longest_adjacent_run: int


def fasta_style_seed_lookup(query: str, target: str, k: int) -> list[DiagonalCandidate]:
    """手写查询 k-tuple 表并按目标扫描命中，形成 FASTA 风格候选对角线。

    参数：query、target 为 DNA 序列，k 为正整数种子长度。
    返回：按命中数、连续程度、对角线编号确定性排序的候选列表。
    边界情况：任意序列长度小于 k 时返回空列表；非法字符或非正 k 抛出 ValueError。
    关键算法点：查询表保存一个 k-mer 的全部位置，不能覆盖重复出现的词。
    """
    _validate_dna(query)
    _validate_dna(target)
    if k <= 0:
        raise ValueError("k 必须为正整数")
    if len(query) < k or len(target) < k:
        return []
    query_table = _build_query_table(query, k)
    grouped: dict[int, list[SeedHit]] = {}
    for target_start in range(len(target) - k + 1):
        word = target[target_start : target_start + k]
        for query_start in query_table.get(word, []):
            hit = SeedHit(query_start, target_start, word)
            grouped.setdefault(hit.diagonal, []).append(hit)
    candidates = [
        DiagonalCandidate(diagonal, tuple(hits), _longest_adjacent_run(hits, k))
        for diagonal, hits in grouped.items()
    ]
    return sorted(
        candidates,
        key=lambda item: (-len(item.hits), -item.longest_adjacent_run, item.diagonal),
    )


def _build_query_table(query: str, k: int) -> dict[str, list[int]]:
    """建立 k-mer 到全部查询起点的倒排表，保留重复种子。"""
    table: dict[str, list[int]] = {}
    for start in range(len(query) - k + 1):
        table.setdefault(query[start : start + k], []).append(start)
    return table


def _longest_adjacent_run(hits: list[SeedHit], k: int) -> int:
    """计算同对角线上相邻或重叠命中的最长链，反映一段连续的词命中。"""
    if not hits:
        return 0
    ordered = sorted(hits, key=lambda hit: hit.query_start)
    best = current = 1
    previous = ordered[0]
    for hit in ordered[1:]:
        # 对角线相同意味着两个坐标同步增长；间隔不超过 k 则两段词相接或重叠。
        if hit.query_start - previous.query_start <= k:
            current += 1
        else:
            current = 1
        best = max(best, current)
        previous = hit
    return best


def _validate_dna(sequence: str) -> None:
    """限制为大写 DNA 教学字母表，避免隐式混入蛋白质或小写规则。"""
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    candidates = fasta_style_seed_lookup("ACGACG", "TTACGACGA", 3)
    assert candidates[0].diagonal == 2
    assert [(hit.query_start, hit.target_start) for hit in candidates[0].hits] == [
        (0, 2),
        (1, 3),
        (2, 4),
        (3, 5),
    ]
    assert candidates[0].longest_adjacent_run == 4
    assert fasta_style_seed_lookup("AC", "ACGT", 3) == []
    assert fasta_style_seed_lookup("AAAA", "AAAAA", 2)[0].diagonal == 0
    print("015_fasta_seed_lookup: all examples passed")
