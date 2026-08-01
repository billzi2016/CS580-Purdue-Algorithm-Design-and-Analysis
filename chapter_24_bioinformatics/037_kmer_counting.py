"""精确 k-mer 计数的教学实现。

适用场景：
- 需要统计一个或多个序列中所有长度为 k 的子串出现次数；
- 常见于组装、错误校正、覆盖度分析和 sketch 构造前的基础计数；
- 适合中小规模教学输入和验证性实验。

核心思想：
- 依次扫描每条序列的每个起点；
- 取出长度为 k 的窗口并累加到计数字典；
- 这是精确计数，不做 canonical k-mer 合并，也不做 probabilistic sketch 近似。

输入输出：
- 输入：序列列表和正整数 k；
- 输出：`k-mer -> 出现次数` 的字典。

时间复杂度：O(total_length * k)
空间复杂度：O(m * k)，其中 m 为不同 k-mer 数量。

关键边界情况：
- k 必须为正整数；
- 当序列长度小于 k 时，该序列贡献 0 个 k-mer；
- 空序列列表返回空字典；
- 本实现默认大小写敏感，并保留输入字符原样。
"""

from __future__ import annotations


def count_kmers(sequences: list[str], k: int) -> dict[str, int]:
    """精确统计多个序列中的 k-mer 次数。

    参数：
    - sequences：字符串序列列表；
    - k：k-mer 长度，必须为正整数。

    返回值：
    - 计数字典，键为 k-mer，值为出现次数。

    边界情况：
    - k 小于等于 0 时抛出异常；
    - 空序列、长度不足 k 的序列会被安全跳过。

    关键算法点：
    - 每个起点都要独立计数，因此重叠窗口会被保留；
    - 这是 exact counting，不做采样、不做近似压缩。
    """

    if k <= 0:
        raise ValueError("k 必须为正整数")

    counts: dict[str, int] = {}
    for sequence in sequences:
        if len(sequence) < k:
            continue
        for start in range(len(sequence) - k + 1):
            kmer = sequence[start : start + k]
            counts[kmer] = counts.get(kmer, 0) + 1
    return counts


if __name__ == "__main__":
    counts = count_kmers(["ATATA", "TAT"], 2)
    assert counts == {"AT": 3, "TA": 3}

    counts_three = count_kmers(["AAACAAA"], 3)
    assert counts_three["AAA"] == 2
    assert counts_three["AAC"] == 1

    assert count_kmers([], 3) == {}
    assert count_kmers(["A"], 2) == {}

    try:
        count_kmers(["ACGT"], 0)
        raise AssertionError("k=0 应抛出异常")
    except ValueError:
        pass

    print("037_kmer_counting: all examples passed")
