"""string graph 组装的教学实现。

适用场景：对少量无错误 DNA reads，先构造 suffix-prefix overlap 图，再移除 contained read
和可由两跳路径完全解释的传递边，最后从不可约图的非分叉路径拼接 contig。
核心思想：string graph 是 overlap 图去除冗余边后的简化表示；这里用显式字符串相等来判定
某条直接边是否能被两跳路径完全替代。
输入输出：输入 reads 与最小 overlap 阈值，输出教学版 string graph 与 contig 列表。
时间复杂度：建图与传递约简最坏 O(r^3L)，其中 r 为 reads 数、L 为 read 长度。
空间复杂度：O(r^2)。
关键边界情况：空输入返回空图；这是教学版，不处理测序错误、反向互补、长链 read-path 约束、
复杂泡结构简化或工业实现中的 FM-index 加速。
"""

from dataclasses import dataclass

DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class StringGraphEdge:
    """string graph 的一条不可约 overlap 边。

    参数：source/target 为 read，overlap 为后缀-前缀重叠长度，extension 为追加到 contig 的后缀。
    返回值：不可变边记录。
    边界情况：同一 source 到不同 target 可以有不同 extension。
    关键算法点：边携带 extension，后续沿非分叉路径拼接时无需重新搜索 overlap。
    """

    source: str
    target: str
    overlap: int
    extension: str


@dataclass(frozen=True)
class StringGraph:
    """教学版 string graph。

    参数：reads 为图中的非包含 reads；edges 为全部不可约边；adjacency/indegree/outdegree 为图结构。
    返回值：供后续路径拼接复用的只读图。
    边界情况：无边图允许。
    关键算法点：这里的节点直接用 read 字符串表示，便于教学示例直接核对图结构。
    """

    reads: tuple[str, ...]
    edges: tuple[StringGraphEdge, ...]
    adjacency: dict[str, tuple[int, ...]]
    indegree: dict[str, int]
    outdegree: dict[str, int]


def overlap_length(left: str, right: str, minimum: int = 1) -> int:
    """返回 left 后缀与 right 前缀的最长重叠长度。"""

    for size in range(min(len(left), len(right)), minimum - 1, -1):
        if left[-size:] == right[:size]:
            return size
    return 0


def build_string_graph(reads: list[str], minimum_overlap: int = 1) -> StringGraph:
    """构造教学版 string graph。

    参数：reads 为大写 DNA reads，minimum_overlap 为正阈值。
    返回值：经过 contained-read 过滤和传递边删除后的 StringGraph。
    边界情况：空输入返回空图；非法字符或非正阈值抛出 ValueError。
    关键算法点：先生成全部 overlap 边，再把能被两跳路径拼出同一字符串的直接边删掉。
    """

    if minimum_overlap <= 0:
        raise ValueError("minimum_overlap 必须为正")
    _validate_reads(reads)
    filtered_reads = _remove_contained_reads(reads)
    candidate_edges: list[StringGraphEdge] = []
    for source in filtered_reads:
        for target in filtered_reads:
            if source == target:
                continue
            overlap = overlap_length(source, target, minimum_overlap)
            if overlap:
                candidate_edges.append(StringGraphEdge(source, target, overlap, target[overlap:]))
    irreducible = [
        edge for edge in candidate_edges if not _is_transitive(edge, candidate_edges)
    ]
    adjacency_lists: dict[str, list[int]] = {read: [] for read in filtered_reads}
    indegree = {read: 0 for read in filtered_reads}
    outdegree = {read: 0 for read in filtered_reads}
    for edge_id, edge in enumerate(irreducible):
        adjacency_lists[edge.source].append(edge_id)
        indegree[edge.target] += 1
        outdegree[edge.source] += 1
    edges = tuple(irreducible)
    adjacency = {read: tuple(edge_ids) for read, edge_ids in adjacency_lists.items()}
    return StringGraph(tuple(sorted(filtered_reads)), edges, adjacency, indegree, outdegree)


