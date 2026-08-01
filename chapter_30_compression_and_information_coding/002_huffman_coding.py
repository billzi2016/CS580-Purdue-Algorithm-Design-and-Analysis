"""Huffman 编码的教学实现。

适用场景：Huffman 编码根据符号频率构造前缀码，常作为无损压缩的熵编码步骤。
本实现手写“反复合并最小权重结点”的构造过程，不调用现成堆或编码库。

输入输出：输入字符串；构建函数返回字符到位串的码表，编码函数返回位串，
解码函数使用同一码表恢复字符串。
时间复杂度：构树为 O(k^2)，k 为不同字符数；编码与解码为 O(n)，n 为位数。
空间复杂度：O(k + n)。
关键边界：空文本产生空码表；单一字符使用位 ``0``；解码会拒绝非二进制位和
不以完整码字结束的位串。
"""

from dataclasses import dataclass


@dataclass
class _HuffmanNode:
    """Huffman 树的内部结点；叶结点的 symbol 非空。"""

    weight: int
    order: int
    symbol: str | None = None
    left: "_HuffmanNode | None" = None
    right: "_HuffmanNode | None" = None


def _two_lightest(nodes: list[_HuffmanNode]) -> tuple[int, int]:
    """返回权重最小的两个结点下标，并以创建顺序稳定地处理并列权重。"""
    first_index, second_index = 0, 1
    if (nodes[second_index].weight, nodes[second_index].order) < (
        nodes[first_index].weight,
        nodes[first_index].order,
    ):
        first_index, second_index = second_index, first_index
    for index in range(2, len(nodes)):
        node_key = (nodes[index].weight, nodes[index].order)
        if node_key < (nodes[first_index].weight, nodes[first_index].order):
            second_index = first_index
            first_index = index
        elif node_key < (nodes[second_index].weight, nodes[second_index].order):
            second_index = index
    return first_index, second_index


def build_huffman_codebook(text: str) -> dict[str, str]:
    """按文本频率构造确定性的 Huffman 前缀码表。

    参数：
        text：用于统计频率并构造码表的字符串。
    返回值：字符映射到由 ``0``、``1`` 构成的 Huffman 码字。
    边界情况：空字符串返回空字典；仅一种字符时返回长度为一的码字 ``0``。
    关键算法点：每轮合并当前权重最小的两个子树；较小权重树被放在左侧并加 ``0``，
        合并过程保证最终码字互不为前缀。
    """
    if not isinstance(text, str):
        raise TypeError("text 必须是字符串")
    if not text:
        return {}

    frequencies: dict[str, int] = {}
    first_seen: dict[str, int] = {}
    for position, symbol in enumerate(text):
        frequencies[symbol] = frequencies.get(symbol, 0) + 1
        first_seen.setdefault(symbol, position)
    nodes = [
        _HuffmanNode(frequencies[symbol], first_seen[symbol], symbol)
        for symbol in frequencies
    ]
    if len(nodes) == 1:
        return {nodes[0].symbol: "0"}  # type: ignore[index]

    next_order = len(nodes)
    while len(nodes) > 1:
        first_index, second_index = _two_lightest(nodes)
        # 先取较大的下标，避免删除第一个结点后第二个下标偏移。
        right_node = nodes.pop(max(first_index, second_index))
        left_node = nodes.pop(min(first_index, second_index))
        nodes.append(
            _HuffmanNode(
                left_node.weight + right_node.weight,
                next_order,
                left=left_node,
                right=right_node,
            )
        )
        next_order += 1

    codebook: dict[str, str] = {}

    def visit(node: _HuffmanNode, prefix: str) -> None:
        if node.symbol is not None:
            codebook[node.symbol] = prefix
            return
        # 非叶结点必有两个孩子，这是每轮二叉合并保持的树结构不变量。
        if node.left is None or node.right is None:
            raise ValueError("Huffman 树结构不完整")
        visit(node.left, prefix + "0")
        visit(node.right, prefix + "1")

    visit(nodes[0], "")
    return codebook


def huffman_encode(text: str, codebook: dict[str, str]) -> str:
    """使用 Huffman 码表把文本转换为位串。

    参数：text 为待编码字符串；codebook 为字符到 Huffman 码字的映射。
    返回值：连接各字符码字所得的位串。
    边界情况：空文本返回空串；码表遗漏字符或含非二进制码字时抛出 ValueError。
    关键算法点：编码只做逐符号替换，前缀码的可解码性由码表构造阶段保证。
    """
    bits: list[str] = []
    for symbol in text:
        code = codebook.get(symbol)
        if code is None or not code or any(bit not in "01" for bit in code):
            raise ValueError("码表必须为每个字符提供非空二进制码字")
        bits.append(code)
    return "".join(bits)


def huffman_decode(bits: str, codebook: dict[str, str]) -> str:
    """使用 Huffman 码表从位串恢复文本。

    参数：bits 为二进制位串；codebook 为字符到码字的映射。
    返回值：完全解码后的字符串。
    边界情况：空位串返回空字符串；不存在匹配、非二进制位或残留前缀均抛出 ValueError。
    关键算法点：逐位累积候选码字；因为 Huffman 码是前缀码，首次匹配即是唯一字符。
    """
    tree: dict[str, object] = {}
    terminal = "_symbol"
    for symbol, code in codebook.items():
        if (
            not isinstance(symbol, str)
            or len(symbol) != 1
            or not code
            or any(bit not in "01" for bit in code)
        ):
            raise ValueError("码表包含非法码字")
        node = tree
        for bit in code:
            # 已有码字若在这里结束，当前码字便以它为前缀，不再是可唯一解码的前缀码。
            if terminal in node:
                raise ValueError("码表不是前缀码")
            child = node.setdefault(bit, {})
            if not isinstance(child, dict):
                raise ValueError("码表结构非法")
            node = child
        if node or terminal in node:
            raise ValueError("码表包含重复码字或不是前缀码")
        node[terminal] = symbol

    decoded: list[str] = []
    node = tree
    for bit in bits:
        if bit not in "01" or bit not in node:
            raise ValueError("位串无法由码表解码")
        child = node[bit]
        if not isinstance(child, dict):
            raise ValueError("码表结构非法")
        node = child
        if terminal in node:
            decoded.append(node[terminal])  # type: ignore[arg-type]
            node = tree
    if node is not tree:
        raise ValueError("位串以不完整的码字结束")
    return "".join(decoded)


if __name__ == "__main__":
    sample = "BANANA_BANDANA"
    sample_codebook = build_huffman_codebook(sample)
    assert (
        huffman_decode(huffman_encode(sample, sample_codebook), sample_codebook)
        == sample
    )
    assert build_huffman_codebook("") == {}
    assert build_huffman_codebook("AAAA") == {"A": "0"}
    assert huffman_decode("000", {"A": "0"}) == "AAA"
    try:
        huffman_decode("01", {"A": "0"})
        raise AssertionError("非法位串应当抛出 ValueError")
    except ValueError:
        pass

    print("002_huffman_coding: all examples passed")
