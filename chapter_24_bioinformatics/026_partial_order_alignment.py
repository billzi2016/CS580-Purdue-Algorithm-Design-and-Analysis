"""由等长 MSA 构造 partial-order alignment（POA）DAG 的教学实现。

适用场景：把已有多序列对齐转为可表达同列替代与跨列路径的有向无环图，并提取最大支持度共识路径。
核心思想：每个非 gap 的“列、碱基”组合是一个节点；每条输入行在其连续非 gap 节点间连边，节点权重为观测次数。
输入输出：输入等长 DNA/gap MSA，输出 POA 图与共识字符串。
时间复杂度 O(RC)，空间复杂度 O(RC)，R 为行数、C 为列数。
关键边界情况：空行与全 gap 列允许；这是从既有 MSA 建图的教学版，不执行序列对图的动态规划插入。
"""

from dataclasses import dataclass

DNA = frozenset("ACGTN")


@dataclass(frozen=True)
class POANode:
    """POA 节点：所属列、碱基与该碱基在该列的支持次数。"""

    column: int
    symbol: str
    support: int


@dataclass(frozen=True)
class POAGraph:
    """按列拓扑有序的节点与去重边。"""

    nodes: tuple[POANode, ...]
    edges: frozenset[tuple[int, int]]


def build_poa(alignment: list[str]) -> POAGraph:
    """从等长 MSA 构建 POA DAG。

    参数：alignment 是至少一行、只含 DNA/gap 的等长对齐。
    返回：节点按列和字符排序的 DAG；边连接每条原始对齐行相邻的非 gap 节点。
    边界情况：全 gap 列不生成节点；空行合法；非法或不等长输入抛出 ValueError。
    关键算法点：相同列的不同碱基没有直接边，因此每一条路径最多选择该列的一个替代节点。
    """
    _validate(alignment)
    identifiers: dict[tuple[int, str], int] = {}
    counts: dict[tuple[int, str], int] = {}
    for row in alignment:
        for column, symbol in enumerate(row):
            if symbol != "-":
                counts[(column, symbol)] = counts.get((column, symbol), 0) + 1
    for key in sorted(counts):
        identifiers[key] = len(identifiers)
    edges: set[tuple[int, int]] = set()
    for row in alignment:
        previous: int | None = None
        for column, symbol in enumerate(row):
            if symbol == "-":
                continue
            current = identifiers[(column, symbol)]
            if previous is not None:
                edges.add((previous, current))
            previous = current
    nodes = tuple(
        POANode(column, symbol, counts[(column, symbol)])
        for (column, symbol), _ in sorted(identifiers.items(), key=lambda item: item[1])
    )
    return POAGraph(nodes, frozenset(edges))


def consensus_path(graph: POAGraph) -> str:
    """在列有序 POA DAG 中找节点支持度之和最大的路径并返回其碱基串。

    参数：graph 是 build_poa 返回的 DAG。
    返回：一条最大支持路径；空图返回空串。
    边界情况：同分时保留较早拓扑节点，结果可复现。
    关键算法点：边只向更大列前进，按节点顺序处理即可完成 DAG 最长路径动态规划。
    """
    if not graph.nodes:
        return ""
    score = [node.support for node in graph.nodes]
    parent: list[int | None] = [None] * len(graph.nodes)
    for left, right in sorted(graph.edges, key=lambda edge: (edge[1], edge[0])):
        candidate = score[left] + graph.nodes[right].support
        if candidate > score[right]:
            score[right], parent[right] = candidate, left
    end = max(range(len(graph.nodes)), key=lambda index: score[index])
    path: list[str] = []
    while end is not None:
        path.append(graph.nodes[end].symbol)
        end = parent[end]
    return "".join(reversed(path))


def _validate(alignment: list[str]) -> None:
    """验证等长 DNA/gap MSA。"""
    if not alignment or len({len(row) for row in alignment}) != 1:
        raise ValueError("MSA 必须非空且所有行等长")
    if any(symbol not in DNA | {"-"} for row in alignment for symbol in row):
        raise ValueError("MSA 只允许 DNA 字符和 gap")


if __name__ == "__main__":
    graph = build_poa(["ACGT", "A-GT", "ACCT"])
    assert len(graph.nodes) == 5
    assert consensus_path(graph) == "ACGT"
    assert consensus_path(build_poa(["--", "--"])) == ""
    try:
        build_poa(["A", "AA"])
        raise AssertionError("应拒绝不等长 MSA")
    except ValueError:
        pass
    print("026_partial_order_alignment: all examples passed")