def assemble_string_graph(reads: list[str], minimum_overlap: int = 1) -> list[str]:
    """从教学版 string graph 的非分叉路径拼接 contig。

    参数：reads 为 DNA reads，minimum_overlap 为 overlap 阈值。
    返回值：按字典序排序的 contig 列表。
    边界情况：空输入返回空列表；若图存在分叉，则输出的是局部无歧义路径而非唯一全局装配。
    关键算法点：与 unitig 提取相同，先从非 1 入 1 出节点启动，再补纯环。
    """

    graph = build_string_graph(reads, minimum_overlap)
    used_edges = [False] * len(graph.edges)
    contigs: list[str] = []
    for read in graph.reads:
        if graph.outdegree[read] == 0 or _is_one_in_one_out(graph, read):
            continue
        for edge_id in graph.adjacency[read]:
            if used_edges[edge_id]:
                continue
            contigs.append(_consume_path(graph, edge_id, used_edges))
    for edge_id in range(len(graph.edges)):
        if not used_edges[edge_id]:
            contigs.append(_consume_cycle(graph, edge_id, used_edges))
    return sorted(contigs)


def _remove_contained_reads(reads: list[str]) -> list[str]:
    """去掉完全包含在其他 read 中的字符串，并按首次出现去重。"""

    deduplicated = list(dict.fromkeys(reads))
    return [
        read
        for read in deduplicated
        if not any(read != other and read in other for other in deduplicated)
    ]


def _is_transitive(edge: StringGraphEdge, edges: list[StringGraphEdge]) -> bool:
    """判断一条直接 overlap 是否能被两跳路径完全替代。"""

    direct = edge.source + edge.extension
    for first in edges:
        if first.source != edge.source or first.target == edge.target:
            continue
        for second in edges:
            if second.source != first.target or second.target != edge.target:
                continue
            via = first.source + first.extension + second.extension
            if via == direct:
                return True
    return False


def _consume_path(graph: StringGraph, first_edge_id: int, used_edges: list[bool]) -> str:
    """从一条不可约边开始拼接非分叉路径。"""

    edge = graph.edges[first_edge_id]
    used_edges[first_edge_id] = True
    contig = edge.source + edge.extension
    current = edge.target
    while _is_one_in_one_out(graph, current):
        next_edge_id = next(identifier for identifier in graph.adjacency[current] if not used_edges[identifier])
        next_edge = graph.edges[next_edge_id]
        used_edges[next_edge_id] = True
        contig += next_edge.extension
        current = next_edge.target
    return contig


def _consume_cycle(graph: StringGraph, first_edge_id: int, used_edges: list[bool]) -> str:
    """提取纯 1 入 1 出环。"""

    edge = graph.edges[first_edge_id]
    used_edges[first_edge_id] = True
    contig = edge.source + edge.extension
    start = edge.source
    current = edge.target
    while current != start:
        next_edge_id = next(identifier for identifier in graph.adjacency[current] if not used_edges[identifier])
        next_edge = graph.edges[next_edge_id]
        used_edges[next_edge_id] = True
        if next_edge.target == start:
            break
        contig += next_edge.extension
        current = next_edge.target
    return contig


def _is_one_in_one_out(graph: StringGraph, read: str) -> bool:
    """判断节点是否是 1 入 1 出的内部 read。"""

    return graph.indegree[read] == 1 and graph.outdegree[read] == 1


def _validate_reads(reads: list[str]) -> None:
    """验证 reads 只包含大写 DNA。"""

    if any(any(symbol not in DNA for symbol in read) for read in reads):
        raise ValueError("reads 只能包含大写 DNA 字符")


if __name__ == "__main__":
    graph = build_string_graph(["AAA", "AGA", "GAT", "ATC"], 2)
    assert graph.reads == ("AAA", "AGA", "ATC", "GAT")
    assert {(edge.source, edge.target) for edge in graph.edges} == {("AGA", "GAT"), ("GAT", "ATC")}
    graph = build_string_graph(["AAGT", "AGTC", "AAGTC"], 2)
    assert graph.reads == ("AAGTC",)
    graph = build_string_graph(["AAG", "AGT", "GTC", "AGTC"], 2)
    assert {(edge.source, edge.target) for edge in graph.edges} == {("AAG", "AGTC")}
    assert assemble_string_graph(["AAG", "AGT", "GTC", "AGTC"], 2) == ["AAGTC"]
    assert assemble_string_graph(["ATG", "TGA", "GAT"], 2) == ["ATGAT"]
    assert assemble_string_graph([], 1) == []
    print("030_string_graph_assembly: all examples passed")
