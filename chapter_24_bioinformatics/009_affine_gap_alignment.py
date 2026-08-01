"""教学版 affine-gap 全局序列比对。

适用场景：缺口打开与延长应有不同代价的短 DNA 序列全局比对。
核心思想：分别维护结尾为字符匹配、first 缺口、second 缺口的三个状态，避免把连续缺口重复收取打开罚分。
输入输出：输入两条 DNA 序列，输出最高全局比对分数；本文件不恢复对齐路径。
时间复杂度 O(nm)，空间复杂度 O(nm)。关键边界：空串允许；仅支持 A/C/G/T/N；这是教学版统一评分模型。
"""

NEGATIVE_INFINITY = -10**12
DNA = frozenset("ACGTN")


def affine_gap_alignment_score(first: str, second: str, match: int = 2, mismatch: int = -1, gap_open: int = -2, gap_extend: int = -1) -> int:
    """计算 affine-gap 评分下的最优全局比对分数。

    参数：first、second 为 DNA 序列；gap_open 是开启缺口代价，gap_extend 是延长既有缺口代价。
    返回：覆盖两条完整序列的最高分数。
    边界情况：空串只形成一个连续缺口；非法字符或正的缺口惩罚抛出 ValueError。
    关键算法点：X/Y 状态只能从自身延长或由 M 打开，故连续缺口只在第一次承担 gap_open。
    """
    if any(symbol not in DNA for symbol in first + second):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")
    if gap_open > 0 or gap_extend > 0:
        raise ValueError("缺口评分必须非正")
    rows, columns = len(first) + 1, len(second) + 1
    matched = [[NEGATIVE_INFINITY] * columns for _ in range(rows)]
    first_gap = [[NEGATIVE_INFINITY] * columns for _ in range(rows)]
    second_gap = [[NEGATIVE_INFINITY] * columns for _ in range(rows)]
    matched[0][0] = 0
    for row in range(1, rows):
        second_gap[row][0] = gap_open + (row - 1) * gap_extend
    for column in range(1, columns):
        first_gap[0][column] = gap_open + (column - 1) * gap_extend
    for row in range(1, rows):
        for column in range(1, columns):
            first_gap[row][column] = max(matched[row][column - 1] + gap_open, first_gap[row][column - 1] + gap_extend)
            second_gap[row][column] = max(matched[row - 1][column] + gap_open, second_gap[row - 1][column] + gap_extend)
            score = match if first[row - 1] == second[column - 1] else mismatch
            matched[row][column] = max(matched[row - 1][column - 1], first_gap[row - 1][column - 1], second_gap[row - 1][column - 1]) + score
    return max(matched[-1][-1], first_gap[-1][-1], second_gap[-1][-1])


if __name__ == "__main__":
    assert affine_gap_alignment_score("AC", "AC") == 4
    assert affine_gap_alignment_score("ACG", "AC") == 2
    assert affine_gap_alignment_score("", "AC") == -3
    assert affine_gap_alignment_score("AC", "TG") == -2
    print("009_affine_gap_alignment: all examples passed")
