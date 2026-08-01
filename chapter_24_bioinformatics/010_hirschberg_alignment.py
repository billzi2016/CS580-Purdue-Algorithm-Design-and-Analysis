"""教学版 Hirschberg 全局序列比对。

适用场景：为两条 DNA 序列恢复一组统一评分的最优端到端对齐，同时避免保存完整 DP 表。
核心思想：用正向和反向的两行 DP 找到最优路径穿过中间行的位置，再递归处理两个子问题。
输入输出：输入 DNA 序列与 match/mismatch/gap 分数，返回最优分数和等长的两条对齐序列。
时间复杂度：O(nm)；工作空间为 O(min(n, m))，不计递归调用与最终输出字符串。
关键边界情况：空序列、单字符子问题及多条最优路径均合法；本教学版不支持 affine gap 或替换矩阵。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class HirschbergAlignment:
    """保存全局对齐分数及一组等长对齐字符串。"""

    score: int
    first: str
    second: str


def hirschberg_alignment(first: str, second: str, match: int = 1, mismatch: int = -1, gap: int = -1) -> HirschbergAlignment:
    """在线性 DP 工作空间内恢复一组最优全局比对。

    参数：first、second 为仅含 A/C/G/T/N 的序列；其余参数是统一整数评分。
    返回：最优分数及覆盖原始两序列的一组对齐。
    边界情况：任一序列为空时以连续 gap 对齐；非法字符抛出 ValueError。
    关键算法点：将较短的序列置于 DP 列方向，保证每次行向量只占 O(min(n,m)) 空间。
    """
    _validate(first)
    _validate(second)
    # 交换后须把输出列顺序再交换，但可确保所有行向量都以较短序列为宽度。
    if len(second) > len(first):
        reversed_result = _align(second, first, match, mismatch, gap)
        return HirschbergAlignment(reversed_result.score, reversed_result.second, reversed_result.first)
    return _align(first, second, match, mismatch, gap)


def _align(first: str, second: str, match: int, mismatch: int, gap: int) -> HirschbergAlignment:
    """递归分治恢复对齐；调用者保证 second 不比 first 长。"""
    if not first:
        return HirschbergAlignment(len(second) * gap, "-" * len(second), second)
    if not second:
        return HirschbergAlignment(len(first) * gap, first, "-" * len(first))
    if len(first) == 1:
        return _single_row_alignment(first, second, match, mismatch, gap)

    middle = len(first) // 2
    forward = _last_score_row(first[:middle], second, match, mismatch, gap)
    backward = _last_score_row(first[middle:][::-1], second[::-1], match, mismatch, gap)
    # 每个候选列代表一条经由 (middle, column) 的完整路径；取第一个以保持确定性。
    split = max(range(len(second) + 1), key=lambda column: forward[column] + backward[len(second) - column])
    left = _align(first[:middle], second[:split], match, mismatch, gap)
    right = _align(first[middle:], second[split:], match, mismatch, gap)
    return HirschbergAlignment(left.score + right.score, left.first + right.first, left.second + right.second)


def _last_score_row(first: str, second: str, match: int, mismatch: int, gap: int) -> list[int]:
    """返回常规全局比对 DP 的最后一行，整个过程只保留一行。"""
    previous = [column * gap for column in range(len(second) + 1)]
    for row, symbol in enumerate(first, start=1):
        current = [row * gap]
        for column, other in enumerate(second, start=1):
            diagonal = previous[column - 1] + (match if symbol == other else mismatch)
            current.append(max(diagonal, previous[column] + gap, current[column - 1] + gap))
        previous = current
    return previous


def _single_row_alignment(first: str, second: str, match: int, mismatch: int, gap: int) -> HirschbergAlignment:
    """用小型完整 DP 解决递归基例，以同时返回合法路径而非只返回分数。"""
    scores = [[0] * (len(second) + 1) for _ in range(2)]
    for column in range(1, len(second) + 1):
        scores[0][column] = scores[0][column - 1] + gap
    scores[1][0] = gap
    for column, symbol in enumerate(second, start=1):
        scores[1][column] = max(
            scores[0][column - 1] + (match if first == symbol else mismatch),
            scores[0][column] + gap,
            scores[1][column - 1] + gap,
        )
    row, column = 1, len(second)
    aligned_first: list[str] = []
    aligned_second: list[str] = []
    while row or column:
        if row and column and scores[row][column] == scores[row - 1][column - 1] + (match if first == second[column - 1] else mismatch):
            aligned_first.append(first)
            aligned_second.append(second[column - 1])
            row, column = 0, column - 1
        elif row and scores[row][column] == scores[row - 1][column] + gap:
            aligned_first.append(first)
            aligned_second.append("-")
            row -= 1
        else:
            aligned_first.append("-")
            aligned_second.append(second[column - 1])
            column -= 1
    return HirschbergAlignment(scores[1][-1], "".join(reversed(aligned_first)), "".join(reversed(aligned_second)))


def _validate(sequence: str) -> None:
    """拒绝教学范围外的字符，避免把小写或蛋白质序列静默当作 DNA。"""
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    result = hirschberg_alignment("GATTACA", "GCATGCA")
    assert result.score == 2
    assert result.first.replace("-", "") == "GATTACA"
    assert result.second.replace("-", "") == "GCATGCA"
    assert len(result.first) == len(result.second)
    assert hirschberg_alignment("", "AC").score == -2
    assert hirschberg_alignment("A", "G").score == -1
    print("010_hirschberg_alignment: all examples passed")
