"""
文件意图：
    本文件手写实现有向无环图（DAG）的拓扑排序。

适用场景：
    任务依赖排序、课程先修关系、编译依赖、DAG 动态规划前置排序。

核心思想：
    使用 Kahn 算法维护入度为 0 的节点队列。每弹出一个节点，就删除它的
    出边并降低后继节点入度。如果最终无法处理所有节点，说明图中存在环。

输入输出：
    输入有向图邻接表，返回一个合法拓扑序。

时间复杂度：
    O(V + E)

空间复杂度：
    O(V)
"""

from collections import deque
from collections.abc import Hashable

Node = Hashable
Graph = dict[Node, list[Node]]


def topological_sort(graph: Graph) -> list[Node]:
    """
    对有向图执行拓扑排序。

    参数：
        graph: 有向图邻接表。

    返回：
        一个合法拓扑序。

    异常：
        如果图中存在环，抛出 ValueError。
    """
    nodes = _collect_all_nodes(graph)
    indegree = {node: 0 for node in nodes}

    for node in nodes:
        for neighbor in graph.get(node, []):
            indegree[neighbor] += 1

    queue: deque[Node] = deque([node for node in nodes if indegree[node] == 0])
    order: list[Node] = []

    while queue:
        current = queue.popleft()
        order.append(current)

        for neighbor in graph.get(current, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(nodes):
        raise ValueError("有向图存在环，无法生成拓扑序")

    return order


def is_valid_topological_order(graph: Graph, order: list[Node]) -> bool:
    """
    验证 order 是否是 graph 的合法拓扑序。
    """
    position = {node: index for index, node in enumerate(order)}
    if len(position) != len(order):
        return False

    for node, neighbors in graph.items():
        if node not in position:
            return False
        for neighbor in neighbors:
            if neighbor not in position or position[node] >= position[neighbor]:
                return False

    return True


def _collect_all_nodes(graph: Graph) -> list[Node]:
    """
    收集 key 和邻接表值中出现的所有节点。
    """
    nodes: list[Node] = []
    seen: set[Node] = set()

    for node, neighbors in graph.items():
        if node not in seen:
            nodes.append(node)
            seen.add(node)
        for neighbor in neighbors:
            if neighbor not in seen:
                nodes.append(neighbor)
                seen.add(neighbor)

    return nodes


if __name__ == "__main__":
    dag = {
        "cook": ["eat"],
        "shop": ["cook"],
        "study": ["exam"],
        "eat": [],
        "exam": [],
    }
    order = topological_sort(dag)
    assert is_valid_topological_order(dag, order)
    assert topological_sort({}) == []

    value_only_node_graph = {"A": ["B"], "B": ["C"]}
    assert is_valid_topological_order(value_only_node_graph, topological_sort(value_only_node_graph))

    try:
        topological_sort({"A": ["B"], "B": ["A"]})
        raise AssertionError("有环图必须抛出 ValueError")
    except ValueError:
        pass

    print("004_topological_sort: all examples passed")
