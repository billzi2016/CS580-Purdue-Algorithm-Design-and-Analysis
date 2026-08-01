"""Winnowing 文本指纹抽样教学实现。

适用场景：将任意字符串的 k-gram 以确定性哈希排序，并从每个滑动窗口选择最右最小指纹；可用于比较候选文本片段。
核心思想：用手写多项式滚动哈希得到 k-gram 指纹，在每个窗口选择最右最小哈希以处理并列并避免重复输出。
输入输出：输入文本、k-gram 长度 k、窗口内 hash 数 w，输出选中指纹及其起点。
时间复杂度：教学版 O(nwk)，用于清晰展示规则；空间复杂度 O(n)。
关键边界情况：Unicode 字符可处理；窗口不足返回空；哈希碰撞不会被当作已验证文本相等，调用者可复核 k-gram。
"""

from dataclasses import dataclass


BASE = 257
MODULUS = 1_000_000_007


@dataclass(frozen=True)
class Fingerprint:
    """一个选中 k-gram 的起点、哈希值与原始片段，片段用于碰撞复核。"""

    position: int
    value: int
    gram: str


def polynomial_hash(text: str) -> int:
    """手写计算文本的模多项式哈希。

    参数：text 为任意字符串。
    返回：范围在 [0, MODULUS) 的确定性整数哈希。
    边界情况：空字符串哈希为零；该函数可能碰撞，不能单独证明字符串相等。
    关键算法点：每次乘以 BASE 相当于在 BASE 进位制中向左移一位，再加入当前字符码。
    """
    value = 0
    for symbol in text:
        value = (value * BASE + ord(symbol)) % MODULUS
    return value


def winnow(text: str, k: int, window_hashes: int) -> list[Fingerprint]:
    """按最右并列规则从滑动 hash 窗口抽取文本指纹。

    参数：text 为任意文本；k 是 k-gram 长度；window_hashes 是窗口含有的 k-gram 数。
    返回：按位置升序、跨窗口去重的指纹。
    边界情况：k 或窗口大小非正抛出 ValueError；没有完整窗口时返回空。
    关键算法点：相同最小哈希选择最右项，使旧最小项离开窗口时无需重复记录仍可复现标准 winnowing 行为。
    """
    if k <= 0 or window_hashes <= 0:
        raise ValueError("k 和 window_hashes 必须为正整数")
    grams = [text[start : start + k] for start in range(max(0, len(text) - k + 1))]
    if len(grams) < window_hashes:
        return []
    values = [polynomial_hash(gram) for gram in grams]
    result: list[Fingerprint] = []
    last_position = -1
    for window_start in range(len(values) - window_hashes + 1):
        window = values[window_start : window_start + window_hashes]
        minimum = min(window)
        offset = max(index for index, value in enumerate(window) if value == minimum)
        position = window_start + offset
        if position != last_position:
            result.append(Fingerprint(position, values[position], grams[position]))
            last_position = position
    return result


if __name__ == "__main__":
    assert polynomial_hash("") == 0
    assert polynomial_hash("ACG") == polynomial_hash("ACG")
    fingerprints = winnow("ACGTAC", 2, 3)
    assert [(item.position, item.gram) for item in fingerprints] == [
        (0, "AC"),
        (1, "CG"),
        (4, "AC"),
    ]
    assert winnow("AC", 3, 1) == []
    try:
        winnow("ACG", 0, 2)
        raise AssertionError("应拒绝非正 k")
    except ValueError:
        pass
    print("019_winnowing: all examples passed")
