"""Canonical Huffman 编码的教学实现。

适用场景：Canonical Huffman 只需传输每个符号的码长即可重建码表，常用于需要
紧凑存储 Huffman 码表的无损压缩格式。本实现先手写构造 Huffman 码长，再按
“码长、符号”排序分配规范码字。

输入输出：从字符串构造字符码表，或从码长表重建码表；另提供位串编码与解码。
时间复杂度：构造码长为 O(k^2)，规范分配为 O(k^2)（使用手写插入排序），
编码和解码为 O(n)。空间复杂度为 O(k + n)。
关键边界：空文本返回空码表；单一符号的码长为 1；非法、无法构成前缀码的码长表
会抛出 ValueError。
"""

from dataclasses import dataclass


@dataclass
class _LengthNode:
    """仅为计算 Huffman 码长使用的二叉树结点。"""

    weight: int
    order: int
    symbol: str | None = None
    left: "_LengthNode | None" = None
    right: "_LengthNode | None" = None


def _take_two_lightest(nodes: list[_LengthNode]) -> tuple[int, int]:
    """找出权重最小的两个结点下标，以稳定顺序消除并列歧义。"""
    first, second = 0, 1
    if (nodes[second].weight, nodes[second].order) < (
        nodes[first].weight,
        nodes[first].order,
    ):
        first, second = second, first
    for index in range(2, len(nodes)):
        key = (nodes[index].weight, nodes[index].order)
        if key < (nodes[first].weight, nodes[first].order):
            second, first = first, index
        elif key < (nodes[second].weight, nodes[second].order):
            second = index
    return first, second


def huffman_code_lengths(text: str) -> dict[str, int]:
    """从文本频率手写构造 Huffman 码长表。

    参数：text 为待统计频率的字符串。
    返回值：每个字符对应的正整数 Huffman 码长。
    边界情况：空文本返回空字典；单一字符的码长固定为 1。
    关键算法点：Huffman 树的叶深度就是码长；反复合并两个最轻结点最小化加权路径长。
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
        _LengthNode(frequencies[symbol], first_seen[symbol], symbol)
        for symbol in frequencies
    ]
    if len(nodes) == 1:
        return {nodes[0].symbol: 1}  # type: ignore[index]

    next_order = len(nodes)
    while len(nodes) > 1:
        first, second = _take_two_lightest(nodes)
        right = nodes.pop(max(first, second))
        left = nodes.pop(min(first, second))
        nodes.append(
            _LengthNode(left.weight + right.weight, next_order, left=left, right=right)
        )
        next_order += 1

    lengths: dict[str, int] = {}

    def collect_lengths(node: _LengthNode, depth: int) -> None:
        if node.symbol is not None:
            lengths[node.symbol] = depth
            return
        if node.left is None or node.right is None:
            raise ValueError("Huffman 树结构不完整")
        collect_lengths(node.left, depth + 1)
        collect_lengths(node.right, depth + 1)

    collect_lengths(nodes[0], 0)
    return lengths


def _insertion_sort_symbols(items: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """按“码长、符号”手写稳定插入排序，避免把排序库当作核心步骤。"""
    ordered = items[:]
    for index in range(1, len(ordered)):
        current = ordered[index]
        previous = index - 1
        while previous >= 0 and (ordered[previous][1], ordered[previous][0]) > (
            current[1],
            current[0],
        ):
            ordered[previous + 1] = ordered[previous]
            previous -= 1
        ordered[previous + 1] = current
    return ordered


def build_canonical_codebook(code_lengths: dict[str, int]) -> dict[str, str]:
    """根据码长表构造 Canonical Huffman 码表。

    参数：code_lengths 将单字符符号映射到正整数码长。
    返回值：同一组码长唯一确定的规范二进制码字。
    边界情况：空字典返回空字典；非法符号、码长或违反前缀码容量的长度表抛出 ValueError。
    关键算法点：第一个码字为全零；每个后继整数码先加一，再左移到更长的码长，
        使同长度码连续且字典序递增。
    """
    for symbol, length in code_lengths.items():
        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError("符号必须恰好包含一个字符")
        if isinstance(length, bool) or not isinstance(length, int) or length <= 0:
            raise ValueError("码长必须是正整数")
    ordered = _insertion_sort_symbols(list(code_lengths.items()))
    if not ordered:
        return {}

    codebook: dict[str, str] = {}
    code = 0
    previous_length = ordered[0][1]
    for index, (symbol, length) in enumerate(ordered):
        if index:
            code = (code + 1) << (length - previous_length)
        # 若数值需要超过 length 位才能表达，表示这些码长已无可用前缀码。
        if code >= (1 << length):
            raise ValueError("码长表不能构成有效前缀码")
        codebook[symbol] = format(code, f"0{length}b")
        previous_length = length
    return codebook


def canonical_encode(text: str, codebook: dict[str, str]) -> str:
    """使用 Canonical Huffman 码表将字符串编码为位串。

    参数：text 是待编码字符串；codebook 是规范码表。
    返回值：按字符顺序连接的二进制位串。
    边界情况：空文本返回空串；码表遗漏字符时抛出 ValueError。
    关键算法点：规范性只影响码表的表示方式，实际编码仍是逐字符替换。
    """
    bits: list[str] = []
    for symbol in text:
        if symbol not in codebook:
            raise ValueError("码表缺少待编码字符")
        bits.append(codebook[symbol])
    return "".join(bits)


def canonical_decode(bits: str, codebook: dict[str, str]) -> str:
    """使用 Canonical Huffman 码表恢复二进制位串。

    参数：bits 是二进制位串；codebook 是字符到规范码字的映射。
    返回值：成功完整解码后的字符串。
    边界情况：空位串返回空串；非法位、重复码字、非前缀码或残留前缀抛出 ValueError。
    关键算法点：构造解码前缀树；若某码字落在已有叶下或成为已有码字前缀，就拒绝该表。
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
            raise ValueError("码表包含非法符号或码字")
        node = tree
        for bit in code:
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
        raise ValueError("位串以不完整码字结束")
    return "".join(decoded)


if __name__ == "__main__":
    sample = "MISSISSIPPI"
    lengths = huffman_code_lengths(sample)
    sample_codebook = build_canonical_codebook(lengths)
    assert (
        canonical_decode(canonical_encode(sample, sample_codebook), sample_codebook)
        == sample
    )
    assert build_canonical_codebook({"A": 1, "B": 2, "C": 2}) == {
        "A": "0",
        "B": "10",
        "C": "11",
    }
    assert huffman_code_lengths("") == {}
    assert build_canonical_codebook({"Z": 1}) == {"Z": "0"}
    try:
        build_canonical_codebook({"A": 1, "B": 1, "C": 1})
        raise AssertionError("超出前缀码容量的长度表应当抛出 ValueError")
    except ValueError:
        pass

    print("003_canonical_huffman: all examples passed")
