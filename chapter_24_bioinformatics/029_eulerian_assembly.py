"""欧拉路径组装建模的教学实现。

适用场景：给定无错误 DNA k-mer 多重集，构造 de Bruijn 多重图，并在满足欧拉路径条件时
用 Hierholzer 算法恢复一条覆盖每条边恰好一次的装配串。
核心思想：节点是 (k-1)-mer，边是 k-mer；若图在非零度节点上连通且度数满足欧拉路径条件，
则边序列可以重建一条候选基因组字符串。
输入输出：输入为 k-mer 列表，输出一条教学版装配序列。
时间复杂度：建图与求路均为 O(E + V)，其中 E 是 k-mer 条数。
空间复杂度：O(E + V)。
关键边界情况：空输入返回空串；这是精确图遍历教学版，不处理测序错误、coverage 剪枝、
反向互补折叠、分型约束或 Pevzner euler 文中更复杂的 Eulerian superpath 约束。
"""

from dataclasses import dataclass

DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class EulerianDeBruijnGraph:
    """用于欧拉遍历的 de Bruijn 多重图。

    参数：adjacency 按源点保存目标点列表，indegree/outdegree 记录度数，edge_count 是总边数。
    返回值：供度数检查与 Hierholzer 遍历复用的图结构。
    边界情况：允许平行边；空图允许空字典。
    关键算法点：邻接表保留重复目标节点，避免把平行边错误折叠为一条边。
    """

    adjacency: dict[str, tuple[str, ...]]
    indegree: dict[str, int]
    outdegree: dict[str, int]
    edge_count: int


def build_kmer_graph(kmers: list[str]) -> EulerianDeBruijnGraph:
    """从等长 k-mer 多重集构造 de Bruijn 图。

    参数：kmers 为非空等长 DNA 串列表；允许重复，重复代表边的多重性。
    返回值：EulerianDeBruijnGraph。
    边界情况：空列表返回空图；长度不一致、k<2 或存在非法字符时抛出 ValueError。
    关键算法点：每个 k-mer 独立映射为 prefix->suffix 一条边，因此多重集中的重复出现会被保留。
    """

    if not kmers:
        return EulerianDeBruijnGraph({}, {}, {}, 0)
    k = len(kmers[0])
    if k < 2:
        raise ValueError("k-mer 长度必须至少为 2")
    adjacency_lists: dict[str, list[str]] = {}
    indegree: dict[str, int] = {}
    outdegree: dict[str, int] = {}
    for kmer in kmers:
        if len(kmer) != k:
            raise ValueError("所有 k-mer 必须等长")
        if any(symbol not in DNA for symbol in kmer):
            raise ValueError("k-mer 只能包含大写 DNA 字符")
        source = kmer[:-1]
        target = kmer[1:]
        adjacency_lists.setdefault(source, []).append(target)
        adjacency_lists.setdefault(target, [])
        indegree[source] = indegree.get(source, 0)
        indegree[target] = indegree.get(target, 0) + 1
        outdegree[source] = outdegree.get(source, 0) + 1
        outdegree[target] = outdegree.get(target, 0)
    adjacency = {node: tuple(targets) for node, targets in adjacency_lists.items()}
    return EulerianDeBruijnGraph(adjacency, indegree, outdegree, len(kmers))


def find_eulerian_path(graph: EulerianDeBruijnGraph) -> list[str]:
    """在满足条件的 de Bruijn 图中找一条欧拉路径。

    参数：graph 为 build_kmer_graph 的结果。
    返回值：按访问顺序排列的节点路径；若无边则返回空列表。
    边界情况：不存在欧拉路径、非零度节点不连通或遍历后边未消费完都会抛出 ValueError。
    关键算法点：先检查度数条件与弱连通性，再用 Hierholzer 算法在多重边图中线性构造路径。
    """

    if graph.edge_count == 0:
        return []
    start = _choose_start_node(graph)
    _validate_connectivity(graph, start)
    remaining = {
        node: list(reversed(targets)) for node, targets in graph.adjacency.items()
    }
    stack = [start]
    path: list[str] = []
    while stack:
        node = stack[-1]
        if remaining.get(node):
            stack.append(remaining[node].pop())
        else:
            path.append(stack.pop())
    if len(path) != graph.edge_count + 1:
        raise ValueError("图不满足欧拉路径条件，无法覆盖全部边")
    path.reverse()
    return path


