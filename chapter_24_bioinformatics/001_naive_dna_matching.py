"""
文件意图：手写实现 DNA 字符串的朴素精确模式匹配。
适用场景：短模式、教学中的基线比较，或需要枚举文本内全部精确命中起点的场景。
核心思想：让模式依次与文本每个可能起点对齐，逐字符比较，只有全部字符相同才记录该位置。
输入输出：输入文本 DNA 序列与模式 DNA 序列，输出全部零基命中起点。
时间复杂度：O((n-m+1)m)，空间复杂度 O(occurrences)。
关键边界情况：空模式在每个边界均匹配；模式长于文本无匹配；允许 N 作为未知碱基字面符号而非通配符。
"""

DNA_ALPHABET = frozenset("ACGTN")


def naive_dna_matches(sequence: str, pattern: str) -> list[int]:
    """找出 pattern 在 sequence 中全部不重叠限制之外的精确出现位置。

    参数：sequence 是待搜索 DNA 字符串；pattern 是待匹配 DNA 字符串。
    返回：每个精确匹配的零基起点，按升序排列。
    边界情况：空模式返回 0 到 len(sequence) 的所有边界；模式较长返回空列表。
    关键算法点：每次新对齐独立比较，不借助字符串查找库，作为其他算法的正确性基线。
    """
    _validate_dna(sequence, "sequence")
    _validate_dna(pattern, "pattern")
    if not pattern:
        return list(range(len(sequence) + 1))
    if len(pattern) > len(sequence):
        return []
    matches: list[int] = []
    for start in range(len(sequence) - len(pattern) + 1):
        # 比较完整窗口；一处不等即该起点不可能是精确命中。
        for offset, symbol in enumerate(pattern):
            if sequence[start + offset] != symbol:
                break
        else:
            matches.append(start)
    return matches


def _validate_dna(sequence: str, name: str) -> None:
    """验证教学示例使用的 DNA 字符串只含大写 A/C/G/T/N。"""
    if any(symbol not in DNA_ALPHABET for symbol in sequence):
        raise ValueError(f"{name} 只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    assert naive_dna_matches("ATATAT", "AT") == [0, 2, 4]
    assert naive_dna_matches("ACGTACGT", "CGT") == [1, 5]
    assert naive_dna_matches("ACGT", "TT") == []
    assert naive_dna_matches("AC", "") == [0, 1, 2]
    assert naive_dna_matches("A", "AC") == []
    print("001_naive_dna_matching: all examples passed")
