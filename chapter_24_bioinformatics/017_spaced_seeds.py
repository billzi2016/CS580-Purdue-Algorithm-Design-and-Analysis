"""间隔种子（spaced seed）教学实现。

适用场景：使用由 1/0 掩码指定的非连续位置提取 DNA 种子，在允许未选位置差异时发现候选匹配。
核心思想：掩码中的 1 为必须比较的位置，0 为跳过位置；相同投影键的窗口构成一个间隔种子命中。
输入输出：输入两条序列和掩码，输出所有匹配窗口的起点对及投影键。
时间复杂度：O((n+m)w+h)，w 为掩码跨度、h 为命中数；空间复杂度 O(n)。
关键边界情况：掩码必须含至少一个 1；序列短于掩码返回空；这是单掩码精确投影教学版。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class SpacedSeedHit:
    """两条序列窗口在掩码选定位置相等的命中。"""

    first_start: int
    second_start: int
    signature: str


def spaced_seed_signature(window: str, pattern: str) -> str:
    """提取窗口在 pattern 的 1 位上的字符串投影。

    参数：window 长度必须等于 pattern；pattern 仅由 0 和 1 构成。
    返回：由所有被选择字符按原序拼接的 signature。
    边界情况：窗口长度不符或模式无 1 抛出 ValueError。
    关键算法点：0 位完全不参与相等判断，因此窗口该处的替换不会改变 signature。
    """
    _validate_pattern(pattern)
    if len(window) != len(pattern):
        raise ValueError("窗口长度必须等于间隔种子模式跨度")
    return "".join(symbol for symbol, flag in zip(window, pattern) if flag == "1")


def spaced_seed_matches(first: str, second: str, pattern: str) -> list[SpacedSeedHit]:
    """为 first 建投影倒排表，在 second 中找全部单模式间隔种子命中。

    参数：first、second 为 DNA，pattern 是 0/1 模式。
    返回：按 first、second 起点排序的所有匹配。
    边界情况：任一序列短于模式跨度返回空；非法 DNA 或模式抛出 ValueError。
    关键算法点：同一 signature 保留 first 的所有位置，避免重复种子丢失候选命中。
    """
    _validate_dna(first)
    _validate_dna(second)
    _validate_pattern(pattern)
    span = len(pattern)
    if len(first) < span or len(second) < span:
        return []
    table: dict[str, list[int]] = {}
    for start in range(len(first) - span + 1):
        signature = spaced_seed_signature(first[start : start + span], pattern)
        table.setdefault(signature, []).append(start)
    hits: list[SpacedSeedHit] = []
    for second_start in range(len(second) - span + 1):
        signature = spaced_seed_signature(second[second_start : second_start + span], pattern)
        hits.extend(SpacedSeedHit(first_start, second_start, signature) for first_start in table.get(signature, []))
    return sorted(hits, key=lambda hit: (hit.first_start, hit.second_start))


def _validate_pattern(pattern: str) -> None:
    """确认模式具有正跨度且至少选择一个比较位置。"""
    if not pattern or any(flag not in "01" for flag in pattern) or "1" not in pattern:
        raise ValueError("模式必须是至少含一个 1 的非空 0/1 字符串")


def _validate_dna(sequence: str) -> None:
    """限制输入为大写 DNA 教学字母表。"""
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    assert spaced_seed_signature("ACGT", "1011") == "AGT"
    hits = spaced_seed_matches("ACGT", "ATGT", "1011")
    assert hits == [SpacedSeedHit(0, 0, "AGT")]
    assert spaced_seed_matches("AC", "ACGT", "111") == []
    try:
        spaced_seed_signature("AC", "00")
        raise AssertionError("应拒绝没有匹配位的模式")
    except ValueError:
        pass
    print("017_spaced_seeds: all examples passed")
