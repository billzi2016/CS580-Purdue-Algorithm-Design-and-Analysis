"""Viterbi 解码在 HMM 基因分型中的教学实现。

适用场景：
- 隐状态表示未知基因型、单倍型块状态或其他离散生物学状态；
- 观测序列表示每个位点读到的等位基因类别、简化测序符号或离散化证据；
- 需要求出给定观测下最可能的整条隐藏状态路径。

核心思想：
- 对每个位置、每个隐状态维护“以该状态结尾的最优路径对数概率”；
- 转移时枚举前一状态，选择对数概率最大的那一条；
- 通过回溯指针恢复全局最优路径。

输入输出：
- 输入：观测序列、状态集合、初始概率、转移概率、发射概率；
- 输出：最优隐藏状态路径及其对数概率。

时间复杂度：O(T * S^2)，其中 T 为观测长度，S 为状态数。
空间复杂度：O(T * S)。

关键边界情况：
- 空观测序列返回空路径和 0 对数概率；
- 概率为 0 的边会被视为不可达；
- 若某个观测在某状态下没有发射概率，视为 0；
- 这是离散教学版，不处理连续发射、缩放因子或复杂测序误差模型。
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, log


@dataclass(frozen=True)
class ViterbiResult:
    """Viterbi 解码结果。"""

    states: tuple[str, ...]
    log_probability: float


def viterbi_decode(
    observations: list[str],
    states: list[str],
    start_probability: dict[str, float],
    transition_probability: dict[str, dict[str, float]],
    emission_probability: dict[str, dict[str, float]],
) -> ViterbiResult:
    """用 Viterbi 算法求最可能隐藏状态路径。

    参数：
    - observations：离散观测序列；
    - states：隐藏状态列表；
    - start_probability：初始状态分布；
    - transition_probability：状态转移概率；
    - emission_probability：状态到观测符号的发射概率。

    返回值：
    - `ViterbiResult`，包含最优路径和对应对数概率。

    边界情况：
    - 空观测直接返回空路径；
    - 若任一时刻所有状态都不可达，会抛出 `ValueError`；
    - 缺失的转移或发射概率按 0 处理。

    关键算法点：
    - 在乘法概率链上使用对数，把连乘改写成连加，避免数值下溢；
    - `backpointer[t][state]` 记录第 `t` 位到达 `state` 的最佳前驱状态。
    """

    _validate_hmm(states, start_probability, transition_probability, emission_probability)

    if not observations:
        return ViterbiResult(states=(), log_probability=0.0)

    negative_infinity = float("-inf")
    score_table: list[dict[str, float]] = []
    backpointer: list[dict[str, str | None]] = []

    first_scores: dict[str, float] = {}
    first_previous: dict[str, str | None] = {}
    first_observation = observations[0]

    for state in states:
        initial_score = _safe_log(start_probability.get(state, 0.0))
        emission_score = _safe_log(emission_probability.get(state, {}).get(first_observation, 0.0))
        first_scores[state] = initial_score + emission_score
        first_previous[state] = None

    if all(score == negative_infinity for score in first_scores.values()):
        raise ValueError("首个观测在所有状态下都不可达")

    score_table.append(first_scores)
    backpointer.append(first_previous)

    for position in range(1, len(observations)):
        observation = observations[position]
        current_scores: dict[str, float] = {}
        current_previous: dict[str, str | None] = {}

        for current_state in states:
            emission_score = _safe_log(
                emission_probability.get(current_state, {}).get(observation, 0.0)
            )
            best_score = negative_infinity
            best_previous_state: str | None = None

            for previous_state in states:
                previous_score = score_table[position - 1][previous_state]
                transition_score = _safe_log(
                    transition_probability.get(previous_state, {}).get(current_state, 0.0)
                )
                candidate_score = previous_score + transition_score + emission_score
                if candidate_score > best_score:
                    best_score = candidate_score
                    best_previous_state = previous_state

            current_scores[current_state] = best_score
            current_previous[current_state] = best_previous_state

        if all(score == negative_infinity for score in current_scores.values()):
            raise ValueError(f"第 {position} 个观测在所有状态下都不可达")

        score_table.append(current_scores)
        backpointer.append(current_previous)

    final_state = max(states, key=lambda state: score_table[-1][state])
    final_score = score_table[-1][final_state]

    decoded_states = [final_state]
    current_state = final_state
    for position in range(len(observations) - 1, 0, -1):
        previous_state = backpointer[position][current_state]
        if previous_state is None:
            raise ValueError("回溯失败：路径在中途断裂")
        decoded_states.append(previous_state)
        current_state = previous_state

    decoded_states.reverse()
    return ViterbiResult(states=tuple(decoded_states), log_probability=final_score)


def _validate_hmm(
    states: list[str],
    start_probability: dict[str, float],
    transition_probability: dict[str, dict[str, float]],
    emission_probability: dict[str, dict[str, float]],
) -> None:
    """校验 HMM 概率表是否合法。"""

    if not states:
        raise ValueError("状态集合不能为空")
    if len(set(states)) != len(states):
        raise ValueError("状态集合不能包含重复项")

    _validate_probability_row(start_probability, "初始概率")

    for state in states:
        if state not in transition_probability:
            raise ValueError(f"缺少状态 {state} 的转移概率")
        if state not in emission_probability:
            raise ValueError(f"缺少状态 {state} 的发射概率")
        _validate_probability_row(transition_probability[state], f"状态 {state} 的转移概率")
        _validate_probability_row(emission_probability[state], f"状态 {state} 的发射概率")


def _validate_probability_row(probabilities: dict[str, float], row_name: str) -> None:
    """校验一行离散概率是否在容差内归一化。"""

    if not probabilities:
        raise ValueError(f"{row_name}不能为空")

    total = 0.0
    for label, probability in probabilities.items():
        if probability < 0.0 or probability > 1.0:
            raise ValueError(f"{row_name} 中 {label} 的概率必须位于 [0, 1]")
        total += probability

    if not isclose(total, 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError(f"{row_name} 之和必须为 1，当前为 {total}")


def _safe_log(probability: float) -> float:
    """把概率转成对数；0 概率映射为负无穷。"""

    if probability < 0.0 or probability > 1.0:
        raise ValueError("概率必须位于 [0, 1]")
    if probability == 0.0:
        return float("-inf")
    return log(probability)


if __name__ == "__main__":
    hidden_states = ["RR", "RA", "AA"]
    start = {"RR": 0.85, "RA": 0.15, "AA": 0.0}
    transition = {
        "RR": {"RR": 0.75, "RA": 0.25, "AA": 0.0},
        "RA": {"RR": 0.15, "RA": 0.7, "AA": 0.15},
        "AA": {"RR": 0.0, "RA": 0.25, "AA": 0.75},
    }
    emission = {
        "RR": {"ref": 0.92, "alt": 0.08},
        "RA": {"ref": 0.5, "alt": 0.5},
        "AA": {"ref": 0.08, "alt": 0.92},
    }

    decoded = viterbi_decode(["ref", "ref", "alt", "alt", "alt", "alt"], hidden_states, start, transition, emission)
    assert decoded.states == ("RR", "RR", "RA", "AA", "AA", "AA")
    assert decoded.log_probability < 0.0

    empty = viterbi_decode([], hidden_states, start, transition, emission)
    assert empty == ViterbiResult(states=(), log_probability=0.0)

    try:
        viterbi_decode(
            ["unknown"],
            hidden_states,
            start,
            transition,
            emission,
        )
        raise AssertionError("未知观测应导致不可达异常")
    except ValueError:
        pass

    print("032_viterbi_hmm_genotyping: all examples passed")
