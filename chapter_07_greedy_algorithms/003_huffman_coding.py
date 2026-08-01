"""
文件意图：
    本文件手写实现 Huffman 编码，用于根据字符频率构造最优前缀码。

适用场景：
    无损压缩中的变长编码；频率越高的符号应获得越短的编码。

核心思想：
    每次合并频率最小的两棵树。这个贪心选择保证最终带权路径长度最小。

时间复杂度：
    O(n log n)

空间复杂度：
    O(n)
"""

import heapq
from dataclasses import dataclass


@dataclass
class HuffmanNode:
    """Huffman 树节点。"""

    frequency: int
    symbol: str | None = None
    left: "HuffmanNode | None" = None
    right: "HuffmanNode | None" = None


def build_huffman_codes(frequencies: dict[str, int]) -> dict[str, str]:
    """
    根据字符频率构造 Huffman 编码表。

    参数：
        frequencies: 字符到正频率的映射。

    返回：
        字符到 0/1 编码串的映射。
    """
    if not frequencies:
        return {}
    for symbol, frequency in frequencies.items():
        if frequency <= 0:
            raise ValueError(f"频率必须为正数：{symbol} -> {frequency}")

    heap: list[tuple[int, int, HuffmanNode]] = []
    counter = 0
    for symbol, frequency in frequencies.items():
        heapq.heappush(heap, (frequency, counter, HuffmanNode(frequency, symbol)))
        counter += 1

    if len(heap) == 1:
        only_node = heap[0][2]
        return {only_node.symbol or "": "0"}

    while len(heap) > 1:
        left_frequency, _, left = heapq.heappop(heap)
        right_frequency, _, right = heapq.heappop(heap)
        merged = HuffmanNode(left_frequency + right_frequency, None, left, right)
        heapq.heappush(heap, (merged.frequency, counter, merged))
        counter += 1

    root = heap[0][2]
    codes: dict[str, str] = {}
    _assign_codes(root, "", codes)
    return codes


def _assign_codes(node: HuffmanNode, prefix: str, codes: dict[str, str]) -> None:
    """
    DFS 遍历 Huffman 树，为叶子节点分配编码。
    """
    if node.symbol is not None:
        codes[node.symbol] = prefix
        return

    if node.left is not None:
        _assign_codes(node.left, prefix + "0", codes)
    if node.right is not None:
        _assign_codes(node.right, prefix + "1", codes)


def is_prefix_free(codes: dict[str, str]) -> bool:
    """
    检查编码表是否满足前缀码性质。
    """
    code_values = list(codes.values())
    for i, first in enumerate(code_values):
        for j, second in enumerate(code_values):
            if i != j and second.startswith(first):
                return False
    return True


if __name__ == "__main__":
    codes = build_huffman_codes({"a": 5, "b": 9, "c": 12, "d": 13, "e": 16, "f": 45})
    assert set(codes) == {"a", "b", "c", "d", "e", "f"}
    assert is_prefix_free(codes)
    assert build_huffman_codes({"x": 7}) == {"x": "0"}
    assert build_huffman_codes({}) == {}

    try:
        build_huffman_codes({"bad": 0})
        raise AssertionError("非正频率必须抛出 ValueError")
    except ValueError:
        pass

    print("003_huffman_coding: all examples passed")
