"""
文件意图：手写 Needleman-Wunsch 全局序列比对的动态规划与回溯恢复。
适用场景：需要端到端对齐两条短 DNA 序列，并采用统一匹配、失配、缺口评分的教学场景。
核心思想：dp[i][j] 是两个前缀的最高全局得分，最后一步只能是对角匹配/失配、删除或插入。
输入输出：输入两条 DNA 序列和评分参数，输出最高分及一组覆盖全部字符的对齐。
时间复杂度：O(nm)，空间复杂度 O(nm)，本教学版保留矩阵以恢复对齐。
关键边界情况：空序列以连续缺口对齐；N 按普通字面字符处理；不实现工业级替换矩阵或 affine gap。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class GlobalAlignment:
    """全局比对的分数与两条等长对齐字符串。"""

    score: int
    first: str
    second: str


def needleman_wunsch(
    first: str, second: str, match: int = 1, mismatch: int = -1, gap: int = -1
) -> GlobalAlignment:
    """计算两条 DNA 序列的一组最优全局比对。

    参数：first、second 为 DNA 序列；match、mismatch、gap 是统一整数评分。
    返回：最高得分和一组端到端对齐结果。
    边界情况：空序列合法；评分参数为任意整数；非法 DNA 字符抛出 ValueError。
    关键算法点：边界初始化为连续 gap 罚分，保证每个字符都必须在全局比对中被消费。
    """
    _validate(first)
    _validate(second)
    scores = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    for row in range(1, len(first) + 1):
        scores[row][0] = scores[row - 1][0] + gap
    for column in range(1, len(second) + 1):
        scores[0][column] = scores[0][column - 1] + gap
    for row in range(1, len(first) + 1):
        for column in range(1, len(second) + 1):
            diagonal = scores[row - 1][column - 1] + (
                match if first[row - 1] == second[column - 1] else mismatch
            )
            scores[row][column] = max(
                diagonal, scores[row - 1][column] + gap, scores[row][column - 1] + gap
            )
    return _backtrack(first, second, scores, match, mismatch, gap)


def _backtrack(
    first: str,
    second: str,
    scores: list[list[int]],
    match: int,
    mismatch: int,
    gap: int,
) -> GlobalAlignment:
    """从右下角回溯一条产生最优全局得分的路径。"""
    row, column = len(first), len(second)
    aligned_first: list[str] = []
    aligned_second: list[str] = []
    while row or column:
        if row and column:
            diagonal = scores[row - 1][column - 1] + (
                match if first[row - 1] == second[column - 1] else mismatch
            )
            if scores[row][column] == diagonal:
                aligned_first.append(first[row - 1])
                aligned_second.append(second[column - 1])
                row, column = row - 1, column - 1
                continue
        if row and scores[row][column] == scores[row - 1][column] + gap:
            aligned_first.append(first[row - 1])
            aligned_second.append("-")
            row -= 1
        else:
            aligned_first.append("-")
            aligned_second.append(second[column - 1])
            column -= 1
    return GlobalAlignment(
        scores[-1][-1],
        "".join(reversed(aligned_first)),
        "".join(reversed(aligned_second)),
    )


def _validate(sequence: str) -> None:
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    result = needleman_wunsch("GATTACA", "GCATGCU".replace("U", "T"))
    assert result.score == 0
    assert len(result.first) == len(result.second)
    assert result.first.replace("-", "") == "GATTACA"
    assert needleman_wunsch("", "AC").score == -2
    assert needleman_wunsch("AC", "AC").score == 2
    print("007_needleman_wunsch: all examples passed")
