"""为确定性双人零和游戏实现蒙特卡洛树搜索（MCTS）。

适用场景：分支大、难以设计静态评估的轮流游戏。核心思想：反复选择、扩展、随机模拟和反向传播。
输入输出：输入状态操作函数，输出根节点推荐动作。时间 O(模拟次数×模拟深度)，空间 O(展开节点数)。
边界：终局值须以根玩家视角返回 -1/0/1；基础版使用随机 rollout，不含置换表或神经网络。
"""

from __future__ import annotations
import math
import random
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Hashable, TypeVar

State = TypeVar("State", bound=Hashable)
Move = TypeVar("Move", bound=Hashable)

@dataclass
class _Node:
    state: State
    parent: "_Node | None" = None
    move: Move | None = None
    children: list["_Node"] = field(default_factory=list)
    untried: list[Move] = field(default_factory=list)
    visits: int = 0
    value: float = 0.0

def monte_carlo_tree_search(root_state: State, legal_moves: Callable[[State], list[Move]], apply_move: Callable[[State, Move], State], terminal_value: Callable[[State], float | None], simulations: int = 500, exploration: float = math.sqrt(2), seed: int | None = None) -> Move:
    """从根状态运行 MCTS，返回访问次数最多的根动作。"""
    if simulations < 1:
        raise ValueError("模拟次数至少为 1")
    if terminal_value(root_state) is not None:
        raise ValueError("终局状态没有可推荐动作")
    rng = random.Random(seed)
    root = _Node(root_state, untried=list(legal_moves(root_state)))
    for _ in range(simulations):
        node = root
        while not node.untried and node.children:
            node = max(node.children, key=lambda child: child.value / child.visits + exploration * math.sqrt(math.log(node.visits) / child.visits))
        if node.untried:
            move = node.untried.pop(rng.randrange(len(node.untried)))
            node = _Node(apply_move(node.state, move), node, move, untried=list(legal_moves(apply_move(node.state, move))))
            node.parent.children.append(node)
        rollout = node.state
        while terminal_value(rollout) is None:
            moves = legal_moves(rollout)
            rollout = apply_move(rollout, rng.choice(moves))
        reward = terminal_value(rollout)
        while node is not None:
            node.visits += 1
            node.value += float(reward)
            node = node.parent
    return max(root.children, key=lambda child: child.visits).move  # type: ignore[return-value]

if __name__ == "__main__":
    # 从剩余石子中取 1 或 2；取到最后一颗者获胜，状态为剩余石子数。
    move = monte_carlo_tree_search(3, lambda state: list(range(1, min(2, state) + 1)), lambda state, action: state - action, lambda state: 1.0 if state == 0 else None, simulations=300, seed=8)
    assert move == 1
    print("012_monte_carlo_tree_search: all examples passed")
