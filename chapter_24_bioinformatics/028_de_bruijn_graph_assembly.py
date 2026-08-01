"""de Bruijn 图组装的教学实现。

适用场景：把无错误 DNA reads 分解为 k-mer，构造以前缀/后缀 (k-1)-mer 为节点的有向多重图，
并从非分叉路径中提取 contig。
核心思想：每个 k-mer 贡献一条 prefix->suffix 有向边；对所有不是 1 入 1 出的节点向外扩展，
再补充纯环，从而得到 unitig 风格的非分叉路径。
输入输出：输入 reads 与 k，输出图结构以及按字典序排列的 contig 列表。
时间复杂度：建图 O(T)，提取路径 O(E)，其中 T 为所有 reads 的总长度，E 为 k-mer 边数。
空间复杂度：O(E + V)。
关键边界情况：空输入返回空图与空 contig；这是教学版，不处理测序错误、覆盖度剪枝、反向互补折叠、
tip/bubble 清理或工业级的图简化策略。
"""

from dataclasses import dataclass

DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class DeBruijnEdge:
    """de Bruijn 多重图中的一条边。

    参数：identifier 是边编号，label 是原始 k-mer，source/target 是对应的 (k-1)-mer。
    返回值：不可变边记录。
    边界情况：重复 k-mer 会形成不同 identifier 的平行边，而不是被直接合并。
    关键算法点：保留边多重性，后续才能按“每条边恰好消费一次”提取非分叉路径。
    """

    identifier: int
    label: str
    source: str
    target: str


@dataclass(frozen=True)
class DeBruijnGraph:
    """教学版 de Bruijn 图。

    参数：nodes 是所有出现过的 (k-1)-mer；edges 是全部有向边；adjacency 保存每个源点的出边编号；
    indegree/outdegree 为节点度数。
    返回值：供路径提取复用的只读图结构。
    边界情况：无边图允许存在空节点集合。
    关键算法点：用边编号而不是目标字符串表示邻接表，避免平行边在遍历时丢失多重性。
    """

    nodes: tuple[str, ...]
    edges: tuple[DeBruijnEdge, ...]
    adjacency: dict[str, tuple[int, ...]]
    indegree: dict[str, int]
    outdegree: dict[str, int]


def build_de_bruijn_graph(reads: list[str], k: int) -> DeBruijnGraph:
    """从 reads 构造以 (k-1)-mer 为节点、k-mer 为边的有向多重图。

    参数：reads 为只含大写 DNA 的字符串列表，k 为正整数且至少为 2。
    返回值：包含节点、边、邻接表和度数的 DeBruijnGraph。
    边界情况：空输入返回空图；长度小于 k 的 read 会被忽略；非法字符或非法 k 抛出 ValueError。
    关键算法点：每个长度为 k 的窗口独立生成一条边，因此重复覆盖会保留为多条平行边。
    """

    if k < 2:
        raise ValueError("k 必须至少为 2")
    _validate_reads(reads)
    edges: list[DeBruijnEdge] = []
    adjacency_lists: dict[str, list[int]] = {}
    indegree: dict[str, int] = {}
    outdegree: dict[str, int] = {}
    nodes: set[str] = set()
    for read in reads:
        if len(read) < k:
            continue
        for start in range(len(read) - k + 1):
            label = read[start : start + k]
            source = label[:-1]
            target = label[1:]
            edge = DeBruijnEdge(len(edges), label, source, target)
            edges.append(edge)
            adjacency_lists.setdefault(source, []).append(edge.identifier)
            adjacency_lists.setdefault(target, [])
            indegree[source] = indegree.get(source, 0)
            indegree[target] = indegree.get(target, 0) + 1
            outdegree[source] = outdegree.get(source, 0) + 1
            outdegree[target] = outdegree.get(target, 0)
            nodes.add(source)
            nodes.add(target)
    adjacency = {node: tuple(edge_ids) for node, edge_ids in adjacency_lists.items()}
    for node in nodes:
        indegree.setdefault(node, 0)
        outdegree.setdefault(node, 0)
        adjacency.setdefault(node, ())
    return DeBruijnGraph(tuple(sorted(nodes)), tuple(edges), adjacency, indegree, outdegree)


