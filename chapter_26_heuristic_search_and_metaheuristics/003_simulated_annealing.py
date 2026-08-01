"""使用模拟退火在离散状态空间中接受受控的暂时变差移动。

适用场景：存在局部最优、邻居可随机采样的组合优化。核心思想：改进必收下；变差以 exp(差值/温度) 的概率收下。
输入输出：输入起点、目标、随机邻居、温度日程，输出遇到过的最佳状态。
时间复杂度：O(I×C)，I 为迭代数、C 为目标计算成本；空间 O(1)。
边界情况：温度必须始终正；随机源可注入种子；返回历史最佳而非最后状态，避免退火末尾退步。
"""

from __future__ import annotations

import math
import random
from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar


State = TypeVar("State")


@dataclass(frozen=True)
class AnnealingResult:
    """模拟退火期间找到的最佳状态、分数和接受移动次数。"""

    state: object
    score: float
    accepted_moves: int


def simulated_annealing(
    initial_state: State,
    objective: Callable[[State], float],
    propose_neighbor: Callable[[State, random.Random], State],
    temperature: Callable[[int], float],
    iterations: int,
    seed: int | None = None,
) -> AnnealingResult:
    """最大化目标函数的模拟退火。

    参数：温度函数按迭代编号给出正温度。返回值是全过程最佳解。
    边界：迭代数可为零；任何非正温度立即报错，避免错误的接受概率。
    关键点：``delta < 0`` 时用指数概率接受，使高温阶段可跳出局部最优。
    """
    if iterations < 0:
        raise ValueError("迭代次数不能为负")
    generator = random.Random(seed)
    current = best = initial_state
    current_score = best_score = objective(current)
    accepted_moves = 0
    for step in range(iterations):
        current_temperature = temperature(step)
        if current_temperature <= 0:
            raise ValueError("温度必须始终为正")
        candidate = propose_neighbor(current, generator)
        candidate_score = objective(candidate)
        delta = candidate_score - current_score
        if delta >= 0 or generator.random() < math.exp(delta / current_temperature):
            current, current_score = candidate, candidate_score
            accepted_moves += 1
            if current_score > best_score:
                best, best_score = current, current_score
    return AnnealingResult(best, best_score, accepted_moves)


if __name__ == "__main__":

    def move(value: int, generator: random.Random) -> int:
        return max(0, min(10, value + generator.choice([-1, 1])))

    result = simulated_annealing(
        0,
        lambda value: -((value - 7) ** 2),
        move,
        lambda step: 5 / (step + 1),
        100,
        seed=3,
    )
    assert result.state == 7 and result.score == 0
    assert result.accepted_moves > 0
    zero_step = simulated_annealing(2, float, move, lambda _: 1, 0)
    assert zero_step.state == 2 and zero_step.score == 2
    print("003_simulated_annealing: all examples passed")
