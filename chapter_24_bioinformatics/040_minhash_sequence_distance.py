"""MinHash 序列距离教学实现。

适用场景：用 sketch 近似比较两条长序列的 k-mer Jaccard 相似度与距离。
核心思想：把序列映射成 k-mer 集合，再用多个哈希函数的最小值组成签名；签名相等比例近似 Jaccard。
输入输出：输入两条 DNA、k、签名长度；输出 MinHash 相似度与距离估计。
时间复杂度：构建签名 O(signature_size * |k-mers|)，空间复杂度 O(signature_size)。
关键边界情况：空 k-mer 集合之间的相似度定义为 1；一空一非空定义为 0；签名长度必须为正。
"""

DNA = frozenset("ACGTN")
COMPLEMENT = str.maketrans("ACGTN", "TGCAN")


def canonical_kmer(kmer: str) -> str:
    return min(kmer, kmer.translate(COMPLEMENT)[::-1])


def kmer_set(sequence: str, k: int) -> set[str]:
    """返回序列的规范化 k-mer 集合。"""

    _validate_dna(sequence)
    if k <= 0:
        raise ValueError("k 必须为正整数")
    if len(sequence) < k:
        return set()
    return {canonical_kmer(sequence[index : index + k]) for index in range(len(sequence) - k + 1)}


def minhash_signature(tokens: set[str], signature_size: int) -> list[int]:
    """为 token 集合构造 MinHash 签名。"""

    if signature_size <= 0:
        raise ValueError("signature_size 必须为正整数")
    if not tokens:
        return [0] * signature_size
    signature: list[int] = []
    for seed in range(signature_size):
        signature.append(min(_stable_hash(token, seed) for token in tokens))
    return signature


def minhash_similarity(left: str, right: str, k: int, signature_size: int) -> float:
    """估计两条序列的 Jaccard 相似度。"""

    left_tokens = kmer_set(left, k)
    right_tokens = kmer_set(right, k)
    if not left_tokens and not right_tokens:
        return 1.0
    if not left_tokens or not right_tokens:
        return 0.0
    left_signature = minhash_signature(left_tokens, signature_size)
    right_signature = minhash_signature(right_tokens, signature_size)
    matches = sum(1 for left_hash, right_hash in zip(left_signature, right_signature, strict=True) if left_hash == right_hash)
    return matches / signature_size


def minhash_distance(left: str, right: str, k: int, signature_size: int) -> float:
    """返回 1 - similarity。"""

    return 1.0 - minhash_similarity(left, right, k, signature_size)


def _stable_hash(token: str, seed: int) -> int:
    value = 2166136261 + seed * 16777619
    for symbol in token:
        value ^= ord(symbol)
        value *= 16777619
        value &= (1 << 64) - 1
    return value


def _validate_dna(sequence: str) -> None:
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    identical = minhash_similarity("ACGTACGT", "ACGTACGT", 3, 32)
    assert identical == 1.0
    different = minhash_similarity("AAAAAA", "CCCCCC", 3, 64)
    assert different == 0.0
    close = minhash_similarity("ACGTACGT", "ACGTTCGT", 3, 64)
    assert 0.0 < close < 1.0
    assert minhash_distance("ACGTACGT", "ACGTACGT", 3, 32) == 0.0
    print("040_minhash_sequence_distance: all examples passed")
