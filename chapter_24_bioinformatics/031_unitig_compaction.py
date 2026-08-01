"""unitig 压缩与 compacted de Bruijn graph 的教学实现。

适用场景：给定一组唯一 k-mer，构造 node-centric de Bruijn 图，并把 maximal unitig 压缩成
更小的 compacted graph 节点。
核心思想：k-mer 作为节点，(k-1)-前后缀重叠作为有向边；所有内部节点满足 1 入 1 出的路径
可以拼成 unitig，再把这些路径视为新节点并恢复它们之间的连接关系。
输入输出：输入 k-mer 列表，输出 unitig 字符串和 compacted graph 邻接信息。
时间复杂度：建图 O(n^2k)，unitig 提取与压缩 O(E + V)。
空间复杂度：O(E + V)。
关键边界情况：空输入返回空图；这是教学版 node-centric 表述，不处理双向 canonical k-mer、
多重边计数、覆盖度过滤、错误修剪或工业级大规模压缩优化。
"""

from dataclasses import dataclass

DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class KmerGraph:
    """node-centric de Bruijn 图。"""

    nodes: tuple[str, ...]
    adjacency: dict[str, tuple[str, ...]]
    indegree: dict[str, int]
    outdegree: dict[str, int]


@dataclass(frozen=True)
class CompactedDBG:
    """压缩后的 de Bruijn 图。

    参数：unitigs 为 maximal unitig 字符串；adjacency 按 unitig 下标给出后继 unitig。
    返回值：教学版 cDBG。
    边界情况：无边时允许孤立 unitig。
    关键算法点：保留 original k-mer 到 unitig 的映射，才能把原始图边投影到压缩图边。
    """

    unitigs: tuple[str, ...]
    adjacency: dict[int, tuple[int, ...]]


def build_node_centric_dbg(kmers: list[str]) -> KmerGraph:
    """从唯一等长 k-mer 构造 node-centric de Bruijn 图。

    参数：kmers 为大写 DNA k-mer 列表。
    返回值：KmerGraph。
    边界情况：空列表返回空图；长度不一致、k<2 或非法字符抛出 ValueError。
    关键算法点：只有当左节点后缀与右节点前缀完全相等时才连边。
    """

    unique = tuple(sorted(dict.fromkeys(kmers)))
    if not unique:
        return KmerGraph((), {}, {}, {})
    k = len(unique[0])
    if k < 2:
        raise ValueError("k-mer 长度必须至少为 2")
    adjacency_lists = {node: [] for node in unique}
    indegree = {node: 0 for node in unique}
    outdegree = {node: 0 for node in unique}
    for left in unique:
        if len(left) != k:
            raise ValueError("所有 k-mer 必须等长")
        if any(symbol not in DNA for symbol in left):
            raise ValueError("k-mer 只能包含大写 DNA 字符")
    for left in unique:
        suffix = left[1:]
        for right in unique:
            if left != right and suffix == right[:-1]:
                adjacency_lists[left].append(right)
                indegree[right] += 1
                outdegree[left] += 1
    adjacency = {node: tuple(targets) for node, targets in adjacency_lists.items()}
    return KmerGraph(unique, adjacency, indegree, outdegree)


def maximal_unitigs(graph: KmerGraph) -> list[list[str]]:
    """提取图中的所有 maximal unitig 路径。

    参数：graph 为 build_node_centric_dbg 返回的图。
    返回值：每条 unitig 表示为 k-mer 节点路径。
    边界情况：纯 1 入 1 出环会作为单独 unitig 返回一个循环位移表示。
    关键算法点：以边为消费对象，而不是以节点为消费对象，避免分叉节点出边丢失。
    """

    used_edges: set[tuple[str, str]] = set()
    unitigs: list[list[str]] = []
    for node in graph.nodes:
        if graph.outdegree.get(node, 0) == 0 or _is_one_in_one_out(graph, node):
            continue
        for target in graph.adjacency.get(node, ()):
            edge = (node, target)
            if edge in used_edges:
                continue
            unitigs.append(_consume_unitig(graph, edge, used_edges))
    for node in graph.nodes:
        for target in graph.adjacency.get(node, ()):
            edge = (node, target)
            if edge not in used_edges:
                unitigs.append(_consume_cycle(graph, edge, used_edges))
    return unitigs


