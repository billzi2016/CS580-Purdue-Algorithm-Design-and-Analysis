"""LZW（Lempel-Ziv-Welch）字典压缩的教学实现。

适用场景：LZW 在编解码两端以同一初始符号表逐步扩展字典，用整数码字替代重复短语。
本实现显式返回初始字母表，因而无需假设 ASCII 或某个固定字符集；不包含工业格式的
位宽增长、清除码和位打包。

输入输出：编码返回 ``(整数码字列表, 初始字母表)``；解码用二者恢复原文本。
时间复杂度：编码与解码均为 O(n)，字典查找为均摊 O(1)；空间复杂度 O(n)。
关键边界：空输入返回两个空列表；解码处理 LZW 特有的“下一个码正好是待新增条目”情况；
非法字典、码字或不存在的码会抛出 ValueError。
"""


def build_initial_alphabet(text: str) -> list[str]:
    """按首次出现顺序提取 LZW 的初始单字符字典。

    参数：text 为待编码字符串。
    返回值：不重复的单字符列表，其下标即初始码字。
    边界情况：空字符串返回空列表；非字符串输入抛出 TypeError。
    关键算法点：初始字典顺序属于编码元数据，解码必须使用完全相同的顺序。
    """
    if not isinstance(text, str):
        raise TypeError("text 必须是字符串")
    alphabet: list[str] = []
    seen: set[str] = set()
    for symbol in text:
        if symbol not in seen:
            seen.add(symbol)
            alphabet.append(symbol)
    return alphabet


def lzw_encode(text: str) -> tuple[list[int], list[str]]:
    """将文本编码成 LZW 整数码字与初始字母表。

    参数：text 为待压缩字符串。
    返回值：``(codes, alphabet)``；alphabet 需与 codes 一同保存以供解码。
    边界情况：空字符串返回 ``([], [])``。
    关键算法点：维护当前最长已知短语；一旦加上新字符后的候选短语不存在，就输出当前
        短语码并新增候选短语，随后从该新字符重新开始。
    """
    alphabet = build_initial_alphabet(text)
    if not text:
        return [], alphabet

    dictionary = {symbol: index for index, symbol in enumerate(alphabet)}
    next_code = len(dictionary)
    current = text[0]
    codes: list[int] = []
    for symbol in text[1:]:
        candidate = current + symbol
        if candidate in dictionary:
            current = candidate
        else:
            codes.append(dictionary[current])
            dictionary[candidate] = next_code
            next_code += 1
            current = symbol
    codes.append(dictionary[current])
    return codes, alphabet


def _validate_alphabet(alphabet: list[str]) -> None:
    """检查 LZW 初始字母表能否唯一映射为单字符码字。"""
    if not isinstance(alphabet, list):
        raise ValueError("alphabet 必须是列表")
    if any(not isinstance(symbol, str) or len(symbol) != 1 for symbol in alphabet):
        raise ValueError("alphabet 中每项必须是单个字符")
    if len(set(alphabet)) != len(alphabet):
        raise ValueError("alphabet 不能包含重复字符")


def lzw_decode(codes: list[int], alphabet: list[str]) -> str:
    """从 LZW 整数码字和初始字母表恢复原文本。

    参数：codes 为编码器输出的整数列表；alphabet 为编码时保存的初始字母表。
    返回值：解码后的字符串。
    边界情况：空码字仅接受空字母表；码字越界、负数或不可能的前向引用抛出 ValueError。
    关键算法点：当读取的码等于下一个待分配码时，短语只能是 ``previous + previous[0]``，
        这是编码器刚输出并新增该短语时造成的唯一合法前向引用。
    """
    _validate_alphabet(alphabet)
    if not isinstance(codes, list) or any(
        isinstance(code, bool) or not isinstance(code, int) for code in codes
    ):
        raise ValueError("codes 必须是整数列表")
    if not codes:
        if alphabet:
            raise ValueError("空码字应使用空初始字母表")
        return ""
    if not alphabet:
        raise ValueError("非空码字需要非空初始字母表")

    dictionary = alphabet[:]
    first_code = codes[0]
    if not 0 <= first_code < len(dictionary):
        raise ValueError("第一个码字必须引用初始字母表")
    previous = dictionary[first_code]
    output = [previous]
    for code in codes[1:]:
        if 0 <= code < len(dictionary):
            entry = dictionary[code]
        elif code == len(dictionary):
            entry = previous + previous[0]
        else:
            raise ValueError("码字引用了不存在的 LZW 字典项")
        output.append(entry)
        dictionary.append(previous + entry[0])
        previous = entry
    return "".join(output)


if __name__ == "__main__":
    sample = "TOBEORNOTTOBEORTOBEORNOT"
    sample_codes, sample_alphabet = lzw_encode(sample)
    assert lzw_decode(sample_codes, sample_alphabet) == sample
    assert lzw_encode("") == ([], [])
    assert lzw_decode([], []) == ""
    assert lzw_decode([0, 1, 2, 4], ["A", "B"]) == "ABABABA"
    try:
        lzw_decode([3], ["A"])
        raise AssertionError("非法首码应当抛出 ValueError")
    except ValueError:
        pass

    print("007_lzw: all examples passed")
