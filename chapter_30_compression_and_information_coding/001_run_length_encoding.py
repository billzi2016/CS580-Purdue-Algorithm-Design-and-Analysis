"""游程长度编码（RLE）的教学实现。

适用场景：输入中存在连续重复符号时，可用 RLE 将每段重复符号表示为
``(符号, 重复次数)``。本文件实现无损的编码与解码，适合说明最基础的
无损压缩思想；它不会对交替出现的字符保证压缩率。

输入输出：编码函数接收字符串，返回 ``(字符, 正整数次数)`` 元组列表；
解码函数接收相同形式的序列，恢复原字符串。
时间复杂度：编码和解码均为 O(n)，其中 n 为输入或输出字符总数。
空间复杂度：O(n)，用于保存编码结果或重建后的字符串。
关键边界：空字符串编码为空列表；解码时拒绝空符号、非整数或非正次数。
"""

from typing import Sequence, TypeAlias


Run: TypeAlias = tuple[str, int]


def run_length_encode(text: str) -> list[Run]:
    """将字符串编码为连续相同字符的游程。

    参数：
        text：待压缩的字符串。
    返回值：按原顺序排列的 ``(字符, 次数)`` 游程列表。
    边界情况：空字符串返回空列表；非字符串输入抛出 TypeError。
    关键算法点：扫描时始终维护当前游程的字符和长度，遇到新字符才提交游程，
        因而不会把原本相邻的相同字符拆开。
    """
    if not isinstance(text, str):
        raise TypeError("text 必须是字符串")
    if not text:
        return []

    runs: list[Run] = []
    current_symbol = text[0]
    current_count = 1
    for symbol in text[1:]:
        if symbol == current_symbol:
            # 循环不变量：current_count 始终等于尚未写出的当前游程长度。
            current_count += 1
        else:
            runs.append((current_symbol, current_count))
            current_symbol = symbol
            current_count = 1
    runs.append((current_symbol, current_count))
    return runs


def run_length_decode(runs: Sequence[Run]) -> str:
    """从游程长度编码无损恢复字符串。

    参数：
        runs：由 ``(单字符符号, 正整数次数)`` 组成的游程序列。
    返回值：拼接每段游程后得到的原字符串。
    边界情况：空序列返回空字符串；格式不合法的游程抛出 ValueError。
    关键算法点：每个游程独立扩展，再按输入顺序拼接，因此恢复顺序与编码前一致。
    """
    pieces: list[str] = []
    for run in runs:
        if not isinstance(run, tuple) or len(run) != 2:
            raise ValueError("每个游程必须是 (字符, 次数) 元组")
        symbol, count = run
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("游程符号必须恰好包含一个字符")
        if isinstance(count, bool) or not isinstance(count, int) or count <= 0:
            raise ValueError("游程次数必须是正整数")
        pieces.append(symbol * count)
    return "".join(pieces)


if __name__ == "__main__":
    assert run_length_encode("AAABCCCCDD") == [("A", 3), ("B", 1), ("C", 4), ("D", 2)]
    assert run_length_decode([("你", 2), ("好", 1)]) == "你你好"
    assert run_length_encode("") == []
    assert run_length_decode([]) == ""
    assert run_length_decode(run_length_encode("ABAB")) == "ABAB"

    print("001_run_length_encoding: all examples passed")
