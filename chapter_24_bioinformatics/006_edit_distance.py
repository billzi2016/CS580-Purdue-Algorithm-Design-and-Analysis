"""
文件意图：手写 Levenshtein 编辑距离动态规划，并恢复一种最短编辑操作序列。
适用场景：允许插入、删除、替换的短 DNA 序列差异计数；这是比 Hamming 距离更一般的基础模型。
核心思想：dp[i][j] 是两个前缀的最小编辑数，最后一步必为删除、插入或匹配/替换三者之一。
输入输出：输入两条 DNA 序列，输出最小编辑距离或一种最短编辑操作名序列。
时间复杂度：O(nm)，空间复杂度 O(nm)，以支持回溯恢复操作。
关键边界情况：任一空串的距离是另一串长度；N 视为普通字面字符，不代表模糊匹配。
"""

DNA_ALPHABET = frozenset("ACGTN")


def edit_distance(first: str, second: str) -> int:
    """计算把 first 变换为 second 所需的最少插入、删除、替换次数。"""
    table = _distance_table(first, second)
    return table[len(first)][len(second)]


def shortest_edit_operations(first: str, second: str) -> list[str]:
    """恢复一种从 first 到 second 的最短编辑操作类型序列。

    参数：first、second 是大写 DNA 序列。
    返回：由 match、replace、delete、insert 组成的操作列表。
    边界情况：两空串返回空列表；若一方为空则全部为另一种单类编辑。
    关键算法点：从右下角沿生成最优 dp 值的前驱回溯，每一步都使剩余最优值减少或保持匹配关系。
    """
    table = _distance_table(first, second)
    row, column = len(first), len(second)
    operations: list[str] = []
    while row or column:
        if row and column and first[row - 1] == second[column - 1] and table[row][column] == table[row - 1][column - 1]:
            operations.append("match")
            row, column = row - 1, column - 1
        elif row and column and table[row][column] == table[row - 1][column - 1] + 1:
            operations.append("replace")
            row, column = row - 1, column - 1
        elif row and table[row][column] == table[row - 1][column] + 1:
            operations.append("delete")
            row -= 1
        else:
            operations.append("insert")
            column -= 1
    return list(reversed(operations))


def _distance_table(first: str, second: str) -> list[list[int]]:
    _validate_dna(first)
    _validate_dna(second)
    table = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    for row in range(len(first) + 1):
        table[row][0] = row
    for column in range(len(second) + 1):
        table[0][column] = column
    for row in range(1, len(first) + 1):
        for column in range(1, len(second) + 1):
            substitution = table[row - 1][column - 1] + (first[row - 1] != second[column - 1])
            table[row][column] = min(table[row - 1][column] + 1, table[row][column - 1] + 1, substitution)
    return table


def _validate_dna(sequence: str) -> None:
    if any(symbol not in DNA_ALPHABET for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    assert edit_distance("GATTACA", "GACTATA") == 2
    assert edit_distance("ACG", "ACGT") == 1
    assert edit_distance("", "AC") == 2
    assert shortest_edit_operations("ACG", "ACGT") == ["match", "match", "match", "insert"]
    assert shortest_edit_operations("", "") == []
    print("006_edit_distance: all examples passed")
