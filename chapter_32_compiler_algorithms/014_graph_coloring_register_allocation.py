"""用简化—选择图着色法做基础寄存器分配。

适用场景：将变量干涉图映射到有限寄存器。核心思想：反复移除度小于 K 的节点，逆序放回并选取未被邻居使用的颜色。
输入输出：输入无向干涉图和寄存器数，输出变量到寄存器编号的映射及无法着色的 spill 集。
时间复杂度：朴素实现 O(V²+E)；空间复杂度 O(V+E)。
边界：图须对称；高阶节点可能 spill；这是基础分配器，不含合并、重着色或 spill 代码插入。
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Allocation:
    """图着色分配结果，``spills`` 中变量没有被伪造为可用寄存器。"""
    registers: dict[str, int]
    spills: set[str]


def allocate_registers(interference: dict[str, set[str]], register_count: int) -> Allocation:
    """以简化—选择法为干涉图尝试 K-着色。

    参数：无向图与寄存器数 K。返回已着色变量和真正无法着色的 spill 集。
    关键点：先移除低度节点保证其放回时至少有一个空颜色；无低度节点时保守挑选候选节点。
    """
    if register_count <= 0:
        raise ValueError("寄存器数量必须为正")
    _validate_graph(interference)
    remaining = {node: set(neighbors) for node, neighbors in interference.items()}
    stack: list[str] = []
    while remaining:
        low_degree = next((node for node, neighbors in remaining.items() if len(neighbors) < register_count), None)
        node = low_degree if low_degree is not None else max(remaining, key=lambda item: len(remaining[item]))
        stack.append(node)
        for neighbor in remaining[node]:
            remaining[neighbor].remove(node)
        del remaining[node]
    registers: dict[str, int] = {}
    spills: set[str] = set()
    while stack:
        node = stack.pop()
        used = {registers[neighbor] for neighbor in interference[node] if neighbor in registers}
        available = next((color for color in range(register_count) if color not in used), None)
        if available is None:
            spills.add(node)
        else:
            registers[node] = available
    return Allocation(registers, spills)


def _validate_graph(graph: dict[str, set[str]]) -> None:
    for node, neighbors in graph.items():
        if node in neighbors or any(neighbor not in graph or node not in graph[neighbor] for neighbor in neighbors):
            raise ValueError("干涉图必须无自环且边必须对称")


if __name__ == "__main__":
    graph = {"a": {"b", "c"}, "b": {"a", "c"}, "c": {"a", "b", "d"}, "d": {"c"}}
    allocation = allocate_registers(graph, 3)
    assert not allocation.spills
    assert all(allocation.registers[node] != allocation.registers[neighbor] for node in allocation.registers for neighbor in graph[node] if neighbor in allocation.registers)
    triangle = {"x": {"y", "z"}, "y": {"x", "z"}, "z": {"x", "y"}}
    assert len(allocate_registers(triangle, 2).spills) == 1
    print("014_graph_coloring_register_allocation: all examples passed")
