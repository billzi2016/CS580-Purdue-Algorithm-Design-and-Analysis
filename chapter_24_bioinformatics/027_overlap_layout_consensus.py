"""Overlap-Layout-Consensus（OLC）短读段组装教学实现。

适用场景：对少量无错误 DNA reads，反复选择最大后缀/前缀重叠并合并得到贪心 contig。
核心思想：手写计算所有有向重叠，选最大且达到阈值者合并，直到不存在可接受边。
输入输出：输入 reads 与最小重叠长度，输出贪心 contig 列表。
时间复杂度：每轮 O(r²L)，空间复杂度 O(rL)。
关键边界情况：包含 reads 会先去重/去包含；贪心策略不保证重复区域中的最优或唯一组装。
"""

DNA = frozenset("ACGTN")


def overlap_length(left: str, right: str, minimum: int = 1) -> int:
    """返回 left 后缀与 right 前缀的最长重叠；不足 minimum 时为零。"""
    for size in range(min(len(left), len(right)), minimum - 1, -1):
        if left[-size:] == right[:size]: return size
    return 0


def olc_assemble(reads: list[str], minimum_overlap: int = 1) -> list[str]:
    """用最大重叠优先的 OLC 贪心布局生成 contig。

    参数：reads 为 DNA 片段，minimum_overlap 为正阈值。
    返回：无可合并边时剩余的 contig，按字典序排列。
    边界情况：空输入返回空；非法 DNA/非正阈值抛出 ValueError。
    关键算法点：每次合并都删去两条旧路径并加入拼接路径，因而不会重复消费 read。
    """
    if minimum_overlap <= 0: raise ValueError("minimum_overlap 必须为正")
    if any(any(c not in DNA for c in read) for read in reads): raise ValueError("reads 只能包含大写 DNA")
    contigs = list(dict.fromkeys(reads))
    contigs = [read for read in contigs if not any(read != other and read in other for other in contigs)]
    while True:
        best_size, best_left, best_right = 0, -1, -1
        for i, left in enumerate(contigs):
            for j, right in enumerate(contigs):
                if i != j:
                    size = overlap_length(left, right, minimum_overlap)
                    if size > best_size: best_size, best_left, best_right = size, i, j
        if not best_size: break
        merged = contigs[best_left] + contigs[best_right][best_size:]
        contigs = [read for k, read in enumerate(contigs) if k not in (best_left, best_right)] + [merged]
    return sorted(contigs)


if __name__ == "__main__":
    assert overlap_length("ATTAC", "TACGA", 2) == 3
    assert olc_assemble(["ATTAC", "TACGA", "CGAAA"], 2) == ["ATTACGAAA"]
    assert olc_assemble(["AC", "AC"], 1) == ["AC"]
    assert olc_assemble([], 1) == []
    print("027_overlap_layout_consensus: all examples passed")
