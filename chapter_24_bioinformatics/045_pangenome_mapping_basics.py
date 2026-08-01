"""pangenome mapping 基础教学实现。

适用场景：把读段映射到包含多条单倍型路径的 variation graph / pangenome graph。
核心思想：先用路径级 seed 匹配得到候选路径，再用简单 Hamming/长度一致比较给出最佳路径。
输入输出：输入命名路径序列字典和 query；输出最佳路径名、错配数和匹配区间。
时间复杂度：教学版 O(路径总长度 * query 长度)，空间复杂度 O(1) 额外空间。
关键边界情况：这里只做等长窗口扫描，不支持 indel；query 长于路径时该路径忽略。
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PangenomeMappingCandidate:
    """最佳路径候选。"""

    path_name: str
    mismatches: int
    interval: tuple[int, int]


def pangenome_map(paths: dict[str, str], query: str) -> PangenomeMappingCandidate | None:
    """在多路径 reference 中寻找 Hamming 错配最少的窗口。"""

    if not paths:
        raise ValueError("paths 不能为空")
    best: PangenomeMappingCandidate | None = None
    for path_name, sequence in paths.items():
        if len(sequence) < len(query):
            continue
        for start in range(len(sequence) - len(query) + 1):
            window = sequence[start : start + len(query)]
            mismatches = sum(1 for left, right in zip(window, query, strict=True) if left != right)
            candidate = PangenomeMappingCandidate(path_name, mismatches, (start, start + len(query)))
            if best is None or (candidate.mismatches, candidate.path_name, candidate.interval) < (
                best.mismatches,
                best.path_name,
                best.interval,
            ):
                best = candidate
    return best


if __name__ == "__main__":
    paths = {"ref": "ACGTAC", "hap1": "ACTTAC", "hap2": "GCGTAC"}
    best = pangenome_map(paths, "ACTTA")
    assert best == PangenomeMappingCandidate("hap1", 0, (0, 5))
    assert pangenome_map({"short": "AC"}, "ACG") is None
    print("045_pangenome_mapping_basics: all examples passed")
