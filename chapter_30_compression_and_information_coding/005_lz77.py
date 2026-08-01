"""LZ77 滑动窗口压缩的教学实现。

适用场景：LZ77 用已输出的窗口内容表示后续重复子串，是许多字典压缩格式的核心思想。
本基础版使用朴素搜索，令三元组为 ``(回看距离, 匹配长度, 下一个字符)``；最后一个
三元组的下一个字符可以为 None。

输入输出：编码字符串为三元组列表；解码同样的三元组列表恢复原字符串。
时间复杂度：朴素编码最坏 O(n * window_size * lookahead_size)，解码 O(n)。
空间复杂度：O(n)，用于 token 或重建文本。
关键边界：空输入产生空 token；允许重叠复制；距离为 0 时长度必须为 0 且必须有字面量。
"""

from typing import TypeAlias


LZ77Token: TypeAlias = tuple[int, int, str | None]


def lz77_encode(text: str, window_size: int = 32, lookahead_size: int = 16) -> list[LZ77Token]:
    """使用有限滑动窗口生成 LZ77 三元组。

    参数：text 为待压缩字符串；window_size 限制回看窗口；lookahead_size 限制最长匹配。
    返回值：依次覆盖原文本的 ``(距离, 长度, 下一个字符)`` token 列表。
    边界情况：空字符串返回空列表；窗口或前瞻大小非正时抛出 ValueError。
    关键算法点：在所有可回看的起点中寻找最长匹配；允许源和目标重叠，因此可表示长重复串。
    """
    if not isinstance(text, str):
        raise TypeError("text 必须是字符串")
    if isinstance(window_size, bool) or isinstance(lookahead_size, bool) or window_size <= 0 or lookahead_size <= 0:
        raise ValueError("window_size 和 lookahead_size 必须是正整数")

    tokens: list[LZ77Token] = []
    position = 0
    while position < len(text):
        best_distance = 0
        best_length = 0
        window_start = max(0, position - window_size)
        maximum_length = min(lookahead_size, len(text) - position)
        for source_start in range(window_start, position):
            length = 0
            # text 作为完整原始输入，允许 source_start + length 进入当前待编码区域，
            # 这等价于解码端逐字符追加时的重叠复制。
            while length < maximum_length and text[source_start + length] == text[position + length]:
                length += 1
                if source_start + length >= position + length:
                    break
            if length > best_length:
                best_distance = position - source_start
                best_length = length

        next_position = position + best_length
        next_symbol = text[next_position] if next_position < len(text) else None
        tokens.append((best_distance, best_length, next_symbol))
        # 长匹配后还需消费字面量；末尾 token 没有字面量时只消费匹配长度。
        position += best_length + (1 if next_symbol is not None else 0)
    return tokens


def lz77_decode(tokens: list[LZ77Token]) -> str:
    """解码 LZ77 三元组并恢复原字符串。

    参数：tokens 为 ``(非负距离, 非负长度, 单字符或 None)`` 列表。
    返回值：按 token 顺序展开后的原字符串。
    边界情况：空列表返回空字符串；越界距离、非法末尾 token 或格式错误抛出 ValueError。
    关键算法点：匹配字符按一个字符一个字符写入输出，故源索引能追上输出尾部并自然支持重叠。
    """
    output: list[str] = []
    for token_index, token in enumerate(tokens):
        if not isinstance(token, tuple) or len(token) != 3:
            raise ValueError("每个 token 必须是 (距离, 长度, 下一个字符) 元组")
        distance, length, next_symbol = token
        if any(isinstance(value, bool) for value in (distance, length)) or not isinstance(distance, int) or not isinstance(length, int):
            raise ValueError("距离和长度必须是整数")
        if distance < 0 or length < 0 or (length > 0 and (distance == 0 or distance > len(output))):
            raise ValueError("token 的距离或长度无效")
        if distance == 0 and length != 0:
            raise ValueError("距离为 0 时匹配长度必须为 0")
        if next_symbol is not None and (not isinstance(next_symbol, str) or len(next_symbol) != 1):
            raise ValueError("下一个字符必须是单字符或 None")
        if next_symbol is None and token_index != len(tokens) - 1:
            raise ValueError("只有最后一个 token 可以没有下一个字符")

        for _ in range(length):
            output.append(output[-distance])
        if next_symbol is not None:
            output.append(next_symbol)
    return "".join(output)


if __name__ == "__main__":
    sample = "ABABABABAB"
    encoded = lz77_encode(sample, window_size=8, lookahead_size=8)
    assert lz77_decode(encoded) == sample
    assert lz77_encode("") == []
    assert lz77_decode([]) == ""
    assert lz77_decode([(0, 0, "A"), (1, 4, None)]) == "AAAAA"
    try:
        lz77_decode([(2, 1, None)])
        raise AssertionError("越界距离应当抛出 ValueError")
    except ValueError:
        pass

    print("005_lz77: all examples passed")
