"""
文件意图：手写计算等长 DNA 序列的 Hamming 距离及不匹配位置。
适用场景：已对齐且等长的短读段、k-mer 或二进制编码序列的替换差异统计。
核心思想：逐位置比较；每个不同字符恰对应一次替换，所有不同位置数量即为 Hamming 距离。
输入输出：输入两条等长 DNA 序列，输出距离或不匹配零基下标。
时间复杂度：O(n)，空间复杂度为 O(1)（距离）或 O(d)（下标列表）。
关键边界情况：两条空串距离为 0；长度不同不能用 Hamming 距离表示并抛出异常。
"""

DNA_ALPHABET = frozenset("ACGTN")


def hamming_distance(first: str, second: str) -> int:
    """返回两条等长 DNA 序列的 Hamming 距离。

    参数：first、second 是等长大写 DNA 序列。
    返回：对应位置字符不相同的数量。
    边界情况：空串对返回 0；长度不同或非法字符抛出 ValueError。
    关键算法点：只允许替换而没有插入/删除，因此必须固定逐位置比较。
    """
    _validate_pair(first, second)
    return sum(left != right for left, right in zip(first, second))


def mismatch_positions(first: str, second: str) -> list[int]:
    """返回两条等长 DNA 序列中全部不匹配的零基位置。"""
    _validate_pair(first, second)
    return [index for index, (left, right) in enumerate(zip(first, second)) if left != right]


def _validate_pair(first: str, second: str) -> None:
    if len(first) != len(second):
        raise ValueError("Hamming 距离只适用于等长序列")
    if any(symbol not in DNA_ALPHABET for symbol in first + second):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    assert hamming_distance("ACGT", "ACGT") == 0
    assert hamming_distance("ACGT", "AGGA") == 2
    assert mismatch_positions("ACGT", "AGGA") == [1, 3]
    assert hamming_distance("", "") == 0
    try:
        hamming_distance("AC", "ACG")
        raise AssertionError("不等长序列应抛出 ValueError")
    except ValueError:
        pass
    print("005_hamming_distance: all examples passed")
