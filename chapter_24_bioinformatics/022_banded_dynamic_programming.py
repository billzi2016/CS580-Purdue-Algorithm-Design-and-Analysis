"""带状动态规划的全局 DNA 编辑距离与路径恢复教学实现。

适用场景：已知两序列最优全局比对接近主对角线时，以固定带宽减少普通 O(nm) DP 的访问范围。
核心思想：第 i 行仅计算 |i-j|<=band 的单元；带外单元视为不可达，回溯时只沿实际计算的最优前驱移动。
输入输出：输入两条 DNA 和 band，返回编辑距离及一组 M/X/I/D 操作；无带内路径返回 None。
时间复杂度 O((n+m)band)，空间复杂度 O((n+m)band)（为恢复路径保留带内字典）。
关键边界情况：长度差大于 band 必不可达；空串合法；本教学版采用单位替换/插入/删除代价。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")
INF = 10**12


@dataclass(frozen=True)
class BandedAlignment:
    """带内最优编辑距离和从左到右的操作串。"""

    distance: int
    operations: str


def banded_global_alignment(
    first: str, second: str, band: int
) -> BandedAlignment | None:
    """在主对角线两侧 band 宽度内计算全局编辑距离并恢复一条路径。

    参数：first、second 是 DNA；band 为非负对角线半宽。
    返回：带内最优结果，若所有全局路径均离开带则返回 None。
    边界情况：长度差超过 band 立即返回 None；非法 DNA 或负带宽抛出 ValueError。
    关键算法点：只存储 j 的合法带区间，缺失字典键即表示带外不可达而非零代价。
    """
    _validate(first)
    _validate(second)
    if band < 0:
        raise ValueError("band 必须非负")
    if abs(len(first) - len(second)) > band:
        return None
    scores: dict[tuple[int, int], int] = {(0, 0): 0}
    parents: dict[tuple[int, int], str] = {}
    for row in range(len(first) + 1):
        low, high = max(0, row - band), min(len(second), row + band)
        for column in range(low, high + 1):
            if row == 0 and column == 0:
                continue
            candidates: list[tuple[int, str]] = []
            if row and column and (row - 1, column - 1) in scores:
                candidates.append(
                    (
                        scores[(row - 1, column - 1)]
                        + (first[row - 1] != second[column - 1]),
                        "M" if first[row - 1] == second[column - 1] else "X",
                    )
                )
            if row and (row - 1, column) in scores:
                candidates.append((scores[(row - 1, column)] + 1, "D"))
            if column and (row, column - 1) in scores:
                candidates.append((scores[(row, column - 1)] + 1, "I"))
            if candidates:
                # 相同代价按对角、删除、插入的加入顺序定向，便于结果可复现。
                scores[(row, column)], parents[(row, column)] = min(
                    candidates, key=lambda item: item[0]
                )
    endpoint = (len(first), len(second))
    if endpoint not in scores:
        return None
    operations: list[str] = []
    row, column = endpoint
    while row or column:
        operation = parents[(row, column)]
        operations.append(operation)
        if operation in "MX":
            row, column = row - 1, column - 1
        elif operation == "D":
            row -= 1
        else:
            column -= 1
    return BandedAlignment(scores[endpoint], "".join(reversed(operations)))


def _validate(sequence: str) -> None:
    """限制为大写 DNA 教学字母表。"""
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    assert banded_global_alignment("ACGT", "ACGT", 0) == BandedAlignment(0, "MMMM")
    assert banded_global_alignment("ACGT", "AGGT", 1) == BandedAlignment(1, "MXMM")
    assert banded_global_alignment("ACGT", "ACG", 1).distance == 1
    assert banded_global_alignment("ACGT", "AC", 1) is None
    assert banded_global_alignment("", "AC", 2) == BandedAlignment(2, "II")
    print("022_banded_dynamic_programming: all examples passed")
