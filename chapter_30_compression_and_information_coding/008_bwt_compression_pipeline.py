"""Burrows-Wheeler Transform（BWT）与 RLE 压缩流水线的教学实现。

适用场景：BWT 重排字符以聚集相似上下文，随后可由游程编码利用连续重复字符。本文件
实现无损的 ``BWT -> RLE`` 流水线；为保持教学透明度，循环移位与排序均手写，未实现
工业格式常见的块划分、Move-to-Front、熵编码或内存优化。

输入输出：BWT 返回 ``(末列, 原串所在行号)``；流水线返回 RLE 末列及行号，解压恢复文本。
时间复杂度：朴素 BWT 与逆变换最坏 O(n^3)，RLE 阶段 O(n)。空间复杂度 O(n^2)。
关键边界：空字符串使用 ``("", 0)``；primary index 越界、RLE 游程格式不合法均抛出异常。
"""

from typing import TypeAlias


Run: TypeAlias = tuple[str, int]


def _insertion_sort_rows(rows: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """按循环移位字符串手写插入排序，并以原起点稳定消除相同移位的歧义。"""
    ordered = rows[:]
    for index in range(1, len(ordered)):
        current = ordered[index]
        previous = index - 1
        while previous >= 0 and ordered[previous] > current:
            ordered[previous + 1] = ordered[previous]
            previous -= 1
        ordered[previous + 1] = current
    return ordered


def _insertion_sort_strings(rows: list[str]) -> list[str]:
    """为 BWT 逆变换逐轮重排字符串表的手写插入排序。"""
    ordered = rows[:]
    for index in range(1, len(ordered)):
        current = ordered[index]
        previous = index - 1
        while previous >= 0 and ordered[previous] > current:
            ordered[previous + 1] = ordered[previous]
            previous -= 1
        ordered[previous + 1] = current
    return ordered


def bwt_transform(text: str) -> tuple[str, int]:
    """计算字符串的 BWT 末列及原字符串在排序循环移位表中的行号。

    参数：text 为待变换字符串。
    返回值：``(last_column, primary_index)``，二者共同构成可逆的 BWT 表示。
    边界情况：空字符串返回 ``("", 0)``；非字符串输入抛出 TypeError。
    关键算法点：排序全部循环移位；原字符串所在行的最后一个字符形成末列的一项，保留该行号
        才能在没有额外终止符的情况下唯一确定原始旋转。
    """
    if not isinstance(text, str):
        raise TypeError("text 必须是字符串")
    if not text:
        return "", 0
    rows = [(text[start:] + text[:start], start) for start in range(len(text))]
    ordered_rows = _insertion_sort_rows(rows)
    last_column = "".join(rotation[-1] for rotation, _ in ordered_rows)
    for index, (_, start) in enumerate(ordered_rows):
        if start == 0:
            return last_column, index
    raise ValueError("未找到原字符串所在行")


def bwt_inverse(last_column: str, primary_index: int) -> str:
    """从 BWT 末列和原串行号恢复原字符串。

    参数：last_column 为 BWT 最后一列；primary_index 为原串所在的零基行号。
    返回值：变换前字符串。
    边界情况：空末列仅接受行号 0；非整数或越界行号抛出 ValueError。
    关键算法点：每轮把末列字符前置到现有行，再按字典序重排；重复 n 轮后每行恰为一个循环移位。
    """
    if not isinstance(last_column, str):
        raise TypeError("last_column 必须是字符串")
    if isinstance(primary_index, bool) or not isinstance(primary_index, int):
        raise ValueError("primary_index 必须是整数")
    if not last_column:
        if primary_index != 0:
            raise ValueError("空 BWT 的 primary_index 必须为 0")
        return ""
    if not 0 <= primary_index < len(last_column):
        raise ValueError("primary_index 超出末列范围")

    rows = [""] * len(last_column)
    for _ in range(len(last_column)):
        rows = _insertion_sort_strings([last_column[index] + rows[index] for index in range(len(last_column))])
    return rows[primary_index]


def _rle_encode(text: str) -> list[Run]:
    """在流水线内部对 BWT 末列进行游程编码。"""
    if not text:
        return []
    runs: list[Run] = []
    symbol, count = text[0], 1
    for current in text[1:]:
        if current == symbol:
            count += 1
        else:
            runs.append((symbol, count))
            symbol, count = current, 1
    runs.append((symbol, count))
    return runs


def _rle_decode(runs: list[Run]) -> str:
    """校验并展开 BWT 流水线内部 RLE 结果。"""
    pieces: list[str] = []
    for run in runs:
        if not isinstance(run, tuple) or len(run) != 2:
            raise ValueError("每个游程必须是 (字符, 次数) 元组")
        symbol, count = run
        if not isinstance(symbol, str) or len(symbol) != 1 or isinstance(count, bool) or not isinstance(count, int) or count <= 0:
            raise ValueError("游程格式无效")
        pieces.append(symbol * count)
    return "".join(pieces)


def bwt_rle_compress(text: str) -> tuple[list[Run], int]:
    """执行 BWT 后再执行 RLE 的无损压缩流水线。

    参数：text 为待压缩字符串。
    返回值：``(BWT 末列的游程, primary_index)``。
    边界情况：空字符串返回 ``([], 0)``。
    关键算法点：RLE 只处理 BWT 末列；primary_index 不可省略，否则循环移位无法区分。
    """
    last_column, primary_index = bwt_transform(text)
    return _rle_encode(last_column), primary_index


def bwt_rle_decompress(runs: list[Run], primary_index: int) -> str:
    """逆转 RLE 与 BWT 流水线，恢复原字符串。

    参数：runs 为 BWT 末列的游程；primary_index 为原串行号。
    返回值：解压后的原字符串。
    边界情况：格式错误的游程或不匹配的行号由下层校验并抛出 ValueError。
    关键算法点：先完整恢复末列，才可按 BWT 的逐轮重建规则恢复原始字符顺序。
    """
    return bwt_inverse(_rle_decode(runs), primary_index)


if __name__ == "__main__":
    sample = "BANANA"
    last, primary = bwt_transform(sample)
    assert (last, primary) == ("NNBAAA", 3)
    assert bwt_inverse(last, primary) == sample
    compressed_runs, compressed_primary = bwt_rle_compress("MISSISSIPPI")
    assert bwt_rle_decompress(compressed_runs, compressed_primary) == "MISSISSIPPI"
    assert bwt_transform("") == ("", 0)
    assert bwt_rle_decompress([], 0) == ""
    try:
        bwt_inverse("ABC", 3)
        raise AssertionError("越界行号应当抛出 ValueError")
    except ValueError:
        pass

    print("008_bwt_compression_pipeline: all examples passed")
