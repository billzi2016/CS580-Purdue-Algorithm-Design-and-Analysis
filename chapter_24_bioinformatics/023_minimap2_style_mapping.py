"""minimap2 风格 seed-chain 候选定位教学实现。

适用场景：在短 DNA reference 中为 query 给出由 minimizer 精确命中和共线链支持的候选映射区间。
核心思想：抽取规范化 minimizer、建立 reference 倒排表、匹配 query minimizer 为锚点，再以 O(a²) DP 找最高分共线链。
输入输出：输入 reference/query/k/window，返回最佳链及其覆盖的 reference/query 候选区间；无种子返回 None。
时间复杂度：教学版抽样 O(nwk)、链 O(a²)；空间复杂度 O(r+q+a)。
关键边界情况：仅正向链；重复 minimizer 会产生多锚点；本版不等同于 minimap2，不做频率过滤、反向链、base-level extension、长 gap 或 splice 处理。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")
COMPLEMENT = str.maketrans("ACGTN", "TGCAN")


@dataclass(frozen=True)
class MappingAnchor:
    """reference 与 query 中一个相同 minimizer 的起点及长度。"""
    reference_start: int
    query_start: int
    length: int


@dataclass(frozen=True)
class MappingCandidate:
    """最佳链及两个序列上由首末锚点界定的候选区间。"""
    anchors: tuple[MappingAnchor, ...]
    score: int
    reference_interval: tuple[int, int]
    query_interval: tuple[int, int]


def minimap2_style_map(reference: str, query: str, k: int, window_kmers: int, max_gap: int = 100) -> MappingCandidate | None:
    """手写执行 minimizer→anchor→chain 三阶段，返回最高分正向候选。

    参数：reference、query 为 DNA；k/window_kmers 控制抽样；max_gap 限制锚点间坐标跨度。
    返回：最佳候选或 None；区间为左闭右开，尚未执行碱基级比对。
    边界情况：短序列无 minimizer 时返回 None；非法字符或参数抛出 ValueError。
    关键算法点：DP 仅连接两轴均递增且不重叠的锚点，避免把重复序列中的交叉命中误接成链。
    """
    _validate(reference); _validate(query)
    if k <= 0 or window_kmers <= 0 or max_gap < 0:
        raise ValueError("k、window_kmers 必须为正，max_gap 必须非负")
    reference_index: dict[str, list[int]] = {}
    for position, word in _minimizers(reference, k, window_kmers):
        reference_index.setdefault(word, []).append(position)
    anchors = [MappingAnchor(ref_pos, query_pos, k) for query_pos, word in _minimizers(query, k, window_kmers) for ref_pos in reference_index.get(word, [])]
    if not anchors:
        return None
    ordered = sorted(anchors, key=lambda item: (item.reference_start, item.query_start))
    scores = [item.length for item in ordered]; parent: list[int | None] = [None] * len(ordered)
    for current_index, current in enumerate(ordered):
        for previous_index in range(current_index):
            previous = ordered[previous_index]
            ref_gap = current.reference_start - (previous.reference_start + k)
            query_gap = current.query_start - (previous.query_start + k)
            if ref_gap < 0 or query_gap < 0 or max(ref_gap, query_gap) > max_gap:
                continue
            candidate = scores[previous_index] + k - abs(ref_gap - query_gap)
            if candidate > scores[current_index]:
                scores[current_index], parent[current_index] = candidate, previous_index
    best = max(range(len(ordered)), key=lambda index: scores[index]); path: list[MappingAnchor] = []
    while best is not None:
        path.append(ordered[best]); best = parent[best]
    path.reverse()
    return MappingCandidate(tuple(path), max(scores), (path[0].reference_start, path[-1].reference_start + k), (path[0].query_start, path[-1].query_start + k))


def _minimizers(sequence: str, k: int, width: int) -> list[tuple[int, str]]:
    """以最右并列规则抽取规范化 minimizer，避免依赖现有模块的数字文件名导入。"""
    words = [min(sequence[i:i+k], sequence[i:i+k].translate(COMPLEMENT)[::-1]) for i in range(max(0, len(sequence)-k+1))]
    selected: list[tuple[int, str]] = []; last = -1
    for start in range(max(0, len(words)-width+1)):
        window = words[start:start+width]; smallest = min(window); position = start + max(i for i, word in enumerate(window) if word == smallest)
        if position != last:
            selected.append((position, words[position])); last = position
    return selected


def _validate(sequence: str) -> None:
    """校验大写 DNA/N 输入。"""
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    candidate = minimap2_style_map("TTACGTACGG", "ACGTAC", 2, 2)
    assert candidate is not None
    assert candidate.reference_interval == (2, 8)
    assert candidate.query_interval == (0, 6)
    assert candidate.score >= 6
    assert minimap2_style_map("AAAA", "CGCG", 2, 2) is None
    assert minimap2_style_map("AC", "AC", 3, 1) is None
    print("023_minimap2_style_mapping: all examples passed")
