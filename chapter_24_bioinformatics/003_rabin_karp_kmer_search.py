"""
文件意图：手写实现基于滚动哈希的 Rabin-Karp k-mer 精确搜索。
适用场景：在 DNA 序列中查找固定 k-mer，或需要从一个窗口快速更新到下一个窗口的教学场景。
核心思想：把字符映射到小整数并维护多项式哈希；窗口右移时删去最高位贡献、乘底数、加入新字符。
输入输出：输入 DNA 序列与非空 k-mer 模式，输出全部精确命中位置。
时间复杂度：平均 O(n+m)，哈希碰撞频繁时最坏 O(nm)；空间复杂度 O(occurrences)。
关键边界情况：模式为空拒绝，模式长于文本返回空；哈希相等后仍逐字符确认以保证结果精确。
"""

DNA_ALPHABET = frozenset("ACGTN")
DNA_VALUE = {"A": 1, "C": 2, "G": 3, "T": 4, "N": 5}
HASH_BASE = 7
HASH_MODULUS = 1_000_000_007


def rabin_karp_kmer_matches(sequence: str, kmer: str) -> list[int]:
    """在 sequence 中用滚动哈希查找 kmer 的全部精确出现位置。

    参数：sequence 是待搜索 DNA 字符串；kmer 是非空查询字符串。
    返回：按升序排列的零基命中位置。
    边界情况：空 k-mer 抛出 ValueError，k-mer 长于 sequence 返回空列表。
    关键算法点：哈希命中只作为候选，仍比较切片，以消除模哈希碰撞造成的假阳性。
    """
    _validate_dna(sequence, "sequence")
    _validate_dna(kmer, "kmer")
    if not kmer:
        raise ValueError("kmer 必须非空")
    pattern_length = len(kmer)
    if pattern_length > len(sequence):
        return []
    highest_power = pow(HASH_BASE, pattern_length - 1, HASH_MODULUS)
    pattern_hash = _hash(kmer)
    window_hash = _hash(sequence[:pattern_length])
    matches: list[int] = []
    for start in range(len(sequence) - pattern_length + 1):
        if (
            window_hash == pattern_hash
            and sequence[start : start + pattern_length] == kmer
        ):
            matches.append(start)
        if start + pattern_length == len(sequence):
            break
        outgoing = DNA_VALUE[sequence[start]]
        incoming = DNA_VALUE[sequence[start + pattern_length]]
        # 先去除最高次项，再左移一位并加入新字符，得到下一窗口哈希。
        window_hash = (window_hash - outgoing * highest_power) % HASH_MODULUS
        window_hash = (window_hash * HASH_BASE + incoming) % HASH_MODULUS
    return matches


def _hash(sequence: str) -> int:
    """按高位在前的多项式规则计算 DNA 字符串哈希。"""
    value = 0
    for symbol in sequence:
        value = (value * HASH_BASE + DNA_VALUE[symbol]) % HASH_MODULUS
    return value


def _validate_dna(sequence: str, name: str) -> None:
    """验证教学实现接受的大写 DNA 字母表。"""
    if any(symbol not in DNA_ALPHABET for symbol in sequence):
        raise ValueError(f"{name} 只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    assert rabin_karp_kmer_matches("ACGTACGTAC", "ACG") == [0, 4]
    assert rabin_karp_kmer_matches("AAAAA", "AAA") == [0, 1, 2]
    assert rabin_karp_kmer_matches("ACGT", "TT") == []
    assert rabin_karp_kmer_matches("AC", "ACG") == []
    try:
        rabin_karp_kmer_matches("AC", "")
        raise AssertionError("空 k-mer 应抛出 ValueError")
    except ValueError:
        pass
    print("003_rabin_karp_kmer_search: all examples passed")
