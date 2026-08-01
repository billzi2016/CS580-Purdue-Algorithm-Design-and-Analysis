"""
文件意图：手写实现 KMP DNA 精确匹配及模式的前缀函数预处理。
适用场景：长序列上重复搜索同一模式，或含大量自重叠模式时避免朴素算法反复比较文本字符。
核心思想：前缀函数记录每个模式前缀的最长真前后缀长度，失配后保留已知可复用的匹配信息。
输入输出：输入 DNA 文本和模式，输出全部零基精确命中位置。
时间复杂度：预处理 O(m)，搜索 O(n)，总计 O(n+m)；空间复杂度 O(m)。
关键边界情况：空模式匹配所有边界；模式长于文本无命中；N 仅被当作普通字面字符。
"""

DNA_ALPHABET = frozenset("ACGTN")


def prefix_function(pattern: str) -> list[int]:
    """计算 KMP 所需的最长真前后缀长度数组。

    参数：pattern 是仅含允许 DNA 字符的模式串。
    返回：pi[i] 是 pattern[:i+1] 的最长真前缀且也是后缀的长度。
    边界情况：空串返回空列表。
    关键算法点：失配时沿 pi 回退，而不重新检查已知相等的前缀部分。
    """
    _validate_dna(pattern, "pattern")
    prefix_lengths = [0] * len(pattern)
    matched_length = 0
    for index in range(1, len(pattern)):
        while matched_length and pattern[index] != pattern[matched_length]:
            matched_length = prefix_lengths[matched_length - 1]
        if pattern[index] == pattern[matched_length]:
            matched_length += 1
        prefix_lengths[index] = matched_length
    return prefix_lengths


def kmp_dna_matches(sequence: str, pattern: str) -> list[int]:
    """使用 KMP 找出 pattern 在 sequence 中的全部精确命中。

    参数：sequence 是待查找 DNA 字符串；pattern 是查询 DNA 字符串。
    返回：按升序排列的全部零基命中起点。
    边界情况：空模式返回所有边界，模式较长返回空列表。
    关键算法点：文本指针从不回退，失配只依据前缀函数缩短当前已匹配模式长度。
    """
    _validate_dna(sequence, "sequence")
    _validate_dna(pattern, "pattern")
    if not pattern:
        return list(range(len(sequence) + 1))
    prefix_lengths = prefix_function(pattern)
    matches: list[int] = []
    matched_length = 0
    for index, symbol in enumerate(sequence):
        while matched_length and symbol != pattern[matched_length]:
            matched_length = prefix_lengths[matched_length - 1]
        if symbol == pattern[matched_length]:
            matched_length += 1
        if matched_length == len(pattern):
            matches.append(index - len(pattern) + 1)
            # 命中后同样回退，才能保留重叠命中的候选前缀。
            matched_length = prefix_lengths[matched_length - 1]
    return matches


def _validate_dna(sequence: str, name: str) -> None:
    """验证教学实现接受的大写 DNA 字母表。"""
    if any(symbol not in DNA_ALPHABET for symbol in sequence):
        raise ValueError(f"{name} 只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    assert prefix_function("ATAT") == [0, 0, 1, 2]
    assert kmp_dna_matches("ATATAT", "ATAT") == [0, 2]
    assert kmp_dna_matches("ACGTACGT", "CGT") == [1, 5]
    assert kmp_dna_matches("ACGT", "TT") == []
    assert kmp_dna_matches("AC", "") == [0, 1, 2]
    print("002_kmp_dna_matching: all examples passed")
