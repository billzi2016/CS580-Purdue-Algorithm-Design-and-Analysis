"""用束搜索在分层状态空间中按启发式保留有限宽度的候选。

适用场景：序列生成、解码或固定深度树搜索。核心思想：每层扩展当前束，再只保留启发式得分最高的 K 个状态。
输入输出：输入起点、展开函数、评分和深度，输出最佳末层状态。时间 O(D×B×分支数)，空间 O(B)。
边界：束宽至少一；它不是完备搜索，可能剪掉全局最优路径。
"""

from __future__ import annotations
from collections.abc import Callable, Iterable
from typing import TypeVar


State = TypeVar("State")

def beam_search(initial: State, expand: Callable[[State], Iterable[State]], score: Callable[[State], float], width: int, depth: int) -> State:
    """执行固定深度的最大化束搜索，返回最后一层得分最高状态。"""
    if width < 1 or depth < 0:
        raise ValueError("束宽和深度无效")
    beam = [initial]
    for _ in range(depth):
        candidates = [child for state in beam for child in expand(state)]
        if not candidates:
            break
        candidates.sort(key=score, reverse=True)
        beam = candidates[:width]
    return max(beam, key=score)


if __name__ == "__main__":
    tree = {"S": ["A", "B"], "A": ["AA", "AB"], "B": ["BA", "BB"]}
    scores = {"S": 0, "A": 2, "B": 1, "AA": 3, "AB": 9, "BA": 4, "BB": 5}
    assert beam_search("S", lambda node: tree.get(node, []), scores.__getitem__, 2, 2) == "AB"
    assert beam_search("S", lambda _: [], scores.__getitem__, 1, 3) == "S"
    print("009_beam_search: all examples passed")
