"""
文件意图：手写计算有限有向无环公平游戏的 Sprague-Grundy 值并判断组合局面胜负。
适用场景：正常玩法下、双方可走步骤相同、没有随机性的无环组合游戏。
核心思想：状态的 Grundy 值是所有后继值集合的 mex；独立子游戏的总值是这些值的异或。
输入输出：输入 DAG 邻接表和若干起始状态，输出每个状态的 Grundy 值或组合局面胜负。
时间复杂度：O(V+E+Σ d_v)，空间复杂度 O(V)，其中 d_v 为后继 Grundy 值去重前的数量。
关键边界情况：图有环、非法后继编号会被拒绝；终止状态的 mex 为空集合，值为 0。
"""


def mex(values: set[int]) -> int:
    """返回非负整数集合中未出现的最小值。"""
    candidate = 0
    while candidate in values:
        candidate += 1
    return candidate


def grundy_values(game_graph: list[list[int]]) -> list[int]:
    """计算每个 DAG 状态的 Sprague-Grundy 值。

    参数：game_graph[v] 列出从状态 v 一步可达的后继状态。
    返回：与图等长的 Grundy 值列表。
    边界情况：空图返回空；自环、环或越界边抛出 ValueError。
    关键算法点：DFS 后序确保计算状态 v 时，所有后继的 Grundy 值已经确定。
    """
    state_count = len(game_graph)
    values = [0] * state_count
    colors = [0] * state_count

    def visit(state: int) -> None:
        if colors[state] == 1:
            raise ValueError("Sprague-Grundy 教学实现只接受无环游戏图")
        if colors[state] == 2:
            return
        colors[state] = 1
        successor_values: set[int] = set()
        for successor in game_graph[state]:
            if not 0 <= successor < state_count:
                raise ValueError("后继状态编号超出范围")
            visit(successor)
            successor_values.add(values[successor])
        # 终止状态没有后继，其后继值集合为空，因此 mex 为零。
        values[state] = mex(successor_values)
        colors[state] = 2

    for state in range(state_count):
        visit(state)
    return values


def is_winning_sum(game_graph: list[list[int]], positions: list[int]) -> bool:
    """判断多个独立游戏状态的直和是否为必胜局面。

    参数：game_graph 是无环游戏图；positions 是每个独立子游戏的当前状态。
    返回：所有对应 Grundy 值异或非零时返回真。
    边界情况：positions 为空时返回假；非法状态编号抛出 ValueError。
    关键算法点：Sprague-Grundy 定理将直和游戏等价为堆大小等于 Grundy 值的 Nim。
    """
    values = grundy_values(game_graph)
    total = 0
    for position in positions:
        if not 0 <= position < len(values):
            raise ValueError("position 编号超出范围")
        total ^= values[position]
    return total != 0


if __name__ == "__main__":
    graph = [[1, 2], [3], [3], []]
    assert grundy_values(graph) == [0, 1, 1, 0]
    assert is_winning_sum(graph, [1])
    assert not is_winning_sum(graph, [1, 2])
    assert not is_winning_sum(graph, [])
    try:
        grundy_values([[1], [0]])
        raise AssertionError("有环游戏图应抛出 ValueError")
    except ValueError:
        pass
    print("002_sprague_grundy: all examples passed")
