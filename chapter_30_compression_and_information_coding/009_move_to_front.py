"""Move-to-Front（MTF）变换的教学实现。

适用场景：MTF 维护一个可变符号表，每次输出符号当前位置并把它移到表首；它常用于
BWT 之后，使频繁出现的相邻符号变为较小整数。本文件实现可逆变换本身，不负责熵编码。

输入输出：编码返回 ``(位置序列, 初始字母表)``；解码用这两项恢复文本。
时间复杂度：朴素列表扫描与移动下，每个符号 O(k)，总计 O(nk)。空间复杂度 O(k+n)。
关键边界：空输入返回两个空列表；字母表必须是不重复的单字符；索引越界抛出 ValueError。
"""


def build_mtf_alphabet(text: str) -> list[str]:
    """按首次出现顺序建立 MTF 的初始字母表。

    参数：text 为待变换字符串。
    返回值：无重复的单字符列表。
    边界情况：空字符串返回空列表；非字符串输入抛出 TypeError。
    关键算法点：初始表是解码所需元数据，不能只依赖位置序列推断。
    """
    if not isinstance(text, str):
        raise TypeError("text 必须是字符串")
    alphabet: list[str] = []
    for symbol in text:
        if symbol not in alphabet:
            alphabet.append(symbol)
    return alphabet


def _validate_alphabet(alphabet: list[str]) -> None:
    """验证 MTF 初始表中每个符号唯一且恰为一个字符。"""
    if not isinstance(alphabet, list) or any(not isinstance(symbol, str) or len(symbol) != 1 for symbol in alphabet):
        raise ValueError("alphabet 必须是单字符列表")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet 不能包含重复字符")


def _find_position(table: list[str], symbol: str) -> int:
    """手写线性扫描，返回 symbol 在当前 MTF 表中的位置。"""
    for index, current in enumerate(table):
        if current == symbol:
            return index
    raise ValueError("符号不在 MTF 表中")


def move_to_front_encode(text: str) -> tuple[list[int], list[str]]:
    """将字符串变换为 Move-to-Front 位置序列。

    参数：text 为待变换字符串。
    返回值：``(positions, alphabet)``，alphabet 必须与 positions 一同传给解码器。
    边界情况：空字符串返回 ``([], [])``。
    关键算法点：每次找到符号位置后都立即将其移动到表首，后续位置才反映最近访问性。
    """
    alphabet = build_mtf_alphabet(text)
    table = alphabet[:]
    positions: list[int] = []
    for symbol in text:
        position = _find_position(table, symbol)
        positions.append(position)
        table.pop(position)
        table.insert(0, symbol)
    return positions, alphabet


def move_to_front_decode(positions: list[int], alphabet: list[str]) -> str:
    """从 MTF 位置序列与初始表恢复原始字符串。

    参数：positions 为非负整数位置；alphabet 为编码时保存的初始表。
    返回值：解码后的字符串。
    边界情况：空位置序列仅接受空字母表；位置越界、布尔值或表格式错误抛出 ValueError。
    关键算法点：解码端选择位置对应符号后采用与编码端相同的“移到表首”操作，两个表持续同步。
    """
    _validate_alphabet(alphabet)
    if not isinstance(positions, list) or any(isinstance(position, bool) or not isinstance(position, int) for position in positions):
        raise ValueError("positions 必须是整数列表")
    if not positions:
        if alphabet:
            raise ValueError("空位置序列应使用空初始字母表")
        return ""
    if not alphabet:
        raise ValueError("非空位置序列需要非空初始字母表")

    table = alphabet[:]
    decoded: list[str] = []
    for position in positions:
        if not 0 <= position < len(table):
            raise ValueError("MTF 位置超出当前表范围")
        symbol = table.pop(position)
        decoded.append(symbol)
        table.insert(0, symbol)
    return "".join(decoded)


if __name__ == "__main__":
    sample = "banana"
    positions, alphabet = move_to_front_encode(sample)
    assert positions == [0, 1, 2, 1, 1, 1]
    assert move_to_front_decode(positions, alphabet) == sample
    assert move_to_front_encode("") == ([], [])
    assert move_to_front_decode([], []) == ""
    assert move_to_front_decode([1, 0, 1], ["a", "b"]) == "bba"
    try:
        move_to_front_decode([2], ["a", "b"])
        raise AssertionError("越界位置应当抛出 ValueError")
    except ValueError:
        pass

    print("009_move_to_front: all examples passed")