def compact_dbg(kmers: list[str]) -> CompactedDBG:
    """把 node-centric de Bruijn 图压缩成 compacted DBG。

    参数：kmers 为唯一等长 k-mer 列表。
    返回值：CompactedDBG。
    边界情况：空输入返回空压缩图。
    关键算法点：先求 maximal unitig，再把原图跨 unitig 的边投影为压缩图边。
    """

    graph = build_node_centric_dbg(kmers)
    paths = maximal_unitigs(graph)
    unitigs = tuple(_spell_path(path) for path in paths)
    owner: dict[str, int] = {}
    for index, path in enumerate(paths):
        for node in path:
            owner[node] = index
    adjacency_sets = {index: set() for index in range(len(paths))}
    for source in graph.nodes:
        for target in graph.adjacency.get(source, ()):
            left = owner[source]
            right = owner[target]
            if left != right:
                adjacency_sets[left].add(right)
    adjacency = {index: tuple(sorted(targets)) for index, targets in adjacency_sets.items()}
    return CompactedDBG(unitigs, adjacency)


def _consume_unitig(graph: KmerGraph, first_edge: tuple[str, str], used_edges: set[tuple[str, str]]) -> list[str]:
    """从一条边开始扩展 maximal unitig。"""

    source, target = first_edge
    used_edges.add(first_edge)
    path = [source, target]
    current = target
    while _is_one_in_one_out(graph, current):
        next_target = next(candidate for candidate in graph.adjacency[current] if (current, candidate) not in used_edges)
        used_edges.add((current, next_target))
        path.append(next_target)
        current = next_target
    return path


def _consume_cycle(graph: KmerGraph, first_edge: tuple[str, str], used_edges: set[tuple[str, str]]) -> list[str]:
    """提取纯 1 入 1 出环。"""

    source, target = first_edge
    used_edges.add(first_edge)
    path = [source, target]
    current = target
    while current != source:
        next_target = next(candidate for candidate in graph.adjacency[current] if (current, candidate) not in used_edges)
        used_edges.add((current, next_target))
        if next_target == source:
            break
        path.append(next_target)
        current = next_target
    return path


def _spell_path(path: list[str]) -> str:
    """把 k-mer 节点路径拼回 unitig 字符串。"""

    return path[0] + "".join(node[-1] for node in path[1:]) if path else ""


def _is_one_in_one_out(graph: KmerGraph, node: str) -> bool:
    """判断节点是否是 1 入 1 出内部节点。"""

    return graph.indegree.get(node, 0) == 1 and graph.outdegree.get(node, 0) == 1


if __name__ == "__main__":
    graph = build_node_centric_dbg(["AAG", "AGT", "GTC", "GTG", "TGA"])
    assert graph.outdegree["AAG"] == 1
    assert graph.indegree["TGA"] == 1
    paths = maximal_unitigs(graph)
    assert sorted(_spell_path(path) for path in paths) == ["AAGT", "AGTC", "AGTGA"]
    compacted = compact_dbg(["AAG", "AGT", "GTC", "GTG", "TGA"])
    assert sorted(compacted.unitigs) == ["AAGT", "AGTC", "AGTGA"]
    cycle = compact_dbg(["ATG", "TGA", "GAT"])
    assert cycle.unitigs == ("ATGAT",)
    assert compact_dbg([]).unitigs == ()
    try:
        build_node_centric_dbg(["AAA", "TT"])
        raise AssertionError("应拒绝不等长 k-mer")
    except ValueError:
        pass
    print("031_unitig_compaction: all examples passed")