def extract_non_branching_contigs(graph: DeBruijnGraph) -> list[str]:
    """从 de Bruijn 图中提取非分叉路径对应的 contig。

    参数：graph 为 build_de_bruijn_graph 返回的图。
    返回值：所有 contig，按字典序排序。
    边界情况：空图返回空列表；纯 1 入 1 出环会作为单独 contig 补充提取。
    关键算法点：先从所有非 1 入 1 出节点出发消费边，再扫描剩余未消费边构造纯环，
    从而保证每条边恰好进入一条输出路径。
    """

    used_edges = [False] * len(graph.edges)
    contigs: list[str] = []
    for node in graph.nodes:
        if graph.outdegree.get(node, 0) == 0 or _is_one_in_one_out(graph, node):
            continue
        for edge_id in graph.adjacency.get(node, ()):
            if used_edges[edge_id]:
                continue
            contigs.append(_consume_path(graph, edge_id, used_edges))
    for edge in graph.edges:
        if used_edges[edge.identifier]:
            continue
        contigs.append(_consume_cycle(graph, edge.identifier, used_edges))
    return sorted(contigs)


def assemble_de_bruijn(reads: list[str], k: int) -> list[str]:
    """执行教学版 de Bruijn 图组装并返回 contig。

    参数：reads 为 DNA reads，k 为 k-mer 长度。
    返回值：按字典序排序的 contig 列表。
    边界情况：所有 read 都短于 k 时返回空列表。
    关键算法点：本函数只负责串联“建图”和“非分叉路径提取”，不尝试在分叉处猜测唯一基因组路径。
    """

    return extract_non_branching_contigs(build_de_bruijn_graph(reads, k))


def _consume_path(graph: DeBruijnGraph, first_edge_id: int, used_edges: list[bool]) -> str:
    """从一条出边开始扩展非分叉路径并返回拼接后的 contig。"""

    edge = graph.edges[first_edge_id]
    used_edges[first_edge_id] = True
    symbols = [edge.source, edge.target[-1]]
    current = edge.target
    while _is_one_in_one_out(graph, current):
        next_edge_id = next(identifier for identifier in graph.adjacency[current] if not used_edges[identifier])
        next_edge = graph.edges[next_edge_id]
        used_edges[next_edge_id] = True
        symbols.append(next_edge.target[-1])
        current = next_edge.target
    return "".join(symbols)


def _consume_cycle(graph: DeBruijnGraph, first_edge_id: int, used_edges: list[bool]) -> str:
    """提取剩余的纯 1 入 1 出环。"""

    edge = graph.edges[first_edge_id]
    used_edges[first_edge_id] = True
    symbols = [edge.source, edge.target[-1]]
    start = edge.source
    current = edge.target
    while current != start:
        next_edge_id = next(identifier for identifier in graph.adjacency[current] if not used_edges[identifier])
        next_edge = graph.edges[next_edge_id]
        used_edges[next_edge_id] = True
        symbols.append(next_edge.target[-1])
        current = next_edge.target
    return "".join(symbols)


def _is_one_in_one_out(graph: DeBruijnGraph, node: str) -> bool:
    """判断节点是否是 1 入 1 出内部节点。"""

    return graph.indegree.get(node, 0) == 1 and graph.outdegree.get(node, 0) == 1


def _validate_reads(reads: list[str]) -> None:
    """验证 reads 只包含大写 DNA 碱基。"""

    if any(any(symbol not in DNA for symbol in read) for read in reads):
        raise ValueError("reads 只能包含大写 DNA 字符")


if __name__ == "__main__":
    graph = build_de_bruijn_graph(["AAG", "AGA", "GAT", "ATT", "TTC", "TCT", "CTA"], 3)
    assert graph.outdegree["AA"] == 1
    assert graph.indegree["CT"] == 1
    assert assemble_de_bruijn(["AAG", "AGA", "GAT", "ATT", "TTC", "TCT", "CTA"], 3) == ["AAGATTCTA"]
    assert len(assemble_de_bruijn(["AAGA", "AGAT", "GATT"], 3)) > 1
    assert assemble_de_bruijn(["ATG", "TGA", "GAT"], 3) == ["ATGAT"]
    assert assemble_de_bruijn([], 3) == []
    assert assemble_de_bruijn(["AA"], 3) == []
    try:
        build_de_bruijn_graph(["AXA"], 2)
        raise AssertionError("应拒绝非法 DNA 字符")
    except ValueError:
        pass
    print("028_de_bruijn_graph_assembly: all examples passed")