def assemble_from_kmers(kmers: list[str]) -> str:
    """从 k-mer 多重集恢复一条教学版装配串。

    参数：kmers 为等长 DNA k-mer 列表。
    返回值：一条覆盖每个 k-mer 一次的候选字符串；空输入返回空串。
    边界情况：若图不满足欧拉路径条件则抛出 ValueError。
    关键算法点：节点路径的第一个节点提供前缀，其后每个节点仅追加最后一个字符。
    """

    path = find_eulerian_path(build_kmer_graph(kmers))
    if not path:
        return ""
    return path[0] + "".join(node[-1] for node in path[1:])


def spectrum_from_reads(reads: list[str], k: int) -> list[str]:
    """把 reads 展开为 k-mer 频谱。

    参数：reads 为 DNA reads，k 为正整数且至少为 2。
    返回值：按输入顺序展开的 k-mer 列表。
    边界情况：长度小于 k 的 read 会被忽略；非法字符或非法 k 抛出 ValueError。
    关键算法点：这里只做窗口枚举，不做去重，因为欧拉建模依赖多重集计数。
    """

    if k < 2:
        raise ValueError("k 必须至少为 2")
    if any(any(symbol not in DNA for symbol in read) for read in reads):
        raise ValueError("reads 只能包含大写 DNA 字符")
    kmers: list[str] = []
    for read in reads:
        for start in range(max(0, len(read) - k + 1)):
            kmers.append(read[start : start + k])
    return kmers


def _choose_start_node(graph: EulerianDeBruijnGraph) -> str:
    """根据度数条件选择欧拉路径起点。"""

    start_candidates = [
        node
        for node in graph.adjacency
        if graph.outdegree.get(node, 0) - graph.indegree.get(node, 0) == 1
    ]
    end_candidates = [
        node
        for node in graph.adjacency
        if graph.indegree.get(node, 0) - graph.outdegree.get(node, 0) == 1
    ]
    invalid = [
        node
        for node in graph.adjacency
        if abs(graph.outdegree.get(node, 0) - graph.indegree.get(node, 0)) > 1
    ]
    if (
        invalid
        or len(start_candidates) not in (0, 1)
        or len(end_candidates) not in (0, 1)
    ):
        raise ValueError("图不满足欧拉路径的度数条件")
    if start_candidates:
        return start_candidates[0]
    return min(
        (node for node in graph.adjacency if graph.outdegree.get(node, 0) > 0),
        default="",
    )


def _validate_connectivity(graph: EulerianDeBruijnGraph, start: str) -> None:
    """验证所有非零度节点在忽略方向后与起点连通。"""

    undirected: dict[str, set[str]] = {node: set() for node in graph.adjacency}
    for source, targets in graph.adjacency.items():
        for target in targets:
            undirected[source].add(target)
            undirected[target].add(source)
    active = {
        node
        for node in graph.adjacency
        if graph.indegree.get(node, 0) + graph.outdegree.get(node, 0) > 0
    }
    if not active:
        return
    seen = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        for neighbor in undirected[node]:
            if neighbor not in seen:
                seen.add(neighbor)
                stack.append(neighbor)
    if not active.issubset(seen):
        raise ValueError("非零度节点不连通，无法形成单条欧拉路径")


if __name__ == "__main__":
    kmers = ["AAG", "AGA", "GAT", "ATT", "TTC", "TCT", "CTA"]
    graph = build_kmer_graph(kmers)
    assert graph.edge_count == 7
    assert find_eulerian_path(graph) == ["AA", "AG", "GA", "AT", "TT", "TC", "CT", "TA"]
    assert assemble_from_kmers(kmers) == "AAGATTCTA"
    assert assemble_from_kmers(["ATG", "TGA", "GAT"]) == "ATGAT"
    assert spectrum_from_reads(["AAGA", "GATT"], 3) == ["AAG", "AGA", "GAT", "ATT"]
    assert assemble_from_kmers([]) == ""
    try:
        assemble_from_kmers(["AAA", "TT"])
        raise AssertionError("应拒绝不等长 k-mer")
    except ValueError:
        pass
    print("029_eulerian_assembly: all examples passed")
