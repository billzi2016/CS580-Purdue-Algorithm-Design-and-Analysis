"""HMM Forward-Backward 算法的教学实现。

适用场景：
- 需要求离散隐马尔可夫模型中每个位点的后验状态概率；
- 常见于简化版基因分型、拷贝数状态估计、序列标注等任务；
- 适合做 posterior decoding、软计数和 Baum-Welch 的基础构件。

核心思想：
- 前向概率累积“到当前位置为止生成观测前缀”的总概率；
- 后向概率累积“从当前位置继续生成剩余后缀”的总概率；
- 两者相乘并按位置归一化，就得到该位置每个状态的后验概率。

输入输出：
- 输入：观测序列、状态集合、初始概率、转移概率、发射概率；
- 输出：前向表、后向表、后验概率表，以及整条观测序列概率。

时间复杂度：O(T * S^2)
空间复杂度：O(T * S)

关键边界情况：
- 空观测返回空表和序列概率 1；
- 若观测序列概率为 0，则说明该序列在模型下不可达；
- 这是直接概率版教学实现，不额外做缩放或对数域运算。
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose


@dataclass(frozen=True)
class ForwardBackwardResult:
    """Forward-Backward 结果。"""

    forward: tuple[dict[str, float], ...]
    backward: tuple[dict[str, float], ...]
    posterior: tuple[dict[str, float], ...]
    sequence_probability: float


def forward_backward(
    observations: list[str],
    states: list[str],
    start_probability: dict[str, float],
    transition_probability: dict[str, dict[str, float]],
    emission_probability: dict[str, dict[str, float]],
) -> ForwardBackwardResult:
    """计算离散 HMM 的前向、后向和后验概率。

    参数：
    - observations：离散观测序列；
    - states：隐藏状态列表；
    - start_probability：初始状态分布；
    - transition_probability：状态转移概率；
    - emission_probability：状态发射概率。

    返回值：
    - `ForwardBackwardResult`，包含前向表、后向表、后验表和整序列概率。

    边界情况：
    - 空观测返回空概率表和序列概率 1；
    - 若某个观测使总概率变为 0，会抛出 `ValueError`。

    关键算法点：
    - 前向递推对所有前驱状态求和，表示“路径不再取最大，而是取总和”；
    - 后向递推与之对称，从右向左累积未来贡献。
    """

    _validate_hmm(
        states, start_probability, transition_probability, emission_probability
    )

    if not observations:
        return ForwardBackwardResult(
            forward=(), backward=(), posterior=(), sequence_probability=1.0
        )

    forward_table: list[dict[str, float]] = []
    first_forward: dict[str, float] = {}
    first_observation = observations[0]

    for state in states:
        first_forward[state] = start_probability.get(
            state, 0.0
        ) * emission_probability.get(state, {}).get(first_observation, 0.0)

    if sum(first_forward.values()) == 0.0:
        raise ValueError("首个观测在模型下不可达")

    forward_table.append(first_forward)

    for position in range(1, len(observations)):
        observation = observations[position]
        current_forward: dict[str, float] = {}

        for current_state in states:
            path_sum = 0.0
            for previous_state in states:
                path_sum += forward_table[position - 1][
                    previous_state
                ] * transition_probability.get(previous_state, {}).get(
                    current_state, 0.0
                )
            current_forward[current_state] = path_sum * emission_probability.get(
                current_state, {}
            ).get(observation, 0.0)

        if sum(current_forward.values()) == 0.0:
            raise ValueError(f"第 {position} 个观测在模型下不可达")

        forward_table.append(current_forward)

    backward_table: list[dict[str, float]] = [
        {state: 0.0 for state in states} for _ in observations
    ]
    for state in states:
        backward_table[-1][state] = 1.0

    for position in range(len(observations) - 2, -1, -1):
        next_observation = observations[position + 1]
        for state in states:
            suffix_sum = 0.0
            for next_state in states:
                suffix_sum += (
                    transition_probability.get(state, {}).get(next_state, 0.0)
                    * emission_probability.get(next_state, {}).get(
                        next_observation, 0.0
                    )
                    * backward_table[position + 1][next_state]
                )
            backward_table[position][state] = suffix_sum

    sequence_probability = sum(forward_table[-1].values())
    if sequence_probability == 0.0:
        raise ValueError("观测序列总概率为 0，无法计算后验")

    posterior_table: list[dict[str, float]] = []
    for position in range(len(observations)):
        posterior_row: dict[str, float] = {}
        row_total = 0.0

        for state in states:
            posterior_value = (
                forward_table[position][state] * backward_table[position][state]
            )
            posterior_row[state] = posterior_value
            row_total += posterior_value

        if row_total == 0.0:
            raise ValueError(f"第 {position} 个位置的后验归一化失败")

        for state in states:
            posterior_row[state] /= row_total

        posterior_table.append(posterior_row)

    return ForwardBackwardResult(
        forward=tuple(forward_table),
        backward=tuple(backward_table),
        posterior=tuple(posterior_table),
        sequence_probability=sequence_probability,
    )


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
        _validate_probability_row(
            transition_probability[state], f"状态 {state} 的转移概率"
        )
        _validate_probability_row(
            emission_probability[state], f"状态 {state} 的发射概率"
        )


def _validate_probability_row(probabilities: dict[str, float], row_name: str) -> None:
    """校验一行概率是否归一化。"""

    if not probabilities:
        raise ValueError(f"{row_name}不能为空")

    total = 0.0
    for label, probability in probabilities.items():
        if probability < 0.0 or probability > 1.0:
            raise ValueError(f"{row_name} 中 {label} 的概率必须位于 [0, 1]")
        total += probability

    if not isclose(total, 1.0, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError(f"{row_name} 之和必须为 1，当前为 {total}")


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

    result = forward_backward(
        ["ref", "ref", "alt", "alt", "alt"], hidden_states, start, transition, emission
    )
    assert result.sequence_probability > 0.0
    assert len(result.forward) == 5
    assert len(result.backward) == 5
    assert len(result.posterior) == 5

    for row in result.posterior:
        assert isclose(sum(row.values()), 1.0, rel_tol=1e-9, abs_tol=1e-9)

    assert max(result.posterior[0], key=result.posterior[0].get) == "RR"
    assert max(result.posterior[-1], key=result.posterior[-1].get) == "AA"

    empty = forward_backward([], hidden_states, start, transition, emission)
    assert empty.sequence_probability == 1.0
    assert empty.posterior == ()

    try:
        forward_backward(["unknown"], hidden_states, start, transition, emission)
        raise AssertionError("未知观测应导致不可达异常")
    except ValueError:
        pass

    print("033_forward_backward: all examples passed")
