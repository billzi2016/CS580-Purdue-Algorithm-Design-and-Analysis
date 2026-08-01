"""将直线三地址代码重命名为静态单赋值（SSA）形式。

适用场景：理解 SSA 的变量版本化核心。核心思想：每次定义产生新版本，随后使用读取最新版本。
输入输出：输入 ``Assignment`` 顺序列表，输出版本化赋值。时间 O(n)，空间 O(变量数)。
边界：这是直线代码基础版，明确不处理 CFG 汇合点、φ 函数、别名、数组或内存 SSA。
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Assignment:
    """一条三地址赋值：目标由操作数和零至两个源操作数计算。"""
    target: str
    operator: str
    operands: tuple[str, ...]


def rename_to_ssa(assignments: list[Assignment]) -> list[Assignment]:
    """将直线代码改写为 SSA 版本名。

    未定义变量的首次使用写为 ``name_0``，便于表示来自过程入口的初值；每次定义版本递增。
    """
    versions: dict[str, int] = {}
    result: list[Assignment] = []
    for assignment in assignments:
        renamed_operands = tuple(_current_name(name, versions) for name in assignment.operands)
        versions[assignment.target] = versions.get(assignment.target, 0) + 1
        result.append(Assignment(f"{assignment.target}_{versions[assignment.target]}", assignment.operator, renamed_operands))
    return result


def _current_name(name: str, versions: dict[str, int]) -> str:
    return f"{name}_{versions.get(name, 0)}"


if __name__ == "__main__":
    source = [Assignment("x", "=", ("a",)), Assignment("x", "+", ("x", "b")), Assignment("y", "*", ("x", "x"))]
    ssa = rename_to_ssa(source)
    assert ssa == [Assignment("x_1", "=", ("a_0",)), Assignment("x_2", "+", ("x_1", "b_0")), Assignment("y_1", "*", ("x_2", "x_2"))]
    assert rename_to_ssa([]) == []
    print("012_static_single_assignment: all examples passed")
