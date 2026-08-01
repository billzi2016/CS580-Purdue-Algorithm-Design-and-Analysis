"""
文件意图：手写 Smith-Waterman 局部序列比对的动态规划与最优片段回溯。
适用场景：希望在两条短 DNA 序列中寻找最高分相似局部片段的教学场景。
核心思想：dp[i][j] 允许重置为 0，因此最优局部对齐可从任意位置开始和结束；从全矩阵最大格回溯至 0。
输入输出：输入两条 DNA 序列和评分参数，输出最高局部分数、对齐片段及其零基区间。
时间复杂度：O(nm)，空间复杂度 O(nm)，教学版保存全部矩阵以恢复路径。
关键边界情况：无正得分匹配时返回空对齐；N 按字面字符处理；不提供统计显著性或工业级索引。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class LocalAlignment:
    """局部比对的得分、对齐片段和原序列半开区间。"""

    score: int
    first: str
    second: str
    first_interval: tuple[int, int]
    second_interval: tuple[int, int]


def smith_waterman(first: str, second: str, match: int = 2, mismatch: int = -1, gap: int = -1) -> LocalAlignment:
    """计算一组最高分局部 DNA 序列比对。

    参数：first、second 是 DNA 序列；其余为统一整数评分。
    返回：最高局部分数、对齐串和各自的原串半开区间。
    边界情况：空串或无正分匹配返回零分空对齐；非法字符抛出 ValueError。
    关键算法点：每格与 0 取最大值切断负贡献前缀，故回溯至零格即为局部起点。
    """
    _validate(first)
    _validate(second)
    scores = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    best_score = 0
    best_cell = (0, 0)
    for row in range(1, len(first) + 1):
        for column in range(1, len(second) + 1):
            diagonal = scores[row - 1][column - 1] + (match if first[row - 1] == second[column - 1] else mismatch)
            scores[row][column] = max(0, diagonal, scores[row - 1][column] + gap, scores[row][column - 1] + gap)
            if scores[row][column] > best_score:
                best_score, best_cell = scores[row][column], (row, column)
    return _backtrack(first, second, scores, best_score, best_cell, match, mismatch, gap)


def _backtrack(first: str, second: str, scores: list[list[int]], best_score: int, best_cell: tuple[int, int], match: int, mismatch: int, gap: int) -> LocalAlignment:
    row, column = best_cell
    end = (row, column)
    aligned_first: list[str] = []
    aligned_second: list[str] = []
    while row and column and scores[row][column]:
        diagonal = scores[row - 1][column - 1] + (match if first[row - 1] == second[column - 1] else mismatch)
        if scores[row][column] == diagonal:
            aligned_first.append(first[row - 1]); aligned_second.append(second[column - 1]); row, column = row - 1, column - 1
        elif scores[row][column] == scores[row - 1][column] + gap:
            aligned_first.append(first[row - 1]); aligned_second.append("-"); row -= 1
        else:
            aligned_first.append("-"); aligned_second.append(second[column - 1]); column -= 1
    return LocalAlignment(best_score, "".join(reversed(aligned_first)), "".join(reversed(aligned_second)), (row, end[0]), (column, end[1]))


def _validate(sequence: str) -> None:
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    result = smith_waterman("ACCGT", "CCG")
    assert result.score == 6 and result.first == result.second == "CCG"
    assert result.first_interval == (1, 4)
    assert smith_waterman("AAA", "TTT").score == 0
    assert smith_waterman("", "AC").first == ""
    print("008_smith_waterman: all examples passed")
