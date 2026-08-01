"""LZ78 字典压缩的教学实现。

适用场景：LZ78 在编码和解码两端同步增量构建短语字典，用“已有短语索引 + 一个字符”
描述新短语。本实现使用 ``(索引, 下一个字符)`` token，最后一个 token 的字符可为 None。

输入输出：编码字符串为 LZ78 token 列表；解码 token 恢复原字符串。
时间复杂度：使用字典查找，编码和解码均为 O(n)；空间复杂度为 O(n)。
关键边界：空输入返回空 token；索引 0 表示空短语；None 仅允许最后一个 token，且其引用
的短语必须非空，避免生成空 token。
"""

from typing import TypeAlias


LZ78Token: TypeAlias = tuple[int, str | None]


def lz78_encode(text: str) -> list[LZ78Token]:
    """以最长已收录前缀构造 LZ78 token。

    参数：text 为待压缩字符串。
    返回值：每个 token 是 ``(字典索引, 新字符)``，最后一项可使用 None 表示完整已知短语。
    边界情况：空字符串返回空列表；非字符串输入抛出 TypeError。
    关键算法点：每次输出“当前最长已知短语加一个新字符”，随后立刻将该新短语加入字典，
        使编码器与解码器的字典增长顺序完全一致。
    """
    if not isinstance(text, str):
        raise TypeError("text 必须是字符串")

    phrase_to_index: dict[str, int] = {"": 0}
    tokens: list[LZ78Token] = []
    position = 0
    while position < len(text):
        end = position
        while end < len(text) and text[position : end + 1] in phrase_to_index:
            end += 1
        known_phrase = text[position:end]
        known_index = phrase_to_index[known_phrase]
        if end == len(text):
            # 剩余内容本身已在字典中，末尾 None 不新增条目也不会丢失字符。
            tokens.append((known_index, None))
            break
        next_symbol = text[end]
        new_phrase = known_phrase + next_symbol
        tokens.append((known_index, next_symbol))
        phrase_to_index[new_phrase] = len(phrase_to_index)
        position = end + 1
    return tokens


def lz78_decode(tokens: list[LZ78Token]) -> str:
    """从 LZ78 token 序列同步重建短语字典并恢复文本。

    参数：tokens 为 ``(已有短语索引, 单字符或 None)`` 序列。
    返回值：所有输出短语按顺序拼接后的原文本。
    边界情况：空 token 列表返回空串；越界索引、错误的 None token 及格式错误抛出 ValueError。
    关键算法点：字典下标从 0 的空短语开始，且每一个带字符 token 都新增一个短语，
        因此后续索引只会引用已经由前序 token 定义的短语。
    """
    dictionary: list[str] = [""]
    output: list[str] = []
    for token_index, token in enumerate(tokens):
        if not isinstance(token, tuple) or len(token) != 2:
            raise ValueError("每个 token 必须是 (索引, 下一个字符) 元组")
        prefix_index, next_symbol = token
        if isinstance(prefix_index, bool) or not isinstance(prefix_index, int) or not 0 <= prefix_index < len(dictionary):
            raise ValueError("token 引用了不存在的字典索引")
        prefix = dictionary[prefix_index]
        if next_symbol is None:
            if token_index != len(tokens) - 1 or not prefix:
                raise ValueError("None 只能表示最后一个非空已知短语")
            output.append(prefix)
            continue
        if not isinstance(next_symbol, str) or len(next_symbol) != 1:
            raise ValueError("下一个字符必须是单字符或 None")
        phrase = prefix + next_symbol
        dictionary.append(phrase)
        output.append(phrase)
    return "".join(output)


if __name__ == "__main__":
    sample = "ABAABABAABBBBBBBBBBA"
    encoded = lz78_encode(sample)
    assert lz78_decode(encoded) == sample
    assert lz78_encode("") == []
    assert lz78_decode([]) == ""
    assert lz78_decode([(0, "A"), (0, "B"), (1, None)]) == "ABA"
    try:
        lz78_decode([(1, "A")])
        raise AssertionError("越界索引应当抛出 ValueError")
    except ValueError:
        pass

    print("006_lz78: all examples passed")
