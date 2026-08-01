"""BLAST 风格 exact-seed-and-extend 的教学实现。

适用场景：从短 DNA 精确种子出发，在固定对角线做无缺口双向 X-drop 延伸以提取局部高分片段。
核心思想：先用 k-mer 倒排表产生种子，再从种子边界向两侧累积 match/mismatch 分数，累计落后最佳分数超过阈值就停止。
输入输出：输入 query、target 与评分参数，输出按分数去重后的局部无缺口片段。
时间复杂度：建立索引 O(q)，种子扫描 O(t)，延伸为所有种子延伸长度之和；空间复杂度 O(q+h)。
关键边界情况：短于 k 的序列无命中；只支持 DNA；这是教学模型，不实现邻近词、gapped extension、E-value 或数据库统计。
"""

from dataclasses import dataclass


DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class UngappedExtension:
    """一段由种子延伸得到的局部无缺口命中区间，末端采用开区间。"""

    query_start: int
    query_end: int
    target_start: int
    target_end: int
    score: int

    @property
    def query_fragment(self) -> tuple[int, int]:
        """返回查询片段下标范围，便于调用者从原序列切片。"""
        return self.query_start, self.query_end


def blast_style_seed_extend(
    query: str, target: str, k: int, match: int = 1, mismatch: int = -1, x_drop: int = 2
) -> list[UngappedExtension]:
    """以所有精确 k-mer 为种子执行手写无缺口 X-drop 双向延伸。

    参数：query、target 为 DNA；k 是种子长度；match/mismatch 是字符评分；x_drop 为非负停止阈值。
    返回：按最高分和坐标排序、完全相同区间已去重的局部片段。
    边界情况：k 不合法、x_drop 负数或非法 DNA 字符抛出 ValueError；短序列返回空列表。
    关键算法点：左右分别从种子边界外推进，保留到达过的最高分位置，而非把低分尾部纳入结果。
    """
    _validate_dna(query)
    _validate_dna(target)
    if k <= 0 or x_drop < 0:
        raise ValueError("k 必须为正，x_drop 必须非负")
    if len(query) < k or len(target) < k:
        return []
    index: dict[str, list[int]] = {}
    for start in range(len(query) - k + 1):
        index.setdefault(query[start : start + k], []).append(start)
    unique: set[UngappedExtension] = set()
    for target_start in range(len(target) - k + 1):
        word = target[target_start : target_start + k]
        for query_start in index.get(word, []):
            unique.add(
                _extend(
                    query, target, query_start, target_start, k, match, mismatch, x_drop
                )
            )
    return sorted(
        unique,
        key=lambda hit: (-hit.score, hit.query_start, hit.target_start, hit.query_end),
    )


def _extend(
    query: str,
    target: str,
    query_start: int,
    target_start: int,
    k: int,
    match: int,
    mismatch: int,
    x_drop: int,
) -> UngappedExtension:
    """从一个精确种子向两侧 X-drop 延伸，并返回分数最优的截断位置。"""
    seed_score = k * match
    left_score, left_best = 0, 0
    query_left, target_left = query_start - 1, target_start - 1
    best_query_start, best_target_start = query_start, target_start
    while query_left >= 0 and target_left >= 0:
        left_score += match if query[query_left] == target[target_left] else mismatch
        if left_score > left_best:
            left_best = left_score
            best_query_start, best_target_start = query_left, target_left
        if left_best - left_score > x_drop:
            break
        query_left -= 1
        target_left -= 1
    right_score, right_best = 0, 0
    query_right, target_right = query_start + k, target_start + k
    best_query_end, best_target_end = query_right, target_right
    while query_right < len(query) and target_right < len(target):
        right_score += match if query[query_right] == target[target_right] else mismatch
        if right_score > right_best:
            right_best = right_score
            best_query_end, best_target_end = query_right + 1, target_right + 1
        if right_best - right_score > x_drop:
            break
        query_right += 1
        target_right += 1
    return UngappedExtension(
        best_query_start,
        best_query_end,
        best_target_start,
        best_target_end,
        seed_score + left_best + right_best,
    )


def _validate_dna(sequence: str) -> None:
    """校验教学模型的 DNA 输入范围。"""
    if any(symbol not in DNA for symbol in sequence):
        raise ValueError("序列只能包含大写 A、C、G、T 或 N")


if __name__ == "__main__":
    hits = blast_style_seed_extend("TTACGTA", "GGACGTACC", 3)
    assert hits[0] == UngappedExtension(2, 7, 2, 7, 5)
    assert blast_style_seed_extend("AC", "ACGT", 3) == []
    assert blast_style_seed_extend("AAAA", "AAAATA", 3)[0].score >= 3
    try:
        blast_style_seed_extend("ACX", "ACG", 2)
        raise AssertionError("应拒绝非法 DNA 字符")
    except ValueError:
        pass
    print("016_blast_seed_extend: all examples passed")
